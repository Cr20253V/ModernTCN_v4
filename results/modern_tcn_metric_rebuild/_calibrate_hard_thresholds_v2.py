from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
STRICT_ROOT = ROOT / "09_strict_gru_tcn_validation"
OUT = ROOT / "10_threshold_recalibration"

RESULTS_FILE = STRICT_ROOT / "five_algorithm_strict_final_results.csv"
CURRENT_THRESHOLDS_FILE = ROOT / "02_metric_freeze" / "hard_constraint_thresholds.json"

PASS_ANCHORS = {
    "baseline_lock",
    "uncertainty_seed101_rerun_20260622",
    "mode_theta_detach_flatreg001_seed21_rerun_20260622",
    "GRU_seed101",
}
REJECT_ANCHORS = {"TCN_seed101"}


def num(value: Any) -> float:
    if value is None:
        return math.nan
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "unavailable"}:
        return math.nan
    try:
        return float(text)
    except ValueError:
        return math.nan


def ratio(value: float, base: float) -> float:
    if not math.isfinite(value) or not math.isfinite(base) or abs(base) < 1e-12:
        return math.nan
    return value / base


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def fmt(value: Any, digits: int = 6) -> str:
    value = num(value)
    if not math.isfinite(value):
        return "NaN"
    return f"{value:.{digits}f}"


def rounded(value: float) -> float:
    if not math.isfinite(value):
        return math.nan
    if abs(value) < 0.1:
        return round(value + 1e-12, 3)
    if abs(value) < 10:
        return round(value + 1e-12, 2)
    return round(value + 1e-12, 1)


def metric_values(row: dict[str, str], baseline: dict[str, str]) -> dict[str, float]:
    return {
        "viol_rate_abs_increase": num(row["viol_rate_mean"]) - num(baseline["viol_rate_mean"]),
        "closed_loop_main_acc_drop": (
            num(baseline["main_acc_pct_closed_loop_mean"]) - num(row["main_acc_pct_closed_loop_mean"])
        )
        / 100.0,
        "omega_cmd_rms_ratio": ratio(num(row["omega_cmd_rms_mean"]), num(baseline["omega_cmd_rms_mean"])),
        "delta_u_proxy_ratio": ratio(num(row["j_du_mean"]), num(baseline["j_du_mean"])),
        "offline_acc_main_drop": num(baseline["offline_acc_main"]) - num(row["offline_acc_main"]),
        "stall_recall_drop": num(baseline["offline_stall_recall"]) - num(row["offline_stall_recall"]),
        "slope_recall_drop": num(baseline["offline_slope_recall"]) - num(row["offline_slope_recall"]),
        "theta_edge_p95_ratio": ratio(
            num(row["offline_theta_edge_p95_abs_err"]),
            num(baseline["offline_theta_edge_p95_abs_err"]),
        ),
        "flat_peak_theta_error_ratio": ratio(
            num(row["offline_flat_peak_theta_error"]),
            num(baseline["offline_flat_peak_theta_error"]),
        ),
        "J_control": num(row["J_control"]),
    }


def failure_list(values: dict[str, float], thresholds: dict[str, Any], include_offline: bool) -> list[str]:
    checks: list[tuple[str, str, float]] = [
        ("viol_rate_abs_increase", "viol_rate_max_abs_increase", values["viol_rate_abs_increase"]),
        ("closed_loop_main_acc_drop", "acc_main_min_drop", values["closed_loop_main_acc_drop"]),
        ("omega_cmd_rms_ratio", "omega_cmd_rms_max_ratio", values["omega_cmd_rms_ratio"]),
        ("delta_u_proxy_ratio", "delta_u_proxy_max_ratio", values["delta_u_proxy_ratio"]),
    ]
    if include_offline:
        checks.extend(
            [
                ("offline_acc_main_drop", "acc_main_min_drop", values["offline_acc_main_drop"]),
                ("stall_recall_drop", "stall_recall_min_drop", values["stall_recall_drop"]),
                ("slope_recall_drop", "slope_recall_min_drop", values["slope_recall_drop"]),
                ("theta_edge_p95_ratio", "theta_edge_p95_max_ratio", values["theta_edge_p95_ratio"]),
                ("flat_peak_theta_error_ratio", "flat_peak_theta_error_max_ratio", values["flat_peak_theta_error_ratio"]),
            ]
        )

    failures = []
    for metric, threshold_key, value in checks:
        limit = num(thresholds[threshold_key])
        if math.isfinite(value) and math.isfinite(limit) and value > limit:
            failures.append(f"{metric}={value:.6g}>{limit:.6g}")
    return failures


