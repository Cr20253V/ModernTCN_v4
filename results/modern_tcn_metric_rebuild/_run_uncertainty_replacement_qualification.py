from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path
from statistics import mean, median
from typing import Any


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent.parent
SCI_ROOT = PROJECT_ROOT / "results" / "modern_tcn_sci_innovation"
NODE_ROOT = ROOT / "12_uncertainty_replacement_qualification"
LOCK_DIR = NODE_ROOT / "00_evidence_lock"
TRAIN_DIR = NODE_ROOT / "01_same_recipe_multiseed"
OFFLINE_DIR = NODE_ROOT / "02_offline_multiseed"
CLOSED_DIR = NODE_ROOT / "03_closed_loop_representatives"
DECISION_DIR = NODE_ROOT / "04_replacement_decision"

TRAIN = PROJECT_ROOT / "src" / "ModernTCN" / "train_modern_tcn.py"
EXPORT = PROJECT_ROOT / "src" / "ModernTCN" / "export_modern_tcn_onnx.py"
CHECK_ONNX = PROJECT_ROOT / "src" / "ModernTCN" / "check_onnxruntime_consistency.py"
ANCHOR_ID = "uncertainty_seed101_rerun_20260622"
ANCHOR_DIR = SCI_ROOT / "01_loss_optimization" / ANCHOR_ID
BASELINE_ID = "baseline_lock"
BASELINE_MATRIX = ROOT / "03_rerank_existing_experiments" / "candidate_metric_matrix.csv"
V2_FULL = ROOT / "10_threshold_recalibration" / "hard_constraint_thresholds_v2_full_proposed.json"
V2_CLOSED = ROOT / "10_threshold_recalibration" / "hard_constraint_thresholds_v2_closed_loop_proposed.json"
FORMAL_PATH_METRICS = ROOT / "05_sandbox_closed_loop_if_needed" / "03_formal_validation" / "formal_validation_path_metrics.csv"
TOP5_CLOSED_RESULTS = ROOT / "11_uncertainty_tuning" / "04_closed_loop_top5" / "closed_loop_results.csv"

SEEDS = [21, 42, 101]
NEW_SEEDS = [21, 42]
RUN_TAG_PREFIX = "uncertainty_anchor_same_recipe"
DEPLOY_ID_PREFIX = "ua_seed"

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


def baseline_offline() -> dict[str, Any]:
    row = next(r for r in read_csv(BASELINE_MATRIX) if r["candidate_id"] == BASELINE_ID)
    return {m: num(row.get(m)) for m in OFFLINE_METRICS}


def metric_alias(row: dict[str, str], metric: str) -> float:
    if metric in row:
        return num(row[metric])
    aliases = {
        "theta_edge_p95_abs_err": "theta_edge_p95_abs_err",
        "flat_peak_theta_error": "flat_peak_theta_error",
    }
    return num(row.get(aliases.get(metric, metric)))


def seed_run_tag(seed: int) -> str:
    if seed == 101:
        return ANCHOR_ID
    return f"{RUN_TAG_PREFIX}_seed{seed}"


def seed_run_dir(seed: int) -> Path:
    if seed == 101:
        return ANCHOR_DIR
    return TRAIN_DIR / seed_run_tag(seed)


def checkpoint_for_seed(seed: int) -> Path:
    return seed_run_dir(seed) / f"modern_tcn_seed{seed}.pt"


def train_command(seed: int) -> list[str]:
    args = dict(anchor_cli_args())
    args["seed"] = seed
    args["output_root"] = str(TRAIN_DIR)
    args["run_tag"] = seed_run_tag(seed)
    args["no_overwrite"] = True
    args["dry_run"] = False
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


