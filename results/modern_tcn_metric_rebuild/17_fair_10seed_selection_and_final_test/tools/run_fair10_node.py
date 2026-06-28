from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, median, pstdev
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROJECT_ROOT = ROOT
NODE_ROOT = ROOT / "results" / "modern_tcn_metric_rebuild" / "17_fair_10seed_selection_and_final_test"
TRAIN_SCRIPT = ROOT / "src" / "ModernTCN" / "train_modern_tcn.py"
EXPORT_SCRIPT = ROOT / "src" / "ModernTCN" / "export_modern_tcn_onnx.py"
CHECK_ONNX_SCRIPT = ROOT / "src" / "ModernTCN" / "check_onnxruntime_consistency.py"
ROBUSTNESS_M_SCRIPT = ROOT / "src" / "Compare" / "run_closed_loop_robustness_experiment.m"
RUN_CLOSED_LOOP_M = NODE_ROOT / "run_fair10_closed_loop.m"

SEEDS = [1, 7, 11, 21, 42, 73, 101, 202, 340, 520]
DATASET_FILE = ROOT / "data" / "tcn" / "ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat"
VALIDATION_SENTINEL_PATHS = [
    ROOT / "data" / "paths" / "agv_theta10_uniform_v2" / "agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16.mat",
    ROOT / "data" / "paths" / "agv_theta10_uniform_v2" / "agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06.mat",
]
FINAL_TEST_PATHS = [
    ROOT / "data" / "paths" / "path_factory_logistics_showcase_theta10_v10.mat",
    ROOT / "data" / "paths" / "path_closed_loop_sharp_turn_transition_theta10_v1.mat",
    ROOT / "data" / "paths" / "path_closed_loop_long_updown_theta10_v1.mat",
    ROOT / "data" / "paths" / "modern_tcn_showcase" / "candidates" / "path_modern_tcn_showcase_candidate_soft_updown_straight_turn_v1.mat",
]
BASELINE_MATRIX = ROOT / "results" / "modern_tcn_metric_rebuild" / "03_rerank_existing_experiments" / "candidate_metric_matrix.csv"
BASELINE_MATRIX_LOCK = "baseline_lock"
TRAIN_OUTPUT_ROOTS = {
    "modern_fixed": NODE_ROOT / "01_train_modern_tcn_small_10seed",
    "uncertainty_weighted": NODE_ROOT / "02_train_uncertainty_weighted_10seed",
}
TRAIN_RUN_TAG_PREFIX = {
    "modern_fixed": "modern_fixed_seed",
    "uncertainty_weighted": "uncertainty_weighted_seed",
}
TRAIN_LOSS_MODE = {
    "modern_fixed": "fixed",
    "uncertainty_weighted": "uncertainty_weighting",
}
TRAIN_REGISTRY = {
    "modern_fixed": {
        "label": "ModernTCN_small_fixed_loss",
        "output_root": TRAIN_OUTPUT_ROOTS["modern_fixed"],
        "run_tag_prefix": TRAIN_RUN_TAG_PREFIX["modern_fixed"],
        "loss_mode": TRAIN_LOSS_MODE["modern_fixed"],
        "recipe_source_config": ROOT
        / "results"
        / "modern_tcn_metric_rebuild"
        / "16_recipe_vs_deployment_comparison"
        / "07_modern_base_seed42_training"
        / "modern_base_seed42"
        / "config.json",
        "extra_args": [],
    },
    "uncertainty_weighted": {
        "label": "Uncertainty_weighted_ModernTCN_small",
        "output_root": TRAIN_OUTPUT_ROOTS["uncertainty_weighted"],
        "run_tag_prefix": TRAIN_RUN_TAG_PREFIX["uncertainty_weighted"],
        "loss_mode": TRAIN_LOSS_MODE["uncertainty_weighted"],
        "recipe_source_config": ROOT
        / "results"
        / "modern_tcn_metric_rebuild"
        / "16_recipe_vs_deployment_comparison"
        / "07_modern_base_seed42_training"
        / "modern_base_seed42"
        / "config.json",
        "extra_args": [],
    },
}

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
OFFLINE_HARD_RULES = {
    "acc_main_min_drop": 0.03,
    "stall_recall_min_drop": 0.05,
    "slope_recall_min_drop": 0.02,
    "theta_edge_p95_max_ratio": 1.10,
    "flat_peak_theta_error_max_ratio": 1.15,
}
SENTINEL_RULES = {
    "mean_J_control_max_ratio": 1.50,
    "worst_J_control_max_ratio": 1.20,
    "path_catastrophic_count_max": 0,
}
DISTURBANCE_LEVELS = [0, 1, 2]
DISTURBANCE_SEED = 20260625
DISTURBANCE_MODE = "hybrid"
CONTROL_METRICS = ["ey_rmse", "xy_rmse", "epsi_rmse", "j_du", "omega_cmd_rms"]


def num(value: Any) -> float:
    if value is None:
        return math.nan
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "missing", "unavailable", "pending"}:
        return math.nan
    try:
        return float(text)
    except ValueError:
        return math.nan


def fmt(value: Any) -> str:
    if value is None:
        return ""
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
    return str(value)


def safe_ratio(value: float, baseline: float) -> float:
    if not math.isfinite(value) or not math.isfinite(baseline) or baseline == 0:
        return math.nan
    return value / baseline


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: fmt(row.get(field, "")) for field in fields})


