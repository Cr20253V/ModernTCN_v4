from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
import torch
from torch.utils.data import DataLoader

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent.parent
SRC_ROOT = PROJECT_ROOT / "src"
MODERN_TCN_ROOT = SRC_ROOT / "ModernTCN"
for path in (SRC_ROOT, MODERN_TCN_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from modern_tcn_data import AGVWindowDataset, class_weights, load_modern_tcn_dataset
from modern_tcn_metrics import compute_metrics
from modern_tcn_model import build_model_from_checkpoint_dict


OUT_ROOT = ROOT / "06_local_residual_optimization_if_needed"
B1_ROOT = OUT_ROOT / "01_baseline_error_map"

BASELINE_CHECKPOINT = (
    PROJECT_ROOT
    / "results"
    / "paper"
    / "agv_model_parameter_correction_workflow"
    / "08_models"
    / "modern_tcn"
    / "modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101"
    / "modern_tcn_seed101.pt"
)
DATASET_FILE = (
    PROJECT_ROOT
    / "data"
    / "tcn"
    / "ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat"
)

FEATURES_OF_INTEREST = [
    "gyro_z",
    "I_sum",
    "I_diff_abs",
    "v_hat",
    "kappa_proxy",
    "drive_load_proxy",
    "yaw_consistency_error",
]


def write_csv(path: Path, rows: List[Dict[str, object]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: format_value(row.get(key, "")) for key in fieldnames})


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def format_value(value: object) -> str:
    if value is None:
        return "NaN"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"
        return f"{value:.15g}"
    if isinstance(value, np.floating):
        value = float(value)
        if math.isnan(value):
            return "NaN"
        return f"{value:.15g}"
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    if isinstance(value, (list, tuple)):
        return ";".join(format_value(v) for v in value)
    text = str(value)
    return text if text else "NaN"


def load_model(checkpoint_path: Path) -> torch.nn.Module:
    ckpt = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    model = build_model_from_checkpoint_dict(ckpt).eval()
    return model


@torch.no_grad()
def predict_split(model: torch.nn.Module, loader: DataLoader, class_w_main: torch.Tensor, class_w_turn: torch.Tensor, cfg):
    logits_main_all: List[np.ndarray] = []
    logits_turn_all: List[np.ndarray] = []
    theta_all: List[np.ndarray] = []
    for batch in loader:
        batch = {k: v.to("cpu") for k, v in batch.items()}
        logits_main, logits_turn, theta_hat = model(batch["X"])
        logits_main_all.append(logits_main.detach().cpu().numpy())
        logits_turn_all.append(logits_turn.detach().cpu().numpy())
        theta_all.append(theta_hat.detach().cpu().numpy().reshape(-1))
    return (
        np.concatenate(logits_main_all, axis=0),
        np.concatenate(logits_turn_all, axis=0),
        np.concatenate(theta_all, axis=0),
    )


def selected_feature_stats(window: np.ndarray, feat_names: List[str]) -> str:
    feat_index = {name: idx for idx, name in enumerate(feat_names)}
    stats: Dict[str, float] = {}
    for name in FEATURES_OF_INTEREST:
        if name not in feat_index:
            continue
        values = np.asarray(window[:, feat_index[name]], dtype=np.float64).reshape(-1)
        stats[f"{name}_mean"] = float(np.mean(values))
        stats[f"{name}_rms"] = float(np.sqrt(np.mean(np.square(values))))
    return json.dumps(stats, separators=(",", ":"), ensure_ascii=False)


def format_run_id(value: object) -> str:
    try:
        num = float(value)
    except Exception:
        return str(value)
    if math.isnan(num):
        return ""
    if abs(num - round(num)) < 1e-6:
        return str(int(round(num)))
    return f"{num:.6f}"


def build_error_map() -> Dict[str, object]:
    data = load_modern_tcn_dataset(DATASET_FILE)
    test_split = data["test"]
    feat_names = list(data["feat_names"])
    model = load_model(BASELINE_CHECKPOINT)
    cfg = model.cfg
    class_w_main = class_weights(data["train"].y_main, 3, cfg.main_class_weight_method, list(cfg.main_class_multipliers))
    class_w_turn = class_weights(data["train"].y_turn, 3, cfg.turn_class_weight_method, list(cfg.turn_class_multipliers))
    loader = DataLoader(AGVWindowDataset(test_split), batch_size=512, shuffle=False)

    logits_main, logits_turn, theta_hat = predict_split(model, loader, class_w_main, class_w_turn, cfg)
    metrics = compute_metrics(logits_main, logits_turn, theta_hat, test_split, float("nan"))
    metrics["theta_edge_p95_abs_err"] = max(
        float(metrics.get("theta_neg_10_8_p95_abs_err_deg", float("nan"))),
        float(metrics.get("theta_pos_8_10_p95_abs_err_deg", float("nan"))),
    )
    metrics["flat_peak_theta_error"] = float(metrics.get("theta_flat_abs_max_deg", float("nan")))

    prob_main = softmax_np(logits_main)
    prob_turn = softmax_np(logits_turn)
    pred_main = prob_main.argmax(axis=1)
    pred_turn_raw = prob_turn.argmax(axis=1) - 1
    y_main = test_split.y_main.reshape(-1)
    y_turn_raw = test_split.y_turn.reshape(-1) - 1
    theta_true_deg = np.rad2deg(np.asarray(test_split.y_theta).reshape(-1))
    theta_pred_deg = np.rad2deg(np.asarray(theta_hat).reshape(-1))
    theta_abs_err_deg = np.abs(theta_pred_deg - theta_true_deg)
    transition_mask = test_split.turn_transition.astype(bool).reshape(-1)
    slope_mask = test_split.mask_theta.astype(bool).reshape(-1)
    flat_mask = y_main == 0
    stall_mask = y_main == 1
    slope_edge_mask = slope_mask & (np.abs(theta_true_deg) >= 8.0) & (np.abs(theta_true_deg) <= 10.0)
    flat_peak_cutoff = float(np.quantile(theta_abs_err_deg[flat_mask], 0.95)) if np.any(flat_mask) else float("nan")
    flat_peak_mask = flat_mask & (theta_abs_err_deg >= flat_peak_cutoff)

    rows: List[Dict[str, object]] = []
    for idx in range(theta_abs_err_deg.size):
        rows.append(
            {
                "sample_id": f"test_{idx:05d}",
                "run_id_if_available": format_run_id(test_split.run_id[idx]),
                "main_true": int(y_main[idx]),
                "main_pred": int(pred_main[idx]),
                "turn_true": int(y_turn_raw[idx]),
                "turn_pred": int(pred_turn_raw[idx]),
                "theta_true_deg": float(theta_true_deg[idx]),
                "theta_pred_deg": float(theta_pred_deg[idx]),
                "theta_abs_err_deg": float(theta_abs_err_deg[idx]),
                "is_main_error": bool(pred_main[idx] != y_main[idx]),
                "is_turn_error": bool(pred_turn_raw[idx] != y_turn_raw[idx]),
                "is_transition_window": bool(transition_mask[idx]),
                "is_stall": bool(stall_mask[idx]),
                "is_slope": bool(slope_mask[idx]),
                "is_flat": bool(flat_mask[idx]),
                "is_theta_edge": bool(slope_edge_mask[idx]),
                "is_flat_peak": bool(flat_peak_mask[idx]),
                "main_conf": float(prob_main[idx].max()),
                "turn_conf": float(prob_turn[idx].max()),
                "input_feature_stats": selected_feature_stats(test_split.X[idx], feat_names),
            }
        )

    rows.sort(key=lambda r: (-float(r["theta_abs_err_deg"]), str(r["sample_id"])))
    for rank, row in enumerate(rows, start=1):
        row["theta_error_rank"] = rank

    output_rows = sorted(rows, key=lambda r: int(r["theta_error_rank"]))
    fieldnames = [
        "sample_id",
        "run_id_if_available",
        "main_true",
        "main_pred",
        "turn_true",
        "turn_pred",
        "theta_true_deg",
        "theta_pred_deg",
        "theta_abs_err_deg",
        "is_main_error",
        "is_turn_error",
        "is_transition_window",
        "is_stall",
        "is_slope",
        "is_flat",
        "is_theta_edge",
        "is_flat_peak",
        "main_conf",
        "turn_conf",
        "theta_error_rank",
        "input_feature_stats",
    ]
    write_csv(B1_ROOT / "baseline_error_map.csv", output_rows, fieldnames)

    top_n = 50 if len(rows) >= 50 else len(rows)
    top_rows = output_rows[:top_n]
    report = build_report(rows, metrics, flat_peak_cutoff, top_rows)
    write_text(B1_ROOT / "error_map_report.md", report)
    write_json(
        B1_ROOT / "baseline_error_map_summary.json",
        {
            "checkpoint": str(BASELINE_CHECKPOINT),
            "dataset": str(DATASET_FILE),
            "n_samples": len(rows),
            "flat_peak_cutoff_deg": flat_peak_cutoff,
            "metrics": clean_json(metrics),
        },
    )
    return {
        "n_samples": len(rows),
        "flat_peak_cutoff_deg": flat_peak_cutoff,
        "top_50_transition_share": float(np.mean([bool(r["is_transition_window"]) for r in top_rows])) if top_rows else float("nan"),
        "top_50_slope_edge_share": float(np.mean([bool(r["is_theta_edge"]) for r in top_rows])) if top_rows else float("nan"),
        "top_50_flat_peak_share": float(np.mean([bool(r["is_flat_peak"]) for r in top_rows])) if top_rows else float("nan"),
        "metrics": clean_json(metrics),
    }


def build_report(rows: List[Dict[str, object]], metrics: Dict[str, object], flat_peak_cutoff: float, top_rows: List[Dict[str, object]]) -> str:
    n = len(rows)
    main_err_rate = mean_bool(rows, "is_main_error")
    turn_err_rate = mean_bool(rows, "is_turn_error")
    transition_share_all = mean_bool(rows, "is_transition_window")
    slope_edge_share_all = mean_bool(rows, "is_theta_edge")
    flat_peak_share_all = mean_bool(rows, "is_flat_peak")
    transition_share_top = mean_bool(top_rows, "is_transition_window")
    slope_edge_share_top = mean_bool(top_rows, "is_theta_edge")
    flat_peak_share_top = mean_bool(top_rows, "is_flat_peak")

    top_lines = []
    for row in top_rows[:10]:
        top_lines.append(
            f"| {row['sample_id']} | {row['run_id_if_available']} | {row['theta_abs_err_deg']:.4f} | "
            f"{int(row['is_transition_window'])} | {int(row['is_theta_edge'])} | {int(row['is_flat_peak'])} | "
            f"{int(row['is_main_error'])} | {int(row['is_turn_error'])} |"
        )

    return "\n".join(
        [
            "# Phase B1 Baseline Error Map",
            "",
            f"- checkpoint: `{BASELINE_CHECKPOINT}`",
            f"- dataset: `{DATASET_FILE}`",
            f"- samples: `{n}`",
            f"- flat_peak_cutoff_deg: `{flat_peak_cutoff:.4f}`",
            "",
            "## Recomputed Aggregate Metrics",
            "",
            f"- acc_main: `{float(metrics['acc_main']):.6f}`",
            f"- acc_turn: `{float(metrics['acc_turn']):.6f}`",
            f"- acc_turn_transition: `{float(metrics['acc_turn_transition']):.6f}`",
            f"- theta_mae_deg: `{float(metrics['theta_mae_deg']):.6f}`",
            f"- flat_recall: `{float(metrics['flat_recall']):.6f}`",
            f"- stall_recall: `{float(metrics['stall_recall']):.6f}`",
            f"- slope_recall: `{float(metrics['slope_recall']):.6f}`",
            f"- theta_edge_p95_abs_err_deg: `{float(metrics['theta_edge_p95_abs_err']):.6f}`",
            f"- flat_peak_theta_error_deg: `{float(metrics['flat_peak_theta_error']):.6f}`",
            "",
            "## Error Concentration",
            "",
            f"- overall main error rate: `{main_err_rate:.4f}`",
            f"- overall turn error rate: `{turn_err_rate:.4f}`",
            f"- transition window share: `{transition_share_all:.4f}`",
            f"- slope-edge share: `{slope_edge_share_all:.4f}`",
            f"- flat-peak share: `{flat_peak_share_all:.4f}`",
            f"- top-50 transition share: `{transition_share_top:.4f}`",
            f"- top-50 slope-edge share: `{slope_edge_share_top:.4f}`",
            f"- top-50 flat-peak share: `{flat_peak_share_top:.4f}`",
            "",
            "## Top Theta Errors",
            "",
            "| sample_id | run_id | theta_abs_err_deg | transition | slope_edge | flat_peak | main_err | turn_err |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
            *top_lines,
            "",
            "## Initial Read",
            "",
            "- B1 is ready for residual design only if the top-error mass is concentrated in one or two flags.",
            "- If transition windows dominate, residual turn correction is the primary branch.",
            "- If slope-edge or flat-peak windows dominate, residual theta correction is the primary branch.",
            "- If both patterns remain strong, a head-specific physics residual is the better next step.",
        ]
    )


def mean_bool(rows: List[Dict[str, object]], key: str) -> float:
    if not rows:
        return float("nan")
    return float(np.mean([bool(r[key]) for r in rows]))


def clean_json(metrics: Dict[str, object]) -> Dict[str, object]:
    clean: Dict[str, object] = {}
    for key, value in metrics.items():
        if isinstance(value, (np.floating, float, int, np.integer)) and not isinstance(value, bool):
            clean[key] = float(value)
        elif isinstance(value, list):
            clean[key] = value
        elif isinstance(value, np.ndarray):
            clean[key] = value.tolist()
        else:
            clean[key] = value
    return clean


def softmax_np(logits: np.ndarray) -> np.ndarray:
    x = np.asarray(logits, dtype=np.float64)
    x = x - np.max(x, axis=1, keepdims=True)
    exp = np.exp(x)
    return exp / np.sum(exp, axis=1, keepdims=True)


def main() -> int:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    B1_ROOT.mkdir(parents=True, exist_ok=True)
    summary = build_error_map()
    write_text(
        OUT_ROOT / "section6_execution_summary.md",
        "\n".join(
            [
                "# Section 6 Execution Summary",
                "",
                f"- baseline error map written: `{B1_ROOT / 'baseline_error_map.csv'}`",
                f"- baseline error report written: `{B1_ROOT / 'error_map_report.md'}`",
                f"- samples analyzed: `{summary['n_samples']}`",
                f"- top-50 transition share: `{summary['top_50_transition_share']:.4f}`",
                f"- top-50 slope-edge share: `{summary['top_50_slope_edge_share']:.4f}`",
                f"- top-50 flat-peak share: `{summary['top_50_flat_peak_share']:.4f}`",
                "",
                "- no residual branch has been trained yet; this is the B1 evidence map only.",
            ]
        )
        + "\n",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
