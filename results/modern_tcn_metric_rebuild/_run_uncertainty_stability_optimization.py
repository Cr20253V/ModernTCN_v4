from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, median
from typing import Any


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent.parent
SCI_ROOT = PROJECT_ROOT / "results" / "modern_tcn_sci_innovation"
NODE_ROOT = ROOT / "14_uncertainty_stability_optimization"
DESIGN_DIR = NODE_ROOT / "00_design"
SMOKE_DIR = NODE_ROOT / "00_smoke"
TRAIN_DIR = NODE_ROOT / "01_seed21_42_stability_search"
SCREEN_DIR = NODE_ROOT / "02_stability_screen"
SEED101_DIR = NODE_ROOT / "03_seed101_confirmation"
CLOSED_DIR = NODE_ROOT / "04_closed_loop_multiseed"
DECISION_DIR = NODE_ROOT / "05_decision"

TRAIN = PROJECT_ROOT / "src" / "ModernTCN" / "train_modern_tcn.py"
EXPORT = PROJECT_ROOT / "src" / "ModernTCN" / "export_modern_tcn_onnx.py"
CHECK_ONNX = PROJECT_ROOT / "src" / "ModernTCN" / "check_onnxruntime_consistency.py"

BASELINE_ID = "baseline_lock"
ANCHOR_ID = "uncertainty_seed101_rerun_20260622"
ANCHOR_DIR = SCI_ROOT / "01_loss_optimization" / ANCHOR_ID
BASELINE_MATRIX = ROOT / "03_rerank_existing_experiments" / "candidate_metric_matrix.csv"
V2_FULL = ROOT / "10_threshold_recalibration" / "hard_constraint_thresholds_v2_full_proposed.json"
V2_CLOSED = ROOT / "10_threshold_recalibration" / "hard_constraint_thresholds_v2_closed_loop_proposed.json"
FORMAL_PATH_METRICS = ROOT / "05_sandbox_closed_loop_if_needed" / "03_formal_validation" / "formal_validation_path_metrics.csv"
PREVIOUS_MULTISEED = ROOT / "13_multiseed_algorithm_comparison" / "01_offline_v2" / "multiseed_offline_v2.csv"
ANCHOR_J = 0.94411711953914

STABILITY_SEEDS = [21, 42]
CONFIRMATION_SEED = 101
ALL_CONFIRM_SEEDS = [21, 42, 101]
MAX_CLOSED_LOOP_CONFIGS = 2

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
HIGHER_BETTER = {
    "acc_main",
    "acc_turn",
    "acc_turn_transition",
    "flat_recall",
    "stall_recall",
    "slope_recall",
}
CONTROL_COMPONENTS = ["ey_rmse", "xy_rmse", "epsi_rmse", "j_du", "omega_cmd_rms"]


@dataclass(frozen=True)
class RunSpec:
    run_id: str
    description: str
    overrides: dict[str, Any]


def num(value: Any) -> float:
    if value is None:
        return math.nan
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "unavailable"}:
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


def safe_ratio(value: float, ref: float) -> float:
    if not math.isfinite(value) or not math.isfinite(ref) or abs(ref) < 1e-12:
        return math.nan
    return value / ref


def anchor_config() -> dict[str, Any]:
    return json.loads((ANCHOR_DIR / "config.json").read_text(encoding="utf-8"))


def anchor_cli_args() -> dict[str, Any]:
    return anchor_config()["cli_args"]


