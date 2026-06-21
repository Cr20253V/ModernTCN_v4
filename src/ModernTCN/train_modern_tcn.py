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
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple

import numpy as np
import torch
from torch.utils.data import DataLoader

from modern_tcn_data import AGVWindowDataset, class_weights, find_project_root, load_modern_tcn_dataset
from modern_tcn_metrics import compute_metrics, metric_row, multitask_loss, seed42_gate, selection_score
from modern_tcn_model import (
    ModernTCNConfig,
    ModernTCNDualKernelConfig,
    ModernTCNFullConfig,
    ModernTCNGroupedConfig,
    build_model_from_config,
    normalize_model_family,
)


FULL_DEFAULT_DATASET = (
    Path("data")
    / "tcn"
    / "ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v4b_weakcombo_rebalanced_passive17_plus_all5.mat"
)

PLANTFIX_22D_DATASET = (
    Path("data")
    / "tcn"
    / "ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat"
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="ModernTCN-small / ModernTCNFull 第一阶段训练脚本")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "--model-family",
        "--model_family",
        dest="model_family",
        type=str,
        default="small",
        choices=["small", "full", "small_gffn", "small_dualkernel"],
    )
    p.add_argument("--dataset-file", "--dataset_file", dest="dataset_file", type=str, default="")
    p.add_argument("--output-root", "--output_root", dest="output_root", type=str, default="")
    p.add_argument("--run-tag", "--run_tag", dest="run_tag", type=str, default="")
    p.add_argument("--no-overwrite", "--no_overwrite", dest="no_overwrite", action="store_true")
    p.add_argument("--epochs", type=int, default=120)
    p.add_argument("--batch-size", "--batch_size", dest="batch_size", type=int, default=256)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--weight-decay", "--weight_decay", dest="weight_decay", type=float, default=1e-4)
    p.add_argument("--patience", type=int, default=25)
    p.add_argument("--min-epochs", type=int, default=30)
    p.add_argument("--channels", type=int, default=64)
    p.add_argument("--dmodel", type=int, default=None)
    p.add_argument("--blocks", type=int, default=5)
    p.add_argument("--kernel-size", "--kernel_size", dest="kernel_size", type=int, default=31)
    p.add_argument("--patch-size", "--patch_size", dest="patch_size", type=int, default=None)
    p.add_argument("--patch-stride", "--patch_stride", dest="patch_stride", type=int, default=None)
    p.add_argument("--dims", type=str, default=None)
    p.add_argument("--stage-blocks", "--stage_blocks", dest="stage_blocks", type=str, default=None)
    p.add_argument("--large-kernels", "--large_kernels", dest="large_kernels", type=str, default=None)
    p.add_argument("--small-kernels", "--small_kernels", dest="small_kernels", type=str, default=None)
    p.add_argument("--large-kernel", "--large_kernel", dest="large_kernel", type=int, default=None)
    p.add_argument("--small-kernel", "--small_kernel", dest="small_kernel", type=int, default=None)
    p.add_argument("--dual-branch-scale", "--dual_branch_scale", dest="dual_branch_scale", type=float, default=None)
    p.add_argument(
        "--small-branch-init",
        "--small_branch_init",
        dest="small_branch_init",
        type=str,
        default=None,
        choices=["default", "zero"],
    )
    p.add_argument(
        "--temporal-padding",
        "--temporal_padding",
        dest="temporal_padding",
        type=str,
        default="same",
        choices=["same", "causal"],
        help="Temporal convolution padding mode. 默认 same，causal 仅用于因果消融实验。",
    )
    p.add_argument("--dropout", type=float, default=0.15)
    p.add_argument("--ffn-ratio", "--ffn_ratio", dest="ffn_ratio", type=int, default=None)
    p.add_argument("--layer-scale-init", "--layer_scale_init", dest="layer_scale_init", type=float, default=None)
    p.add_argument("--command-dropout-prob", "--command_dropout_prob", dest="command_dropout_prob", type=float, default=0.0)
    p.add_argument("--command-dropout-start-index", "--command_dropout_start_index", dest="command_dropout_start_index", type=int, default=-1)
    p.add_argument("--command-dropout-feature-count", "--command_dropout_feature_count", dest="command_dropout_feature_count", type=int, default=0)
    p.add_argument(
        "--command-dropout-mode",
        "--command_dropout_mode",
        dest="command_dropout_mode",
        type=str,
        default="window_block",
        choices=["window_block", "time_block", "channel_block"],
        help="训练期命令特征 dropout。只作用于 train batch，验证/测试/导出不启用。",
    )
    p.add_argument("--turn-head-source", "--turn_head_source", dest="turn_head_source", type=str, default="full", choices=["full", "inputstats", "kinematic_stats"])
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
    p.add_argument("--lambda-turn-release", type=float, default=0.0)
    p.add_argument("--lambda-false-turn-straight", type=float, default=0.0)
    p.add_argument("--theta-excess-target-deg", type=float, default=1.0)
    p.add_argument("--theta-flat-excess-target-deg", type=float, default=0.5)
    p.add_argument("--theta-small-neg-min-deg", type=float, default=-4.0)
    p.add_argument("--theta-small-neg-max-deg", type=float, default=-2.0)
    p.add_argument("--theta-gate-mode", type=str, default="none", choices=["none", "main_slope_prob"])
    p.add_argument("--theta-gate-power", type=float, default=1.0)
    p.add_argument("--theta-gate-floor", type=float, default=0.0)
    p.add_argument("--theta-neg-weight", type=float, default=1.0)
    p.add_argument("--theta-pos-weight", type=float, default=1.0)
    p.add_argument("--main-class-multipliers", "--main_class_multipliers", dest="main_class_multipliers", type=float, nargs=3, default=None)
    p.add_argument("--turn-class-weight-method", "--turn_class_weight_method", dest="turn_class_weight_method", type=str, default=None, choices=["none", "inverse", "sqrt_inverse"])
    p.add_argument("--main-class-weight-method", "--main_class_weight_method", dest="main_class_weight_method", type=str, default=None, choices=["none", "inverse", "sqrt_inverse"])
    p.add_argument("--main-neg-slope-weight", "--main_neg_slope_weight", dest="main_neg_slope_weight", type=float, default=None)
    p.add_argument("--main-pos-slope-weight", "--main_pos_slope_weight", dest="main_pos_slope_weight", type=float, default=None)
    p.add_argument("--turn-transition-weight", type=float, default=1.0)
    p.add_argument("--turn-class-multipliers", type=float, nargs=3, default=[1.00, 1.10, 1.00])
    p.add_argument("--select-turn-weight", type=float, default=0.30)
    p.add_argument("--select-turn-transition-weight", type=float, default=1.00)
    p.add_argument("--select-turn-transition-target", type=float, default=0.75)
    p.add_argument("--select-turn-left-weight", type=float, default=0.00)
    p.add_argument("--select-turn-left-target", type=float, default=0.80)
    p.add_argument("--select-turn-lr-weight", type=float, default=0.00)
    p.add_argument("--select-turn-lr-target", type=float, default=0.80)
    p.add_argument("--select-stall-weight", "--select_stall_weight", dest="select_stall_weight", type=float, default=0.0)
    p.add_argument("--select-stall-target", "--select_stall_target", dest="select_stall_target", type=float, default=0.70)
    p.add_argument("--select-theta-weight", type=float, default=0.15)
    p.add_argument("--select-theta-ref-deg", type=float, default=5.0)
    p.add_argument("--select-theta-p95-weight", type=float, default=0.0)
    p.add_argument("--select-theta-p95-target-deg", type=float, default=1.0)
    p.add_argument("--select-theta-flat-p95-weight", type=float, default=0.0)
    p.add_argument("--select-theta-flat-p95-target-deg", type=float, default=1.0)
    p.add_argument("--select-theta-flat-peak-weight", type=float, default=0.0)
    p.add_argument("--select-theta-flat-peak-target-deg", type=float, default=3.0)
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
    p.add_argument("--num-workers", "--num_workers", dest="num_workers", type=int, default=0)
    p.add_argument("--limit-train", "--limit_train", dest="limit_train", type=int, default=0, help="仅用于 smoke test，正式实验必须为 0。")
    p.add_argument("--limit-val", "--limit_val", dest="limit_val", type=int, default=0, help="仅用于 smoke test，正式实验必须为 0。")
    p.add_argument("--limit-test", "--limit_test", dest="limit_test", type=int, default=0, help="仅用于 smoke test，正式实验必须为 0。")
    p.add_argument("--dry-run", "--dry_run", dest="dry_run", action="store_true", help="只读取数据并跑一次前向，不保存训练结果。")
    return p.parse_args()


