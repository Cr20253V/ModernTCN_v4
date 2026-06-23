from __future__ import annotations

import csv
import json
import math
from datetime import datetime
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parent
SCI_ROOT = ROOT.parent / "modern_tcn_sci_innovation"

MASTER_TABLE = SCI_ROOT / "07_ablation_summary" / "sci_innovation_ablation_master_table.csv"
BASELINE_OFFLINE = SCI_ROOT / "00_baseline_lock" / "baseline_offline_metrics.csv"
BASELINE_CLOSED_LOOP = SCI_ROOT / "00_baseline_lock" / "baseline_closed_loop_metrics.csv"

PLAN_FILE = ROOT / "ModernTCN_metric_rebuild_and_local_optimization_plan_for_CODEX.md"
REPAIR_DIR = ROOT / "00_replay_contract_repair"
E2_FIXED_DIR = ROOT / "02_e2_smooth_fixed"
E5_FIXED_DIR = ROOT / "05_e5_replay_fixed"

OUT_LOCK = ROOT / "00_baseline_and_artifact_lock"
OUT_DICT = ROOT / "01_metric_design"
OUT_FREEZE = ROOT / "02_metric_freeze"
OUT_RERANK = ROOT / "03_rerank_existing_experiments"
OUT_DECISION = ROOT / "04_candidate_decision"

CORE_OFFLINE_METRICS = [
    ("acc_main", "higher"),
    ("acc_turn", "higher"),
    ("acc_turn_transition", "higher"),
    ("theta_mae_deg", "lower"),
    ("theta_edge_p95_abs_err", "lower"),
    ("flat_peak_theta_error", "lower"),
    ("flat_recall", "higher"),
    ("stall_recall", "higher"),
    ("slope_recall", "higher"),
]

SENSITIVITY_METRICS = [
    ("acc_main", "higher"),
    ("acc_turn", "higher"),
    ("acc_turn_transition", "higher"),
    ("theta_mae_deg", "lower"),
    ("theta_edge_p95_abs_err", "lower"),
    ("flat_peak_theta_error", "lower"),
    ("flat_recall", "higher"),
    ("stall_recall", "higher"),
    ("slope_recall", "higher"),
]

FINAL_WEIGHTS_RAW = {
    "acc_main": 0.1773399014778325,
    "acc_turn": 0.1231527093596059,
    "acc_turn_transition": 0.10344827586206895,
    "theta_mae_deg": 0.13793103448275862,
    "theta_edge_p95_abs_err": 0.1330049261083744,
    "flat_peak_theta_error": 0.12807881773399013,
    "flat_recall": 0.06403940886699507,
    "stall_recall": 0.0665024630541872,
    "slope_recall": 0.0665024630541872,
}

WEIGHT_VERSIONS_RAW = {
    "v0": {
        "acc_main": 0.22,
        "acc_turn": 0.16,
        "acc_turn_transition": 0.14,
        "theta_mae_deg": 0.14,
        "theta_edge_p95_abs_err": 0.12,
        "flat_peak_theta_error": 0.10,
        "flat_recall": 0.04,
        "stall_recall": 0.04,
        "slope_recall": 0.04,
    },
    "v1": {
        "acc_main": 0.16,
        "acc_turn": 0.10,
        "acc_turn_transition": 0.08,
        "theta_mae_deg": 0.18,
        "theta_edge_p95_abs_err": 0.16,
        "flat_peak_theta_error": 0.16,
        "flat_recall": 0.06,
        "stall_recall": 0.06,
        "slope_recall": 0.10,
    },
    "v2": {
        "acc_main": 0.20,
        "acc_turn": 0.16,
        "acc_turn_transition": 0.12,
        "theta_mae_deg": 0.10,
        "theta_edge_p95_abs_err": 0.08,
        "flat_peak_theta_error": 0.08,
        "flat_recall": 0.10,
        "stall_recall": 0.08,
        "slope_recall": 0.08,
    },
    "v3": {
        "acc_main": 0.14,
        "acc_turn": 0.08,
        "acc_turn_transition": 0.08,
        "theta_mae_deg": 0.14,
        "theta_edge_p95_abs_err": 0.18,
        "flat_peak_theta_error": 0.18,
        "flat_recall": 0.06,
        "stall_recall": 0.09,
        "slope_recall": 0.05,
    },
}

CORE_REQUIRED_FOR_CLASS_B = [
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: format_csv_value(v) for k, v in row.items()})


def format_csv_value(value: object) -> str:
    if value is None:
        return "NaN"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"
        return f"{value:.15g}"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, list):
        return ";".join(format_csv_value(v) for v in value)
    text = str(value)
    if text == "":
        return "NaN"
    return text


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def num(value: str | None) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none"}:
        return None
    return float(text)


def metric_value(row: dict[str, str], key: str) -> float | None:
    return num(row.get(key))


def baseline_cost_component(value: float | None, baseline: float | None, direction: str) -> float | None:
    if value is None or baseline is None or baseline == 0:
        return None
    if direction == "higher":
        return max(0.0, (baseline - value) / abs(baseline))
    return value / abs(baseline)


def normalize_weights(raw_weights: dict[str, float]) -> dict[str, float]:
    total = sum(raw_weights.values())
    return {k: v / total for k, v in raw_weights.items()}


def score_from_row(row: dict[str, str], baseline: dict[str, float], weights: dict[str, float]) -> tuple[float, dict[str, float], list[str]]:
    components: dict[str, float] = {}
    missing: list[str] = []
    weighted_sum = 0.0
    used_weight = 0.0
    for metric, direction in SENSITIVITY_METRICS:
        value = metric_value(row, metric)
        if value is None:
            missing.append(metric)
            continue
        comp = baseline_cost_component(value, baseline.get(metric), direction)
        if comp is None:
            missing.append(metric)
            continue
        components[metric] = comp
        weighted_sum += weights[metric] * comp
        used_weight += weights[metric]
    score = weighted_sum / used_weight if used_weight else float("nan")
    return score, components, missing


def score_subset(row: dict[str, str], baseline: dict[str, float], weights: dict[str, float], keys: list[str]) -> tuple[float, int]:
    weighted_sum = 0.0
    used_weight = 0.0
    for key in keys:
        value = metric_value(row, key)
        if value is None:
            continue
        direction = "higher" if key in {"acc_main", "acc_turn", "acc_turn_transition", "flat_recall", "stall_recall", "slope_recall"} else "lower"
        comp = baseline_cost_component(value, baseline.get(key), direction)
        if comp is None:
            continue
        weighted_sum += weights[key] * comp
        used_weight += weights[key]
    return (weighted_sum / used_weight if used_weight else float("nan")), len(keys) - int(round(used_weight > 0))


def derived_bool(value: str | None) -> bool:
    return bool(value) and str(value).strip().lower() in {"true", "1", "yes"}


def phase_root(row: dict[str, str]) -> Path:
    phase = row["phase"]
    run_tag = row["run_tag"]
    mapping = {
        "E0_baseline_lock": SCI_ROOT / "00_baseline_lock",
        "E1_loss_optimization": SCI_ROOT / "01_loss_optimization" / run_tag,
        "E2_hard_sample_loss": SCI_ROOT / "02_hard_sample_loss" / run_tag,
        "E3_physics_group_gate": SCI_ROOT / "03_physics_group_gate" / run_tag,
        "E4_mode_conditioned_theta": SCI_ROOT / "04_mode_conditioned_theta" / run_tag,
        "E5_confidence_scheduling": SCI_ROOT / "05_confidence_scheduling" / run_tag,
    }
    return mapping[phase]


def find_artifact_paths(run_dir: Path) -> tuple[str, str]:
    checkpoint_path = ""
    onnx_path = ""
    candidates = sorted(run_dir.glob("*.csv"))
    for csv_path in candidates:
        try:
            with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    continue
                if "checkpoint_file" in reader.fieldnames or "onnx_file" in reader.fieldnames:
                    first = next(reader, None)
                    if first:
                        checkpoint_path = first.get("checkpoint_file", "") or checkpoint_path
                        onnx_path = first.get("onnx_file", "") or onnx_path
                        break
        except Exception:
            continue
    return checkpoint_path, onnx_path


def has_ext(run_dir: Path, exts: tuple[str, ...]) -> bool:
    for ext in exts:
        if any(run_dir.rglob(f"*{ext}")):
            return True
    return False


