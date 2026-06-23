from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, median
from typing import Any


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent.parent
SCI_ROOT = PROJECT_ROOT / "results" / "modern_tcn_sci_innovation"
NODE_ROOT = ROOT / "11_uncertainty_tuning"
DESIGN_DIR = NODE_ROOT / "00_design"
SMOKE_DIR = NODE_ROOT / "00_smoke"
SEED101_DIR = NODE_ROOT / "01_seed101_search"
SCREEN_DIR = NODE_ROOT / "02_seed101_screen"
MULTISEED_DIR = NODE_ROOT / "03_multiseed"
TOP5_DIR = NODE_ROOT / "04_closed_loop_top5"
DECISION_DIR = NODE_ROOT / "05_decision"

TRAIN = PROJECT_ROOT / "src" / "ModernTCN" / "train_modern_tcn.py"
EXPORT = PROJECT_ROOT / "src" / "ModernTCN" / "export_modern_tcn_onnx.py"
CHECK_ONNX = PROJECT_ROOT / "src" / "ModernTCN" / "check_onnxruntime_consistency.py"
ANCHOR_DIR = SCI_ROOT / "01_loss_optimization" / "uncertainty_seed101_rerun_20260622"
BASELINE_MATRIX = ROOT / "03_rerank_existing_experiments" / "candidate_metric_matrix.csv"
V2_FULL = ROOT / "10_threshold_recalibration" / "hard_constraint_thresholds_v2_full_proposed.json"
V2_CLOSED = ROOT / "10_threshold_recalibration" / "hard_constraint_thresholds_v2_closed_loop_proposed.json"
FORMAL_PATH_METRICS = ROOT / "05_sandbox_closed_loop_if_needed" / "03_formal_validation" / "formal_validation_path_metrics.csv"
ANCHOR_FINAL_RESULTS = ROOT / "10_threshold_recalibration" / "rerank_with_v2_thresholds.csv"

DATASET = "data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat"
ANCHOR_ID = "uncertainty_seed101_rerun_20260622"
ANCHOR_J = 0.94411711953914
BASELINE_ID = "baseline_lock"

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
    "main_acc_pct",
    "turn_acc_pct",
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
    if not text or text.lower() in {"nan", "none", "unavailable", "false"}:
        if text.lower() == "false":
            return 0.0
        return math.nan
    if text.lower() == "true":
        return 1.0
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
    log_file.parent.mkdir(parents=True, exist_ok=True) if log_file else None
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


def specs() -> list[RunSpec]:
    return [
        RunSpec("u01_lwlr0003", "loss_weight_lr=0.0003", {"loss_weight_lr": 0.0003}),
        RunSpec("u02_lwlr0006", "loss_weight_lr=0.0006", {"loss_weight_lr": 0.0006}),
        RunSpec("u03_lwlr0015", "loss_weight_lr=0.0015", {"loss_weight_lr": 0.0015}),
        RunSpec("u04_lwlr0030", "loss_weight_lr=0.0030", {"loss_weight_lr": 0.0030}),
        RunSpec("u05_lr0007", "lr=0.0007", {"lr": 0.0007}),
        RunSpec("u06_lr0013", "lr=0.0013", {"lr": 0.0013}),
        RunSpec("u07_lturn016", "lambda_turn=0.16", {"lambda_turn": 0.16}),
        RunSpec("u08_lturn024", "lambda_turn=0.24", {"lambda_turn": 0.24}),
        RunSpec("u09_lturn030", "lambda_turn=0.30", {"lambda_turn": 0.30}),
        RunSpec("u10_tt20", "turn_transition_weight=2.0", {"turn_transition_weight": 2.0}),
        RunSpec("u11_tt30", "turn_transition_weight=3.0", {"turn_transition_weight": 3.0}),
        RunSpec("u12_tt35", "turn_transition_weight=3.5", {"turn_transition_weight": 3.5}),
        RunSpec("u13_mainneg16", "main_neg_slope_weight=1.6", {"main_neg_slope_weight": 1.6}),
        RunSpec("u14_mainneg24", "main_neg_slope_weight=2.4", {"main_neg_slope_weight": 2.4}),
        RunSpec("u15_mainneg28", "main_neg_slope_weight=2.8", {"main_neg_slope_weight": 2.8}),
        RunSpec("u16_ltheta045", "lambda_theta=0.45", {"lambda_theta": 0.45}),
        RunSpec("u17_ltheta050", "lambda_theta=0.50", {"lambda_theta": 0.50}),
        RunSpec("u18_ltheta065", "lambda_theta=0.65", {"lambda_theta": 0.65}),
        RunSpec("u19_tflat008", "lambda_theta_flat=0.08", {"lambda_theta_flat": 0.08}),
        RunSpec("u20_tflat016", "lambda_theta_flat=0.16", {"lambda_theta_flat": 0.16}),
        RunSpec("u21_edge_select", "theta edge selection emphasis", {"select_theta_edge_p95_weight": 1.0, "select_theta_edge_p95_target_deg": 1.2}),
        RunSpec(
            "u22_flat_select",
            "flat theta selection emphasis",
            {
                "select_theta_flat_p95_weight": 0.55,
                "select_theta_flat_p95_target_deg": 0.6,
                "select_theta_flat_bias_weight": 0.45,
                "select_theta_flat_bias_target_deg": 0.10,
            },
        ),
        RunSpec(
            "u23_turn_protect_mix",
            "turn protection mix",
            {"loss_weight_lr": 0.0006, "lambda_turn": 0.24, "turn_transition_weight": 3.0, "main_neg_slope_weight": 2.4},
        ),
        RunSpec(
            "u24_control_theta_mix",
            "control theta mix",
            {
                "loss_weight_lr": 0.0006,
                "lambda_theta": 0.50,
                "lambda_theta_flat": 0.10,
                "select_theta_edge_p95_weight": 1.0,
                "select_theta_edge_p95_target_deg": 1.2,
            },
        ),
    ]