def main() -> Dict[str, object]:
    args = parse_args()
    return train_one_seed(args)


def train_one_seed(args: argparse.Namespace) -> Dict[str, object]:
    root = find_project_root()
    model_family = normalize_model_family(getattr(args, "model_family", "small"))
    run_tag = getattr(args, "run_tag", "") or _default_run_tag(model_family, args.seed)
    output_root = _resolve_output_root(root, getattr(args, "output_root", ""), model_family)
    out_dir = output_root / run_tag
    dataset_file = _resolve_dataset_file(root, getattr(args, "dataset_file", ""), model_family)

    if getattr(args, "no_overwrite", False) and out_dir.exists() and any(out_dir.iterdir()):
        raise FileExistsError(f"--no-overwrite enabled and output directory already exists: {out_dir}")

    _set_seed(args.seed)
    device = _select_device(getattr(args, "device", "auto"))
    data = load_modern_tcn_dataset(
        dataset_file=dataset_file,
        limit_train=getattr(args, "limit_train", 0),
        limit_val=getattr(args, "limit_val", 0),
        limit_test=getattr(args, "limit_test", 0),
    )
    train_split = data["train"]
    val_split = data["val"]
    test_split = data["test"]
    contract = data["contract"]

    cfg = _build_config(args, contract, model_family)
    model = build_model_from_config(cfg, model_family).to(device)

    # smoke test 只验证数据契约和模型维度，不写任何模型文件。
    if getattr(args, "dry_run", False):
        xb = torch.from_numpy(train_split.X[:4]).float().to(device)
        with torch.no_grad():
            outputs = model(xb)
        print(f"[ModernTCN {model_family} dry-run] 数据和模型前向检查通过")
        print(f"  X: {tuple(xb.shape)}")
        print(f"  logits_main/logits_turn/theta: {[tuple(o.shape) for o in outputs]}")
        return {"status": "dry_run_ok"}

    out_dir.mkdir(parents=True, exist_ok=True)
    file_prefix = _file_prefix(model_family, args.seed)
    checkpoint_file = out_dir / f"{file_prefix}.pt"
    summary_csv = out_dir / f"{file_prefix}_summary.csv"
    history_csv = out_dir / f"{file_prefix}_history.csv"
    report_file = out_dir / _report_file_name(model_family)
    config_json = out_dir / "config.json"
    config_md = out_dir / "config.md"
    git_hash_file = out_dir / "git_hash.txt"
    contract_copy_file = out_dir / "dataset_contract_copy.json"
    feature_names_file = out_dir / "feature_names.txt"
    train_log_file = out_dir / "train_log.txt"
    metrics_val_csv = out_dir / "metrics_val.csv"
    metrics_test_csv = out_dir / "metrics_test.csv"

    train_loader = DataLoader(
        AGVWindowDataset(train_split),
        batch_size=getattr(args, "batch_size", 256),
        shuffle=True,
        num_workers=getattr(args, "num_workers", 0),
        pin_memory=(device.type == "cuda"),
    )
    val_loader = DataLoader(AGVWindowDataset(val_split), batch_size=getattr(args, "batch_size", 256), shuffle=False, num_workers=0)
    test_loader = DataLoader(AGVWindowDataset(test_split), batch_size=getattr(args, "batch_size", 256), shuffle=False, num_workers=0)

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

    opt = torch.optim.AdamW(model.parameters(), lr=getattr(args, "lr", 1e-3), weight_decay=getattr(args, "weight_decay", 1e-4))
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=max(getattr(args, "epochs", 120), 1))

    print(f"[ModernTCN {model_family}] 第一阶段训练开始")
    print(f"  seed={args.seed}, device={device}, out={out_dir}")
    print(f"  dataset={contract.dataset_file}")
    print(f"  train/val/test={len(train_split.X)}/{len(val_split.X)}/{len(test_split.X)}")
    print(f"  model_family={model_family}")
    if model_family == "full":
        print(
            f"  full patch={cfg.patch_size}/{cfg.patch_stride}, dims={cfg.dims}, "
            f"stage_blocks={cfg.stage_blocks}, large_kernels={cfg.large_kernels}"
        )
    elif model_family == "small_gffn":
        print(
            f"  grouped dmodel={cfg.dmodel}, blocks={cfg.blocks}, kernel={cfg.kernel_size}, "
            f"ffn_ratio={cfg.ffn_ratio}, layer_scale_init={cfg.layer_scale_init:g}"
        )
    elif model_family == "small_dualkernel":
        print(
            f"  dual-kernel channels={cfg.channels}, blocks={cfg.blocks}, large={cfg.large_kernel}, "
            f"small={cfg.small_kernel}, branch_scale={cfg.dual_branch_scale:g}, "
            f"small_branch_init={cfg.small_branch_init}, layer_scale_init={cfg.layer_scale_init:g}"
        )
    else:
        print(
            f"  model channels={cfg.channels}, blocks={cfg.blocks}, kernel={cfg.kernel_size}, "
            f"temporal_padding={cfg.temporal_padding}"
        )
    if cfg.command_dropout_prob > 0:
        print(
            "  command_dropout="
            f"prob={cfg.command_dropout_prob:g}, start={cfg.command_dropout_start_index}, "
            f"count={cfg.command_dropout_feature_count}, mode={cfg.command_dropout_mode}"
        )

    best_score = math.inf
    best_epoch = 0
    best_state = None
    best_val_metrics: Dict[str, object] = {}
    patience_count = 0
    history_rows = []
    t0 = time.time()

    for epoch in range(1, getattr(args, "epochs", 120) + 1):
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

        if epoch == 1 or epoch % 5 == 0 or epoch == getattr(args, "epochs", 120):
            print(
                f"  epoch {epoch:03d} | train={train_loss:.4f} val={val_metrics['loss_total']:.4f} "
                f"main={val_metrics['acc_main']:.4f} turn={val_metrics['acc_turn']:.4f} "
                f"turnL={val_metrics['turn_left_recall']:.4f} turnT={val_metrics['acc_turn_transition']:.4f} "
                f"theta={val_metrics['theta_mae_deg']:.4f} score={score:.4f}"
            )

        if epoch >= getattr(args, "min_epochs", 30) and patience_count >= getattr(args, "patience", 25):
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
            "model_family": model_family,
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
    row["model"] = _model_label(model_family)
    _write_csv(summary_csv, [row])
    _write_csv(history_csv, history_rows)
    val_row = metric_row(args.seed, best_epoch, best_val_metrics, paths)
    val_row["model"] = _model_label(model_family)
    _write_csv(metrics_val_csv, [val_row])
    _write_csv(metrics_test_csv, [row])
    _write_run_metadata(
        root=root,
        out_dir=out_dir,
        args=args,
        cfg=cfg,
        contract=contract.__dict__,
        feat_names=data["feat_names"],
        model_family=model_family,
        run_tag=run_tag,
        files={
            "config_json": config_json,
            "config_md": config_md,
            "git_hash_file": git_hash_file,
            "contract_copy_file": contract_copy_file,
            "feature_names_file": feature_names_file,
            "train_log_file": train_log_file,
        },
    )
    _write_report(report_file, args, cfg, contract.__dict__, row, test_metrics, best_val_metrics, train_seconds, model_family)

    print(f"[ModernTCN {model_family}] 训练完成")
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