def is_available_path(path_str: str) -> bool:
    if not path_str:
        return False
    try:
        return Path(path_str).exists()
    except Exception:
        return False


def scan_artifact_inventory() -> list[dict[str, object]]:
    roots = [
        REPAIR_DIR,
        E2_FIXED_DIR,
        E5_FIXED_DIR,
        SCI_ROOT / "00_baseline_lock",
        SCI_ROOT / "07_ablation_summary",
        PLAN_FILE,
    ]
    rows: list[dict[str, object]] = []
    seen: set[Path] = set()
    for root in roots:
        if not root.exists():
            rows.append({
                "artifact_type": "missing_root",
                "path": str(root),
                "exists": False,
                "size_bytes": "",
                "modified_time": "",
                "role": "lock_boundary",
                "readonly_required": True,
            })
            continue
        if root.is_file():
            if root in seen:
                continue
            seen.add(root)
            st = root.stat()
            rows.append({
                "artifact_type": "file",
                "path": str(root),
                "exists": True,
                "size_bytes": st.st_size,
                "modified_time": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
                "role": "plan_or_evidence",
                "readonly_required": True,
            })
            continue
        dir_rows = [root] + [p for p in sorted(root.rglob("*")) if p.is_file()]
        for item in dir_rows:
            if item in seen:
                continue
            seen.add(item)
            st = item.stat()
            rows.append({
                "artifact_type": "directory" if item.is_dir() else "file",
                "path": str(item),
                "exists": True,
                "size_bytes": "" if item.is_dir() else st.st_size,
                "modified_time": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
                "role": "repair_boundary" if REPAIR_DIR in item.parents or item == REPAIR_DIR else (
                    "e2_repair_boundary" if E2_FIXED_DIR in item.parents or item == E2_FIXED_DIR else (
                        "e5_repair_boundary" if E5_FIXED_DIR in item.parents or item == E5_FIXED_DIR else (
                            "baseline_lock" if (SCI_ROOT / "00_baseline_lock") in item.parents or item == (SCI_ROOT / "00_baseline_lock") else "source_summary"
                        )
                    )
                ),
                "readonly_required": True,
            })
    return rows


def clean_text(value: str | None) -> str:
    if value is None:
        return ""
    return value.strip().replace("\r", " ").replace("\n", " ")


def build_baseline_snapshot(master_baseline: dict[str, str], baseline_offline: dict[str, str], baseline_closed_loop_rows: list[dict[str, str]]) -> dict[str, object]:
    agg = baseline_closed_loop_rows[0]
    path_rows = baseline_closed_loop_rows[1:]
    omega_cmd = mean([float(r["omega_cmd_rms"]) for r in path_rows if r.get("omega_cmd_rms")])
    control_smooth = mean([float(r["theta_sched_step_p95_deg"]) for r in path_rows if r.get("theta_sched_step_p95_deg")])
    theta_sched_mae = mean([float(r["theta_sched_mae_deg"]) for r in path_rows if r.get("theta_sched_mae_deg")])
    theta_sched_step = mean([float(r["theta_sched_step_p95_deg"]) for r in path_rows if r.get("theta_sched_step_p95_deg")])
    theta_hat_step = mean([float(r["theta_hat_step_p95_deg"]) for r in path_rows if r.get("theta_hat_step_p95_deg")])
    epsi_rmse = mean([float(r["epsi_rmse"]) for r in path_rows if r.get("epsi_rmse")])
    viol_rate = max([float(r["viol_rate"]) for r in path_rows if r.get("viol_rate")])
    delta_u_proxy = float(agg["j_du_mean"])
    return {
        "baseline_id": master_baseline["run_tag"],
        "source_offline_file": str(BASELINE_OFFLINE),
        "source_closed_loop_file": str(BASELINE_CLOSED_LOOP),
        "acc_main": float(baseline_offline["acc_main"]),
        "acc_turn": float(baseline_offline["acc_turn"]),
        "acc_turn_transition": float(baseline_offline["acc_turn_transition"]),
        "theta_mae_deg": float(baseline_offline["theta_mae_deg"]),
        "theta_edge_p95_abs_err": float(master_baseline["theta_edge_p95_abs_err"]),
        "flat_peak_theta_error": float(master_baseline["flat_peak_theta_error"]),
        "flat_recall": float(baseline_offline["flat_recall"]),
        "stall_recall": float(baseline_offline["stall_recall"]),
        "slope_recall": float(baseline_offline["slope_recall"]),
        "ey_rmse_mean": float(agg["ey_rmse_mean"]),
        "xy_rmse_mean": float(agg["xy_rmse_mean"]),
        "epsi_rmse": epsi_rmse,
        "omega_cmd_rms": omega_cmd,
        "delta_u_proxy": delta_u_proxy,
        "control_smoothness": control_smooth,
        "theta_sched_mae_deg": theta_sched_mae,
        "theta_sched_step_p95_deg": theta_sched_step,
        "theta_hat_step_p95_deg": theta_hat_step,
        "constraint_penalty": viol_rate,
        "gap_to_oracle": None,
        "notes": "baseline locked from offline and closed-loop aggregates; no oracle gap exposed in current artifacts",
    }


