from __future__ import annotations

import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent.parent
NODE_ROOT = ROOT / "13_multiseed_algorithm_comparison"
INV_DIR = NODE_ROOT / "00_evidence_inventory"
OFFLINE_DIR = NODE_ROOT / "01_offline_v2"
CLOSED_DIR = NODE_ROOT / "02_closed_loop_v2"
REPORT_DIR = NODE_ROOT / "03_report"

BASELINE_MATRIX = ROOT / "03_rerank_existing_experiments" / "candidate_metric_matrix.csv"
V2_FULL = ROOT / "10_threshold_recalibration" / "hard_constraint_thresholds_v2_full_proposed.json"
V2_CLOSED = ROOT / "10_threshold_recalibration" / "hard_constraint_thresholds_v2_closed_loop_proposed.json"
UNCERTAINTY_OFFLINE = (
    ROOT
    / "12_uncertainty_replacement_qualification"
    / "02_offline_multiseed"
    / "same_recipe_offline_multiseed.csv"
)
UNCERTAINTY_CLOSED = (
    ROOT
    / "12_uncertainty_replacement_qualification"
    / "03_closed_loop_representatives"
    / "closed_loop_replacement_results.csv"
)
STRICT_CLOSED = (
    ROOT
    / "09_strict_gru_tcn_validation"
    / "strict_gru_tcn_new_metric_aggregate.csv"
)
MODERN_MULTI_CLOSED_SUMMARY = (
    PROJECT_ROOT
    / "results"
    / "paper"
    / "agv_model_parameter_correction_workflow"
    / "09_closed_loop"
    / "modern_multiseed_l020_tt25_full"
    / "modern_multiseed_summary.csv"
)
MODERN_MODEL_ROOT = (
    PROJECT_ROOT
    / "results"
    / "paper"
    / "agv_model_parameter_correction_workflow"
    / "08_models"
    / "modern_tcn"
)
GRU_LOG_ROOT = (
    PROJECT_ROOT
    / "results"
    / "paper"
    / "agv_model_parameter_correction_workflow"
    / "08_models"
    / "matlab_logs"
)
LEGACY_GRU_THETA10 = (
    PROJECT_ROOT
    / "results"
    / "gru"
    / "train_logs_theta10_uniform_h0_v2"
    / "GRU_theta10_v2_multi_seed_summary.csv"
)

