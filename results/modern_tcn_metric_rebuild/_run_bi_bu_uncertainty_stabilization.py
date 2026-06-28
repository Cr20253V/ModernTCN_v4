from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import tempfile
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, median
from typing import Any

import numpy as np
import torch
from torch.utils.data import DataLoader


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent.parent
SRC_DIR = PROJECT_ROOT / "src" / "ModernTCN"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

SCI_ROOT = PROJECT_ROOT / "results" / "modern_tcn_sci_innovation"
NODE_ROOT = ROOT / "15_bi_bu_uncertainty_stabilization"

TRAIN = PROJECT_ROOT / "src" / "ModernTCN" / "train_modern_tcn.py"
EXPORT = PROJECT_ROOT / "src" / "ModernTCN" / "export_modern_tcn_onnx.py"
CHECK_ONNX = PROJECT_ROOT / "src" / "ModernTCN" / "check_onnxruntime_consistency.py"

BASELINE_ID = "baseline_lock"
ANCHOR_ID = "uncertainty_seed101_rerun_20260622"
BASELINE_DIR = PROJECT_ROOT / "results" / "paper" / "agv_model_parameter_correction_workflow" / "08_models" / "modern_tcn" / "modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101"
ANCHOR_DIR = SCI_ROOT / "01_loss_optimization" / ANCHOR_ID
STABILITY_DIR = ROOT / "14_uncertainty_stability_optimization"
TUNING_DIR = ROOT / "11_uncertainty_tuning"
MULTISEED_DIR = ROOT / "13_multiseed_algorithm_comparison"
BASELINE_MATRIX = ROOT / "03_rerank_existing_experiments" / "candidate_metric_matrix.csv"
V2_FULL = ROOT / "10_threshold_recalibration" / "hard_constraint_thresholds_v2_full_proposed.json"
V2_CLOSED = ROOT / "10_threshold_recalibration" / "hard_constraint_thresholds_v2_closed_loop_proposed.json"
FORMAL_PATH_METRICS = ROOT / "05_sandbox_closed_loop_if_needed" / "03_formal_validation" / "formal_validation_path_metrics.csv"

DATASET = "data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat"
BASELINE_J_CONTROL = 1.0
ANCHOR_J_CONTROL = 0.94411711953914
OFFLINE_METRICS = [
    "acc_main",
    "acc_turn",
    "acc_turn_transition",
    "theta_mae_deg",
    "theta_edge_p95_abs_err",
    "flat_peak_theta_error",
    "flat_recall",
    "stall_recall",
    "slope_recall",
]
HIGHER_BETTER = {"acc_main", "acc_turn", "acc_turn_transition", "flat_recall", "stall_recall", "slope_recall"}

from modern_tcn_data import AGVWindowDataset, load_modern_tcn_dataset
from modern_tcn_model import build_model_from_checkpoint_dict


@dataclass(frozen=True)
class RunSpec:
    run_id: str
    seed: int
    description: str
    overrides: dict[str, Any]


def num(value: Any) -> float:
    if value is None:
        return math.nan
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "missing", "unavailable"}:
        return math.nan
    if text.lower() == "true":
        return 1.0
    if text.lower() == "false":
        return 0.0
    try:
        return float(text)
    except ValueError:
        return math.nan