def _default_run_tag(model_family: str, seed: int) -> str:
    if model_family == "full":
        return f"modern_tcn_full_v4b_seed{seed}"
    if model_family == "small_dualkernel":
        return f"dual_k31_s5_seed{seed}"
    if model_family == "small_gffn":
        return f"gffn_d4_k31_seed{seed}"
    return f"modern_tcn_v4_industrial_seed{seed}"


def _result_dir_name(model_family: str) -> str:
    if model_family == "full":
        return "modern_tcn_full"
    if model_family == "small_dualkernel":
        return "modern_tcn_ablation/exp2_dual_kernel"
    if model_family == "small_gffn":
        return "modern_tcn_ablation/exp1_grouped_ffn"
    return "modern_tcn"


def _file_prefix(model_family: str, seed: int) -> str:
    if model_family == "full":
        return f"modern_tcn_full_seed{seed}"
    if model_family == "small_dualkernel":
        return f"modern_tcn_dualkernel_seed{seed}"
    if model_family == "small_gffn":
        return f"modern_tcn_gffn_seed{seed}"
    return f"modern_tcn_seed{seed}"


def _report_file_name(model_family: str) -> str:
    if model_family == "full":
        return "ModernTCNFull_train_report.md"
    if model_family == "small_dualkernel":
        return "ModernTCNDualKernel_train_report.md"
    if model_family == "small_gffn":
        return "ModernTCNGrouped_train_report.md"
    return "ModernTCN_train_report.md"