def anchor_cli_args() -> dict[str, Any]:
    return json.loads((ANCHOR_DIR / "config.json").read_text(encoding="utf-8"))["cli_args"]


def anchor_model_config() -> dict[str, Any]:
    return json.loads((ANCHOR_DIR / "config.json").read_text(encoding="utf-8"))["model_config"]


def baseline_offline() -> dict[str, Any]:
    row = next(r for r in read_csv(BASELINE_MATRIX) if r["candidate_id"] == BASELINE_ID)
    return {
        "algorithm_id": BASELINE_ID,
        "acc_main": num(row["acc_main"]),
        "acc_turn": num(row["acc_turn"]),
        "acc_turn_transition": num(row["acc_turn_transition"]),
        "theta_mae_deg": num(row["theta_mae_deg"]),
        "theta_edge_p95_abs_err": num(row["theta_edge_p95_abs_err"]),
        "flat_peak_theta_error": num(row["flat_peak_theta_error"]),
        "flat_recall": num(row["flat_recall"]),
        "stall_recall": num(row["stall_recall"]),
        "slope_recall": num(row["slope_recall"]),
    }


def anchor_closed_loop() -> dict[str, Any]:
    rows = read_csv(ANCHOR_FINAL_RESULTS)
    return next(r for r in rows if r["algorithm_id"] == ANCHOR_ID)


def load_thresholds() -> dict[str, Any]:
    return json.loads(V2_FULL.read_text(encoding="utf-8"))


def design_rows() -> list[dict[str, Any]]:
    rows = []
    for spec in specs():
        row = {
            "run_id": spec.run_id,
            "description": spec.description,
            "seed101_run_tag": f"{spec.run_id}_seed101",
            "seed21_run_tag": f"{spec.run_id}_seed21",
            "seed42_run_tag": f"{spec.run_id}_seed42",
            "overrides_json": json.dumps(spec.overrides, ensure_ascii=False, sort_keys=True),
        }
        rows.append(row)
    return rows