def node_lock() -> None:
    NODE_ROOT.mkdir(parents=True, exist_ok=True)
    cfg = anchor_config()
    lock_rows = [
        {
            "artifact": "anchor_config",
            "role": "frozen_anchor_recipe",
            "path": str(ANCHOR_DIR / "config.json"),
            "exists": (ANCHOR_DIR / "config.json").exists(),
        },
        {
            "artifact": "anchor_checkpoint",
            "role": "seed101_reference_checkpoint",
            "path": str(ANCHOR_DIR / "modern_tcn_seed101.pt"),
            "exists": (ANCHOR_DIR / "modern_tcn_seed101.pt").exists(),
        },
        {
            "artifact": "anchor_metrics_test",
            "role": "seed101_offline_reference",
            "path": str(ANCHOR_DIR / "metrics_test.csv"),
            "exists": (ANCHOR_DIR / "metrics_test.csv").exists(),
        },
        {
            "artifact": "formal_path_metrics",
            "role": "baseline_and_anchor_closed_loop_reference",
            "path": str(FORMAL_PATH_METRICS),
            "exists": FORMAL_PATH_METRICS.exists(),
        },
        {
            "artifact": "v2_full_thresholds",
            "role": "offline_gate",
            "path": str(V2_FULL),
            "exists": V2_FULL.exists(),
        },
        {
            "artifact": "v2_closed_loop_thresholds",
            "role": "closed_loop_gate",
            "path": str(V2_CLOSED),
            "exists": V2_CLOSED.exists(),
        },
    ]
    write_csv(LOCK_DIR / "artifact_lock.csv", lock_rows, ["artifact", "role", "path", "exists"])
    write_json(
        LOCK_DIR / "replacement_contract.json",
        {
            "node_root": str(NODE_ROOT),
            "objective": "Confirm whether uncertainty_seed101_rerun_20260622 can replace baseline ModernTCN_small.",
            "anchor_id": ANCHOR_ID,
            "baseline_id": BASELINE_ID,
            "new_training_seeds": NEW_SEEDS,
            "reference_seed": 101,
            "recipe_policy": "derive train commands from anchor config cli_args; only seed/run_tag/output_root change",
            "dataset_file": cfg["cli_args"]["dataset_file"],
            "model_family": cfg["cli_args"]["model_family"],
            "loss_mode": cfg["cli_args"]["loss_mode"],
            "disabled_unreliable_terms": {
                "lambda_transition_focal": cfg["cli_args"]["lambda_transition_focal"],
                "lambda_stall_focal": cfg["cli_args"]["lambda_stall_focal"],
                "lambda_theta_smooth": cfg["cli_args"]["lambda_theta_smooth"],
                "theta_smooth_mode": cfg["cli_args"]["theta_smooth_mode"],
            },
            "decision_rule": {
                "qualified": ">=2/3 seeds offline v2 pass, anchor closed-loop pass, at least one non101 closed-loop pass, and median tested closed-loop J_control < 1.0",
                "not_qualified": "otherwise anchor remains best variant but not a full baseline replacement",
            },
        },
    )
    write_text(
        LOCK_DIR / "evidence_lock_report.md",
        "\n".join(
            [
                "# Evidence Lock",
                "",
                f"- anchor: `{ANCHOR_ID}`",
                f"- baseline: `{BASELINE_ID}`",
                "- seed21/42 will be retrained with the same anchor recipe.",
                "- E2/E5 degraded evidence remains out of scope.",
            ]
        )
        + "\n",
    )


def node_train_seeds() -> None:
    rows: list[dict[str, Any]] = []
    for seed in NEW_SEEDS:
        run_tag = seed_run_tag(seed)
        run_dir = seed_run_dir(seed)
        checkpoint = checkpoint_for_seed(seed)
        metrics = run_dir / "metrics_test.csv"
        if checkpoint.exists() and metrics.exists():
            rows.append({"seed": seed, "run_tag": run_tag, "status": "skipped_existing", "returncode": 0, "run_dir": str(run_dir)})
            continue
        proc = run_command(train_command(seed), TRAIN_DIR / f"{run_tag}.log")
        status = "ok" if proc.returncode == 0 else "failed"
        rows.append({"seed": seed, "run_tag": run_tag, "status": status, "returncode": proc.returncode, "run_dir": str(run_dir)})
    write_csv(TRAIN_DIR / "same_recipe_training_status.csv", rows, ["seed", "run_tag", "status", "returncode", "run_dir"])
    write_text(
        TRAIN_DIR / "same_recipe_training_report.md",
        "\n".join(["# Same Recipe Training", "", "| seed | run | status |", "|---:|---|---|"] + [f"| {r['seed']} | `{r['run_tag']}` | {r['status']} |" for r in rows])
        + "\n",
    )
    failed = [r for r in rows if r["status"] == "failed"]
    if failed:
        raise SystemExit(f"Training failed for: {', '.join(r['run_tag'] for r in failed)}")


