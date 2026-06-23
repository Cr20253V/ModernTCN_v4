from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parent
OUT_ROOT = ROOT / "05_sandbox_closed_loop_if_needed" / "03_formal_validation"
THRESHOLDS = ROOT / "02_metric_freeze" / "hard_constraint_thresholds.json"

LOWER_BETTER = [
    "ey_rmse",
    "ey_peak",
    "epsi_rmse",
    "ev_rmse",
    "eomega_rmse",
    "xy_rmse",
    "j_du",
    "omega_cmd_rms",
    "omega_cmd_peak",
    "viol_rate",
    "theta_mae_deg",
    "theta_sched_mae_deg",
]
HIGHER_BETTER = [
    "main_acc_pct",
    "turn_acc_pct",
    "slope_recall_pct",
    "right_recall_pct",
    "left_recall_pct",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: fmt(row.get(key, "")) for key in fieldnames})


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def fmt(value: object) -> str:
    if value is None:
        return "NaN"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        if isinstance(value, float) and math.isnan(value):
            return "NaN"
        return f"{value:.15g}" if isinstance(value, float) else str(value)
    text = str(value)
    return text if text else "NaN"


def num(row: dict[str, str], key: str) -> float:
    text = str(row.get(key, "")).strip()
    if not text or text.lower() in {"nan", "none"}:
        return float("nan")
    return float(text)


def safe_ratio(value: float, baseline: float) -> float:
    if not math.isfinite(value) or not math.isfinite(baseline) or abs(baseline) < 1e-12:
        return float("nan")
    return value / baseline


def load_path_rows() -> tuple[list[dict[str, object]], dict[str, list[dict[str, str]]]]:
    path_rows = read_csv(OUT_ROOT / "formal_path_runs.csv")
    by_path: dict[str, list[dict[str, str]]] = {}
    flat_rows: list[dict[str, object]] = []
    for path_row in path_rows:
        path_tag = path_row["path_tag"]
        summary_file = Path(path_row["summary_file"])
        rows = read_csv(summary_file)
        by_path[path_tag] = rows
        for row in rows:
            out = {"path_tag": path_tag, **row}
            flat_rows.append(out)
    return flat_rows, by_path