def command_for_run(spec: RunSpec, seed: int, output_root: Path, *, smoke: bool = False) -> list[str]:
    args = anchor_cli_args()
    cmd = [
        sys.executable,
        str(TRAIN),
        "--seed",
        str(seed),
        "--model-family",
        "small",
        "--dataset-file",
        DATASET,
        "--output-root",
        str(output_root),
        "--run-tag",
        f"{spec.run_id}_seed{seed}",
        "--no-overwrite",
        "--loss-mode",
        "uncertainty_weighting",
        "--epochs",
        str(2 if smoke else 140),
        "--batch-size",
        str(args.get("batch_size", 256)),
        "--lr",
        str(spec.overrides.get("lr", 0.001)),
        "--weight-decay",
        "0.0001",
        "--patience",
        str(2 if smoke else 30),
        "--min-epochs",
        str(1 if smoke else 40),
        "--channels",
        "64",
        "--blocks",
        "5",
        "--kernel-size",
        "31",
        "--temporal-padding",
        "same",
        "--dropout",
        "0.15",
        "--loss-weight-lr",
        str(spec.overrides.get("loss_weight_lr", args.get("loss_weight_lr", 0.001))),
        "--gradnorm-alpha",
        "1.5",
        "--gradnorm-update-interval",
        "0",
        "--turn-head-source",
        "full",
        "--lambda-turn",
        str(spec.overrides.get("lambda_turn", args.get("lambda_turn", 0.2))),
        "--lambda-theta",
        str(spec.overrides.get("lambda_theta", args.get("lambda_theta", 0.55))),
        "--lambda-theta-flat",
        str(spec.overrides.get("lambda_theta_flat", args.get("lambda_theta_flat", 0.12))),
        "--theta-flat-loss-mode",
        "near_zero",
        "--theta-flat-zero-tol-deg",
        "0.3",
        "--lambda-theta-near-flat",
        "0.0",
        "--lambda-theta-error-excess",
        "0.05",
        "--lambda-theta-flat-excess",
        "0.0",
        "--lambda-theta-near-flat-excess",
        "0.0",
        "--lambda-theta-true-zero-excess",
        "0.1",
        "--lambda-theta-active-excess",
        "0.1",
        "--lambda-theta-small-neg",
        "0.0",
        "--lambda-theta-small-neg-excess",
        "0.0",
        "--lambda-turn-release",
        "0.0",
        "--lambda-false-turn-straight",
        "0.0",
        "--lambda-transition-focal",
        "0.0",
        "--lambda-stall-focal",
        "0.0",
        "--lambda-theta-smooth",
        "0.0",
        "--theta-smooth-mode",
        "off",
        "--focal-gamma",
        "2.0",
        "--theta-excess-target-deg",
        "1.0",
        "--theta-flat-excess-target-deg",
        "0.5",
        "--theta-small-neg-min-deg",
        "-4.0",
        "--theta-small-neg-max-deg",
        "-2.0",
        "--theta-gate-mode",
        "none",
        "--theta-gate-power",
        "1.0",
        "--theta-gate-floor",
        "0.0",
        "--theta-neg-weight",
        "1.0",
        "--theta-pos-weight",
        "1.0",
        "--main-class-multipliers",
        "1.2",
        "1.0",
        "0.95",
        "--turn-class-multipliers",
        "1.4",
        "0.8",
        "1.4",
        "--main-class-weight-method",
        "sqrt_inverse",
        "--turn-class-weight-method",
        "sqrt_inverse",
        "--main-neg-slope-weight",
        str(spec.overrides.get("main_neg_slope_weight", args.get("main_neg_slope_weight", 2.0))),
        "--main-pos-slope-weight",
        "1.0",
        "--turn-transition-weight",
        str(spec.overrides.get("turn_transition_weight", args.get("turn_transition_weight", 2.5))),
        "--select-turn-weight",
        "0.55",
        "--select-turn-transition-weight",
        "1.2",
        "--select-turn-transition-target",
        "0.82",
        "--select-turn-left-weight",
        "0.0",
        "--select-turn-left-target",
        "0.88",
        "--select-turn-lr-weight",
        "0.6",
        "--select-turn-lr-target",
        "0.88",
        "--select-stall-weight",
        "0.0",
        "--select-stall-target",
        "0.7",
        "--select-theta-weight",
        "0.3",
        "--select-theta-ref-deg",
        "2.0",
        "--select-theta-p95-weight",
        "0.8",
        "--select-theta-p95-target-deg",
        "1.2",
        "--select-theta-flat-p95-weight",
        str(spec.overrides.get("select_theta_flat_p95_weight", args.get("select_theta_flat_p95_weight", 0.35))),
        "--select-theta-flat-p95-target-deg",
        str(spec.overrides.get("select_theta_flat_p95_target_deg", args.get("select_theta_flat_p95_target_deg", 0.7))),
        "--select-theta-flat-peak-weight",
        "0.0",
        "--select-theta-flat-peak-target-deg",
        "3.0",
        "--select-theta-near-flat-p95-weight",
        "0.2",
        "--select-theta-near-flat-p95-target-deg",
        "0.7",
        "--select-theta-true-zero-p95-weight",
        "0.45",
        "--select-theta-true-zero-p95-target-deg",
        "0.5",
        "--select-theta-extreme-p95-weight",
        "0.6",
        "--select-theta-extreme-p95-target-deg",
        "1.2",
        "--select-theta-edge-p95-weight",
        str(spec.overrides.get("select_theta_edge_p95_weight", args.get("select_theta_edge_p95_weight", 0.7))),
        "--select-theta-edge-p95-target-deg",
        str(spec.overrides.get("select_theta_edge_p95_target_deg", args.get("select_theta_edge_p95_target_deg", 1.5))),
        "--select-theta-small-nonzero-p95-weight",
        "0.8",
        "--select-theta-small-nonzero-p95-target-deg",
        "1.0",
        "--select-theta-flat-bias-weight",
        str(spec.overrides.get("select_theta_flat_bias_weight", args.get("select_theta_flat_bias_weight", 0.3))),
        "--select-theta-flat-bias-target-deg",
        str(spec.overrides.get("select_theta_flat_bias_target_deg", args.get("select_theta_flat_bias_target_deg", 0.15))),
        "--device",
        "auto",
        "--num-workers",
        "0",
    ]
    if smoke:
        cmd.extend(["--limit-train", "256", "--limit-val", "128", "--limit-test", "128"])
    return cmd


def node_design() -> None:
    NODE_ROOT.mkdir(parents=True, exist_ok=True)
    rows = design_rows()
    write_csv(DESIGN_DIR / "tuning_design.csv", rows, ["run_id", "description", "seed101_run_tag", "seed21_run_tag", "seed42_run_tag", "overrides_json"])
    seed_prior = []
    for seed in [21, 42, 101]:
        path = SCI_ROOT / "01_loss_optimization" / f"uncertainty_seed{seed}" / "metrics_test.csv"
        if not path.exists():
            seed_prior.append({"seed": seed, "status": "missing"})
            continue
        metric = read_csv(path)[0]
        seed_prior.append(
            {
                "seed": seed,
                "status": "ok",
                "source": str(path),
                **{m: metric.get(m, "NaN") for m in OFFLINE_METRICS},
            }
        )
    write_csv(DESIGN_DIR / "seed_variance_prior.csv", seed_prior, ["seed", "status", "source", *OFFLINE_METRICS])
    contract = {
        "node_root": str(NODE_ROOT),
        "dataset": DATASET,
        "model_family": "small",
        "loss_mode": "uncertainty_weighting",
        "anchor_id": ANCHOR_ID,
        "anchor_j_control": ANCHOR_J,
        "baseline_id": BASELINE_ID,
        "v2_full_thresholds": str(V2_FULL),
        "v2_closed_loop_thresholds": str(V2_CLOSED),
        "n_seed101_designs": len(rows),
        "sentinel_target": 6,
        "top5_closed_loop_target": 5,
        "disabled_unreliable_terms": {
            "lambda_transition_focal": 0.0,
            "lambda_stall_focal": 0.0,
            "lambda_theta_smooth": 0.0,
            "theta_smooth_mode": "off",
        },
    }
    write_json(DESIGN_DIR / "tuning_contract.json", contract)
    write_text(
        DESIGN_DIR / "node0_design_report.md",
        "\n".join(
            [
                "# Node 0 Design",
                "",
                "- Created tuning design and seed variance prior.",
                "- Existing uncertainty seed21/42/101 are prior evidence only, not replacements for new Sentinel seeds.",
                "- New outputs are isolated under `results/modern_tcn_metric_rebuild/11_uncertainty_tuning/`.",
            ]
        )
        + "\n",
    )


