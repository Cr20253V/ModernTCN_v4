from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, median, pstdev
from typing import Any


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent.parent
NODE_ROOT = ROOT / "16_recipe_vs_deployment_comparison"

OFFLINE_13 = ROOT / "13_multiseed_algorithm_comparison" / "01_offline_v2" / "multiseed_offline_v2.csv"
CLOSED_13 = ROOT / "13_multiseed_algorithm_comparison" / "02_closed_loop_v2" / "current_closed_loop_v2_existing.csv"
PATH_12 = ROOT / "12_uncertainty_replacement_qualification" / "03_closed_loop_representatives" / "closed_loop_path_metrics.csv"
CLOSED_14 = ROOT / "14_uncertainty_stability_optimization" / "04_closed_loop_multiseed" / "closed_loop_results.csv"
PATH_14 = ROOT / "14_uncertainty_stability_optimization" / "04_closed_loop_multiseed" / "closed_loop_path_metrics.csv"
OFFLINE_14 = ROOT / "14_uncertainty_stability_optimization" / "02_stability_screen" / "final_multiseed_offline_metrics.csv"
A2_OFFLINE_15 = ROOT / "15_bi_bu_uncertainty_stabilization" / "04_phase2_screen.csv"
A2_SENTINEL_15 = ROOT / "15_bi_bu_uncertainty_stabilization" / "06_sentinel_closed_loop" / "sentinel_closed_loop_aggregate.csv"
A2_PATH_15 = ROOT / "15_bi_bu_uncertainty_stabilization" / "06_sentinel_closed_loop" / "sentinel_closed_loop_results.csv"
FINAL_15 = ROOT / "15_bi_bu_uncertainty_stabilization" / "09_final_decision" / "final_decision.json"
MODERN_BASE_TRAIN_42 = NODE_ROOT / "07_modern_base_seed42_training" / "modern_base_seed42"
MODERN_BASE_EXPORTS = NODE_ROOT / "08_modern_base_exports"
MODERN_BASE_CLOSED = NODE_ROOT / "09_modern_base_closed_loop"
MODERN_BASE_CLOSED_RUNS = MODERN_BASE_CLOSED / "01_closed_loop_runs"
MODERN_BASE_CLOSED_RESULTS = MODERN_BASE_CLOSED / "closed_loop_results.csv"
MODERN_BASE_PATH_METRICS = MODERN_BASE_CLOSED / "closed_loop_path_metrics.csv"

BASELINE_J = 1.0
ANCHOR_J = 0.94411711953914
TARGET_SEEDS = [21, 42, 101]
PATH_TAGS = [
    "path_factory_logistics_showcase_theta10_v3",
    "path_closed_loop_long_updown_theta10_v1",
    "path_closed_loop_sharp_turn_transition_theta10_v1",
]
CONTROL_METRICS = ["ey_rmse", "xy_rmse", "epsi_rmse", "j_du", "omega_cmd_rms"]

MODERN_BASE_CHECKPOINT_ROOT = (
    PROJECT_ROOT
    / "results"
    / "paper"
    / "agv_model_parameter_correction_workflow"
    / "08_models"
    / "modern_tcn"
)


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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
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