def specs() -> list[RunSpec]:
    return [
        RunSpec(
            "s01_lr13_select_edges_flat",
            "u06-like lr=0.0013 plus edge and flat peak checkpoint selection",
            {
                "lr": 0.0013,
                "select_theta_edge_p95_weight": 1.2,
                "select_theta_edge_p95_target_deg": 1.15,
                "select_theta_flat_peak_weight": 1.0,
                "select_theta_flat_peak_target_deg": 5.0,
                "select_stall_weight": 0.20,
                "select_stall_target": 0.70,
            },
        ),
        RunSpec(
            "s02_flat_excess_loss",
            "reduce seed21 flat peak with flat excess loss and flat peak selection",
            {
                "lr": 0.0013,
                "lambda_theta_flat": 0.16,
                "lambda_theta_flat_excess": 0.06,
                "theta_flat_excess_target_deg": 0.45,
                "select_theta_flat_peak_weight": 1.4,
                "select_theta_flat_peak_target_deg": 4.8,
                "select_theta_edge_p95_weight": 0.6,
                "select_theta_edge_p95_target_deg": 1.25,
            },
        ),
        RunSpec(
            "s03_edge_active_loss",
            "reduce seed42 edge error with active/error excess loss and positive theta weight",
            {
                "lr": 0.0013,
                "lambda_theta": 0.60,
                "lambda_theta_error_excess": 0.05,
                "lambda_theta_active_excess": 0.05,
                "theta_pos_weight": 1.35,
                "theta_neg_weight": 1.10,
                "select_theta_edge_p95_weight": 1.5,
                "select_theta_edge_p95_target_deg": 1.10,
                "select_theta_flat_peak_weight": 0.6,
                "select_theta_flat_peak_target_deg": 5.2,
            },
        ),
        RunSpec(
            "s04_balanced_protect",
            "combine stronger uncertainty loss adaptation with main/turn protection",
            {
                "loss_weight_lr": 0.0030,
                "lr": 0.0013,
                "lambda_turn": 0.24,
                "turn_transition_weight": 3.0,
                "main_neg_slope_weight": 2.4,
                "lambda_theta": 0.50,
                "lambda_theta_flat": 0.16,
                "lambda_theta_flat_excess": 0.05,
                "lambda_theta_error_excess": 0.04,
                "select_theta_edge_p95_weight": 1.0,
                "select_theta_flat_peak_weight": 1.0,
                "select_theta_flat_peak_target_deg": 5.0,
            },
        ),
        RunSpec(
            "s05_conservative_lr",
            "lower optimizer lr while selecting flat/edge protection",
            {
                "lr": 0.0009,
                "loss_weight_lr": 0.0015,
                "lambda_theta": 0.55,
                "lambda_theta_flat": 0.14,
                "lambda_theta_flat_excess": 0.06,
                "lambda_theta_error_excess": 0.04,
                "select_theta_edge_p95_weight": 1.0,
                "select_theta_edge_p95_target_deg": 1.20,
                "select_theta_flat_peak_weight": 1.2,
                "select_theta_flat_peak_target_deg": 5.0,
            },
        ),
        RunSpec(
            "s06_strong_flat_soft_edge",
            "stronger flat peak loss with soft edge selection",
            {
                "lr": 0.0013,
                "lambda_theta_flat": 0.20,
                "lambda_theta_flat_excess": 0.10,
                "theta_flat_excess_target_deg": 0.40,
                "select_theta_flat_peak_weight": 1.8,
                "select_theta_flat_peak_target_deg": 4.8,
                "select_theta_edge_p95_weight": 0.7,
                "select_theta_edge_p95_target_deg": 1.25,
            },
        ),
        RunSpec(
            "s07_pos_edge_guard",
            "positive edge guard for seed42 while keeping flat peak selected",
            {
                "lr": 0.0013,
                "lambda_theta": 0.58,
                "theta_pos_weight": 1.50,
                "theta_neg_weight": 1.15,
                "lambda_theta_error_excess": 0.08,
                "lambda_theta_active_excess": 0.04,
                "select_theta_edge_p95_weight": 1.6,
                "select_theta_edge_p95_target_deg": 1.10,
                "select_theta_flat_peak_weight": 0.9,
                "select_theta_flat_peak_target_deg": 5.0,
            },
        ),
        RunSpec(
            "s08_full_protect_mix",
            "u23-like main/turn protection plus flat/edge objectives",
            {
                "loss_weight_lr": 0.0006,
                "lambda_turn": 0.24,
                "turn_transition_weight": 3.0,
                "main_neg_slope_weight": 2.4,
                "lambda_theta": 0.55,
                "lambda_theta_flat": 0.16,
                "lambda_theta_flat_excess": 0.06,
                "lambda_theta_error_excess": 0.05,
                "select_theta_edge_p95_weight": 1.1,
                "select_theta_flat_peak_weight": 1.1,
                "select_theta_flat_peak_target_deg": 5.0,
                "select_stall_weight": 0.25,
                "select_stall_target": 0.70,
            },
        ),
    ]


def baseline_offline() -> dict[str, float]:
    row = next(r for r in read_csv(BASELINE_MATRIX) if r["candidate_id"] == BASELINE_ID)
    return {metric: num(row.get(metric)) for metric in OFFLINE_METRICS}


def load_thresholds() -> dict[str, Any]:
    return json.loads(V2_FULL.read_text(encoding="utf-8"))


def run_tag(spec: RunSpec, seed: int) -> str:
    return f"{spec.run_id}_seed{seed}"


def seed_root(seed: int) -> Path:
    return SEED101_DIR if seed == CONFIRMATION_SEED else TRAIN_DIR


def run_dir(spec: RunSpec, seed: int) -> Path:
    return seed_root(seed) / run_tag(spec, seed)


def checkpoint_file(spec: RunSpec, seed: int) -> Path:
    return run_dir(spec, seed) / f"modern_tcn_seed{seed}.pt"


def metric_file(spec: RunSpec, seed: int) -> Path:
    return run_dir(spec, seed) / "metrics_test.csv"


def command_from_args(args: dict[str, Any]) -> list[str]:
    cmd = [sys.executable, str(TRAIN)]
    for key, value in args.items():
        if value is None:
            continue
        flag = "--" + key.replace("_", "-")
        if isinstance(value, bool):
            if value:
                cmd.append(flag)
            continue
        cmd.append(flag)
        if isinstance(value, list):
            cmd.extend(str(v) for v in value)
        else:
            cmd.append(str(value))
    return cmd


def train_args(spec: RunSpec, seed: int, output_root: Path, smoke: bool = False) -> dict[str, Any]:
    args = dict(anchor_cli_args())
    args.update(spec.overrides)
    args["seed"] = seed
    args["output_root"] = str(output_root)
    args["run_tag"] = run_tag(spec, seed)
    args["no_overwrite"] = True
    args["dry_run"] = False
    if smoke:
        args["epochs"] = 2
        args["patience"] = 2
        args["min_epochs"] = 1
        args["limit_train"] = 512
        args["limit_val"] = 256
        args["limit_test"] = 256
        args["run_tag"] = f"smoke_{spec.run_id}_seed{seed}"
        args["output_root"] = str(SMOKE_DIR)
        args["no_overwrite"] = False
    return args