def run_one_training(spec: RunSpec, seed: int, output_root: Path, *, smoke: bool = False) -> dict[str, Any]:
    run_tag = f"{spec.run_id}_seed{seed}"
    run_dir = output_root / run_tag
    if run_dir.exists() and (run_dir / "metrics_test.csv").exists() and (run_dir / f"modern_tcn_seed{seed}.pt").exists():
        return {"run_id": spec.run_id, "seed": seed, "run_tag": run_tag, "status": "skipped_existing", "run_dir": str(run_dir), "returncode": 0}
    cmd = command_for_run(spec, seed, output_root, smoke=smoke)
    proc = run_command(cmd, output_root / f"{run_tag}.log")
    status = "ok" if proc.returncode == 0 else "failed"
    return {"run_id": spec.run_id, "seed": seed, "run_tag": run_tag, "status": status, "run_dir": str(run_dir), "returncode": proc.returncode}


def node_smoke() -> None:
    if SMOKE_DIR.exists():
        shutil.rmtree(SMOKE_DIR)
    spec = specs()[0]
    result = run_one_training(spec, 101, SMOKE_DIR, smoke=True)
    write_csv(SMOKE_DIR / "smoke_status.csv", [result], ["run_id", "seed", "run_tag", "status", "run_dir", "returncode"])
    write_text(
        SMOKE_DIR / "smoke_report.md",
        f"# Smoke Report\n\n- run: `{result['run_tag']}`\n- status: `{result['status']}`\n- returncode: `{result['returncode']}`\n",
    )
    if result["status"] != "ok":
        raise SystemExit(f"Smoke failed: {SMOKE_DIR / (result['run_tag'] + '.log')}")


def node_train_seed101() -> None:
    status_rows = []
    for spec in specs():
        print(f"[seed101] training {spec.run_id}")
        status_rows.append(run_one_training(spec, 101, SEED101_DIR, smoke=False))
        write_csv(SEED101_DIR / "seed101_training_status.csv", status_rows, ["run_id", "seed", "run_tag", "status", "run_dir", "returncode"])
    failed = [r for r in status_rows if r["status"] == "failed"]
    if failed:
        print(f"[seed101] failed runs: {len(failed)}")


def metric_from_run(run_dir: Path) -> dict[str, Any]:
    metric_file = run_dir / "metrics_test.csv"
    if not metric_file.exists():
        return {"status": "missing_metrics"}
    row = read_csv(metric_file)[0]
    out = {k: row.get(k, "NaN") for k in row.keys()}
    out["status"] = "ok"
    out["checkpoint_file"] = row.get("checkpoint_file", str(run_dir / "modern_tcn_seed101.pt"))
    out["run_dir"] = str(run_dir)
    return out


def offline_hard(row: dict[str, Any], baseline: dict[str, Any], thresholds: dict[str, Any]) -> tuple[str, str]:
    checks = [
        ("offline_acc_main_drop", baseline["acc_main"] - num(row.get("acc_main")), thresholds["acc_main_min_drop"]),
        ("stall_recall_drop", baseline["stall_recall"] - num(row.get("stall_recall")), thresholds["stall_recall_min_drop"]),
        ("slope_recall_drop", baseline["slope_recall"] - num(row.get("slope_recall")), thresholds["slope_recall_min_drop"]),
        ("theta_edge_p95_ratio", safe_ratio(num(row.get("theta_edge_p95_abs_err")), baseline["theta_edge_p95_abs_err"]), thresholds["theta_edge_p95_max_ratio"]),
        ("flat_peak_theta_error_ratio", safe_ratio(num(row.get("flat_peak_theta_error")), baseline["flat_peak_theta_error"]), thresholds["flat_peak_theta_error_max_ratio"]),
    ]
    failures = [f"{name}={value:.6g}>{limit:.6g}" for name, value, limit in checks if math.isfinite(value) and value > float(limit)]
    return ("pass" if not failures else "fail"), "; ".join(failures) if failures else "none"


def safe_ratio(value: float, base: float) -> float:
    if not math.isfinite(value) or not math.isfinite(base) or abs(base) < 1e-12:
        return math.nan
    return value / base