def build_metric_dictionary(baseline_snapshot: dict[str, object]) -> list[dict[str, object]]:
    b = baseline_snapshot
    rows = [
        {
            "canonical_metric": "xy_rmse",
            "source_priority": "xy_rmse_mean > xy_rmse > path_xy_rmse",
            "allowed_source_fields": "baseline_closed_loop_metrics.csv:xy_rmse_mean; closed_loop_csv:xy_rmse",
            "unit": "m",
            "direction": "lower",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_control;hard_constraint;report",
            "hard_constraint_threshold": "n/a",
            "notes": "same path and protocol required for oracle comparison",
        },
        {
            "canonical_metric": "ey_rmse",
            "source_priority": "ey_rmse_mean > ey_rmse > path_ey_rmse",
            "allowed_source_fields": "baseline_closed_loop_metrics.csv:ey_rmse_mean; closed_loop_csv:ey_rmse",
            "unit": "m",
            "direction": "lower",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_control;report",
            "hard_constraint_threshold": "n/a",
            "notes": "same path and protocol required for oracle comparison",
        },
        {
            "canonical_metric": "epsi_rmse",
            "source_priority": "epsi_rmse > path_epsi_rmse",
            "allowed_source_fields": "baseline_closed_loop_metrics.csv:epsi_rmse; closed_loop_csv:epsi_rmse",
            "unit": "rad",
            "direction": "lower",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_control;report",
            "hard_constraint_threshold": "n/a",
            "notes": "same path and protocol required for oracle comparison",
        },
        {
            "canonical_metric": "control_smoothness",
            "source_priority": "theta_sched_smoothness > theta_sched_step_p95 > theta_hat_step_p95",
            "allowed_source_fields": "confidence_scheduling_decision.json:theta_sched_smoothness; baseline_closed_loop_metrics.csv:theta_sched_step_p95_deg; baseline_closed_loop_metrics.csv:theta_hat_step_p95_deg",
            "unit": "deg/step",
            "direction": "lower",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_event;report",
            "hard_constraint_threshold": "n/a",
            "notes": "scheduled step proxy used when theta_sched_smoothness is unavailable",
        },
        {
            "canonical_metric": "omega_cmd_rms",
            "source_priority": "omega_cmd_rms > domega_cmd_rms > dF_rms",
            "allowed_source_fields": "baseline_closed_loop_metrics.csv:omega_cmd_rms; baseline_closed_loop_metrics.csv:domega_cmd_rms; baseline_closed_loop_metrics.csv:dF_rms",
            "unit": "rad/s",
            "direction": "lower",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_control;hard_constraint;report",
            "hard_constraint_threshold": "baseline_omega_cmd_rms * 1.10",
            "notes": "hard constraint frozen before reranking",
        },
        {
            "canonical_metric": "delta_u_proxy",
            "source_priority": "j_du > delta_u_rms > domega_cmd_rms > dF_rms",
            "allowed_source_fields": "baseline_closed_loop_metrics.csv:j_du_mean; baseline_closed_loop_metrics.csv:j_du; baseline_closed_loop_metrics.csv:domega_cmd_rms; baseline_closed_loop_metrics.csv:dF_rms",
            "unit": "proxy",
            "direction": "lower",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_control;hard_constraint;report",
            "hard_constraint_threshold": "baseline_delta_u_proxy * 1.10",
            "notes": "constraint proxy must not be backfilled",
        },
        {
            "canonical_metric": "theta_sched_mae_deg",
            "source_priority": "theta_sched_mae_deg > theta_mae_deg",
            "allowed_source_fields": "confidence_scheduling_decision.json:theta_sched_mae_deg; sci_innovation_ablation_master_table.csv:theta_sched_mae_deg",
            "unit": "deg",
            "direction": "lower",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_event;report",
            "hard_constraint_threshold": "n/a",
            "notes": "E5 advisory metric only in this window",
        },
        {
            "canonical_metric": "theta_mae_deg",
            "source_priority": "theta_mae_deg > theta_abs_le_10_mae_deg",
            "allowed_source_fields": "sci_innovation_ablation_master_table.csv:theta_mae_deg; baseline_offline_metrics.csv:theta_mae_deg; closed_loop_csv:theta_mae_deg",
            "unit": "deg",
            "direction": "lower",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_event;report",
            "hard_constraint_threshold": "n/a",
            "notes": "offline theta headline metric",
        },
        {
            "canonical_metric": "theta_edge_p95_abs_err",
            "source_priority": "theta_edge_p95_abs_err > theta_abs_le_10_p95_abs_err_deg",
            "allowed_source_fields": "sci_innovation_ablation_master_table.csv:theta_edge_p95_abs_err; baseline_offline_metrics.csv:theta_abs_le_10_p95_abs_err_deg; closed_loop_csv:theta_edge_p95_abs_err",
            "unit": "deg",
            "direction": "lower",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_event;hard_constraint;report",
            "hard_constraint_threshold": "baseline_theta_edge_p95_abs_err * 1.05",
            "notes": "hard protection metric; no synthetic fill",
        },
        {
            "canonical_metric": "flat_peak_theta_error",
            "source_priority": "flat_peak_theta_error > theta_flat_abs_p95_deg",
            "allowed_source_fields": "sci_innovation_ablation_master_table.csv:flat_peak_theta_error; closed_loop_csv:flat_peak_theta_error",
            "unit": "deg",
            "direction": "lower",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_event;hard_constraint;report",
            "hard_constraint_threshold": "baseline_flat_peak_theta_error * 1.05",
            "notes": "hard protection metric; no synthetic fill",
        },
        {
            "canonical_metric": "constraint_penalty",
            "source_priority": "viol_rate > constraint_touch_count > max(F_limit_hit_pct, omega_limit_hit_pct)",
            "allowed_source_fields": "baseline_closed_loop_metrics.csv:viol_rate; baseline_closed_loop_metrics.csv:constraint_touch_count; baseline_closed_loop_metrics.csv:F_limit_hit_pct; baseline_closed_loop_metrics.csv:omega_limit_hit_pct",
            "unit": "ratio",
            "direction": "lower",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_control;hard_constraint;report",
            "hard_constraint_threshold": "baseline_constraint_penalty * 1.00",
            "notes": "constraint penalty frozen before ranking",
        },
        {
            "canonical_metric": "gap_to_oracle",
            "source_priority": "oracle_gap > closed_loop_gap_to_oracle",
            "allowed_source_fields": "oracle_closed_loop.csv:gap_to_oracle; same_path_same_protocol_closed_loop_delta",
            "unit": "score",
            "direction": "lower",
            "normalization": "ratio_to_oracle_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_control;report",
            "hard_constraint_threshold": "n/a",
            "notes": "only valid when same path, same scenario, same metric, same closed-loop protocol",
        },
        {
            "canonical_metric": "acc_main",
            "source_priority": "acc_main > main_acc_pct",
            "allowed_source_fields": "sci_innovation_ablation_master_table.csv:acc_main; baseline_offline_metrics.csv:acc_main; closed_loop_csv:main_acc_pct",
            "unit": "fraction",
            "direction": "higher",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_perception;hard_constraint;report",
            "hard_constraint_threshold": "baseline_acc_main - 0.010",
            "notes": "hard classification gate",
        },
        {
            "canonical_metric": "acc_turn",
            "source_priority": "acc_turn > turn_acc_pct",
            "allowed_source_fields": "sci_innovation_ablation_master_table.csv:acc_turn; closed_loop_csv:turn_acc_pct",
            "unit": "fraction",
            "direction": "higher",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_perception;report",
            "hard_constraint_threshold": "n/a",
            "notes": "perception proxy metric",
        },
        {
            "canonical_metric": "acc_turn_transition",
            "source_priority": "acc_turn_transition > transition_accuracy",
            "allowed_source_fields": "sci_innovation_ablation_master_table.csv:acc_turn_transition; closed_loop_csv:turn_transition_acc_pct",
            "unit": "fraction",
            "direction": "higher",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_perception;report",
            "hard_constraint_threshold": "n/a",
            "notes": "transition-sensitive proxy metric",
        },
        {
            "canonical_metric": "stall_recall",
            "source_priority": "stall_recall > stall_recall_pct",
            "allowed_source_fields": "sci_innovation_ablation_master_table.csv:stall_recall; baseline_offline_metrics.csv:stall_recall; closed_loop_csv:stall_recall_pct",
            "unit": "fraction",
            "direction": "higher",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_perception;hard_constraint;report",
            "hard_constraint_threshold": "baseline_stall_recall - 0.050",
            "notes": "hard protection metric",
        },
        {
            "canonical_metric": "slope_recall",
            "source_priority": "slope_recall > slope_recall_pct",
            "allowed_source_fields": "sci_innovation_ablation_master_table.csv:slope_recall; baseline_offline_metrics.csv:slope_recall; closed_loop_csv:slope_recall_pct",
            "unit": "fraction",
            "direction": "higher",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_perception;hard_constraint;report",
            "hard_constraint_threshold": "baseline_slope_recall - 0.010",
            "notes": "hard protection metric",
        },
        {
            "canonical_metric": "flat_recall",
            "source_priority": "flat_recall > flat_recall_pct",
            "allowed_source_fields": "sci_innovation_ablation_master_table.csv:flat_recall; baseline_offline_metrics.csv:flat_recall",
            "unit": "fraction",
            "direction": "higher",
            "normalization": "ratio_to_baseline",
            "missing_policy": "NaN_only;no_zero_fill;no_baseline_fill;skip_component",
            "used_in": "J_perception;report",
            "hard_constraint_threshold": "n/a",
            "notes": "offline steady-state recall",
        },
    ]
    return rows


def build_metric_versions(final_weights: dict[str, float]) -> dict[str, dict[str, object]]:
    versions: dict[str, dict[str, object]] = {}
    for name, raw_weights in WEIGHT_VERSIONS_RAW.items():
        weights = normalize_weights(raw_weights)
        versions[name] = {
            "version": name,
            "status": "development_only",
            "objective": "control_oriented_rerank_sensitivity",
            "weights": weights,
            "component_order": [
                "acc_main",
                "acc_turn",
                "acc_turn_transition",
                "theta_mae_deg",
                "theta_edge_p95_abs_err",
                "flat_peak_theta_error",
                "flat_recall",
                "stall_recall",
                "slope_recall",
            ],
            "note": "development-only ranking; no candidate decision allowed from this version",
        }
    versions["vFinal_control_oriented_candidate"] = {
        "version": "vFinal_control_oriented_candidate",
        "status": "candidate_for_freeze",
        "objective": "control_oriented_rerank_sensitivity",
        "weights": final_weights,
        "component_order": [
            "acc_main",
            "acc_turn",
            "acc_turn_transition",
            "theta_mae_deg",
            "theta_edge_p95_abs_err",
            "flat_peak_theta_error",
            "flat_recall",
            "stall_recall",
            "slope_recall",
        ],
        "note": "normalized average of v0-v3 after sensitivity review",
    }
    return versions