def run_one_training(spec: RunSpec, seed: int, output_root: Path, smoke: bool = False) -> dict[str, Any]:
    target_dir = (SMOKE_DIR / f"smoke_{spec.run_id}_seed{seed}") if smoke else (output_root / run_tag(spec, seed))
    ckpt = target_dir / f"modern_tcn_seed{seed}.pt"
    metrics = target_dir / "metrics_test.csv"
    if not smoke and ckpt.exists() and metrics.exists():
        return {
            "run_id": spec.run_id,
            "seed": seed,
            "run_tag": run_tag(spec, seed),
            "status": "skipped_existing",
            "returncode": 0,
            "run_dir": str(target_dir),
            "log_file": "",
        }
    args = train_args(spec, seed, output_root, smoke=smoke)
    tag = args["run_tag"]
    log_file = (SMOKE_DIR if smoke else output_root) / f"{tag}.log"
    proc = run_command(command_from_args(args), log_file)
    status = "ok" if proc.returncode == 0 else "failed"
    return {
        "run_id": spec.run_id,
        "seed": seed,
        "run_tag": tag,
        "status": status,
        "returncode": proc.returncode,
        "run_dir": str(target_dir),
        "log_file": str(log_file),
    }


def metric_alias(row: dict[str, str], metric: str) -> float:
    if metric in row:
        return num(row[metric])
    if metric == "theta_edge_p95_abs_err":
        return max(num(row.get("theta_pos_8_10_p95_abs_err_deg")), num(row.get("theta_neg_10_8_p95_abs_err_deg")))
    if metric == "flat_peak_theta_error":
        return num(row.get("theta_flat_abs_max_deg"))
    return num(row.get(metric))


def read_metrics(spec: RunSpec, seed: int) -> dict[str, Any]:
    path = metric_file(spec, seed)
    if not path.exists():
        return {
            "metric_status": "missing_metrics",
            "run_dir": str(run_dir(spec, seed)),
            "checkpoint_file": str(checkpoint_file(spec, seed)),
        }
    row = read_csv(path)[0]
    out = {metric: metric_alias(row, metric) for metric in OFFLINE_METRICS}
    out.update(
        {
            "metric_status": "ok",
            "run_dir": str(run_dir(spec, seed)),
            "checkpoint_file": row.get("checkpoint_file", str(checkpoint_file(spec, seed))),
            "source": str(path),
        }
    )
    return out


def offline_hard(row: dict[str, Any], baseline: dict[str, float], thresholds: dict[str, Any]) -> tuple[str, str]:
    checks = [
        ("acc_main_drop", baseline["acc_main"] - num(row.get("acc_main")), thresholds["acc_main_min_drop"]),
        ("stall_recall_drop", baseline["stall_recall"] - num(row.get("stall_recall")), thresholds["stall_recall_min_drop"]),
        ("slope_recall_drop", baseline["slope_recall"] - num(row.get("slope_recall")), thresholds["slope_recall_min_drop"]),
        ("theta_edge_p95_ratio", safe_ratio(num(row.get("theta_edge_p95_abs_err")), baseline["theta_edge_p95_abs_err"]), thresholds["theta_edge_p95_max_ratio"]),
        ("flat_peak_theta_error_ratio", safe_ratio(num(row.get("flat_peak_theta_error")), baseline["flat_peak_theta_error"]), thresholds["flat_peak_theta_error_max_ratio"]),
    ]
    failures = [f"{name}={value:.6g}>{limit:.6g}" for name, value, limit in checks if math.isfinite(value) and value > float(limit)]
    missing = [name for name, value, _ in checks if not math.isfinite(value)]
    if failures:
        return "fail", "; ".join(failures)
    if missing:
        return "unavailable", "missing:" + ";".join(missing)
    return "pass", "none"


def offline_score(row: dict[str, Any], baseline: dict[str, float]) -> float:
    weights = {
        "acc_main": 0.14,
        "acc_turn": 0.06,
        "acc_turn_transition": 0.08,
        "theta_mae_deg": 0.10,
        "theta_edge_p95_abs_err": 0.22,
        "flat_peak_theta_error": 0.22,
        "flat_recall": 0.05,
        "stall_recall": 0.09,
        "slope_recall": 0.04,
    }
    total = 0.0
    used = 0.0
    for metric, weight in weights.items():
        value = num(row.get(metric))
        ref = baseline.get(metric, math.nan)
        if not math.isfinite(value) or not math.isfinite(ref) or abs(ref) < 1e-12:
            continue
        component = max(0.0, (ref - value) / abs(ref)) if metric in HIGHER_BETTER else value / abs(ref)
        total += weight * component
        used += weight
    return total / used if used else math.nan


def collect_rows(seeds: list[int]) -> list[dict[str, Any]]:
    baseline = baseline_offline()
    thresholds = load_thresholds()
    rows: list[dict[str, Any]] = []
    for spec in specs():
        for seed in seeds:
            metric = read_metrics(spec, seed)
            status, failures = offline_hard(metric, baseline, thresholds) if metric["metric_status"] == "ok" else ("missing", "missing_metrics")
            rows.append(
                {
                    "run_id": spec.run_id,
                    "description": spec.description,
                    "seed": seed,
                    "run_tag": run_tag(spec, seed),
                    "metric_status": metric["metric_status"],
                    "offline_v2_status": status,
                    "offline_v2_failures": failures,
                    "offline_score": offline_score(metric, baseline) if metric["metric_status"] == "ok" else math.nan,
                    **{m: metric.get(m, "NaN") for m in OFFLINE_METRICS},
                    "checkpoint_file": metric.get("checkpoint_file", str(checkpoint_file(spec, seed))),
                    "run_dir": metric.get("run_dir", str(run_dir(spec, seed))),
                    "source": metric.get("source", ""),
                    "overrides_json": json.dumps(spec.overrides, ensure_ascii=False, sort_keys=True),
                }
            )
    return rows