def offline_score(row: dict[str, Any], baseline: dict[str, Any]) -> float:
    weights = {
        "acc_main": 0.18,
        "acc_turn": 0.10,
        "acc_turn_transition": 0.12,
        "theta_mae_deg": 0.12,
        "theta_edge_p95_abs_err": 0.15,
        "flat_peak_theta_error": 0.12,
        "flat_recall": 0.07,
        "stall_recall": 0.10,
        "slope_recall": 0.04,
    }
    total = 0.0
    used = 0.0
    for metric, weight in weights.items():
        value = num(row.get(metric))
        base = baseline[metric]
        if not math.isfinite(value) or not math.isfinite(base) or abs(base) < 1e-12:
            continue
        if metric in HIGHER_BETTER:
            component = max(0.0, (base - value) / abs(base))
        else:
            component = value / abs(base)
        total += weight * component
        used += weight
    return total / used if used else math.nan


def collect_seed101_screen() -> list[dict[str, Any]]:
    baseline = baseline_offline()
    thresholds = load_thresholds()
    rows = []
    for spec in specs():
        run_dir = SEED101_DIR / f"{spec.run_id}_seed101"
        metric = metric_from_run(run_dir)
        hard_status, failures = offline_hard(metric, baseline, thresholds) if metric["status"] == "ok" else ("missing", "missing_metrics")
        row = {
            "run_id": spec.run_id,
            "seed": 101,
            "run_tag": f"{spec.run_id}_seed101",
            "description": spec.description,
            "overrides_json": json.dumps(spec.overrides, ensure_ascii=False, sort_keys=True),
            "metric_status": metric["status"],
            "full_v2_offline_status": hard_status,
            "full_v2_offline_failures": failures,
            "offline_score": offline_score(metric, baseline) if metric["status"] == "ok" else math.nan,
            **{m: metric.get(m, "NaN") for m in OFFLINE_METRICS},
            "checkpoint_file": metric.get("checkpoint_file", ""),
            "run_dir": metric.get("run_dir", str(run_dir)),
        }
        rows.append(row)
    for rank, row in enumerate(sorted(rows, key=lambda r: (r["full_v2_offline_status"] != "pass", num(r["offline_score"]), r["run_id"])), 1):
        row["seed101_rank"] = rank
    return rows


