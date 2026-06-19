"""Stage 2 targeted ModernTCN search for the plantfix workflow.

This runner keeps the v5 plantfix passive17_plus_all5 dataset and the
ModernTCN-small architecture fixed. It only searches a narrow turn-loss
neighborhood around the current closed-loop champion, ranks candidates by
offline metrics, exports the top candidates to ONNX, and writes a manifest for
the workflow closed-loop runner.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[4]
NODE_DIR = ROOT / "results" / "paper" / "agv_model_parameter_correction_workflow" / "08_models"
STAGE2_DIR = NODE_DIR / "modern_tcn_stage2_targeted"
DATASET_FILE = (
    ROOT
    / "data"
    / "tcn"
    / "ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat"
)
MODERN_SRC = ROOT / "src" / "ModernTCN"
if str(MODERN_SRC) not in sys.path:
    sys.path.insert(0, str(MODERN_SRC))

from train_modern_tcn import train_one_seed  # noqa: E402


@dataclass(frozen=True)
class CaseSpec:
    case: str
    lambda_turn: float
    turn_transition_weight: float
    turn_class_multipliers: List[float]
    select_turn_weight: float
    select_turn_transition_weight: float
    select_turn_lr_weight: float
    note: str


CASES = [
    CaseSpec("l018_tt22_bal", 0.18, 2.20, [1.35, 0.85, 1.35], 0.55, 1.25, 0.55, "slightly softer than champion"),
    CaseSpec("l020_tt25_bal", 0.20, 2.50, [1.40, 0.80, 1.40], 0.55, 1.20, 0.60, "current champion neighborhood"),
    CaseSpec("l022_tt28_turn", 0.22, 2.80, [1.45, 0.75, 1.45], 0.62, 1.35, 0.70, "stronger turn transition focus"),
    CaseSpec("l020_tt30_lr", 0.20, 3.00, [1.50, 0.75, 1.50], 0.60, 1.45, 0.80, "strongest L/R balance focus"),
]
SEEDS = [101, 303]
CHAMPION = {
    "label": "ModernTCN_turn_seed101_champion",
    "seed": 101,
    "run_tag": "modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101",
    "onnx_file": str(
        NODE_DIR
        / "modern_tcn"
        / "modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101"
        / "modern_tcn_seed101.onnx"
    ),
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Stage 2 targeted ModernTCN search")
    p.add_argument("--mode", choices=["preflight", "train", "export", "manifest", "all"], default="all")
    p.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    p.add_argument("--epochs", type=int, default=180)
    p.add_argument("--batch-size", type=int, default=256)
    p.add_argument("--patience", type=int, default=35)
    p.add_argument("--min-epochs", type=int, default=50)
    p.add_argument("--top-k", type=int, default=2)
    p.add_argument("--skip-existing", action="store_true", default=True)
    p.add_argument("--no-skip-existing", action="store_false", dest="skip_existing")
    p.add_argument("--sample-count", type=int, default=16)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    STAGE2_DIR.mkdir(parents=True, exist_ok=True)
    (STAGE2_DIR / "logs").mkdir(exist_ok=True)
    preflight = run_preflight()
    if args.mode == "preflight":
        write_report(preflight, [], [])
        return

    rows: List[Dict[str, Any]] = []
    if args.mode in {"train", "all"}:
        rows = run_training(args)
    else:
        rows = collect_rows()

    ranked = rank_rows(rows)
    write_csv(STAGE2_DIR / "stage2_modern_tcn_candidates.csv", ranked)

    selected = select_top_candidates(ranked, args.top_k)
    write_csv(STAGE2_DIR / "stage2_modern_tcn_selected.csv", selected)

    if args.mode in {"export", "all"}:
        export_selected(selected, args)

    selected = refresh_selected_onnx(selected)
    write_csv(STAGE2_DIR / "stage2_modern_tcn_selected.csv", selected)

    if args.mode in {"manifest", "all", "export"}:
        write_manifest(selected)

    write_report(preflight, ranked, selected)
    print(f"[stage2 modern] report: {STAGE2_DIR / 'stage2_modern_tcn_targeted_report.md'}")
    print(f"[stage2 modern] manifest: {STAGE2_DIR / 'stage2_closed_loop_manifest.json'}")


def run_preflight() -> Dict[str, Any]:
    checks = {
        "dataset_exists": DATASET_FILE.exists(),
        "champion_onnx_exists": Path(CHAMPION["onnx_file"]).exists(),
        "modern_src_exists": MODERN_SRC.exists(),
    }
    preflight = {
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "dataset_file": str(DATASET_FILE),
        "cases": [case.__dict__ for case in CASES],
        "seeds": SEEDS,
        "checks": checks,
        "pass": all(checks.values()),
    }
    (STAGE2_DIR / "stage2_preflight.json").write_text(json.dumps(preflight, indent=2), encoding="utf-8")
    if not preflight["pass"]:
        raise RuntimeError(f"Stage 2 preflight failed: {checks}")
    return preflight


def run_training(args: argparse.Namespace) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for case in CASES:
        for seed in SEEDS:
            out_dir = STAGE2_DIR / f"modern_tcn_v5_plantfix_stage2_{case.case}_seed{seed}"
            checkpoint = out_dir / f"modern_tcn_seed{seed}.pt"
            summary_file = out_dir / f"modern_tcn_seed{seed}_summary.csv"
            if args.skip_existing and checkpoint.exists() and summary_file.exists():
                print(f"[stage2 modern] reuse {case.case} seed={seed}: {checkpoint}")
            else:
                train_case(case, seed, out_dir, args)
            row = read_summary_row(summary_file)
            row.update(
                {
                    "case": case.case,
                    "note": case.note,
                    "run_tag": str(out_dir),
                    "output_dir": str(out_dir),
                    "checkpoint_file": str(checkpoint),
                    "lambda_turn": case.lambda_turn,
                    "turn_transition_weight": case.turn_transition_weight,
                    "turn_class_multipliers": " ".join(f"{x:g}" for x in case.turn_class_multipliers),
                    "select_turn_weight": case.select_turn_weight,
                    "select_turn_transition_weight": case.select_turn_transition_weight,
                    "select_turn_lr_weight": case.select_turn_lr_weight,
                }
            )
            rows.append(row)
    return rows


def train_case(case: CaseSpec, seed: int, out_dir: Path, args: argparse.Namespace) -> None:
    train_args = argparse.Namespace(
        seed=seed,
        model_family="small",
        dataset_file=str(DATASET_FILE),
        run_tag=str(out_dir),
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=1e-3,
        weight_decay=1e-4,
        patience=args.patience,
        min_epochs=args.min_epochs,
        channels=64,
        blocks=5,
        kernel_size=31,
        temporal_padding="same",
        dropout=0.15,
        turn_head_source="full",
        lambda_turn=case.lambda_turn,
        lambda_theta=0.55,
        lambda_theta_flat=0.12,
        theta_flat_loss_mode="near_zero",
        theta_flat_zero_tol_deg=0.3,
        lambda_theta_near_flat=0.0,
        theta_near_flat_deg=0.5,
        lambda_theta_error_excess=0.05,
        lambda_theta_flat_excess=0.0,
        lambda_theta_near_flat_excess=0.0,
        lambda_theta_true_zero_excess=0.10,
        lambda_theta_active_excess=0.10,
        lambda_theta_small_neg=0.0,
        lambda_theta_small_neg_excess=0.0,
        lambda_turn_release=0.0,
        lambda_false_turn_straight=0.0,
        theta_excess_target_deg=1.0,
        theta_flat_excess_target_deg=0.5,
        theta_small_neg_min_deg=-4.0,
        theta_small_neg_max_deg=-2.0,
        theta_gate_mode="none",
        theta_gate_power=1.0,
        theta_gate_floor=0.0,
        theta_neg_weight=1.0,
        theta_pos_weight=1.0,
        turn_transition_weight=case.turn_transition_weight,
        turn_class_multipliers=case.turn_class_multipliers,
        select_turn_weight=case.select_turn_weight,
        select_turn_transition_weight=case.select_turn_transition_weight,
        select_turn_transition_target=0.82,
        select_turn_left_weight=0.0,
        select_turn_left_target=0.88,
        select_turn_lr_weight=case.select_turn_lr_weight,
        select_turn_lr_target=0.88,
        select_theta_weight=0.30,
        select_theta_ref_deg=2.0,
        select_theta_p95_weight=0.80,
        select_theta_p95_target_deg=1.20,
        select_theta_flat_p95_weight=0.35,
        select_theta_flat_p95_target_deg=0.70,
        select_theta_near_flat_p95_weight=0.20,
        select_theta_near_flat_p95_target_deg=0.70,
        select_theta_true_zero_p95_weight=0.45,
        select_theta_true_zero_p95_target_deg=0.50,
        select_theta_extreme_p95_weight=0.60,
        select_theta_extreme_p95_target_deg=1.20,
        select_theta_edge_p95_weight=0.70,
        select_theta_edge_p95_target_deg=1.50,
        select_theta_small_nonzero_p95_weight=0.80,
        select_theta_small_nonzero_p95_target_deg=1.00,
        select_theta_flat_bias_weight=0.30,
        select_theta_flat_bias_target_deg=0.15,
        device=args.device,
        num_workers=0,
        limit_train=0,
        limit_val=0,
        limit_test=0,
        dry_run=False,
    )
    print(f"[stage2 modern] train case={case.case} seed={seed}")
    train_one_seed(train_args)


def collect_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for case in CASES:
        for seed in SEEDS:
            out_dir = STAGE2_DIR / f"modern_tcn_v5_plantfix_stage2_{case.case}_seed{seed}"
            summary_file = out_dir / f"modern_tcn_seed{seed}_summary.csv"
            if summary_file.exists():
                row = read_summary_row(summary_file)
                row.update(
                    {
                        "case": case.case,
                        "note": case.note,
                        "run_tag": str(out_dir),
                        "output_dir": str(out_dir),
                        "checkpoint_file": str(out_dir / f"modern_tcn_seed{seed}.pt"),
                        "lambda_turn": case.lambda_turn,
                        "turn_transition_weight": case.turn_transition_weight,
                        "turn_class_multipliers": " ".join(f"{x:g}" for x in case.turn_class_multipliers),
                        "select_turn_weight": case.select_turn_weight,
                        "select_turn_transition_weight": case.select_turn_transition_weight,
                        "select_turn_lr_weight": case.select_turn_lr_weight,
                    }
                )
                rows.append(row)
    if not rows:
        raise RuntimeError("No Stage 2 summary rows found. Run --mode train or --mode all first.")
    return rows


def rank_rows(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    ranked: List[Dict[str, Any]] = []
    for row in rows:
        right = to_float(row.get("turn_right_recall"))
        left = to_float(row.get("turn_left_recall"))
        lr_ratio = min(right, left) / max(right, left) if max(right, left) > 0 else 0.0
        turn_transition = to_float(row.get("acc_turn_transition"))
        acc_main = to_float(row.get("acc_main"))
        theta = to_float(row.get("theta_mae_deg"))
        theta_p95 = to_float(row.get("theta_abs_le_10_p95_abs_err_deg"))
        flat_p95 = to_float(row.get("theta_flat_abs_p95_deg"))
        flat_recall = to_float(row.get("flat_recall"))
        slope_recall = to_float(row.get("slope_recall"))
        score = (
            2.0 * max(0.0, 0.965 - acc_main)
            + 1.5 * max(0.0, 0.970 - slope_recall)
            + 1.0 * max(0.0, 0.940 - flat_recall)
            + 1.1 * max(0.0, 0.58 - turn_transition)
            + 0.9 * max(0.0, 0.82 - lr_ratio)
            + 0.5 * max(0.0, theta - 0.68)
            + 0.15 * max(0.0, theta_p95 - 1.85)
            + 0.05 * max(0.0, flat_p95 - 2.60)
        )
        out = dict(row)
        out["turn_lr_ratio"] = lr_ratio
        out["stage2_offline_score"] = score
        out["stage2_gate"] = int(acc_main >= 0.955 and slope_recall >= 0.970 and lr_ratio >= 0.78 and theta <= 0.75)
        ranked.append(out)
    ranked.sort(key=lambda x: (int(x["stage2_gate"]) == 0, float(x["stage2_offline_score"])))
    for i, row in enumerate(ranked, start=1):
        row["stage2_rank"] = i
    return ranked


def select_top_candidates(rows: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    selected = rows[: max(1, top_k)]
    for row in selected:
        seed = int(float(row["seed"]))
        row["onnx_file"] = str(Path(row["output_dir"]) / f"modern_tcn_seed{seed}.onnx")
    return selected


def export_selected(rows: List[Dict[str, Any]], args: argparse.Namespace) -> None:
    for row in rows:
        checkpoint = Path(row["checkpoint_file"])
        seed = int(float(row["seed"]))
        onnx_file = checkpoint.with_suffix(".onnx")
        sample_file = checkpoint.with_name(f"modern_tcn_seed{seed}_pytorch_reference.mat")
        if args.skip_existing and onnx_file.exists() and sample_file.exists():
            print(f"[stage2 modern] reuse ONNX: {onnx_file}")
        else:
            run_command(
                f"export_{Path(row['output_dir']).name}",
                [
                    sys.executable,
                    str(MODERN_SRC / "export_modern_tcn_onnx.py"),
                    "--checkpoint",
                    str(checkpoint),
                    "--sample-count",
                    str(args.sample_count),
                ],
            )
        run_command(
            f"ort_{Path(row['output_dir']).name}",
            [
                sys.executable,
                str(MODERN_SRC / "check_onnxruntime_consistency.py"),
                "--onnx-file",
                str(onnx_file),
                "--sample-file",
                str(sample_file),
            ],
        )


def refresh_selected_onnx(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    refreshed = []
    for row in rows:
        seed = int(float(row["seed"]))
        out = dict(row)
        out["onnx_file"] = str(Path(row["output_dir"]) / f"modern_tcn_seed{seed}.onnx")
        refreshed.append(out)
    return refreshed


def write_manifest(selected: List[Dict[str, Any]]) -> None:
    runs = [CHAMPION]
    for row in selected:
        seed = int(float(row["seed"]))
        runs.append(
            {
                "label": f"ModernTCN_stage2_{row['case']}_seed{seed}",
                "seed": seed,
                "run_tag": row["run_tag"],
                "onnx_file": row["onnx_file"],
                "offline_score": row["stage2_offline_score"],
                "offline_rank": row["stage2_rank"],
            }
        )
    manifest = {
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "dataset_file": str(DATASET_FILE),
        "selection_source": str(STAGE2_DIR / "stage2_modern_tcn_selected.csv"),
        "runs": runs,
    }
    (STAGE2_DIR / "stage2_closed_loop_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def run_command(name: str, command: List[str]) -> None:
    log_out = STAGE2_DIR / "logs" / f"{name}.stdout.log"
    log_err = STAGE2_DIR / "logs" / f"{name}.stderr.log"
    print(f"[stage2 command] {name}")
    with log_out.open("w", encoding="utf-8", errors="replace") as out, log_err.open(
        "w", encoding="utf-8", errors="replace"
    ) as err:
        proc = subprocess.run(command, cwd=ROOT, stdout=out, stderr=err, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"{name} failed with exit code {proc.returncode}; see {log_out} and {log_err}")


def read_summary_row(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise RuntimeError(f"Expected one row in {path}, got {len(rows)}")
    return rows[0]


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        return
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(preflight: Dict[str, Any], ranked: List[Dict[str, Any]], selected: List[Dict[str, Any]]) -> None:
    report = STAGE2_DIR / "stage2_modern_tcn_targeted_report.md"
    with report.open("w", encoding="utf-8") as f:
        f.write("# Stage 2 ModernTCN Targeted Search Report\n\n")
        f.write(f"- generated: `{time.strftime('%Y-%m-%d %H:%M:%S')}`\n")
        f.write(f"- dataset: `{DATASET_FILE}`\n")
        f.write(f"- preflight_pass: `{int(preflight['pass'])}`\n")
        f.write("- fixed: architecture, input_dim=22, passive17_plus_all5, plantfix raw/dataset\n\n")
        f.write("## Candidate Space\n\n")
        f.write("| case | lambda_turn | transition_weight | multipliers | note |\n")
        f.write("|---|---:|---:|---|---|\n")
        for case in CASES:
            f.write(
                f"| {case.case} | {case.lambda_turn:.3g} | {case.turn_transition_weight:.3g} | "
                f"{case.turn_class_multipliers} | {case.note} |\n"
            )
        if ranked:
            f.write("\n## Offline Ranking\n\n")
            keep = [
                "stage2_rank",
                "case",
                "seed",
                "stage2_gate",
                "stage2_offline_score",
                "acc_main",
                "acc_turn_transition",
                "turn_lr_ratio",
                "theta_mae_deg",
                "theta_abs_le_10_p95_abs_err_deg",
                "flat_recall",
                "slope_recall",
            ]
            write_md_table(f, ranked, keep)
        if selected:
            f.write("\n## Selected For Closed Loop\n\n")
            keep = ["stage2_rank", "case", "seed", "stage2_offline_score", "checkpoint_file", "onnx_file"]
            write_md_table(f, selected, keep)


def write_md_table(f, rows: List[Dict[str, Any]], keys: List[str]) -> None:
    f.write("| " + " | ".join(keys) + " |\n")
    f.write("|" + "|".join(["---"] * len(keys)) + "|\n")
    for row in rows:
        vals = [fmt(row.get(key, "")) for key in keys]
        f.write("| " + " | ".join(vals) + " |\n")


def fmt(value: Any) -> str:
    try:
        x = float(value)
        if math.isfinite(x):
            return f"{x:.6g}"
    except (TypeError, ValueError):
        pass
    return str(value)


def to_float(value: Any) -> float:
    try:
        x = float(value)
        return x if math.isfinite(x) else 0.0
    except (TypeError, ValueError):
        return 0.0


if __name__ == "__main__":
    main()