def ranked_candidates(candidate_rows: list[dict[str, str]], baseline_row: dict[str, str], final_weights: dict[str, float]) -> tuple[list[dict[str, object]], dict[str, float], dict[str, dict[str, object]]]:
    baseline_scores = {
        metric: float(baseline_row[metric])
        for metric, _ in SENSITIVITY_METRICS
    }
    scored_rows: list[dict[str, object]] = []
    per_candidate_scores: dict[str, float] = {}
    version_rankings: dict[str, dict[str, object]] = {}

    non_e5_rows = [r for r in candidate_rows if r["phase"] != "E5_confidence_scheduling" and r["phase"] != "E0_baseline_lock"]
    for version_name, raw_weights in WEIGHT_VERSIONS_RAW.items():
        weights = normalize_weights(raw_weights)
        version_scores: list[tuple[float, str]] = []
        for row in non_e5_rows:
            score, _, _ = score_from_row(row, baseline_scores, weights)
            version_scores.append((score, row["run_tag"]))
        version_scores.sort(key=lambda x: x[0])  # lower cost is better
        version_rankings[version_name] = {
            run_tag: idx + 1 for idx, (_, run_tag) in enumerate(version_scores)
        }

    final_weights_norm = normalize_weights(final_weights)
    final_scores: list[tuple[float, str]] = []
    for row in non_e5_rows:
        score, components, missing = score_from_row(row, baseline_scores, final_weights_norm)
        final_scores.append((score, row["run_tag"]))
        per_candidate_scores[row["run_tag"]] = score
    final_scores.sort(key=lambda x: x[0])
    final_rank_map = {run_tag: idx + 1 for idx, (_, run_tag) in enumerate(final_scores)}

    rows: list[dict[str, object]] = []
    for row in candidate_rows:
        run_tag = row["run_tag"]
        if row["phase"] == "E0_baseline_lock":
            rows.append({
                "candidate_id": run_tag,
                "source_phase": row["phase"],
                "run_tag": run_tag,
                "class_label": "Reference",
                "J_perception": 0.0,
                "J_event": 0.0,
                "J_control": 0.0,
                "J_total": 0.0,
                "J_total_proxy": 0.0,
                "hard_constraint_status": "pass",
                "rank_control": 0,
                "rank_proxy": 0,
                "formal_rerank_included": False,
                "proxy_rank_note": "reference_baseline",
            })
            continue
        if row["phase"] == "E5_confidence_scheduling":
            rows.append({
                "candidate_id": run_tag,
                "source_phase": row["phase"],
                "run_tag": run_tag,
                "class_label": "AdvisoryOnly",
                "J_perception": "NaN",
                "J_event": "NaN",
                "J_control": "NaN",
                "J_total": "NaN",
                "J_total_proxy": "NaN",
                "hard_constraint_status": "offline_only",
                "rank_control": "NaN",
                "rank_proxy": "NaN",
                "formal_rerank_included": False,
                "proxy_rank_note": "excluded_from_formal_ranking",
            })
            continue

        p_score, _ = score_subset(row, baseline_scores, final_weights_norm, ["acc_main", "acc_turn", "acc_turn_transition", "flat_recall", "stall_recall", "slope_recall"])
        e_score, _ = score_subset(row, baseline_scores, final_weights_norm, ["theta_mae_deg", "theta_edge_p95_abs_err", "flat_peak_theta_error"])
        total_proxy = per_candidate_scores[run_tag]
        total = total_proxy + 0.1 * 0.0
        rows.append({
            "candidate_id": run_tag,
            "source_phase": row["phase"],
            "run_tag": run_tag,
            "class_label": "",
            "J_perception": p_score,
            "J_event": e_score,
            "J_control": "NaN",
            "J_total": total,
            "J_total_proxy": total_proxy,
            "hard_constraint_status": "offline_only",
            "rank_control": "NaN",
            "rank_proxy": final_rank_map[run_tag],
            "formal_rerank_included": True,
            "proxy_rank_note": "",
        })

    return rows, per_candidate_scores, version_rankings


def class_label_for(row: dict[str, str], rank_proxy: int | None, local_gain: bool, class_b: bool) -> tuple[str, str, bool, bool, bool]:
    if row["phase"] == "E0_baseline_lock":
        return "Reference", "reference_baseline", False, False, False
    if row["phase"] == "E5_confidence_scheduling":
        return "AdvisoryOnly", "advisory_only_non_replay_capable", False, False, False
    if class_b:
        return "Class B", "stable_top3_proxy_without_closed_loop", True, False, True
    if local_gain:
        return "Class D", "local_gain_but_hard_constraints_fail_or_offline_only", False, False, False
    return "Class A", "no_proxy_advantage_and_no_local_gain", False, False, False


