"""训练 ModernTCN-small，并输出与 TCN/GRU baseline 对齐的测试指标。

使用方式：
    python ModernTCN/train_modern_tcn.py --seed 42

重要约束：
    1. 默认读取 data/tcn/ModernTCN_dataset_v4_industrial.mat。
    2. 不重新划分 split，不重新拟合 scaler。
    3. 多 seed 实验建议通过 results/modern_tcn/scripts 下的脚本统一启动。
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import time
from pathlib import Path
from typing import Dict, Iterable, Tuple

import numpy as np
import torch
from torch.utils.data import DataLoader

from modern_tcn_data import AGVWindowDataset, class_weights, find_project_root, load_modern_tcn_dataset
from modern_tcn_metrics import compute_metrics, metric_row, multitask_loss, seed42_gate, selection_score
from modern_tcn_model import ModernTCNConfig, ModernTCNSmall


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="ModernTCN-small 第一阶段训练脚本")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--dataset-file", type=str, default="")
    p.add_argument("--run-tag", type=str, default="")
    p.add_argument("--epochs", type=int, default=120)
    p.add_argument("--batch-size", type=int, default=256)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--weight-decay", type=float, default=1e-4)
    p.add_argument("--patience", type=int, default=25)
    p.add_argument("--min-epochs", type=int, default=30)
    p.add_argument("--channels", type=int, default=64)
    p.add_argument("--blocks", type=int, default=5)
    p.add_argument("--kernel-size", type=int, default=31)
    p.add_argument("--dropout", type=float, default=0.15)
    p.add_argument("--turn-head-source", type=str, default="full", choices=["full", "inputstats", "kinematic_stats"])
    p.add_argument("--lambda-turn", type=float, default=0.05)
    p.add_argument("--lambda-theta", type=float, default=0.35)
    p.add_argument("--lambda-theta-flat", type=float, default=0.20)
    p.add_argument(
        "--theta-flat-loss-mode",
        type=str,
        default="near_zero",
        choices=["near_zero", "true_zero", "near_flat", "main_flat", "none"],
    )
    p.add_argument("--theta-flat-zero-tol-deg", type=float, default=0.3)
    p.add_argument("--lambda-theta-near-flat", type=float, default=0.0)
    p.add_argument("--theta-near-flat-deg", type=float, default=0.5)
    p.add_argument("--lambda-theta-error-excess", type=float, default=0.0)
    p.add_argument("--lambda-theta-flat-excess", type=float, default=0.0)
    p.add_argument("--lambda-theta-near-flat-excess", type=float, default=0.0)
    p.add_argument("--lambda-theta-true-zero-excess", type=float, default=0.0)
    p.add_argument("--lambda-theta-active-excess", type=float, default=0.0)
    p.add_argument("--lambda-theta-small-neg", type=float, default=0.0)
    p.add_argument("--lambda-theta-small-neg-excess", type=float, default=0.0)
    p.add_argument("--theta-excess-target-deg", type=float, default=1.0)
    p.add_argument("--theta-flat-excess-target-deg", type=float, default=0.5)
    p.add_argument("--theta-small-neg-min-deg", type=float, default=-4.0)
    p.add_argument("--theta-small-neg-max-deg", type=float, default=-2.0)
    p.add_argument("--theta-gate-mode", type=str, default="none", choices=["none", "main_slope_prob"])
    p.add_argument("--theta-gate-power", type=float, default=1.0)
    p.add_argument("--theta-gate-floor", type=float, default=0.0)
    p.add_argument("--theta-neg-weight", type=float, default=1.0)
    p.add_argument("--theta-pos-weight", type=float, default=1.0)
    p.add_argument("--turn-transition-weight", type=float, default=1.0)
    p.add_argument("--turn-class-multipliers", type=float, nargs=3, default=[1.00, 1.10, 1.00])
    p.add_argument("--select-turn-weight", type=float, default=0.30)
    p.add_argument("--select-turn-transition-weight", type=float, default=1.00)
    p.add_argument("--select-turn-transition-target", type=float, default=0.75)
    p.add_argument("--select-turn-left-weight", type=float, default=0.00)
    p.add_argument("--select-turn-left-target", type=float, default=0.80)
    p.add_argument("--select-turn-lr-weight", type=float, default=0.00)
    p.add_argument("--select-turn-lr-target", type=float, default=0.80)
    p.add_argument("--select-theta-weight", type=float, default=0.15)
    p.add_argument("--select-theta-ref-deg", type=float, default=5.0)
    p.add_argument("--select-theta-p95-weight", type=float, default=0.0)
    p.add_argument("--select-theta-p95-target-deg", type=float, default=1.0)
    p.add_argument("--select-theta-flat-p95-weight", type=float, default=0.0)
    p.add_argument("--select-theta-flat-p95-target-deg", type=float, default=1.0)
    p.add_argument("--select-theta-near-flat-p95-weight", type=float, default=0.0)
    p.add_argument("--select-theta-near-flat-p95-target-deg", type=float, default=1.0)
    p.add_argument("--select-theta-true-zero-p95-weight", type=float, default=0.0)
    p.add_argument("--select-theta-true-zero-p95-target-deg", type=float, default=1.0)
    p.add_argument("--select-theta-extreme-p95-weight", type=float, default=0.0)
    p.add_argument("--select-theta-extreme-p95-target-deg", type=float, default=1.0)
    p.add_argument("--select-theta-edge-p95-weight", type=float, default=0.0)
    p.add_argument("--select-theta-edge-p95-target-deg", type=float, default=1.2)
    p.add_argument("--select-theta-small-nonzero-p95-weight", type=float, default=0.0)
    p.add_argument("--select-theta-small-nonzero-p95-target-deg", type=float, default=1.0)
    p.add_argument("--select-theta-flat-bias-weight", type=float, default=0.0)
    p.add_argument("--select-theta-flat-bias-target-deg", type=float, default=0.2)
    p.add_argument("--device", type=str, default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--num-workers", type=int, default=0)
    p.add_argument("--limit-train", type=int, default=0, help="仅用于 smoke test，正式实验必须为 0。")
    p.add_argument("--limit-val", type=int, default=0, help="仅用于 smoke test，正式实验必须为 0。")
    p.add_argument("--limit-test", type=int, default=0, help="仅用于 smoke test，正式实验必须为 0。")
    p.add_argument("--dry-run", action="store_true", help="只读取数据并跑一次前向，不保存训练结果。")
    return p.parse_args()


def main() -> Dict[str, object]:
    args = parse_args()
    return train_one_seed(args)


def train_one_seed(args: argparse.Namespace) -> Dict[str, object]:
    root = find_project_root()
    run_tag = args.run_tag or f"modern_tcn_v4_industrial_seed{args.seed}"
    out_dir = root / "results" / "modern_tcn" / run_tag
    dataset_file = Path(args.dataset_file) if args.dataset_file else None

    _set_seed(args.seed)
    device = _select_device(args.device)
    data = load_modern_tcn_dataset(
        dataset_file=dataset_file,
        limit_train=args.limit_train,
        limit_val=args.limit_val,
        limit_test=args.limit_test,
    )
    train_split = data["train"]
    val_split = data["val"]
    test_split = data["test"]
    contract = data["contract"]

    cfg = ModernTCNConfig(
        input_dim=contract.input_dim,
        seq_len=contract.seq_len,
        channels=args.channels,
        blocks=args.blocks,
        kernel_size=args.kernel_size,
        dropout=args.dropout,
        turn_head_source=args.turn_head_source,
        lambda_turn=args.lambda_turn,
        lambda_theta=args.lambda_theta,
        lambda_theta_flat=args.lambda_theta_flat,
        theta_flat_loss_mode=args.theta_flat_loss_mode,
        theta_flat_zero_tol_deg=args.theta_flat_zero_tol_deg,
        lambda_theta_near_flat=args.lambda_theta_near_flat,
        theta_near_flat_deg=args.theta_near_flat_deg,
        lambda_theta_error_excess=args.lambda_theta_error_excess,
        lambda_theta_flat_excess=args.lambda_theta_flat_excess,
        lambda_theta_near_flat_excess=args.lambda_theta_near_flat_excess,
        lambda_theta_true_zero_excess=args.lambda_theta_true_zero_excess,
        lambda_theta_active_excess=args.lambda_theta_active_excess,
        lambda_theta_small_neg=args.lambda_theta_small_neg,
        lambda_theta_small_neg_excess=args.lambda_theta_small_neg_excess,
        theta_excess_target_deg=args.theta_excess_target_deg,
        theta_flat_excess_target_deg=args.theta_flat_excess_target_deg,
        theta_small_neg_min_deg=args.theta_small_neg_min_deg,
        theta_small_neg_max_deg=args.theta_small_neg_max_deg,
        theta_gate_mode=args.theta_gate_mode,
        theta_gate_power=args.theta_gate_power,
        theta_gate_floor=args.theta_gate_floor,
        theta_neg_weight=args.theta_neg_weight,
        theta_pos_weight=args.theta_pos_weight,
        turn_transition_weight=args.turn_transition_weight,
        turn_class_multipliers=tuple(args.turn_class_multipliers),
        select_turn_weight=args.select_turn_weight,
        select_turn_transition_weight=args.select_turn_transition_weight,
        select_turn_transition_target=getattr(args, "select_turn_transition_target", 0.75),
        select_turn_left_weight=args.select_turn_left_weight,
        select_turn_left_target=args.select_turn_left_target,
        select_turn_lr_weight=getattr(args, "select_turn_lr_weight", 0.0),
        select_turn_lr_target=getattr(args, "select_turn_lr_target", 0.80),
        select_theta_weight=args.select_theta_weight,
        select_theta_ref_deg=args.select_theta_ref_deg,
        select_theta_p95_weight=args.select_theta_p95_weight,
        select_theta_p95_target_deg=getattr(args, "select_theta_p95_target_deg", 1.0),
        select_theta_flat_p95_weight=args.select_theta_flat_p95_weight,
        select_theta_flat_p95_target_deg=getattr(args, "select_theta_flat_p95_target_deg", 1.0),
        select_theta_near_flat_p95_weight=args.select_theta_near_flat_p95_weight,
        select_theta_near_flat_p95_target_deg=getattr(args, "select_theta_near_flat_p95_target_deg", 1.0),
        select_theta_true_zero_p95_weight=args.select_theta_true_zero_p95_weight,
        select_theta_true_zero_p95_target_deg=getattr(args, "select_theta_true_zero_p95_target_deg", 1.0),
        select_theta_extreme_p95_weight=args.select_theta_extreme_p95_weight,
        select_theta_extreme_p95_target_deg=getattr(args, "select_theta_extreme_p95_target_deg", 1.0),
        select_theta_edge_p95_weight=getattr(args, "select_theta_edge_p95_weight", 0.0),
        select_theta_edge_p95_target_deg=getattr(args, "select_theta_edge_p95_target_deg", 1.2),
        select_theta_small_nonzero_p95_weight=args.select_theta_small_nonzero_p95_weight,
        select_theta_small_nonzero_p95_target_deg=getattr(args, "select_theta_small_nonzero_p95_target_deg", 1.0),
        select_theta_flat_bias_weight=args.select_theta_flat_bias_weight,
        select_theta_flat_bias_target_deg=getattr(args, "select_theta_flat_bias_target_deg", 0.2),
    )
    model = ModernTCNSmall(cfg).to(device)

    # smoke test 只验证数据契约和模型维度，不写任何模型文件。
    if args.dry_run:
        xb = torch.from_numpy(train_split.X[:4]).float().to(device)
        with torch.no_grad():
            outputs = model(xb)
        print("[ModernTCN dry-run] 数据和模型前向检查通过")
        print(f"  X: {tuple(xb.shape)}")
        print(f"  logits_main/logits_turn/theta: {[tuple(o.shape) for o in outputs]}")
        return {"status": "dry_run_ok"}

    out_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_file = out_dir / f"modern_tcn_seed{args.seed}.pt"
    summary_csv = out_dir / f"modern_tcn_seed{args.seed}_summary.csv"
    history_csv = out_dir / f"modern_tcn_seed{args.seed}_history.csv"
    report_file = out_dir / "ModernTCN_train_report.md"

    train_loader = DataLoader(
        AGVWindowDataset(train_split),
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        pin_memory=(device.type == "cuda"),
    )
    val_loader = DataLoader(AGVWindowDataset(val_split), batch_size=args.batch_size, shuffle=False, num_workers=0)
    test_loader = DataLoader(AGVWindowDataset(test_split), batch_size=args.batch_size, shuffle=False, num_workers=0)

    class_w_main = class_weights(
        train_split.y_main,
        3,
        cfg.main_class_weight_method,
        list(cfg.main_class_multipliers),
    ).to(device)
    class_w_turn = class_weights(
        train_split.y_turn,
        3,
        cfg.turn_class_weight_method,
        list(cfg.turn_class_multipliers),
    ).to(device)

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=max(args.epochs, 1))

    print("[ModernTCN] 第一阶段训练开始")
    print(f"  seed={args.seed}, device={device}, out={out_dir}")
    print(f"  dataset={contract.dataset_file}")
    print(f"  train/val/test={len(train_split.X)}/{len(val_split.X)}/{len(test_split.X)}")
    print(f"  model channels={cfg.channels}, blocks={cfg.blocks}, kernel={cfg.kernel_size}")

    best_score = math.inf
    best_epoch = 0
    best_state = None
    best_val_metrics: Dict[str, object] = {}
    patience_count = 0
    history_rows = []
    t0 = time.time()

    for epoch in range(1, args.epochs + 1):
        train_loss = _train_epoch(model, train_loader, opt, device, class_w_main, class_w_turn, cfg)
        scheduler.step()
        val_loss, val_logits_main, val_logits_turn, val_theta = _predict_full(
            model, val_loader, val_split, device, class_w_main, class_w_turn, cfg
        )
        val_metrics = compute_metrics(val_logits_main, val_logits_turn, val_theta, val_split, val_loss)
        score = selection_score(val_metrics, cfg)
        history_rows.append(_history_row(epoch, opt.param_groups[0]["lr"], train_loss, val_metrics, score))

        if score < best_score:
            best_score = score
            best_epoch = epoch
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            best_val_metrics = dict(val_metrics)
            patience_count = 0
        else:
            patience_count += 1

        if epoch == 1 or epoch % 5 == 0 or epoch == args.epochs:
            print(
                f"  epoch {epoch:03d} | train={train_loss:.4f} val={val_metrics['loss_total']:.4f} "
                f"main={val_metrics['acc_main']:.4f} turn={val_metrics['acc_turn']:.4f} "
                f"turnL={val_metrics['turn_left_recall']:.4f} turnT={val_metrics['acc_turn_transition']:.4f} "
                f"theta={val_metrics['theta_mae_deg']:.4f} score={score:.4f}"
            )

        if epoch >= args.min_epochs and patience_count >= args.patience:
            print(f"[ModernTCN] 早停：epoch={epoch}, best_epoch={best_epoch}")
            break

    if best_state is None:
        raise RuntimeError("训练未产生有效 checkpoint。")

    model.load_state_dict(best_state)
    test_loss, logits_main, logits_turn, theta_hat = _predict_full(
        model, test_loader, test_split, device, class_w_main, class_w_turn, cfg
    )
    test_metrics = compute_metrics(logits_main, logits_turn, theta_hat, test_split, test_loss)
    train_seconds = time.time() - t0

    torch.save(
        {
            "model_state": best_state,
            "model_config": cfg.to_dict(),
            "seed": args.seed,
            "best_epoch": best_epoch,
            "best_val_score": best_score,
            "best_val_metrics": best_val_metrics,
            "test_metrics": test_metrics,
            "contract": contract.__dict__,
            "feat_names": data["feat_names"],
            "scaler": data["scaler"],
            "train_seconds": train_seconds,
        },
        checkpoint_file,
    )

    paths = {"checkpoint_file": str(checkpoint_file), "report_file": str(report_file)}
    row = metric_row(args.seed, best_epoch, test_metrics, paths)
    _write_csv(summary_csv, [row])
    _write_csv(history_csv, history_rows)
    _write_report(report_file, args, cfg, contract.__dict__, row, test_metrics, best_val_metrics, train_seconds)

    print("[ModernTCN] 训练完成")
    print(f"  checkpoint: {checkpoint_file}")
    print(f"  summary: {summary_csv}")
    print(f"  report: {report_file}")
    print(
        f"  test main={test_metrics['acc_main']:.4f}, turnT={test_metrics['acc_turn_transition']:.4f}, "
        f"turnL={test_metrics['turn_left_recall']:.4f}, theta={test_metrics['theta_mae_deg']:.4f}, flat={test_metrics['flat_recall']:.4f}, "
        f"slope={test_metrics['slope_recall']:.4f}"
    )

    if args.seed == 42:
        passed, failures = seed42_gate(test_metrics)
        print(f"  seed42 gate pass={int(passed)}")
        for msg in failures:
            print(f"    - {msg}")

    return {
        "checkpoint_file": str(checkpoint_file),
        "summary_csv": str(summary_csv),
        "report_file": str(report_file),
        "test_metrics": test_metrics,
        "best_epoch": best_epoch,
    }


def _train_epoch(model, loader, opt, device, class_w_main, class_w_turn, cfg) -> float:
    model.train()
    total_loss = 0.0
    total_n = 0
    for batch in loader:
        batch = _to_device(batch, device)
        opt.zero_grad(set_to_none=True)
        logits_main, logits_turn, theta_hat = model(batch["X"])
        loss, _ = multitask_loss(logits_main, logits_turn, theta_hat, batch, class_w_main, class_w_turn, cfg)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        opt.step()
        n = int(batch["X"].shape[0])
        total_loss += float(loss.detach().cpu()) * n
        total_n += n
    return total_loss / max(total_n, 1)


@torch.no_grad()
def _predict_full(model, loader, split, device, class_w_main, class_w_turn, cfg) -> Tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    model.eval()
    logits_main_all = []
    logits_turn_all = []
    theta_all = []
    loss_sum = 0.0
    n_sum = 0
    for batch in loader:
        batch = _to_device(batch, device)
        logits_main, logits_turn, theta_hat = model(batch["X"])
        loss, _ = multitask_loss(logits_main, logits_turn, theta_hat, batch, class_w_main, class_w_turn, cfg)
        n = int(batch["X"].shape[0])
        loss_sum += float(loss.detach().cpu()) * n
        n_sum += n
        logits_main_all.append(logits_main.detach().cpu().numpy())
        logits_turn_all.append(logits_turn.detach().cpu().numpy())
        theta_all.append(theta_hat.detach().cpu().numpy())
    return (
        loss_sum / max(n_sum, 1),
        np.concatenate(logits_main_all, axis=0),
        np.concatenate(logits_turn_all, axis=0),
        np.concatenate(theta_all, axis=0).reshape(-1),
    )


def _to_device(batch: Dict[str, torch.Tensor], device: torch.device) -> Dict[str, torch.Tensor]:
    return {k: v.to(device, non_blocking=True) for k, v in batch.items()}


def _set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


def _select_device(mode: str) -> torch.device:
    if mode == "cuda":
        return torch.device("cuda")
    if mode == "cpu":
        return torch.device("cpu")
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _history_row(epoch: int, lr: float, train_loss: float, val_metrics: Dict[str, object], score: float) -> Dict[str, object]:
    return {
        "epoch": epoch,
        "lr": lr,
        "train_loss": train_loss,
        "val_loss": val_metrics["loss_total"],
        "val_score": score,
        "val_acc_main": val_metrics["acc_main"],
        "val_acc_turn": val_metrics["acc_turn"],
        "val_main_confidence_mean": val_metrics.get("main_confidence_mean", float("nan")),
        "val_turn_confidence_mean": val_metrics.get("turn_confidence_mean", float("nan")),
        "val_main_low_conf_0p60_ratio": val_metrics.get("main_low_conf_0p60_ratio", float("nan")),
        "val_turn_low_conf_0p60_ratio": val_metrics.get("turn_low_conf_0p60_ratio", float("nan")),
        "val_turn_left_recall": val_metrics["turn_left_recall"],
        "val_turn_right_recall": val_metrics["turn_right_recall"],
        "val_acc_turn_transition": val_metrics["acc_turn_transition"],
        "val_theta_mae_deg": val_metrics["theta_mae_deg"],
        "val_theta_abs_le_10_p95_abs_err_deg": val_metrics["theta_abs_le_10_p95_abs_err_deg"],
        "val_theta_neg_10_8_p95_abs_err_deg": val_metrics["theta_neg_10_8_p95_abs_err_deg"],
        "val_theta_pos_8_10_p95_abs_err_deg": val_metrics["theta_pos_8_10_p95_abs_err_deg"],
        "val_theta_abs_le_8_p95_abs_err_deg": val_metrics["theta_abs_le_8_p95_abs_err_deg"],
        "val_theta_neg_8_6_p95_abs_err_deg": val_metrics["theta_neg_8_6_p95_abs_err_deg"],
        "val_theta_pos_6_8_p95_abs_err_deg": val_metrics["theta_pos_6_8_p95_abs_err_deg"],
        "val_theta_neg_2_0p5_p95_abs_err_deg": val_metrics["theta_neg_2_0p5_p95_abs_err_deg"],
        "val_theta_pos_0p5_2_p95_abs_err_deg": val_metrics["theta_pos_0p5_2_p95_abs_err_deg"],
        "val_theta_flat_abs_p95_deg": val_metrics["theta_flat_abs_p95_deg"],
        "val_theta_flat_bias_deg": val_metrics["theta_flat_bias_deg"],
        "val_theta_near_flat_abs_p95_deg": val_metrics["theta_near_flat_abs_p95_deg"],
        "val_theta_true_zero_abs_p95_deg": val_metrics["theta_true_zero_abs_p95_deg"],
        "val_flat_recall": val_metrics["flat_recall"],
        "val_stall_recall": val_metrics["stall_recall"],
        "val_slope_recall": val_metrics["slope_recall"],
    }


def _write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    rows = list(rows)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_report(
    path: Path,
    args: argparse.Namespace,
    cfg: ModernTCNConfig,
    contract: Dict[str, object],
    row: Dict[str, object],
    test_metrics: Dict[str, object],
    val_metrics: Dict[str, object],
    train_seconds: float,
) -> None:
    passed, failures = seed42_gate(test_metrics) if args.seed == 42 else (False, [])
    with path.open("w", encoding="utf-8") as f:
        f.write("# ModernTCN-small 第一阶段训练报告\n\n")
        f.write("## 固定约束\n\n")
        f.write(f"- dataset: `{contract['dataset_file']}`\n")
        f.write(f"- vehicle: `{contract.get('vehicle_type', '')}`; active=`{contract.get('active_drive_steer_wheels', '')}`; passive=`{contract.get('passive_support_wheels', '')}`\n")
        f.write(f"- feature_policy: `{contract.get('feature_policy', '')}`\n")
        f.write(f"- label_time_policy: `{contract.get('label_time_policy', '')}`, horizon_steps={contract.get('horizon_steps', 0)}\n")
        f.write("- split: 使用 MAT 文件已有 run-level split，不重划分。\n")
        f.write("- scaler: 使用 MAT 文件已有归一化后 X，不重新拟合。\n")
        f.write(f"- confidence_policy: `{contract.get('confidence_policy', '')}`\n")
        f.write(f"- input: `[batch, time={contract['seq_len']}, feature={contract['input_dim']}]`\n")
        f.write("- output: `logits_main`, `logits_turn`, `theta_hat`\n\n")
        f.write("## 配置\n\n")
        f.write("```json\n")
        f.write(json.dumps(cfg.to_dict(), indent=2, ensure_ascii=False))
        f.write("\n```\n\n")
        f.write("## 测试集指标\n\n")
        f.write("| metric | value |\n|---|---:|\n")
        for key in [
            "acc_main",
            "acc_turn",
            "acc_turn_pure",
            "acc_turn_transition",
            "main_confidence_mean",
            "main_low_conf_0p60_ratio",
            "main_low_conf_0p70_ratio",
            "turn_confidence_mean",
            "turn_low_conf_0p60_ratio",
            "turn_low_conf_0p70_ratio",
            "turn_right_recall",
            "turn_straight_recall",
            "turn_left_recall",
            "theta_mae_deg",
            "theta_abs_le_10_p95_abs_err_deg",
            "theta_neg_10_8_p95_abs_err_deg",
            "theta_pos_8_10_p95_abs_err_deg",
            "theta_abs_le_8_p95_abs_err_deg",
            "theta_neg_8_6_p95_abs_err_deg",
            "theta_pos_6_8_p95_abs_err_deg",
            "theta_neg_2_0p5_p95_abs_err_deg",
            "theta_pos_0p5_2_p95_abs_err_deg",
            "theta_flat_abs_p95_deg",
            "theta_flat_bias_deg",
            "theta_near_flat_abs_p95_deg",
            "theta_true_zero_abs_p95_deg",
            "theta_near_flat_bias_deg",
            "theta_flat_turn_abs_p95_deg",
            "flat_recall",
            "stall_recall",
            "slope_recall",
            "uphill_recall",
            "downhill_recall",
        ]:
            f.write(f"| {key} | {float(row[key]):.4f} |\n")
        f.write(f"\n- best_epoch: {row['best_epoch']}\n")
        f.write(f"- train_seconds: {train_seconds:.1f}\n\n")
        f.write("## 置信度分桶\n\n")
        _write_confidence_bins(f, "main", test_metrics)
        _write_confidence_bins(f, "turn", test_metrics)
        if args.seed == 42:
            f.write("## seed42 进入三 seed 判定\n\n")
            f.write(f"- pass: `{int(passed)}`\n")
            if failures:
                for msg in failures:
                    f.write(f"- {msg}\n")
            else:
                f.write("- seed42 已满足进入 `[42, 73, 101]` 的最低门槛。\n")
        f.write("\n## 验证集最佳点\n\n")
        f.write("```json\n")
        f.write(json.dumps(val_metrics, indent=2, ensure_ascii=False))
        f.write("\n```\n")


def _write_confidence_bins(f, prefix: str, metrics: Dict[str, object]) -> None:
    f.write(f"### {prefix}\n\n")
    f.write("| confidence bin | n | error rate | mean confidence |\n|---|---:|---:|---:|\n")
    for row in metrics.get(f"{prefix}_confidence_bins", []):
        f.write(
            f"| {row['bin']} | {int(row['n'])} | "
            f"{float(row['error_rate']):.4f} | {float(row['mean_confidence']):.4f} |\n"
        )
    f.write("\n")


if __name__ == "__main__":
    main()
