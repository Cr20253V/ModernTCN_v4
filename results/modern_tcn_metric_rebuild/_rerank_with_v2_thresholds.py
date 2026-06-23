from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
STRICT_ROOT = ROOT / "09_strict_gru_tcn_validation"
THRESHOLD_ROOT = ROOT / "10_threshold_recalibration"

FINAL_RESULTS = STRICT_ROOT / "five_algorithm_strict_final_results.csv"
RECLASSIFICATION = THRESHOLD_ROOT / "threshold_reclassification_v2.csv"

OUT_CSV = THRESHOLD_ROOT / "rerank_with_v2_thresholds.csv"
OUT_REPORT = THRESHOLD_ROOT / "rerank_with_v2_thresholds_report.md"


def num(value: Any) -> float:
    if value is None:
        return math.nan
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "false"}:
        if text.lower() == "false":
            return 0.0
        return math.nan
    if text.lower() == "true":
        return 1.0
    try:
        return float(text)
    except ValueError:
        return math.nan


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


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def decision(row: dict[str, Any], profile: str) -> str:
    algorithm_id = row["algorithm_id"]
    hard_status = row[f"{profile}_status"]
    j_better = bool(row["J_control_better_than_baseline"])
    if algorithm_id == "baseline_lock":
        return "reference_baseline"
    if hard_status != "pass":
        return "reject_hard_fail"
    if j_better:
        return "promote_candidate_under_v2"
    return "hard_pass_but_not_better_than_baseline"


def rank_key(row: dict[str, Any], profile: str) -> tuple[int, float, str]:
    hard_pass = row[f"{profile}_status"] == "pass"
    algorithm_id = row["algorithm_id"]
    if algorithm_id == "baseline_lock":
        bucket = 1
    elif hard_pass and bool(row["J_control_better_than_baseline"]):
        bucket = 0
    elif hard_pass:
        bucket = 2
    else:
        bucket = 3
    return bucket, num(row["J_control"]), algorithm_id


