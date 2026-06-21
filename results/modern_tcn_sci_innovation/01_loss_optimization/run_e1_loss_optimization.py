"""E1 / Phase 1 loss-only optimization runner for ModernTCN-small.

This script is intentionally scoped to:
results/modern_tcn_sci_innovation/01_loss_optimization/

It never exports ONNX, never calls MATLAB/Simulink, and refuses to overwrite
non-empty run directories when training.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import py_compile
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[3]
E1_DIR = ROOT / "results" / "modern_tcn_sci_innovation" / "01_loss_optimization"
E0_DIR = ROOT / "results" / "modern_tcn_sci_innovation" / "00_baseline_lock"
BASELINE_METRICS = E0_DIR / "baseline_offline_metrics.csv"
E0_DECISION = E0_DIR / "e0_decision.json"
BASELINE_LOCK = E0_DIR / "baseline_lock.md"
DATASET = ROOT / "data" / "tcn" / "ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat"
TRAIN_SCRIPT = ROOT / "src" / "ModernTCN" / "train_modern_tcn.py"
METRICS_SCRIPT = ROOT / "src" / "ModernTCN" / "modern_tcn_metrics.py"

SEEDS = [21, 42, 101]
METHODS = {
    "uncertainty_weighting": "uncertainty",
    "gradnorm": "gradnorm",
}
CORE_METRICS = [
    "acc_main",
    "acc_turn",
    "acc_turn_transition",
    "theta_mae_deg",
    "flat_recall",
    "stall_recall",
    "slope_recall",
    "theta_edge_p95_abs_err",
    "flat_peak_theta_error",
]
LOWER_IS_BETTER = {"theta_mae_deg", "theta_edge_p95_abs_err", "flat_peak_theta_error"}
PROTECTION_TOLERANCE = {
    "acc_main": -0.003,
    "acc_turn": -0.005,
    "flat_recall": -0.010,
    "stall_recall": -0.050,
    "slope_recall": -0.005,
}

BASELINE_ARGS = [
    "--model-family",
    "small",
    "--dataset-file",
    str(DATASET),
    "--channels",
    "64",
    "--blocks",
    "5",
    "--kernel-size",
    "31",
    "--dropout",
    "0.15",
    "--temporal-padding",
    "same",
    "--lambda-turn",
    "0.2",
    "--lambda-theta",
    "0.55",
    "--lambda-theta-flat",
    "0.12",
    "--theta-flat-loss-mode",
    "near_zero",
    "--theta-flat-zero-tol-deg",
    "0.3",
    "--lambda-theta-error-excess",
    "0.05",
    "--lambda-theta-true-zero-excess",
    "0.1",
    "--lambda-theta-active-excess",
    "0.1",
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
    "2.0",
    "--main-pos-slope-weight",
    "1.0",
    "--theta-neg-weight",
    "1.0",
    "--theta-pos-weight",
    "1.0",
    "--turn-transition-weight",
    "2.5",
    "--select-turn-weight",
    "0.55",
    "--select-turn-transition-weight",
    "1.2",
    "--select-turn-transition-target",
    "0.82",
    "--select-turn-left-target",
    "0.88",
    "--select-turn-lr-weight",
    "0.6",
    "--select-turn-lr-target",
    "0.88",
    "--select-theta-weight",
    "0.3",
    "--select-theta-ref-deg",
    "2.0",
    "--select-theta-p95-weight",
    "0.8",
    "--select-theta-p95-target-deg",
    "1.2",
    "--select-theta-flat-p95-weight",
    "0.35",
    "--select-theta-flat-p95-target-deg",
    "0.7",
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
    "0.7",
    "--select-theta-edge-p95-target-deg",
    "1.5",
    "--select-theta-small-nonzero-p95-weight",
    "0.8",
    "--select-theta-small-nonzero-p95-target-deg",
    "1.0",
    "--select-theta-flat-bias-weight",
    "0.3",
    "--select-theta-flat-bias-target-deg",
    "0.15",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run E1 loss-only optimization.")
    parser.add_argument("--smoke-only", action="store_true")
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--epochs", type=int, default=120)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--loss-weight-lr", type=float, default=1e-3)
    args = parser.parse_args()

    E1_DIR.mkdir(parents=True, exist_ok=True)
    try:
        py_compile.compile(str(TRAIN_SCRIPT), doraise=True)
        py_compile.compile(str(METRICS_SCRIPT), doraise=True)
        preflight = run_preflight(skip_existing=args.skip_existing)
        write_preflight(preflight)
        smoke_rows = run_smoke(args.device)
        write_smoke_report(smoke_rows)
        if args.smoke_only:
            return 0
        run_full_training(args)
        rows = build_master_table()
        write_master_table(rows)
        decision = build_decision(rows)
        write_summary(rows, decision)
        write_decision(decision)
        verify_no_forbidden_outputs()
        return 0 if decision["e1_status"] == "PASS" else 2
    except Exception as exc:
        write_failure_report(exc)
        raise


def run_preflight(skip_existing: bool = False) -> Dict[str, object]:
    e0 = read_json(E0_DECISION)
    baseline = read_csv(BASELINE_METRICS)[0]
    blocked = []
    if e0.get("decision") != "PASS":
        blocked.append("E0 decision is not PASS")
    if not e0.get("can_enter_e1", False):
        blocked.append("E0 can_enter_e1 is false")
    identity = e0.get("baseline_identity", {})
    for key, expected in {
        "input_dim": 22,
        "seq_len": 128,
        "feature_contract": "passive17_plus_all5",
        "plant_revision": "agv_physics_v2_plantfix",
    }.items():
        if identity.get(key) != expected:
            blocked.append(f"baseline_identity.{key}={identity.get(key)!r}, expected {expected!r}")
    if not DATASET.exists():
        blocked.append(f"dataset missing: {DATASET}")
    for path in planned_run_dirs():
        if path.exists() and any(path.iterdir()):
            mode = loss_mode_for_run_dir(path)
            if not skip_existing:
                blocked.append(f"would overwrite non-empty output dir: {path}")
            else:
                ok, reason = validate_run_dir(path, mode, smoke=False)
                if not ok:
                    blocked.append(f"existing output dir is incomplete or invalid: {path}; {reason}")
    return {
        "status": "PASS" if not blocked else "FAIL",
        "blocked": blocked,
        "e0_decision": e0.get("decision"),
        "can_enter_e1": e0.get("can_enter_e1"),
        "dataset": str(DATASET),
        "baseline_metrics": baseline,
        "planned_run_dirs": [str(p) for p in planned_run_dirs()],
        "skip_existing": skip_existing,
        "git_hash": git(["rev-parse", "HEAD"]),
        "git_status_short": git(["status", "--short"], check=False),
    }


def write_preflight(preflight: Dict[str, object]) -> None:
    lines = [
        "# E1 Engineering Preflight",
        "",
        f"- status: {preflight['status']}",
        f"- E0 decision: {preflight['e0_decision']}",
        f"- can_enter_e1: {preflight['can_enter_e1']}",
        f"- dataset: `{preflight['dataset']}`",
        f"- skip_existing: {preflight.get('skip_existing', False)}",
        f"- git_hash: `{preflight['git_hash']}`",
        "- scope: E1 / 01_loss_optimization only; no ONNX; no MATLAB/Simulink.",
        "",
        "## Planned Output Dirs",
        "",
    ]
    lines.extend(f"- `{p}`" for p in preflight["planned_run_dirs"])
    if preflight["blocked"]:
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {x}" for x in preflight["blocked"])
    (E1_DIR / "e1_preflight.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if preflight["status"] != "PASS":
        raise RuntimeError("E1 preflight failed: " + "; ".join(preflight["blocked"]))


def run_smoke(device: str) -> List[Dict[str, object]]:
    smoke_root = E1_DIR / "_smoke"
    if smoke_root.exists():
        shutil.rmtree(smoke_root)
    smoke_root.mkdir(parents=True, exist_ok=True)
    rows = []
    for mode in ["fixed", "uncertainty_weighting", "gradnorm"]:
        run_tag = f"{mode}_smoke_seed21"
        cmd = base_train_cmd(
            mode=mode,
            seed=21,
            output_root=smoke_root,
            run_tag=run_tag,
            device=device,
            epochs=2,
            batch_size=64,
            extra=[
                "--min-epochs",
                "1",
                "--patience",
                "2",
                "--limit-train",
                "256",
                "--limit-val",
                "128",
                "--limit-test",
                "128",
                "--no-overwrite",
            ],
        )
        result = run_cmd(cmd, smoke_root / f"{run_tag}.log")
        run_dir = smoke_root / run_tag
        ok, reason = validate_run_dir(run_dir, mode, smoke=True)
        rows.append(
            {
                "loss_mode": mode,
                "run_tag": run_tag,
                "returncode": result,
                "status": "PASS" if result == 0 and ok else "FAIL",
                "reason": reason,
                "run_dir": str(run_dir),
            }
        )
    failures = [r for r in rows if r["status"] != "PASS"]
    if failures:
        raise RuntimeError(f"E1 smoke failed: {failures}")
    return rows


def write_smoke_report(rows: List[Dict[str, object]]) -> None:
    lines = ["# E1 Smoke Report", "", "| loss_mode | status | run_dir | reason |", "|---|---|---|---|"]
    for row in rows:
        lines.append(f"| {row['loss_mode']} | {row['status']} | `{row['run_dir']}` | {row['reason']} |")
    (E1_DIR / "e1_smoke_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_full_training(args: argparse.Namespace) -> None:
    for mode, prefix in METHODS.items():
        for seed in SEEDS:
            run_tag = f"{prefix}_seed{seed}"
            run_dir = E1_DIR / run_tag
            if args.skip_existing and run_dir.exists() and (run_dir / "metrics_test.csv").exists():
                continue
            cmd = base_train_cmd(
                mode=mode,
                seed=seed,
                output_root=E1_DIR,
                run_tag=run_tag,
                device=args.device,
                epochs=args.epochs,
                batch_size=args.batch_size,
                lr=args.lr,
                loss_weight_lr=args.loss_weight_lr,
                extra=["--no-overwrite"],
            )
            result = run_cmd(cmd, E1_DIR / f"{run_tag}.log")
            if result != 0:
                if mode == "gradnorm":
                    (run_dir / "GRADNORM_STOPPED.md").write_text(
                        "# GradNorm stopped\n\nTraining returned non-zero. See sibling log file.\n",
                        encoding="utf-8",
                    )
                    return
                raise RuntimeError(f"training failed for {run_tag}")
            ok, reason = validate_run_dir(run_dir, mode, smoke=False)
            if not ok:
                raise RuntimeError(f"run validation failed for {run_tag}: {reason}")


def base_train_cmd(
    mode: str,
    seed: int,
    output_root: Path,
    run_tag: str,
    device: str,
    epochs: int,
    batch_size: int,
    lr: float = 1e-3,
    loss_weight_lr: float = 1e-3,
    extra: Iterable[str] = (),
) -> List[str]:
    return [
        sys.executable,
        str(TRAIN_SCRIPT),
        "--seed",
        str(seed),
        "--loss-mode",
        mode,
        "--output-root",
        str(output_root),
        "--run-tag",
        run_tag,
        "--epochs",
        str(epochs),
        "--batch-size",
        str(batch_size),
        "--lr",
        str(lr),
        "--loss-weight-lr",
        str(loss_weight_lr),
        "--device",
        device,
        "--gradnorm-update-interval",
        "0",
        *BASELINE_ARGS,
        *list(extra),
    ]


def validate_run_dir(run_dir: Path, mode: str, smoke: bool) -> Tuple[bool, str]:
    required = ["config.json", "git_hash.txt", "dataset_contract_copy.json", "feature_names.txt", "metrics_test.csv"]
    missing = [name for name in required if not (run_dir / name).exists()]
    if missing:
        return False, "missing " + ",".join(missing)
    cfg = read_json(run_dir / "config.json")
    if cfg.get("loss_mode") not in {mode, "fixed"}:
        return False, f"config loss_mode={cfg.get('loss_mode')}"
    contract = cfg.get("dataset_contract", {})
    if contract.get("input_dim") != 22 or contract.get("seq_len") != 128:
        return False, f"bad input contract {contract.get('seq_len')}x{contract.get('input_dim')}"
    history_files = list(run_dir.glob("*_history.csv"))
    if not history_files:
        return False, "missing history csv"
    history_rows = read_csv(history_files[0])
    required_history = ["train_loss_main", "train_loss_turn", "train_loss_theta", "val_loss_main", "val_loss_turn", "val_loss_theta"]
    if history_rows:
        missing_history = [key for key in required_history if key not in history_rows[0]]
        if missing_history:
            return False, "missing history fields " + ",".join(missing_history)
        if mode == "uncertainty_weighting":
            for key in ["s_main", "s_turn", "s_theta", "weight_main", "weight_turn", "weight_theta"]:
                if key not in history_rows[0]:
                    return False, f"missing uncertainty history field {key}"
        if mode == "gradnorm":
            for key in ["task_weight_main", "task_weight_turn", "task_weight_theta", "grad_norm_main", "grad_norm_turn", "grad_norm_theta"]:
                if key not in history_rows[0]:
                    return False, f"missing gradnorm history field {key}"
    if not smoke and not (run_dir / "config.json").exists():
        return False, "missing full config"
    return True, "ok"


def build_master_table() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    baseline = enrich_metric_row(read_csv(BASELINE_METRICS)[0])
    baseline["loss_mode"] = "baseline"
    baseline["run_tag"] = "baseline_lock"
    baseline["seed"] = "101"
    baseline["eligible"] = "reference"
    rows.append(baseline)
    for mode, prefix in METHODS.items():
        for seed in SEEDS:
            run_dir = E1_DIR / f"{prefix}_seed{seed}"
            metrics_file = run_dir / "metrics_test.csv"
            if not metrics_file.exists():
                rows.append({"loss_mode": mode, "run_tag": run_dir.name, "seed": seed, "status": "MISSING"})
                continue
            row = enrich_metric_row(read_csv(metrics_file)[0])
            row["loss_mode"] = mode
            row["run_tag"] = run_dir.name
            row["seed"] = seed
            row["config_file"] = str(run_dir / "config.json")
            row["status"] = "OK"
            for metric in CORE_METRICS:
                row[f"delta_{metric}"] = metric_delta(metric, as_float(row.get(metric)), as_float(baseline.get(metric)))
            row["eligible"], row["eligibility_reason"] = run_eligible(row, baseline)
            rows.append(row)
    return rows


def write_master_table(rows: List[Dict[str, object]]) -> None:
    keys: List[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with (E1_DIR / "loss_optimization_master_table.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def build_decision(rows: List[Dict[str, object]]) -> Dict[str, object]:
    method_stats = []
    baseline = next(r for r in rows if r.get("loss_mode") == "baseline")
    for mode in METHODS:
        method_rows = [r for r in rows if r.get("loss_mode") == mode and r.get("status") == "OK"]
        if not method_rows:
            method_stats.append({"loss_mode": mode, "eligible": False, "reason": "no completed runs", "score": -999})
            continue
        medians: Dict[str, float] = {}
        improvements = 0
        degradations = 0
        for metric in CORE_METRICS:
            values = [as_float(r.get(metric)) for r in method_rows if is_finite(as_float(r.get(metric)))]
            medians[metric] = median(values)
            delta = metric_delta(metric, medians[metric], as_float(baseline.get(metric)))
            if delta > 0:
                improvements += 1
            elif delta < 0:
                degradations += 1
        eligible_rows = [r for r in method_rows if r.get("eligible") == "yes"]
        protection_ok = bool(eligible_rows)
        score = improvements - degradations
        method_stats.append(
            {
                "loss_mode": mode,
                "n_runs": len(method_rows),
                "n_eligible_runs": len(eligible_rows),
                "eligible": protection_ok,
                "median_metrics": medians,
                "improvements_vs_baseline": improvements,
                "degradations_vs_baseline": degradations,
                "score": score,
                "reason": "ok" if protection_ok else "protection metrics failed or no eligible runs",
            }
        )
    promotable = [m for m in method_stats if m["eligible"] and m["score"] > 0]
    if promotable:
        best = sorted(promotable, key=lambda x: (x["score"], x["improvements_vs_baseline"], x["n_eligible_runs"]), reverse=True)[0]
        recommendation = best["loss_mode"]
        can_enter_e2 = True
        e1_status = "PASS"
    else:
        best = {"loss_mode": "fixed", "reason": "dynamic losses did not beat baseline"}
        recommendation = "fixed"
        can_enter_e2 = True
        e1_status = "PASS"
    return {
        "phase": "E1_loss_optimization",
        "e1_status": e1_status,
        "can_enter_e2": can_enter_e2,
        "recommended_e2_loss_mode": recommendation,
        "best_loss_mode": best["loss_mode"],
        "method_stats": method_stats,
        "baseline_source": str(BASELINE_METRICS),
        "no_onnx_export": True,
        "no_matlab_simulink_closed_loop": True,
        "no_baseline_overwrite": True,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }


def write_summary(rows: List[Dict[str, object]], decision: Dict[str, object]) -> None:
    method_lines = []
    for stat in decision["method_stats"]:
        method_lines.append(
            f"- {stat['loss_mode']}: score={stat['score']}, eligible_runs={stat.get('n_eligible_runs', 0)}, "
            f"improvements={stat.get('improvements_vs_baseline', 0)}, degradations={stat.get('degradations_vs_baseline', 0)}, reason={stat['reason']}"
        )
    lines = [
        "# E1 Loss Optimization Summary",
        "",
        f"- E1 status: {decision['e1_status']}",
        f"- can enter E2: {decision['can_enter_e2']}",
        f"- recommended E2 loss_mode: `{decision['recommended_e2_loss_mode']}`",
        f"- baseline source: `{BASELINE_METRICS}`",
        "- no ONNX export: True",
        "- no MATLAB/Simulink closed-loop: True",
        "",
        "## Method Ranking",
        "",
        *method_lines,
        "",
        "## Evidence",
        "",
        f"- master table: `{E1_DIR / 'loss_optimization_master_table.csv'}`",
        f"- decision json: `{E1_DIR / 'loss_optimization_decision.json'}`",
        f"- smoke report: `{E1_DIR / 'e1_smoke_report.md'}`",
        f"- preflight: `{E1_DIR / 'e1_preflight.md'}`",
    ]
    (E1_DIR / "loss_optimization_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_decision(decision: Dict[str, object]) -> None:
    (E1_DIR / "loss_optimization_decision.json").write_text(
        json.dumps(decision, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def verify_no_forbidden_outputs() -> None:
    onnx = list(E1_DIR.rglob("*.onnx"))
    if onnx:
        raise RuntimeError(f"forbidden ONNX files under E1: {onnx}")


def write_failure_report(exc: Exception) -> None:
    E1_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# E1 Failure Report",
        "",
        f"- error_type: `{type(exc).__name__}`",
        f"- error: `{exc}`",
        "- no ONNX export requested by this script.",
        "- no MATLAB/Simulink closed-loop requested by this script.",
    ]
    (E1_DIR / "failure_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_eligible(row: Dict[str, object], baseline: Dict[str, object]) -> Tuple[str, str]:
    reasons = []
    for metric, tolerance in PROTECTION_TOLERANCE.items():
        value = as_float(row.get(metric))
        base = as_float(baseline.get(metric))
        if is_finite(value) and is_finite(base) and value < base + tolerance:
            reasons.append(f"{metric} {value:.6g} < baseline+tolerance {base + tolerance:.6g}")
    return ("yes", "ok") if not reasons else ("no", "; ".join(reasons))


def metric_delta(metric: str, value: float, baseline: float) -> float:
    if not is_finite(value) or not is_finite(baseline):
        return float("nan")
    return baseline - value if metric in LOWER_IS_BETTER else value - baseline


def enrich_metric_row(row: Dict[str, object]) -> Dict[str, object]:
    out = dict(row)
    for key in list(out):
        value = as_float(out[key])
        if is_finite(value):
            out[key] = value
    if "theta_edge_p95_abs_err" not in out or not is_finite(as_float(out.get("theta_edge_p95_abs_err"))):
        out["theta_edge_p95_abs_err"] = max(
            as_float(out.get("theta_neg_10_8_p95_abs_err_deg")),
            as_float(out.get("theta_pos_8_10_p95_abs_err_deg")),
        )
    if "flat_peak_theta_error" not in out or not is_finite(as_float(out.get("flat_peak_theta_error"))):
        out["flat_peak_theta_error"] = as_float(out.get("theta_flat_abs_max_deg"))
    return out


def planned_run_dirs() -> List[Path]:
    return [E1_DIR / f"{prefix}_seed{seed}" for prefix in METHODS.values() for seed in SEEDS]


def loss_mode_for_run_dir(path: Path) -> str:
    name = path.name
    if name.startswith("uncertainty_"):
        return "uncertainty_weighting"
    if name.startswith("gradnorm_"):
        return "gradnorm"
    return "fixed"


def run_cmd(cmd: List[str], log_file: Path) -> int:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("w", encoding="utf-8") as log:
        proc = subprocess.run(cmd, cwd=str(ROOT), stdout=log, stderr=subprocess.STDOUT, text=True)
    return int(proc.returncode)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def read_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def git(args: List[str], check: bool = True) -> str:
    proc = subprocess.run(["git", *args], cwd=str(ROOT), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if check and proc.returncode != 0:
        raise RuntimeError(proc.stdout.strip())
    return proc.stdout.strip()


def as_float(value: object) -> float:
    try:
        return float(value)
    except Exception:
        return float("nan")


def is_finite(value: float) -> bool:
    return math.isfinite(value)


def median(values: List[float]) -> float:
    clean = sorted(v for v in values if is_finite(v))
    if not clean:
        return float("nan")
    mid = len(clean) // 2
    if len(clean) % 2:
        return clean[mid]
    return 0.5 * (clean[mid - 1] + clean[mid])


if __name__ == "__main__":
    raise SystemExit(main())