def _model_label(model_family: str) -> str:
    if model_family == "small_gffn":
        return "ModernTCN-small-gffn"
    if model_family == "small_dualkernel":
        return "ModernTCN-small-dualkernel"
    if model_family == "full":
        return "ModernTCNFull"
    return "ModernTCN-small"


def _resolve_output_root(root: Path, output_root_arg: str, model_family: str) -> Path:
    if output_root_arg:
        path = Path(output_root_arg)
        return path if path.is_absolute() else root / path
    return root / "results" / _result_dir_name(model_family)


def _resolve_dataset_file(root: Path, dataset_arg: str, model_family: str) -> Optional[Path]:
    if dataset_arg:
        path = Path(dataset_arg)
        return path if path.is_absolute() else root / path
    if model_family == "small_dualkernel":
        return root / PLANTFIX_22D_DATASET
    if model_family == "full":
        return root / FULL_DEFAULT_DATASET
    return None


def _arg(args: argparse.Namespace, name: str, default):
    value = getattr(args, name, default)
    return default if value is None else value


def _tuple_arg(args: argparse.Namespace, name: str, default: Tuple[int, ...]) -> Tuple[int, ...]:
    value = getattr(args, name, None)
    if value is None:
        return tuple(default)
    if isinstance(value, (tuple, list)):
        return tuple(int(x) for x in value)
    parts = [item.strip() for item in str(value).split(",") if item.strip()]
    if not parts:
        raise ValueError(f"{name} must contain at least one integer.")
    return tuple(int(item) for item in parts)