def offline_row_for_seed(seed: int) -> dict[str, Any]:
    metric_file = seed_run_dir(seed) / "metrics_test.csv"
    metric = read_csv(metric_file)[0]
    row: dict[str, Any] = {
        "seed": seed,
        "run_tag": seed_run_tag(seed),
        "source": str(metric_file),
        "checkpoint_file": str(checkpoint_for_seed(seed)),
    }
    for metric_name in OFFLINE_METRICS:
        row[metric_name] = metric_alias(metric, metric_name)
    return row


def offline_hard(row: dict[str, Any], baseline: dict[str, Any], thresholds: dict[str, Any]) -> tuple[str, str]:
    checks = [
        ("acc_main_drop", baseline["acc_main"] - num(row["acc_main"]), thresholds["acc_main_min_drop"]),
        ("stall_recall_drop", baseline["stall_recall"] - num(row["stall_recall"]), thresholds["stall_recall_min_drop"]),
        ("slope_recall_drop", baseline["slope_recall"] - num(row["slope_recall"]), thresholds["slope_recall_min_drop"]),
        ("theta_edge_p95_ratio", safe_ratio(num(row["theta_edge_p95_abs_err"]), baseline["theta_edge_p95_abs_err"]), thresholds["theta_edge_p95_max_ratio"]),
        ("flat_peak_theta_error_ratio", safe_ratio(num(row["flat_peak_theta_error"]), baseline["flat_peak_theta_error"]), thresholds["flat_peak_theta_error_max_ratio"]),
    ]
    failures = [f"{name}={value:.6g}>{limit:.6g}" for name, value, limit in checks if math.isfinite(value) and value > float(limit)]
    return ("pass" if not failures else "fail"), "; ".join(failures) if failures else "none"


def offline_score(row: dict[str, Any], baseline: dict[str, Any]) -> float:
    terms: list[float] = []
    for metric in OFFLINE_METRICS:
        value = num(row.get(metric))
        ref = baseline.get(metric, math.nan)
        ratio = safe_ratio(ref, value) if metric in HIGHER_BETTER else safe_ratio(value, ref)
        if math.isfinite(ratio):
            terms.append(ratio)
    return mean(terms) if terms else math.nan


def node_offline() -> None:
    thresholds = json.loads(V2_FULL.read_text(encoding="utf-8"))
    baseline = baseline_offline()
    rows = []
    for seed in SEEDS:
        row = offline_row_for_seed(seed)
        status, failures = offline_hard(row, baseline, thresholds)
        row["offline_v2_status"] = status
        row["offline_v2_failures"] = failures
        row["offline_score_vs_baseline"] = offline_score(row, baseline)
        rows.append(row)
    rows_sorted = sorted(rows, key=lambda r: (r["offline_v2_status"] != "pass", num(r["offline_score_vs_baseline"])))
    for rank, row in enumerate(rows_sorted, 1):
        row["offline_rank"] = rank
    pass_count = sum(1 for r in rows if r["offline_v2_status"] == "pass")
    stability = "robust_pass" if pass_count == 3 else "usable_seed_sensitive" if pass_count == 2 else "reject_seed_fragile"
    write_csv(
        OFFLINE_DIR / "same_recipe_offline_multiseed.csv",
        sorted(rows, key=lambda r: r["seed"]),
        ["seed", "run_tag", "offline_rank", "offline_v2_status", "offline_v2_failures", "offline_score_vs_baseline", *OFFLINE_METRICS, "checkpoint_file", "source"],
    )
    write_json(
        OFFLINE_DIR / "offline_stability_summary.json",
        {
            "pass_count": pass_count,
            "n_seeds": 3,
            "stability_label": stability,
            "median_offline_score_vs_baseline": median([num(r["offline_score_vs_baseline"]) for r in rows if math.isfinite(num(r["offline_score_vs_baseline"]))]),
            "best_non101_seed": min([r for r in rows if r["seed"] in NEW_SEEDS], key=lambda r: num(r["offline_score_vs_baseline"]))["seed"],
        },
    )
    lines = ["# Same Recipe Offline Multiseed", "", f"- pass_count: {pass_count}/3", f"- stability_label: `{stability}`", "", "| seed | status | score | failures |", "|---:|---|---:|---|"]
    for row in sorted(rows, key=lambda r: r["seed"]):
        lines.append(f"| {row['seed']} | {row['offline_v2_status']} | {num(row['offline_score_vs_baseline']):.6f} | {row['offline_v2_failures']} |")
    write_text(OFFLINE_DIR / "offline_multiseed_report.md", "\n".join(lines) + "\n")