def write_json(path: Path, data: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    ensure_dir(path.parent)
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


def md_table(rows: list[dict[str, Any]], fields: list[str], max_rows: int | None = None) -> str:
    selected = rows if max_rows is None else rows[:max_rows]
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join(["---"] * len(fields)) + " |"]
    for row in selected:
        lines.append("| " + " | ".join(fmt(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def run_command(cmd: list[str], log_file: Path | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    if log_file:
        ensure_dir(log_file.parent)
    proc = subprocess.run(
        cmd,
        cwd=str(cwd or PROJECT_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
    )
    if log_file:
        log_file.write_text(proc.stdout, encoding="utf-8")
    return proc


def find_single_csv_row(path: Path) -> dict[str, str]:
    rows = read_csv(path)
    if not rows:
        raise FileNotFoundError(f"CSV has no rows: {path}")
    return rows[0]


def baseline_metrics() -> dict[str, Any]:
    row = next(r for r in read_csv(BASELINE_MATRIX) if r["candidate_id"] == BASELINE_MATRIX_LOCK)
    return {
        "candidate_id": BASELINE_MATRIX_LOCK,
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


def offline_v2_score(row: dict[str, Any], baseline: dict[str, Any]) -> float:
    ratios: list[float] = []
    for metric in OFFLINE_METRICS:
        value = num(row.get(metric))
        base = num(baseline.get(metric))
        if not math.isfinite(value) or not math.isfinite(base) or base == 0:
            continue
        if metric in HIGHER_BETTER:
            if value > 0:
                ratios.append(base / value)
        else:
            ratios.append(value / base)
    return mean(ratios) if ratios else math.nan


def feature_contract_file(output_dir: Path) -> Path:
    return output_dir / "dataset_contract_copy.json"


def train_output_dir(algorithm_key: str, seed: int) -> Path:
    return TRAIN_OUTPUT_ROOTS[algorithm_key] / f"{TRAIN_RUN_TAG_PREFIX[algorithm_key]}{seed}"


def train_summary_path(algorithm_key: str, seed: int) -> Path:
    return train_output_dir(algorithm_key, seed) / f"modern_tcn_seed{seed}_summary.csv"


def train_history_path(algorithm_key: str, seed: int) -> Path:
    return train_output_dir(algorithm_key, seed) / f"modern_tcn_seed{seed}_history.csv"


def train_checkpoint_path(algorithm_key: str, seed: int) -> Path:
    return train_output_dir(algorithm_key, seed) / f"modern_tcn_seed{seed}.pt"


def train_config_path(algorithm_key: str, seed: int) -> Path:
    return train_output_dir(algorithm_key, seed) / "config.json"


def train_report_path(algorithm_key: str, seed: int) -> Path:
    return train_output_dir(algorithm_key, seed) / "ModernTCN_train_report.md"


def validate_path_file(path: Path, label: str) -> None:
    if path.exists():
        return
    raise FileNotFoundError(f"Missing {label}: {path}")


def manifest_row_for_training(algorithm_key: str, seed: int) -> dict[str, Any]:
    out_dir = train_output_dir(algorithm_key, seed)
    summary = train_summary_path(algorithm_key, seed)
    history = train_history_path(algorithm_key, seed)
    checkpoint = train_checkpoint_path(algorithm_key, seed)
    config = train_config_path(algorithm_key, seed)
    report = train_report_path(algorithm_key, seed)
    return {
        "algorithm_id": algorithm_key,
        "algorithm_label": TRAIN_REGISTRY[algorithm_key]["label"],
        "seed": seed,
        "run_tag": f"{TRAIN_RUN_TAG_PREFIX[algorithm_key]}{seed}",
        "output_dir": str(out_dir),
        "checkpoint_file": str(checkpoint),
        "summary_csv": str(summary),
        "history_csv": str(history),
        "config_json": str(config),
        "report_file": str(report),
        "loss_mode": TRAIN_REGISTRY[algorithm_key]["loss_mode"],
    }


def build_train_command(algorithm_key: str, seed: int) -> list[str]:
    spec = TRAIN_REGISTRY[algorithm_key]
    source_config = Path(spec["recipe_source_config"])
    if not source_config.exists():
        raise FileNotFoundError(f"Missing recipe source config: {source_config}")
    config = json.loads(source_config.read_text(encoding="utf-8"))
    cli_args = dict(config.get("cli_args", {}))
    cli_args["seed"] = seed
    cli_args["dataset_file"] = str(DATASET_FILE)
    cli_args["output_root"] = str(spec["output_root"])
    cli_args["run_tag"] = f"{spec['run_tag_prefix']}{seed}"
    cli_args["loss_mode"] = spec["loss_mode"]
    cli_args["no_overwrite"] = True
    cmd = [sys.executable, str(TRAIN_SCRIPT)]
    for key in sorted(cli_args):
        value = cli_args[key]
        if value is None:
            continue
        flag = f"--{key.replace('_', '-')}"
        if isinstance(value, bool):
            if value:
                cmd.append(flag)
            continue
        if isinstance(value, list):
            cmd.append(flag)
            cmd.extend(str(v) for v in value)
            continue
        cmd.extend([flag, str(value)])
    return cmd


def write_manual_script(path: Path, title: str, body_lines: list[str]) -> None:
    ensure_dir(path.parent)
    if path.suffix.lower() == ".ps1":
        text = [
            f"# {title}",
            "",
            "$ErrorActionPreference = 'Stop'",
            "$ProgressPreference = 'SilentlyContinue'",
            "",
        ]
    else:
        text = [
            f"% {title}",
            "",
        ]
    text.extend(body_lines)
    write_text(path, "\n".join(text) + "\n")


def file_prefix_for_path_split(path_split: str) -> str:
    return {
        "validation_sentinel": "validation_sentinel",
        "final_test": "final_test",
        "disturbance_validation": "disturbance_validation",
    }[path_split]


def local_assert(condition: bool, msg: str) -> None:
    if not condition:
        raise RuntimeError(msg)


@dataclass
class ClosedLoopCandidate:
    algorithm_id: str
    seed: int
    candidate_id: str
    checkpoint_file: Path
    onnx_file: Path
    sample_file: Path
    summary_csv: Path
    history_csv: Path
    config_json: Path
    report_file: Path
    offline_v2_score: float
    training_success: bool
    loss_mode: str
    screen_exception_used: bool = False
    exception_rank: int | None = None
    offline_gate_status: str = "pending"
    enter_validation_sentinel: bool = False
    failure_reason: str = ""
    validation_sentinel_J_control_mean: float = math.nan
    validation_sentinel_J_control_worst: float = math.nan
    path_catastrophic_count: int = 0
    sentinel_status: str = "pending"
    selected_seed: int | None = None
    selection_metric: float = math.nan
    selected_candidate_id: str = ""
    selection_status: str = "pending"
    selection_reason: str = ""


def preflight() -> dict[str, Any]:
    required = [
        TRAIN_SCRIPT,
        EXPORT_SCRIPT,
        CHECK_ONNX_SCRIPT,
        RUN_CLOSED_LOOP_M,
        ROBUSTNESS_M_SCRIPT,
        BASELINE_MATRIX,
        DATASET_FILE,
        TRAIN_REGISTRY["modern_fixed"]["recipe_source_config"],
        TRAIN_REGISTRY["uncertainty_weighted"]["recipe_source_config"],
    ]
    missing = [str(p) for p in required if not p.exists()]
    sentinel_base = ROOT / "results" / "modern_tcn_metric_rebuild" / "05_sandbox_closed_loop_if_needed" / "03_formal_validation"
    missing_validation_baseline_outputs = []
    validation_rows = []
    for path in VALIDATION_SENTINEL_PATHS:
        baseline_out = sentinel_baseline_out(sentinel_base, path)
        if not baseline_out.exists():
            missing_validation_baseline_outputs.append(str(baseline_out))
        validation_rows.append(
            {
                "path_file": str(path),
                "exists": path.exists(),
                "baseline_out": str(baseline_out),
                "baseline_out_exists": baseline_out.exists(),
            }
        )
    final_rows = []
    for path in FINAL_TEST_PATHS:
        baseline_out = sentinel_baseline_out(sentinel_base, path)
        final_rows.append(
            {
                "path_file": str(path),
                "exists": path.exists(),
                "baseline_out": str(baseline_out),
                "baseline_out_exists": baseline_out.exists(),
            }
        )
    disjoint = set(map(str, VALIDATION_SENTINEL_PATHS)).isdisjoint(set(map(str, FINAL_TEST_PATHS)))
    return {
        "node_root": str(NODE_ROOT),
        "train_script": str(TRAIN_SCRIPT),
        "export_script": str(EXPORT_SCRIPT),
        "check_onnx_script": str(CHECK_ONNX_SCRIPT),
        "run_closed_loop_m": str(RUN_CLOSED_LOOP_M),
        "robustness_m": str(ROBUSTNESS_M_SCRIPT),
        "missing_required": missing,
        "missing_validation_baseline_outputs": sorted(set(missing_validation_baseline_outputs)),
        "can_start": not missing and disjoint and not missing_validation_baseline_outputs,
        "validation_paths_disjoint": disjoint,
        "validation_rows": validation_rows,
        "final_rows": final_rows,
        "seeds": SEEDS,
        "dataset_file": str(DATASET_FILE),
        "baseline_matrix": str(BASELINE_MATRIX),
    }


def sentinel_baseline_out(base: Path, path_file: Path) -> Path:
    path_tag = path_file.stem
    candidate = base / path_tag / "baseline_lock_out.mat"
    if candidate.exists():
        return candidate
    fallback = base / path_tag / "window2_formal_out.mat"
    return fallback


def write_protocol_lock(pre: dict[str, Any]) -> None:
    protocol_dir = NODE_ROOT / "00_protocol_lock"
    ensure_dir(protocol_dir)
    write_json(protocol_dir / "protocol_lock.json", pre)
    write_json(protocol_dir / "seed_list.json", {"seeds": SEEDS})
    write_csv(
        protocol_dir / "algorithm_registry.csv",
        [
            {
                "algorithm_id": k,
                "algorithm_label": v["label"],
                "loss_mode": v["loss_mode"],
                "output_root": str(v["output_root"]),
                "run_tag_prefix": v["run_tag_prefix"],
            }
            for k, v in TRAIN_REGISTRY.items()
        ],
        ["algorithm_id", "algorithm_label", "loss_mode", "output_root", "run_tag_prefix"],
    )
    write_text(
        protocol_dir / "path_split_protocol.md",
        "# Path Split Protocol\n\n"
        f"- validation sentinel paths: {', '.join(f'`{p}`' for p in map(str, VALIDATION_SENTINEL_PATHS))}\n"
        f"- final test paths: {', '.join(f'`{p}`' for p in map(str, FINAL_TEST_PATHS))}\n"
        f"- disjoint: `{pre['validation_paths_disjoint']}`\n",
    )
    write_text(
        protocol_dir / "metric_protocol.md",
        "# Metric Protocol\n\n"
        "- offline_v2_score: lower is better, computed as mean of baseline/value or value/baseline ratios\n"
        "- hard screen uses baseline-relative thresholds and never relaxes them\n"
        "- validation sentinel and final test are separated; final-test results never affect selection\n",
    )


def write_manual_scripts() -> None:
    protocol_dir = NODE_ROOT / "00_protocol_lock"
    fixed_lines = []
    for seed in SEEDS:
        cmd = "& " + " ".join(f'"{x}"' if " " in x or "\\" in x else x for x in build_train_command("modern_fixed", seed))
        fixed_lines.append(f"# seed {seed}")
        fixed_lines.append(cmd)
        fixed_lines.append("")
    uncertainty_lines = []
    for seed in SEEDS:
        cmd = "& " + " ".join(f'"{x}"' if " " in x or "\\" in x else x for x in build_train_command("uncertainty_weighted", seed))
        uncertainty_lines.append(f"# seed {seed}")
        uncertainty_lines.append(cmd)
        uncertainty_lines.append("")
    write_manual_script(protocol_dir / "manual_train_modern_fixed.ps1", "Manual train ModernTCN fixed-loss 10 seeds", fixed_lines)
    write_manual_script(protocol_dir / "manual_train_uncertainty.ps1", "Manual train uncertainty-weighted ModernTCN 10 seeds", uncertainty_lines)
    write_manual_script(
        protocol_dir / "manual_export_sentinel.ps1",
        "Manual export validation sentinel candidates",
        [
            "# Export each selected validation sentinel candidate after offline screening.",
            "# Read 03_offline_screen/offline_screen_decision.csv and keep rows where enter_validation_sentinel=true.",
            "# For each row run:",
            "#   python src\\ModernTCN\\export_modern_tcn_onnx.py --checkpoint <checkpoint_file> --onnx-file <candidate.onnx> --sample-file <candidate_pytorch_reference.mat> --no-overwrite",
            "#   python src\\ModernTCN\\check_onnxruntime_consistency.py --onnx-file <candidate.onnx> --sample-file <candidate_pytorch_reference.mat>",
        ],
    )
    write_manual_script(
        protocol_dir / "manual_run_validation_sentinel.m",
        "Manual MATLAB validation sentinel entrypoint",
        [
            "init_project;",
            "cfg = struct();",
            "cfg.path_split = 'validation_sentinel';",
            "cfg.reuse_existing = true;",
            "run_fair10_closed_loop(cfg);",
        ],
    )
    write_manual_script(
        protocol_dir / "manual_run_final_test.m",
        "Manual MATLAB final test entrypoint",
        [
            "init_project;",
            "cfg = struct();",
            "cfg.path_split = 'final_test';",
            "cfg.reuse_existing = true;",
            "run_fair10_closed_loop(cfg);",
        ],
    )
    write_manual_script(
        protocol_dir / "manual_run_disturbance_validation.m",
        "Manual MATLAB disturbance validation entrypoint",
        [
            "init_project;",
            "cfg = struct();",
            "cfg.path_split = 'disturbance_validation';",
            "cfg.reuse_existing = true;",
            "cfg.disturbance_mode = 'hybrid';",
            f"cfg.disturbance_seed = {DISTURBANCE_SEED};",
            f"cfg.disturbance_levels = [{', '.join(map(str, DISTURBANCE_LEVELS))}];",
            "run_fair10_closed_loop(cfg);",
        ],
    )


def _ensure_protocol_lock_written(pre: dict[str, Any]) -> None:
    protocol_dir = NODE_ROOT / "00_protocol_lock"
    ensure_dir(protocol_dir)
    write_json(protocol_dir / "protocol_lock.json", pre)
    write_json(protocol_dir / "seed_list.json", {"seeds": SEEDS})
    write_csv(
        protocol_dir / "algorithm_registry.csv",
        [
            {
                "algorithm_id": key,
                "algorithm_label": spec["label"],
                "loss_mode": spec["loss_mode"],
                "output_root": str(spec["output_root"]),
                "run_tag_prefix": spec["run_tag_prefix"],
            }
            for key, spec in TRAIN_REGISTRY.items()
        ],
        ["algorithm_id", "algorithm_label", "loss_mode", "output_root", "run_tag_prefix"],
    )
    write_text(
        protocol_dir / "path_split_protocol.md",
        "# Path Split Protocol\n\n"
        f"- validation sentinel: {', '.join(f'`{p}`' for p in map(str, VALIDATION_SENTINEL_PATHS))}\n"
        f"- final test: {', '.join(f'`{p}`' for p in map(str, FINAL_TEST_PATHS))}\n"
        f"- disjoint: `{pre['validation_paths_disjoint']}`\n",
    )
    write_text(
        protocol_dir / "metric_protocol.md",
        "# Metric Protocol\n\n"
        "- offline_v2_score is lower-is-better and is computed from baseline/value style ratios\n"
        "- hard screen thresholds are frozen and never relaxed\n"
        "- validation sentinel and final test are separated, and final-test results do not affect selection\n",
    )


def node_preflight() -> dict[str, Any]:
    pre = preflight()
    ensure_dir(NODE_ROOT)
    ensure_dir(NODE_ROOT / "00_protocol_lock")
    pre["can_start"] = pre["can_start"] and not pre["missing_validation_baseline_outputs"]
    write_json(NODE_ROOT / "00_protocol_lock" / "preflight_decision.json", pre)
    _ensure_protocol_lock_written(pre)
    write_csv(
        NODE_ROOT / "00_protocol_lock" / "preflight_validation_paths.csv",
        pre["validation_rows"],
        ["path_file", "exists", "baseline_out", "baseline_out_exists"],
    )
    write_csv(
        NODE_ROOT / "00_protocol_lock" / "preflight_final_paths.csv",
        pre["final_rows"],
        ["path_file", "exists", "baseline_out", "baseline_out_exists"],
    )
    write_text(
        NODE_ROOT / "00_protocol_lock" / "runner_preflight_report.md",
        "# Runner Preflight\n\n"
        f"- can_start: `{pre['can_start']}`\n"
        f"- validation_paths_disjoint: `{pre['validation_paths_disjoint']}`\n"
        f"- seeds: `{', '.join(map(str, SEEDS))}`\n"
        f"- dataset: `{DATASET_FILE}`\n\n"
        "## Required Paths\n\n"
        + md_table(
            [
                {"label": "train_script", **file_info(TRAIN_SCRIPT)},
                {"label": "export_script", **file_info(EXPORT_SCRIPT)},
                {"label": "check_onnx_script", **file_info(CHECK_ONNX_SCRIPT)},
                {"label": "run_closed_loop_m", **file_info(RUN_CLOSED_LOOP_M)},
                {"label": "robustness_m", **file_info(ROBUSTNESS_M_SCRIPT)},
                {"label": "baseline_matrix", **file_info(BASELINE_MATRIX)},
                {"label": "dataset_file", **file_info(DATASET_FILE)},
            ],
            ["label", "exists", "path", "size_bytes", "sha256"],
        )
        + "\n\n## Validation Paths\n\n"
        + md_table(pre["validation_rows"], ["path_file", "exists", "baseline_out", "baseline_out_exists"])
        + "\n\n## Final Paths\n\n"
        + md_table(pre["final_rows"], ["path_file", "exists", "baseline_out", "baseline_out_exists"])
        + "\n\n## Missing Baseline Outputs\n\n"
        + ("- none" if not pre["missing_validation_baseline_outputs"] else "\n".join(f"- `{x}`" for x in pre["missing_validation_baseline_outputs"]))
        + "\n",
    )
    write_manual_scripts()
    pyc = run_command([sys.executable, "-m", "py_compile", str(sys.argv[0])], cwd=PROJECT_ROOT)
    write_json(
        NODE_ROOT / "00_protocol_lock" / "py_compile_result.json",
        {"returncode": pyc.returncode, "stdout": pyc.stdout, "command": [sys.executable, "-m", "py_compile", str(sys.argv[0])]},
    )
    return pre


def train_one(algorithm_key: str, seed: int, no_overwrite: bool = True, dry_run: bool = False) -> dict[str, Any]:
    spec = TRAIN_REGISTRY[algorithm_key]
    out_dir = train_output_dir(algorithm_key, seed)
    ensure_dir(out_dir.parent)
    cmd = build_train_command(algorithm_key, seed)
    if dry_run:
        cmd.append("--dry-run")
    log_file = out_dir / "train.log"
    proc = run_command(cmd, log_file=log_file)
    summary = train_summary_path(algorithm_key, seed)
    history = train_history_path(algorithm_key, seed)
    checkpoint = train_checkpoint_path(algorithm_key, seed)
    config = train_config_path(algorithm_key, seed)
    report = train_report_path(algorithm_key, seed)
    config_json = {}
    if config.exists():
        try:
            config_json = json.loads(config.read_text(encoding="utf-8"))
        except Exception:
            config_json = {}
    return {
        "algorithm_id": algorithm_key,
        "algorithm_label": spec["label"],
        "seed": seed,
        "run_tag": f"{spec['run_tag_prefix']}{seed}",
        "status": "ok" if proc.returncode == 0 else "failed",
        "returncode": proc.returncode,
        "output_dir": str(out_dir),
        "log_file": str(log_file),
        "checkpoint_file": str(checkpoint),
        "summary_csv": str(summary),
        "history_csv": str(history),
        "config_json": str(config),
        "report_file": str(report),
        "dry_run": dry_run,
        "loss_mode": spec["loss_mode"],
        "config": config_json,
    }


def summarize_training(algorithm_key: str) -> dict[str, Any]:
    rows = []
    for seed in SEEDS:
        summary = train_summary_path(algorithm_key, seed)
        config = train_config_path(algorithm_key, seed)
        checkpoint = train_checkpoint_path(algorithm_key, seed)
        history = train_history_path(algorithm_key, seed)
        out_row = {
            "algorithm_id": algorithm_key,
            "algorithm_label": TRAIN_REGISTRY[algorithm_key]["label"],
            "seed": seed,
            "training_success": summary.exists() and checkpoint.exists(),
            "summary_csv": str(summary),
            "history_csv": str(history),
            "checkpoint_file": str(checkpoint),
            "config_json": str(config),
            "report_file": str(train_report_path(algorithm_key, seed)),
        }
        if summary.exists():
            try:
                row = find_single_csv_row(summary)
                out_row.update(
                    {
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
                )
                out_row["offline_v2_score"] = offline_v2_score(out_row, baseline_metrics())
                out_row["failure_reason"] = ""
            except Exception as exc:
                out_row["offline_v2_score"] = math.nan
                out_row["failure_reason"] = str(exc)
        rows.append(out_row)
    path = NODE_ROOT / ("01_train_modern_tcn_small_10seed" if algorithm_key == "modern_fixed" else "02_train_uncertainty_weighted_10seed") / "training_summary.csv"
    write_csv(
        path,
        rows,
        [
            "algorithm_id",
            "algorithm_label",
            "seed",
            "training_success",
            "summary_csv",
            "history_csv",
            "checkpoint_file",
            "config_json",
            "report_file",
            "acc_main",
            "acc_turn",
            "acc_turn_transition",
            "theta_mae_deg",
            "theta_edge_p95_abs_err",
            "flat_peak_theta_error",
            "flat_recall",
            "stall_recall",
            "slope_recall",
            "offline_v2_score",
            "failure_reason",
        ],
    )
    return {"training_summary": str(path), "rows": rows}


def offline_screen() -> dict[str, Any]:
    baseline = baseline_metrics()
    out_rows = []
    for algorithm_key in TRAIN_REGISTRY:
        training_summary = NODE_ROOT / ("01_train_modern_tcn_small_10seed" if algorithm_key == "modern_fixed" else "02_train_uncertainty_weighted_10seed") / "training_summary.csv"
        rows = read_csv(training_summary)
        if not rows:
            continue
        alg_rows = [r for r in rows if r.get("algorithm_id") == algorithm_key]
        hard_pass_count = 0
        finite_rows = []
        for row in alg_rows:
            seed = int(num(row.get("seed")))
            training_success = str(row.get("training_success", "")).lower() in {"true", "1", "yes"}
            off_score = num(row.get("offline_v2_score"))
            gate_reasons = []
            acc_main = num(row.get("acc_main"))
            stall_recall = num(row.get("stall_recall"))
            slope_recall = num(row.get("slope_recall"))
            theta_edge = num(row.get("theta_edge_p95_abs_err"))
            flat_peak = num(row.get("flat_peak_theta_error"))
            if not training_success:
                gate_reasons.append("training_success=false")
            if math.isfinite(acc_main) and acc_main < baseline["acc_main"] - OFFLINE_HARD_RULES["acc_main_min_drop"]:
                gate_reasons.append("acc_main")
            if math.isfinite(stall_recall) and stall_recall < baseline["stall_recall"] - OFFLINE_HARD_RULES["stall_recall_min_drop"]:
                gate_reasons.append("stall_recall")
            if math.isfinite(slope_recall) and slope_recall < baseline["slope_recall"] - OFFLINE_HARD_RULES["slope_recall_min_drop"]:
                gate_reasons.append("slope_recall")
            if math.isfinite(theta_edge) and theta_edge > baseline["theta_edge_p95_abs_err"] * OFFLINE_HARD_RULES["theta_edge_p95_max_ratio"]:
                gate_reasons.append("theta_edge_p95_abs_err")
            if math.isfinite(flat_peak) and flat_peak > baseline["flat_peak_theta_error"] * OFFLINE_HARD_RULES["flat_peak_theta_error_max_ratio"]:
                gate_reasons.append("flat_peak_theta_error")
            gate_pass = training_success and not gate_reasons
            if gate_pass:
                hard_pass_count += 1
            if math.isfinite(off_score):
                finite_rows.append({"seed": seed, "offline_v2_score": off_score, "row": row, "gate_pass": gate_pass, "gate_reasons": gate_reasons})
        if hard_pass_count > 0:
            for item in finite_rows:
                row = item["row"]
                gate_pass = item["gate_pass"]
                row_out = {
                    "algorithm_id": algorithm_key,
                    "seed": int(num(row.get("seed"))),
                    "candidate_id": f"{TRAIN_RUN_TAG_PREFIX[algorithm_key]}{int(num(row.get('seed')))}",
                    "training_success": str(row.get("training_success", "")).lower() in {"true", "1", "yes"},
                    "offline_v2_score": num(row.get("offline_v2_score")),
                    "offline_gate_status": "pass" if gate_pass else "fail",
                    "enter_validation_sentinel": gate_pass,
                    "screen_exception_used": False,
                    "exception_rank": "",
                    "failure_reason": ";".join(item["gate_reasons"]) if item["gate_reasons"] else "",
                    "checkpoint_file": row.get("checkpoint_file", ""),
                    "summary_csv": row.get("summary_csv", ""),
                    "history_csv": row.get("history_csv", ""),
                    "config_json": row.get("config_json", ""),
                    "report_file": row.get("report_file", ""),
                }
                out_rows.append(row_out)
        else:
            finite_sorted = sorted(finite_rows, key=lambda x: x["offline_v2_score"])
            exception_rows = finite_sorted[:3]
            if not exception_rows:
                raise RuntimeError(f"{algorithm_key}: no finite offline_v2_score candidates; no_exception_possible")
            for rank, item in enumerate(exception_rows, start=1):
                row = item["row"]
                row_out = {
                    "algorithm_id": algorithm_key,
                    "seed": int(num(row.get("seed"))),
                    "candidate_id": f"{TRAIN_RUN_TAG_PREFIX[algorithm_key]}{int(num(row.get('seed')))}",
                    "training_success": str(row.get("training_success", "")).lower() in {"true", "1", "yes"},
                    "offline_v2_score": num(row.get("offline_v2_score")),
                    "offline_gate_status": "fail",
                    "enter_validation_sentinel": True,
                    "screen_exception_used": True,
                    "exception_rank": rank,
                    "failure_reason": "exception_candidate_from_offline_v2_score",
                    "checkpoint_file": row.get("checkpoint_file", ""),
                    "summary_csv": row.get("summary_csv", ""),
                    "history_csv": row.get("history_csv", ""),
                    "config_json": row.get("config_json", ""),
                    "report_file": row.get("report_file", ""),
                }
                out_rows.append(row_out)
    out_root = NODE_ROOT / "03_offline_screen"
    write_csv(
        out_root / "offline_screen_decision.csv",
        out_rows,
        [
            "algorithm_id",
            "seed",
            "candidate_id",
            "training_success",
            "offline_v2_score",
            "offline_gate_status",
            "enter_validation_sentinel",
            "screen_exception_used",
            "exception_rank",
            "failure_reason",
            "checkpoint_file",
            "summary_csv",
            "history_csv",
            "config_json",
            "report_file",
        ],
    )
    write_csv(
        out_root / "exception_sentinel_candidates.csv",
        [r for r in out_rows if str(r["screen_exception_used"]).lower() in {"true", "1", "yes"}],
        [
            "algorithm_id",
            "seed",
            "candidate_id",
            "offline_v2_score",
            "exception_rank",
            "checkpoint_file",
            "summary_csv",
            "history_csv",
            "config_json",
            "report_file",
        ],
    )
    write_json(
        out_root / "offline_screen_decision.json",
        {"baseline": baseline, "rows": out_rows, "algorithm_ids": list(TRAIN_REGISTRY.keys())},
    )
    return {"offline_screen_decision": str(out_root / "offline_screen_decision.csv"), "rows": out_rows}


def sentinel_manifest_rows() -> list[dict[str, Any]]:
    rows = read_csv(NODE_ROOT / "03_offline_screen" / "offline_screen_decision.csv")
    out = []
    for row in rows:
        if str(row.get("enter_validation_sentinel", "")).lower() not in {"true", "1", "yes"}:
            continue
        candidate_id = str(row.get("candidate_id"))
        seed = int(num(row.get("seed")))
        algorithm_id = str(row.get("algorithm_id"))
        checkpoint = Path(row.get("checkpoint_file", ""))
        if not checkpoint.exists():
            checkpoint = train_checkpoint_path(algorithm_id, seed)
        sample_file = checkpoint.with_name(f"{checkpoint.stem}_pytorch_reference.mat")
        onnx_file = checkpoint.with_suffix(".onnx")
        out.append(
            {
                "algorithm_id": algorithm_id,
                "seed": seed,
                "candidate_id": candidate_id,
                "screen_exception_used": str(row.get("screen_exception_used", "")).lower() in {"true", "1", "yes"},
                "enter_validation_sentinel": True,
                "offline_v2_score": num(row.get("offline_v2_score")),
                "checkpoint_file": str(checkpoint),
                "onnx_file": str(onnx_file),
                "sample_file": str(sample_file),
                "summary_csv": row.get("summary_csv", ""),
                "history_csv": row.get("history_csv", ""),
                "config_json": row.get("config_json", ""),
                "report_file": row.get("report_file", ""),
            }
        )
    return out


def export_validation_candidates() -> dict[str, Any]:
    rows = sentinel_manifest_rows()
    out_root = NODE_ROOT / "04_validation_sentinel_closed_loop"
    ensure_dir(out_root)
    ensure_dir(out_root / "exports")
    export_rows = []
    for row in rows:
        checkpoint = Path(row["checkpoint_file"])
        onnx_file = Path(row["onnx_file"])
        sample_file = Path(row["sample_file"])
        if not checkpoint.exists():
            raise FileNotFoundError(f"Missing checkpoint for export: {checkpoint}")
        if onnx_file.exists() and sample_file.exists():
            export_rows.append(
                {
                    **row,
                    "export_status": "reused",
                    "onnx_file_exists": True,
                    "sample_file_exists": True,
                }
            )
            continue
        cmd = [
            sys.executable,
            str(EXPORT_SCRIPT),
            "--checkpoint",
            str(checkpoint),
            "--onnx-file",
            str(onnx_file),
            "--sample-file",
            str(sample_file),
            "--no-overwrite",
        ]
        log_file = out_root / "exports" / f"{row['candidate_id']}_export.log"
        proc = run_command(cmd, log_file=log_file)
        if proc.returncode != 0:
            raise RuntimeError(f"ONNX export failed for {row['candidate_id']}: {log_file}")
        consistency_cmd = [
            sys.executable,
            str(CHECK_ONNX_SCRIPT),
            "--onnx-file",
            str(onnx_file),
            "--sample-file",
            str(sample_file),
        ]
        cons_log = out_root / "exports" / f"{row['candidate_id']}_consistency.log"
        cons_proc = run_command(consistency_cmd, log_file=cons_log)
        if cons_proc.returncode != 0:
            raise RuntimeError(f"ONNXRuntime consistency failed for {row['candidate_id']}: {cons_log}")
        export_rows.append(
            {
                **row,
                "export_status": "ok",
                "onnx_file_exists": onnx_file.exists(),
                "sample_file_exists": sample_file.exists(),
            }
        )
    write_csv(
        out_root / "validation_exports.csv",
        export_rows,
        [
            "algorithm_id",
            "seed",
            "candidate_id",
            "screen_exception_used",
            "enter_validation_sentinel",
            "offline_v2_score",
            "checkpoint_file",
            "onnx_file",
            "sample_file",
            "summary_csv",
            "history_csv",
            "config_json",
            "report_file",
            "export_status",
            "onnx_file_exists",
            "sample_file_exists",
        ],
    )
    return {"validation_exports": str(out_root / "validation_exports.csv"), "rows": export_rows}


def write_selected_manifest(rows: list[dict[str, Any]], status: str, reason: str) -> Path:
    out_root = NODE_ROOT / "05_seed_selection"
    ensure_dir(out_root)
    selected_rows = []
    for row in rows:
        selected_rows.append(
            {
                "algorithm_id": row["algorithm_id"],
                "seed": row["seed"],
                "candidate_id": row["candidate_id"],
                "screen_exception_used": row["screen_exception_used"],
                "offline_v2_score": row["offline_v2_score"],
                "validation_sentinel_J_control_mean": row["validation_sentinel_J_control_mean"],
                "validation_sentinel_J_control_worst": row["validation_sentinel_J_control_worst"],
                "path_catastrophic_count": row["path_catastrophic_count"],
                "selected_seed": row["selected_seed"] if row["selected_seed"] is not None else "",
                "selected_candidate_id": row["selected_candidate_id"],
                "selection_metric": row["selection_metric"],
                "selection_status": row["selection_status"],
                "selection_reason": row["selection_reason"],
                "selected": str(row["selection_status"]).lower() == "pass",
                "checkpoint_file": row["checkpoint_file"],
                "onnx_file": row["onnx_file"],
                "sample_file": row["sample_file"],
                "summary_csv": row["summary_csv"],
                "history_csv": row["history_csv"],
                "config_json": row["config_json"],
                "report_file": row["report_file"],
            }
        )
    write_csv(
        out_root / "selected_seed_decision.csv",
        selected_rows,
        [
            "algorithm_id",
            "seed",
            "candidate_id",
            "screen_exception_used",
            "offline_v2_score",
            "validation_sentinel_J_control_mean",
            "validation_sentinel_J_control_worst",
            "path_catastrophic_count",
            "selected_seed",
            "selected_candidate_id",
            "selection_metric",
            "selection_status",
            "selection_reason",
            "selected",
            "checkpoint_file",
            "onnx_file",
            "sample_file",
            "summary_csv",
            "history_csv",
            "config_json",
            "report_file",
        ],
    )
    write_json(
        out_root / "selected_seed_decision.json",
        {"status": status, "reason": reason, "rows": selected_rows},
    )
    return out_root / "selected_seed_decision.csv"


def run_validation_sentinel_closed_loop() -> dict[str, Any]:
    rows = sentinel_manifest_rows()
    if not rows:
        raise RuntimeError("No candidates selected for validation sentinel")
    manifest = NODE_ROOT / "04_validation_sentinel_closed_loop" / "sentinel_manifest.csv"
    write_csv(
        manifest,
        rows,
        [
            "algorithm_id",
            "seed",
            "candidate_id",
            "screen_exception_used",
            "enter_validation_sentinel",
            "offline_v2_score",
            "checkpoint_file",
            "onnx_file",
            "sample_file",
            "summary_csv",
            "history_csv",
            "config_json",
            "report_file",
        ],
    )
    manifest_path = str(manifest).replace("\\", "/")
    node_root_path = str(NODE_ROOT).replace("\\", "/")
    matlab_cmd = [
        "matlab",
        "-batch",
        (
            "init_project; "
            f"addpath('{node_root_path}'); "
            "cfg = struct(); "
            f"cfg.manifest_file = '{manifest_path}'; "
            "cfg.path_split = 'validation_sentinel'; "
            "cfg.reuse_existing = true; "
            "run_fair10_closed_loop(cfg);"
        ),
    ]
    log_file = NODE_ROOT / "04_validation_sentinel_closed_loop" / "validation_sentinel_matlab.log"
    proc = run_command(matlab_cmd, log_file=log_file, cwd=PROJECT_ROOT)
    if proc.returncode != 0:
        raise RuntimeError(f"validation sentinel MATLAB run failed; see {log_file}")
    return {"manifest": str(manifest), "log_file": str(log_file)}


def summarize_validation_sentinel() -> dict[str, Any]:
    out_root = NODE_ROOT / "04_validation_sentinel_closed_loop"
    path_rows = read_csv(out_root / "validation_sentinel_path_runs.csv")
    candidate_rows = collect_closed_loop_candidate_path_metrics(out_root, path_rows)
    fields = [
        "path_tag",
        "candidate_id",
        "controller",
        "algorithm_id",
        "seed",
        "J_control_path",
        "path_fail",
        "path_catastrophic",
        "ey_rmse",
        "xy_rmse",
        "epsi_rmse",
        "j_du",
        "omega_cmd_rms",
        "summary_file",
    ]
    write_csv(out_root / "sentinel_candidate_path_metrics.csv", candidate_rows, fields)
    write_csv(out_root / "sentinel_path_metrics.csv", path_rows, list(path_rows[0].keys()) if path_rows else [])
    return {"rows": path_rows, "candidate_path_metrics": candidate_rows}


def path_j_control(row: dict[str, Any], baseline: dict[str, Any]) -> float:
    ratios = []
    for metric in CONTROL_METRICS:
        ratio = safe_ratio(num(row.get(metric)), num(baseline.get(metric)))
        if math.isfinite(ratio):
            ratios.append(ratio)
    return mean(ratios) if ratios else math.nan


def collect_closed_loop_candidate_path_metrics(out_root: Path, path_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    manifest_by_candidate = {str(row["candidate_id"]): row for row in sentinel_manifest_rows()}
    candidate_rows: list[dict[str, Any]] = []
    for path_row in path_rows:
        if str(path_row.get("status", "")).lower() != "ok":
            continue
        summary_file = Path(path_row.get("summary_file", ""))
        if not summary_file.exists():
            alt = out_root / str(path_row.get("path_tag", "")) / "validation_sentinel_summary.csv"
            summary_file = alt if alt.exists() else summary_file
        summary_rows = [r for r in read_csv(summary_file) if str(r.get("zone", "")).lower() == "all"]
        if not summary_rows:
            continue
        baseline = next((r for r in summary_rows if str(r.get("controller", "")) in {"ModernTCN", "baseline_lock"}), None)
        if baseline is None:
            continue
        for row in summary_rows:
            controller = str(row.get("controller", ""))
            if controller not in manifest_by_candidate:
                continue
            manifest = manifest_by_candidate[controller]
            j_path = path_j_control(row, baseline)
            candidate_rows.append(
                {
                    "path_tag": path_row.get("path_tag", ""),
                    "candidate_id": controller,
                    "controller": controller,
                    "algorithm_id": manifest["algorithm_id"],
                    "seed": int(manifest["seed"]),
                    "J_control_path": j_path,
                    "path_fail": math.isfinite(j_path) and j_path > 1.0,
                    "path_catastrophic": math.isfinite(j_path) and j_path > SENTINEL_RULES["mean_J_control_max_ratio"],
                    "ey_rmse": num(row.get("ey_rmse")),
                    "xy_rmse": num(row.get("xy_rmse")),
                    "epsi_rmse": num(row.get("epsi_rmse")),
                    "j_du": num(row.get("j_du")),
                    "omega_cmd_rms": num(row.get("omega_cmd_rms")),
                    "summary_file": str(summary_file),
                }
            )
    return candidate_rows


def select_seed() -> dict[str, Any]:
    validation_summary = summarize_validation_sentinel()
    rows = validation_summary["candidate_path_metrics"]
    if not rows:
        raise RuntimeError("No validation sentinel path rows found")
    grouped: dict[tuple[str, int], list[dict[str, str]]] = {}
    for row in rows:
        algorithm_id = str(row.get("algorithm_id", row.get("candidate_id", "")))
        seed = int(num(row.get("seed")))
        grouped.setdefault((algorithm_id, seed), []).append(row)
    manifest_rows = { (r["algorithm_id"], int(r["seed"])): r for r in sentinel_manifest_rows() }
    selected_rows = []
    for (algorithm_id, seed), items in grouped.items():
        values = [num(r.get("J_control_path")) for r in items if math.isfinite(num(r.get("J_control_path")))]
        mean_j = mean(values) if values else math.nan
        worst_j = max(values, default=math.nan)
        path_cat = sum(1 for r in items if str(r.get("path_catastrophic", "")).lower() in {"true", "1", "yes"})
        base = manifest_rows.get((algorithm_id, seed))
        if base is None:
            continue
        selection_metric = mean_j
        selected_rows.append(
            {
                "algorithm_id": algorithm_id,
                "seed": seed,
                "candidate_id": base["candidate_id"],
                "screen_exception_used": base["screen_exception_used"],
                "offline_v2_score": base["offline_v2_score"],
                "validation_sentinel_J_control_mean": mean_j,
                "validation_sentinel_J_control_worst": worst_j,
                "path_catastrophic_count": path_cat,
                "selection_metric": selection_metric,
                "selected_seed": seed,
                "selected_candidate_id": base["candidate_id"],
                "selection_status": "pass" if path_cat == 0 and math.isfinite(mean_j) and mean_j <= SENTINEL_RULES["mean_J_control_max_ratio"] else "fail",
                "selection_reason": "lowest_validation_sentinel_J_control_mean" if path_cat == 0 else "validation_sentinel_failed",
                "checkpoint_file": base["checkpoint_file"],
                "onnx_file": base["onnx_file"],
                "sample_file": base["sample_file"],
                "summary_csv": base["summary_csv"],
                "history_csv": base["history_csv"],
                "config_json": base["config_json"],
                "report_file": base["report_file"],
            }
        )
    final_rows = []
    for algorithm_id in TRAIN_REGISTRY:
        candidates = [r for r in selected_rows if r["algorithm_id"] == algorithm_id and r["selection_status"] == "pass"]
        if not candidates:
            final_rows.append(
                {
                    "algorithm_id": algorithm_id,
                    "selected_seed": "",
                    "selected_candidate_id": "",
                    "screen_exception_used": False,
                    "selection_metric": math.nan,
                    "offline_v2_score": math.nan,
                    "validation_sentinel_J_control_mean": math.nan,
                    "path_catastrophic_count": math.nan,
                    "selection_status": "no_selected_seed",
                    "selection_reason": "no_validation_sentinel_pass",
                    "checkpoint_file": "",
                    "onnx_file": "",
                    "sample_file": "",
                    "summary_csv": "",
                    "history_csv": "",
                    "config_json": "",
                    "report_file": "",
                }
            )
            continue
        candidates = sorted(
            candidates,
            key=lambda r: (num(r["selection_metric"]), num(r["offline_v2_score"]), int(num(r["selected_seed"]))),
        )
        best = candidates[0]
        final_rows.append(best)
    selected_csv = write_selected_manifest(final_rows, "ok", "validation_sentinel_selection_complete")
    write_csv(
        NODE_ROOT / "05_seed_selection" / "selected_seed_decision.csv",
        final_rows,
        [
            "algorithm_id",
            "selected_seed",
            "selected_candidate_id",
            "screen_exception_used",
            "selection_metric",
            "offline_v2_score",
            "validation_sentinel_J_control_mean",
            "path_catastrophic_count",
            "selection_status",
            "selection_reason",
            "checkpoint_file",
            "onnx_file",
            "sample_file",
            "summary_csv",
            "history_csv",
            "config_json",
            "report_file",
        ],
    )
    return {"selected_csv": str(selected_csv), "selected_rows": final_rows}


def run_closed_loop(path_split: str) -> dict[str, Any]:
    selected_csv = NODE_ROOT / "05_seed_selection" / "selected_seed_decision.csv"
    local_assert(selected_csv.exists(), f"missing selected seed decision: {selected_csv}")
    rows = read_csv(selected_csv)
    valid_rows = [r for r in rows if str(r.get("selection_status", "")).lower() == "pass"]
    if not valid_rows:
        raise RuntimeError("selected_seed_decision.csv has no pass rows")
    node_root_path = str(NODE_ROOT).replace("\\", "/")
    matlab_cmd = [
        "matlab",
        "-batch",
        (
            "init_project; "
            f"addpath('{node_root_path}'); "
            "cfg = struct(); "
            f"cfg.path_split = '{path_split}'; "
            "cfg.reuse_existing = true; "
            "run_fair10_closed_loop(cfg);"
        ),
    ]
    out_root = NODE_ROOT / ("06_final_test_closed_loop" if path_split == "final_test" else "07_disturbance_validation")
    log_file = out_root / f"{path_split}_matlab.log"
    proc = run_command(matlab_cmd, log_file=log_file, cwd=PROJECT_ROOT)
    if proc.returncode != 0:
        raise RuntimeError(f"{path_split} MATLAB run failed; see {log_file}")
    return {"log_file": str(log_file), "selected_csv": str(selected_csv)}


def summarize_final_outputs() -> dict[str, Any]:
    final_root = NODE_ROOT / "09_final_report"
    ensure_dir(final_root)
    offline_rows = read_csv(NODE_ROOT / "03_offline_screen" / "offline_screen_decision.csv")
    selected_rows = read_csv(NODE_ROOT / "05_seed_selection" / "selected_seed_decision.csv")
    summary_rows = []
    for algorithm_id in TRAIN_REGISTRY:
        off_rows = [r for r in offline_rows if r.get("algorithm_id") == algorithm_id]
        sel_row = next((r for r in selected_rows if r.get("algorithm_id") == algorithm_id), {})
        summary_rows.append(
            {
                "algorithm_id": algorithm_id,
                "training_count": len([r for r in off_rows if str(r.get("training_success", "")).lower() in {"true", "1", "yes"}]),
                "hard_screen_pass_count": len([r for r in off_rows if str(r.get("offline_gate_status", "")).lower() == "pass"]),
                "exception_candidate_count": len([r for r in off_rows if str(r.get("screen_exception_used", "")).lower() in {"true", "1", "yes"}]),
                "selected_seed": sel_row.get("selected_seed", ""),
                "selected_candidate_id": sel_row.get("selected_candidate_id", ""),
                "selected_exception_used": sel_row.get("screen_exception_used", ""),
                "selection_status": sel_row.get("selection_status", ""),
                "selection_reason": sel_row.get("selection_reason", ""),
            }
        )
    write_csv(
        final_root / "final_summary_table.csv",
        summary_rows,
        [
            "algorithm_id",
            "training_count",
            "hard_screen_pass_count",
            "exception_candidate_count",
            "selected_seed",
            "selected_candidate_id",
            "selected_exception_used",
            "selection_status",
            "selection_reason",
        ],
    )
    final_decision = {
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "selected_rows": selected_rows,
        "summary_rows": summary_rows,
        "final_test_paths": [str(p) for p in FINAL_TEST_PATHS],
        "validation_sentinel_paths": [str(p) for p in VALIDATION_SENTINEL_PATHS],
        "screen_exception_used_any": any(str(r.get("screen_exception_used", "")).lower() in {"true", "1", "yes"} for r in selected_rows),
    }
    write_json(final_root / "final_decision.json", final_decision)
    write_text(
        final_root / "fair_10seed_selection_final_report.md",
        "# Fair 10-Seed Selection Final Report\n\n"
        + md_table(summary_rows, ["algorithm_id", "training_count", "hard_screen_pass_count", "exception_candidate_count", "selected_seed", "selected_candidate_id", "selected_exception_used", "selection_status"])
        + "\n",
    )
    return {"final_decision": str(final_root / "final_decision.json"), "final_summary": str(final_root / "final_summary_table.csv")}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--node",
        required=True,
        choices=[
            "preflight",
            "train_modern_fixed",
            "train_uncertainty",
            "summarize_train_modern",
            "summarize_train_uncertainty",
            "offline_screen",
            "export_validation",
            "validation_sentinel",
            "select_seed",
            "final_test",
            "disturbance_validation",
            "final_report",
        ],
    )
    parser.add_argument("--no-overwrite", action="store_true")
    args = parser.parse_args()

    ensure_dir(NODE_ROOT)
    if args.node == "preflight":
        pre = node_preflight()
        write_json(NODE_ROOT / "00_protocol_lock" / "node_status.json", {"node": args.node, "status": "ok", "preflight": pre})
        return 0
    if args.node == "train_modern_fixed":
        node_preflight()
        rows = []
        for seed in SEEDS:
            rows.append(train_one("modern_fixed", seed))
        write_csv(
            NODE_ROOT / "01_train_modern_tcn_small_10seed" / "training_status.csv",
            rows,
            [
                "algorithm_id",
                "algorithm_label",
                "seed",
                "run_tag",
                "status",
                "returncode",
                "output_dir",
                "log_file",
                "checkpoint_file",
                "summary_csv",
                "history_csv",
                "config_json",
                "report_file",
                "dry_run",
                "loss_mode",
            ],
        )
        write_json(NODE_ROOT / "01_train_modern_tcn_small_10seed" / "node_status.json", {"node": args.node, "rows": rows})
        return 0
    if args.node == "train_uncertainty":
        node_preflight()
        rows = []
        for seed in SEEDS:
            rows.append(train_one("uncertainty_weighted", seed))
        write_csv(
            NODE_ROOT / "02_train_uncertainty_weighted_10seed" / "training_status.csv",
            rows,
            [
                "algorithm_id",
                "algorithm_label",
                "seed",
                "run_tag",
                "status",
                "returncode",
                "output_dir",
                "log_file",
                "checkpoint_file",
                "summary_csv",
                "history_csv",
                "config_json",
                "report_file",
                "dry_run",
                "loss_mode",
            ],
        )
        write_json(NODE_ROOT / "02_train_uncertainty_weighted_10seed" / "node_status.json", {"node": args.node, "rows": rows})
        return 0
    if args.node == "summarize_train_modern":
        node_preflight()
        result = summarize_training("modern_fixed")
        write_json(NODE_ROOT / "01_train_modern_tcn_small_10seed" / "node_status.json", {"node": args.node, **result})
        return 0
    if args.node == "summarize_train_uncertainty":
        node_preflight()
        result = summarize_training("uncertainty_weighted")
        write_json(NODE_ROOT / "02_train_uncertainty_weighted_10seed" / "node_status.json", {"node": args.node, **result})
        return 0
    if args.node == "offline_screen":
        node_preflight()
        result = offline_screen()
        write_json(NODE_ROOT / "03_offline_screen" / "node_status.json", {"node": args.node, **result})
        return 0
    if args.node == "export_validation":
        node_preflight()
        result = export_validation_candidates()
        write_json(NODE_ROOT / "04_validation_sentinel_closed_loop" / "node_status.json", {"node": args.node, **result})
        return 0
    if args.node == "validation_sentinel":
        node_preflight()
        result = run_validation_sentinel_closed_loop()
        write_json(NODE_ROOT / "04_validation_sentinel_closed_loop" / "node_status.json", {"node": args.node, **result})
        return 0
    if args.node == "select_seed":
        node_preflight()
        result = select_seed()
        write_json(NODE_ROOT / "05_seed_selection" / "node_status.json", {"node": args.node, **result})
        return 0
    if args.node in {"final_test", "disturbance_validation"}:
        node_preflight()
        result = run_closed_loop(args.node)
        write_json((NODE_ROOT / ("06_final_test_closed_loop" if args.node == "final_test" else "07_disturbance_validation")) / "node_status.json", {"node": args.node, **result})
        return 0
    if args.node == "final_report":
        node_preflight()
        result = summarize_final_outputs()
        write_json(NODE_ROOT / "09_final_report" / "node_status.json", {"node": args.node, **result})
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