def _build_config(args: argparse.Namespace, contract, model_family: str) -> ModernTCNConfig:
    if model_family == "full":
        base = ModernTCNFullConfig()
    elif model_family == "small_dualkernel":
        base = ModernTCNDualKernelConfig()
    elif model_family == "small_gffn":
        base = ModernTCNGroupedConfig()
    else:
        base = ModernTCNConfig()
    common = {
        "input_dim": contract.input_dim,
        "seq_len": contract.seq_len,
        "channels": _arg(args, "channels", base.channels),
        "blocks": _arg(args, "blocks", base.blocks),
        "kernel_size": _arg(args, "kernel_size", base.kernel_size),
        "temporal_padding": _arg(args, "temporal_padding", base.temporal_padding),
        "dropout": _arg(args, "dropout", base.dropout),
        "command_dropout_prob": _arg(args, "command_dropout_prob", base.command_dropout_prob),
        "command_dropout_start_index": _arg(
            args, "command_dropout_start_index", base.command_dropout_start_index
        ),
        "command_dropout_feature_count": _arg(
            args, "command_dropout_feature_count", base.command_dropout_feature_count
        ),
        "command_dropout_mode": _arg(args, "command_dropout_mode", base.command_dropout_mode),
        "turn_head_source": _arg(args, "turn_head_source", base.turn_head_source),
        "lambda_turn": _arg(args, "lambda_turn", base.lambda_turn),
        "lambda_theta": _arg(args, "lambda_theta", base.lambda_theta),
        "lambda_theta_flat": _arg(args, "lambda_theta_flat", base.lambda_theta_flat),
        "theta_flat_loss_mode": _arg(args, "theta_flat_loss_mode", base.theta_flat_loss_mode),
        "theta_flat_zero_tol_deg": _arg(args, "theta_flat_zero_tol_deg", base.theta_flat_zero_tol_deg),
        "lambda_theta_near_flat": _arg(args, "lambda_theta_near_flat", base.lambda_theta_near_flat),
        "theta_near_flat_deg": _arg(args, "theta_near_flat_deg", base.theta_near_flat_deg),
        "lambda_theta_error_excess": _arg(args, "lambda_theta_error_excess", base.lambda_theta_error_excess),
        "lambda_theta_flat_excess": _arg(args, "lambda_theta_flat_excess", base.lambda_theta_flat_excess),
        "lambda_theta_near_flat_excess": _arg(
            args, "lambda_theta_near_flat_excess", base.lambda_theta_near_flat_excess
        ),
        "lambda_theta_true_zero_excess": _arg(args, "lambda_theta_true_zero_excess", base.lambda_theta_true_zero_excess),
        "lambda_theta_active_excess": _arg(args, "lambda_theta_active_excess", base.lambda_theta_active_excess),
        "lambda_theta_small_neg": _arg(args, "lambda_theta_small_neg", base.lambda_theta_small_neg),
        "lambda_theta_small_neg_excess": _arg(args, "lambda_theta_small_neg_excess", base.lambda_theta_small_neg_excess),
        "lambda_turn_release": _arg(args, "lambda_turn_release", base.lambda_turn_release),
        "lambda_false_turn_straight": _arg(args, "lambda_false_turn_straight", base.lambda_false_turn_straight),
        "theta_excess_target_deg": _arg(args, "theta_excess_target_deg", base.theta_excess_target_deg),
        "theta_flat_excess_target_deg": _arg(args, "theta_flat_excess_target_deg", base.theta_flat_excess_target_deg),
        "theta_true_zero_tol_deg": _arg(args, "theta_true_zero_tol_deg", base.theta_true_zero_tol_deg),
        "theta_small_neg_min_deg": _arg(args, "theta_small_neg_min_deg", base.theta_small_neg_min_deg),
        "theta_small_neg_max_deg": _arg(args, "theta_small_neg_max_deg", base.theta_small_neg_max_deg),
        "theta_gate_mode": _arg(args, "theta_gate_mode", base.theta_gate_mode),
        "theta_gate_power": _arg(args, "theta_gate_power", base.theta_gate_power),
        "theta_gate_floor": _arg(args, "theta_gate_floor", base.theta_gate_floor),
        "main_class_multipliers": tuple(_arg(args, "main_class_multipliers", base.main_class_multipliers)),
        "turn_class_multipliers": tuple(_arg(args, "turn_class_multipliers", base.turn_class_multipliers)),
        "main_class_weight_method": _arg(args, "main_class_weight_method", base.main_class_weight_method),
        "turn_class_weight_method": _arg(args, "turn_class_weight_method", base.turn_class_weight_method),
        "main_neg_slope_weight": _arg(args, "main_neg_slope_weight", base.main_neg_slope_weight),
        "main_pos_slope_weight": _arg(args, "main_pos_slope_weight", base.main_pos_slope_weight),
        "theta_neg_weight": _arg(args, "theta_neg_weight", 1.0),
        "theta_pos_weight": _arg(args, "theta_pos_weight", base.theta_pos_weight),
        "turn_transition_weight": _arg(args, "turn_transition_weight", base.turn_transition_weight),
        "select_turn_weight": _arg(args, "select_turn_weight", base.select_turn_weight),
        "select_turn_transition_weight": _arg(
            args, "select_turn_transition_weight", base.select_turn_transition_weight
        ),
        "select_turn_transition_target": _arg(
            args, "select_turn_transition_target", base.select_turn_transition_target
        ),
        "select_turn_left_weight": _arg(args, "select_turn_left_weight", base.select_turn_left_weight),
        "select_turn_left_target": _arg(args, "select_turn_left_target", base.select_turn_left_target),
        "select_turn_lr_weight": _arg(args, "select_turn_lr_weight", base.select_turn_lr_weight),
        "select_turn_lr_target": _arg(args, "select_turn_lr_target", base.select_turn_lr_target),
        "select_stall_weight": _arg(args, "select_stall_weight", base.select_stall_weight),
        "select_stall_target": _arg(args, "select_stall_target", base.select_stall_target),
        "select_theta_weight": _arg(args, "select_theta_weight", base.select_theta_weight),
        "select_theta_ref_deg": _arg(args, "select_theta_ref_deg", base.select_theta_ref_deg),
        "select_theta_p95_weight": _arg(args, "select_theta_p95_weight", base.select_theta_p95_weight),
        "select_theta_p95_target_deg": _arg(args, "select_theta_p95_target_deg", base.select_theta_p95_target_deg),
        "select_theta_flat_p95_weight": _arg(
            args, "select_theta_flat_p95_weight", base.select_theta_flat_p95_weight
        ),
        "select_theta_flat_p95_target_deg": _arg(
            args, "select_theta_flat_p95_target_deg", base.select_theta_flat_p95_target_deg
        ),
        "select_theta_near_flat_p95_weight": _arg(
            args, "select_theta_near_flat_p95_weight", base.select_theta_near_flat_p95_weight
        ),
        "select_theta_near_flat_p95_target_deg": _arg(
            args, "select_theta_near_flat_p95_target_deg", base.select_theta_near_flat_p95_target_deg
        ),
        "select_theta_true_zero_p95_weight": _arg(
            args, "select_theta_true_zero_p95_weight", base.select_theta_true_zero_p95_weight
        ),
        "select_theta_true_zero_p95_target_deg": _arg(
            args, "select_theta_true_zero_p95_target_deg", base.select_theta_true_zero_p95_target_deg
        ),
        "select_theta_flat_peak_weight": _arg(
            args, "select_theta_flat_peak_weight", base.select_theta_flat_peak_weight
        ),
        "select_theta_flat_peak_target_deg": _arg(
            args, "select_theta_flat_peak_target_deg", base.select_theta_flat_peak_target_deg
        ),
        "select_theta_small_neg_p95_weight": _arg(
            args, "select_theta_small_neg_p95_weight", base.select_theta_small_neg_p95_weight
        ),
        "select_theta_small_neg_p95_target_deg": _arg(
            args, "select_theta_small_neg_p95_target_deg", base.select_theta_small_neg_p95_target_deg
        ),
        "select_theta_extreme_p95_weight": _arg(
            args, "select_theta_extreme_p95_weight", base.select_theta_extreme_p95_weight
        ),
        "select_theta_extreme_p95_target_deg": _arg(
            args, "select_theta_extreme_p95_target_deg", base.select_theta_extreme_p95_target_deg
        ),
        "select_theta_edge_p95_weight": _arg(args, "select_theta_edge_p95_weight", base.select_theta_edge_p95_weight),
        "select_theta_edge_p95_target_deg": _arg(
            args, "select_theta_edge_p95_target_deg", base.select_theta_edge_p95_target_deg
        ),
        "select_theta_small_nonzero_p95_weight": _arg(
            args, "select_theta_small_nonzero_p95_weight", base.select_theta_small_nonzero_p95_weight
        ),
        "select_theta_small_nonzero_p95_target_deg": _arg(
            args, "select_theta_small_nonzero_p95_target_deg", base.select_theta_small_nonzero_p95_target_deg
        ),
        "select_theta_flat_bias_weight": _arg(args, "select_theta_flat_bias_weight", base.select_theta_flat_bias_weight),
        "select_theta_flat_bias_target_deg": _arg(
            args, "select_theta_flat_bias_target_deg", base.select_theta_flat_bias_target_deg
        ),
    }
    if model_family == "full":
        common.update(
            {
                "patch_size": _arg(args, "patch_size", base.patch_size),
                "patch_stride": _arg(args, "patch_stride", base.patch_stride),
                "dims": _tuple_arg(args, "dims", base.dims),
                "stage_blocks": _tuple_arg(args, "stage_blocks", base.stage_blocks),
                "large_kernels": _tuple_arg(args, "large_kernels", base.large_kernels),
                "small_kernels": _tuple_arg(args, "small_kernels", base.small_kernels),
                "ffn_ratio": _arg(args, "ffn_ratio", base.ffn_ratio),
                "layer_scale_init": _arg(args, "layer_scale_init", base.layer_scale_init),
            }
        )
        return ModernTCNFullConfig(**common)
    if model_family == "small_dualkernel":
        common.update(
            {
                "large_kernel": _arg(args, "large_kernel", base.large_kernel),
                "small_kernel": _arg(args, "small_kernel", base.small_kernel),
                "dual_branch_scale": _arg(args, "dual_branch_scale", base.dual_branch_scale),
                "small_branch_init": _arg(args, "small_branch_init", base.small_branch_init),
                "layer_scale_init": _arg(args, "layer_scale_init", base.layer_scale_init),
            }
        )
        return ModernTCNDualKernelConfig(**common)
    if model_family == "small_gffn":
        common.update(
            {
                "dmodel": _arg(args, "dmodel", base.dmodel),
                "ffn_ratio": _arg(args, "ffn_ratio", base.ffn_ratio),
                "layer_scale_init": _arg(args, "layer_scale_init", base.layer_scale_init),
            }
        )
        return ModernTCNGroupedConfig(**common)
    return ModernTCNConfig(**common)