def export_one(seed: int) -> dict[str, Any]:
    run_tag = seed_run_tag(seed)
    candidate_id = f"{DEPLOY_ID_PREFIX}{seed}"
    checkpoint = checkpoint_for_seed(seed)
    export_dir = CLOSED_DIR / "00_exported_onnx" / candidate_id
    export_dir.mkdir(parents=True, exist_ok=True)
    onnx_file = export_dir / f"{candidate_id}.onnx"
    sample_file = export_dir / f"{candidate_id}_pytorch_reference.mat"
    if not onnx_file.exists() or not sample_file.exists():
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
        "seed": seed,
        "source_run_tag": run_tag,
        "candidate_id": candidate_id,
        "checkpoint_file": str(checkpoint),
        "onnx_file": str(onnx_file),
        "sample_file": str(sample_file),
        "export_status": export_status,
        "consistency_json": str(consistency_json),
        "consistency_status": consistency_status,
        "consistency_pass": consistency_pass,
        "selected_for_closed_loop": consistency_pass,
    }


def node_export_non101() -> None:
    manifest = [export_one(seed) for seed in NEW_SEEDS]
    write_csv(
        CLOSED_DIR / "replacement_closed_loop_manifest.csv",
        manifest,
        ["seed", "source_run_tag", "candidate_id", "checkpoint_file", "onnx_file", "sample_file", "export_status", "consistency_json", "consistency_status", "consistency_pass", "selected_for_closed_loop"],
    )
    write_json(CLOSED_DIR / "replacement_closed_loop_manifest.json", manifest)
    lines = ["# Replacement Closed-Loop Manifest", "", "| seed | candidate | consistency | selected |", "|---:|---|---|---|"]
    for row in manifest:
        lines.append(f"| {row['seed']} | `{row['candidate_id']}` | {row['consistency_pass']} | {row['selected_for_closed_loop']} |")
    write_text(CLOSED_DIR / "replacement_closed_loop_manifest.md", "\n".join(lines) + "\n")
    failed = [r for r in manifest if not r["consistency_pass"]]
    if failed:
        raise SystemExit(f"ONNX consistency failed for: {', '.join(r['candidate_id'] for r in failed)}")


def aggregate_path_metrics() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    formal = read_csv(FORMAL_PATH_METRICS)
    for row in formal:
        if row["controller"] in {BASELINE_ID, ANCHOR_ID}:
            rows.append({**row, "candidate_id": row["controller"], "source": str(FORMAL_PATH_METRICS)})
    manifest = read_csv(CLOSED_DIR / "replacement_closed_loop_manifest.csv")
    selected = {r["candidate_id"] for r in manifest if str(r.get("selected_for_closed_loop", "")).lower() == "true"}
    for path_dir in (CLOSED_DIR / "01_closed_loop_runs").glob("path_*"):
        summary = path_dir / "uncertainty_replacement_summary.csv"
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
    write_csv(CLOSED_DIR / "closed_loop_replacement_results.csv", sorted(final, key=lambda r: num(r["rank_by_J_control"])), fields)
    lines = ["# Replacement Closed-Loop Results", "", "| rank | candidate | J_control | v2 status | failures |", "|---:|---|---:|---|---|"]
    for row in sorted(final, key=lambda r: num(r["rank_by_J_control"])):
        lines.append(f"| {row['rank_by_J_control']} | `{row['candidate_id']}` | {num(row['J_control']):.6f} | {row['closed_loop_v2_status']} | {row['closed_loop_v2_failures']} |")
    write_text(CLOSED_DIR / "closed_loop_replacement_report.md", "\n".join(lines) + "\n")


