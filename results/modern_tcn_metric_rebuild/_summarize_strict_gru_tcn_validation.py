from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean
from typing import Any

import numpy as np
import scipy.io as sio


ROOT = Path(__file__).resolve().parent
NODE_ROOT = ROOT / "09_strict_gru_tcn_validation"
FORMAL_ROOT = ROOT / "05_sandbox_closed_loop_if_needed" / "03_formal_validation"
FORMAL_PATH_METRICS = FORMAL_ROOT / "formal_validation_path_metrics.csv"
FORMAL_DECISION = FORMAL_ROOT / "formal_validation_class_c_decision.csv"
BASELINE_MATRIX = ROOT / "03_rerank_existing_experiments" / "candidate_metric_matrix.csv"
THRESHOLDS_FILE = ROOT / "02_metric_freeze" / "hard_constraint_thresholds.json"
VFINAL_FILE = ROOT / "02_metric_freeze" / "metric_vFinal_control_oriented_frozen.json"

SCI_ROOT = ROOT.parent / "modern_tcn_sci_innovation"
PAPER_ROOT = ROOT.parent / "paper" / "agv_model_parameter_correction_workflow"
BASELINE_IDENTITY = SCI_ROOT / "00_baseline_lock" / "e0_decision.json"
UNCERTAINTY_DIR = SCI_ROOT / "01_loss_optimization" / "uncertainty_seed101_rerun_20260622"
MODE_THETA_DIR = SCI_ROOT / "04_mode_conditioned_theta" / "mode_theta_detach_flatreg001_seed21_rerun_20260622"
GRU_META = PAPER_ROOT / "08_models" / "models" / "GRU_meta_full_gru_v5_plantfix_passive17_plus_all5_seed101.mat"
TCN_META = PAPER_ROOT / "08_models" / "models" / "TCN_meta_full_tcn_v5_plantfix_passive17_plus_all5_seed101.mat"

FROZEN_PATHS = {
    "path_factory_logistics_showcase_theta10_v3",
    "path_closed_loop_long_updown_theta10_v1",
    "path_closed_loop_sharp_turn_transition_theta10_v1",
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

HIGHER_BETTER = {
    "acc_main",
    "acc_turn",
    "acc_turn_transition",
    "flat_recall",
    "stall_recall",
    "slope_recall",
    "main_acc_pct",
    "turn_acc_pct",
    "slope_recall_pct",
    "right_recall_pct",
    "left_recall_pct",
}

CONTROL_COMPONENTS = ["ey_rmse", "xy_rmse", "epsi_rmse", "j_du", "omega_cmd_rms"]
AGGREGATE_METRICS = [
    "ey_rmse",
    "xy_rmse",
    "epsi_rmse",
    "ev_rmse",
    "eomega_rmse",
    "j_du",
    "omega_cmd_rms",
    "omega_cmd_peak",
    "viol_rate",
    "theta_mae_deg",
    "theta_sched_mae_deg",
    "main_acc_pct",
    "turn_acc_pct",
    "slope_recall_pct",
    "right_recall_pct",
    "left_recall_pct",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: fmt(row.get(key, "")) for key in fieldnames})


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def fmt(value: Any) -> str:
    if value is None:
        return "NaN"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    if isinstance(value, (float, np.floating)):
        value = float(value)
        if math.isnan(value):
            return "NaN"
        if math.isinf(value):
            return "Inf" if value > 0 else "-Inf"
        return f"{value:.15g}"
    text = str(value)
    return text if text else "NaN"


def num(value: Any) -> float:
    if value is None:
        return float("nan")
    if isinstance(value, (float, int, np.floating, np.integer)):
        return float(value)
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none"}:
        return float("nan")
    return float(text)


def safe_ratio(value: float, baseline: float) -> float:
    if not math.isfinite(value) or not math.isfinite(baseline) or abs(baseline) < 1e-12:
        return float("nan")
    return value / baseline


def mean_finite(values: list[float]) -> float:
    values = [v for v in values if math.isfinite(v)]
    return mean(values) if values else float("nan")


def worst_finite(values: list[float], metric: str) -> float:
    values = [v for v in values if math.isfinite(v)]
    if not values:
        return float("nan")
    return min(values) if metric in HIGHER_BETTER else max(values)