def summarize_separation(
    metric: str,
    current_limit: float,
    proposed_limit: float,
    values_by_algorithm: dict[str, dict[str, float]],
    profile: str,
    rationale: str,
) -> dict[str, Any]:
    pass_values = [values_by_algorithm[a][metric] for a in PASS_ANCHORS if a in values_by_algorithm]
    reject_values = [values_by_algorithm[a][metric] for a in REJECT_ANCHORS if a in values_by_algorithm]
    pass_values = [v for v in pass_values if math.isfinite(v)]
    reject_values = [v for v in reject_values if math.isfinite(v)]
    pass_max = max(pass_values) if pass_values else math.nan
    reject_min = min(reject_values) if reject_values else math.nan
    separable = math.isfinite(pass_max) and math.isfinite(reject_min) and pass_max < reject_min
    return {
        "profile": profile,
        "metric": metric,
        "current_limit": current_limit,
        "pass_anchor_max": pass_max,
        "reject_anchor_min": reject_min,
        "separable_by_threshold": bool(separable),
        "proposed_limit": proposed_limit,
        "passes_all_pass_anchors": all(v <= proposed_limit for v in pass_values),
        "rejects_tcn_anchor": any(v > proposed_limit for v in reject_values),
        "rationale": rationale,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = read_csv(RESULTS_FILE)
    current = json.loads(CURRENT_THRESHOLDS_FILE.read_text(encoding="utf-8"))
    baseline = next(row for row in rows if row["algorithm_id"] == "baseline_lock")
    values_by_algorithm = {row["algorithm_id"]: metric_values(row, baseline) for row in rows}

    closed_loop_v2 = dict(current)
    closed_loop_v2.update(
        {
            "acc_main_min_drop": 0.030,
            "omega_cmd_rms_max_ratio": 5.00,
            "delta_u_proxy_max_ratio": 45.00,
        }
    )

    full_v2 = dict(closed_loop_v2)
    full_v2.update(
        {
            "stall_recall_min_drop": 0.100,
            "slope_recall_min_drop": 0.030,
            "theta_edge_p95_max_ratio": 1.05,
            "flat_peak_theta_error_max_ratio": 1.15,
        }
    )

    (OUT / "hard_constraint_thresholds_v2_closed_loop_proposed.json").write_text(
        json.dumps(closed_loop_v2, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (OUT / "hard_constraint_thresholds_v2_full_proposed.json").write_text(
        json.dumps(full_v2, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    value_rows = []
    for row in rows:
        algorithm_id = row["algorithm_id"]
        values = values_by_algorithm[algorithm_id]
        value_rows.append(
            {
                "algorithm_id": algorithm_id,
                "anchor_role": "pass_anchor" if algorithm_id in PASS_ANCHORS else ("reject_anchor" if algorithm_id in REJECT_ANCHORS else "context"),
                **values,
            }
        )
    write_csv(
        OUT / "threshold_metric_values.csv",
        value_rows,
        [
            "algorithm_id",
            "anchor_role",
            "viol_rate_abs_increase",
            "closed_loop_main_acc_drop",
            "omega_cmd_rms_ratio",
            "delta_u_proxy_ratio",
            "offline_acc_main_drop",
            "stall_recall_drop",
            "slope_recall_drop",
            "theta_edge_p95_ratio",
            "flat_peak_theta_error_ratio",
            "J_control",
        ],
    )

    diagnostics = [
        summarize_separation(
            "closed_loop_main_acc_drop",
            current["acc_main_min_drop"],
            closed_loop_v2["acc_main_min_drop"],
            values_by_algorithm,
            "closed_loop_v2",
            "Guard band above the worst accepted closed-loop anchor; still far below TCN degradation.",
        ),
        summarize_separation(
            "omega_cmd_rms_ratio",
            current["omega_cmd_rms_max_ratio"],
            closed_loop_v2["omega_cmd_rms_max_ratio"],
            values_by_algorithm,
            "closed_loop_v2",
            "Not separable because TCN has lower omega ratio than GRU; keep only as a broad instability ceiling.",
        ),
        summarize_separation(
            "delta_u_proxy_ratio",
            current["delta_u_proxy_max_ratio"],
            closed_loop_v2["delta_u_proxy_max_ratio"],
            values_by_algorithm,
            "closed_loop_v2",
            "Separable between accepted GRU and rejected TCN, but ratio is inflated by the very smooth baseline.",
        ),
        summarize_separation(
            "stall_recall_drop",
            current["stall_recall_min_drop"],
            full_v2["stall_recall_min_drop"],
            values_by_algorithm,
            "full_v2",
            "Relaxed to pass GRU while rejecting TCN; requires more seeds before formal freeze.",
        ),
        summarize_separation(
            "slope_recall_drop",
            current["slope_recall_min_drop"],
            full_v2["slope_recall_min_drop"],
            values_by_algorithm,
            "full_v2",
            "Relaxed modestly; GRU already passes, TCN remains clearly failed.",
        ),
        summarize_separation(
            "theta_edge_p95_ratio",
            current["theta_edge_p95_max_ratio"],
            full_v2["theta_edge_p95_max_ratio"],
            values_by_algorithm,
            "full_v2",
            "Kept strict because GRU is below baseline and TCN is clearly above threshold.",
        ),
        summarize_separation(
            "flat_peak_theta_error_ratio",
            current["flat_peak_theta_error_max_ratio"],
            full_v2["flat_peak_theta_error_max_ratio"],
            values_by_algorithm,
            "full_v2",
            "Relaxed to match the accepted GRU/mode-theta range while keeping TCN rejected.",
        ),
    ]
    write_csv(
        OUT / "threshold_separation_diagnostics.csv",
        diagnostics,
        [
            "profile",
            "metric",
            "current_limit",
            "pass_anchor_max",
            "reject_anchor_min",
            "separable_by_threshold",
            "proposed_limit",
            "passes_all_pass_anchors",
            "rejects_tcn_anchor",
            "rationale",
        ],
    )

    reclassified = []
    for row in rows:
        algorithm_id = row["algorithm_id"]
        values = values_by_algorithm[algorithm_id]
        if algorithm_id == "baseline_lock":
            closed_failures: list[str] = []
            full_failures: list[str] = []
            closed_status = "pass"
            full_status = "pass"
        else:
            closed_failures = failure_list(values, closed_loop_v2, include_offline=False)
            full_failures = failure_list(values, full_v2, include_offline=True)
            closed_status = "pass" if not closed_failures else "fail"
            full_status = "pass" if not full_failures else "fail"
        j_better = values["J_control"] < values_by_algorithm["baseline_lock"]["J_control"]
        reclassified.append(
            {
                "algorithm_id": algorithm_id,
                "original_full_status": row["hard_constraint_status"],
                "closed_loop_v2_status": closed_status,
                "closed_loop_v2_failures": "; ".join(closed_failures) if closed_failures else "none",
                "full_v2_status": full_status,
                "full_v2_failures": "; ".join(full_failures) if full_failures else "none",
                "J_control": values["J_control"],
                "J_control_better_than_baseline": bool(j_better),
                "v2_hard_pass_and_J_better_than_baseline": bool(full_status == "pass" and j_better and algorithm_id != "baseline_lock"),
            }
        )
    write_csv(
        OUT / "threshold_reclassification_v2.csv",
        reclassified,
        [
            "algorithm_id",
            "original_full_status",
            "closed_loop_v2_status",
            "closed_loop_v2_failures",
            "full_v2_status",
            "full_v2_failures",
            "J_control",
            "J_control_better_than_baseline",
            "v2_hard_pass_and_J_better_than_baseline",
        ],
    )

    report_lines = [
        "# Hard Threshold Recalibration v2 Proposal",
        "",
        "## Method",
        "",
        "- Keep the frozen v1 thresholds unchanged; write v2 proposals in this node only.",
        "- Treat `baseline_lock`, the two rerun ModernTCN candidates, and `GRU_seed101` as accepted anchors for threshold calibration.",
        "- Treat `TCN_seed101` as the rejected anchor because the strict closed-loop comparison showed materially worse behavior.",
        "- For each hard metric, check whether a single threshold can pass accepted anchors and reject TCN.",
        "- Metrics that cannot separate GRU from TCN are not used as decisive hard gates; they remain broad instability ceilings or scored penalties.",
        "",
        "## Proposed Closed-Loop v2 Thresholds",
        "",
        "| threshold | v1 | proposed v2 | reason |",
        "|---|---:|---:|---|",
        f"| `acc_main_min_drop` | {current['acc_main_min_drop']:.3f} | {closed_loop_v2['acc_main_min_drop']:.3f} | passes GRU and uncertainty; still rejects TCN by a wide margin |",
        f"| `omega_cmd_rms_max_ratio` | {current['omega_cmd_rms_max_ratio']:.2f} | {closed_loop_v2['omega_cmd_rms_max_ratio']:.2f} | not discriminative; use as broad ceiling, not as main evidence |",
        f"| `delta_u_proxy_max_ratio` | {current['delta_u_proxy_max_ratio']:.2f} | {closed_loop_v2['delta_u_proxy_max_ratio']:.2f} | passes GRU but rejects TCN; ratio is high because baseline `j_du` is very small |",
        "",
        "## Proposed Full v2 Additions",
        "",
        "| threshold | v1 | proposed v2 | reason |",
        "|---|---:|---:|---|",
        f"| `stall_recall_min_drop` | {current['stall_recall_min_drop']:.3f} | {full_v2['stall_recall_min_drop']:.3f} | passes GRU while rejecting TCN |",
        f"| `slope_recall_min_drop` | {current['slope_recall_min_drop']:.3f} | {full_v2['slope_recall_min_drop']:.3f} | modest relaxation; TCN remains failed |",
        f"| `theta_edge_p95_max_ratio` | {current['theta_edge_p95_max_ratio']:.2f} | {full_v2['theta_edge_p95_max_ratio']:.2f} | unchanged; already separates GRU from TCN |",
        f"| `flat_peak_theta_error_max_ratio` | {current['flat_peak_theta_error_max_ratio']:.2f} | {full_v2['flat_peak_theta_error_max_ratio']:.2f} | passes GRU/mode-theta range, still rejects TCN |",
        "",
        "## Reclassification Under v2",
        "",
        "| algorithm | old hard | closed-loop v2 | full v2 | J_control | J < baseline |",
        "|---|---|---|---|---:|---|",
    ]
    for row in reclassified:
        report_lines.append(
            f"| `{row['algorithm_id']}` | {row['original_full_status']} | {row['closed_loop_v2_status']} | "
            f"{row['full_v2_status']} | {num(row['J_control']):.6f} | {row['J_control_better_than_baseline']} |"
        )
    report_lines.extend(
        [
            "",
            "## Recommendation",
            "",
            "- Adopt `hard_constraint_thresholds_v2_closed_loop_proposed.json` first if the immediate goal is to make the closed-loop gate match visual/engineering acceptability.",
            "- Do not overwrite the v1 frozen file; freeze v2 only after naming a new metric version and rerunning the comparison reports.",
            "- `GRU_seed101` passes the proposed closed-loop v2 and full v2 hard gates, but its `J_control` remains much worse than baseline, so this does not make it a Class C replacement.",
            "- `TCN_seed101` remains failed under both v2 profiles.",
            "- The full v2 profile would also make `uncertainty_seed101_rerun_20260622` pass hard gates while retaining `J_control < baseline`; this is a promotion side effect that should be reviewed before any formal freeze.",
        ]
    )
    (OUT / "threshold_recalibration_report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
