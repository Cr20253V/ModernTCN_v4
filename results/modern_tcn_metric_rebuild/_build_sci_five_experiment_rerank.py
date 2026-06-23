from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parent
SCI_ROOT = ROOT.parent / "modern_tcn_sci_innovation"
OUT_ROOT = ROOT / "11_sci_five_experiment_rerank"

REGISTRY = ROOT / "03_rerank_existing_experiments" / "candidate_registry.csv"
MATRIX = ROOT / "03_rerank_existing_experiments" / "candidate_metric_matrix.csv"
CLASSES = ROOT / "04_candidate_decision" / "candidate_classes.csv"
WEIGHTS_FILE = ROOT / "02_metric_freeze" / "metric_vFinal_control_oriented_frozen.json"
THRESHOLDS_FILE = ROOT / "02_metric_freeze" / "hard_constraint_thresholds.json"
FORMAL_AGG = ROOT / "05_sandbox_closed_loop_if_needed" / "03_formal_validation" / "formal_validation_aggregate.csv"
FORMAL_DECISION = ROOT / "05_sandbox_closed_loop_if_needed" / "03_formal_validation" / "formal_validation_class_c_decision.csv"
FORMAL_PATH_RUNS = ROOT / "05_sandbox_closed_loop_if_needed" / "03_formal_validation" / "formal_path_runs.csv"
SANDBOX_MANIFEST = ROOT / "05_sandbox_closed_loop_if_needed" / "sandbox_candidate_manifest.csv"
E2_DECISION = ROOT / "02_e2_smooth_fixed" / "e2_smooth_fixed_decision.json"
E5_DECISION = ROOT / "05_e5_replay_fixed" / "e5_replay_fixed_decision.json"
INVALID_REGISTRY = ROOT / "00_replay_contract_repair" / "invalid_evidence_registry.csv"

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
STRICT_REQUIRED = [
    "ey_rmse_mean",
    "xy_rmse_mean",
    "epsi_rmse_mean",
    "j_du_mean",
    "omega_cmd_rms_mean",
    "viol_rate_mean",
    "main_acc_pct_mean",
    "theta_mae_deg_mean",
]