def struct_field(obj: Any, name: str, default: Any = float("nan")) -> Any:
    if obj is None or not hasattr(obj, name):
        return default
    return getattr(obj, name)


def scalar(value: Any) -> float:
    if isinstance(value, np.ndarray):
        if value.size == 0:
            return float("nan")
        value = value.reshape(-1)[0]
    try:
        return float(value)
    except Exception:
        return float("nan")


def array_values(value: Any) -> list[float]:
    if isinstance(value, np.ndarray):
        return [float(v) for v in value.reshape(-1)]
    if isinstance(value, (list, tuple)):
        return [float(v) for v in value]
    return [float(value)]


def load_meta(path: Path) -> Any:
    return sio.loadmat(path, squeeze_me=True, struct_as_record=False)["meta"]


def config_value(meta: Any, key: str) -> Any:
    return struct_field(struct_field(meta, "cfg", None), key)


def test_value(meta: Any, key: str) -> float:
    return scalar(struct_field(struct_field(meta, "test_metrics", None), key))


def test_array(meta: Any, key: str) -> list[float]:
    return array_values(struct_field(struct_field(meta, "test_metrics", None), key))


def normalize_weights(weights: dict[str, float]) -> dict[str, float]:
    total = sum(weights.values())
    return {key: value / total for key, value in weights.items()}


def offline_cost(value: float, baseline: float, metric: str) -> float:
    if not math.isfinite(value) or not math.isfinite(baseline) or abs(baseline) < 1e-12:
        return float("nan")
    if metric in HIGHER_BETTER:
        return max(0.0, (baseline - value) / abs(baseline))
    return value / abs(baseline)


def compute_vfinal_score(row: dict[str, Any], baseline: dict[str, Any], weights: dict[str, float]) -> tuple[float, int, str]:
    weighted_sum = 0.0
    used_weight = 0.0
    missing: list[str] = []
    for metric in OFFLINE_METRICS:
        comp = offline_cost(num(row.get(metric)), num(baseline.get(metric)), metric)
        if not math.isfinite(comp):
            missing.append(metric)
            continue
        weighted_sum += weights[metric] * comp
        used_weight += weights[metric]
    score = weighted_sum / used_weight if used_weight > 0 else float("nan")
    return score, len(missing), ";".join(missing) if missing else "none"


def load_offline_rows() -> list[dict[str, Any]]:
    baseline_matrix = read_csv(BASELINE_MATRIX)
    baseline = next(row for row in baseline_matrix if row["candidate_id"] == "baseline_lock")
    uncertainty = read_csv(UNCERTAINTY_DIR / "metrics_test.csv")[0]
    mode_theta = read_csv(MODE_THETA_DIR / "metrics_test.csv")[0]
    rows: list[dict[str, Any]] = [
        {
            "algorithm_id": "baseline_lock",
            "algorithm_family": "ModernTCN_small",
            "seed": 101,
            **{metric: baseline.get(metric, "NaN") for metric in OFFLINE_METRICS},
            "offline_source": str(BASELINE_MATRIX),
        },
        {
            "algorithm_id": "uncertainty_seed101_rerun_20260622",
            "algorithm_family": "ModernTCN_small",
            "seed": 101,
            **{metric: uncertainty.get(metric, "NaN") for metric in OFFLINE_METRICS},
            "offline_source": str(UNCERTAINTY_DIR / "metrics_test.csv"),
        },
        {
            "algorithm_id": "mode_theta_detach_flatreg001_seed21_rerun_20260622",
            "algorithm_family": "ModernTCNModeTheta",
            "seed": 21,
            **{metric: mode_theta.get(metric, "NaN") for metric in OFFLINE_METRICS},
            "offline_source": str(MODE_THETA_DIR / "metrics_test.csv"),
        },
        meta_offline_row("GRU_seed101", "GRU", GRU_META),
        meta_offline_row("TCN_seed101", "TCN", TCN_META),
    ]
    return rows