def main() -> None:
    final_rows = {row["algorithm_id"]: row for row in read_csv(FINAL_RESULTS)}
    reclass_rows = read_csv(RECLASSIFICATION)

    rows: list[dict[str, Any]] = []
    for rc in reclass_rows:
        algorithm_id = rc["algorithm_id"]
        fr = final_rows[algorithm_id]
        rows.append(
            {
                "algorithm_id": algorithm_id,
                "algorithm_family": fr["algorithm_family"],
                "evidence_role": fr["evidence_role"],
                "J_control": num(fr["J_control"]),
                "old_hard_status": rc["original_full_status"],
                "closed_loop_v2_status": rc["closed_loop_v2_status"],
                "closed_loop_v2_failures": rc["closed_loop_v2_failures"],
                "full_v2_status": rc["full_v2_status"],
                "full_v2_failures": rc["full_v2_failures"],
                "J_control_better_than_baseline": bool_text(rc["J_control_better_than_baseline"]),
                "ey_rmse_mean": num(fr["ey_rmse_mean"]),
                "xy_rmse_mean": num(fr["xy_rmse_mean"]),
                "epsi_rmse_mean": num(fr["epsi_rmse_mean"]),
                "j_du_mean": num(fr["j_du_mean"]),
                "omega_cmd_rms_mean": num(fr["omega_cmd_rms_mean"]),
                "main_acc_pct_closed_loop_mean": num(fr["main_acc_pct_closed_loop_mean"]),
                "turn_acc_pct_closed_loop_mean": num(fr["turn_acc_pct_closed_loop_mean"]),
            }
        )

    for rank, row in enumerate(sorted(rows, key=lambda r: (num(r["J_control"]), r["algorithm_id"])), start=1):
        row["rank_by_J_control"] = rank

    for profile in ("closed_loop_v2", "full_v2"):
        for rank, row in enumerate(sorted(rows, key=lambda r, p=profile: rank_key(r, p)), start=1):
            row[f"engineering_rank_{profile}"] = rank
            row[f"decision_{profile}"] = decision(row, profile)

    fields = [
        "algorithm_id",
        "algorithm_family",
        "evidence_role",
        "J_control",
        "rank_by_J_control",
        "old_hard_status",
        "closed_loop_v2_status",
        "engineering_rank_closed_loop_v2",
        "decision_closed_loop_v2",
        "closed_loop_v2_failures",
        "full_v2_status",
        "engineering_rank_full_v2",
        "decision_full_v2",
        "full_v2_failures",
        "J_control_better_than_baseline",
        "ey_rmse_mean",
        "xy_rmse_mean",
        "epsi_rmse_mean",
        "j_du_mean",
        "omega_cmd_rms_mean",
        "main_acc_pct_closed_loop_mean",
        "turn_acc_pct_closed_loop_mean",
    ]
    write_csv(OUT_CSV, sorted(rows, key=lambda r: r["engineering_rank_closed_loop_v2"]), fields)

    lines = [
        "# Rerank With v2 Thresholds",
        "",
        "## Rule",
        "",
        "- Numeric `J_control` ranking is unchanged by threshold changes.",
        "- Engineering ranking uses `closed_loop_v2_status` first, then `J_control`.",
        "- `baseline_lock` is kept as a reference row, not a candidate promotion.",
        "- `full_v2` is reported as a secondary view because it includes offline protection metrics.",
        "",
        "## Primary Ranking: Closed-Loop v2 Gate + J_control",
        "",
        "| rank | algorithm | hard v2 | J_control | J < baseline | decision | main acc | xy | j_du | omega |",
        "|---:|---|---|---:|---|---|---:|---:|---:|---:|",
    ]
    for row in sorted(rows, key=lambda r: r["engineering_rank_closed_loop_v2"]):
        lines.append(
            f"| {row['engineering_rank_closed_loop_v2']} | `{row['algorithm_id']}` | {row['closed_loop_v2_status']} | "
            f"{fmt(row['J_control'])} | {row['J_control_better_than_baseline']} | {row['decision_closed_loop_v2']} | "
            f"{fmt(row['main_acc_pct_closed_loop_mean'], 3)} | {fmt(row['xy_rmse_mean'], 6)} | "
            f"{fmt(row['j_du_mean'], 6)} | {fmt(row['omega_cmd_rms_mean'], 6)} |"
        )

    lines.extend(
        [
            "",
            "## Numeric Ranking Only",
            "",
            "| rank | algorithm | J_control | old hard | closed-loop v2 | full v2 |",
            "|---:|---|---:|---|---|---|",
        ]
    )
    for row in sorted(rows, key=lambda r: r["rank_by_J_control"]):
        lines.append(
            f"| {row['rank_by_J_control']} | `{row['algorithm_id']}` | {fmt(row['J_control'])} | "
            f"{row['old_hard_status']} | {row['closed_loop_v2_status']} | {row['full_v2_status']} |"
        )

    lines.extend(
        [
            "",
            "## Full v2 Gate View",
            "",
            "| rank | algorithm | full v2 | J_control | decision | failures |",
            "|---:|---|---|---:|---|---|",
        ]
    )
    for row in sorted(rows, key=lambda r: r["engineering_rank_full_v2"]):
        lines.append(
            f"| {row['engineering_rank_full_v2']} | `{row['algorithm_id']}` | {row['full_v2_status']} | "
            f"{fmt(row['J_control'])} | {row['decision_full_v2']} | {row['full_v2_failures']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Under v2, `uncertainty_seed101_rerun_20260622` becomes the only non-reference candidate that both passes hard gates and has `J_control < baseline`.",
            "- `GRU_seed101` now passes the v2 hard gate, matching the visual closed-loop acceptability judgment, but its aggregate `J_control` is still far worse than baseline.",
            "- `mode_theta_detach_flatreg001_seed21_rerun_20260622` also passes v2 hard gates, but it remains worse than baseline by `J_control`.",
            "- `TCN_seed101` remains rejected because closed-loop main accuracy and delta-u proxy remain beyond the proposed v2 limits.",
        ]
    )
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_REPORT}")


if __name__ == "__main__":
    main()