def node_decision() -> None:
    node_summarize_closed_loop()
    offline_summary = json.loads((OFFLINE_DIR / "offline_stability_summary.json").read_text(encoding="utf-8"))
    closed_rows = read_csv(CLOSED_DIR / "closed_loop_replacement_results.csv")
    manifest = read_csv(CLOSED_DIR / "replacement_closed_loop_manifest.csv")
    non101_ids = {r["candidate_id"] for r in manifest}
    non101 = [r for r in closed_rows if r["candidate_id"] in non101_ids]
    anchor = next(r for r in closed_rows if r["candidate_id"] == ANCHOR_ID)
    tested_j = [num(anchor["J_control"])] + [num(r["J_control"]) for r in non101 if math.isfinite(num(r["J_control"]))]
    non101_pass = [r for r in non101 if r["closed_loop_v2_status"] == "pass"]
    median_tested_j = median(tested_j) if tested_j else math.nan
    qualified = (
        int(offline_summary["pass_count"]) >= 2
        and anchor["closed_loop_v2_status"] == "pass"
        and len(non101_pass) >= 1
        and math.isfinite(median_tested_j)
        and median_tested_j < 1.0
    )
    decision = "ReplacementQualified" if qualified else "AnchorOnlyNotFullReplacement"
    final_rows = []
    for row in closed_rows:
        if row["candidate_id"] == BASELINE_ID:
            role = "ModernTCN_small_baseline"
        elif row["candidate_id"] == ANCHOR_ID:
            role = "seed101_anchor"
        elif row["candidate_id"] in non101_ids:
            role = "same_recipe_non101_seed"
        else:
            role = "other"
        final_rows.append({**row, "role": role, "replacement_decision": decision})
    write_csv(
        DECISION_DIR / "replacement_candidate_table.csv",
        final_rows,
        ["candidate_id", "role", "replacement_decision", "J_control", "rank_by_J_control", "closed_loop_v2_status", "closed_loop_v2_failures", "n_paths", "ey_rmse_mean", "xy_rmse_mean", "epsi_rmse_mean", "j_du_mean", "omega_cmd_rms_mean", "main_acc_pct_mean", "turn_acc_pct_mean"],
    )
    lines = [
        "# Uncertainty Anchor Replacement Qualification",
        "",
        f"- decision: `{decision}`",
        f"- offline stability: `{offline_summary['stability_label']}` ({offline_summary['pass_count']}/3 pass)",
        f"- median tested closed-loop J_control: {median_tested_j:.6f}",
        f"- anchor: `{ANCHOR_ID}`",
        f"- baseline: `{BASELINE_ID}`",
        "",
        "| rank | candidate | role | J_control | v2 status |",
        "|---:|---|---|---:|---|",
    ]
    for row in sorted(final_rows, key=lambda r: num(r["rank_by_J_control"])):
        lines.append(f"| {row['rank_by_J_control']} | `{row['candidate_id']}` | {row['role']} | {num(row['J_control']):.6f} | {row['closed_loop_v2_status']} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `ReplacementQualified` means the uncertainty-weighted recipe can be used as the selected replacement for the original ModernTCN_small baseline under the current v2 gates.",
            "- `AnchorOnlyNotFullReplacement` means seed101 remains the best anchor, but the recipe is not yet robust enough to replace the baseline generally.",
        ]
    )
    write_text(DECISION_DIR / "replacement_qualification_report.md", "\n".join(lines) + "\n")
    write_text(
        DECISION_DIR / "handoff_next_window.md",
        "\n".join(
            [
                "# Handoff Next Window",
                "",
                f"- decision: `{decision}`",
                "- Use `replacement_qualification_report.md` and `replacement_candidate_table.csv` as the decision source.",
                "- Do not overwrite the original ModernTCN_small baseline unless replacement remains qualified after any later threshold freeze.",
            ]
        )
        + "\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["lock", "train-seeds", "offline", "export-non101", "summarize-closed-loop", "decision", "all-offline"])
    args = parser.parse_args()
    if args.command == "lock":
        node_lock()
    elif args.command == "train-seeds":
        node_train_seeds()
    elif args.command == "offline":
        node_offline()
    elif args.command == "export-non101":
        node_export_non101()
    elif args.command == "summarize-closed-loop":
        node_summarize_closed_loop()
    elif args.command == "decision":
        node_decision()
    elif args.command == "all-offline":
        node_lock()
        node_train_seeds()
        node_offline()
        node_export_non101()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