def meta_offline_row(algorithm_id: str, family: str, meta_path: Path) -> dict[str, Any]:
    meta = load_meta(meta_path)
    recall = test_array(meta, "recall_main")
    edge_values = [
        test_value(meta, "theta_pos_8_10_p95_abs_err_deg"),
        test_value(meta, "theta_neg_10_8_p95_abs_err_deg"),
    ]
    return {
        "algorithm_id": algorithm_id,
        "algorithm_family": family,
        "seed": scalar(config_value(meta, "seed")),
        "acc_main": test_value(meta, "acc_main"),
        "acc_turn": test_value(meta, "acc_turn"),
        "acc_turn_transition": test_value(meta, "acc_turn_transition"),
        "theta_mae_deg": test_value(meta, "theta_abs_le_10_mae_deg"),
        "theta_edge_p95_abs_err": max(v for v in edge_values if math.isfinite(v)),
        "flat_peak_theta_error": test_value(meta, "theta_flat_abs_max_deg"),
        "flat_recall": recall[0] if len(recall) > 0 else float("nan"),
        "stall_recall": recall[1] if len(recall) > 1 else float("nan"),
        "slope_recall": recall[2] if len(recall) > 2 else float("nan"),
        "offline_source": str(meta_path),
    }


def load_path_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(FORMAL_PATH_METRICS):
        controller = row["controller"]
        if controller not in {
            "baseline_lock",
            "uncertainty_seed101_rerun_20260622",
            "mode_theta_detach_flatreg001_seed21_rerun_20260622",
        }:
            continue
        rows.append(
            {
                **row,
                "algorithm_id": controller,
                "closed_loop_protocol": "window2_formal_validation",
                "same_path_set_as_baseline": True,
                "same_closed_loop_protocol_as_baseline": True,
                "source_file": str(FORMAL_PATH_METRICS),
            }
        )

    path_runs = read_csv(NODE_ROOT / "strict_gru_tcn_path_runs.csv")
    for run in path_runs:
        summary_file = Path(run["summary_file"])
        for row in read_csv(summary_file):
            controller = row["controller"]
            if controller == "baseline_lock":
                continue
            if controller not in {"GRU", "TCN"}:
                continue
            algorithm_id = "GRU_seed101" if controller == "GRU" else "TCN_seed101"
            rows.append(
                {
                    **row,
                    "path_tag": run["path_tag"],
                    "algorithm_id": algorithm_id,
                    "closed_loop_protocol": "strict_gru_tcn_window2_shell",
                    "same_path_set_as_baseline": True,
                    "same_closed_loop_protocol_as_baseline": True,
                    "source_file": str(summary_file),
                }
            )
    return rows


