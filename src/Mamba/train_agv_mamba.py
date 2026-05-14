"""
脚本名称: train_agv_mamba.py
版本: V1.0
最后修改时间: 2026-03-30

功能概述:
1) 使用 MambaAGVDataset 读取 Mamba_dataset_export.mat。
2) 支持在同一训练框架下切换 mamba1 / mamba2 / mamba3 三种骨干。
3) 进行多头训练:
   - 回归: y_theta, y_delta
   - 分类: y_main(3类), y_turn(3类), y_slip(2类), y_stall(2类)
4) 输出训练日志、验证损失，并保存 best checkpoint。
5) 输出异常头 (slip/stall) 的分类指标，并将每轮结果写入 history.jsonl。
6) 支持早停机制（默认 patience=5）。

使用示例:
python train_agv_mamba.py \
  --model mamba1 \
  --data /mnt/e/Matlab/Simulink/S-Function_16/data/mamba/Mamba_dataset_export.mat \
  --epochs 30 --batch-size 32 --lr 1e-3

python train_agv_mamba.py --model mamba2 --data /mnt/e/.../Mamba_dataset_export.mat
python train_agv_mamba.py --model mamba3 --data /mnt/e/.../Mamba_dataset_export.mat
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

try:
    import matplotlib
    matplotlib.use("Agg")  # 无显示器环境（WSL/Linux server）
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    _MATPLOTLIB_AVAILABLE = True
except ImportError:
    _MATPLOTLIB_AVAILABLE = False
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader

from mamba_dataset import MambaAGVDataset


# 将本地 mamba_ssm 源码路径加入 import 搜索路径
THIS_FILE = Path(__file__).resolve()
MAMBA_PKG_ROOT = THIS_FILE.parent / "model" / "mamba"
if str(MAMBA_PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(MAMBA_PKG_ROOT))

from mamba_ssm.modules.mamba_simple import Mamba  # type: ignore
from mamba_ssm.modules.mamba2 import Mamba2  # type: ignore

try:
    from mamba_ssm.modules.mamba3 import Mamba3  # type: ignore
except Exception:
    Mamba3 = None


@dataclass
class LossWeights:
    """多头损失权重。"""

    theta: float = 1.0
    delta: float = 1.0
    main: float = 1.0
    turn: float = 1.0
    slip: float = 1.0
    stall: float = 1.0


class ResidualMambaBlock(nn.Module):
    """
    函数名/类名: ResidualMambaBlock
    功能: 对 Mamba 系列层进行 PreNorm + Residual 封装。

    结构:
    - x -> LayerNorm -> MambaLayer -> Dropout -> Residual Add
    """

    def __init__(self, d_model: int, layer: nn.Module, dropout: float = 0.0):
        super().__init__()
        self.norm = nn.LayerNorm(d_model)
        self.layer = layer
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        y = self.layer(self.norm(x))
        y = self.dropout(y)
        return x + y


class AGVMambaMultiTaskModel(nn.Module):
    """
    函数名/类名: AGVMambaMultiTaskModel
    功能: AGV 时序多任务模型，骨干可切换 mamba1/mamba2/mamba3。

    输入:
    - x: [B, L, D_in]

    输出:
    - 字典形式多头输出，均为逐时间步预测。
    """

    def __init__(
        self,
        model_name: str,
        input_dim: int,
        d_model: int,
        n_layers: int,
        dropout: float,
        d_state: int,
        d_conv: int,
        expand: int,
        mamba3_headdim: int,
        mamba3_mimo: bool,
        mamba3_mimo_rank: int,
    ):
        super().__init__()

        self.model_name = model_name.lower()
        if self.model_name not in {"mamba1", "mamba2", "mamba3"}:
            raise ValueError(f"未知模型类型: {model_name}")

        if self.model_name == "mamba3" and Mamba3 is None:
            raise RuntimeError(
                "当前环境无法导入 Mamba3。请按 README 从源码安装支持 Mamba-3 的 mamba-ssm。"
            )

        self.in_proj = nn.Linear(input_dim, d_model)

        blocks = []
        for i in range(n_layers):
            if self.model_name == "mamba1":
                layer = Mamba(
                    d_model=d_model,
                    d_state=d_state,
                    d_conv=d_conv,
                    expand=expand,
                    layer_idx=i,
                )
            elif self.model_name == "mamba2":
                layer = Mamba2(
                    d_model=d_model,
                    d_state=d_state,
                    d_conv=d_conv,
                    expand=expand,
                    layer_idx=i,
                )
            else:
                layer = Mamba3(
                    d_model=d_model,
                    d_state=d_state,
                    headdim=mamba3_headdim,
                    is_mimo=mamba3_mimo,
                    mimo_rank=mamba3_mimo_rank,
                    layer_idx=i,
                )

            blocks.append(ResidualMambaBlock(d_model=d_model, layer=layer, dropout=dropout))

        self.blocks = nn.ModuleList(blocks)
        self.out_norm = nn.LayerNorm(d_model)

        # 回归头
        self.head_theta = nn.Linear(d_model, 1)
        self.head_delta = nn.Linear(d_model, 1)

        # 分类头
        self.head_main = nn.Linear(d_model, 3)   # 1/2/3 -> 0/1/2
        self.head_turn = nn.Linear(d_model, 3)   # -1/0/1 -> 0/1/2
        self.head_slip = nn.Linear(d_model, 2)   # 0/1
        self.head_stall = nn.Linear(d_model, 2)  # 0/1

    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        h = self.in_proj(x)
        for blk in self.blocks:
            h = blk(h)
        h = self.out_norm(h)

        return {
            "theta": self.head_theta(h).squeeze(-1),
            "delta": self.head_delta(h).squeeze(-1),
            "main": self.head_main(h),
            "turn": self.head_turn(h),
            "slip": self.head_slip(h),
            "stall": self.head_stall(h),
        }


def set_seed(seed: int) -> None:
    """固定随机种子，提升复现性。"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def flatten_logits_and_targets(
    logits: torch.Tensor, targets: torch.Tensor
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    将逐时间步分类输出展平到 CE 可用形状。

    输入:
    - logits: [B, L, C]
    - targets: [B, L]

    返回:
    - logits_2d: [B*L, C]
    - targets_1d: [B*L]
    """
    b, l, c = logits.shape
    return logits.reshape(b * l, c), targets.reshape(b * l)


def compute_multitask_loss(
    outputs: Dict[str, torch.Tensor],
    batch: Dict[str, torch.Tensor],
    loss_w: LossWeights,
) -> Tuple[torch.Tensor, Dict[str, float]]:
    """
    计算多头损失并返回总损失与分量损失。

    标签映射规则:
    - y_main: 原值 1/2/3 -> 0/1/2
    - y_turn: 原值 -1/0/1 -> 0/1/2
    - y_slip/y_stall: 0/1 保持不变
    """
    y_theta = batch["y_theta"]
    y_delta = batch["y_delta"]

    y_main = batch["y_main"] - 1
    y_turn = batch["y_turn"] + 1
    y_slip = batch["y_slip"]
    y_stall = batch["y_stall"]

    loss_theta = F.mse_loss(outputs["theta"], y_theta)
    loss_delta = F.mse_loss(outputs["delta"], y_delta)

    main_logits, main_targets = flatten_logits_and_targets(outputs["main"], y_main)
    turn_logits, turn_targets = flatten_logits_and_targets(outputs["turn"], y_turn)
    slip_logits, slip_targets = flatten_logits_and_targets(outputs["slip"], y_slip)
    stall_logits, stall_targets = flatten_logits_and_targets(outputs["stall"], y_stall)

    loss_main = F.cross_entropy(main_logits, main_targets)

    # turn 头：右转严重少数类（~4-5%），用类别权重惩罚漏报
    # weight 顺序对应训练标签 0=right(-1), 1=straight(0), 2=left(1)
    turn_class_weight = getattr(loss_w, "turn_class_weight", None)
    if turn_class_weight is not None:
        turn_cw = torch.tensor(turn_class_weight, dtype=torch.float32, device=turn_logits.device)
        loss_turn = F.cross_entropy(turn_logits, turn_targets, weight=turn_cw)
    else:
        loss_turn = F.cross_entropy(turn_logits, turn_targets)

    # slip 头：打滑正样本稀少，用类别权重惩罚漏报
    # weight 顺序对应训练标签 0=normal, 1=slip
    slip_class_weight = getattr(loss_w, "slip_class_weight", None)
    if slip_class_weight is not None:
        slip_cw = torch.tensor(slip_class_weight, dtype=torch.float32, device=slip_logits.device)
        loss_slip = F.cross_entropy(slip_logits, slip_targets, weight=slip_cw)
    else:
        loss_slip = F.cross_entropy(slip_logits, slip_targets)

    # stall 头：堵转正样本极稀少，用类别权重惩罚漏报
    # weight 顺序对应训练标签 0=normal, 1=stall
    stall_class_weight = getattr(loss_w, "stall_class_weight", None)
    if stall_class_weight is not None:
        stall_cw = torch.tensor(stall_class_weight, dtype=torch.float32, device=stall_logits.device)
        loss_stall = F.cross_entropy(stall_logits, stall_targets, weight=stall_cw)
    else:
        loss_stall = F.cross_entropy(stall_logits, stall_targets)

    total = (
        loss_w.theta * loss_theta
        + loss_w.delta * loss_delta
        + loss_w.main * loss_main
        + loss_w.turn * loss_turn
        + loss_w.slip * loss_slip
        + loss_w.stall * loss_stall
    )

    logs = {
        "loss_total": float(total.detach().item()),
        "loss_theta": float(loss_theta.detach().item()),
        "loss_delta": float(loss_delta.detach().item()),
        "loss_main": float(loss_main.detach().item()),
        "loss_turn": float(loss_turn.detach().item()),
        "loss_slip": float(loss_slip.detach().item()),
        "loss_stall": float(loss_stall.detach().item()),
    }
    return total, logs


def move_batch_to_device(batch: Dict[str, torch.Tensor], device: torch.device) -> Dict[str, torch.Tensor]:
    """将 batch 张量迁移到目标设备。"""
    out = {}
    for k, v in batch.items():
        out[k] = v.to(device, non_blocking=True)
    return out


def init_binary_counter() -> Dict[str, int]:
    """初始化二分类混淆矩阵计数器。"""
    return {"tp": 0, "fp": 0, "tn": 0, "fn": 0}


def update_binary_counter(counter: Dict[str, int], logits: torch.Tensor, targets: torch.Tensor) -> None:
    """
    使用一个 batch 的预测结果更新二分类计数器。

    参数:
    - logits: [B, L, 2]
    - targets: [B, L]，标签取值 0/1
    """
    pred = torch.argmax(logits.detach(), dim=-1)
    tgt = targets.detach().long()

    pred_flat = pred.reshape(-1)
    tgt_flat = tgt.reshape(-1)

    tp = ((pred_flat == 1) & (tgt_flat == 1)).sum().item()
    fp = ((pred_flat == 1) & (tgt_flat == 0)).sum().item()
    tn = ((pred_flat == 0) & (tgt_flat == 0)).sum().item()
    fn = ((pred_flat == 0) & (tgt_flat == 1)).sum().item()

    counter["tp"] += int(tp)
    counter["fp"] += int(fp)
    counter["tn"] += int(tn)
    counter["fn"] += int(fn)


def binary_metrics_from_counter(counter: Dict[str, int], prefix: str) -> Dict[str, float]:
    """从二分类混淆矩阵计数器计算常见指标。"""
    tp = float(counter["tp"])
    fp = float(counter["fp"])
    tn = float(counter["tn"])
    fn = float(counter["fn"])

    total = tp + fp + tn + fn
    acc = (tp + tn) / total if total > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2.0 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0

    return {
        f"{prefix}_acc": acc,
        f"{prefix}_precision": precision,
        f"{prefix}_recall": recall,
        f"{prefix}_f1": f1,
        f"{prefix}_fpr": fpr,
        f"{prefix}_fnr": fnr,
        f"{prefix}_tp": tp,
        f"{prefix}_fp": fp,
        f"{prefix}_tn": tn,
        f"{prefix}_fn": fn,
    }


def plot_training_curves(history_path: Path, save_dir: Path) -> None:
    """Parse history.jsonl and save a publication-quality training convergence figure.

    Layout (3 rows x 1 col):
      Row 1 – Total loss:      train_total vs val_total
      Row 2 – Component val losses: theta / delta (regression) + main / turn (classification)
      Row 3 – Key metrics:     val slip-F1 and stall-F1
    """
    if not _MATPLOTLIB_AVAILABLE:
        print("[plot_training_curves] matplotlib 未安装，跳过绘图。可运行: pip install matplotlib")
        return

    records = []
    try:
        with open(history_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
    except Exception as exc:
        print(f"[plot_training_curves] Cannot read {history_path}: {exc}")
        return

    if not records:
        return

    epochs      = [r["epoch"]                    for r in records]
    tr_total    = [r["train"]["loss_total"]       for r in records]
    val_total   = [r["val"]["loss_total"]         for r in records]
    val_theta   = [r["val"]["loss_theta"]         for r in records]
    val_delta   = [r["val"]["loss_delta"]         for r in records]
    val_main    = [r["val"]["loss_main"]          for r in records]
    val_turn    = [r["val"]["loss_turn"]          for r in records]
    val_slip_f1  = [r["val"].get("slip_f1",  0.0) for r in records]
    val_stall_f1 = [r["val"].get("stall_f1", 0.0) for r in records]

    # 找 best val epoch
    best_epoch = epochs[int(np.argmin(val_total))]

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(3, 1, figsize=(8, 11), dpi=300,
                             gridspec_kw={"hspace": 0.45})
    fig.suptitle("Mamba2 AGV Multi-task Training Convergence",
                 fontsize=14, fontweight="bold", y=0.99)

    # ── Row 1: total loss ───────────────────────────────────────────────────
    ax = axes[0]
    ax.plot(epochs, tr_total,  color="#2196F3", lw=1.8, marker="o", ms=3,
            label="Train – total loss")
    ax.plot(epochs, val_total, color="#F44336", lw=1.8, marker="s", ms=3,
            label="Val – total loss")
    ax.axvline(best_epoch, color="gray", lw=1.2, ls="--", alpha=0.7,
               label=f"Best epoch ({best_epoch})")
    ax.set_ylabel("Total Loss")
    ax.set_title("(a) Training & Validation Total Loss", loc="left", fontsize=11)
    ax.legend(fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.4f"))

    # ── Row 2: component val losses ─────────────────────────────────────────
    ax = axes[1]
    ax.plot(epochs, val_theta, lw=1.5, color="#9C27B0",
            label=r"Val $\theta$ loss (regression)")
    ax.plot(epochs, val_delta, lw=1.5, color="#673AB7", ls="--",
            label=r"Val $\delta$ loss (regression)")
    ax.plot(epochs, val_main,  lw=1.5, color="#FF9800",
            label="Val main-state cls")
    ax.plot(epochs, val_turn,  lw=1.5, color="#FF5722", ls="--",
            label="Val turn cls")
    ax.axvline(best_epoch, color="gray", lw=1.2, ls="--", alpha=0.7)
    ax.set_ylabel("Component Loss")
    ax.set_title("(b) Validation Component Losses", loc="left", fontsize=11)
    ax.legend(fontsize=9, ncol=2)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.4f"))

    # ── Row 3: classification metrics ───────────────────────────────────────
    ax = axes[2]
    ax.plot(epochs, val_slip_f1,  color="#4CAF50", lw=1.8, marker="^", ms=4,
            label="Val slip F1")
    ax.plot(epochs, val_stall_f1, color="#FF5722", lw=1.8, marker="v", ms=4,
            label="Val stall F1")
    ax.axvline(best_epoch, color="gray", lw=1.2, ls="--", alpha=0.7,
               label=f"Best epoch ({best_epoch})")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("F1 Score")
    ax.set_ylim([-0.02, 1.05])
    ax.set_title("(c) Anomaly Detection Metrics (Slip & Stall F1)", loc="left", fontsize=11)
    ax.legend(fontsize=9)

    for ax in axes:
        ax.set_xlim([epochs[0] - 0.5, epochs[-1] + 0.5])
        ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    out_path = save_dir / "training_curve.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[Training curve] saved → {out_path}")


def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    scaler: torch.amp.GradScaler,
    device: torch.device,
    loss_w: LossWeights,
    use_amp: bool,
    grad_clip: float,
) -> Dict[str, float]:
    """训练 1 个 epoch，返回平均损失日志。"""
    model.train()

    meter = {
        "loss_total": 0.0,
        "loss_theta": 0.0,
        "loss_delta": 0.0,
        "loss_main": 0.0,
        "loss_turn": 0.0,
        "loss_slip": 0.0,
        "loss_stall": 0.0,
    }
    slip_counter = init_binary_counter()
    stall_counter = init_binary_counter()

    amp_device = "cuda" if device.type == "cuda" else "cpu"

    n_steps = 0
    for batch in loader:
        batch = move_batch_to_device(batch, device)
        optimizer.zero_grad(set_to_none=True)

        with torch.amp.autocast(device_type=amp_device, enabled=use_amp):
            outputs = model(batch["x"])
            loss, logs = compute_multitask_loss(outputs, batch, loss_w)

        update_binary_counter(slip_counter, outputs["slip"], batch["y_slip"])
        update_binary_counter(stall_counter, outputs["stall"], batch["y_stall"])

        if use_amp:
            scaler.scale(loss).backward()
            if grad_clip > 0:
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            if grad_clip > 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
            optimizer.step()

        n_steps += 1
        for k in meter:
            meter[k] += logs[k]

    for k in meter:
        meter[k] /= max(n_steps, 1)
    meter.update(binary_metrics_from_counter(slip_counter, "slip"))
    meter.update(binary_metrics_from_counter(stall_counter, "stall"))
    return meter


@torch.no_grad()
def evaluate(
    model: nn.Module,
    loader: DataLoader,
    device: torch.device,
    loss_w: LossWeights,
    use_amp: bool,
) -> Dict[str, float]:
    """验证 1 个 epoch，返回平均损失日志。"""
    model.eval()

    meter = {
        "loss_total": 0.0,
        "loss_theta": 0.0,
        "loss_delta": 0.0,
        "loss_main": 0.0,
        "loss_turn": 0.0,
        "loss_slip": 0.0,
        "loss_stall": 0.0,
    }
    slip_counter = init_binary_counter()
    stall_counter = init_binary_counter()

    amp_device = "cuda" if device.type == "cuda" else "cpu"

    n_steps = 0
    for batch in loader:
        batch = move_batch_to_device(batch, device)
        with torch.amp.autocast(device_type=amp_device, enabled=use_amp):
            outputs = model(batch["x"])
            _, logs = compute_multitask_loss(outputs, batch, loss_w)

        update_binary_counter(slip_counter, outputs["slip"], batch["y_slip"])
        update_binary_counter(stall_counter, outputs["stall"], batch["y_stall"])

        n_steps += 1
        for k in meter:
            meter[k] += logs[k]

    for k in meter:
        meter[k] /= max(n_steps, 1)
    meter.update(binary_metrics_from_counter(slip_counter, "slip"))
    meter.update(binary_metrics_from_counter(stall_counter, "stall"))
    return meter


def build_dataloaders(data_path: str, batch_size: int, num_workers: int) -> Tuple[DataLoader, DataLoader]:
    """构建 train/val DataLoader。

    WSL2 兼容性说明:
      WSL2 的进程间通信限制会导致 num_workers>0 + pin_memory=True 组合时
      DataLoader worker 被 SIGABRT 杀掉（LLVM pthread_join 错误）。
      解决方案: 强制 num_workers=0（主进程加载），pin_memory 仅在非 WSL 环境启用。
    """
    import platform, os
    _is_wsl = "microsoft" in platform.uname().release.lower() or \
              os.path.exists("/proc/sys/fs/binfmt_misc/WSLInterop")
    _safe_workers = 0 if _is_wsl else num_workers
    _pin = (not _is_wsl)

    train_ds = MambaAGVDataset(data_path, split="train")
    val_ds = MambaAGVDataset(data_path, split="val")

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        shuffle=True,
        num_workers=_safe_workers,
        pin_memory=_pin,
        drop_last=False,
    )

    val_loader = DataLoader(
        val_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=_safe_workers,
        pin_memory=_pin,
        drop_last=False,
    )

    return train_loader, val_loader


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    p = argparse.ArgumentParser(description="Train AGV Mamba with mamba1/mamba2/mamba3")

    p.add_argument("--model", type=str, default="mamba1", choices=["mamba1", "mamba2", "mamba3"])
    p.add_argument("--data", type=str, required=True, help="Path to Mamba_dataset_export.mat")

    p.add_argument("--epochs", type=int, default=30)
    p.add_argument("--batch-size", type=int, default=32)
    p.add_argument("--num-workers", type=int, default=2)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--weight-decay", type=float, default=1e-4)
    p.add_argument("--seed", type=int, default=42)

    p.add_argument("--d-model", type=int, default=128)
    p.add_argument("--n-layers", type=int, default=4)
    p.add_argument("--dropout", type=float, default=0.1)
    p.add_argument("--d-state", type=int, default=64)
    p.add_argument("--d-conv", type=int, default=4)
    p.add_argument("--expand", type=int, default=2)

    p.add_argument("--mamba3-headdim", type=int, default=64)
    p.add_argument("--mamba3-mimo", action="store_true")
    p.add_argument("--mamba3-mimo-rank", type=int, default=4)

    p.add_argument("--w-theta", type=float, default=1.0)
    p.add_argument("--w-delta", type=float, default=1.0)
    p.add_argument("--w-main", type=float, default=1.0)
    p.add_argument("--w-turn", type=float, default=1.0)
    p.add_argument("--w-slip", type=float, default=1.0)
    p.add_argument("--w-stall", type=float, default=1.0)
    # 类别权重（解决少数类不平衡）
    # turn-right-weight: 右转类的惩罚倍率（相对于直行=1.0），默认 10.0
    # slip-pos-weight:   slip=1 类的惩罚倍率（相对于 normal=1.0），默认 8.0
    p.add_argument("--turn-right-weight", type=float, default=10.0,
                   help="Class weight for right-turn (label=0 in training). Default 10.0")
    p.add_argument("--slip-pos-weight", type=float, default=8.0,
                   help="Class weight for slip=1. Default 8.0")
    p.add_argument("--stall-pos-weight", type=float, default=15.0,
                   help="Class weight for stall=1. Default 15.0")

    p.add_argument("--grad-clip", type=float, default=1.0)
    p.add_argument("--no-amp", action="store_true", help="Disable mixed precision")
    p.add_argument("--early-stop-patience", type=int, default=5, help="Early stop patience (epochs)")

    p.add_argument("--save-root", type=str, default="results/mamba/train")
    p.add_argument("--exp-name", type=str, default="")

    return p.parse_args()


def main() -> None:
    """训练主函数。"""
    args = parse_args()
    set_seed(args.seed)

    if not os.path.exists(args.data):
        raise FileNotFoundError(f"数据文件不存在: {args.data}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    use_amp = (device.type == "cuda") and (not args.no_amp)

    tstamp = time.strftime("%Y%m%d_%H%M%S")
    exp_name = args.exp_name.strip() or f"{args.model}_dm{args.d_model}_nl{args.n_layers}_{tstamp}"
    save_dir = Path(args.save_root) / exp_name
    save_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 72)
    print(f"[Info] Device: {device}")
    print(f"[Info] Model : {args.model}")
    print(f"[Info] Data  : {args.data}")
    print(f"[Info] Save  : {save_dir}")
    print("=" * 72)

    train_loader, val_loader = build_dataloaders(
        data_path=args.data,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
    )

    model = AGVMambaMultiTaskModel(
        model_name=args.model,
        input_dim=10,
        d_model=args.d_model,
        n_layers=args.n_layers,
        dropout=args.dropout,
        d_state=args.d_state,
        d_conv=args.d_conv,
        expand=args.expand,
        mamba3_headdim=args.mamba3_headdim,
        mamba3_mimo=args.mamba3_mimo,
        mamba3_mimo_rank=args.mamba3_mimo_rank,
    ).to(device)

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=args.lr,
        weight_decay=args.weight_decay,
    )

    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=max(args.epochs, 1))

    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)

    loss_w = LossWeights(
        theta=args.w_theta,
        delta=args.w_delta,
        main=args.w_main,
        turn=args.w_turn,
        slip=args.w_slip,
        stall=args.w_stall,
    )
    # 挂载类别权重到 loss_w（顺序：right=0, straight=1, left=2）
    loss_w.turn_class_weight = [args.turn_right_weight, 1.0, 1.0]
    # 挂载 slip 类别权重（normal=0, slip=1）
    loss_w.slip_class_weight = [1.0, args.slip_pos_weight]
    # 挂载 stall 类别权重（normal=0, stall=1）
    loss_w.stall_class_weight = [1.0, args.stall_pos_weight]

    config_path = save_dir / "config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(vars(args), f, ensure_ascii=False, indent=2)

    best_val = float("inf")
    no_improve = 0
    best_ckpt = save_dir / "best.pt"
    last_ckpt = save_dir / "last.pt"
    history_path = save_dir / "history.jsonl"

    for epoch in range(1, args.epochs + 1):
        train_logs = train_one_epoch(
            model=model,
            loader=train_loader,
            optimizer=optimizer,
            scaler=scaler,
            device=device,
            loss_w=loss_w,
            use_amp=use_amp,
            grad_clip=args.grad_clip,
        )

        val_logs = evaluate(
            model=model,
            loader=val_loader,
            device=device,
            loss_w=loss_w,
            use_amp=use_amp,
        )

        scheduler.step()

        lr_cur = optimizer.param_groups[0]["lr"]
        print(
            f"Epoch {epoch:03d}/{args.epochs:03d} | "
            f"lr={lr_cur:.3e} | "
            f"train_total={train_logs['loss_total']:.4f} | "
            f"val_total={val_logs['loss_total']:.4f} | "
            f"val_slip_f1={val_logs['slip_f1']:.4f} | "
            f"val_stall_f1={val_logs['stall_f1']:.4f}"
        )

        epoch_record = {
            "epoch": epoch,
            "lr": lr_cur,
            "train": train_logs,
            "val": val_logs,
        }
        with open(history_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(epoch_record, ensure_ascii=False) + "\n")

        state = {
            "epoch": epoch,
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "scheduler": scheduler.state_dict(),
            "train_logs": train_logs,
            "val_logs": val_logs,
            "args": vars(args),
        }
        torch.save(state, last_ckpt)

        if val_logs["loss_total"] < best_val:
            best_val = val_logs["loss_total"]
            no_improve = 0
            torch.save(state, best_ckpt)
            print(f"  -> New best val_total: {best_val:.4f}, saved to {best_ckpt}")
        else:
            no_improve += 1
            if args.early_stop_patience > 0 and no_improve >= args.early_stop_patience:
                print(f"  -> Early stopping triggered (patience={args.early_stop_patience}).")
                break

    # DataLoader 内部持有 HDF5 句柄，训练结束后尽量显式释放
    if hasattr(train_loader.dataset, "close"):
        train_loader.dataset.close()
    if hasattr(val_loader.dataset, "close"):
        val_loader.dataset.close()

    print("=" * 72)
    print("Training finished.")
    print(f"Best val_total: {best_val:.6f}")
    print(f"Best checkpoint: {best_ckpt}")
    print("=" * 72)

    # 训练收敛曲线可视化（论文用图）
    plot_training_curves(history_path, save_dir)

    # 自动导出 mu_sigma.npz 到实验目录，避免启动推理服务时手动提取
    try:
        import h5py  # type: ignore
        _npz_path = save_dir / "mu_sigma.npz"
        with h5py.File(args.data, "r") as _f:
            _mu    = np.array(_f["mu"]).squeeze()
            _sigma = np.array(_f["sigma"]).squeeze()
        np.savez(str(_npz_path), mu=_mu, sigma=_sigma)
        print(f"[mu_sigma] 已保存 -> {_npz_path}")
    except Exception as _e:
        print(f"[mu_sigma] 导出失败（不影响训练结果）: {_e}")


if __name__ == "__main__":
    main()