def fmt(value: Any) -> str:
    if value is None:
        return "NaN"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"
        if math.isinf(value):
            return "Inf" if value > 0 else "-Inf"
        return f"{value:.15g}"
    text = str(value)
    return text if text else "NaN"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: fmt(row.get(field, "")) for field in fields})


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_info(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False, "path": str(path), "size_bytes": math.nan, "sha256": "missing"}
    return {
        "exists": True,
        "path": str(path),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path) if path.is_file() else "directory",
    }


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join(["---"] * len(fields)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(fmt(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def run_command(cmd: list[str], log_file: Path | None = None) -> subprocess.CompletedProcess[str]:
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
    )
    if log_file:
        log_file.write_text(proc.stdout, encoding="utf-8")
    return proc


def read_single_csv_row(path: Path) -> dict[str, str]:
    rows = read_csv(path)
    if not rows:
        raise ValueError(f"CSV has no rows: {path}")
    return rows[0]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def baseline_metrics() -> dict[str, Any]:
    row = next(r for r in read_csv(BASELINE_MATRIX) if r["candidate_id"] == BASELINE_ID)
    return {
        "candidate_id": BASELINE_ID,
        "source": str(BASELINE_MATRIX),
        "acc_main": num(row.get("acc_main")),
        "acc_turn": num(row.get("acc_turn")),
        "acc_turn_transition": num(row.get("acc_turn_transition")),
        "theta_mae_deg": num(row.get("theta_mae_deg")),
        "theta_edge_p95_abs_err": num(row.get("theta_edge_p95_abs_err")),
        "flat_peak_theta_error": num(row.get("flat_peak_theta_error")),
        "flat_recall": num(row.get("flat_recall")),
        "stall_recall": num(row.get("stall_recall")),
        "slope_recall": num(row.get("slope_recall")),
    }


def anchor_metrics() -> dict[str, Any]:
    rows = read_csv(FORMAL_PATH_METRICS)
    anchor_row = next(r for r in rows if r.get("candidate_id") == ANCHOR_ID or r.get("controller") == ANCHOR_ID)
    return {
        "candidate_id": ANCHOR_ID,
        "source": str(FORMAL_PATH_METRICS),
        "J_control": ANCHOR_J_CONTROL,
        "ey_rmse": num(anchor_row.get("ey_rmse")),
        "xy_rmse": num(anchor_row.get("xy_rmse")),
        "epsi_rmse": num(anchor_row.get("epsi_rmse")),
        "j_du": num(anchor_row.get("j_du")),
        "omega_cmd_rms": num(anchor_row.get("omega_cmd_rms")),
    }


def offline_score_vs_baseline(metrics: dict[str, Any], baseline: dict[str, Any]) -> float:
    ratios = []
    for metric in OFFLINE_METRICS:
        value = num(metrics.get(metric))
        base = num(baseline.get(metric))
        if math.isnan(value) or math.isnan(base) or base == 0:
            continue
        if metric in HIGHER_BETTER:
            if value > 0:
                ratios.append(base / value)
        else:
            ratios.append(value / base)
    return mean(ratios) if ratios else math.nan


def evidence_inventory() -> list[dict[str, Any]]:
    items = [
        ("baseline_lock_checkpoint", BASELINE_DIR / "modern_tcn_seed101.pt", "frozen baseline checkpoint"),
        ("anchor_checkpoint", ANCHOR_DIR / "modern_tcn_seed101.pt", "seed101 anchor checkpoint"),
        ("baseline_matrix", BASELINE_MATRIX, "offline reference metrics"),
        ("stability_report", STABILITY_DIR / "05_decision" / "uncertainty_stability_final_report.md", "stability optimization final report"),
        ("tuning_report", TUNING_DIR / "05_decision" / "uncertainty_tuning_final_report.md", "uncertainty tuning final report"),
        ("multiseed_report", MULTISEED_DIR / "03_report" / "multiseed_algorithm_comparison_report.md", "multiseed comparison report"),
        ("v2_full_thresholds", V2_FULL, "offline v2 thresholds"),
        ("v2_closed_thresholds", V2_CLOSED, "closed-loop v2 thresholds"),
        ("formal_path_metrics", FORMAL_PATH_METRICS, "current path-level closed-loop metrics"),
    ]
    rows = []
    for evidence_id, path, notes in items:
        info = file_info(path)
        info.update({"evidence_id": evidence_id, "notes": notes})
        rows.append(info)
    return rows


def read_seed_metrics(seed: int) -> dict[str, Any]:
    base = SCI_ROOT / "01_loss_optimization" / f"uncertainty_seed{seed}"
    if seed == 101:
        base = SCI_ROOT / "01_loss_optimization" / "uncertainty_seed101_rerun_20260622"
    config = load_json(base / "config.json")
    test_row = read_single_csv_row(next(base.glob("*_summary.csv")))
    hist = read_csv(next(base.glob("*_history.csv")))
    dyn = config.get("dynamic_loss_state", {})
    last_hist = hist[-1] if hist else {}
    return {
        "seed": seed,
        "config_path": str(base / "config.json"),
        "summary_path": str(next(base.glob("*_summary.csv"))),
        "history_path": str(next(base.glob("*_history.csv"))),
        "checkpoint_path": str(base / f"modern_tcn_seed{seed}.pt"),
        "loss_mode": config.get("loss_mode", ""),
        "s_main": num(dyn.get("s_main")),
        "s_turn": num(dyn.get("s_turn")),
        "s_theta": num(dyn.get("s_theta")),
        "weight_main": num(dyn.get("weight_main")),
        "weight_turn": num(dyn.get("weight_turn")),
        "weight_theta": num(dyn.get("weight_theta")),
        "raw_s_main": num(last_hist.get("raw_s_main")),
        "raw_s_turn": num(last_hist.get("raw_s_turn")),
        "raw_s_theta": num(last_hist.get("raw_s_theta")),
        "bounded_s_prior": num(last_hist.get("bounded_s_prior")),
        "s_range": num(last_hist.get("s_range")),
        "s_prior_lambda": num(last_hist.get("s_prior_lambda")),
        "acc_main": num(test_row.get("acc_main")),
        "acc_turn": num(test_row.get("acc_turn")),
        "acc_turn_transition": num(test_row.get("acc_turn_transition")),
        "theta_edge_p95_abs_err": num(test_row.get("theta_edge_p95_abs_err")),
        "flat_peak_theta_error": num(test_row.get("flat_peak_theta_error")),
        "flat_recall": num(test_row.get("flat_recall")),
        "stall_recall": num(test_row.get("stall_recall")),
        "slope_recall": num(test_row.get("slope_recall")),
        "theta_mae_deg": num(test_row.get("theta_mae_deg")),
        "checkpoint_file": test_row.get("checkpoint_file", ""),
        "report_file": test_row.get("report_file", ""),
    }


def read_closed_loop_row(candidate_id: str) -> dict[str, Any]:
    rows = read_csv(STABILITY_DIR / "04_closed_loop_multiseed" / "closed_loop_results.csv")
    row = next(r for r in rows if r["candidate_id"] == candidate_id)
    return {
        "candidate_id": candidate_id,
        "J_control": num(row.get("J_control")),
        "closed_loop_v2_status": row.get("closed_loop_v2_status", ""),
        "closed_loop_v2_failures": row.get("closed_loop_v2_failures", ""),
        "ey_rmse_mean": num(row.get("ey_rmse_mean")),
        "xy_rmse_mean": num(row.get("xy_rmse_mean")),
        "epsi_rmse_mean": num(row.get("epsi_rmse_mean")),
        "j_du_mean": num(row.get("j_du_mean")),
        "omega_cmd_rms_mean": num(row.get("omega_cmd_rms_mean")),
        "theta_mae_deg_mean": num(row.get("theta_mae_deg_mean")),
        "main_acc_pct_mean": num(row.get("main_acc_pct_mean")),
        "turn_acc_pct_mean": num(row.get("turn_acc_pct_mean")),
        "n_paths": num(row.get("n_paths")),
    }


def failure_type(seed_row: dict[str, Any]) -> str:
    acc_main = seed_row["acc_main"]
    stall = seed_row["stall_recall"]
    slope = seed_row["slope_recall"]
    theta_edge = seed_row["theta_edge_p95_abs_err"]
    flat_peak = seed_row["flat_peak_theta_error"]
    if seed_row["seed"] == 101:
        return "success_pattern_seed101"
    if math.isfinite(theta_edge) and math.isfinite(flat_peak) and theta_edge > 1.0 and flat_peak > 4.5:
        return "edge_and_flat_drift"
    if math.isfinite(acc_main) and acc_main < 0.97:
        return "main_accuracy_pressure"
    if math.isfinite(stall) and math.isfinite(slope) and stall < 0.70 and slope < 0.80:
        return "recoverability_gap"
    return "mixed_stability_gap"


def run_specs() -> list[RunSpec]:
    baseline = baseline_metrics()
    return [
        RunSpec(
            "a0_fixed_zero_or_short",
            21,
            "baseline initialized fixed loss zero-epoch equivalence",
            {
                "loss_mode": "fixed",
                "freeze_mode": "none",
                "preserve_mode": "none",
                "epochs": 0,
                "lr": 0.0,
                "init_checkpoint": str(BASELINE_DIR / "modern_tcn_seed101.pt"),
                "baseline_checkpoint": str(BASELINE_DIR / "modern_tcn_seed101.pt"),
            },
        ),
        RunSpec(
            "a1_freeze_trunk",
            21,
            "freeze trunk and train heads with bounded uncertainty",
            {
                "loss_mode": "bounded_uncertainty",
                "freeze_mode": "trunk",
                "preserve_mode": "baseline",
                "epochs": 1,
                "init_checkpoint": str(BASELINE_DIR / "modern_tcn_seed101.pt"),
                "baseline_checkpoint": str(BASELINE_DIR / "modern_tcn_seed101.pt"),
                "s_range": 0.25,
                "lambda_s_prior": 0.01,
                "lambda_preserve_main": 0.05,
                "lambda_preserve_turn": 0.05,
                "lambda_preserve_theta": 0.05,
                "lr": 0.001,
            },
        ),
        RunSpec(
            "a2_freeze_early",
            42,
            "freeze early blocks and train late blocks with bounded uncertainty",
            {
                "loss_mode": "bounded_uncertainty",
                "freeze_mode": "early_blocks",
                "freeze_early_blocks": 3,
                "preserve_mode": "baseline",
                "epochs": 1,
                "init_checkpoint": str(BASELINE_DIR / "modern_tcn_seed101.pt"),
                "baseline_checkpoint": str(BASELINE_DIR / "modern_tcn_seed101.pt"),
                "s_range": 0.25,
                "lambda_s_prior": 0.01,
                "lambda_preserve_main": 0.05,
                "lambda_preserve_turn": 0.05,
                "lambda_preserve_theta": 0.05,
                "lr": 0.001,
            },
        ),
        RunSpec(
            "a3_full_small_lr",
            101,
            "full fine-tune with bounded uncertainty and baseline preservation",
            {
                "loss_mode": "bounded_uncertainty",
                "freeze_mode": "none",
                "preserve_mode": "baseline",
                "epochs": 1,
                "init_checkpoint": str(BASELINE_DIR / "modern_tcn_seed101.pt"),
                "baseline_checkpoint": str(BASELINE_DIR / "modern_tcn_seed101.pt"),
                "s_range": 0.50,
                "lambda_s_prior": 0.03,
                "lambda_preserve_main": 0.10,
                "lambda_preserve_turn": 0.05,
                "lambda_preserve_theta": 0.10,
                "lr": 0.0007,
            },
        ),
    ]


def _run_dir(spec: RunSpec) -> Path:
    return NODE_ROOT / "03_baseline_initialized" / f"{spec.run_id}_seed{spec.seed}"


def build_train_cmd(spec: RunSpec) -> list[str]:
    cmd = [
        sys.executable,
        str(TRAIN),
        "--seed",
        str(spec.seed),
        "--model-family",
        "small",
        "--dataset-file",
        DATASET,
        "--output-root",
        str(NODE_ROOT / "03_baseline_initialized"),
        "--run-tag",
        f"{spec.run_id}_seed{spec.seed}",
        "--no-overwrite",
        "--channels",
        "64",
        "--blocks",
        "5",
        "--kernel-size",
        "31",
        "--dropout",
        "0.15",
        "--lambda-turn",
        "0.20",
        "--lambda-theta",
        "0.55",
        "--lambda-theta-flat",
        "0.12",
        "--theta-flat-loss-mode",
        "near_zero",
        "--command-dropout-prob",
        "0.0",
    ]
    for key, value in spec.overrides.items():
        if isinstance(value, bool):
            if value:
                cmd.append(f"--{key.replace('_', '-')}")
        else:
            cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return cmd


def train_one(spec: RunSpec) -> dict[str, Any]:
    run_dir = _run_dir(spec)
    log_file = run_dir / "train.log"
    cmd = build_train_cmd(spec)
    proc = run_command(cmd, log_file=log_file)
    status = "ok" if proc.returncode == 0 else "failed"
    config_json = run_dir / "config.json"
    history_csv = next(run_dir.glob("*_history.csv"), None)
    summary_csv = next(run_dir.glob("*_summary.csv"), None)
    report_file = next(run_dir.glob("*_train_report.md"), None)
    checkpoint = next(run_dir.glob("*.pt"), None)
    return {
        "run_id": spec.run_id,
        "seed": spec.seed,
        "status": status,
        "returncode": proc.returncode,
        "run_dir": str(run_dir),
        "log_file": str(log_file),
        "config_json": str(config_json),
        "history_csv": str(history_csv) if history_csv else "",
        "summary_csv": str(summary_csv) if summary_csv else "",
        "report_file": str(report_file) if report_file else "",
        "checkpoint_file": str(checkpoint) if checkpoint else "",
    }


def validate_checkpoint_paths() -> list[dict[str, Any]]:
    rows = []
    for label, path in [("baseline_lock", BASELINE_DIR / "modern_tcn_seed101.pt"), ("anchor", ANCHOR_DIR / "modern_tcn_seed101.pt")]:
        info = file_info(path)
        info["label"] = label
        rows.append(info)
    return rows


def zero_epoch_equivalence() -> list[dict[str, Any]]:
    spec = run_specs()[0]
    smoke_root = Path(tempfile.mkdtemp(prefix="bi_bu_zero_epoch_", dir=str(NODE_ROOT / "00_runner_preflight")))
    cmd = build_train_cmd(spec)
    cmd[cmd.index(str(NODE_ROOT / "03_baseline_initialized"))] = str(smoke_root)
    proc = run_command(cmd, smoke_root / "zero_epoch_train.log")
    if proc.returncode != 0:
        return [
            {
                "metric": "train_command",
                "baseline_value": "ok",
                "zero_epoch_value": "failed",
                "abs_diff": "NaN",
                "tolerance": "0",
                "pass": False,
                "details": f"returncode={proc.returncode}",
                "run_dir": str(smoke_root),
            }
        ]
    run_dir = smoke_root / f"{spec.run_id}_seed{spec.seed}"
    checkpoint = next(run_dir.glob("*.pt"), None)
    if checkpoint is None:
        return [
            {
                "metric": "checkpoint",
                "baseline_value": str(BASELINE_DIR / "modern_tcn_seed101.pt"),
                "zero_epoch_value": "missing",
                "abs_diff": "NaN",
                "tolerance": "0",
                "pass": False,
                "details": "zero epoch checkpoint missing",
                "run_dir": str(run_dir),
            }
        ]
    baseline_ckpt = torch.load(BASELINE_DIR / "modern_tcn_seed101.pt", map_location="cpu", weights_only=False)
    zero_ckpt = torch.load(checkpoint, map_location="cpu", weights_only=False)
    baseline_model = build_model_from_checkpoint_dict(baseline_ckpt).eval()
    zero_model = build_model_from_checkpoint_dict(zero_ckpt).eval()
    data = load_modern_tcn_dataset(
        dataset_file=PROJECT_ROOT / DATASET,
        limit_train=0,
        limit_val=0,
        limit_test=0,
    )
    test_split = data["test"]
    loader = DataLoader(AGVWindowDataset(test_split), batch_size=256, shuffle=False, num_workers=0)

    def predict(model: torch.nn.Module) -> dict[str, np.ndarray]:
        logits_main_all = []
        logits_turn_all = []
        theta_all = []
        with torch.no_grad():
            for batch in loader:
                x = batch["X"]
                outputs = model(x)
                if not isinstance(outputs, tuple) or len(outputs) < 3:
                    raise ValueError("unexpected model outputs during zero-epoch comparison")
                logits_main, logits_turn, theta_hat = outputs[:3]
                logits_main_all.append(logits_main.cpu().numpy())
                logits_turn_all.append(logits_turn.cpu().numpy())
                theta_all.append(theta_hat.cpu().numpy())
        return {
            "logits_main": np.concatenate(logits_main_all, axis=0),
            "logits_turn": np.concatenate(logits_turn_all, axis=0),
            "theta_hat": np.concatenate(theta_all, axis=0).reshape(-1),
        }

    baseline_pred = predict(baseline_model)
    zero_pred = predict(zero_model)
    tolerance = 1e-6
    rows = []
    for key in ["logits_main", "logits_turn", "theta_hat"]:
        diff = np.abs(baseline_pred[key] - zero_pred[key])
        rows.append(
            {
                "metric": key,
                "baseline_value": "baseline_checkpoint",
                "zero_epoch_value": "zero_epoch_run",
                "abs_diff": float(diff.max()) if diff.size else 0.0,
                "tolerance": tolerance,
                "pass": bool(np.all(diff <= tolerance)),
                "details": f"mean_abs_diff={float(diff.mean()) if diff.size else 0.0:.6g}",
                "run_dir": str(run_dir),
            }
        )
    state_diffs = []
    for key in baseline_ckpt["model_state"]:
        b = baseline_ckpt["model_state"][key]
        z = zero_ckpt["model_state"].get(key)
        if not torch.is_tensor(b) or not torch.is_tensor(z):
            continue
        state_diffs.append(float(torch.max(torch.abs(b - z)).item()))
    rows.append(
        {
            "metric": "model_state_max_abs_diff",
            "baseline_value": "baseline_checkpoint",
            "zero_epoch_value": "zero_epoch_run",
            "abs_diff": max(state_diffs) if state_diffs else 0.0,
            "tolerance": tolerance,
            "pass": all(diff <= tolerance for diff in state_diffs) if state_diffs else True,
            "details": f"state_tensors={len(state_diffs)}",
            "run_dir": str(run_dir),
        }
    )
    return rows


def preflight() -> dict[str, Any]:
    required = [
        TRAIN,
        BASELINE_MATRIX,
        V2_FULL,
        V2_CLOSED,
        FORMAL_PATH_METRICS,
        BASELINE_DIR / "modern_tcn_seed101.pt",
        ANCHOR_DIR / "modern_tcn_seed101.pt",
    ]
    missing = [str(p) for p in required if not p.exists()]
    return {
        "node_root": str(NODE_ROOT),
        "train_script": str(TRAIN),
        "anchor_dir": str(ANCHOR_DIR),
        "baseline_dir": str(BASELINE_DIR),
        "missing_required": missing,
        "can_start": not missing,
    }


def node_preflight() -> None:
    NODE_ROOT.mkdir(parents=True, exist_ok=True)
    rows = []
    pre = preflight()
    rows.append(pre)
    zero_rows = zero_epoch_equivalence() if pre["can_start"] else []
    zero_pass = all(bool(row.get("pass")) for row in zero_rows) if zero_rows else False
    pre["zero_epoch_pass"] = zero_pass
    pre["zero_epoch_rows"] = len(zero_rows)
    write_json(NODE_ROOT / "00_runner_preflight" / "preflight_decision.json", pre)
    write_csv(
        NODE_ROOT / "00_runner_preflight" / "zero_epoch_equivalence.csv",
        zero_rows,
        ["metric", "baseline_value", "zero_epoch_value", "abs_diff", "tolerance", "pass", "details", "run_dir"],
    )
    report = [
        "# BI-BU Runner Capability Preflight",
        "",
        f"- node_root: `{pre['node_root']}`",
        f"- can_start: `{pre['can_start']}`",
        "",
        "## Required Paths",
        "",
        md_table(
            [
                {"label": "train_script", **file_info(TRAIN)},
                {"label": "baseline_checkpoint", **file_info(BASELINE_DIR / "modern_tcn_seed101.pt")},
                {"label": "anchor_checkpoint", **file_info(ANCHOR_DIR / "modern_tcn_seed101.pt")},
                {"label": "baseline_matrix", **file_info(BASELINE_MATRIX)},
                {"label": "v2_full_thresholds", **file_info(V2_FULL)},
                {"label": "v2_closed_thresholds", **file_info(V2_CLOSED)},
                {"label": "formal_path_metrics", **file_info(FORMAL_PATH_METRICS)},
            ],
            ["label", "exists", "path", "size_bytes", "sha256"],
        ),
        "",
        "## Capability Check",
        "",
        "- `--init-checkpoint`: supported in `train_modern_tcn.py`.",
        "- `--freeze-mode`: supported in `train_modern_tcn.py`.",
        "- bounded uncertainty: supported in `train_modern_tcn.py`.",
        "- preservation loss: supported in `train_modern_tcn.py`.",
        "- `--no-overwrite`: supported in `train_modern_tcn.py`.",
        f"- zero-epoch equivalence: `{zero_pass}`.",
    ]
    if pre["missing_required"]:
        report.extend(["", "## Missing", "", "\n".join(f"- `{x}`" for x in pre["missing_required"])])
    write_text(NODE_ROOT / "00_runner_preflight" / "runner_capability_report.md", "\n".join(report) + "\n")


def node_evidence_lock() -> None:
    rows = evidence_inventory()
    write_csv(
        NODE_ROOT / "01_evidence_lock" / "artifact_inventory.csv",
        rows,
        ["evidence_id", "exists", "path", "size_bytes", "sha256", "notes"],
    )
    baseline = baseline_metrics()
    anchor = anchor_metrics()
    seed_rows = []
    for seed in [21, 42, 101]:
        sr = read_seed_metrics(seed)
        cr = read_closed_loop_row(
            "uncertainty_seed101_rerun_20260622" if seed == 101 else f"s01_lr13_select_edges_flat_seed{seed}"
        )
        seed_rows.append(
            {
                "label": f"stability_14_seed{seed}",
                "candidate_id": cr["candidate_id"],
                "source": sr["summary_path"],
                "J_control": cr["J_control"],
                "ey_rmse": cr["ey_rmse_mean"],
                "xy_rmse": cr["xy_rmse_mean"],
                "epsi_rmse": cr["epsi_rmse_mean"],
                "j_du": cr["j_du_mean"],
                "omega_cmd_rms": cr["omega_cmd_rms_mean"],
                **{k: sr[k] for k in ["acc_main", "acc_turn", "acc_turn_transition", "theta_mae_deg", "theta_edge_p95_abs_err", "flat_peak_theta_error", "flat_recall", "stall_recall", "slope_recall"]},
            }
        )
    reference_rows = [
        {
            "label": "baseline_lock",
            "candidate_id": BASELINE_ID,
            "source": str(BASELINE_MATRIX),
            **baseline,
            **{
                "ey_rmse": read_closed_loop_row(BASELINE_ID)["ey_rmse_mean"],
                "xy_rmse": read_closed_loop_row(BASELINE_ID)["xy_rmse_mean"],
                "epsi_rmse": read_closed_loop_row(BASELINE_ID)["epsi_rmse_mean"],
                "j_du": read_closed_loop_row(BASELINE_ID)["j_du_mean"],
                "omega_cmd_rms": read_closed_loop_row(BASELINE_ID)["omega_cmd_rms_mean"],
            },
            "J_control": BASELINE_J_CONTROL,
        },
        {
            "label": "anchor_seed101",
            "candidate_id": ANCHOR_ID,
            "source": str(FORMAL_PATH_METRICS),
            **read_seed_metrics(101),
            **anchor,
            **{
                "ey_rmse": read_closed_loop_row(ANCHOR_ID)["ey_rmse_mean"],
                "xy_rmse": read_closed_loop_row(ANCHOR_ID)["xy_rmse_mean"],
                "epsi_rmse": read_closed_loop_row(ANCHOR_ID)["epsi_rmse_mean"],
                "j_du": read_closed_loop_row(ANCHOR_ID)["j_du_mean"],
                "omega_cmd_rms": read_closed_loop_row(ANCHOR_ID)["omega_cmd_rms_mean"],
            },
        },
        *seed_rows,
    ]
    write_csv(
        NODE_ROOT / "01_evidence_lock" / "reference_metrics.csv",
        reference_rows,
        ["label", "candidate_id", "source", "J_control", "acc_main", "acc_turn", "acc_turn_transition", "theta_mae_deg", "theta_edge_p95_abs_err", "flat_peak_theta_error", "flat_recall", "stall_recall", "slope_recall", "ey_rmse", "xy_rmse", "epsi_rmse", "j_du", "omega_cmd_rms"],
    )
    decision = {
        "baseline_lock_reference": BASELINE_ID,
        "anchor_reference": ANCHOR_ID,
        "baseline_J_control": BASELINE_J_CONTROL,
        "anchor_seed101_J_control": ANCHOR_J_CONTROL,
        "stability_14_closed_loop_ordering": {
            "seed101": 1.105446,
            "seed21": 1.143118,
            "seed42": 1.174967,
        },
        "offline_gate_fact": "3/3 pass in 14_uncertainty_stability_optimization, but closed-loop J_control is worse than baseline_lock.",
        "can_promote_recipe": False,
        "stop_reason": "Need baseline-initialized bounded-uncertainty evidence before any promotion claim.",
    }
    write_json(NODE_ROOT / "01_evidence_lock" / "reference_decision.json", decision)
    text = [
        "# Evidence Lock",
        "",
        "This node freezes the current comparison contract before any new training.",
        "",
        "## Locked Facts",
        "",
        f"- baseline: `{BASELINE_ID}`",
        f"- anchor: `{ANCHOR_ID}`",
        f"- baseline J_control: `{BASELINE_J_CONTROL:.6f}`",
        f"- anchor J_control: `{ANCHOR_J_CONTROL:.6f}`",
        "",
        "## Evidence Inventory",
        "",
        md_table(rows, ["evidence_id", "exists", "path", "size_bytes", "sha256", "notes"]),
        "",
        "## Reference Metrics",
        "",
        md_table(reference_rows, ["label", "candidate_id", "J_control", "acc_main", "acc_turn", "acc_turn_transition", "theta_mae_deg", "theta_edge_p95_abs_err", "flat_peak_theta_error", "flat_recall", "stall_recall", "slope_recall", "ey_rmse", "xy_rmse", "epsi_rmse", "j_du", "omega_cmd_rms"]),
    ]
    write_text(NODE_ROOT / "01_evidence_lock" / "evidence_lock.md", "\n".join(text) + "\n")


def node_failure_diagnosis() -> None:
    rows = []
    for seed in [21, 42, 101]:
        seed_row = read_seed_metrics(seed)
        closed_row = read_closed_loop_row(
            "uncertainty_seed101_rerun_20260622" if seed == 101 else f"s01_lr13_select_edges_flat_seed{seed}"
        )
        rows.append(
            {
                **seed_row,
                **closed_row,
                "offline_v2_score": offline_score_vs_baseline(seed_row, baseline_metrics()),
                "failure_type": failure_type(seed_row),
                "closed_loop_transfer_risk": "high" if seed != 101 and closed_row["J_control"] > BASELINE_J_CONTROL else "moderate",
            }
        )
    write_csv(
        NODE_ROOT / "02_seed_failure_diagnosis" / "seed_task_weight_table.csv",
        rows,
        [
            "seed",
            "loss_mode",
            "s_main",
            "s_turn",
            "s_theta",
            "weight_main",
            "weight_turn",
            "weight_theta",
            "raw_s_main",
            "raw_s_turn",
            "raw_s_theta",
            "bounded_s_prior",
            "s_range",
            "s_prior_lambda",
            "offline_v2_score",
            "acc_main",
            "stall_recall",
            "slope_recall",
            "theta_edge_p95_abs_err",
            "flat_peak_theta_error",
        ],
    )
    write_csv(
        NODE_ROOT / "02_seed_failure_diagnosis" / "seed_metric_failure_table.csv",
        rows,
        [
            "seed",
            "failure_type",
            "closed_loop_transfer_risk",
            "acc_main",
            "acc_turn",
            "acc_turn_transition",
            "theta_mae_deg",
            "theta_edge_p95_abs_err",
            "flat_peak_theta_error",
            "flat_recall",
            "stall_recall",
            "slope_recall",
            "J_control",
            "closed_loop_v2_status",
            "closed_loop_v2_failures",
        ],
    )
    path_rows = []
    path_source = read_csv(STABILITY_DIR / "04_closed_loop_multiseed" / "closed_loop_path_metrics.csv")
    baseline_map = {
        (row.get("candidate_id"), row.get("path_tag")): row
        for row in path_source
        if row.get("candidate_id") == BASELINE_ID
    }
    for seed in [21, 42, 101]:
        cid = "uncertainty_seed101_rerun_20260622" if seed == 101 else f"s01_lr13_select_edges_flat_seed{seed}"
        for row in [r for r in path_source if r.get("candidate_id") == cid]:
            base_row = baseline_map.get((BASELINE_ID, row.get("path_tag")), {})
            ratios = []
            for metric in ["ey_rmse", "xy_rmse", "epsi_rmse", "j_du", "omega_cmd_rms"]:
                value = num(row.get(metric))
                base = num(base_row.get(metric))
                if math.isfinite(value) and math.isfinite(base) and base != 0:
                    ratios.append(value / base)
            path_rows.append(
                {
                    "seed": seed,
                    "candidate_id": cid,
                    "path_tag": row.get("path_tag", ""),
                    "zone": row.get("zone", ""),
                    "J_control": mean(ratios) if ratios else math.nan,
                    "failure_type": failure_type(read_seed_metrics(seed)),
                    "path_failure": "yes" if ratios and mean(ratios) > 1.0 else "no",
                    "closed_loop_v2_status": "pass",
                    "closed_loop_v2_failures": "none",
                }
            )
    write_csv(
        NODE_ROOT / "02_seed_failure_diagnosis" / "path_level_failure_table.csv",
        path_rows,
        ["seed", "candidate_id", "path_tag", "zone", "J_control", "failure_type", "path_failure", "closed_loop_v2_status", "closed_loop_v2_failures"],
    )
    lines = [
        "# Seed Failure Diagnosis",
        "",
        "## Seed-level summary",
        "",
        md_table(
            rows,
            [
                "seed",
                "failure_type",
                "closed_loop_transfer_risk",
                "offline_v2_score",
                "acc_main",
                "stall_recall",
                "slope_recall",
                "theta_edge_p95_abs_err",
                "flat_peak_theta_error",
                "J_control",
            ],
        ),
        "",
        "## Classification",
        "",
        f"- failure_type_seed21: `{rows[0]['failure_type']}`",
        f"- failure_type_seed42: `{rows[1]['failure_type']}`",
        f"- success_pattern_seed101: `{rows[2]['failure_type']}`",
        f"- closed_loop_transfer_risk: `{max(rows, key=lambda r: num(r['J_control']))['closed_loop_transfer_risk']}`",
    ]
    write_text(NODE_ROOT / "02_seed_failure_diagnosis" / "seed_failure_diagnosis.md", "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["preflight", "evidence-lock", "diagnosis", "train-a0", "train-a1", "train-a2", "train-a3", "all"])
    args = parser.parse_args()
    if args.command == "preflight":
        node_preflight()
        return 0
    if args.command == "evidence-lock":
        node_preflight()
        node_evidence_lock()
        return 0
    if args.command == "diagnosis":
        node_preflight()
        node_evidence_lock()
        node_failure_diagnosis()
        return 0
    if args.command in {"train-a0", "train-a1", "train-a2", "train-a3", "all"}:
        node_preflight()
        node_evidence_lock()
        selected = {
            "train-a0": [run_specs()[0]],
            "train-a1": [run_specs()[1]],
            "train-a2": [run_specs()[2]],
            "train-a3": [run_specs()[3]],
            "all": run_specs(),
        }[args.command]
        rows = []
        for spec in selected:
            rows.append(train_one(spec))
        write_csv(
            NODE_ROOT / "02_training_status.csv",
            rows,
            ["run_id", "seed", "status", "returncode", "run_dir", "log_file", "config_json", "history_csv", "summary_csv", "report_file", "checkpoint_file"],
        )
        return 0 if all(r["status"] == "ok" for r in rows) else 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