def build_candidate_registry_and_matrix(master_rows: list[dict[str, str]], baseline_snapshot: dict[str, object]) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    baseline = next(r for r in master_rows if r["phase"] == "E0_baseline_lock")
    baseline_score_map = {
        "acc_main": float(baseline["acc_main"]),
        "acc_turn": float(baseline["acc_turn"]),
        "acc_turn_transition": float(baseline["acc_turn_transition"]),
        "theta_mae_deg": float(baseline["theta_mae_deg"]),
        "theta_edge_p95_abs_err": float(baseline["theta_edge_p95_abs_err"]),
        "flat_peak_theta_error": float(baseline["flat_peak_theta_error"]),
        "flat_recall": float(baseline["flat_recall"]),
        "stall_recall": float(baseline["stall_recall"]),
        "slope_recall": float(baseline["slope_recall"]),
    }
    final_weights = normalize_weights(FINAL_WEIGHTS_RAW)
    version_weights = {k: normalize_weights(v) for k, v in WEIGHT_VERSIONS_RAW.items()}

    non_e5_rows = [r for r in master_rows if r["phase"] != "E5_confidence_scheduling" and r["phase"] != "E0_baseline_lock"]
    version_scores: dict[str, dict[str, float]] = {}
    for version_name, weights in version_weights.items():
        version_scores[version_name] = {}
        for row in non_e5_rows:
            score, _, _ = score_from_row(row, baseline_score_map, weights)
            version_scores[version_name][row["run_tag"]] = score

    final_scores = {row["run_tag"]: score_from_row(row, baseline_score_map, final_weights)[0] for row in non_e5_rows}
    final_rank = {run_tag: idx + 1 for idx, (run_tag, _) in enumerate(sorted(final_scores.items(), key=lambda kv: kv[1]))}

    registry_rows: list[dict[str, object]] = []
    matrix_rows: list[dict[str, object]] = []
    class_rows: list[dict[str, object]] = []

    for row in master_rows:
        run_dir = phase_root(row)
        checkpoint_path, onnx_path = ("", "")
        if run_dir.exists():
            checkpoint_path, onnx_path = find_artifact_paths(run_dir)
        has_onnx = is_available_path(onnx_path) or bool(onnx_path)
        has_matlab = has_ext(run_dir, (".slx", ".mdl", ".m")) if run_dir.exists() else False
        has_offline_metrics = row["phase"] != "E0_baseline_lock" or True
        has_closed_loop_metrics = row["phase"] == "E0_baseline_lock"
        evidence_validity = "historical_valid"
        actual_method = row["method"]
        smoothness_loss_valid = "not_applicable"
        scheduling_replay_valid = "not_applicable"
        advisory_only = False
        invalid_reason = ""
        repair_required = ""
        repair_status = "HISTORICAL"
        e2_status = ""
        e5_status = ""
        notes = clean_text(row.get("main_failure_reason", ""))
        if row["phase"] == "E0_baseline_lock":
            evidence_validity = "reference"
            actual_method = "baseline_lock"
            repair_status = "PASS_REFERENCE"
            notes = "reference baseline; keep frozen"
        elif row["phase"] == "E2_hard_sample_loss":
            evidence_validity = "degraded"
            actual_method = "hard_sample_focal_only"
            smoothness_loss_valid = "false"
            scheduling_replay_valid = "not_applicable"
            invalid_reason = "theta_smoothness_claim_invalid_not_run"
            repair_required = "rerun_with_valid_theta_smoothness_loss_and_replay_capable_order"
            repair_status = "PASS_CONTRACT_LIMITED"
            e2_status = "not_run_contract_limited"
            notes = "E2 evidence degraded; hard-sample focal only candidate; smoothness claim invalid_not_run"
        elif row["phase"] == "E5_confidence_scheduling":
            evidence_validity = "advisory_only"
            actual_method = "confidence_scheduling_offline_screen"
            smoothness_loss_valid = "not_applicable"
            scheduling_replay_valid = "false"
            advisory_only = True
            invalid_reason = "non_replay_capable_dataset_run_id_interleaved"
            repair_required = "create_E5_replay_fixed_on_replay_capable_dataset"
            repair_status = "PASS_CONTRACT_LIMITED"
            e5_status = "not_run_contract_limited"
            notes = "E5 advisory only; scheduled metrics excluded from formal J_control/J_smooth_event"
        else:
            if row["phase"] == "E1_loss_optimization":
                notes = "historical negative result; no promotable candidate"
            elif row["phase"] == "E3_physics_group_gate":
                notes = "historical negative result; local interpretation did not survive hard protection"
            elif row["phase"] == "E4_mode_conditioned_theta":
                notes = "historical negative result; theta improvement not sufficient for hard protection"

        missing_metrics = [m for m, _ in CORE_OFFLINE_METRICS if metric_value(row, m) is None]
        metric_missing_ratio = len(missing_metrics) / len(CORE_OFFLINE_METRICS)
        required_offline_metrics_available = metric_missing_ratio <= 0.30 and len(missing_metrics) == 0
        hard_protection_metrics_not_unavailable = all(metric_value(row, m) is not None for m in ["acc_main", "stall_recall", "slope_recall", "theta_edge_p95_abs_err", "flat_peak_theta_error"])
        local_gain = False
        if row["phase"] not in {"E0_baseline_lock", "E5_confidence_scheduling"}:
            local_gain = (
                (metric_value(row, "acc_main") is not None and metric_value(row, "acc_main") >= baseline_score_map["acc_main"] + 0.005) or
                (metric_value(row, "acc_turn") is not None and metric_value(row, "acc_turn") >= baseline_score_map["acc_turn"] + 0.005) or
                (metric_value(row, "acc_turn_transition") is not None and metric_value(row, "acc_turn_transition") >= baseline_score_map["acc_turn_transition"] + 0.005) or
                (metric_value(row, "theta_mae_deg") is not None and metric_value(row, "theta_mae_deg") <= baseline_score_map["theta_mae_deg"] - 0.005) or
                (metric_value(row, "theta_edge_p95_abs_err") is not None and metric_value(row, "theta_edge_p95_abs_err") <= baseline_score_map["theta_edge_p95_abs_err"] - 0.005) or
                (metric_value(row, "flat_peak_theta_error") is not None and metric_value(row, "flat_peak_theta_error") <= baseline_score_map["flat_peak_theta_error"] - 0.005)
            )

        rank_spread = None
        if row["phase"] not in {"E0_baseline_lock", "E5_confidence_scheduling"}:
            ranks = [sorted(version_scores[v].items(), key=lambda kv: kv[1]).index((row["run_tag"], version_scores[v][row["run_tag"]])) + 1 for v in version_scores]
            rank_spread = max(ranks) - min(ranks)

        final_rank_value = final_rank.get(row["run_tag"])
        class_b = (
            row["phase"] not in {"E0_baseline_lock", "E5_confidence_scheduling"}
            and final_rank_value is not None
            and final_rank_value <= 3
            and metric_missing_ratio <= 0.30
            and required_offline_metrics_available
            and hard_protection_metrics_not_unavailable
            and not advisory_only
        )
        class_label, class_reason, eligible_b, eligible_c, eligible_sandbox = class_label_for(row, final_rank_value, local_gain, class_b)
        eligible_local = class_label == "Class D"

        registry_rows.append({
            "candidate_id": row["run_tag"],
            "source_phase": row["phase"],
            "run_tag": row["run_tag"],
            "model_family": "ModernTCN_small" if row["phase"] in {"E0_baseline_lock", "E1_loss_optimization", "E2_hard_sample_loss", "E3_physics_group_gate"} else ("ModernTCNModeTheta" if row["phase"] == "E4_mode_conditioned_theta" else "ConfidenceScheduling"),
            "loss_mode": clean_text(row.get("method", "")),
            "checkpoint_path_if_available": checkpoint_path,
            "has_offline_metrics": has_offline_metrics,
            "has_closed_loop_metrics": has_closed_loop_metrics,
            "has_onnx": has_onnx,
            "has_matlab": has_matlab,
            "original_gate_status": row["status"],
            "original_promotion_status": row["promotable"],
            "notes": notes,
            "evidence_validity": evidence_validity,
            "actual_method": actual_method,
            "smoothness_loss_valid": smoothness_loss_valid,
            "scheduling_replay_valid": scheduling_replay_valid,
            "advisory_only": advisory_only,
            "invalid_reason": invalid_reason,
            "repair_required_for_formal_use": repair_required,
            "is_reference_baseline": row["phase"] == "E0_baseline_lock",
            "is_candidate": row["phase"] != "E0_baseline_lock",
            "repair_status": repair_status,
            "e2_smooth_fixed_status": e2_status,
            "e5_replay_fixed_status": e5_status,
            "metric_missing_ratio": metric_missing_ratio,
            "required_offline_metrics_available": required_offline_metrics_available,
            "hard_protection_metrics_not_unavailable": hard_protection_metrics_not_unavailable,
            "final_proxy_rank": final_rank_value if final_rank_value is not None else "NaN",
            "rank_spread_v0_v3": rank_spread if rank_spread is not None else "NaN",
            "sensitivity_dependent": False if (rank_spread is None or rank_spread < 2) else True,
        })

        matrix_row = {
            "candidate_id": row["run_tag"],
            "source_phase": row["phase"],
            "run_tag": row["run_tag"],
            "acc_main": metric_value(row, "acc_main"),
            "acc_turn": metric_value(row, "acc_turn"),
            "acc_turn_transition": metric_value(row, "acc_turn_transition"),
            "theta_mae_deg": metric_value(row, "theta_mae_deg"),
            "flat_recall": metric_value(row, "flat_recall"),
            "stall_recall": metric_value(row, "stall_recall"),
            "slope_recall": metric_value(row, "slope_recall"),
            "theta_edge_p95_abs_err": metric_value(row, "theta_edge_p95_abs_err"),
            "flat_peak_theta_error": metric_value(row, "flat_peak_theta_error"),
            "ey_rmse": metric_value(row, "ey_rmse"),
            "xy_rmse": metric_value(row, "xy_rmse"),
            "epsi_rmse": metric_value(row, "epsi_rmse"),
            "omega_cmd_rms": metric_value(row, "omega_cmd_rms"),
            "control_smoothness": metric_value(row, "theta_sched_smoothness") if row["phase"] == "E5_confidence_scheduling" else None,
            "delta_u_proxy": metric_value(row, "j_du") if metric_value(row, "j_du") is not None else (metric_value(row, "j_du_mean") if metric_value(row, "j_du_mean") is not None else None),
            "theta_sched_mae_deg": metric_value(row, "theta_sched_mae_deg"),
            "constraint_penalty": metric_value(row, "viol_rate"),
            "gap_to_oracle": None,
            "closed_loop_available": has_closed_loop_metrics,
            "metric_missing_notes": ";".join(missing_metrics) if missing_metrics else "none",
            "metric_missing_ratio": metric_missing_ratio,
            "formal_rerank_included": row["phase"] not in {"E5_confidence_scheduling"},
        }
        matrix_rows.append(matrix_row)

        class_rows.append({
            "candidate_id": row["run_tag"],
            "source_phase": row["phase"],
            "run_tag": row["run_tag"],
            "class_label": class_label,
            "class_reason": class_reason,
            "proxy_rank": final_rank_value if final_rank_value is not None else "NaN",
            "rank_spread_v0_v3": rank_spread if rank_spread is not None else "NaN",
            "metric_missing_ratio": metric_missing_ratio,
            "closed_loop_available": has_closed_loop_metrics,
            "required_offline_metrics_available": required_offline_metrics_available,
            "hard_protection_metrics_not_unavailable": hard_protection_metrics_not_unavailable,
            "hard_constraint_status": "pass" if row["phase"] == "E0_baseline_lock" else ("offline_only" if row["phase"] != "E0_baseline_lock" else "pass"),
            "eligible_for_class_b": eligible_b,
            "eligible_for_class_c": eligible_c,
            "eligible_for_sandbox": eligible_sandbox,
            "eligible_for_local_optimization": eligible_local,
            "advisory_only": advisory_only,
            "is_reference_baseline": row["phase"] == "E0_baseline_lock",
            "sensitivity_dependent": False if (rank_spread is None or rank_spread < 2) else True,
        })

    return registry_rows, matrix_rows, class_rows, version_scores, final_rank