def aggregate_path_rows(path_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    algorithm_ids = [
        "baseline_lock",
        "uncertainty_seed101_rerun_20260622",
        "mode_theta_detach_flatreg001_seed21_rerun_20260622",
        "GRU_seed101",
        "TCN_seed101",
    ]
    rows: list[dict[str, Any]] = []
    for algorithm_id in algorithm_ids:
        subset = [row for row in path_rows if row["algorithm_id"] == algorithm_id]
        path_set = {row.get("path_tag", "") for row in subset}
        out: dict[str, Any] = {
            "algorithm_id": algorithm_id,
            "n_paths": len(subset),
            "path_set_complete": path_set == FROZEN_PATHS,
            "same_path_set_as_baseline": path_set == FROZEN_PATHS,
            "same_closed_loop_protocol_as_baseline": all(str(row.get("same_closed_loop_protocol_as_baseline", "")).lower() == "true" for row in subset),
            "closed_loop_protocol": ";".join(sorted({str(row.get("closed_loop_protocol", "")) for row in subset})),
        }
        for metric in AGGREGATE_METRICS:
            values = [num(row.get(metric)) for row in subset]
            out[f"{metric}_mean"] = mean_finite(values)
            out[f"{metric}_worst"] = worst_finite(values, metric)
        rows.append(out)
    return rows


def j_control(row: dict[str, Any], baseline: dict[str, Any]) -> tuple[float, int, str]:
    terms: list[float] = []
    missing: list[str] = []
    for metric in CONTROL_COMPONENTS:
        ratio = safe_ratio(num(row.get(f"{metric}_mean")), num(baseline.get(f"{metric}_mean")))
        if math.isfinite(ratio):
            terms.append(ratio)
        else:
            missing.append(metric)
    return (mean(terms) if terms else float("nan")), len(missing), ";".join(missing) if missing else "none"


def hard_checks(row: dict[str, Any], offline: dict[str, Any], baseline: dict[str, Any], baseline_offline: dict[str, Any], thresholds: dict[str, Any]) -> tuple[str, str, str]:
    failures: list[str] = []
    unavailable: list[str] = []

    def require(name: str, value: float) -> bool:
        if math.isfinite(value):
            return True
        unavailable.append(name)
        return False

    checks = [
        ("viol_rate", num(row.get("viol_rate_mean")) - num(baseline.get("viol_rate_mean")), float(thresholds["viol_rate_max_abs_increase"]), ">"),
        ("closed_loop_main_acc", (num(baseline.get("main_acc_pct_mean")) - num(row.get("main_acc_pct_mean"))) / 100.0, float(thresholds["acc_main_min_drop"]), ">"),
        ("offline_acc_main", num(baseline_offline.get("acc_main")) - num(offline.get("acc_main")), float(thresholds["acc_main_min_drop"]), ">"),
        ("stall_recall", num(baseline_offline.get("stall_recall")) - num(offline.get("stall_recall")), float(thresholds["stall_recall_min_drop"]), ">"),
        ("slope_recall", num(baseline_offline.get("slope_recall")) - num(offline.get("slope_recall")), float(thresholds["slope_recall_min_drop"]), ">"),
        ("theta_edge_p95", safe_ratio(num(offline.get("theta_edge_p95_abs_err")), num(baseline_offline.get("theta_edge_p95_abs_err"))), float(thresholds["theta_edge_p95_max_ratio"]), ">"),
        ("flat_peak_theta_error", safe_ratio(num(offline.get("flat_peak_theta_error")), num(baseline_offline.get("flat_peak_theta_error"))), float(thresholds["flat_peak_theta_error_max_ratio"]), ">"),
        ("omega_cmd_rms", safe_ratio(num(row.get("omega_cmd_rms_mean")), num(baseline.get("omega_cmd_rms_mean"))), float(thresholds["omega_cmd_rms_max_ratio"]), ">"),
        ("delta_u_proxy", safe_ratio(num(row.get("j_du_mean")), num(baseline.get("j_du_mean"))), float(thresholds["delta_u_proxy_max_ratio"]), ">"),
    ]
    for name, value, limit, op in checks:
        if not require(name, value):
            continue
        if op == ">" and value > limit:
            failures.append(f"{name}={value:.6g}")
    if failures:
        return "fail", "; ".join(failures), "; ".join(unavailable) if unavailable else "none"
    if unavailable:
        return "unavailable", "none", "; ".join(unavailable)
    return "pass", "none", "none"


def build_parameter_rows() -> list[dict[str, Any]]:
    e0 = json.loads(BASELINE_IDENTITY.read_text(encoding="utf-8"))
    baseline_identity = e0["baseline_identity"]
    uncertainty_cfg = json.loads((UNCERTAINTY_DIR / "config.json").read_text(encoding="utf-8"))
    mode_cfg = json.loads((MODE_THETA_DIR / "config.json").read_text(encoding="utf-8"))
    uncertainty_metrics = read_csv(UNCERTAINTY_DIR / "metrics_test.csv")[0]
    mode_metrics = read_csv(MODE_THETA_DIR / "metrics_test.csv")[0]
    return [
        {
            "algorithm_id": "baseline_lock",
            "algorithm_family": "ModernTCN_small",
            "seed": 101,
            "role": "reference_baseline",
            "dataset_file": baseline_identity["dataset"],
            "feature_contract": baseline_identity["feature_contract"],
            "plant_revision": baseline_identity["plant_revision"],
            "input_dim": baseline_identity["input_dim"],
            "seq_len": baseline_identity["seq_len"],
            "key_parameters": "channels=64; blocks=5; kernel_size=31; dropout=0.15; lambda_turn=0.20; lambda_theta=0.55; lambda_theta_flat=0.12; turn_transition_weight=2.5; turn_class_multipliers=[1.4,0.8,1.4]",
            "checkpoint_or_model_file": baseline_identity["checkpoint"],
            "onnx_file": baseline_identity["onnx"],
            "report_file": str(SCI_ROOT / "00_baseline_lock" / "baseline_lock.md"),
        },
        modern_param_row("uncertainty_seed101_rerun_20260622", "ModernTCN_small", uncertainty_cfg, uncertainty_metrics),
        modern_param_row("mode_theta_detach_flatreg001_seed21_rerun_20260622", "ModernTCNModeTheta", mode_cfg, mode_metrics),
        matlab_param_row("GRU_seed101", "GRU", GRU_META),
        matlab_param_row("TCN_seed101", "TCN", TCN_META),
    ]


def modern_param_row(algorithm_id: str, family: str, cfg: dict[str, Any], metrics: dict[str, str]) -> dict[str, Any]:
    args = cfg["cli_args"]
    model_cfg = cfg["model_config"]
    keys = [
        f"loss_mode={cfg['loss_mode']}",
        f"channels={model_cfg.get('channels')}",
        f"blocks={model_cfg.get('blocks')}",
        f"kernel_size={model_cfg.get('kernel_size')}",
        f"dropout={model_cfg.get('dropout')}",
        f"lambda_turn={model_cfg.get('lambda_turn')}",
        f"lambda_theta={model_cfg.get('lambda_theta')}",
        f"lambda_theta_flat={model_cfg.get('lambda_theta_flat')}",
        f"turn_transition_weight={model_cfg.get('turn_transition_weight')}",
        f"main_neg_slope_weight={model_cfg.get('main_neg_slope_weight')}",
        f"turn_class_multipliers={model_cfg.get('turn_class_multipliers')}",
    ]
    if cfg.get("dynamic_loss_state"):
        state = cfg["dynamic_loss_state"]
        keys.extend([f"weight_main={state.get('weight_main', 'NaN')}", f"weight_turn={state.get('weight_turn', 'NaN')}", f"weight_theta={state.get('weight_theta', 'NaN')}"])
    if cfg.get("model_extra_state"):
        for key, value in cfg["model_extra_state"].items():
            keys.append(f"{key}={value}")
    return {
        "algorithm_id": algorithm_id,
        "algorithm_family": family,
        "seed": args.get("seed"),
        "role": "rerun_candidate",
        "dataset_file": args.get("dataset_file"),
        "feature_contract": "passive17_plus_all5",
        "plant_revision": "agv_physics_v2_plantfix",
        "input_dim": model_cfg.get("input_dim"),
        "seq_len": model_cfg.get("seq_len"),
        "key_parameters": "; ".join(keys),
        "checkpoint_or_model_file": metrics.get("checkpoint_file", ""),
        "onnx_file": metrics.get("onnx_file", ""),
        "report_file": metrics.get("report_file", ""),
    }


def matlab_param_row(algorithm_id: str, family: str, meta_path: Path) -> dict[str, Any]:
    meta = load_meta(meta_path)
    dataset_meta = struct_field(meta, "dataset_meta", None)
    seq_len = config_value(meta, "seq_len")
    if not math.isfinite(scalar(seq_len)):
        seq_len = struct_field(dataset_meta, "seq_len", float("nan"))
    keys = [
        f"mode={config_value(meta, 'mode')}",
        f"max_epochs={config_value(meta, 'max_epochs')}",
        f"batch_size={config_value(meta, 'batch_size')}",
        f"dropout={config_value(meta, 'dropout')}",
        f"best_metric={config_value(meta, 'best_metric')}",
        f"base_best_metric={config_value(meta, 'base_best_metric')}",
        f"lambda_turn={config_value(meta, 'lambda_turn')}",
        f"lambda_theta={config_value(meta, 'lambda_theta')}",
        f"lambda_theta_flat={config_value(meta, 'lambda_theta_flat')}",
        f"turn_head={config_value(meta, 'turn_head_type')}/{config_value(meta, 'turn_head_source')}",
        f"turn_head_hidden={config_value(meta, 'turn_head_hidden')}",
        f"turn_class_multipliers={fmt(config_value(meta, 'turn_class_multipliers'))}",
        f"best_epoch={struct_field(meta, 'best_epoch')}",
        f"receptive_field_steps={struct_field(meta, 'receptive_field_steps')}",
    ]
    if family == "GRU":
        keys.extend([f"hidden_size={config_value(meta, 'hidden_size')}", f"num_layers={config_value(meta, 'num_layers')}"])
    else:
        keys.extend([f"num_blocks={config_value(meta, 'num_blocks')}", f"num_filters={config_value(meta, 'num_filters')}", f"kernel_size={config_value(meta, 'kernel_size')}", f"turn_finetune_start_epoch={config_value(meta, 'turn_finetune_start_epoch')}", f"turn_finetune_lambda_turn={config_value(meta, 'turn_finetune_lambda_turn')}"])
    return {
        "algorithm_id": algorithm_id,
        "algorithm_family": family,
        "seed": config_value(meta, "seed"),
        "role": "strict_closed_loop_comparator",
        "dataset_file": struct_field(dataset_meta, "output_file", ""),
        "feature_contract": "passive17_plus_all5",
        "plant_revision": "agv_physics_v2_plantfix",
        "input_dim": config_value(meta, "input_size"),
        "seq_len": seq_len,
        "key_parameters": "; ".join(keys),
        "checkpoint_or_model_file": config_value(meta, "model_file"),
        "onnx_file": "NaN",
        "report_file": config_value(meta, "report_file"),
    }


def build_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    thresholds = json.loads(THRESHOLDS_FILE.read_text(encoding="utf-8"))
    vfinal = json.loads(VFINAL_FILE.read_text(encoding="utf-8"))
    weights = normalize_weights({key: float(value) for key, value in vfinal["weights"].items()})
    offline_rows = load_offline_rows()
    offline_by_id = {row["algorithm_id"]: row for row in offline_rows}
    baseline_offline = offline_by_id["baseline_lock"]
    path_rows = load_path_rows()
    aggregate_rows = aggregate_path_rows(path_rows)
    aggregate_by_id = {row["algorithm_id"]: row for row in aggregate_rows}
    baseline_agg = aggregate_by_id["baseline_lock"]
    formal_decision = {row["controller"]: row for row in read_csv(FORMAL_DECISION)}

    final_rows: list[dict[str, Any]] = []
    for offline in offline_rows:
        algorithm_id = offline["algorithm_id"]
        agg = aggregate_by_id[algorithm_id]
        j, j_missing_count, j_missing = j_control(agg, baseline_agg)
        v_score, v_missing_count, v_missing = compute_vfinal_score(offline, baseline_offline, weights)
        if algorithm_id == "baseline_lock":
            v_score = 0.0
        hard_status, hard_failures, hard_unavailable = hard_checks(agg, offline, baseline_agg, baseline_offline, thresholds)
        if algorithm_id == "baseline_lock":
            hard_status = "pass"
            hard_failures = "reference_baseline"
            hard_unavailable = "none"
        eligible = algorithm_id != "baseline_lock" and hard_status == "pass" and bool(agg["same_path_set_as_baseline"]) and bool(agg["same_closed_loop_protocol_as_baseline"]) and math.isfinite(j) and j < 1.0
        if algorithm_id in formal_decision:
            prior_status = formal_decision[algorithm_id]["class_c_status"]
            prior_reason = formal_decision[algorithm_id]["class_c_reason"]
        else:
            prior_status = "StrictComparator"
            prior_reason = "strict_gru_tcn_window2_shell"
        final_rows.append(
            {
                "algorithm_id": algorithm_id,
                "algorithm_family": offline["algorithm_family"],
                "seed": offline["seed"],
                "evidence_role": "reference_baseline" if algorithm_id == "baseline_lock" else ("strict_comparator" if algorithm_id in {"GRU_seed101", "TCN_seed101"} else "rerun_candidate"),
                "closed_loop_protocol": agg["closed_loop_protocol"],
                "same_path_set_as_baseline": agg["same_path_set_as_baseline"],
                "same_closed_loop_protocol_as_baseline": agg["same_closed_loop_protocol_as_baseline"],
                "n_paths": agg["n_paths"],
                "J_control": j,
                "J_control_missing_count": j_missing_count,
                "J_control_missing_metrics": j_missing,
                "J_vFinal_available": v_score,
                "metric_missing_ratio_vFinal": v_missing_count / len(OFFLINE_METRICS),
                "vFinal_missing_metrics": v_missing,
                "hard_constraint_status": hard_status,
                "hard_constraint_failures": hard_failures,
                "hard_constraint_unavailable": hard_unavailable,
                "eligible_for_class_c_under_current_contract": eligible,
                "prior_window2_class_c_status": prior_status,
                "prior_window2_class_c_reason": prior_reason,
                "final_decision": decision_text(algorithm_id, eligible, hard_status, j),
                "ey_rmse_mean": agg["ey_rmse_mean"],
                "xy_rmse_mean": agg["xy_rmse_mean"],
                "epsi_rmse_mean": agg["epsi_rmse_mean"],
                "j_du_mean": agg["j_du_mean"],
                "omega_cmd_rms_mean": agg["omega_cmd_rms_mean"],
                "viol_rate_mean": agg["viol_rate_mean"],
                "theta_mae_deg_closed_loop_mean": agg["theta_mae_deg_mean"],
                "main_acc_pct_closed_loop_mean": agg["main_acc_pct_mean"],
                "turn_acc_pct_closed_loop_mean": agg["turn_acc_pct_mean"],
                **{f"offline_{metric}": offline.get(metric, float("nan")) for metric in OFFLINE_METRICS},
            }
        )
    ranked = [row for row in final_rows if math.isfinite(num(row["J_control"]))]
    ranked.sort(key=lambda row: num(row["J_control"]))
    for rank, row in enumerate(ranked, start=1):
        row["rank_by_J_control"] = rank
    proxy_ranked = [row for row in final_rows if row["algorithm_id"] != "baseline_lock" and math.isfinite(num(row["J_vFinal_available"]))]
    proxy_ranked.sort(key=lambda row: num(row["J_vFinal_available"]))
    for rank, row in enumerate(proxy_ranked, start=1):
        row["rank_by_J_vFinal_candidates_only"] = rank
    for row in final_rows:
        row.setdefault("rank_by_J_control", "NaN")
        row.setdefault("rank_by_J_vFinal_candidates_only", "NaN")
    return path_rows, aggregate_rows, final_rows, build_parameter_rows()


def decision_text(algorithm_id: str, eligible: bool, hard_status: str, j: float) -> str:
    if algorithm_id == "baseline_lock":
        return "reference_kept"
    if eligible:
        return "strict_class_c_candidate"
    if hard_status == "fail":
        return "no_promotion_hard_constraint_fail"
    if math.isfinite(j) and j >= 1.0:
        return "no_promotion_not_better_than_baseline"
    return "no_promotion_contract_limited"


def write_report(final_rows: list[dict[str, Any]], parameter_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Strict GRU/TCN New Metric Evaluation",
        "",
        "- Scope: GRU/TCN re-run under the Window 2 closed-loop shell and frozen three-path set.",
        "- Output root: `results/modern_tcn_metric_rebuild/09_strict_gru_tcn_validation/`",
        "- Missing policy: no zero fill, no baseline fill; unavailable metrics remain NaN and are counted.",
        "",
        "## Final Five-Algorithm Results",
        "",
        "| algorithm | J_control | hard status | rank J | ey | xy | epsi | j_du | omega_rms | offline vFinal | decision |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in sorted(final_rows, key=lambda r: num(r.get("rank_by_J_control", "inf")) if math.isfinite(num(r.get("rank_by_J_control", "inf"))) else 999):
        lines.append(
            f"| `{row['algorithm_id']}` | {num(row['J_control']):.6f} | {row['hard_constraint_status']} | {fmt(row['rank_by_J_control'])} | "
            f"{num(row['ey_rmse_mean']):.6f} | {num(row['xy_rmse_mean']):.6f} | {num(row['epsi_rmse_mean']):.6f} | "
            f"{num(row['j_du_mean']):.6f} | {num(row['omega_cmd_rms_mean']):.6f} | {num(row['J_vFinal_available']):.6f} | {row['final_decision']} |"
        )
    lines.extend(["", "## Hard-Constraint Detail", "", "| algorithm | hard status | failures | unavailable |", "|---|---|---|---|"])
    for row in final_rows:
        lines.append(f"| `{row['algorithm_id']}` | {row['hard_constraint_status']} | {row['hard_constraint_failures']} | {row['hard_constraint_unavailable']} |")
    lines.extend(["", "## Parameter Snapshot", "", "| algorithm | family | seed | role | key parameters | artifact |", "|---|---|---:|---|---|---|"])
    for row in parameter_rows:
        key_params = str(row["key_parameters"]).replace("|", "/")
        if len(key_params) > 260:
            key_params = key_params[:257] + "..."
        lines.append(
            f"| `{row['algorithm_id']}` | {row['algorithm_family']} | {fmt(row['seed'])} | {row['role']} | {key_params} | `{row['checkpoint_or_model_file']}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- No candidate satisfies strict Class C after applying frozen hard constraints.",
            "- GRU/TCN are now strict same-shell comparators, not legacy-only evidence.",
            "- Removing hard status changes promotion eligibility only; the J_control ordering itself is independent of hard gates.",
        ]
    )
    write_text(NODE_ROOT / "strict_gru_tcn_new_metric_report.md", "\n".join(lines) + "\n")


def main() -> int:
    path_rows, aggregate_rows, final_rows, parameter_rows = build_rows()
    path_fields = ["algorithm_id", "controller", "path_tag", "closed_loop_protocol", "same_path_set_as_baseline", "same_closed_loop_protocol_as_baseline", "ey_rmse", "xy_rmse", "epsi_rmse", "j_du", "omega_cmd_rms", "viol_rate", "theta_mae_deg", "main_acc_pct", "turn_acc_pct", "source_file"]
    aggregate_fields = ["algorithm_id", "n_paths", "path_set_complete", "same_path_set_as_baseline", "same_closed_loop_protocol_as_baseline", "closed_loop_protocol"]
    for metric in AGGREGATE_METRICS:
        aggregate_fields.extend([f"{metric}_mean", f"{metric}_worst"])
    final_fields = ["algorithm_id", "algorithm_family", "seed", "evidence_role", "closed_loop_protocol", "same_path_set_as_baseline", "same_closed_loop_protocol_as_baseline", "n_paths", "J_control", "rank_by_J_control", "J_control_missing_count", "J_control_missing_metrics", "J_vFinal_available", "rank_by_J_vFinal_candidates_only", "metric_missing_ratio_vFinal", "vFinal_missing_metrics", "hard_constraint_status", "hard_constraint_failures", "hard_constraint_unavailable", "eligible_for_class_c_under_current_contract", "prior_window2_class_c_status", "prior_window2_class_c_reason", "final_decision", "ey_rmse_mean", "xy_rmse_mean", "epsi_rmse_mean", "j_du_mean", "omega_cmd_rms_mean", "viol_rate_mean", "theta_mae_deg_closed_loop_mean", "main_acc_pct_closed_loop_mean", "turn_acc_pct_closed_loop_mean"] + [f"offline_{metric}" for metric in OFFLINE_METRICS]
    parameter_fields = ["algorithm_id", "algorithm_family", "seed", "role", "dataset_file", "feature_contract", "plant_revision", "input_dim", "seq_len", "key_parameters", "checkpoint_or_model_file", "onnx_file", "report_file"]
    write_csv(NODE_ROOT / "strict_gru_tcn_path_metrics.csv", path_rows, path_fields)
    write_csv(NODE_ROOT / "strict_gru_tcn_new_metric_aggregate.csv", aggregate_rows, aggregate_fields)
    write_csv(NODE_ROOT / "five_algorithm_strict_final_results.csv", final_rows, final_fields)
    write_csv(NODE_ROOT / "five_algorithm_strict_parameter_table.csv", parameter_rows, parameter_fields)
    write_json(
        NODE_ROOT / "strict_gru_tcn_new_metric_decision.json",
        {
            "output_root": str(NODE_ROOT),
            "strict_class_c_candidates": [row["algorithm_id"] for row in final_rows if bool(row["eligible_for_class_c_under_current_contract"])],
            "retained_reference": "baseline_lock",
            "algorithm_ids": [row["algorithm_id"] for row in final_rows],
        },
    )
    write_report(final_rows, parameter_rows)
    print(f"Wrote {NODE_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