def aggregate(flat_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    controllers = sorted({str(row["controller"]) for row in flat_rows})
    rows: list[dict[str, object]] = []
    for controller in controllers:
        subset = [row for row in flat_rows if str(row["controller"]) == controller]
        out: dict[str, object] = {"controller": controller, "n_paths": len(subset)}
        for key in sorted(set(LOWER_BETTER + HIGHER_BETTER)):
            values = [float(row[key]) for row in subset if key in row and str(row[key]).strip()]
            values = [v for v in values if math.isfinite(v)]
            out[f"{key}_mean"] = mean(values) if values else float("nan")
            out[f"{key}_worst"] = max(values) if values else float("nan")
        rows.append(out)
    return rows


def decide(aggregate_rows: list[dict[str, object]], thresholds: dict[str, object]) -> list[dict[str, object]]:
    baseline = next(row for row in aggregate_rows if row["controller"] == "baseline_lock")
    decisions: list[dict[str, object]] = []
    baseline_j = j_control(baseline, baseline)
    for row in aggregate_rows:
        if row["controller"] == "baseline_lock":
            decisions.append(
                {
                    "controller": row["controller"],
                    "is_reference_baseline": True,
                    "J_control": baseline_j,
                    "hard_constraint_status": "pass",
                    "eligible_for_class_c": False,
                    "class_c_status": "Reference",
                    "class_c_reason": "reference_baseline",
                }
            )
            continue
        checks = hard_checks(row, baseline, thresholds)
        j = j_control(row, baseline)
        pass_hard = not checks
        eligible = pass_hard and math.isfinite(j) and j < baseline_j
        decisions.append(
            {
                "controller": row["controller"],
                "is_reference_baseline": False,
                "J_control": j,
                "J_control_baseline": baseline_j,
                "hard_constraint_status": "pass" if pass_hard else "fail",
                "eligible_for_class_c": eligible,
                "class_c_status": "Class C" if eligible else "NoClassC",
                "class_c_reason": "formal_validation_pass" if eligible else "; ".join(checks or ["J_control_not_better_than_baseline"]),
            }
        )
    return decisions


def hard_checks(row: dict[str, object], baseline: dict[str, object], thresholds: dict[str, object]) -> list[str]:
    failures: list[str] = []
    viol_abs = float(row["viol_rate_mean"]) - float(baseline["viol_rate_mean"])
    if math.isfinite(viol_abs) and viol_abs > float(thresholds["viol_rate_max_abs_increase"]):
        failures.append(f"viol_rate_abs_increase={viol_abs:.6g}")
    main_drop = (float(baseline["main_acc_pct_mean"]) - float(row["main_acc_pct_mean"])) / 100.0
    if math.isfinite(main_drop) and main_drop > float(thresholds["acc_main_min_drop"]):
        failures.append(f"main_acc_drop={main_drop:.6g}")
    omega_ratio = safe_ratio(float(row["omega_cmd_rms_mean"]), float(baseline["omega_cmd_rms_mean"]))
    if math.isfinite(omega_ratio) and omega_ratio > float(thresholds["omega_cmd_rms_max_ratio"]):
        failures.append(f"omega_cmd_rms_ratio={omega_ratio:.6g}")
    du_ratio = safe_ratio(float(row["j_du_mean"]), float(baseline["j_du_mean"]))
    if math.isfinite(du_ratio) and du_ratio > float(thresholds["delta_u_proxy_max_ratio"]):
        failures.append(f"delta_u_proxy_ratio={du_ratio:.6g}")
    return failures


def j_control(row: dict[str, object], baseline: dict[str, object]) -> float:
    terms = [
        safe_ratio(float(row["ey_rmse_mean"]), float(baseline["ey_rmse_mean"])),
        safe_ratio(float(row["xy_rmse_mean"]), float(baseline["xy_rmse_mean"])),
        safe_ratio(float(row["epsi_rmse_mean"]), float(baseline["epsi_rmse_mean"])),
        safe_ratio(float(row["j_du_mean"]), float(baseline["j_du_mean"])),
        safe_ratio(float(row["omega_cmd_rms_mean"]), float(baseline["omega_cmd_rms_mean"])),
    ]
    terms = [v for v in terms if math.isfinite(v)]
    return mean(terms) if terms else float("nan")


def write_report(aggregate_rows: list[dict[str, object]], decisions: list[dict[str, object]]) -> None:
    by_controller = {row["controller"]: row for row in aggregate_rows}
    lines = [
        "# Window 2 Formal Validation Aggregate Report",
        "",
        "- scope: formal validation over the frozen baseline path set",
        "- output root: `results/modern_tcn_metric_rebuild/05_sandbox_closed_loop_if_needed/03_formal_validation/`",
        "- strict Class C requires hard-constraint pass and aggregate J_control below baseline.",
        "",
        "## Aggregate Means",
        "",
        "| controller | ey_rmse | xy_rmse | epsi_rmse | j_du | omega_cmd_rms | viol_rate | theta_mae_deg | main_acc_pct | turn_acc_pct |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in aggregate_rows:
        lines.append(
            f"| `{row['controller']}` | {row['ey_rmse_mean']:.6f} | {row['xy_rmse_mean']:.6f} | "
            f"{row['epsi_rmse_mean']:.6f} | {row['j_du_mean']:.6f} | {row['omega_cmd_rms_mean']:.6f} | "
            f"{row['viol_rate_mean']:.6f} | {row['theta_mae_deg_mean']:.6f} | "
            f"{row['main_acc_pct_mean']:.4f} | {row['turn_acc_pct_mean']:.4f} |"
        )
    lines.extend(
        [
            "",
            "## Class C Gate",
            "",
            "| controller | J_control | hard_constraint_status | eligible_for_class_c | reason |",
            "|---|---:|---|---:|---|",
        ]
    )
    for row in decisions:
        lines.append(
            f"| `{row['controller']}` | {float(row['J_control']):.6f} | {row['hard_constraint_status']} | "
            f"{int(bool(row['eligible_for_class_c']))} | {row['class_c_reason']} |"
        )
    winners = [row for row in decisions if bool(row["eligible_for_class_c"])]
    lines.extend(["", "## Decision", ""])
    if winners:
        best = min(winners, key=lambda r: float(r["J_control"]))
        lines.append(f"- strict Class C candidate: `{best['controller']}`")
    else:
        lines.append("- no strict Class C candidate after formal validation.")
        lines.append("- sandbox gains do not survive the full frozen path-set validation.")
    write_text(OUT_ROOT / "formal_validation_aggregate_report.md", "\n".join(lines) + "\n")


def main() -> int:
    thresholds = json.loads(THRESHOLDS.read_text(encoding="utf-8"))
    flat_rows, _ = load_path_rows()
    write_csv(
        OUT_ROOT / "formal_validation_path_metrics.csv",
        flat_rows,
        list(flat_rows[0].keys()),
    )
    aggregate_rows = aggregate(flat_rows)
    aggregate_fields = ["controller", "n_paths"]
    for key in sorted(set(LOWER_BETTER + HIGHER_BETTER)):
        aggregate_fields.extend([f"{key}_mean", f"{key}_worst"])
    write_csv(OUT_ROOT / "formal_validation_aggregate.csv", aggregate_rows, aggregate_fields)
    decisions = decide(aggregate_rows, thresholds)
    decision_fields = [
        "controller",
        "is_reference_baseline",
        "J_control",
        "J_control_baseline",
        "hard_constraint_status",
        "eligible_for_class_c",
        "class_c_status",
        "class_c_reason",
    ]
    write_csv(OUT_ROOT / "formal_validation_class_c_decision.csv", decisions, decision_fields)
    write_json(
        OUT_ROOT / "formal_validation_decision.json",
        {
            "strict_class_c_candidates": [row["controller"] for row in decisions if bool(row["eligible_for_class_c"])],
            "decisions": decisions,
        },
    )
    write_report(aggregate_rows, decisions)
    print(json.dumps({"decisions": decisions}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