MODERN_BASE_SEEDS = [21, 73, 101]
GRU_PLANTFIX_SEEDS = [21, 73, 101]
UNCERTAINTY_SEEDS = [21, 42, 101]
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
HARD_METRICS = [
    "acc_main",
    "stall_recall",
    "slope_recall",
    "theta_edge_p95_abs_err",
    "flat_peak_theta_error",
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
    if not text or text.lower() in {"nan", "none", "unavailable", "missing"}:
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
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def first_row(path: Path) -> dict[str, str]:
    rows = read_csv(path)
    if not rows:
        raise RuntimeError(f"empty csv: {path}")
    return rows[0]


def baseline_metrics() -> dict[str, float]:
    rows = read_csv(BASELINE_MATRIX)
    for row in rows:
        if row.get("candidate_id") == "baseline_lock":
            return {key: num(value) for key, value in row.items()}
    raise RuntimeError("baseline_lock not found in candidate metric matrix")


def modern_summary_path(seed: int, variant: str) -> Path:
    if variant == "base":
        folder = f"modern_tcn_v5_plantfix_passive17_plus_all5_seed{seed}"
    elif variant == "champion":
        folder = "modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101"
    else:
        raise ValueError(variant)
    return MODERN_MODEL_ROOT / folder / f"modern_tcn_seed{seed}_summary.csv"


def modern_report_path(seed: int, variant: str) -> Path:
    return modern_summary_path(seed, variant).with_name("ModernTCN_train_report.md")


def modern_metrics_from_summary(path: Path) -> dict[str, Any]:
    row = first_row(path)
    edge = max(num(row.get("theta_pos_8_10_p95_abs_err_deg")), num(row.get("theta_neg_10_8_p95_abs_err_deg")))
    return {
        "seed": int(num(row.get("seed"))),
        "best_epoch": num(row.get("best_epoch")),
        "acc_main": num(row.get("acc_main")),
        "acc_turn": num(row.get("acc_turn")),
        "acc_turn_transition": num(row.get("acc_turn_transition")),
        "theta_mae_deg": num(row.get("theta_mae_deg")),
        "theta_edge_p95_abs_err": edge,
        "flat_peak_theta_error": num(row.get("theta_flat_abs_max_deg")),
        "flat_recall": num(row.get("flat_recall")),
        "stall_recall": num(row.get("stall_recall")),
        "slope_recall": num(row.get("slope_recall")),
        "checkpoint_file": row.get("checkpoint_file", ""),
        "report_file": row.get("report_file", ""),
    }


def parse_json_block(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, flags=re.S)
    if not match:
        return {}
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return {}


def extract_report_value(text: str, label: str) -> float:
    pattern = rf"\|\s*{re.escape(label)}\s*\|\s*([-+0-9.eE]+)\s*\|"
    match = re.search(pattern, text)
    return num(match.group(1)) if match else math.nan


def parse_confusion_recall(text: str, name: str) -> float:
    pattern = rf"\|\s*{re.escape(name)}\s*\|\s*\d+\s*\|\s*\d+\s*\|\s*\d+\s*\|\s*([-+0-9.eE]+)\s*\|"
    match = re.search(pattern, text)
    return num(match.group(1)) if match else math.nan


def parse_gru_report(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    seed_match = re.search(r"seed(\d+)", str(path))
    model_match = re.search(r"- 模型文件:\s*`([^`]+)`", text)
    dataset_match = re.search(r"- 数据集:\s*`([^`]+)`", text)
    edge = max(extract_report_value(text, "[-10,-8] P95 deg"), extract_report_value(text, "[8,10] P95 deg"))
    return {
        "seed": int(seed_match.group(1)) if seed_match else "",
        "best_epoch": extract_report_value(text, "最佳轮次"),
        "acc_main": extract_report_value(text, "主工况准确率"),
        "acc_turn": extract_report_value(text, "转弯准确率"),
        "acc_turn_transition": extract_report_value(text, "转弯过渡窗口准确率"),
        "theta_mae_deg": extract_report_value(text, "坡度 MAE deg"),
        "theta_edge_p95_abs_err": edge,
        "flat_peak_theta_error": math.nan,
        "flat_recall": parse_confusion_recall(text, "flat"),
        "stall_recall": parse_confusion_recall(text, "stall"),
        "slope_recall": parse_confusion_recall(text, "slope"),
        "checkpoint_file": model_match.group(1) if model_match else "",
        "dataset_file": dataset_match.group(1) if dataset_match else "",
        "report_file": str(path),
    }


def offline_hard_gate(metrics: dict[str, Any], baseline: dict[str, float], thresholds: dict[str, Any]) -> tuple[str, str, str]:
    failures: list[str] = []
    missing: list[str] = []

    checks = [
        ("acc_main", "min_drop", thresholds["acc_main_min_drop"]),
        ("stall_recall", "min_drop", thresholds["stall_recall_min_drop"]),
        ("slope_recall", "min_drop", thresholds["slope_recall_min_drop"]),
        ("theta_edge_p95_abs_err", "max_ratio", thresholds["theta_edge_p95_max_ratio"]),
        ("flat_peak_theta_error", "max_ratio", thresholds["flat_peak_theta_error_max_ratio"]),
    ]
    for metric, mode, threshold in checks:
        value = num(metrics.get(metric))
        base = num(baseline.get(metric))
        if math.isnan(value) or math.isnan(base):
            missing.append(metric)
            continue
        if mode == "min_drop":
            drop = base - value
            if drop > threshold + 1e-12:
                failures.append(f"{metric}_drop={drop:.6g}>{threshold:.6g}")
        elif mode == "max_ratio":
            ratio = value / base if base else math.inf
            if ratio > threshold + 1e-12:
                failures.append(f"{metric}_ratio={ratio:.6g}>{threshold:.6g}")

    if failures:
        status = "fail"
    elif missing:
        status = "unavailable"
    else:
        status = "pass"
    return status, ";".join(failures) if failures else "none", ";".join(missing) if missing else "none"


def offline_score(metrics: dict[str, Any], baseline: dict[str, float]) -> float:
    ratios: list[float] = []
    for metric in OFFLINE_METRICS:
        value = num(metrics.get(metric))
        base = num(baseline.get(metric))
        if math.isnan(value) or math.isnan(base) or base == 0:
            continue
        if metric in HIGHER_BETTER:
            if value <= 0:
                continue
            ratios.append(base / value)
        else:
            ratios.append(value / base)
    return mean(ratios) if ratios else math.nan


def metric_missing_ratio(metrics: dict[str, Any]) -> float:
    missing = sum(1 for metric in OFFLINE_METRICS if math.isnan(num(metrics.get(metric))))
    return missing / len(OFFLINE_METRICS)


def make_offline_row(
    algorithm_group: str,
    variant_id: str,
    source_contract: str,
    evidence_level: str,
    metrics: dict[str, Any],
    source_file: Path,
    baseline: dict[str, float],
    thresholds: dict[str, Any],
    is_reference_baseline: bool = False,
    notes: str = "",
) -> dict[str, Any]:
    status, failures, missing = offline_hard_gate(metrics, baseline, thresholds)
    if is_reference_baseline:
        status, failures, missing = "pass", "reference", "none"
    official = evidence_level == "current_contract_complete" and status != "unavailable"
    return {
        "algorithm_group": algorithm_group,
        "variant_id": variant_id,
        "seed": metrics.get("seed"),
        "source_contract": source_contract,
        "evidence_level": evidence_level,
        "is_reference_baseline": is_reference_baseline,
        "official_offline_comparison_eligible": official,
        "offline_v2_status": status,
        "hard_gate_failures": failures,
        "hard_gate_unavailable": missing,
        "offline_score_vs_baseline": offline_score(metrics, baseline),
        "metric_missing_ratio": metric_missing_ratio(metrics),
        "best_epoch": metrics.get("best_epoch"),
        "acc_main": metrics.get("acc_main"),
        "acc_turn": metrics.get("acc_turn"),
        "acc_turn_transition": metrics.get("acc_turn_transition"),
        "theta_mae_deg": metrics.get("theta_mae_deg"),
        "theta_edge_p95_abs_err": metrics.get("theta_edge_p95_abs_err"),
        "flat_peak_theta_error": metrics.get("flat_peak_theta_error"),
        "flat_recall": metrics.get("flat_recall"),
        "stall_recall": metrics.get("stall_recall"),
        "slope_recall": metrics.get("slope_recall"),
        "checkpoint_file": metrics.get("checkpoint_file", ""),
        "report_file": metrics.get("report_file", ""),
        "source_file": str(source_file),
        "notes": notes,
    }


def collect_offline_rows(baseline: dict[str, float], thresholds: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for seed in MODERN_BASE_SEEDS:
        source = modern_summary_path(seed, "base")
        metrics = modern_metrics_from_summary(source)
        rows.append(
            make_offline_row(
                "ModernTCN_small_base",
                f"plantfix_passive17_plus_all5_seed{seed}",
                "plantfix_passive17_plus_all5",
                "current_contract_complete",
                metrics,
                source,
                baseline,
                thresholds,
                notes="原始 ModernTCN_small 多 seed 训练历史；不是当前 frozen champion。",
            )
        )

    champion_source = modern_summary_path(101, "champion")
    champion_metrics = modern_metrics_from_summary(champion_source)
    rows.append(
        make_offline_row(
            "ModernTCN_small_champion_baseline",
            "turn_l020_tt25_tcm14_stw055_slrw060_seed101",
            "plantfix_passive17_plus_all5_turn_champion",
            "current_contract_complete",
            champion_metrics,
            champion_source,
            baseline,
            thresholds,
            is_reference_baseline=True,
            notes="当前 baseline_lock / frozen ModernTCN_small champion。",
        )
    )

    for row in read_csv(UNCERTAINTY_OFFLINE):
        metrics = {
            "seed": int(num(row["seed"])),
            "best_epoch": math.nan,
            "acc_main": num(row.get("acc_main")),
            "acc_turn": num(row.get("acc_turn")),
            "acc_turn_transition": num(row.get("acc_turn_transition")),
            "theta_mae_deg": num(row.get("theta_mae_deg")),
            "theta_edge_p95_abs_err": num(row.get("theta_edge_p95_abs_err")),
            "flat_peak_theta_error": num(row.get("flat_peak_theta_error")),
            "flat_recall": num(row.get("flat_recall")),
            "stall_recall": num(row.get("stall_recall")),
            "slope_recall": num(row.get("slope_recall")),
            "checkpoint_file": row.get("checkpoint_file", ""),
            "report_file": "",
        }
        rows.append(
            make_offline_row(
                "Uncertainty_weighted_ModernTCN_small",
                row.get("run_tag", f"seed{row.get('seed')}"),
                "plantfix_passive17_plus_all5_uncertainty_same_recipe",
                "current_contract_complete",
                metrics,
                Path(row.get("source", UNCERTAINTY_OFFLINE)),
                baseline,
                thresholds,
                notes="uncertainty weighting 同配方复验；seed21/42 是 replacement qualification 节点补训。",
            )
        )

    for seed in GRU_PLANTFIX_SEEDS:
        report = GRU_LOG_ROOT / f"full_gru_v5_plantfix_passive17_plus_all5_seed{seed}" / "GRU_train_report.md"
        metrics = parse_gru_report(report)
        rows.append(
            make_offline_row(
                "GRU_plantfix",
                f"full_gru_v5_plantfix_passive17_plus_all5_seed{seed}",
                "plantfix_passive17_plus_all5",
                "current_contract_limited",
                metrics,
                report,
                baseline,
                thresholds,
                notes="同 plantfix 数据契约，但训练报告缺少 flat_peak_theta_error，不能正式判定 full offline pass。",
            )
        )
    return rows


def summarise_offline(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["algorithm_group"] == "ModernTCN_small_champion_baseline":
            continue
        grouped[row["algorithm_group"]].append(row)

    summaries: list[dict[str, Any]] = []
    for group, group_rows in grouped.items():
        scores = [num(row["offline_score_vs_baseline"]) for row in group_rows if not math.isnan(num(row["offline_score_vs_baseline"]))]
        pass_rows = [row for row in group_rows if row["offline_v2_status"] == "pass"]
        fail_rows = [row for row in group_rows if row["offline_v2_status"] == "fail"]
        unavailable_rows = [row for row in group_rows if row["offline_v2_status"] == "unavailable"]
        best = min(group_rows, key=lambda row: num(row["offline_score_vs_baseline"]) if not math.isnan(num(row["offline_score_vs_baseline"])) else math.inf)
        summaries.append(
            {
                "algorithm_group": group,
                "seeds_available": "/".join(str(row["seed"]) for row in group_rows),
                "n_seeds": len(group_rows),
                "offline_pass_count": len(pass_rows),
                "offline_fail_count": len(fail_rows),
                "offline_unavailable_count": len(unavailable_rows),
                "best_seed_by_offline_score": best["seed"],
                "best_variant_id": best["variant_id"],
                "best_offline_score_vs_baseline": best["offline_score_vs_baseline"],
                "median_offline_score_vs_baseline": median(scores) if scores else math.nan,
                "status_summary": f"pass={len(pass_rows)}, fail={len(fail_rows)}, unavailable={len(unavailable_rows)}",
            }
        )
    return sorted(summaries, key=lambda row: num(row["best_offline_score_vs_baseline"]))


def closed_loop_score(row: dict[str, Any], baseline: dict[str, Any]) -> float:
    ratios: list[float] = []
    for metric in CONTROL_COMPONENTS:
        value = num(row.get(metric)) if metric in row else num(row.get(f"{metric}_mean"))
        base = num(baseline.get(metric)) if metric in baseline else num(baseline.get(f"{metric}_mean"))
        if not math.isnan(value) and not math.isnan(base) and base != 0:
            ratios.append(value / base)
    return mean(ratios) if ratios else math.nan


def closed_loop_status(row: dict[str, Any], baseline: dict[str, Any], thresholds: dict[str, Any]) -> tuple[str, str]:
    failures: list[str] = []
    viol = num(row.get("viol_rate_mean"))
    base_viol = num(baseline.get("viol_rate_mean"))
    if not math.isnan(viol) and not math.isnan(base_viol):
        if viol - base_viol > thresholds["viol_rate_max_abs_increase"] + 1e-12:
            failures.append(f"viol_rate_abs_increase={viol - base_viol:.6g}>{thresholds['viol_rate_max_abs_increase']:.6g}")
    for metric, threshold_key in [("omega_cmd_rms_mean", "omega_cmd_rms_max_ratio"), ("j_du_mean", "delta_u_proxy_max_ratio")]:
        value = num(row.get(metric))
        base = num(baseline.get(metric))
        if not math.isnan(value) and not math.isnan(base) and base != 0:
            ratio = value / base
            if ratio > thresholds[threshold_key] + 1e-12:
                failures.append(f"{metric}_ratio={ratio:.6g}>{thresholds[threshold_key]:.6g}")
    main = num(row.get("main_acc_pct_mean"))
    base_main = num(baseline.get("main_acc_pct_mean"))
    if not math.isnan(main) and not math.isnan(base_main):
        drop = (base_main - main) / 100.0
        if drop > thresholds["acc_main_min_drop"] + 1e-12:
            failures.append(f"main_acc_drop={drop:.6g}>{thresholds['acc_main_min_drop']:.6g}")
    slope = num(row.get("slope_recall_pct_mean"))
    base_slope = num(baseline.get("slope_recall_pct_mean"))
    if not math.isnan(slope) and not math.isnan(base_slope):
        drop = (base_slope - slope) / 100.0
        if drop > thresholds["slope_recall_min_drop"] + 1e-12:
            failures.append(f"slope_recall_drop={drop:.6g}>{thresholds['slope_recall_min_drop']:.6g}")
    return ("fail" if failures else "pass"), ";".join(failures) if failures else "none"


def collect_current_closed_loop(thresholds: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    uncertainty_rows = read_csv(UNCERTAINTY_CLOSED)
    repl_by_id = {row["candidate_id"]: row for row in uncertainty_rows}
    baseline_repl = repl_by_id["baseline_lock"]
    for candidate_id, group, variant, seed in [
        ("baseline_lock", "ModernTCN_small_champion_baseline", "turn_l020_tt25_tcm14_stw055_slrw060_seed101", 101),
        ("uncertainty_seed101_rerun_20260622", "Uncertainty_weighted_ModernTCN_small", "uncertainty_seed101_rerun_20260622", 101),
        ("ua_seed21", "Uncertainty_weighted_ModernTCN_small", "uncertainty_anchor_same_recipe_seed21", 21),
        ("ua_seed42", "Uncertainty_weighted_ModernTCN_small", "uncertainty_anchor_same_recipe_seed42", 42),
    ]:
        src = repl_by_id[candidate_id]
        rows.append(
            {
                "algorithm_group": group,
                "variant_id": variant,
                "seed": seed,
                "closed_loop_evidence_level": "current_v2_three_path",
                "n_paths": num(src.get("n_paths")),
                "J_control_current_v2": num(src.get("J_control")),
                "closed_loop_v2_status": src.get("closed_loop_v2_status"),
                "closed_loop_v2_failures": src.get("closed_loop_v2_failures"),
                "ey_rmse_mean": num(src.get("ey_rmse_mean")),
                "xy_rmse_mean": num(src.get("xy_rmse_mean")),
                "epsi_rmse_mean": num(src.get("epsi_rmse_mean")),
                "j_du_mean": num(src.get("j_du_mean")),
                "omega_cmd_rms_mean": num(src.get("omega_cmd_rms_mean")),
                "theta_mae_deg_mean": num(src.get("theta_mae_deg_mean")),
                "main_acc_pct_mean": num(src.get("main_acc_pct_mean")),
                "turn_acc_pct_mean": num(src.get("turn_acc_pct_mean")),
                "source_file": str(UNCERTAINTY_CLOSED),
                "notes": "当前 v2 replacement qualification 三路径闭环结果。",
            }
        )

    strict_rows = read_csv(STRICT_CLOSED)
    strict_by_id = {row["algorithm_id"]: row for row in strict_rows}
    strict_baseline = strict_by_id["baseline_lock"]
    if "GRU_seed101" in strict_by_id:
        gru = strict_by_id["GRU_seed101"]
        status, failures = closed_loop_status(gru, strict_baseline, thresholds)
        rows.append(
            {
                "algorithm_group": "GRU_plantfix",
                "variant_id": "full_gru_v5_plantfix_passive17_plus_all5_seed101",
                "seed": 101,
                "closed_loop_evidence_level": "current_v2_three_path",
                "n_paths": num(gru.get("n_paths")),
                "J_control_current_v2": closed_loop_score(gru, strict_baseline),
                "closed_loop_v2_status": status,
                "closed_loop_v2_failures": failures,
                "ey_rmse_mean": num(gru.get("ey_rmse_mean")),
                "xy_rmse_mean": num(gru.get("xy_rmse_mean")),
                "epsi_rmse_mean": num(gru.get("epsi_rmse_mean")),
                "j_du_mean": num(gru.get("j_du_mean")),
                "omega_cmd_rms_mean": num(gru.get("omega_cmd_rms_mean")),
                "theta_mae_deg_mean": num(gru.get("theta_mae_deg_mean")),
                "main_acc_pct_mean": num(gru.get("main_acc_pct_mean")),
                "turn_acc_pct_mean": num(gru.get("turn_acc_pct_mean")),
                "source_file": str(STRICT_CLOSED),
                "notes": "严格 GRU/TCN 三路径闭环节点已有 seed101；未发现同 contract 的 seed21/73 闭环。",
            }
        )
    return sorted(rows, key=lambda row: num(row["J_control_current_v2"]))


def collect_historical_modern_closed_loop() -> list[dict[str, Any]]:
    if not MODERN_MULTI_CLOSED_SUMMARY.exists():
        return []
    path_rows = read_csv(MODERN_MULTI_CLOSED_SUMMARY)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in path_rows:
        grouped[row["controller"]].append(row)
    if "ModernTCN_turn_seed101_champion" not in grouped:
        return []

    def aggregate(rows: list[dict[str, str]]) -> dict[str, Any]:
        return {
            "ey_rmse": mean(num(row["ey_rmse"]) for row in rows),
            "xy_rmse": mean(num(row["xy_rmse"]) for row in rows),
            "epsi_rmse": mean(num(row["epsi_rmse"]) for row in rows),
            "j_du": mean(num(row["j_du"]) for row in rows),
            "omega_cmd_rms": mean(num(row["omega_cmd_rms"]) for row in rows),
            "theta_mae_deg": mean(num(row["theta_mae_deg"]) for row in rows),
            "main_acc_pct": mean(num(row["main_acc_pct"]) for row in rows),
            "turn_acc_pct": mean(num(row["turn_acc_pct"]) for row in rows),
        }

    reference = aggregate(grouped["ModernTCN_turn_seed101_champion"])
    out: list[dict[str, Any]] = []
    for controller, rows in grouped.items():
        agg = aggregate(rows)
        seed_match = re.search(r"seed(\d+)", controller)
        seed = int(seed_match.group(1)) if seed_match else ""
        ratios = [agg[metric] / reference[metric] for metric in CONTROL_COMPONENTS if reference[metric] != 0]
        out.append(
            {
                "controller": controller,
                "seed": seed,
                "n_paths": len(rows),
                "J_control_vs_historical_champion": mean(ratios),
                "ey_rmse_mean": agg["ey_rmse"],
                "xy_rmse_mean": agg["xy_rmse"],
                "epsi_rmse_mean": agg["epsi_rmse"],
                "j_du_mean": agg["j_du"],
                "omega_cmd_rms_mean": agg["omega_cmd_rms"],
                "theta_mae_deg_mean": agg["theta_mae_deg"],
                "main_acc_pct_mean": agg["main_acc_pct"],
                "turn_acc_pct_mean": agg["turn_acc_pct"],
                "source_file": str(MODERN_MULTI_CLOSED_SUMMARY),
                "notes": "历史 ModernTCN turn champion 多 seed 闭环；以同文件 seed101 champion 为本地 reference，不与 current_v2 J_control 混排。",
            }
        )
    return sorted(out, key=lambda row: num(row["J_control_vs_historical_champion"]))


def build_legacy_gru_excluded() -> list[dict[str, Any]]:
    if not LEGACY_GRU_THETA10.exists():
        return []
    rows: list[dict[str, Any]] = []
    for row in read_csv(LEGACY_GRU_THETA10):
        seed = int(num(row.get("seed")))
        if seed not in {21, 42, 73, 101}:
            continue
        rows.append(
            {
                "algorithm_group": "GRU_theta10_v2_legacy",
                "case_name": row.get("case_name"),
                "seed": seed,
                "acc_main": num(row.get("acc_main")),
                "acc_turn": num(row.get("acc_turn")),
                "theta_mae_deg": num(row.get("theta_mae_deg")),
                "theta_edge_p95_abs_err": max(num(row.get("theta_neg_10_8_p95_abs_err_deg")), num(row.get("theta_pos_8_10_p95_abs_err_deg"))),
                "flat_recall": num(row.get("flat_recall")),
                "stall_recall": num(row.get("stall_recall")),
                "slope_recall": num(row.get("slope_recall")),
                "model_file": row.get("model_file"),
                "report_file": row.get("report_file"),
                "official_use": "excluded_old_contract",
                "exclude_reason": "theta10_uniform_h0_v2 / old model path; not the current plantfix passive17_plus_all5 contract.",
                "source_file": str(LEGACY_GRU_THETA10),
            }
        )
    return rows


def build_parameter_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for group, variant, seed, report in [
        (
            "ModernTCN_small_base",
            "plantfix_passive17_plus_all5_seed101",
            101,
            modern_report_path(101, "base"),
        ),
        (
            "ModernTCN_small_champion_baseline",
            "turn_l020_tt25_tcm14_stw055_slrw060_seed101",
            101,
            modern_report_path(101, "champion"),
        ),
    ]:
        cfg = parse_json_block(report)
        text = report.read_text(encoding="utf-8", errors="ignore") if report.exists() else ""
        dataset_match = re.search(r"- dataset:\s*`([^`]+)`", text)
        rows.append(
            {
                "algorithm_group": group,
                "variant_id": variant,
                "seed": seed,
                "model_family": "small",
                "loss_mode": "standard_multitask",
                "dataset_file": dataset_match.group(1) if dataset_match else cfg.get("dataset", ""),
                "input_dim": cfg.get("input_dim"),
                "seq_len": cfg.get("seq_len"),
                "channels": cfg.get("channels"),
                "blocks": cfg.get("blocks"),
                "kernel_size": cfg.get("kernel_size"),
                "dropout": cfg.get("dropout"),
                "lambda_turn": cfg.get("lambda_turn"),
                "lambda_theta": cfg.get("lambda_theta"),
                "lambda_theta_flat": cfg.get("lambda_theta_flat"),
                "main_neg_slope_weight": cfg.get("main_neg_slope_weight"),
                "turn_transition_weight": cfg.get("turn_transition_weight"),
                "turn_head_source": cfg.get("turn_head_source"),
                "loss_weight_lr": "",
                "dynamic_weight_main": "",
                "dynamic_weight_turn": "",
                "dynamic_weight_theta": "",
                "gru_head_pooling": "",
                "gru_turn_head": "",
                "source_file": str(report),
                "notes": "ModernTCN report JSON block.",
            }
        )

    uncertainty_cfg_path = (
        PROJECT_ROOT
        / "results"
        / "modern_tcn_sci_innovation"
        / "01_loss_optimization"
        / "uncertainty_seed101_rerun_20260622"
        / "config.json"
    )
    cfg = json.loads(uncertainty_cfg_path.read_text(encoding="utf-8"))
    cli = cfg.get("cli_args", {})
    dyn = cfg.get("dynamic_loss_state", {})
    rows.append(
        {
            "algorithm_group": "Uncertainty_weighted_ModernTCN_small",
            "variant_id": "uncertainty_seed101_rerun_20260622",
            "seed": 101,
            "model_family": cfg.get("model_family"),
            "loss_mode": cfg.get("loss_mode"),
            "dataset_file": cli.get("dataset_file"),
            "input_dim": 22,
            "seq_len": 128,
            "channels": cli.get("channels"),
            "blocks": cli.get("blocks"),
            "kernel_size": cli.get("kernel_size"),
            "dropout": cli.get("dropout"),
            "lambda_turn": cli.get("lambda_turn"),
            "lambda_theta": cli.get("lambda_theta"),
            "lambda_theta_flat": cli.get("lambda_theta_flat"),
            "main_neg_slope_weight": cli.get("main_neg_slope_weight"),
            "turn_transition_weight": cli.get("turn_transition_weight"),
            "turn_head_source": cli.get("turn_head_source"),
            "loss_weight_lr": cli.get("loss_weight_lr"),
            "dynamic_weight_main": dyn.get("weight_main"),
            "dynamic_weight_turn": dyn.get("weight_turn"),
            "dynamic_weight_theta": dyn.get("weight_theta"),
            "gru_head_pooling": "",
            "gru_turn_head": "",
            "source_file": str(uncertainty_cfg_path),
            "notes": "Uncertainty weighting anchor config; same recipe seed21/42 uses same hyper-parameter family.",
        }
    )

    for seed in GRU_PLANTFIX_SEEDS:
        report = GRU_LOG_ROOT / f"full_gru_v5_plantfix_passive17_plus_all5_seed{seed}" / "GRU_train_report.md"
        text = report.read_text(encoding="utf-8", errors="ignore")
        dataset = re.search(r"- 数据集:\s*`([^`]+)`", text)
        pooling = re.search(r"- Head pooling:\s*`([^`]+)`", text)
        turn_head = re.search(r"- Turn head:\s*`([^`]+)`, source=`([^`]+)`, hidden=([0-9]+)", text)
        loss_weights = re.search(r"- 损失权重:\s*([^\n]+)", text)
        rows.append(
            {
                "algorithm_group": "GRU_plantfix",
                "variant_id": f"full_gru_v5_plantfix_passive17_plus_all5_seed{seed}",
                "seed": seed,
                "model_family": "GRU",
                "loss_mode": "physics_guided",
                "dataset_file": dataset.group(1) if dataset else "",
                "input_dim": 22,
                "seq_len": 128,
                "channels": "",
                "blocks": "",
                "kernel_size": "",
                "dropout": "",
                "lambda_turn": "",
                "lambda_theta": "",
                "lambda_theta_flat": "",
                "main_neg_slope_weight": "1.0",
                "turn_transition_weight": "1.2 selection",
                "turn_head_source": turn_head.group(2) if turn_head else "",
                "loss_weight_lr": "",
                "dynamic_weight_main": "",
                "dynamic_weight_turn": "",
                "dynamic_weight_theta": "",
                "gru_head_pooling": pooling.group(1) if pooling else "",
                "gru_turn_head": f"{turn_head.group(1)} hidden={turn_head.group(3)}" if turn_head else "",
                "source_file": str(report),
                "notes": loss_weights.group(1) if loss_weights else "",
            }
        )
    return rows


def evidence_inventory() -> list[dict[str, Any]]:
    items = [
        ("baseline_metric_matrix", BASELINE_MATRIX, "baseline_lock offline reference metrics"),
        ("v2_full_thresholds", V2_FULL, "offline hard gate thresholds"),
        ("v2_closed_loop_thresholds", V2_CLOSED, "closed-loop hard gate thresholds"),
        ("uncertainty_offline_multiseed", UNCERTAINTY_OFFLINE, "Uncertainty seed21/42/101 offline v2 table"),
        ("uncertainty_closed_loop_multiseed", UNCERTAINTY_CLOSED, "Uncertainty seed21/42/101 current v2 closed-loop representatives"),
        ("strict_gru_tcn_closed_loop", STRICT_CLOSED, "GRU seed101 strict three-path closed-loop aggregate"),
        ("modern_turn_historical_multiseed_closed_loop", MODERN_MULTI_CLOSED_SUMMARY, "ModernTCN turn champion seed101/202/303 historical closed-loop summary"),
        ("legacy_gru_theta10_v2", LEGACY_GRU_THETA10, "old-contract GRU seed21/42/73/101 summary, excluded from official comparison"),
    ]
    rows = []
    for evidence_id, path, notes in items:
        rows.append(
            {
                "evidence_id": evidence_id,
                "exists": path.exists(),
                "path": str(path),
                "official_use": "yes" if evidence_id != "legacy_gru_theta10_v2" else "excluded",
                "notes": notes,
            }
        )
    for seed in MODERN_BASE_SEEDS:
        p = modern_summary_path(seed, "base")
        rows.append({"evidence_id": f"modern_base_seed{seed}_offline", "exists": p.exists(), "path": str(p), "official_use": "yes", "notes": "ModernTCN_small base current-contract offline summary"})
    p = modern_summary_path(101, "champion")
    rows.append({"evidence_id": "modern_champion_seed101_offline", "exists": p.exists(), "path": str(p), "official_use": "yes", "notes": "current baseline_lock offline summary"})
    for seed in GRU_PLANTFIX_SEEDS:
        p = GRU_LOG_ROOT / f"full_gru_v5_plantfix_passive17_plus_all5_seed{seed}" / "GRU_train_report.md"
        rows.append({"evidence_id": f"gru_plantfix_seed{seed}_offline_report", "exists": p.exists(), "path": str(p), "official_use": "limited", "notes": "GRU current-contract training report, flat_peak_theta_error unavailable"})
    return rows


def md_table(rows: list[dict[str, Any]], fields: list[str], max_rows: int | None = None) -> str:
    selected = rows if max_rows is None else rows[:max_rows]
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join(["---"] * len(fields)) + " |"]
    for row in selected:
        lines.append("| " + " | ".join(fmt(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def build_report(
    offline_rows: list[dict[str, Any]],
    offline_summary: list[dict[str, Any]],
    current_closed: list[dict[str, Any]],
    historical_closed: list[dict[str, Any]],
    legacy_gru: list[dict[str, Any]],
) -> str:
    pass_rows = [row for row in offline_rows if row["offline_v2_status"] == "pass"]
    best_offline = min(
        [row for row in offline_rows if row["algorithm_group"] != "ModernTCN_small_champion_baseline"],
        key=lambda row: num(row["offline_score_vs_baseline"]) if not math.isnan(num(row["offline_score_vs_baseline"])) else math.inf,
    )
    best_closed = min(current_closed, key=lambda row: num(row["J_control_current_v2"]))
    text = f"""# Multi-seed Algorithm Comparison under Current v2 Metrics

## 结论

1. 当前同 contract 离线多 seed 可比集合不是完全一致的 `21/42/101`：
   - `ModernTCN_small_base`: seed `21/73/101`
   - `Uncertainty_weighted_ModernTCN_small`: seed `21/42/101`
   - `GRU_plantfix`: seed `21/73/101`
2. 按 v2 offline hard gate，完整可判定 pass 的是 `ModernTCN_small_base` 的 1/3、当前 `ModernTCN_small_champion_baseline` 的 reference pass、以及 `Uncertainty_weighted_ModernTCN_small` 的 1/3。`GRU_plantfix` 因训练报告缺少 `flat_peak_theta_error`，不能被判为 full offline pass；其中 seed21/73 还额外存在硬保护失败。
3. 当前已有三路径闭环 v2 结果中，最佳仍是 `uncertainty_seed101_rerun_20260622`，`J_control_current_v2={num(best_closed['J_control_current_v2']):.6g}`；当前 frozen ModernTCN_small baseline 为 `J=1.0`。
4. 多 seed 稳定性角度，Uncertainty 还不能直接替代 ModernTCN_small：seed21/42 离线分别因 flat peak / edge theta 失败，闭环 J 也显著波动。更合理的定位仍是 seed101 anchor / paper innovation candidate，而不是 full replacement baseline。
5. GRU 的离线主任务表现不差，但当前闭环 seed101 的路径跟踪和控制代价远差于 ModernTCN_small / Uncertainty；并且缺少 plantfix 多 seed 闭环，所以不能作为当前最优。

## Offline v2 summary

{md_table(offline_summary, ['algorithm_group', 'seeds_available', 'offline_pass_count', 'offline_fail_count', 'offline_unavailable_count', 'best_seed_by_offline_score', 'best_offline_score_vs_baseline', 'median_offline_score_vs_baseline'])}

## Offline seed-level details

{md_table(offline_rows, ['algorithm_group', 'variant_id', 'seed', 'offline_v2_status', 'hard_gate_failures', 'hard_gate_unavailable', 'offline_score_vs_baseline', 'acc_main', 'stall_recall', 'slope_recall', 'theta_edge_p95_abs_err', 'flat_peak_theta_error'])}

## Current closed-loop v2 results

{md_table(current_closed, ['algorithm_group', 'variant_id', 'seed', 'J_control_current_v2', 'closed_loop_v2_status', 'closed_loop_v2_failures', 'ey_rmse_mean', 'xy_rmse_mean', 'epsi_rmse_mean', 'j_du_mean', 'omega_cmd_rms_mean'])}

## Historical ModernTCN turn-champion multi-seed closed-loop

这个表只用于理解 ModernTCN turn champion 的历史 seed 波动。它以同一文件中的 `ModernTCN_turn_seed101_champion` 为 local reference，不和 current v2 `J_control` 混排。

{md_table(historical_closed, ['controller', 'seed', 'J_control_vs_historical_champion', 'ey_rmse_mean', 'xy_rmse_mean', 'epsi_rmse_mean', 'j_du_mean', 'omega_cmd_rms_mean']) if historical_closed else 'No historical ModernTCN closed-loop multiseed file found.'}

## Legacy GRU theta10_v2 evidence

旧 `GRU_theta10_v2` 确实有 seed `21/42/73/101`，但它不是当前 plantfix passive17_plus_all5 contract，因此只记录为 excluded evidence，不能和当前 baseline / uncertainty 正式排名。

{md_table(legacy_gru, ['algorithm_group', 'case_name', 'seed', 'acc_main', 'acc_turn', 'theta_mae_deg', 'theta_edge_p95_abs_err', 'official_use'], max_rows=8) if legacy_gru else 'No legacy GRU theta10_v2 summary found.'}

## Output files

- Evidence inventory: `results/modern_tcn_metric_rebuild/13_multiseed_algorithm_comparison/00_evidence_inventory/evidence_inventory.csv`
- Parameter table: `results/modern_tcn_metric_rebuild/13_multiseed_algorithm_comparison/00_evidence_inventory/algorithm_parameter_table.csv`
- Offline seed-level comparison: `results/modern_tcn_metric_rebuild/13_multiseed_algorithm_comparison/01_offline_v2/multiseed_offline_v2.csv`
- Offline algorithm summary: `results/modern_tcn_metric_rebuild/13_multiseed_algorithm_comparison/01_offline_v2/algorithm_offline_summary.csv`
- Current closed-loop v2 comparison: `results/modern_tcn_metric_rebuild/13_multiseed_algorithm_comparison/02_closed_loop_v2/current_closed_loop_v2_existing.csv`
- Historical ModernTCN multiseed closed-loop: `results/modern_tcn_metric_rebuild/13_multiseed_algorithm_comparison/02_closed_loop_v2/historical_modern_tcn_multiseed_closed_loop.csv`
- Report: `results/modern_tcn_metric_rebuild/13_multiseed_algorithm_comparison/03_report/multiseed_algorithm_comparison_report.md`

## Method notes

- 缺失值没有用 0 或 baseline 回填。
- `flat_peak_theta_error` 对 GRU plantfix 报告不可用，因此 GRU full offline hard pass 只能是 `unavailable` 或 `fail`，不能强行 pass。
- Current v2 `J_control` 采用 `ey_rmse / xy_rmse / epsi_rmse / j_du / omega_cmd_rms` 相对 baseline 的平均比值；越低越好。
- Historical ModernTCN multiseed 闭环是独立历史证据，避免和 current v2 strict validation 混排。
"""
    return text


def main() -> None:
    baseline = baseline_metrics()
    full_thresholds = json.loads(V2_FULL.read_text(encoding="utf-8"))
    closed_thresholds = json.loads(V2_CLOSED.read_text(encoding="utf-8"))

    inv = evidence_inventory()
    write_csv(INV_DIR / "evidence_inventory.csv", inv, ["evidence_id", "exists", "path", "official_use", "notes"])
    write_json(INV_DIR / "comparison_contract.json", {
        "node_root": str(NODE_ROOT),
        "baseline_reference": "baseline_lock",
        "offline_threshold_file": str(V2_FULL),
        "closed_loop_threshold_file": str(V2_CLOSED),
        "official_seed_sets": {
            "ModernTCN_small_base": MODERN_BASE_SEEDS,
            "Uncertainty_weighted_ModernTCN_small": UNCERTAINTY_SEEDS,
            "GRU_plantfix": GRU_PLANTFIX_SEEDS,
        },
        "missing_policy": "do_not_impute; missing hard metrics make pass unavailable",
    })

    param_rows = build_parameter_rows()
    write_csv(
        INV_DIR / "algorithm_parameter_table.csv",
        param_rows,
        [
            "algorithm_group",
            "variant_id",
            "seed",
            "model_family",
            "loss_mode",
            "dataset_file",
            "input_dim",
            "seq_len",
            "channels",
            "blocks",
            "kernel_size",
            "dropout",
            "lambda_turn",
            "lambda_theta",
            "lambda_theta_flat",
            "main_neg_slope_weight",
            "turn_transition_weight",
            "turn_head_source",
            "loss_weight_lr",
            "dynamic_weight_main",
            "dynamic_weight_turn",
            "dynamic_weight_theta",
            "gru_head_pooling",
            "gru_turn_head",
            "source_file",
            "notes",
        ],
    )

    offline_rows = collect_offline_rows(baseline, full_thresholds)
    offline_fields = [
        "algorithm_group",
        "variant_id",
        "seed",
        "source_contract",
        "evidence_level",
        "is_reference_baseline",
        "official_offline_comparison_eligible",
        "offline_v2_status",
        "hard_gate_failures",
        "hard_gate_unavailable",
        "offline_score_vs_baseline",
        "metric_missing_ratio",
        "best_epoch",
        "acc_main",
        "acc_turn",
        "acc_turn_transition",
        "theta_mae_deg",
        "theta_edge_p95_abs_err",
        "flat_peak_theta_error",
        "flat_recall",
        "stall_recall",
        "slope_recall",
        "checkpoint_file",
        "report_file",
        "source_file",
        "notes",
    ]
    write_csv(OFFLINE_DIR / "multiseed_offline_v2.csv", offline_rows, offline_fields)
    offline_summary = summarise_offline(offline_rows)
    write_csv(
        OFFLINE_DIR / "algorithm_offline_summary.csv",
        offline_summary,
        [
            "algorithm_group",
            "seeds_available",
            "n_seeds",
            "offline_pass_count",
            "offline_fail_count",
            "offline_unavailable_count",
            "best_seed_by_offline_score",
            "best_variant_id",
            "best_offline_score_vs_baseline",
            "median_offline_score_vs_baseline",
            "status_summary",
        ],
    )

    legacy_gru = build_legacy_gru_excluded()
    write_csv(
        OFFLINE_DIR / "legacy_gru_theta10_v2_excluded.csv",
        legacy_gru,
        [
            "algorithm_group",
            "case_name",
            "seed",
            "acc_main",
            "acc_turn",
            "theta_mae_deg",
            "theta_edge_p95_abs_err",
            "flat_recall",
            "stall_recall",
            "slope_recall",
            "model_file",
            "report_file",
            "official_use",
            "exclude_reason",
            "source_file",
        ],
    )

    current_closed = collect_current_closed_loop(closed_thresholds)
    write_csv(
        CLOSED_DIR / "current_closed_loop_v2_existing.csv",
        current_closed,
        [
            "algorithm_group",
            "variant_id",
            "seed",
            "closed_loop_evidence_level",
            "n_paths",
            "J_control_current_v2",
            "closed_loop_v2_status",
            "closed_loop_v2_failures",
            "ey_rmse_mean",
            "xy_rmse_mean",
            "epsi_rmse_mean",
            "j_du_mean",
            "omega_cmd_rms_mean",
            "theta_mae_deg_mean",
            "main_acc_pct_mean",
            "turn_acc_pct_mean",
            "source_file",
            "notes",
        ],
    )
    historical_closed = collect_historical_modern_closed_loop()
    write_csv(
        CLOSED_DIR / "historical_modern_tcn_multiseed_closed_loop.csv",
        historical_closed,
        [
            "controller",
            "seed",
            "n_paths",
            "J_control_vs_historical_champion",
            "ey_rmse_mean",
            "xy_rmse_mean",
            "epsi_rmse_mean",
            "j_du_mean",
            "omega_cmd_rms_mean",
            "theta_mae_deg_mean",
            "main_acc_pct_mean",
            "turn_acc_pct_mean",
            "source_file",
            "notes",
        ],
    )

    report = build_report(offline_rows, offline_summary, current_closed, historical_closed, legacy_gru)
    write_text(REPORT_DIR / "multiseed_algorithm_comparison_report.md", report)

    print(f"Wrote {NODE_ROOT}")
    print(f"offline_rows={len(offline_rows)} current_closed_rows={len(current_closed)} historical_closed_rows={len(historical_closed)}")


if __name__ == "__main__":
    main()