def md_table(rows: list[dict[str, Any]], fields: list[str], max_rows: int | None = None) -> str:
    selected = rows if max_rows is None else rows[:max_rows]
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join(["---"] * len(fields)) + " |"]
    for row in selected:
        lines.append("| " + " | ".join(fmt(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def finite(values: list[float]) -> list[float]:
    return [v for v in values if math.isfinite(v)]


def infer_path_tag(row: dict[str, Any]) -> str:
    tag = str(row.get("path_tag", "")).strip()
    if tag and tag.lower() != "nan":
        return tag
    source = str(row.get("source", ""))
    for known in PATH_TAGS:
        if known in source:
            return known
    return ""


def path_j(row: dict[str, Any], baseline: dict[str, Any]) -> float:
    ratios: list[float] = []
    for metric in CONTROL_METRICS:
        value = num(row.get(metric))
        base = num(baseline.get(metric))
        if math.isfinite(value) and math.isfinite(base) and base != 0:
            ratios.append(value / base)
    return mean(ratios) if ratios else math.nan


def make_path_gate_rows(
    path_file: Path,
    source_scope: str,
    candidate_id_map: dict[str, str] | None = None,
    include_baseline: bool = False,
) -> list[dict[str, Any]]:
    rows = read_csv(path_file)
    if not rows:
        return []
    for row in rows:
        row.setdefault("source", str(path_file))
    baseline_by_path: dict[str, dict[str, Any]] = {}
    for row in rows:
        cid = row.get("candidate_id") or row.get("controller")
        tag = infer_path_tag(row)
        if cid == "baseline_lock" and tag:
            baseline_by_path[tag] = row

    out: list[dict[str, Any]] = []
    for row in rows:
        raw_cid = row.get("candidate_id") or row.get("controller") or ""
        if raw_cid == "baseline_lock" and not include_baseline:
            continue
        tag = infer_path_tag(row)
        if not tag or tag not in baseline_by_path:
            continue
        mapped = candidate_id_map.get(raw_cid, raw_cid) if candidate_id_map else raw_cid
        j = path_j(row, baseline_by_path[tag])
        out.append(
            {
                "source_scope": source_scope,
                "candidate_id": mapped,
                "raw_candidate_id": raw_cid,
                "path_tag": tag,
                "J_control_path": j,
                "path_fail": math.isfinite(j) and j > 1.0,
                "path_catastrophic": math.isfinite(j) and j > 1.5,
                "ey_rmse": num(row.get("ey_rmse")),
                "xy_rmse": num(row.get("xy_rmse")),
                "epsi_rmse": num(row.get("epsi_rmse")),
                "j_du": num(row.get("j_du")),
                "omega_cmd_rms": num(row.get("omega_cmd_rms")),
                "source_file": str(path_file),
            }
        )
    return out


def make_a2_path_gate_rows() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in read_csv(A2_PATH_15):
        j = num(row.get("J_control"))
        out.append(
            {
                "source_scope": "bi_bu_a2_sentinel",
                "candidate_id": row.get("run_id", ""),
                "raw_candidate_id": row.get("run_id", ""),
                "path_tag": row.get("path_tag", ""),
                "J_control_path": j,
                "path_fail": math.isfinite(j) and j > 1.0,
                "path_catastrophic": bool(num(row.get("path_catastrophic"))),
                "ey_rmse": num(row.get("ey_rmse")),
                "xy_rmse": num(row.get("xy_rmse")),
                "epsi_rmse": num(row.get("epsi_rmse")),
                "j_du": num(row.get("j_du")),
                "omega_cmd_rms": num(row.get("omega_cmd_rms")),
                "source_file": str(A2_PATH_15),
            }
        )
    return out


def make_modern_base_path_gate_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path_tag in PATH_TAGS:
        summary_file = MODERN_BASE_CLOSED_RUNS / path_tag / "modern_base_recipe_summary.csv"
        rows.extend(make_path_gate_rows(summary_file, "modern_base_recipe_16"))
    return rows


def path_stats(path_rows: list[dict[str, Any]], candidate_id: str) -> dict[str, Any]:
    rows = [r for r in path_rows if r.get("candidate_id") == candidate_id]
    values = finite([num(r.get("J_control_path")) for r in rows])
    return {
        "path_count": len(rows),
        "worst_path_J": max(values) if values else math.nan,
        "path_fail_count": sum(1 for r in rows if str(r.get("path_fail")).lower() == "true"),
        "path_catastrophic_count": sum(1 for r in rows if str(r.get("path_catastrophic")).lower() == "true"),
    }


def deployment_status(j_control: float, catastrophic_count: int, candidate_id: str) -> tuple[str, str]:
    if candidate_id == "baseline_lock":
        return "reference", "locked ModernTCN_small champion baseline"
    if not math.isfinite(j_control):
        return "unavailable", "closed-loop J_control missing"
    reasons: list[str] = []
    if j_control > BASELINE_J:
        reasons.append(f"mean_J_control={j_control:.6g}>baseline={BASELINE_J:.6g}")
    if catastrophic_count > 0:
        reasons.append(f"path_catastrophic_count={catastrophic_count}>0")
    if reasons:
        return "fail", ";".join(reasons)
    return "pass", "mean_J_control<=baseline and no path catastrophic failure"


def collect_path_rows() -> list[dict[str, Any]]:
    replacement_map = {
        "ua_seed21": "uncertainty_anchor_same_recipe_seed21",
        "ua_seed42": "uncertainty_anchor_same_recipe_seed42",
        "uncertainty_seed101_rerun_20260622": "uncertainty_seed101_rerun_20260622",
    }
    rows = make_path_gate_rows(PATH_12, "uncertainty_replacement_12", replacement_map, include_baseline=True)
    stability_rows = make_path_gate_rows(PATH_14, "uncertainty_stability_14")
    rows.extend(
        row
        for row in stability_rows
        if str(row.get("raw_candidate_id", "")).startswith("s01_lr13_select_edges_flat")
    )
    rows.extend(make_a2_path_gate_rows())
    rows.extend(make_modern_base_path_gate_rows())
    return rows


def aggregate_control_j(candidate_rows: list[dict[str, Any]], baseline_rows: list[dict[str, Any]]) -> float:
    ratios: list[float] = []
    candidate_paths = {str(r.get("path_tag", "")) for r in candidate_rows}
    matched_baseline = [r for r in baseline_rows if str(r.get("path_tag", "")) in candidate_paths]
    for metric in CONTROL_METRICS:
        candidate_values = finite([num(r.get(metric)) for r in candidate_rows])
        baseline_values = finite([num(r.get(metric)) for r in matched_baseline])
        if not candidate_values or not baseline_values:
            continue
        base = mean(baseline_values)
        if base != 0:
            ratios.append(mean(candidate_values) / base)
    return mean(ratios) if ratios else math.nan


def aggregate_deployment_from_path_scope(
    path_rows: list[dict[str, Any]],
    source_scope: str,
    recipe: str,
    source_file: Path,
    evidence_scope: str,
) -> list[dict[str, Any]]:
    baseline_rows = [r for r in path_rows if r.get("candidate_id") == "baseline_lock"]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in path_rows:
        if row.get("source_scope") == source_scope:
            grouped[str(row.get("candidate_id", ""))].append(row)

    rows: list[dict[str, Any]] = []
    for candidate_id, candidate_rows in grouped.items():
        if not candidate_id or candidate_id == "baseline_lock":
            continue
        stats = path_stats(path_rows, candidate_id)
        j = aggregate_control_j(candidate_rows, baseline_rows)
        status, reason = deployment_status(j, int(stats["path_catastrophic_count"]), candidate_id)
        seed_text = candidate_id.split("seed")[-1] if "seed" in candidate_id else ""
        rows.append(
            {
                "algorithm_recipe": recipe,
                "candidate_id": candidate_id,
                "seed": int(seed_text) if seed_text.isdigit() else seed_text,
                "evidence_scope": evidence_scope,
                "n_paths": len(candidate_rows),
                "J_control": j,
                **stats,
                "deployment_champion_gate_status": status,
                "deployment_champion_gate_reason": reason,
                "source_file": str(source_file),
            }
        )
    return sorted(rows, key=lambda r: num(r.get("J_control")))


def collect_deployment_rows(path_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(CLOSED_13):
        group = row.get("algorithm_group", "")
        variant = row.get("variant_id", "")
        if group == "GRU_plantfix":
            continue
        if group == "ModernTCN_small_champion_baseline":
            candidate_id = "baseline_lock"
            recipe = "ModernTCN_small_locked_champion"
        elif group == "Uncertainty_weighted_ModernTCN_small":
            candidate_id = variant
            recipe = "Uncertainty_weighted_same_recipe"
        else:
            continue
        stats = path_stats(path_rows, candidate_id)
        j = num(row.get("J_control_current_v2"))
        status, reason = deployment_status(j, int(stats["path_catastrophic_count"]), candidate_id)
        rows.append(
            {
                "algorithm_recipe": recipe,
                "candidate_id": candidate_id,
                "seed": int(num(row.get("seed"))) if math.isfinite(num(row.get("seed"))) else "",
                "evidence_scope": row.get("closed_loop_evidence_level", "current_v2_three_path"),
                "n_paths": int(num(row.get("n_paths"))) if math.isfinite(num(row.get("n_paths"))) else stats["path_count"],
                "J_control": j,
                **stats,
                "deployment_champion_gate_status": status,
                "deployment_champion_gate_reason": reason,
                "source_file": row.get("source_file", str(CLOSED_13)),
            }
        )

    for row in read_csv(CLOSED_14):
        candidate_id = row.get("candidate_id", "")
        if candidate_id in {"baseline_lock", "uncertainty_seed101_rerun_20260622"}:
            continue
        stats = path_stats(path_rows, candidate_id)
        j = num(row.get("J_control"))
        status, reason = deployment_status(j, int(stats["path_catastrophic_count"]), candidate_id)
        seed = candidate_id.split("seed")[-1] if "seed" in candidate_id else ""
        rows.append(
            {
                "algorithm_recipe": "Uncertainty_stability_s01",
                "candidate_id": candidate_id,
                "seed": seed,
                "evidence_scope": "current_v2_three_path",
                "n_paths": int(num(row.get("n_paths"))) if math.isfinite(num(row.get("n_paths"))) else stats["path_count"],
                "J_control": j,
                **stats,
                "deployment_champion_gate_status": status,
                "deployment_champion_gate_reason": reason,
                "source_file": str(CLOSED_14),
            }
        )

    for row in read_csv(A2_SENTINEL_15):
        candidate_id = row.get("run_id", "")
        stats = path_stats(path_rows, candidate_id)
        j = num(row.get("mean_J_control"))
        status, reason = deployment_status(j, int(stats["path_catastrophic_count"]), candidate_id)
        rows.append(
            {
                "algorithm_recipe": "BI_BU_A2_freeze_early",
                "candidate_id": candidate_id,
                "seed": int(num(row.get("seed"))) if math.isfinite(num(row.get("seed"))) else "",
                "evidence_scope": "sentinel_three_path",
                "n_paths": int(num(row.get("n_paths"))) if math.isfinite(num(row.get("n_paths"))) else stats["path_count"],
                "J_control": j,
                **stats,
                "deployment_champion_gate_status": status,
                "deployment_champion_gate_reason": reason,
                "source_file": str(A2_SENTINEL_15),
            }
        )
    rows.extend(
        aggregate_deployment_from_path_scope(
            path_rows,
            "modern_base_recipe_16",
            "ModernTCN_small_base",
            MODERN_BASE_CLOSED_RESULTS,
            "current_v2_three_path_node16",
        )
    )
    return sorted(rows, key=lambda r: (str(r["algorithm_recipe"]), num(r["J_control"])))


def offline_lookup() -> dict[tuple[str, int], dict[str, Any]]:
    out: dict[tuple[str, int], dict[str, Any]] = {}
    for row in read_csv(OFFLINE_13):
        group = row.get("algorithm_group", "")
        seed = int(num(row.get("seed"))) if math.isfinite(num(row.get("seed"))) else -1
        if group == "ModernTCN_small_base":
            recipe = "ModernTCN_small_base"
        elif group == "Uncertainty_weighted_ModernTCN_small":
            recipe = "Uncertainty_weighted_same_recipe"
        elif group == "ModernTCN_small_champion_baseline":
            recipe = "ModernTCN_small_locked_champion"
        else:
            continue
        out[(recipe, seed)] = {
            "offline_variant_id": row.get("variant_id", ""),
            "offline_status": row.get("offline_v2_status", ""),
            "offline_failures": row.get("hard_gate_failures", ""),
            "offline_score": num(row.get("offline_score_vs_baseline")),
            "checkpoint_file": row.get("checkpoint_file", ""),
            "offline_source_file": row.get("source_file", str(OFFLINE_13)),
        }

    for row in read_csv(OFFLINE_14):
        seed = int(num(row.get("seed"))) if math.isfinite(num(row.get("seed"))) else -1
        out[("Uncertainty_stability_s01", seed)] = {
            "offline_variant_id": row.get("run_tag", ""),
            "offline_status": row.get("offline_v2_status", ""),
            "offline_failures": row.get("offline_v2_failures", ""),
            "offline_score": num(row.get("offline_score")),
            "checkpoint_file": row.get("checkpoint_file", ""),
            "offline_source_file": str(OFFLINE_14),
        }

    for row in read_csv(A2_OFFLINE_15):
        seed = int(num(row.get("seed"))) if math.isfinite(num(row.get("seed"))) else -1
        out[("BI_BU_A2_freeze_early", seed)] = {
            "offline_variant_id": row.get("run_id", ""),
            "offline_status": "pass" if bool(num(row.get("strict_offline_pass"))) else "fail",
            "offline_failures": row.get("strict_offline_reasons", ""),
            "offline_score": num(row.get("offline_v2_score")),
            "checkpoint_file": "",
            "offline_source_file": str(A2_OFFLINE_15),
        }

    seed42_summary = MODERN_BASE_TRAIN_42 / "modern_tcn_seed42_summary.csv"
    seed42_rows = read_csv(seed42_summary)
    if seed42_rows:
        row = seed42_rows[0]
        checks = [
            ("acc_main", num(row.get("acc_main")), ">=", 0.90),
            ("flat_recall", num(row.get("flat_recall")), ">=", 0.90),
            ("slope_recall", num(row.get("slope_recall")), ">=", 0.88),
            ("acc_turn_transition", num(row.get("acc_turn_transition")), ">=", 0.75),
            ("theta_mae_deg", num(row.get("theta_mae_deg")), "<=", 0.70),
        ]
        failures = []
        for name, value, op, threshold in checks:
            if not math.isfinite(value):
                failures.append(f"{name} missing")
                continue
            passed = value >= threshold if op == ">=" else value <= threshold
            if not passed:
                failures.append(f"{name} {op} {threshold:.4f} unmet actual {value:.4f}")
        out[("ModernTCN_small_base", 42)] = {
            "offline_variant_id": "modern_base_seed42",
            "offline_status": "pass" if not failures else "fail",
            "offline_failures": ";".join(failures) if failures else "none",
            "offline_score": math.nan,
            "checkpoint_file": row.get(
                "checkpoint_file",
                str(MODERN_BASE_TRAIN_42 / "modern_tcn_seed42.pt"),
            ),
            "offline_source_file": str(seed42_summary),
        }
    return out


def build_seed_status_rows(deployment_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    offline = offline_lookup()
    dep_by_recipe_seed: dict[tuple[str, int], dict[str, Any]] = {}
    for row in deployment_rows:
        seed = int(num(row.get("seed"))) if math.isfinite(num(row.get("seed"))) else -1
        dep_by_recipe_seed[(row["algorithm_recipe"], seed)] = row

    def has_target_closed_loop(recipe: str) -> bool:
        return all(
            math.isfinite(num(dep_by_recipe_seed.get((recipe, seed), {}).get("J_control")))
            for seed in TARGET_SEEDS
        )

    recipe_comparison_available = has_target_closed_loop("ModernTCN_small_base") and has_target_closed_loop(
        "Uncertainty_weighted_same_recipe"
    )

    recipes = [
        "ModernTCN_small_base",
        "ModernTCN_small_locked_champion",
        "Uncertainty_weighted_same_recipe",
        "Uncertainty_stability_s01",
        "BI_BU_A2_freeze_early",
    ]
    rows: list[dict[str, Any]] = []
    for recipe in recipes:
        seeds = TARGET_SEEDS if recipe != "ModernTCN_small_locked_champion" else [101]
        if recipe == "ModernTCN_small_base":
            seeds = [21, 42, 73, 101]
        for seed in seeds:
            off = offline.get((recipe, seed), {})
            dep = dep_by_recipe_seed.get((recipe, seed), {})
            if recipe == "BI_BU_A2_freeze_early" and seed in {21, 42}:
                deployment_gate = "fail"
                recipe_status = "sentinel_failed_no_full_recipe_claim"
                selected_status = "not_applicable_for_individual_seed"
            else:
                deployment_gate = dep.get("deployment_champion_gate_status", "unavailable")
                if recipe == "ModernTCN_small_locked_champion":
                    recipe_status = "not_a_recipe_multiseed_row"
                elif recipe == "BI_BU_A2_freeze_early":
                    recipe_status = "sentinel_incomplete_and_pending_comparator"
                elif recipe in {"ModernTCN_small_base", "Uncertainty_weighted_same_recipe"} and recipe_comparison_available:
                    recipe_status = "recipe_multiseed_comparison_available"
                elif (
                    recipe == "Uncertainty_stability_s01"
                    and has_target_closed_loop("ModernTCN_small_base")
                    and has_target_closed_loop(recipe)
                ):
                    recipe_status = "secondary_recipe_multiseed_comparison_available"
                else:
                    recipe_status = "pending_until_ModernTCN_small_multiseed_closed_loop_available"
                selected_status = "not_applicable_for_individual_seed"
            rows.append(
                {
                    "algorithm_recipe": recipe,
                    "seed": seed,
                    "required_for_recipe_comparison": seed in TARGET_SEEDS and recipe != "ModernTCN_small_locked_champion",
                    "offline_variant_id": off.get("offline_variant_id", "missing"),
                    "offline_status": off.get("offline_status", "missing"),
                    "offline_score": off.get("offline_score", math.nan),
                    "offline_failures": off.get("offline_failures", "missing"),
                    "candidate_id": dep.get("candidate_id", "missing"),
                    "closed_loop_scope": dep.get("evidence_scope", "missing"),
                    "J_control": dep.get("J_control", math.nan),
                    "worst_path_J": dep.get("worst_path_J", math.nan),
                    "path_fail_count": dep.get("path_fail_count", math.nan),
                    "path_catastrophic_count": dep.get("path_catastrophic_count", math.nan),
                    "deployment_champion_gate_status": deployment_gate,
                    "deployment_champion_gate_reason": dep.get("deployment_champion_gate_reason", "closed-loop evidence missing"),
                    "recipe_multiseed_status": recipe_status,
                    "selected_model_status": selected_status,
                    "checkpoint_file": off.get("checkpoint_file", ""),
                    "offline_source_file": off.get("offline_source_file", ""),
                    "closed_loop_source_file": dep.get("source_file", ""),
                }
            )
    return rows


def aggregate_recipe(
    recipe: str,
    seed_rows: list[dict[str, Any]],
    deployment_rows: list[dict[str, Any]],
    status: str,
    notes: str,
) -> dict[str, Any]:
    required = [r for r in seed_rows if r["algorithm_recipe"] == recipe and r["required_for_recipe_comparison"]]
    closed = [r for r in required if math.isfinite(num(r.get("J_control")))]
    js = finite([num(r.get("J_control")) for r in closed])
    pass_count = sum(1 for r in required if r.get("offline_status") == "pass")
    dep_pass = sum(1 for r in closed if r.get("deployment_champion_gate_status") == "pass")
    missing_off = [str(r["seed"]) for r in required if r.get("offline_status") == "missing"]
    missing_cl = [str(r["seed"]) for r in required if not math.isfinite(num(r.get("J_control")))]
    extra_seeds = [str(r["seed"]) for r in seed_rows if r["algorithm_recipe"] == recipe and not r["required_for_recipe_comparison"]]
    path_cat = sum(int(num(r.get("path_catastrophic_count"))) for r in closed if math.isfinite(num(r.get("path_catastrophic_count"))))
    return {
        "algorithm_recipe": recipe,
        "target_seed_set": "/".join(str(s) for s in TARGET_SEEDS),
        "available_seed_rows": "/".join(str(r["seed"]) for r in seed_rows if r["algorithm_recipe"] == recipe),
        "extra_non_target_seeds": "/".join(extra_seeds) if extra_seeds else "none",
        "missing_offline_target_seeds": "/".join(missing_off) if missing_off else "none",
        "missing_closed_loop_target_seeds": "/".join(missing_cl) if missing_cl else "none",
        "offline_pass_count": pass_count,
        "closed_loop_count": len(closed),
        "mean_J_control": mean(js) if js else math.nan,
        "median_J_control": median(js) if js else math.nan,
        "best_J_control": min(js) if js else math.nan,
        "worst_J_control": max(js) if js else math.nan,
        "std_J_control": pstdev(js) if len(js) > 1 else 0.0 if len(js) == 1 else math.nan,
        "deployment_pass_rate_vs_champion": dep_pass / len(closed) if closed else math.nan,
        "path_catastrophic_count": path_cat,
        "recipe_multiseed_status": status,
        "notes": notes,
    }


def build_recipe_summary(seed_rows: list[dict[str, Any]], deployment_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    base_row = aggregate_recipe(
        "ModernTCN_small_base",
        seed_rows,
        deployment_rows,
        "pending_until_ModernTCN_small_seed21_42_101_closed_loop_available",
        "ModernTCN_small base seed21/42/101 same-path closed-loop distribution is not complete yet.",
    )
    uncertainty_row = aggregate_recipe(
        "Uncertainty_weighted_same_recipe",
        seed_rows,
        deployment_rows,
        "pending_until_ModernTCN_small_multiseed_closed_loop_available",
        "Uncertainty same-recipe has closed-loop evidence, but recipe-level comparison requires the ModernTCN_small base distribution.",
    )

    base_complete = (
        base_row["missing_offline_target_seeds"] == "none"
        and base_row["missing_closed_loop_target_seeds"] == "none"
        and int(base_row["closed_loop_count"]) == len(TARGET_SEEDS)
    )
    uncertainty_complete = (
        uncertainty_row["missing_offline_target_seeds"] == "none"
        and uncertainty_row["missing_closed_loop_target_seeds"] == "none"
        and int(uncertainty_row["closed_loop_count"]) == len(TARGET_SEEDS)
    )
    if base_complete and uncertainty_complete:
        base_mean = num(base_row["mean_J_control"])
        uncertainty_mean = num(uncertainty_row["mean_J_control"])
        base_row["recipe_multiseed_status"] = "complete_base_recipe_distribution_available"
        if uncertainty_mean < base_mean:
            uncertainty_row["recipe_multiseed_status"] = "complete_uncertainty_recipe_better_by_mean_J"
            uncertainty_row["notes"] = "Complete same-seed comparison is available; uncertainty recipe has lower mean J_control than ModernTCN_small base."
        else:
            uncertainty_row["recipe_multiseed_status"] = "complete_uncertainty_recipe_not_better_by_mean_J"
            uncertainty_row["notes"] = "Complete same-seed comparison is available; uncertainty recipe does not improve mean J_control over ModernTCN_small base."
        base_row["notes"] = "Complete ModernTCN_small base seed21/42/101 same-path closed-loop distribution is available."

    stability_row = aggregate_recipe(
        "Uncertainty_stability_s01",
        seed_rows,
        deployment_rows,
        "closed_loop_negative_vs_champion_but_recipe_comparison_pending",
        "This robust-offline recipe has 3/3 offline pass but all three closed-loop J_control values are above the locked champion.",
    )
    stability_complete = (
        stability_row["missing_offline_target_seeds"] == "none"
        and stability_row["missing_closed_loop_target_seeds"] == "none"
        and int(stability_row["closed_loop_count"]) == len(TARGET_SEEDS)
    )
    if base_complete and stability_complete:
        stability_row["recipe_multiseed_status"] = "complete_secondary_recipe_distribution_available_but_fails_champion"
        stability_row["notes"] = "Secondary recipe comparison is available; this recipe is more stable than ModernTCN_small base by mean J_control but all seeds fail the locked champion gate."

    return [
        base_row,
        uncertainty_row,
        stability_row,
        aggregate_recipe(
            "BI_BU_A2_freeze_early",
            seed_rows,
            deployment_rows,
            "sentinel_failed_no_full_recipe_claim",
            "A2 seed21/42 failed the deployment sentinel; seed101 full closed-loop was not promoted.",
        ),
    ]


def modern_base_checkpoint(seed: int) -> Path:
    if seed == 42:
        local_ckpt = MODERN_BASE_TRAIN_42 / "modern_tcn_seed42.pt"
        if local_ckpt.exists():
            return local_ckpt
    return (
        MODERN_BASE_CHECKPOINT_ROOT
        / f"modern_tcn_v5_plantfix_passive17_plus_all5_seed{seed}"
        / f"modern_tcn_seed{seed}.pt"
    )


def build_missing_experiments(seed_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for seed in TARGET_SEEDS:
        ckpt = modern_base_checkpoint(seed)
        row = next((r for r in seed_rows if r["algorithm_recipe"] == "ModernTCN_small_base" and r["seed"] == seed), {})
        closed_missing = not math.isfinite(num(row.get("J_control")))
        offline_missing = row.get("offline_status") == "missing"
        if offline_missing or closed_missing:
            if offline_missing and not ckpt.exists():
                action = "train_ModernTCN_small_base_seed_then_export_onnx_and_run_three_path_closed_loop"
            elif closed_missing:
                action = "export_existing_checkpoint_to_onnx_and_run_three_path_closed_loop"
            else:
                action = "none"
            rows.append(
                {
                    "algorithm_recipe": "ModernTCN_small_base",
                    "seed": seed,
                    "checkpoint_exists": ckpt.exists(),
                    "checkpoint_file": str(ckpt),
                    "offline_status": row.get("offline_status", "missing"),
                    "closed_loop_status": "missing" if closed_missing else "available",
                    "required_path_set": ";".join(PATH_TAGS),
                    "required_action": action,
                    "reason": "needed for fair recipe-level ModernTCN_small seed21/42/101 vs Uncertainty seed21/42/101 comparison",
                }
            )
    return rows


def build_selected_best_rows(deployment_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_recipe: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in deployment_rows:
        if math.isfinite(num(row.get("J_control"))):
            by_recipe[row["algorithm_recipe"]].append(row)

    def best(recipe: str) -> dict[str, Any] | None:
        rows = by_recipe.get(recipe, [])
        if not rows:
            return None
        return min(rows, key=lambda r: num(r["J_control"]))

    entries: list[dict[str, Any]] = []
    baseline = next((r for r in deployment_rows if r["candidate_id"] == "baseline_lock"), None)
    if baseline:
        entries.append(
            {
                "algorithm_recipe": "ModernTCN_small_locked_champion",
                "selected_candidate_id": "baseline_lock",
                "seed": 101,
                "selection_protocol": "already_locked_deployment_champion",
                "J_control": baseline["J_control"],
                "selected_model_status": "reference",
                "notes": "This is the fixed deployment champion, not a recipe distribution.",
            }
        )

    for recipe, protocol in [
        ("ModernTCN_small_base", "same_target_seed_set_diagnostic_best"),
        ("Uncertainty_weighted_same_recipe", "historical_anchor_seed101_selection"),
        ("Uncertainty_stability_s01", "best_seed_after_robust_offline_recipe"),
        ("BI_BU_A2_freeze_early", "sentinel_best_seed_only"),
    ]:
        row = best(recipe)
        if not row:
            continue
        if recipe == "BI_BU_A2_freeze_early":
            status = "fail_sentinel_not_selectable"
        elif num(row["J_control"]) <= BASELINE_J and int(row.get("path_catastrophic_count", 0)) == 0:
            status = "pass_vs_locked_champion"
        else:
            status = "fail_vs_locked_champion"
        entries.append(
            {
                "algorithm_recipe": recipe,
                "selected_candidate_id": row["candidate_id"],
                "seed": row["seed"],
                "selection_protocol": protocol,
                "J_control": row["J_control"],
                "selected_model_status": status,
                "notes": "Selected-best comparison is only paper-valid if the same validation/offline selection protocol is documented for every algorithm.",
            }
        )

    if "ModernTCN_small_base" not in by_recipe:
        entries.append(
            {
                "algorithm_recipe": "ModernTCN_small_base",
                "selected_candidate_id": "pending",
                "seed": "pending",
                "selection_protocol": "same_protocol_not_yet_available",
                "J_control": math.nan,
                "selected_model_status": "pending_until_modern_base_closed_loop_available",
                "notes": "Need ModernTCN_small base seed21/42/101 closed-loop to select by the same rule.",
            }
        )
    return entries


def evidence_inventory() -> list[dict[str, Any]]:
    items = [
        ("offline_multiseed_13", OFFLINE_13, "offline seed table from node 13"),
        ("closed_loop_current_13", CLOSED_13, "existing current-v2 closed-loop aggregate from node 13"),
        ("replacement_path_metrics_12", PATH_12, "path-level uncertainty same-recipe closed-loop evidence"),
        ("stability_closed_loop_14", CLOSED_14, "stability recipe closed-loop aggregate"),
        ("stability_path_metrics_14", PATH_14, "stability recipe path metrics"),
        ("stability_offline_14", OFFLINE_14, "stability recipe offline metrics"),
        ("bi_bu_a2_offline_15", A2_OFFLINE_15, "BI-BU A2 offline screen"),
        ("bi_bu_a2_sentinel_15", A2_SENTINEL_15, "BI-BU A2 sentinel aggregate"),
        ("bi_bu_a2_path_15", A2_PATH_15, "BI-BU A2 sentinel path metrics"),
        ("bi_bu_final_decision_15", FINAL_15, "BI-BU final decision"),
        ("modern_base_seed42_training_16", MODERN_BASE_TRAIN_42, "new ModernTCN_small base seed42 training output"),
        ("modern_base_exports_16", MODERN_BASE_EXPORTS, "new ModernTCN_small base seed21/42/101 ONNX exports"),
        ("modern_base_closed_loop_results_16", MODERN_BASE_CLOSED_RESULTS, "new ModernTCN_small base closed-loop aggregate"),
        ("modern_base_path_metrics_16", MODERN_BASE_PATH_METRICS, "new ModernTCN_small base path metrics"),
    ]
    rows = []
    for evidence_id, path, notes in items:
        rows.append(
            {
                "evidence_id": evidence_id,
                "exists": path.exists(),
                "path": str(path),
                "size_bytes": path.stat().st_size if path.exists() else math.nan,
                "notes": notes,
            }
        )
    return rows


def build_report(
    deployment_rows: list[dict[str, Any]],
    seed_rows: list[dict[str, Any]],
    recipe_rows: list[dict[str, Any]],
    selected_rows: list[dict[str, Any]],
    missing_rows: list[dict[str, Any]],
) -> str:
    a2_rows = [r for r in seed_rows if r["algorithm_recipe"] == "BI_BU_A2_freeze_early" and r["seed"] in {21, 42}]
    base_recipe = next((r for r in recipe_rows if r["algorithm_recipe"] == "ModernTCN_small_base"), {})
    uncertainty_recipe = next((r for r in recipe_rows if r["algorithm_recipe"] == "Uncertainty_weighted_same_recipe"), {})
    anchor_row = next((r for r in deployment_rows if r["candidate_id"] == "uncertainty_seed101_rerun_20260622"), {})
    base_selected = next((r for r in selected_rows if r["algorithm_recipe"] == "ModernTCN_small_base"), {})
    uncertainty_selected = next((r for r in selected_rows if r["algorithm_recipe"] == "Uncertainty_weighted_same_recipe"), {})

    base_complete = (
        base_recipe.get("missing_offline_target_seeds") == "none"
        and base_recipe.get("missing_closed_loop_target_seeds") == "none"
        and int(num(base_recipe.get("closed_loop_count"))) == len(TARGET_SEEDS)
    )
    uncertainty_complete = (
        uncertainty_recipe.get("missing_offline_target_seeds") == "none"
        and uncertainty_recipe.get("missing_closed_loop_target_seeds") == "none"
        and int(num(uncertainty_recipe.get("closed_loop_count"))) == len(TARGET_SEEDS)
    )
    if base_complete and uncertainty_complete:
        base_mean = num(base_recipe.get("mean_J_control"))
        uncertainty_mean = num(uncertainty_recipe.get("mean_J_control"))
        winner = "Uncertainty_weighted_same_recipe" if uncertainty_mean < base_mean else "ModernTCN_small_base"
        recipe_answer = (
            f"complete. Lower mean J_control is better; winner by mean J_control is `{winner}` "
            f"(ModernTCN_small_base={base_mean:.6f}, Uncertainty_weighted_same_recipe={uncertainty_mean:.6f})."
        )
    else:
        recipe_answer = (
            "pending. ModernTCN_small base and Uncertainty-weighted recipe do not both have complete "
            "seed21/42/101 same-path closed-loop distributions yet."
        )

    if math.isfinite(num(base_selected.get("J_control"))) and math.isfinite(num(uncertainty_selected.get("J_control"))):
        selected_answer = (
            "diagnostic selected-best table is available: "
            f"ModernTCN_small_base `{base_selected.get('selected_candidate_id')}` J={num(base_selected.get('J_control')):.6f}; "
            f"Uncertainty_weighted_same_recipe `{uncertainty_selected.get('selected_candidate_id')}` "
            f"J={num(uncertainty_selected.get('J_control')):.6f}. "
            "Paper-valid selected-best claims still require a common validation/offline selection protocol."
        )
    else:
        selected_answer = "pending until both recipes have selectable candidates under the same protocol."

    text = f"""# Recipe vs Deployment Comparison

## Core Decision

1. Deployment champion replacement: `uncertainty_seed101_rerun_20260622` has `J_control={num(anchor_row.get('J_control')):.6f}` versus locked champion `1.000000`; status is `{anchor_row.get('deployment_champion_gate_status', 'unavailable')}`. BI-BU A2 seed21/42 remain deployment-gate failures.
2. Recipe-level multiseed comparison: {recipe_answer}
3. Selected-best comparison: {selected_answer}

## A2 Required Status Fields

{md_table(a2_rows, ['algorithm_recipe', 'seed', 'J_control', 'deployment_champion_gate_status', 'recipe_multiseed_status', 'selected_model_status', 'deployment_champion_gate_reason'])}

## Deployment Champion Comparison

{md_table(deployment_rows, ['algorithm_recipe', 'candidate_id', 'seed', 'evidence_scope', 'J_control', 'worst_path_J', 'path_catastrophic_count', 'deployment_champion_gate_status', 'deployment_champion_gate_reason'])}

## Recipe Multiseed Summary

{md_table(recipe_rows, ['algorithm_recipe', 'target_seed_set', 'available_seed_rows', 'missing_offline_target_seeds', 'missing_closed_loop_target_seeds', 'offline_pass_count', 'closed_loop_count', 'mean_J_control', 'median_J_control', 'best_J_control', 'worst_J_control', 'std_J_control', 'deployment_pass_rate_vs_champion', 'path_catastrophic_count', 'recipe_multiseed_status'])}

## Selected-best Comparison

{md_table(selected_rows, ['algorithm_recipe', 'selected_candidate_id', 'seed', 'selection_protocol', 'J_control', 'selected_model_status'])}

## Missing Experiments

{md_table(missing_rows, ['algorithm_recipe', 'seed', 'checkpoint_exists', 'offline_status', 'closed_loop_status', 'required_action'])}

## Interpretation

- Do not use the locked ModernTCN_small champion alone to declare Uncertainty or BI-BU recipe-level failure.
- It is valid to say A2 seed21/42 failed the deployment champion replacement gate.
- Recipe-level claims use the identical seed set `21/42/101`, identical path set, and identical `J_control` definition.
- Selected-best claims are diagnostic unless the seed selection protocol is validation/offline-only and applied equally to every algorithm.

## Method Notes

- Deployment gate here is `mean J_control <= 1.0` and no path-level catastrophic failure.
- Path-level catastrophic failure uses the existing sentinel flag where available; otherwise it is counted when path-level `J_control > 1.5`.
- Recipe-level status remains pending whenever either ModernTCN_small base or Uncertainty-weighted seed21/42/101 closed-loop distribution is unavailable.

## Outputs

- Evidence inventory: `results/modern_tcn_metric_rebuild/16_recipe_vs_deployment_comparison/00_evidence_inventory/evidence_inventory.csv`
- Seed-level status table: `results/modern_tcn_metric_rebuild/16_recipe_vs_deployment_comparison/01_seed_level_status/seed_level_gate_status.csv`
- Deployment comparison: `results/modern_tcn_metric_rebuild/16_recipe_vs_deployment_comparison/02_deployment_champion/deployment_champion_comparison.csv`
- Recipe summary: `results/modern_tcn_metric_rebuild/16_recipe_vs_deployment_comparison/03_recipe_multiseed/recipe_multiseed_summary.csv`
- Selected-best comparison: `results/modern_tcn_metric_rebuild/16_recipe_vs_deployment_comparison/04_selected_best/selected_best_comparison.csv`
- Missing experiment manifest: `results/modern_tcn_metric_rebuild/16_recipe_vs_deployment_comparison/05_missing_experiments/modern_tcn_small_required_closed_loop.csv`
- ModernTCN base closed-loop aggregate: `results/modern_tcn_metric_rebuild/16_recipe_vs_deployment_comparison/09_modern_base_closed_loop/closed_loop_results.csv`
"""
    return text


def main() -> None:
    NODE_ROOT.mkdir(parents=True, exist_ok=True)
    path_rows = collect_path_rows()
    deployment_rows = collect_deployment_rows(path_rows)
    modern_base_path_rows = [r for r in path_rows if r.get("source_scope") == "modern_base_recipe_16"]
    modern_base_deployment_rows = [
        r for r in deployment_rows if r.get("algorithm_recipe") == "ModernTCN_small_base"
    ]
    write_csv(
        MODERN_BASE_PATH_METRICS,
        modern_base_path_rows,
        [
            "source_scope",
            "candidate_id",
            "raw_candidate_id",
            "path_tag",
            "J_control_path",
            "path_fail",
            "path_catastrophic",
            "ey_rmse",
            "xy_rmse",
            "epsi_rmse",
            "j_du",
            "omega_cmd_rms",
            "source_file",
        ],
    )
    write_csv(
        MODERN_BASE_CLOSED_RESULTS,
        modern_base_deployment_rows,
        [
            "algorithm_recipe",
            "candidate_id",
            "seed",
            "evidence_scope",
            "n_paths",
            "J_control",
            "path_count",
            "worst_path_J",
            "path_fail_count",
            "path_catastrophic_count",
            "deployment_champion_gate_status",
            "deployment_champion_gate_reason",
            "source_file",
        ],
    )
    inventory = evidence_inventory()
    seed_rows = build_seed_status_rows(deployment_rows)
    recipe_rows = build_recipe_summary(seed_rows, deployment_rows)
    selected_rows = build_selected_best_rows(deployment_rows)
    missing_rows = build_missing_experiments(seed_rows)

    write_csv(
        NODE_ROOT / "00_evidence_inventory" / "evidence_inventory.csv",
        inventory,
        ["evidence_id", "exists", "path", "size_bytes", "notes"],
    )
    write_json(
        NODE_ROOT / "00_evidence_inventory" / "comparison_contract.json",
        {
            "baseline_champion": "baseline_lock",
            "baseline_J_control": BASELINE_J,
            "target_seed_set": TARGET_SEEDS,
            "path_set": PATH_TAGS,
            "decision_axes": [
                "deployment_champion_gate_status",
                "recipe_multiseed_status",
                "selected_model_status",
            ],
            "deployment_gate_rule": "mean_J_control <= 1.0 and path_catastrophic_count == 0",
            "path_catastrophic_definition": "existing sentinel flag when available; otherwise path-level J_control > 1.5",
            "missing_policy": "missing values are explicit; no baseline or zero imputation",
        },
    )
    write_csv(
        NODE_ROOT / "01_seed_level_status" / "seed_level_gate_status.csv",
        seed_rows,
        [
            "algorithm_recipe",
            "seed",
            "required_for_recipe_comparison",
            "offline_variant_id",
            "offline_status",
            "offline_score",
            "offline_failures",
            "candidate_id",
            "closed_loop_scope",
            "J_control",
            "worst_path_J",
            "path_fail_count",
            "path_catastrophic_count",
            "deployment_champion_gate_status",
            "deployment_champion_gate_reason",
            "recipe_multiseed_status",
            "selected_model_status",
            "checkpoint_file",
            "offline_source_file",
            "closed_loop_source_file",
        ],
    )
    write_csv(
        NODE_ROOT / "02_deployment_champion" / "deployment_champion_comparison.csv",
        deployment_rows,
        [
            "algorithm_recipe",
            "candidate_id",
            "seed",
            "evidence_scope",
            "n_paths",
            "J_control",
            "path_count",
            "worst_path_J",
            "path_fail_count",
            "path_catastrophic_count",
            "deployment_champion_gate_status",
            "deployment_champion_gate_reason",
            "source_file",
        ],
    )
    write_csv(
        NODE_ROOT / "02_deployment_champion" / "path_level_gate_table.csv",
        path_rows,
        [
            "source_scope",
            "candidate_id",
            "raw_candidate_id",
            "path_tag",
            "J_control_path",
            "path_fail",
            "path_catastrophic",
            "ey_rmse",
            "xy_rmse",
            "epsi_rmse",
            "j_du",
            "omega_cmd_rms",
            "source_file",
        ],
    )
    write_csv(
        NODE_ROOT / "03_recipe_multiseed" / "recipe_multiseed_summary.csv",
        recipe_rows,
        [
            "algorithm_recipe",
            "target_seed_set",
            "available_seed_rows",
            "extra_non_target_seeds",
            "missing_offline_target_seeds",
            "missing_closed_loop_target_seeds",
            "offline_pass_count",
            "closed_loop_count",
            "mean_J_control",
            "median_J_control",
            "best_J_control",
            "worst_J_control",
            "std_J_control",
            "deployment_pass_rate_vs_champion",
            "path_catastrophic_count",
            "recipe_multiseed_status",
            "notes",
        ],
    )
    write_csv(
        NODE_ROOT / "04_selected_best" / "selected_best_comparison.csv",
        selected_rows,
        [
            "algorithm_recipe",
            "selected_candidate_id",
            "seed",
            "selection_protocol",
            "J_control",
            "selected_model_status",
            "notes",
        ],
    )
    write_csv(
        NODE_ROOT / "05_missing_experiments" / "modern_tcn_small_required_closed_loop.csv",
        missing_rows,
        [
            "algorithm_recipe",
            "seed",
            "checkpoint_exists",
            "checkpoint_file",
            "offline_status",
            "closed_loop_status",
            "required_path_set",
            "required_action",
            "reason",
        ],
    )

    base_recipe = next((r for r in recipe_rows if r["algorithm_recipe"] == "ModernTCN_small_base"), {})
    uncertainty_recipe = next(
        (r for r in recipe_rows if r["algorithm_recipe"] == "Uncertainty_weighted_same_recipe"), {}
    )
    anchor_row = next((r for r in deployment_rows if r["candidate_id"] == "uncertainty_seed101_rerun_20260622"), {})
    base_complete = (
        base_recipe.get("missing_offline_target_seeds") == "none"
        and base_recipe.get("missing_closed_loop_target_seeds") == "none"
        and int(num(base_recipe.get("closed_loop_count"))) == len(TARGET_SEEDS)
    )
    uncertainty_complete = (
        uncertainty_recipe.get("missing_offline_target_seeds") == "none"
        and uncertainty_recipe.get("missing_closed_loop_target_seeds") == "none"
        and int(num(uncertainty_recipe.get("closed_loop_count"))) == len(TARGET_SEEDS)
    )
    if base_complete and uncertainty_complete:
        base_mean = num(base_recipe.get("mean_J_control"))
        uncertainty_mean = num(uncertainty_recipe.get("mean_J_control"))
        if uncertainty_mean < base_mean:
            recipe_answer = "complete_uncertainty_weighted_recipe_better_by_mean_J_control"
        else:
            recipe_answer = "complete_uncertainty_weighted_recipe_not_better_by_mean_J_control"
    else:
        recipe_answer = "pending_until_both_recipe_seed21_42_101_same_path_closed_loop_available"

    final_decision = {
        "baseline_J_control": BASELINE_J,
        "anchor_seed101_J_control": num(anchor_row.get("J_control")) if anchor_row else ANCHOR_J,
        "deployment_champion_answer": "uncertainty_seed101_rerun_20260622 passes; BI-BU A2 seed21/42 fail; non-anchor candidates are reported individually.",
        "recipe_multiseed_answer": recipe_answer,
        "selected_best_answer": "diagnostic_selected_best_available_if_rows_have_J_control; paper_valid_only_with_common_validation_or_offline_selection_protocol",
        "modern_base_recipe_summary": base_recipe,
        "uncertainty_weighted_recipe_summary": uncertainty_recipe,
        "a2_seed21_status": {
            "deployment_champion_gate_status": "fail",
            "recipe_multiseed_status": "sentinel_failed_no_full_recipe_claim",
            "selected_model_status": "not_applicable_for_individual_seed",
        },
        "a2_seed42_status": {
            "deployment_champion_gate_status": "fail",
            "recipe_multiseed_status": "sentinel_failed_no_full_recipe_claim",
            "selected_model_status": "not_applicable_for_individual_seed",
        },
        "required_next_experiments": [
            {
                "algorithm_recipe": row["algorithm_recipe"],
                "seed": row["seed"],
                "required_action": row["required_action"],
            }
            for row in missing_rows
        ],
    }
    write_json(NODE_ROOT / "06_report" / "final_decision.json", final_decision)
    write_text(
        NODE_ROOT / "06_report" / "recipe_vs_deployment_comparison_report.md",
        build_report(deployment_rows, seed_rows, recipe_rows, selected_rows, missing_rows),
    )

    print(f"Wrote {NODE_ROOT}")
    print(f"deployment_rows={len(deployment_rows)} seed_rows={len(seed_rows)} missing_experiments={len(missing_rows)}")


if __name__ == "__main__":
    main()