def _train_epoch(model, loader, opt, device, class_w_main, class_w_turn, cfg) -> float:
    model.train()
    total_loss = 0.0
    total_n = 0
    for batch in loader:
        batch = _to_device(batch, device)
        batch = _apply_command_feature_dropout(batch, cfg)
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


def _apply_command_feature_dropout(batch: Dict[str, torch.Tensor], cfg: ModernTCNConfig) -> Dict[str, torch.Tensor]:
    prob = float(getattr(cfg, "command_dropout_prob", 0.0) or 0.0)
    if prob <= 0.0:
        return batch
    if not (0.0 <= prob < 1.0):
        raise ValueError(f"command_dropout_prob 必须在 [0,1) 内，实际 {prob}")

    x = batch["X"]
    start = int(getattr(cfg, "command_dropout_start_index", -1) or -1)
    count = int(getattr(cfg, "command_dropout_feature_count", 0) or 0)
    end = start + count
    if start < 0 or count <= 0 or end > int(x.shape[2]):
        raise ValueError(
            "command dropout 配置与输入维度不匹配："
            f"start={start}, count={count}, input_dim={int(x.shape[2])}"
        )

    mode = str(getattr(cfg, "command_dropout_mode", "window_block") or "window_block").lower()
    if mode == "window_block":
        keep = (torch.rand((x.shape[0], 1, 1), device=x.device) >= prob).to(dtype=x.dtype)
    elif mode == "time_block":
        keep = (torch.rand((x.shape[0], x.shape[1], 1), device=x.device) >= prob).to(dtype=x.dtype)
    elif mode == "channel_block":
        keep = (torch.rand((x.shape[0], 1, count), device=x.device) >= prob).to(dtype=x.dtype)
    else:
        raise ValueError(f"未知 command_dropout_mode: {mode}")

    x_drop = x.clone()
    x_drop[:, :, start:end] = x_drop[:, :, start:end] * keep
    out = dict(batch)
    out["X"] = x_drop
    return out


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