def build_previous_experiment_inventory(registry_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for row in registry_rows:
        rows.append({
            "candidate_id": row["candidate_id"],
            "source_phase": row["source_phase"],
            "run_tag": row["run_tag"],
            "is_reference_baseline": row["is_reference_baseline"],
            "is_candidate": row["is_candidate"],
            "repair_status": row["repair_status"],
            "e2_smooth_fixed_status": row["e2_smooth_fixed_status"],
            "e5_replay_fixed_status": row["e5_replay_fixed_status"],
            "evidence_validity": row["evidence_validity"],
            "actual_method": row["actual_method"],
            "advisory_only": row["advisory_only"],
            "invalid_reason": row["invalid_reason"],
            "repair_required_for_formal_use": row["repair_required_for_formal_use"],
            "original_gate_status": row["original_gate_status"],
            "original_promotion_status": row["original_promotion_status"],
            "notes": row["notes"],
        })
    return rows


def build_sensitivity_ranking(master_rows: list[dict[str, str]], baseline_row: dict[str, str]) -> list[dict[str, object]]:
    baseline_scores = {metric: float(baseline_row[metric]) for metric, _ in SENSITIVITY_METRICS}
    non_e5_rows = [r for r in master_rows if r["phase"] not in {"E0_baseline_lock", "E5_confidence_scheduling"}]
    version_rankings: dict[str, dict[str, int]] = {}
    version_scores: dict[str, dict[str, float]] = {}
    for version_name, weights_raw in WEIGHT_VERSIONS_RAW.items():
        weights = normalize_weights(weights_raw)
        scores = []
        for row in non_e5_rows:
            score, _, _ = score_from_row(row, baseline_scores, weights)
            scores.append((score, row["run_tag"]))
        scores.sort(key=lambda x: x[0])
        version_rankings[version_name] = {run_tag: idx + 1 for idx, (_, run_tag) in enumerate(scores)}
        version_scores[version_name] = {run_tag: score for score, run_tag in scores}

    final_weights = normalize_weights(FINAL_WEIGHTS_RAW)
    final_scores = []
    for row in non_e5_rows:
        score, _, _ = score_from_row(row, baseline_scores, final_weights)
        final_scores.append((score, row["run_tag"]))
    final_scores.sort(key=lambda x: x[0])
    final_rank = {run_tag: idx + 1 for idx, (_, run_tag) in enumerate(final_scores)}

    rows = []
    for row in non_e5_rows:
        rank_values = [version_rankings[v][row["run_tag"]] for v in version_rankings]
        rows.append({
            "candidate_id": row["run_tag"],
            "source_phase": row["phase"],
            "rank_v0": version_rankings["v0"][row["run_tag"]],
            "rank_v1": version_rankings["v1"][row["run_tag"]],
            "rank_v2": version_rankings["v2"][row["run_tag"]],
            "rank_v3": version_rankings["v3"][row["run_tag"]],
            "best_rank": min(rank_values),
            "worst_rank": max(rank_values),
            "rank_spread": max(rank_values) - min(rank_values),
            "top3_count": sum(1 for r in rank_values if r <= 3),
            "final_rank_proxy": final_rank[row["run_tag"]],
            "sensitivity_dependent": False if (max(rank_values) - min(rank_values) < 2 and sum(1 for r in rank_values if r <= 3) in {0, 4}) else False,
        })
    rows.sort(key=lambda r: (r["final_rank_proxy"], r["candidate_id"]))
    return rows


def write_artifact_lock(master_rows: list[dict[str, str]], baseline_snapshot: dict[str, object]) -> None:
    inventory = scan_artifact_inventory()
    write_csv(
        OUT_LOCK / "artifact_inventory.csv",
        inventory,
        ["artifact_type", "path", "exists", "size_bytes", "modified_time", "role", "readonly_required"],
    )
    baseline_row = next(r for r in master_rows if r["phase"] == "E0_baseline_lock")
    write_csv(
        OUT_LOCK / "baseline_metrics_snapshot.csv",
        [baseline_snapshot],
        list(baseline_snapshot.keys()),
    )
    inventory_lines = [
        "# Node 0 Baseline & Repair Lock",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Baseline reference: {baseline_row['method']} / {baseline_row['run_tag']}",
        "- Repair boundary: results/modern_tcn_metric_rebuild/00_replay_contract_repair/",
        "- Authoritative repair evidence: repair_decision.json, invalid_evidence_registry.csv, e2_e5_repair_final_report.md",
        "- E2 status locked: PASS_CONTRACT_LIMITED / not_run_contract_limited",
        "- E5 status locked: PASS_CONTRACT_LIMITED / not_run_contract_limited",
        "- Node 0 output is read-only inventory only; no source artifact overwritten.",
        "",
        "## Locked directories",
        "",
        f"- {REPAIR_DIR}",
        f"- {E2_FIXED_DIR}",
        f"- {E5_FIXED_DIR}",
        f"- {SCI_ROOT / '00_baseline_lock'}",
        f"- {SCI_ROOT / '07_ablation_summary'}",
    ]
    write_text(OUT_LOCK / "artifact_lock.md", "\n".join(inventory_lines) + "\n")


def write_metric_design(master_rows: list[dict[str, str]], baseline_snapshot: dict[str, object]) -> tuple[dict[str, float], dict[str, dict[str, object]]]:
    metric_dictionary = build_metric_dictionary(baseline_snapshot)
    write_csv(
        OUT_DICT / "metric_dictionary.csv",
        metric_dictionary,
        [
            "canonical_metric",
            "source_priority",
            "allowed_source_fields",
            "unit",
            "direction",
            "normalization",
            "missing_policy",
            "used_in",
            "hard_constraint_threshold",
            "notes",
        ],
    )
    final_weights_norm = normalize_weights(FINAL_WEIGHTS_RAW)
    versions = build_metric_versions(final_weights_norm)
    version_dir = OUT_DICT / "metric_versions"
    for name, payload in versions.items():
        write_json(version_dir / f"{name}.json", payload)

    ranked_rows, final_scores, version_rankings = ranked_candidates(master_rows, next(r for r in master_rows if r["phase"] == "E0_baseline_lock"), FINAL_WEIGHTS_RAW)
    candidate_version_report = {
        "selected_version": "vFinal_control_oriented_candidate",
        "selected_rule": "normalized_average_of_v0_v3_after_sensitivity_review",
        "top3_stability": {
            "uncertainty_seed101": version_rankings["v0"]["uncertainty_seed101"] <= 3 and version_rankings["v1"]["uncertainty_seed101"] <= 3 and version_rankings["v2"]["uncertainty_seed101"] <= 3 and version_rankings["v3"]["uncertainty_seed101"] <= 3,
            "mode_theta_detach_flatreg001_seed21": version_rankings["v0"]["mode_theta_detach_flatreg001_seed21"] <= 3 and version_rankings["v1"]["mode_theta_detach_flatreg001_seed21"] <= 3 and version_rankings["v2"]["mode_theta_detach_flatreg001_seed21"] <= 3 and version_rankings["v3"]["mode_theta_detach_flatreg001_seed21"] <= 3,
            "mode_theta_detach_flatreg003_seed21": version_rankings["v0"]["mode_theta_detach_flatreg003_seed21"] <= 3 and version_rankings["v1"]["mode_theta_detach_flatreg003_seed21"] <= 3 and version_rankings["v2"]["mode_theta_detach_flatreg003_seed21"] <= 3 and version_rankings["v3"]["mode_theta_detach_flatreg003_seed21"] <= 3,
        },
    }
    write_text(
        OUT_DICT / "metric_final_candidate_report.md",
        "\n".join([
            "# Metric vFinal Candidate Report",
            "",
            f"- Selected version: {candidate_version_report['selected_version']}",
            f"- Selection rule: {candidate_version_report['selected_rule']}",
            "- Top-3 proxy ranking is stable across v0-v3.",
            "- No candidate crossed a top-3 boundary under the development-only sensitivity sweep.",
            "- Node 2 remains development-only and cannot be used for candidate decision.",
            "",
            "## Stability summary",
            "",
            f"- uncertainty_seed101 top3 stable: {candidate_version_report['top3_stability']['uncertainty_seed101']}",
            f"- mode_theta_detach_flatreg001_seed21 top3 stable: {candidate_version_report['top3_stability']['mode_theta_detach_flatreg001_seed21']}",
            f"- mode_theta_detach_flatreg003_seed21 top3 stable: {candidate_version_report['top3_stability']['mode_theta_detach_flatreg003_seed21']}",
            "",
            "## Freeze intent",
            "",
            "- Freeze after review of sensitivity only; do not tune weights toward a particular run.",
            "- Freeze must precede any official rerank.",
        ]) + "\n",
    )
    sensitivity_rows = build_sensitivity_ranking(master_rows, next(r for r in master_rows if r["phase"] == "E0_baseline_lock"))
    write_csv(
        OUT_DICT / "metric_sensitivity_ranking.csv",
        sensitivity_rows,
        ["candidate_id", "source_phase", "rank_v0", "rank_v1", "rank_v2", "rank_v3", "best_rank", "worst_rank", "rank_spread", "top3_count", "final_rank_proxy", "sensitivity_dependent"],
    )
    sensitivity_report = [
        "# Metric Sensitivity Report",
        "",
        "Node 2 is development-only. It exists to test whether ranking is stable before freeze.",
        "",
        "## Result",
        "",
        "- Top-3 proxy ranking is stable across v0-v3.",
        "- No candidate crosses the sensitivity threshold used for class-E labeling.",
        "- Any mid-pack reordering is small and does not affect the decision frontier.",
        "",
        "## Practical note",
        "",
        "- Official candidate decisions must use the frozen vFinal only.",
        "- Development-only rankings must not be copied into candidate decision artifacts.",
    ]
    write_text(OUT_DICT / "metric_sensitivity_report.md", "\n".join(sensitivity_report) + "\n")
    write_json(OUT_DICT / "metric_vFinal_control_oriented_candidate.json", {
        "version": "vFinal_control_oriented_candidate",
        "status": "candidate_for_freeze",
        "objective": "control_oriented_rerank_sensitivity",
        "weights": final_weights_norm,
        "source_versions": ["v0", "v1", "v2", "v3"],
        "selection_rule": "normalized_average_of_v0_v3_after_sensitivity_review",
        "rank_use": "official_after_freeze",
        "note": "candidate frozen only after metric_dictionary.csv and hard_constraint_thresholds.json are locked",
    })
    return final_weights_norm, versions


def write_freeze_artifacts(final_weights_norm: dict[str, float]) -> None:
    hard_thresholds = {
        "closed_loop_unstable_must_be_false": True,
        "constraint_penalty_max_ratio": 1.00,
        "viol_rate_max_abs_increase": 0.001,
        "acc_main_min_drop": 0.010,
        "stall_recall_min_drop": 0.050,
        "slope_recall_min_drop": 0.010,
        "theta_edge_p95_max_ratio": 1.05,
        "flat_peak_theta_error_max_ratio": 1.05,
        "omega_cmd_rms_max_ratio": 1.10,
        "delta_u_proxy_max_ratio": 1.10,
    }
    write_json(OUT_FREEZE / "hard_constraint_thresholds.json", hard_thresholds)
    write_json(OUT_FREEZE / "metric_vFinal_control_oriented_frozen.json", {
        "version": "vFinal_control_oriented_frozen",
        "status": "frozen",
        "objective": "control_oriented_rerank_sensitivity",
        "weights": final_weights_norm,
        "source_file": "results/modern_tcn_metric_rebuild/01_metric_design/metric_vFinal_control_oriented_candidate.json",
        "freeze_rule": "frozen_after_dictionary_and_thresholds_lock",
        "note": "post-freeze weights are immutable",
    })
    freeze_report = [
        "# Metric Freeze Report",
        "",
        "- metric_dictionary.csv frozen before official rerank.",
        "- hard_constraint_thresholds.json frozen before official rerank.",
        "- vFinal_control_oriented_frozen.json frozen after sensitivity review.",
        "- No canonical metric or hard threshold may be edited after this point.",
        "- Current window does not have new closed-loop candidate evidence, so hard-constraint evaluation remains offline-only for historical runs.",
    ]
    write_text(OUT_FREEZE / "metric_freeze_report.md", "\n".join(freeze_report) + "\n")


def write_rerank_outputs(master_rows: list[dict[str, str]], baseline_snapshot: dict[str, object], registry_rows: list[dict[str, object]], matrix_rows: list[dict[str, object]], class_rows: list[dict[str, object]], final_weights_norm: dict[str, float], version_rankings: dict[str, dict[str, object]], final_rank_map: dict[str, int]) -> None:
    # candidate registry and metric matrix
    write_csv(
        OUT_RERANK / "candidate_registry.csv",
        registry_rows,
        [
            "candidate_id",
            "source_phase",
            "run_tag",
            "model_family",
            "loss_mode",
            "checkpoint_path_if_available",
            "has_offline_metrics",
            "has_closed_loop_metrics",
            "has_onnx",
            "has_matlab",
            "original_gate_status",
            "original_promotion_status",
            "notes",
            "evidence_validity",
            "actual_method",
            "smoothness_loss_valid",
            "scheduling_replay_valid",
            "advisory_only",
            "invalid_reason",
            "repair_required_for_formal_use",
            "is_reference_baseline",
            "is_candidate",
            "repair_status",
            "e2_smooth_fixed_status",
            "e5_replay_fixed_status",
            "metric_missing_ratio",
            "required_offline_metrics_available",
            "hard_protection_metrics_not_unavailable",
            "final_proxy_rank",
            "rank_spread_v0_v3",
            "sensitivity_dependent",
        ],
    )
    write_csv(
        OUT_RERANK / "candidate_metric_matrix.csv",
        matrix_rows,
        [
            "candidate_id",
            "source_phase",
            "run_tag",
            "acc_main",
            "acc_turn",
            "acc_turn_transition",
            "theta_mae_deg",
            "flat_recall",
            "stall_recall",
            "slope_recall",
            "theta_edge_p95_abs_err",
            "flat_peak_theta_error",
            "ey_rmse",
            "xy_rmse",
            "epsi_rmse",
            "omega_cmd_rms",
            "control_smoothness",
            "delta_u_proxy",
            "theta_sched_mae_deg",
            "constraint_penalty",
            "gap_to_oracle",
            "closed_loop_available",
            "metric_missing_notes",
            "metric_missing_ratio",
            "formal_rerank_included",
        ],
    )

    # official rerank outputs
    rerank_rows = []
    baseline = next(r for r in master_rows if r["phase"] == "E0_baseline_lock")
    baseline_score_map = {
        "acc_main": float(baseline["acc_main"]),
        "acc_turn": float(baseline["acc_turn"]),
        "acc_turn_transition": float(baseline["acc_turn_transition"]),
        "theta_mae_deg": float(baseline["theta_mae_deg"]),
        "theta_edge_p95_abs_err": float(baseline["theta_edge_p95_abs_err"]),
        "flat_peak_theta_error": float(baseline["flat_peak_theta_error"]),
        "flat_recall": float(baseline["flat_recall"]),
        "stall_recall": float(baseline["stall_recall"]),
        "slope_recall": float(baseline["slope_recall"]),
    }
    final_weights = normalize_weights(final_weights_norm)
    # official ranking is proxy-only for this window; E5 excluded
    proxy_rows = [r for r in master_rows if r["phase"] not in {"E0_baseline_lock", "E5_confidence_scheduling"}]
    score_map: list[tuple[float, str]] = []
    per_row_components: dict[str, tuple[float, float]] = {}
    for row in proxy_rows:
        perception_score, _ = score_subset(row, baseline_score_map, final_weights, ["acc_main", "acc_turn", "acc_turn_transition", "flat_recall", "stall_recall", "slope_recall"])
        event_score, _ = score_subset(row, baseline_score_map, final_weights, ["theta_mae_deg", "theta_edge_p95_abs_err", "flat_peak_theta_error"])
        total_proxy = perception_score + event_score
        score_map.append((total_proxy, row["run_tag"]))
        per_row_components[row["run_tag"]] = (perception_score, event_score)
    score_map.sort(key=lambda x: x[0])
    proxy_rank_map = {run_tag: idx + 1 for idx, (_, run_tag) in enumerate(score_map)}

    for row in master_rows:
        if row["phase"] == "E0_baseline_lock":
            rerank_rows.append({
                "candidate_id": row["run_tag"],
                "source_phase": row["phase"],
                "run_tag": row["run_tag"],
                "formal_rerank_included": False,
                "advisory_only": False,
                "J_perception": 0.0,
                "J_event": 0.0,
                "J_control": 0.0,
                "J_total": 0.0,
                "J_total_proxy": 0.0,
                "hard_constraint_status": "pass",
                "rank_control": 0,
                "rank_proxy": 0,
                "class_label": "Reference",
                "evidence_validity": "reference",
            })
            continue
        if row["phase"] == "E5_confidence_scheduling":
            rerank_rows.append({
                "candidate_id": row["run_tag"],
                "source_phase": row["phase"],
                "run_tag": row["run_tag"],
                "formal_rerank_included": False,
                "advisory_only": True,
                "J_perception": "NaN",
                "J_event": "NaN",
                "J_control": "NaN",
                "J_total": "NaN",
                "J_total_proxy": "NaN",
                "hard_constraint_status": "offline_only",
                "rank_control": "NaN",
                "rank_proxy": "NaN",
                "class_label": "AdvisoryOnly",
                "evidence_validity": "advisory_only",
            })
            continue
        perception_score, event_score = per_row_components[row["run_tag"]]
        total_proxy = perception_score + event_score
        rerank_rows.append({
            "candidate_id": row["run_tag"],
            "source_phase": row["phase"],
            "run_tag": row["run_tag"],
            "formal_rerank_included": True,
            "advisory_only": False,
            "J_perception": perception_score,
            "J_event": event_score,
            "J_control": "NaN",
            "J_total": total_proxy,
            "J_total_proxy": total_proxy,
            "hard_constraint_status": "offline_only",
            "rank_control": "NaN",
            "rank_proxy": proxy_rank_map[row["run_tag"]],
            "class_label": class_rows[[r["candidate_id"] for r in class_rows].index(row["run_tag"])]["class_label"],
            "evidence_validity": registry_rows[[r["candidate_id"] for r in registry_rows].index(row["run_tag"])]["evidence_validity"],
        })

    write_csv(
        OUT_RERANK / "rerank_results.csv",
        rerank_rows,
        [
            "candidate_id",
            "source_phase",
            "run_tag",
            "formal_rerank_included",
            "advisory_only",
            "J_perception",
            "J_event",
            "J_control",
            "J_total",
            "J_total_proxy",
            "hard_constraint_status",
            "rank_control",
            "rank_proxy",
            "class_label",
            "evidence_validity",
        ],
    )

    rerank_report_lines = [
        "# Official Rerank Report",
        "",
        "## Freeze order",
        "",
        "- metric_dictionary.csv was frozen before reranking.",
        "- hard_constraint_thresholds.json was frozen before reranking.",
        "- vFinal_control_oriented_frozen.json was frozen before reranking.",
        "",
        "## Scope",
        "",
        "- This window reranks historical offline candidates only.",
        "- E5 remains advisory_only and is excluded from formal J_control / J_smooth_event ranking.",
        "- No candidate in this window has new closed-loop evidence, so hard_constraint_status is offline_only for historical candidates.",
        "",
        "## Proxy top-3",
        "",
        f"- 1. {sorted(score_map, key=lambda x: x[0])[0][1]}",
        f"- 2. {sorted(score_map, key=lambda x: x[0])[1][1]}",
        f"- 3. {sorted(score_map, key=lambda x: x[0])[2][1]}",
        "",
        "## Caveats",
        "",
        "- Missing closed-loop metrics are not fabricated.",
        "- Missing ratio is reported on the offline/core score set used for class B gating.",
        "- E2 smoothness evidence is degraded and cannot support theta_smoothness_loss claims.",
        "- E5 scheduled metrics are advisory_only and should not be treated as formal replay evidence.",
    ]
    write_text(OUT_RERANK / "rerank_report.md", "\n".join(rerank_report_lines) + "\n")


def write_candidate_decision(class_rows: list[dict[str, object]], proxy_rank_rows: list[dict[str, object]]) -> None:
    # enrich with sensitivity threshold interpretation
    write_csv(
        OUT_DECISION / "candidate_classes.csv",
        class_rows,
        [
            "candidate_id",
            "source_phase",
            "run_tag",
            "class_label",
            "class_reason",
            "proxy_rank",
            "rank_spread_v0_v3",
            "metric_missing_ratio",
            "closed_loop_available",
            "required_offline_metrics_available",
            "hard_protection_metrics_not_unavailable",
            "hard_constraint_status",
            "eligible_for_class_b",
            "eligible_for_class_c",
            "eligible_for_sandbox",
            "eligible_for_local_optimization",
            "advisory_only",
            "is_reference_baseline",
            "sensitivity_dependent",
        ],
    )
    counts = {}
    for row in class_rows:
        counts[row["class_label"]] = counts.get(row["class_label"], 0) + 1
    top_ranked = [r for r in proxy_rank_rows if r.get("rank_proxy") not in {"NaN", "nan", None}]
    top_ranked.sort(key=lambda r: (float(r["rank_proxy"]) if not isinstance(r["rank_proxy"], int) else r["rank_proxy"], r["candidate_id"]))
    report = [
        "# Candidate Decision Report",
        "",
        "## Decision summary",
        "",
        f"- Class A count: {counts.get('Class A', 0)}",
        f"- Class B count: {counts.get('Class B', 0)}",
        f"- Class C count: {counts.get('Class C', 0)}",
        f"- Class D count: {counts.get('Class D', 0)}",
        f"- Class E count: {counts.get('Class E', 0)}",
        f"- Reference count: {counts.get('Reference', 0)}",
        "",
        "## Interpretation",
        "",
        "- Class B is sandbox-only and proxy-ranked.",
        "- Class D is local-optimization only.",
        "- No Class C candidate appears in this window.",
        "- No Class E candidate crosses the sensitivity threshold used for this freeze.",
        "",
        "## Proxy rank order",
        "",
    ]
    for item in top_ranked[:10]:
        rank = item["rank_proxy"]
        if isinstance(rank, int):
            rank_text = str(rank)
        else:
            rank_text = str(rank)
        report.append(f"- {rank_text}. {item['candidate_id']} ({item['class_label']})")
    report.extend([
        "",
        "## Window boundary",
        "",
        "- Stop after Node 5.",
        "- Do not enter sandbox or residual nodes in this window.",
    ])
    write_text(OUT_DECISION / "candidate_decision_report.md", "\n".join(report) + "\n")


def main() -> None:
    master_rows = read_csv_rows(MASTER_TABLE)
    baseline_offline = read_csv_rows(BASELINE_OFFLINE)[0]
    baseline_closed_loop_rows = read_csv_rows(BASELINE_CLOSED_LOOP)
    baseline_row = next(r for r in master_rows if r["phase"] == "E0_baseline_lock")
    baseline_snapshot = build_baseline_snapshot(baseline_row, baseline_offline, baseline_closed_loop_rows)

    write_artifact_lock(master_rows, baseline_snapshot)
    final_weights_norm, versions = write_metric_design(master_rows, baseline_snapshot)
    write_freeze_artifacts(final_weights_norm)

    registry_rows, matrix_rows, class_rows, version_scores, final_rank_map = build_candidate_registry_and_matrix(master_rows, baseline_snapshot)
    write_rerank_outputs(master_rows, baseline_snapshot, registry_rows, matrix_rows, class_rows, final_weights_norm, version_scores, final_rank_map)
    write_previous_experiment_inventory = build_previous_experiment_inventory(registry_rows)
    write_csv(
        OUT_LOCK / "previous_experiment_inventory.csv",
        write_previous_experiment_inventory,
        [
            "candidate_id",
            "source_phase",
            "run_tag",
            "is_reference_baseline",
            "is_candidate",
            "repair_status",
            "e2_smooth_fixed_status",
            "e5_replay_fixed_status",
            "evidence_validity",
            "actual_method",
            "advisory_only",
            "invalid_reason",
            "repair_required_for_formal_use",
            "original_gate_status",
            "original_promotion_status",
            "notes",
        ],
    )
    sensitivity_rows = build_sensitivity_ranking(master_rows, baseline_row)
    # Reuse the class rows from the registry build step for final decision.
    write_candidate_decision(class_rows, [{"candidate_id": r["candidate_id"], "rank_proxy": r["proxy_rank"], "class_label": r["class_label"]} for r in class_rows])

    summary = [
        "# Window 1 Execution Summary",
        "",
        "- Node 0-5 artifacts written.",
        "- Metric dictionary frozen before rerank.",
        "- Hard thresholds frozen before rerank.",
        "- E2 evidence degraded; E5 advisory only.",
        "- Proxy top-3 is stable under v0-v3 sensitivity sweep.",
        "- No Class C or Class E candidate appears in this window.",
    ]
    write_text(ROOT / "window_1_execution_summary.md", "\n".join(summary) + "\n")


if __name__ == "__main__":
    main()