RERUN_CANDIDATES = {
    "uncertainty_seed101_rerun_20260622": {
        "source_phase": "E1_loss_optimization",
        "run_tag": "uncertainty_seed101_rerun_20260622",
        "source_run_tag": "uncertainty_seed101",
        "model_family": "ModernTCN_small",
        "actual_method": "loss_mode=uncertainty_weighting",
        "loss_mode": "loss_mode=uncertainty_weighting",
        "source_dir": SCI_ROOT / "01_loss_optimization" / "uncertainty_seed101_rerun_20260622",
        "metrics_file": SCI_ROOT / "01_loss_optimization" / "uncertainty_seed101_rerun_20260622" / "metrics_test.csv",
        "report_file": SCI_ROOT / "01_loss_optimization" / "uncertainty_seed101_rerun_20260622" / "ModernTCN_train_report.md",
        "config_file": SCI_ROOT / "01_loss_optimization" / "uncertainty_seed101_rerun_20260622" / "config.json",
        "supersedes": "uncertainty_seed101",
    },
    "mode_theta_detach_flatreg001_seed21_rerun_20260622": {
        "source_phase": "E4_mode_conditioned_theta",
        "run_tag": "mode_theta_detach_flatreg001_seed21_rerun_20260622",
        "source_run_tag": "mode_theta_detach_flatreg001_seed21",
        "model_family": "ModernTCNModeTheta",
        "actual_method": "mode_theta_detach_flatreg=0.01",
        "loss_mode": "mode_theta_detach_flatreg=0.01",
        "source_dir": SCI_ROOT / "04_mode_conditioned_theta" / "mode_theta_detach_flatreg001_seed21_rerun_20260622",
        "metrics_file": SCI_ROOT / "04_mode_conditioned_theta" / "mode_theta_detach_flatreg001_seed21_rerun_20260622" / "metrics_test.csv",
        "report_file": SCI_ROOT / "04_mode_conditioned_theta" / "mode_theta_detach_flatreg001_seed21_rerun_20260622" / "ModernTCNModeTheta_train_report.md",
        "config_file": SCI_ROOT / "04_mode_conditioned_theta" / "mode_theta_detach_flatreg001_seed21_rerun_20260622" / "config.json",
        "supersedes": "mode_theta_detach_flatreg001_seed21",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"
        if math.isinf(value):
            return "Inf" if value > 0 else "-Inf"
        return f"{value:.15g}"
    if isinstance(value, list):
        return ";".join(fmt(v) for v in value)
    text = str(value)
    return text if text else "NaN"


def num(value: Any) -> float:
    if value is None:
        return float("nan")
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none"}:
        return float("nan")
    return float(text)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def rel(path: Path | str | None) -> str:
    if path is None:
        return "NaN"
    path = Path(str(path))
    try:
        return str(path.resolve().relative_to(ROOT.parent.parent.resolve()))
    except Exception:
        return str(path)


def abs_path(text: str | None) -> Path | None:
    if text is None:
        return None
    stripped = str(text).strip()
    if not stripped or stripped.lower() in {"nan", "none"}:
        return None
    return Path(stripped)


def phase_run_dir(source_phase: str, run_tag: str) -> Path:
    mapping = {
        "E0_baseline_lock": SCI_ROOT / "00_baseline_lock",
        "E1_loss_optimization": SCI_ROOT / "01_loss_optimization" / run_tag,
        "E2_hard_sample_loss": SCI_ROOT / "02_hard_sample_loss" / run_tag,
        "E3_physics_group_gate": SCI_ROOT / "03_physics_group_gate" / run_tag,
        "E4_mode_conditioned_theta": SCI_ROOT / "04_mode_conditioned_theta" / run_tag,
        "E5_confidence_scheduling": SCI_ROOT / "05_confidence_scheduling" / run_tag,
    }
    return mapping[source_phase]


def first_existing(paths: list[Path]) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def infer_metrics_file(source_phase: str, run_tag: str, run_dir: Path) -> Path | None:
    if source_phase == "E0_baseline_lock":
        return first_existing([run_dir / "baseline_offline_metrics.csv"])
    if source_phase == "E5_confidence_scheduling":
        return first_existing([run_dir / f"{run_tag}_offline_metrics.csv"])
    return first_existing([run_dir / "metrics_test.csv"])


def infer_report_file(source_phase: str, run_tag: str, run_dir: Path) -> Path | None:
    candidates = [
        run_dir / "ModernTCN_train_report.md",
        run_dir / "ModernTCNModeTheta_train_report.md",
        run_dir / "ModernTCNPhysicsGroupGate_train_report.md",
        run_dir / f"{run_tag}_offline_summary.md",
    ]
    if source_phase == "E0_baseline_lock":
        candidates.append(run_dir / "e0_baseline_lock.md")
    return first_existing(candidates)


def infer_config_file(source_phase: str, run_dir: Path) -> Path | None:
    if source_phase == "E0_baseline_lock":
        return first_existing([run_dir / "e0_decision.json"])
    return first_existing([run_dir / "config.json"])


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot_sources(paths: list[Path]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for path in sorted({p for p in paths if p and p.exists()}):
        stat = path.stat()
        rows[str(path.resolve())] = {
            "path": str(path.resolve()),
            "exists": True,
            "size_bytes": stat.st_size,
            "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
            "sha256": sha256(path),
        }
    return rows


def hash_diff(before: dict[str, dict[str, Any]], after: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in sorted(before):
        b = before[key]
        a = after.get(key, {})
        unchanged = bool(a) and b.get("sha256") == a.get("sha256") and b.get("size_bytes") == a.get("size_bytes")
        rows.append(
            {
                "path": key,
                "exists_before": True,
                "exists_after": bool(a),
                "size_before": b.get("size_bytes"),
                "size_after": a.get("size_bytes", "NaN"),
                "sha256_before": b.get("sha256"),
                "sha256_after": a.get("sha256", "NaN"),
                "unchanged": unchanged,
            }
        )
    return rows


def file_exists(path: Path | None) -> bool:
    return bool(path) and path.exists()


def read_first_csv(path: Path | None) -> dict[str, str]:
    if not path or not path.exists():
        return {}
    rows = read_csv(path)
    return rows[0] if rows else {}


def offline_cost(value: float, baseline: float, metric: str) -> float:
    if not math.isfinite(value) or not math.isfinite(baseline) or abs(baseline) < 1e-12:
        return float("nan")
    if metric in HIGHER_BETTER:
        return max(0.0, (baseline - value) / abs(baseline))
    return value / abs(baseline)


def offline_score(row: dict[str, Any], baseline: dict[str, Any], weights: dict[str, float]) -> tuple[float, int, str]:
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
    return (weighted_sum / used_weight if used_weight else float("nan"), len(missing), ";".join(missing) if missing else "none")


def competition_ranks(rows: list[dict[str, Any]], key: str, rank_key: str) -> None:
    current_rank = 0
    previous = None
    for index, row in enumerate(rows, start=1):
        value = num(row.get(key))
        if previous is None or not math.isclose(value, previous, rel_tol=0.0, abs_tol=1e-12):
            current_rank = index
            previous = value
        row[rank_key] = current_rank


def build_formal_maps() -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]], dict[str, list[str]]]:
    agg = {row["controller"]: row for row in read_csv(FORMAL_AGG)}
    dec = {row["controller"]: row for row in read_csv(FORMAL_DECISION)}
    mat_map: dict[str, list[str]] = {}
    for row in read_csv(FORMAL_PATH_RUNS):
        baseline = row.get("baseline_file", "")
        if baseline:
            mat_map.setdefault("baseline_lock", []).append(baseline)
        for item in row.get("candidate_files", "").split(";"):
            item = item.strip()
            if not item:
                continue
            name = Path(item).name
            controller = name.removesuffix("_out.mat")
            mat_map.setdefault(controller, []).append(item)
    return agg, dec, mat_map


def build_manifest_maps() -> dict[str, dict[str, str]]:
    if not SANDBOX_MANIFEST.exists():
        return {}
    return {row["candidate_id"]: row for row in read_csv(SANDBOX_MANIFEST)}


def main() -> int:
    weights = read_json(WEIGHTS_FILE)["weights"]
    thresholds = read_json(THRESHOLDS_FILE)
    registry_rows = read_csv(REGISTRY)
    matrix_rows = {row["candidate_id"]: row for row in read_csv(MATRIX)}
    class_rows = {row["candidate_id"]: row for row in read_csv(CLASSES)}
    formal_agg, formal_decision, formal_mats = build_formal_maps()
    manifest = build_manifest_maps()

    source_paths = [
        REGISTRY,
        MATRIX,
        CLASSES,
        WEIGHTS_FILE,
        THRESHOLDS_FILE,
        FORMAL_AGG,
        FORMAL_DECISION,
        FORMAL_PATH_RUNS,
        SANDBOX_MANIFEST,
        E2_DECISION,
        E5_DECISION,
        INVALID_REGISTRY,
    ]

    candidates: dict[str, dict[str, Any]] = {}
    for row in registry_rows:
        candidate_id = row["candidate_id"]
        source_phase = row["source_phase"]
        run_tag = row["run_tag"]
        run_dir = phase_run_dir(source_phase, run_tag)
        metrics_file = infer_metrics_file(source_phase, run_tag, run_dir)
        report_file = infer_report_file(source_phase, run_tag, run_dir)
        config_file = infer_config_file(source_phase, run_dir)
        checkpoint = abs_path(row.get("checkpoint_path_if_available"))
        matrix = matrix_rows.get(candidate_id, {})
        if candidate_id == "baseline_lock":
            baseline_metrics = read_first_csv(metrics_file)
            checkpoint = abs_path(baseline_metrics.get("checkpoint_file")) or checkpoint
            onnx = abs_path(baseline_metrics.get("onnx_file"))
        else:
            onnx = None
        candidates[candidate_id] = {
            **row,
            "candidate_id": candidate_id,
            "source_phase": source_phase,
            "run_tag": run_tag,
            "source_dir": run_dir,
            "config_file": config_file,
            "metrics_file": metrics_file,
            "report_file": report_file,
            "checkpoint_path": checkpoint,
            "onnx_file": onnx,
            "closed_loop_mat_files": formal_mats.get(candidate_id, []),
            "offline_metrics": matrix,
            "is_rerun_20260622": False,
            "superseded_by": "",
        }
        for p in [config_file, metrics_file, report_file, checkpoint, onnx]:
            if p:
                source_paths.append(p)

    for candidate_id, spec in RERUN_CANDIDATES.items():
        metrics = read_first_csv(spec["metrics_file"])
        checkpoint = abs_path(metrics.get("checkpoint_file"))
        manifest_row = manifest.get(candidate_id, {})
        onnx = abs_path(manifest_row.get("onnx_file"))
        offline = {metric: metrics.get(metric, "NaN") for metric in OFFLINE_METRICS}
        candidates[candidate_id] = {
            "candidate_id": candidate_id,
            "source_phase": spec["source_phase"],
            "run_tag": spec["run_tag"],
            "model_family": spec["model_family"],
            "loss_mode": spec["loss_mode"],
            "checkpoint_path_if_available": str(checkpoint) if checkpoint else "NaN",
            "has_offline_metrics": "true",
            "has_closed_loop_metrics": str(candidate_id in formal_agg).lower(),
            "has_onnx": str(file_exists(onnx)).lower(),
            "has_matlab": str(bool(formal_mats.get(candidate_id))).lower(),
            "original_gate_status": "rerun_20260622",
            "original_promotion_status": "strict_repair_candidate",
            "notes": "reused existing rerun_20260622 evidence; original source run not overwritten",
            "evidence_validity": "historical_valid",
            "actual_method": spec["actual_method"],
            "smoothness_loss_valid": "not_applicable",
            "scheduling_replay_valid": "not_applicable",
            "advisory_only": "false",
            "invalid_reason": "NaN",
            "repair_required_for_formal_use": "false",
            "is_reference_baseline": "false",
            "is_candidate": "true",
            "repair_status": "reused_existing_rerun_20260622",
            "metric_missing_ratio": "0",
            "source_dir": spec["source_dir"],
            "config_file": spec["config_file"],
            "metrics_file": spec["metrics_file"],
            "report_file": spec["report_file"],
            "checkpoint_path": checkpoint,
            "onnx_file": onnx,
            "closed_loop_mat_files": formal_mats.get(candidate_id, []),
            "offline_metrics": offline,
            "is_rerun_20260622": True,
            "supersedes": spec["supersedes"],
            "superseded_by": "",
        }
        if spec["supersedes"] in candidates:
            candidates[spec["supersedes"]]["superseded_by"] = candidate_id
        for p in [spec["config_file"], spec["metrics_file"], spec["report_file"], checkpoint, onnx]:
            if p:
                source_paths.append(p)
        for p in formal_mats.get(candidate_id, []):
            source_paths.append(Path(p))

    for p in formal_mats.get("baseline_lock", []):
        source_paths.append(Path(p))
    before_hashes = snapshot_sources(source_paths)

    baseline = matrix_rows["baseline_lock"]
    inventory_rows: list[dict[str, Any]] = []
    offline_rows: list[dict[str, Any]] = []
    repair_rows: list[dict[str, Any]] = []

    for candidate_id, item in candidates.items():
        advisory = boolish(item.get("advisory_only"))
        source_phase = item["source_phase"]
        evidence_validity = item.get("evidence_validity", "historical_valid")
        has_checkpoint = file_exists(item.get("checkpoint_path"))
        has_offline = file_exists(item.get("metrics_file")) or bool(item.get("offline_metrics"))
        has_onnx = file_exists(item.get("onnx_file"))
        has_closed_loop = bool(item.get("closed_loop_mat_files")) and all(Path(p).exists() for p in item.get("closed_loop_mat_files", []))
        is_reference = boolish(item.get("is_reference_baseline"))

        if is_reference:
            evidence_tier = "full"
        elif advisory or evidence_validity == "advisory_only" or source_phase == "E5_confidence_scheduling":
            evidence_tier = "advisory_only"
            evidence_validity = "advisory_only"
        elif evidence_validity == "degraded" or source_phase == "E2_hard_sample_loss":
            evidence_tier = "degraded"
            evidence_validity = "degraded"
        elif not has_checkpoint:
            evidence_tier = "missing_checkpoint"
        elif has_offline and has_checkpoint and has_onnx and has_closed_loop:
            evidence_tier = "full"
        else:
            evidence_tier = "offline_only"

        off = dict(item.get("offline_metrics") or {})
        score, missing_count, missing_metrics = offline_score(off, baseline, weights)
        missing_ratio = missing_count / len(OFFLINE_METRICS)
        prior_class = class_rows.get(candidate_id, {})
        include_offline = (
            not is_reference
            and evidence_tier in {"full", "offline_only", "degraded", "missing_checkpoint"}
            and has_offline
            and math.isfinite(score)
        )
        rank_eligible = (
            include_offline
            and file_exists(item.get("config_file"))
            and has_offline
            and file_exists(item.get("report_file"))
            and has_checkpoint
        )
        inventory_rows.append(
            {
                "candidate_id": candidate_id,
                "source_phase": source_phase,
                "run_tag": item["run_tag"],
                "evidence_tier": evidence_tier,
                "evidence_validity": evidence_validity,
                "actual_method": item.get("actual_method", "NaN"),
                "repair_status": item.get("repair_status", "HISTORICAL"),
                "superseded_by": item.get("superseded_by", ""),
                "is_rerun_20260622": item.get("is_rerun_20260622", False),
                "has_config": file_exists(item.get("config_file")),
                "has_metrics": has_offline,
                "has_report": file_exists(item.get("report_file")),
                "has_checkpoint": has_checkpoint,
                "has_onnx": has_onnx,
                "has_closed_loop_mat": has_closed_loop,
                "closed_loop_mat_count": len(item.get("closed_loop_mat_files", [])),
                "config_file": rel(item.get("config_file")),
                "metrics_file": rel(item.get("metrics_file")),
                "report_file": rel(item.get("report_file")),
                "checkpoint_path": rel(item.get("checkpoint_path")),
                "onnx_file": rel(item.get("onnx_file")),
                "closed_loop_mat_files": [rel(p) for p in item.get("closed_loop_mat_files", [])],
                "offline_proxy_score": score if include_offline else float("nan"),
                "offline_metric_missing_ratio": missing_ratio,
                "offline_missing_metrics": missing_metrics,
                "prior_class_label": prior_class.get("class_label", "NaN"),
                "prior_eligible_for_class_b": prior_class.get("eligible_for_class_b", "false"),
                "advisory_only": evidence_tier == "advisory_only",
            }
        )
        if include_offline:
            offline_rows.append(
                {
                    "candidate_id": candidate_id,
                    "source_phase": source_phase,
                    "run_tag": item["run_tag"],
                    "evidence_validity": evidence_validity,
                    "evidence_tier": evidence_tier,
                    "repair_status": item.get("repair_status", "HISTORICAL"),
                    "superseded_by": item.get("superseded_by", ""),
                    "offline_proxy_score": score,
                    "metric_missing_ratio": missing_ratio,
                    "missing_metrics": missing_metrics,
                    "prior_class_label": prior_class.get("class_label", "NaN"),
                    "rank_eligible": rank_eligible,
                    "has_config": file_exists(item.get("config_file")),
                    "has_metrics": has_offline,
                    "has_report": file_exists(item.get("report_file")),
                    "has_checkpoint": has_checkpoint,
                    "eligible_for_strict_repair": boolish(prior_class.get("eligible_for_sandbox")) and not item.get("superseded_by"),
                    **{metric: off.get(metric, "NaN") for metric in OFFLINE_METRICS},
                }
            )
        if (
            not is_reference
            and source_phase != "E5_confidence_scheduling"
            and evidence_tier != "full"
            and boolish(prior_class.get("eligible_for_sandbox"))
            and not item.get("superseded_by")
        ):
            repair_rows.append(
                {
                    "candidate_id": candidate_id,
                    "source_phase": source_phase,
                    "missing_checkpoint": not has_checkpoint,
                    "missing_onnx": not has_onnx,
                    "missing_closed_loop_mat": not has_closed_loop,
                    "repair_decision": "not_run_in_this_node",
                    "reason": "existing_top2_rerun_20260622_formal_validation_completed; candidate remains offline_only unless a new strict-repair node is opened",
                }
            )

    offline_rows.sort(key=lambda row: (num(row["offline_proxy_score"]), row["candidate_id"]))
    competition_ranks(offline_rows, "offline_proxy_score", "offline_proxy_score_rank_all")
    offline_rank_rows = [dict(row) for row in offline_rows if boolish(row.get("rank_eligible"))]
    offline_rank_rows.sort(key=lambda row: (num(row["offline_proxy_score"]), row["candidate_id"]))
    competition_ranks(offline_rank_rows, "offline_proxy_score", "offline_proxy_rank")

    strict_rows: list[dict[str, Any]] = []
    for controller, agg in formal_agg.items():
        decision = formal_decision.get(controller, {})
        item = candidates.get(controller, {})
        missing = [key for key in STRICT_REQUIRED if not math.isfinite(num(agg.get(key)))]
        strict_rows.append(
            {
                "candidate_id": controller,
                "source_phase": item.get("source_phase", "E0_baseline_lock" if controller == "baseline_lock" else "unknown"),
                "evidence_validity": "reference" if controller == "baseline_lock" else "full",
                "repair_status": "PASS_REFERENCE" if controller == "baseline_lock" else "reused_existing_rerun_20260622",
                "J_control": decision.get("J_control", "NaN"),
                "hard_constraint_status": decision.get("hard_constraint_status", "NaN"),
                "eligible_for_class_c": decision.get("eligible_for_class_c", "false"),
                "class_c_status": decision.get("class_c_status", "NaN"),
                "class_c_reason": decision.get("class_c_reason", "NaN"),
                "metric_missing_ratio": len(missing) / len(STRICT_REQUIRED),
                "missing_metrics": ";".join(missing) if missing else "none",
                "n_paths": agg.get("n_paths", "NaN"),
                "ey_rmse_mean": agg.get("ey_rmse_mean", "NaN"),
                "xy_rmse_mean": agg.get("xy_rmse_mean", "NaN"),
                "epsi_rmse_mean": agg.get("epsi_rmse_mean", "NaN"),
                "j_du_mean": agg.get("j_du_mean", "NaN"),
                "omega_cmd_rms_mean": agg.get("omega_cmd_rms_mean", "NaN"),
                "viol_rate_mean": agg.get("viol_rate_mean", "NaN"),
                "main_acc_pct_mean": agg.get("main_acc_pct_mean", "NaN"),
                "theta_mae_deg_mean": agg.get("theta_mae_deg_mean", "NaN"),
            }
        )
    strict_rows.sort(key=lambda row: (num(row["J_control"]), row["candidate_id"]))
    competition_ranks(strict_rows, "J_control", "strict_rank_by_J_control")

    strict_by_id = {row["candidate_id"]: row for row in strict_rows}
    offline_all_by_id = {row["candidate_id"]: row for row in offline_rows}
    offline_rank_by_id = {row["candidate_id"]: row for row in offline_rank_rows}
    decision_rows: list[dict[str, Any]] = []
    for inv in inventory_rows:
        cid = inv["candidate_id"]
        strict = strict_by_id.get(cid, {})
        offline = offline_rank_by_id.get(cid, {})
        offline_all = offline_all_by_id.get(cid, {})
        is_reference = cid == "baseline_lock"
        prior_class_b = boolish(inv.get("prior_eligible_for_class_b"))
        strict_present = cid in strict_by_id and cid != "baseline_lock"
        eligible_c = boolish(strict.get("eligible_for_class_c"))
        eligible_b = (
            prior_class_b
            and not strict_present
            and inv["evidence_tier"] == "offline_only"
            and not inv.get("superseded_by")
        )
        hard_status = strict.get("hard_constraint_status")
        if not hard_status:
            hard_status = "pass" if is_reference else ("offline_only" if inv["evidence_tier"] not in {"advisory_only", "missing_checkpoint"} else inv["evidence_tier"])
        exclude_reason = ""
        if is_reference:
            exclude_reason = "reference_baseline"
        elif eligible_c:
            exclude_reason = "none"
        elif cid in strict_by_id:
            exclude_reason = strict.get("class_c_reason", "strict_not_promoted")
        elif inv["evidence_tier"] == "advisory_only":
            exclude_reason = "advisory_only_non_replay_capable"
        elif inv["evidence_tier"] == "degraded":
            exclude_reason = "degraded_hard_sample_focal_only_no_smoothness_claim"
        elif inv["evidence_tier"] == "missing_checkpoint":
            exclude_reason = "missing_checkpoint"
        elif inv.get("superseded_by"):
            exclude_reason = f"superseded_by_{inv['superseded_by']}"
        elif eligible_b:
            exclude_reason = "offline_class_b_only_requires_new_strict_repair_before_formal_use"
        else:
            exclude_reason = "offline_only_not_selected_for_strict_repair"

        decision_rows.append(
            {
                "candidate_id": cid,
                "source_phase": inv["source_phase"],
                "evidence_validity": inv["evidence_validity"],
                "evidence_tier": inv["evidence_tier"],
                "repair_status": inv["repair_status"],
                "hard_constraint_status": hard_status,
                "metric_missing_ratio": strict.get("metric_missing_ratio", inv["offline_metric_missing_ratio"]),
                "eligible_for_class_b": eligible_b,
                "eligible_for_class_c": eligible_c,
                "exclude_reason": exclude_reason,
                "offline_proxy_rank": offline.get("offline_proxy_rank", "NaN"),
                "offline_proxy_score": offline_all.get("offline_proxy_score", inv["offline_proxy_score"]),
                "strict_rank_by_J_control": strict.get("strict_rank_by_J_control", "NaN"),
                "J_control": strict.get("J_control", "NaN"),
                "class_c_reason": strict.get("class_c_reason", "NaN"),
                "superseded_by": inv.get("superseded_by", ""),
                "has_checkpoint": inv["has_checkpoint"],
                "has_onnx": inv["has_onnx"],
                "has_closed_loop_mat": inv["has_closed_loop_mat"],
            }
        )

    decision_rows.sort(
        key=lambda row: (
            0 if row["candidate_id"] == "baseline_lock" else 1,
            str(row["source_phase"]),
            str(row["candidate_id"]),
        )
    )

    advisory_rows = [row for row in inventory_rows if row["evidence_tier"] == "advisory_only"]
    write_csv(
        OUT_ROOT / "candidate_evidence_inventory.csv",
        inventory_rows,
        [
            "candidate_id",
            "source_phase",
            "run_tag",
            "evidence_tier",
            "evidence_validity",
            "actual_method",
            "repair_status",
            "superseded_by",
            "is_rerun_20260622",
            "has_config",
            "has_metrics",
            "has_report",
            "has_checkpoint",
            "has_onnx",
            "has_closed_loop_mat",
            "closed_loop_mat_count",
            "config_file",
            "metrics_file",
            "report_file",
            "checkpoint_path",
            "onnx_file",
            "closed_loop_mat_files",
            "offline_proxy_score",
            "offline_metric_missing_ratio",
            "offline_missing_metrics",
            "prior_class_label",
            "prior_eligible_for_class_b",
            "advisory_only",
        ],
    )
    write_csv(
        OUT_ROOT / "offline_proxy_all_scored_candidates.csv",
        offline_rows,
        [
            "offline_proxy_score_rank_all",
            "candidate_id",
            "source_phase",
            "run_tag",
            "evidence_validity",
            "evidence_tier",
            "repair_status",
            "superseded_by",
            "offline_proxy_score",
            "metric_missing_ratio",
            "missing_metrics",
            "prior_class_label",
            "rank_eligible",
            "has_config",
            "has_metrics",
            "has_report",
            "has_checkpoint",
            "eligible_for_strict_repair",
            *OFFLINE_METRICS,
        ],
    )
    write_csv(
        OUT_ROOT / "offline_proxy_ranking.csv",
        offline_rank_rows,
        [
            "offline_proxy_rank",
            "candidate_id",
            "source_phase",
            "run_tag",
            "evidence_validity",
            "evidence_tier",
            "repair_status",
            "superseded_by",
            "offline_proxy_score",
            "metric_missing_ratio",
            "missing_metrics",
            "prior_class_label",
            "rank_eligible",
            "has_config",
            "has_metrics",
            "has_report",
            "has_checkpoint",
            "eligible_for_strict_repair",
            *OFFLINE_METRICS,
        ],
    )
    write_csv(
        OUT_ROOT / "strict_closed_loop_ranking.csv",
        strict_rows,
        [
            "strict_rank_by_J_control",
            "candidate_id",
            "source_phase",
            "evidence_validity",
            "repair_status",
            "J_control",
            "hard_constraint_status",
            "eligible_for_class_c",
            "class_c_status",
            "class_c_reason",
            "metric_missing_ratio",
            "missing_metrics",
            "n_paths",
            "ey_rmse_mean",
            "xy_rmse_mean",
            "epsi_rmse_mean",
            "j_du_mean",
            "omega_cmd_rms_mean",
            "viol_rate_mean",
            "main_acc_pct_mean",
            "theta_mae_deg_mean",
        ],
    )
    write_csv(
        OUT_ROOT / "five_experiment_decision_table.csv",
        decision_rows,
        [
            "candidate_id",
            "source_phase",
            "evidence_validity",
            "evidence_tier",
            "repair_status",
            "hard_constraint_status",
            "metric_missing_ratio",
            "eligible_for_class_b",
            "eligible_for_class_c",
            "exclude_reason",
            "offline_proxy_rank",
            "offline_proxy_score",
            "strict_rank_by_J_control",
            "J_control",
            "class_c_reason",
            "superseded_by",
            "has_checkpoint",
            "has_onnx",
            "has_closed_loop_mat",
        ],
    )
    write_csv(
        OUT_ROOT / "strict_repair_queue.csv",
        repair_rows,
        ["candidate_id", "source_phase", "missing_checkpoint", "missing_onnx", "missing_closed_loop_mat", "repair_decision", "reason"],
    )
    write_csv(
        OUT_ROOT / "advisory_only_e5_registry.csv",
        advisory_rows,
        [
            "candidate_id",
            "source_phase",
            "evidence_tier",
            "evidence_validity",
            "repair_status",
            "offline_metric_missing_ratio",
            "offline_missing_metrics",
            "has_checkpoint",
            "has_onnx",
            "has_closed_loop_mat",
            "actual_method",
        ],
    )

    after_hashes = snapshot_sources(source_paths)
    hash_rows = hash_diff(before_hashes, after_hashes)
    write_csv(
        OUT_ROOT / "source_artifact_hash_manifest.csv",
        hash_rows,
        ["path", "exists_before", "exists_after", "size_before", "size_after", "sha256_before", "sha256_after", "unchanged"],
    )

    strict_class_c = [row["candidate_id"] for row in strict_rows if boolish(row.get("eligible_for_class_c"))]
    class_b_remaining = [row["candidate_id"] for row in decision_rows if boolish(row.get("eligible_for_class_b"))]
    repair_queue_candidates = [row["candidate_id"] for row in repair_rows]
    source_hash_ok = all(boolish(row["unchanged"]) for row in hash_rows)
    write_json(
        OUT_ROOT / "strict_metric_rerank_decision.json",
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "output_root": str(OUT_ROOT),
            "metric_version": read_json(WEIGHTS_FILE)["version"],
            "threshold_source": str(THRESHOLDS_FILE),
            "thresholds": thresholds,
            "new_training_triggered": False,
            "new_onnx_export_triggered": False,
            "new_matlab_simulink_triggered": False,
            "strict_class_c_candidates": strict_class_c,
            "remaining_offline_class_b_candidates": class_b_remaining,
            "strict_repair_queue_candidates": repair_queue_candidates,
            "source_hash_unchanged": source_hash_ok,
            "write_scope_under_output_root": True,
            "e2_rule": "hard_sample_focal_only; theta_smoothness_claim_invalid_not_run",
            "e5_rule": "advisory_only unless new E5_replay_fixed replay-capable evidence exists",
        },
    )

    report_lines = [
        "# SCI Five-Experiment New-Metric Rerank",
        "",
        f"- generated_at: `{datetime.now().isoformat(timespec='seconds')}`",
        "- scope: E1-E5 under `results/modern_tcn_sci_innovation/`",
        "- metric source: frozen `02_metric_freeze/metric_vFinal_control_oriented_frozen.json` and `hard_constraint_thresholds.json`",
        "- rerun policy: reused existing `rerun_20260622` evidence; no new training, ONNX export, or MATLAB/Simulink run was triggered in this node.",
        "",
        "## Evidence Boundary",
        "",
        "- E2 is kept as `hard_sample_focal_only`; `theta_smoothness_claim` is invalid/not-run and is not used for ranking.",
        "- E5 remains `advisory_only`; scheduled/smoothness/step metrics are excluded from formal offline and strict closed-loop ranking.",
        "- Candidates with missing checkpoints are scored in `offline_proxy_all_scored_candidates.csv` but excluded from formal `offline_proxy_ranking.csv`.",
        "- Strict closed-loop ranking includes only evidence-complete candidates with checkpoint, ONNX, and frozen path-set `.mat` evidence.",
        "",
        "## Offline Proxy Ranking",
        "",
        "| rank | candidate | phase | tier | score | note |",
        "|---:|---|---|---|---:|---|",
    ]
    for row in offline_rank_rows[:10]:
        note = row.get("superseded_by") or row.get("prior_class_label", "")
        report_lines.append(
            f"| {fmt(row['offline_proxy_rank'])} | `{row['candidate_id']}` | {row['source_phase']} | {row['evidence_tier']} | {num(row['offline_proxy_score']):.6f} | {note} |"
        )
    report_lines.extend(
        [
            "",
            "## Strict Closed-Loop Ranking",
            "",
            "| rank | candidate | J_control | hard status | Class C | reason |",
            "|---:|---|---:|---|---:|---|",
        ]
    )
    for row in strict_rows:
        report_lines.append(
            f"| {fmt(row['strict_rank_by_J_control'])} | `{row['candidate_id']}` | {num(row['J_control']):.6f} | "
            f"{row['hard_constraint_status']} | {fmt(row['eligible_for_class_c'])} | {row['class_c_reason']} |"
        )
    report_lines.extend(
        [
            "",
            "## Decision",
            "",
        ]
    )
    if strict_class_c:
        report_lines.append(f"- strict Class C candidate(s): `{';'.join(strict_class_c)}`")
    else:
        report_lines.append("- no strict Class C candidate after the frozen strict closed-loop comparison.")
    if class_b_remaining:
        report_lines.append(
            "- remaining offline-only Class B candidate(s) need a separate strict-repair node before formal use: "
            + ", ".join(f"`{cid}`" for cid in class_b_remaining)
        )
    else:
        report_lines.append("- no final Class B/C promotion is made by this node.")
    if repair_queue_candidates:
        report_lines.append(
            "- strict repair queue candidate(s), excluded from strict ranking until repaired: "
            + ", ".join(f"`{cid}`" for cid in repair_queue_candidates)
        )
    report_lines.extend(
        [
            f"- source artifact hashes unchanged: `{str(source_hash_ok).lower()}`",
            "- write scope: only files under `results/modern_tcn_metric_rebuild/11_sci_five_experiment_rerank/` were generated by this script.",
            "",
            "## Output Files",
            "",
            "- `offline_proxy_all_scored_candidates.csv`",
            "- `candidate_evidence_inventory.csv`",
            "- `offline_proxy_ranking.csv`",
            "- `strict_closed_loop_ranking.csv`",
            "- `five_experiment_decision_table.csv`",
            "- `strict_repair_queue.csv`",
            "- `advisory_only_e5_registry.csv`",
            "- `source_artifact_hash_manifest.csv`",
            "- `write_scope_audit.csv`",
            "- `strict_metric_rerank_decision.json`",
        ]
    )
    write_text(OUT_ROOT / "five_experiment_rerank_report.md", "\n".join(report_lines) + "\n")

    generated_files = sorted(p for p in OUT_ROOT.rglob("*") if p.is_file() and p.name != "write_scope_audit.csv")
    write_csv(
        OUT_ROOT / "write_scope_audit.csv",
        [
            {
                "path": str(path.resolve()),
                "under_output_root": str(path.resolve()).startswith(str(OUT_ROOT.resolve())),
                "size_bytes": path.stat().st_size,
                "modified_time": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
            }
            for path in generated_files
        ],
        ["path", "under_output_root", "size_bytes", "modified_time"],
    )

    print(
        json.dumps(
            {
                "output_root": str(OUT_ROOT),
                "offline_scored_candidates": len(offline_rows),
                "offline_ranked_candidates": len(offline_rank_rows),
                "strict_ranked_candidates": len(strict_rows),
                "strict_class_c_candidates": strict_class_c,
                "remaining_offline_class_b_candidates": class_b_remaining,
                "strict_repair_queue_candidates": repair_queue_candidates,
                "source_hash_unchanged": source_hash_ok,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