def _git_hash(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(root),
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unknown"


def _write_run_metadata(
    root: Path,
    out_dir: Path,
    args: argparse.Namespace,
    cfg: ModernTCNConfig,
    contract: Dict[str, object],
    feat_names,
    model_family: str,
    run_tag: str,
    files: Dict[str, Path],
) -> None:
    git_hash = _git_hash(root)
    config = {
        "model_family": model_family,
        "run_tag": run_tag,
        "output_dir": str(out_dir),
        "cli_args": vars(args),
        "model_config": cfg.to_dict(),
        "dataset_contract": contract,
        "feature_names": list(feat_names),
        "git_hash": git_hash,
        "python": sys.version,
        "torch_version": torch.__version__,
    }
    files["config_json"].write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    files["contract_copy_file"].write_text(json.dumps(contract, indent=2, ensure_ascii=False), encoding="utf-8")
    files["feature_names_file"].write_text("\n".join(str(x) for x in feat_names) + "\n", encoding="utf-8")
    files["git_hash_file"].write_text(git_hash + "\n", encoding="utf-8")
    with files["config_md"].open("w", encoding="utf-8") as f:
        f.write(f"# ModernTCN run config\n\n")
        f.write(f"- model_family: `{model_family}`\n")
        f.write(f"- run_tag: `{run_tag}`\n")
        f.write(f"- output_dir: `{out_dir}`\n")
        f.write(f"- git_hash: `{git_hash}`\n")
        f.write(f"- dataset: `{contract.get('dataset_file', '')}`\n")
        f.write(f"- input: `[batch,{contract.get('seq_len')},{contract.get('input_dim')}]`\n\n")
        f.write("## Model Config\n\n```json\n")
        f.write(json.dumps(cfg.to_dict(), indent=2, ensure_ascii=False))
        f.write("\n```\n")
    with files["train_log_file"].open("w", encoding="utf-8") as f:
        f.write("Training log placeholder. Console logs are not captured by train_one_seed API.\n")
        f.write(f"summary_csv: `{out_dir / (_file_prefix(model_family, args.seed) + '_summary.csv')}`\n")
        f.write(f"history_csv: `{out_dir / (_file_prefix(model_family, args.seed) + '_history.csv')}`\n")


def _write_report(
    path: Path,
    args: argparse.Namespace,
    cfg: ModernTCNConfig,
    contract: Dict[str, object],
    row: Dict[str, object],
    test_metrics: Dict[str, object],
    val_metrics: Dict[str, object],
    train_seconds: float,
    model_family: str,
) -> None:
    passed, failures = seed42_gate(test_metrics) if args.seed == 42 else (False, [])
    with path.open("w", encoding="utf-8") as f:
        if model_family == "full":
            title = "ModernTCNFull v0 第一阶段训练报告"
        elif model_family == "small_dualkernel":
            title = "ModernTCN dual-kernel small 第一阶段训练报告"
        elif model_family == "small_gffn":
            title = "ModernTCN grouped-FFN small 第一阶段训练报告"
        else:
            title = "ModernTCN-small 第一阶段训练报告"
        f.write(f"# {title}\n\n")
        f.write("## 固定约束\n\n")
        f.write(f"- model_family: `{model_family}`\n")
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