def summarise_config(rows: list[dict[str, Any]], seeds: list[int]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for spec in specs():
        subset = [r for r in rows if r["run_id"] == spec.run_id and int(num(r["seed"])) in seeds]
        if not subset:
            continue
        pass_count = sum(1 for r in subset if r["offline_v2_status"] == "pass")
        scores = [num(r["offline_score"]) for r in subset if math.isfinite(num(r["offline_score"]))]
        best = min(subset, key=lambda r: num(r["offline_score"]) if math.isfinite(num(r["offline_score"])) else math.inf)
        status = "dual_seed_pass" if pass_count == len(seeds) else "partial_pass" if pass_count > 0 else "reject_offline"
        seed_status = ";".join(f"seed{r['seed']}={r['offline_v2_status']}({r['offline_v2_failures']})" for r in subset)
        summary.append(
            {
                "run_id": spec.run_id,
                "description": spec.description,
                "stability_screen_status": status,
                "pass_count": pass_count,
                "n_seeds": len(seeds),
                "median_offline_score": median(scores) if scores else math.nan,
                "mean_offline_score": mean(scores) if scores else math.nan,
                "best_seed": best["seed"],
                "best_seed_score": best["offline_score"],
                "seed_status": seed_status,
                "overrides_json": json.dumps(spec.overrides, ensure_ascii=False, sort_keys=True),
            }
        )
    sorted_summary = sorted(
        summary,
        key=lambda r: (
            {"dual_seed_pass": 0, "partial_pass": 1, "reject_offline": 2}[r["stability_screen_status"]],
            num(r["median_offline_score"]) if math.isfinite(num(r["median_offline_score"])) else math.inf,
            r["run_id"],
        ),
    )
    for rank, row in enumerate(sorted_summary, 1):
        row["stability_rank"] = rank
    return sorted_summary


def node_design() -> None:
    NODE_ROOT.mkdir(parents=True, exist_ok=True)
    thresholds = load_thresholds()
    baseline = baseline_offline()
    previous_rows = read_csv(PREVIOUS_MULTISEED) if PREVIOUS_MULTISEED.exists() else []
    fail_focus = [
        {
            "source": row.get("variant_id"),
            "seed": row.get("seed"),
            "offline_v2_status": row.get("offline_v2_status"),
            "hard_gate_failures": row.get("hard_gate_failures"),
            "theta_edge_p95_abs_err": row.get("theta_edge_p95_abs_err"),
            "flat_peak_theta_error": row.get("flat_peak_theta_error"),
        }
        for row in previous_rows
        if row.get("algorithm_group") == "Uncertainty_weighted_ModernTCN_small"
    ]
    design_rows = [
        {
            "run_id": spec.run_id,
            "description": spec.description,
            "seed_policy": "train seed21/42 first; only dual_seed_pass gets seed101 confirmation",
            "overrides_json": json.dumps(spec.overrides, ensure_ascii=False, sort_keys=True),
        }
        for spec in specs()
    ]
    write_csv(DESIGN_DIR / "stability_tuning_design.csv", design_rows, ["run_id", "description", "seed_policy", "overrides_json"])
    write_csv(DESIGN_DIR / "failure_focus_prior.csv", fail_focus, ["source", "seed", "offline_v2_status", "hard_gate_failures", "theta_edge_p95_abs_err", "flat_peak_theta_error"])
    write_json(
        DESIGN_DIR / "stability_contract.json",
        {
            "node_root": str(NODE_ROOT),
            "objective": "Reduce seed21/42 flat_peak_theta_error and theta_edge_p95_abs_err failures for Uncertainty-weighted ModernTCN_small.",
            "baseline_id": BASELINE_ID,
            "anchor_id": ANCHOR_ID,
            "anchor_j_control": ANCHOR_J,
            "stability_seeds": STABILITY_SEEDS,
            "confirmation_seed": CONFIRMATION_SEED,
            "closed_loop_policy": "Only configs passing seed21 and seed42 offline v2 hard gates get seed101 confirmation and multi-seed closed-loop.",
            "offline_threshold_file": str(V2_FULL),
            "closed_loop_threshold_file": str(V2_CLOSED),
            "baseline_hard_metric_values": baseline,
            "hard_thresholds": thresholds,
            "disabled_unreliable_terms": {
                "lambda_transition_focal": 0,
                "lambda_stall_focal": 0,
                "lambda_theta_smooth": 0,
                "theta_smooth_mode": "off",
            },
        },
    )
    lines = [
        "# Uncertainty Stability Optimization Design",
        "",
        "- scope: seed21/42 stability first; no architecture changes.",
        "- primary failure targets: `flat_peak_theta_error`, `theta_edge_p95_abs_err`.",
        "- closed-loop is gated by seed21/42 offline pass.",
        "",
        "| run | description |",
        "|---|---|",
    ]
    for spec in specs():
        lines.append(f"| `{spec.run_id}` | {spec.description} |")
    write_text(DESIGN_DIR / "stability_design_report.md", "\n".join(lines) + "\n")


def node_smoke() -> None:
    spec = specs()[0]
    row = run_one_training(spec, 21, SMOKE_DIR, smoke=True)
    write_csv(SMOKE_DIR / "smoke_status.csv", [row], ["run_id", "seed", "run_tag", "status", "returncode", "run_dir", "log_file"])
    if row["status"] != "ok":
        raise SystemExit(f"Smoke failed: {row['log_file']}")


def node_train_seed21_42() -> None:
    rows: list[dict[str, Any]] = []
    status_file = TRAIN_DIR / "seed21_42_training_status.csv"
    existing: dict[tuple[str, int], dict[str, str]] = {}
    if status_file.exists():
        for row in read_csv(status_file):
            existing[(row["run_id"], int(num(row["seed"])))] = row
    for spec in specs():
        for seed in STABILITY_SEEDS:
            key = (spec.run_id, seed)
            if key in existing and existing[key].get("status") in {"ok", "skipped_existing"} and metric_file(spec, seed).exists():
                row = dict(existing[key])
                row["status"] = "skipped_existing"
            else:
                print(f"[stability] training {spec.run_id} seed{seed}")
                row = run_one_training(spec, seed, TRAIN_DIR, smoke=False)
            rows.append(row)
            write_csv(status_file, rows, ["run_id", "seed", "run_tag", "status", "returncode", "run_dir", "log_file"])
    failed = [r for r in rows if r["status"] == "failed"]
    if failed:
        raise SystemExit("Training failed: " + ", ".join(r["run_tag"] for r in failed))


def node_screen() -> None:
    rows = collect_rows(STABILITY_SEEDS)
    write_csv(
        SCREEN_DIR / "seed21_42_stability_metrics.csv",
        rows,
        ["run_id", "description", "seed", "run_tag", "metric_status", "offline_v2_status", "offline_v2_failures", "offline_score", *OFFLINE_METRICS, "checkpoint_file", "run_dir", "source", "overrides_json"],
    )
    summary = summarise_config(rows, STABILITY_SEEDS)
    write_csv(
        SCREEN_DIR / "stability_screen_results.csv",
        summary,
        ["stability_rank", "run_id", "description", "stability_screen_status", "pass_count", "n_seeds", "median_offline_score", "mean_offline_score", "best_seed", "best_seed_score", "seed_status", "overrides_json"],
    )
    selected = [r for r in summary if r["stability_screen_status"] == "dual_seed_pass"]
    write_csv(
        SCREEN_DIR / "seed101_confirmation_manifest.csv",
        selected,
        ["stability_rank", "run_id", "description", "stability_screen_status", "pass_count", "median_offline_score", "best_seed", "best_seed_score", "overrides_json"],
    )
    lines = ["# Seed21/42 Stability Screen", "", "| rank | run | status | pass | median score | seed status |", "|---:|---|---|---:|---:|---|"]
    for row in summary:
        lines.append(f"| {row['stability_rank']} | `{row['run_id']}` | {row['stability_screen_status']} | {row['pass_count']}/{row['n_seeds']} | {num(row['median_offline_score']):.6f} | {row['seed_status']} |")
    if not selected:
        lines.extend(["", "No config passed both seed21 and seed42. Seed101 confirmation and closed-loop are intentionally blocked."])
    write_text(SCREEN_DIR / "stability_screen_report.md", "\n".join(lines) + "\n")


def selected_specs_for_seed101() -> list[RunSpec]:
    manifest = SCREEN_DIR / "seed101_confirmation_manifest.csv"
    if not manifest.exists():
        node_screen()
    selected_ids = [r["run_id"] for r in read_csv(manifest)]
    by_id = {spec.run_id: spec for spec in specs()}
    return [by_id[run_id] for run_id in selected_ids]


def node_train_seed101() -> None:
    selected = selected_specs_for_seed101()
    rows: list[dict[str, Any]] = []
    if not selected:
        write_csv(SEED101_DIR / "seed101_training_status.csv", rows, ["run_id", "seed", "run_tag", "status", "returncode", "run_dir", "log_file"])
        write_text(SEED101_DIR / "seed101_training_report.md", "# Seed101 Confirmation\n\nNo dual-seed pass configs; seed101 confirmation skipped.\n")
        return
    for spec in selected:
        print(f"[seed101 confirm] training {spec.run_id} seed101")
        row = run_one_training(spec, CONFIRMATION_SEED, SEED101_DIR, smoke=False)
        rows.append(row)
        write_csv(SEED101_DIR / "seed101_training_status.csv", rows, ["run_id", "seed", "run_tag", "status", "returncode", "run_dir", "log_file"])
    failed = [r for r in rows if r["status"] == "failed"]
    if failed:
        raise SystemExit("Seed101 confirmation failed: " + ", ".join(r["run_tag"] for r in failed))


def node_final_offline() -> None:
    selected = selected_specs_for_seed101()
    selected_ids = {spec.run_id for spec in selected}
    if not selected_ids:
        write_csv(SCREEN_DIR / "final_multiseed_offline_metrics.csv", [], ["run_id", "seed", "offline_v2_status"])
        write_csv(SCREEN_DIR / "final_multiseed_offline_summary.csv", [], ["run_id", "stability_label"])
        return
    rows = [r for r in collect_rows(ALL_CONFIRM_SEEDS) if r["run_id"] in selected_ids]
    write_csv(
        SCREEN_DIR / "final_multiseed_offline_metrics.csv",
        rows,
        ["run_id", "description", "seed", "run_tag", "metric_status", "offline_v2_status", "offline_v2_failures", "offline_score", *OFFLINE_METRICS, "checkpoint_file", "run_dir", "source", "overrides_json"],
    )
    summary = summarise_config(rows, ALL_CONFIRM_SEEDS)
    for row in summary:
        row["stability_label"] = "robust_pass" if row["pass_count"] == 3 else "usable_seed_sensitive" if row["pass_count"] == 2 else "reject_seed_fragile"
    write_csv(
        SCREEN_DIR / "final_multiseed_offline_summary.csv",
        summary,
        ["stability_rank", "run_id", "description", "stability_label", "stability_screen_status", "pass_count", "n_seeds", "median_offline_score", "mean_offline_score", "best_seed", "best_seed_score", "seed_status", "overrides_json"],
    )


def final_offline_summary() -> list[dict[str, str]]:
    path = SCREEN_DIR / "final_multiseed_offline_summary.csv"
    if not path.exists():
        node_final_offline()
    return read_csv(path) if path.exists() else []


def export_one(spec: RunSpec, seed: int, stability_label: str) -> dict[str, Any]:
    candidate_id = run_tag(spec, seed)
    ckpt = checkpoint_file(spec, seed)
    export_dir = CLOSED_DIR / "00_exported_onnx" / candidate_id
    export_dir.mkdir(parents=True, exist_ok=True)
    onnx_file = export_dir / f"{candidate_id}.onnx"
    sample_file = export_dir / f"{candidate_id}_pytorch_reference.mat"
    if not ckpt.exists():
        return {
            "run_id": spec.run_id,
            "candidate_id": candidate_id,
            "seed": seed,
            "stability_label": stability_label,
            "checkpoint_file": str(ckpt),
            "onnx_file": str(onnx_file),
            "sample_file": str(sample_file),
            "export_status": "missing_checkpoint",
            "consistency_json": "",
            "consistency_status": "missing_checkpoint",
            "consistency_pass": False,
            "selected_for_closed_loop": False,
        }
    if not onnx_file.exists() or not sample_file.exists():
        proc = run_command(
            [
                sys.executable,
                str(EXPORT),
                "--checkpoint",
                str(ckpt),
                "--onnx-file",
                str(onnx_file),
                "--sample-file",
                str(sample_file),
                "--opset",
                "17",
                "--sample-count",
                "16",
                "--no-overwrite",
            ],
            export_dir / f"{candidate_id}_export.log",
        )
        export_status = "ok" if proc.returncode == 0 else "failed"
    else:
        export_status = "skipped_existing"
    consistency_json = onnx_file.with_name(onnx_file.stem + "_onnxruntime_consistency.json")
    consistency_pass = False
    if onnx_file.exists() and sample_file.exists():
        proc = run_command(
            [
                sys.executable,
                str(CHECK_ONNX),
                "--onnx-file",
                str(onnx_file),
                "--sample-file",
                str(sample_file),
                "--max-abs-tol",
                "1e-4",
                "--mean-abs-tol",
                "1e-5",
            ],
            export_dir / f"{candidate_id}_onnxruntime.log",
        )
        if consistency_json.exists():
            consistency_pass = bool(json.loads(consistency_json.read_text(encoding="utf-8")).get("pass"))
        consistency_status = "ok" if proc.returncode == 0 and consistency_pass else "failed"
    else:
        consistency_status = "missing_export"
    return {
        "run_id": spec.run_id,
        "candidate_id": candidate_id,
        "seed": seed,
        "stability_label": stability_label,
        "checkpoint_file": str(ckpt),
        "onnx_file": str(onnx_file),
        "sample_file": str(sample_file),
        "export_status": export_status,
        "consistency_json": str(consistency_json),
        "consistency_status": consistency_status,
        "consistency_pass": consistency_pass,
        "selected_for_closed_loop": consistency_pass,
    }


def node_export_closed_loop() -> None:
    summary = final_offline_summary()
    robust = [r for r in summary if r.get("stability_label") == "robust_pass"]
    robust = sorted(robust, key=lambda r: (num(r["median_offline_score"]), r["run_id"]))[:MAX_CLOSED_LOOP_CONFIGS]
    by_id = {spec.run_id: spec for spec in specs()}
    manifest: list[dict[str, Any]] = []
    for row in robust:
        spec = by_id[row["run_id"]]
        for seed in ALL_CONFIRM_SEEDS:
            manifest.append(export_one(spec, seed, row["stability_label"]))
    write_csv(
        CLOSED_DIR / "closed_loop_manifest.csv",
        manifest,
        ["run_id", "candidate_id", "seed", "stability_label", "checkpoint_file", "onnx_file", "sample_file", "export_status", "consistency_json", "consistency_status", "consistency_pass", "selected_for_closed_loop"],
    )
    write_json(CLOSED_DIR / "closed_loop_manifest.json", manifest)
    if not manifest:
        write_text(CLOSED_DIR / "closed_loop_manifest.md", "# Closed-loop Manifest\n\nNo robust-pass configs; closed-loop skipped.\n")
        return
    lines = ["# Closed-loop Manifest", "", "| run | candidate | seed | consistency | selected |", "|---|---|---:|---|---|"]
    for row in manifest:
        lines.append(f"| `{row['run_id']}` | `{row['candidate_id']}` | {row['seed']} | {row['consistency_pass']} | {row['selected_for_closed_loop']} |")
    write_text(CLOSED_DIR / "closed_loop_manifest.md", "\n".join(lines) + "\n")
    failed = [r for r in manifest if not r["consistency_pass"]]
    if failed:
        raise SystemExit("ONNX consistency failed: " + ", ".join(r["candidate_id"] for r in failed))


def aggregate_path_metrics() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    formal = read_csv(FORMAL_PATH_METRICS)
    for row in formal:
        if row["controller"] in {BASELINE_ID, ANCHOR_ID}:
            rows.append({**row, "candidate_id": row["controller"], "source": str(FORMAL_PATH_METRICS)})
    manifest_file = CLOSED_DIR / "closed_loop_manifest.csv"
    if not manifest_file.exists():
        return rows
    selected = {r["candidate_id"] for r in read_csv(manifest_file) if str(r.get("selected_for_closed_loop", "")).lower() == "true"}
    for path_dir in (CLOSED_DIR / "01_closed_loop_runs").glob("path_*"):
        summary = path_dir / "uncertainty_stability_summary.csv"
        if not summary.exists():
            continue
        for row in read_csv(summary):
            if row["controller"] in selected:
                rows.append({**row, "candidate_id": row["controller"], "source": str(summary)})
    return rows


def aggregate_by_candidate(path_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for cid in sorted({r["candidate_id"] for r in path_rows}):
        subset = [r for r in path_rows if r["candidate_id"] == cid]
        row: dict[str, Any] = {"candidate_id": cid, "n_paths": len(subset)}
        for metric in ["ey_rmse", "xy_rmse", "epsi_rmse", "j_du", "omega_cmd_rms", "viol_rate", "theta_mae_deg", "main_acc_pct", "turn_acc_pct"]:
            values = [num(r.get(metric)) for r in subset if math.isfinite(num(r.get(metric)))]
            row[f"{metric}_mean"] = mean(values) if values else math.nan
        out[cid] = row
    return out


def closed_loop_hard(row: dict[str, Any], baseline: dict[str, Any], thresholds: dict[str, Any]) -> tuple[str, str]:
    checks = [
        ("viol_rate_abs_increase", num(row.get("viol_rate_mean")) - num(baseline.get("viol_rate_mean")), thresholds["viol_rate_max_abs_increase"]),
        ("closed_loop_main_acc_drop", (num(baseline.get("main_acc_pct_mean")) - num(row.get("main_acc_pct_mean"))) / 100.0, thresholds["acc_main_min_drop"]),
        ("omega_cmd_rms_ratio", safe_ratio(num(row.get("omega_cmd_rms_mean")), num(baseline.get("omega_cmd_rms_mean"))), thresholds["omega_cmd_rms_max_ratio"]),
        ("delta_u_proxy_ratio", safe_ratio(num(row.get("j_du_mean")), num(baseline.get("j_du_mean"))), thresholds["delta_u_proxy_max_ratio"]),
    ]
    failures = [f"{name}={value:.6g}>{limit:.6g}" for name, value, limit in checks if math.isfinite(value) and value > float(limit)]
    return ("pass" if not failures else "fail"), "; ".join(failures) if failures else "none"


def j_control(row: dict[str, Any], baseline: dict[str, Any]) -> float:
    terms = []
    for metric in CONTROL_COMPONENTS:
        ratio = safe_ratio(num(row.get(f"{metric}_mean")), num(baseline.get(f"{metric}_mean")))
        if math.isfinite(ratio):
            terms.append(ratio)
    return mean(terms) if terms else math.nan


def node_summarize_closed_loop() -> None:
    path_rows = aggregate_path_metrics()
    write_csv(CLOSED_DIR / "closed_loop_path_metrics.csv", path_rows, sorted({k for row in path_rows for k in row.keys()}))
    agg = aggregate_by_candidate(path_rows)
    if BASELINE_ID not in agg:
        raise SystemExit("baseline_lock missing from closed-loop path metrics")
    baseline = agg[BASELINE_ID]
    thresholds = json.loads(V2_CLOSED.read_text(encoding="utf-8"))
    final: list[dict[str, Any]] = []
    for cid, row in agg.items():
        if cid == BASELINE_ID:
            status, failures, jc = "pass", "reference", 1.0
        else:
            status, failures = closed_loop_hard(row, baseline, thresholds)
            jc = j_control(row, baseline)
        final.append({**row, "J_control": jc, "closed_loop_v2_status": status, "closed_loop_v2_failures": failures})
    for rank, row in enumerate(sorted(final, key=lambda r: num(r["J_control"])), 1):
        row["rank_by_J_control"] = rank
    fields = ["candidate_id", "n_paths", "J_control", "rank_by_J_control", "closed_loop_v2_status", "closed_loop_v2_failures", "ey_rmse_mean", "xy_rmse_mean", "epsi_rmse_mean", "j_du_mean", "omega_cmd_rms_mean", "viol_rate_mean", "theta_mae_deg_mean", "main_acc_pct_mean", "turn_acc_pct_mean"]
    write_csv(CLOSED_DIR / "closed_loop_results.csv", sorted(final, key=lambda r: num(r["rank_by_J_control"])), fields)
    lines = ["# Uncertainty Stability Closed-loop Report", "", "| rank | candidate | J_control | v2 status | failures |", "|---:|---|---:|---|---|"]
    for row in sorted(final, key=lambda r: num(r["rank_by_J_control"])):
        lines.append(f"| {row['rank_by_J_control']} | `{row['candidate_id']}` | {num(row['J_control']):.6f} | {row['closed_loop_v2_status']} | {row['closed_loop_v2_failures']} |")
    write_text(CLOSED_DIR / "closed_loop_report.md", "\n".join(lines) + "\n")


def node_decision() -> None:
    if (CLOSED_DIR / "closed_loop_results.csv").exists():
        node_summarize_closed_loop()
    final_summary = read_csv(SCREEN_DIR / "final_multiseed_offline_summary.csv") if (SCREEN_DIR / "final_multiseed_offline_summary.csv").exists() else []
    robust = [r for r in final_summary if r.get("stability_label") == "robust_pass"]
    closed = read_csv(CLOSED_DIR / "closed_loop_results.csv") if (CLOSED_DIR / "closed_loop_results.csv").exists() else []
    candidate_closed = [r for r in closed if r["candidate_id"] not in {BASELINE_ID, ANCHOR_ID}]
    promoted = [r for r in candidate_closed if r["closed_loop_v2_status"] == "pass" and math.isfinite(num(r["J_control"])) and num(r["J_control"]) < ANCHOR_J]
    if promoted:
        decision = "PromotedStabilityCandidate"
    elif robust:
        decision = "RobustOfflineOnlyNeedsClosedLoop" if not candidate_closed else "RobustOfflineNoClosedLoopPromotion"
    else:
        decision = "NoRobustOfflineCandidate"
    lines = [
        "# Uncertainty Stability Optimization Final Report",
        "",
        f"- decision: `{decision}`",
        f"- robust offline configs: {len(robust)}",
        f"- promoted closed-loop candidates: {len(promoted)}",
        "",
        "## Offline Final Summary",
        "",
        "| run | label | pass | median score | seed status |",
        "|---|---|---:|---:|---|",
    ]
    for row in final_summary:
        lines.append(f"| `{row['run_id']}` | {row.get('stability_label', '')} | {row.get('pass_count', '')}/{row.get('n_seeds', '')} | {num(row.get('median_offline_score')):.6f} | {row.get('seed_status', '')} |")
    if not final_summary:
        lines.append("| none | none | 0/0 | NaN | seed101 confirmation skipped |")
    lines.extend(["", "## Closed-loop Summary", ""])
    if closed:
        lines.extend(["| rank | candidate | J_control | status |", "|---:|---|---:|---|"])
        for row in closed:
            lines.append(f"| {row['rank_by_J_control']} | `{row['candidate_id']}` | {num(row['J_control']):.6f} | {row['closed_loop_v2_status']} |")
    else:
        lines.append("Closed-loop was not executed because no config reached robust offline eligibility.")
    lines.extend(
        [
            "",
            "## Output Files",
            "",
            "- design: `results/modern_tcn_metric_rebuild/14_uncertainty_stability_optimization/00_design/`",
            "- seed21/42 metrics: `results/modern_tcn_metric_rebuild/14_uncertainty_stability_optimization/02_stability_screen/seed21_42_stability_metrics.csv`",
            "- stability screen: `results/modern_tcn_metric_rebuild/14_uncertainty_stability_optimization/02_stability_screen/stability_screen_results.csv`",
            "- final offline summary: `results/modern_tcn_metric_rebuild/14_uncertainty_stability_optimization/02_stability_screen/final_multiseed_offline_summary.csv`",
            "- closed-loop outputs: `results/modern_tcn_metric_rebuild/14_uncertainty_stability_optimization/04_closed_loop_multiseed/`",
        ]
    )
    write_text(DECISION_DIR / "uncertainty_stability_final_report.md", "\n".join(lines) + "\n")
    write_json(
        DECISION_DIR / "uncertainty_stability_decision.json",
        {
            "decision": decision,
            "robust_offline_count": len(robust),
            "promoted_closed_loop_count": len(promoted),
            "node_root": str(NODE_ROOT),
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=[
            "design",
            "smoke",
            "train-seed21-42",
            "screen",
            "train-seed101",
            "final-offline",
            "export-closed-loop",
            "summarize-closed-loop",
            "decision",
            "all-offline",
        ],
    )
    args = parser.parse_args()
    if args.command == "design":
        node_design()
    elif args.command == "smoke":
        node_smoke()
    elif args.command == "train-seed21-42":
        node_train_seed21_42()
    elif args.command == "screen":
        node_screen()
    elif args.command == "train-seed101":
        node_train_seed101()
    elif args.command == "final-offline":
        node_final_offline()
    elif args.command == "export-closed-loop":
        node_export_closed_loop()
    elif args.command == "summarize-closed-loop":
        node_summarize_closed_loop()
    elif args.command == "decision":
        node_decision()
    elif args.command == "all-offline":
        node_design()
        node_smoke()
        node_train_seed21_42()
        node_screen()
        node_train_seed101()
        node_final_offline()
        node_export_closed_loop()
        node_decision()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