def select_sentinel(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: dict[str, dict[str, Any]] = {}

    def add(row: dict[str, Any], reason: str) -> None:
        if row["run_id"] not in selected:
            selected[row["run_id"]] = {**row, "sentinel_reason": reason}

    hard_pass = [r for r in rows if r["full_v2_offline_status"] == "pass" and math.isfinite(num(r["offline_score"]))]
    ranked = sorted(hard_pass, key=lambda r: (num(r["offline_score"]), r["run_id"]))
    for row in ranked[:3]:
        add(row, "top3_seed101_v2_offline_score")
    if hard_pass:
        main_slot = sorted(hard_pass, key=lambda r: (-num(r["acc_main"]), -num(r["stall_recall"]), r["run_id"]))[0]
        add(main_slot, "main_protection_slot")
        theta_slot = sorted(hard_pass, key=lambda r: (num(r["theta_edge_p95_abs_err"]), num(r["flat_peak_theta_error"]), r["run_id"]))[0]
        add(theta_slot, "theta_protection_slot")
    diversity_candidates = [r for r in rows if r["run_id"] in {"u23_turn_protect_mix", "u24_control_theta_mix"} and r["full_v2_offline_status"] == "pass"]
    if diversity_candidates:
        add(sorted(diversity_candidates, key=lambda r: (num(r["offline_score"]), r["run_id"]))[0], "diversity_mix_slot")
    for row in ranked:
        if len(selected) >= 6:
            break
        add(row, "fill_next_hard_pass_rank")
    if len(selected) < 6:
        for row in sorted(rows, key=lambda r: (num(r["offline_score"]) if math.isfinite(num(r["offline_score"])) else 999, r["run_id"])):
            if len(selected) >= 6:
                break
            add(row, "fill_next_available_rank")
    out = list(selected.values())
    for idx, row in enumerate(out, 1):
        row["sentinel_rank"] = idx
    return out


def node_screen() -> None:
    rows = collect_seed101_screen()
    fields = ["run_id", "seed", "run_tag", "seed101_rank", "description", "metric_status", "full_v2_offline_status", "full_v2_offline_failures", "offline_score", *OFFLINE_METRICS, "checkpoint_file", "run_dir", "overrides_json"]
    write_csv(SCREEN_DIR / "seed101_screen_results.csv", sorted(rows, key=lambda r: num(r.get("seed101_rank"))), fields)
    sentinel = select_sentinel(rows)
    write_csv(SCREEN_DIR / "sentinel6_selection.csv", sentinel, ["sentinel_rank", "run_id", "seed101_rank", "sentinel_reason", "description", "full_v2_offline_status", "offline_score", *OFFLINE_METRICS, "overrides_json"])
    lines = ["# Sentinel6 Selection", "", "| rank | run | reason | seed101 rank | status | score |", "|---:|---|---|---:|---|---:|"]
    for row in sentinel:
        lines.append(f"| {row['sentinel_rank']} | `{row['run_id']}` | {row['sentinel_reason']} | {row['seed101_rank']} | {row['full_v2_offline_status']} | {num(row['offline_score']):.6f} |")
    write_text(SCREEN_DIR / "sentinel6_selection.md", "\n".join(lines) + "\n")


def load_spec(run_id: str) -> RunSpec:
    return next(s for s in specs() if s.run_id == run_id)


def node_train_sentinel() -> None:
    sentinel_file = SCREEN_DIR / "sentinel6_selection.csv"
    if not sentinel_file.exists():
        node_screen()
    sentinel = read_csv(sentinel_file)
    status_rows = []
    for row in sentinel:
        spec = load_spec(row["run_id"])
        for seed in [21, 42]:
            print(f"[sentinel] training {spec.run_id} seed{seed}")
            status_rows.append(run_one_training(spec, seed, MULTISEED_DIR, smoke=False))
            write_csv(MULTISEED_DIR / "sentinel_training_status.csv", status_rows, ["run_id", "seed", "run_tag", "status", "run_dir", "returncode"])
    summarize_multiseed()


def multiseed_run_rows() -> list[dict[str, Any]]:
    sentinel = read_csv(SCREEN_DIR / "sentinel6_selection.csv")
    baseline = baseline_offline()
    thresholds = load_thresholds()
    rows = []
    for sent in sentinel:
        spec = load_spec(sent["run_id"])
        for seed, root in [(101, SEED101_DIR), (21, MULTISEED_DIR), (42, MULTISEED_DIR)]:
            run_dir = root / f"{spec.run_id}_seed{seed}"
            metric = metric_from_run(run_dir)
            status, failures = offline_hard(metric, baseline, thresholds) if metric["status"] == "ok" else ("missing", "missing_metrics")
            rows.append(
                {
                    "run_id": spec.run_id,
                    "seed": seed,
                    "run_tag": f"{spec.run_id}_seed{seed}",
                    "metric_status": metric["status"],
                    "full_v2_offline_status": status,
                    "full_v2_offline_failures": failures,
                    "offline_score": offline_score(metric, baseline) if metric["status"] == "ok" else math.nan,
                    **{m: metric.get(m, "NaN") for m in OFFLINE_METRICS},
                    "checkpoint_file": metric.get("checkpoint_file", ""),
                    "run_dir": metric.get("run_dir", str(run_dir)),
                }
            )
    return rows


def summarize_multiseed() -> None:
    rows = multiseed_run_rows()
    write_csv(MULTISEED_DIR / "multiseed_run_results.csv", rows, ["run_id", "seed", "run_tag", "metric_status", "full_v2_offline_status", "full_v2_offline_failures", "offline_score", *OFFLINE_METRICS, "checkpoint_file", "run_dir"])
    summary = []
    for run_id in sorted({r["run_id"] for r in rows}):
        subset = [r for r in rows if r["run_id"] == run_id]
        pass_count = sum(1 for r in subset if r["full_v2_offline_status"] == "pass")
        scores = [num(r["offline_score"]) for r in subset if math.isfinite(num(r["offline_score"]))]
        if pass_count == 3:
            label = "robust_pass"
        elif pass_count == 2:
            label = "usable_seed_sensitive"
        else:
            label = "reject_seed_fragile"
        best = min(subset, key=lambda r: num(r["offline_score"]) if math.isfinite(num(r["offline_score"])) else 999)
        summary.append(
            {
                "run_id": run_id,
                "stability_label": label,
                "pass_count": pass_count,
                "median_offline_score": median(scores) if scores else math.nan,
                "mean_offline_score": mean(scores) if scores else math.nan,
                "best_seed": best["seed"],
                "best_seed_score": best["offline_score"],
                "best_checkpoint_file": best["checkpoint_file"],
                "best_run_dir": best["run_dir"],
            }
        )
    summary_sorted = sorted(summary, key=lambda r: ({"robust_pass": 0, "usable_seed_sensitive": 1, "reject_seed_fragile": 2}[r["stability_label"]], num(r["median_offline_score"]), r["run_id"]))
    for idx, row in enumerate(summary_sorted, 1):
        row["multiseed_rank"] = idx
    write_csv(MULTISEED_DIR / "multiseed_results.csv", summary_sorted, ["multiseed_rank", "run_id", "stability_label", "pass_count", "median_offline_score", "mean_offline_score", "best_seed", "best_seed_score", "best_checkpoint_file", "best_run_dir"])
    lines = ["# Multiseed Report", "", "| rank | run | label | pass count | median score | best seed |", "|---:|---|---|---:|---:|---:|"]
    for row in summary_sorted:
        lines.append(f"| {row['multiseed_rank']} | `{row['run_id']}` | {row['stability_label']} | {row['pass_count']} | {num(row['median_offline_score']):.6f} | {row['best_seed']} |")
    write_text(MULTISEED_DIR / "multiseed_report.md", "\n".join(lines) + "\n")


def top5_rows() -> list[dict[str, str]]:
    results = read_csv(MULTISEED_DIR / "multiseed_results.csv")
    eligible = [r for r in results if r["stability_label"] in {"robust_pass", "usable_seed_sensitive"}]
    if len(eligible) < 5:
        eligible = results
    return eligible[:5]


def node_export_top5() -> None:
    rows = top5_rows()
    manifest = []
    for row in rows:
        run_id = row["run_id"]
        best_seed = int(float(row["best_seed"]))
        run_tag = f"{run_id}_seed{best_seed}"
        checkpoint = Path(row["best_checkpoint_file"])
        export_dir = TOP5_DIR / "00_exported_onnx" / run_tag
        export_dir.mkdir(parents=True, exist_ok=True)
        onnx_file = export_dir / f"{run_tag}.onnx"
        sample_file = export_dir / f"{run_tag}_pytorch_reference.mat"
        if not onnx_file.exists():
            proc = run_command(
                [
                    sys.executable,
                    str(EXPORT),
                    "--checkpoint",
                    str(checkpoint),
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
                export_dir / f"{run_tag}_export.log",
            )
            export_status = "ok" if proc.returncode == 0 else "failed"
        else:
            export_status = "skipped_existing"
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
                export_dir / f"{run_tag}_onnxruntime.log",
            )
            consistency_json = onnx_file.with_name(onnx_file.stem + "_onnxruntime_consistency.json")
            consistency_pass = False
            if consistency_json.exists():
                consistency_pass = bool(json.loads(consistency_json.read_text(encoding="utf-8")).get("pass"))
            consistency_status = "ok" if proc.returncode == 0 and consistency_pass else "failed"
        else:
            consistency_json = export_dir / f"{run_tag}_onnxruntime_consistency.json"
            consistency_status = "missing_export"
            consistency_pass = False
        manifest.append(
            {
                "run_id": run_id,
                "candidate_id": run_tag,
                "seed": best_seed,
                "stability_label": row["stability_label"],
                "checkpoint_file": str(checkpoint),
                "onnx_file": str(onnx_file),
                "sample_file": str(sample_file),
                "export_status": export_status,
                "consistency_json": str(consistency_json),
                "consistency_pass": consistency_pass,
                "selected_for_closed_loop": consistency_pass,
            }
        )
    write_csv(TOP5_DIR / "top5_closed_loop_manifest.csv", manifest, ["run_id", "candidate_id", "seed", "stability_label", "checkpoint_file", "onnx_file", "sample_file", "export_status", "consistency_json", "consistency_pass", "selected_for_closed_loop"])
    write_json(TOP5_DIR / "top5_manifest.json", manifest)


def aggregate_path_metrics() -> list[dict[str, Any]]:
    manifest = read_csv(TOP5_DIR / "top5_closed_loop_manifest.csv")
    selected = [r for r in manifest if str(r["selected_for_closed_loop"]).lower() == "true"]
    rows = []
    baseline_rows = [r for r in read_csv(FORMAL_PATH_METRICS) if r["controller"] == BASELINE_ID]
    anchor_rows = [r for r in read_csv(FORMAL_PATH_METRICS) if r["controller"] == ANCHOR_ID]
    for row in baseline_rows:
        rows.append({**row, "candidate_id": BASELINE_ID, "source": str(FORMAL_PATH_METRICS)})
    for row in anchor_rows:
        rows.append({**row, "candidate_id": ANCHOR_ID, "source": str(FORMAL_PATH_METRICS)})
    for cand in selected:
        for path_dir in (TOP5_DIR / "01_closed_loop_runs").glob("path_*"):
            summary = path_dir / "uncertainty_tuning_top5_summary.csv"
            if not summary.exists():
                continue
            for row in read_csv(summary):
                if row["controller"] == cand["candidate_id"]:
                    rows.append({**row, "candidate_id": cand["candidate_id"], "source": str(summary)})
    return rows


def aggregate_by_candidate(path_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out = {}
    for cid in sorted({r["candidate_id"] for r in path_rows}):
        subset = [r for r in path_rows if r["candidate_id"] == cid]
        agg = {"candidate_id": cid, "n_paths": len(subset)}
        for metric in ["ey_rmse", "xy_rmse", "epsi_rmse", "j_du", "omega_cmd_rms", "viol_rate", "theta_mae_deg", "main_acc_pct", "turn_acc_pct"]:
            values = [num(r.get(metric)) for r in subset if math.isfinite(num(r.get(metric)))]
            agg[f"{metric}_mean"] = mean(values) if values else math.nan
        out[cid] = agg
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
        r = safe_ratio(num(row.get(f"{metric}_mean")), num(baseline.get(f"{metric}_mean")))
        if math.isfinite(r):
            terms.append(r)
    return mean(terms) if terms else math.nan


def node_summarize_closed_loop() -> None:
    path_rows = aggregate_path_metrics()
    write_csv(TOP5_DIR / "closed_loop_path_metrics.csv", path_rows, sorted({k for r in path_rows for k in r.keys()}))
    agg = aggregate_by_candidate(path_rows)
    baseline = agg[BASELINE_ID]
    thresholds = json.loads(V2_CLOSED.read_text(encoding="utf-8"))
    final = []
    for cid, row in agg.items():
        status, failures = ("pass", "reference") if cid == BASELINE_ID else closed_loop_hard(row, baseline, thresholds)
        jc = 1.0 if cid == BASELINE_ID else j_control(row, baseline)
        final.append({**row, "J_control": jc, "closed_loop_v2_status": status, "closed_loop_v2_failures": failures})
    for rank, row in enumerate(sorted(final, key=lambda r: num(r["J_control"])), 1):
        row["rank_by_J_control"] = rank
    fields = ["candidate_id", "n_paths", "J_control", "rank_by_J_control", "closed_loop_v2_status", "closed_loop_v2_failures", "ey_rmse_mean", "xy_rmse_mean", "epsi_rmse_mean", "j_du_mean", "omega_cmd_rms_mean", "viol_rate_mean", "theta_mae_deg_mean", "main_acc_pct_mean", "turn_acc_pct_mean"]
    write_csv(TOP5_DIR / "closed_loop_results.csv", sorted(final, key=lambda r: num(r["rank_by_J_control"])), fields)
    lines = ["# Top5 Closed-Loop Report", "", "| rank | candidate | J_control | v2 status | failures |", "|---:|---|---:|---|---|"]
    for row in sorted(final, key=lambda r: num(r["rank_by_J_control"])):
        lines.append(f"| {row['rank_by_J_control']} | `{row['candidate_id']}` | {num(row['J_control']):.6f} | {row['closed_loop_v2_status']} | {row['closed_loop_v2_failures']} |")
    write_text(TOP5_DIR / "closed_loop_report.md", "\n".join(lines) + "\n")


def node_decision() -> None:
    node_summarize_closed_loop()
    multiseed = {r["run_id"]: r for r in read_csv(MULTISEED_DIR / "multiseed_results.csv")}
    manifest = {r["candidate_id"]: r for r in read_csv(TOP5_DIR / "top5_closed_loop_manifest.csv")}
    closed = read_csv(TOP5_DIR / "closed_loop_results.csv")
    rows = []
    for row in closed:
        cid = row["candidate_id"]
        if cid in {BASELINE_ID, ANCHOR_ID}:
            label = "Reference"
            stability = "reference"
            run_id = cid
        else:
            run_id = manifest[cid]["run_id"]
            stability = multiseed[run_id]["stability_label"]
            j = num(row["J_control"])
            if stability == "robust_pass" and row["closed_loop_v2_status"] == "pass" and j < ANCHOR_J:
                label = "Promoted"
            elif stability == "usable_seed_sensitive" and row["closed_loop_v2_status"] == "pass" and j < ANCHOR_J:
                label = "Provisional"
            elif row["closed_loop_v2_status"] == "pass" and ANCHOR_J <= j < 1.0:
                label = "SandboxOnly"
            else:
                label = "Reject"
        rows.append({**row, "run_id": run_id, "stability_label": stability, "final_class": label})
    write_csv(DECISION_DIR / "final_candidate_table.csv", rows, ["candidate_id", "run_id", "stability_label", "final_class", "J_control", "rank_by_J_control", "closed_loop_v2_status", "closed_loop_v2_failures", "n_paths", "ey_rmse_mean", "xy_rmse_mean", "epsi_rmse_mean", "j_du_mean", "omega_cmd_rms_mean", "main_acc_pct_mean", "turn_acc_pct_mean"])
    promoted = [r for r in rows if r["final_class"] == "Promoted"]
    lines = [
        "# Uncertainty Tuning Final Report",
        "",
        f"- anchor: `{ANCHOR_ID}`, J_control={ANCHOR_J:.6f}",
        f"- promoted count: {len(promoted)}",
        "",
        "| class | candidate | J_control | stability | v2 status |",
        "|---|---|---:|---|---|",
    ]
    for row in sorted(rows, key=lambda r: num(r["rank_by_J_control"])):
        lines.append(f"| {row['final_class']} | `{row['candidate_id']}` | {num(row['J_control']):.6f} | {row['stability_label']} | {row['closed_loop_v2_status']} |")
    write_text(DECISION_DIR / "uncertainty_tuning_final_report.md", "\n".join(lines) + "\n")
    write_text(
        DECISION_DIR / "handoff_next_window.md",
        "\n".join(
            [
                "# Handoff Next Window",
                "",
                f"- promoted candidates: {', '.join(r['candidate_id'] for r in promoted) if promoted else 'none'}",
                "- Use `final_candidate_table.csv` as the decision source.",
                "- Do not overwrite v1/v2 threshold files unless a new freeze window is explicitly approved.",
            ]
        )
        + "\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["design", "smoke", "train-seed101", "screen", "train-sentinel", "export-top5", "summarize-closed-loop", "decision", "all-offline"])
    args = parser.parse_args()
    if args.command == "design":
        node_design()
    elif args.command == "smoke":
        node_smoke()
    elif args.command == "train-seed101":
        node_train_seed101()
    elif args.command == "screen":
        node_screen()
    elif args.command == "train-sentinel":
        node_train_sentinel()
    elif args.command == "export-top5":
        node_export_top5()
    elif args.command == "summarize-closed-loop":
        node_summarize_closed_loop()
    elif args.command == "decision":
        node_decision()
    elif args.command == "all-offline":
        node_design()
        node_smoke()
        node_train_seed101()
        node_screen()
        node_train_sentinel()
        node_export_top5()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
