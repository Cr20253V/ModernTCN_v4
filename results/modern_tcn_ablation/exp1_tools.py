"""Utilities for the 22D grouped-FFN ModernTCN ablation.

This script keeps exp1 support artifacts isolated under
``results/modern_tcn_ablation`` and never retrains or overwrites the current
plantfix champion.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
ABLATION_ROOT = ROOT / "results" / "modern_tcn_ablation"
SNAPSHOT_DIR = ABLATION_ROOT / "_baseline_snapshot"
SCHEMA_DIR = ABLATION_ROOT / "_schemas"
EXP1_DIR = ABLATION_ROOT / "exp1_grouped_ffn"
PAPER_FLOW = ROOT / "results" / "paper" / "agv_model_parameter_correction_workflow"
CHAMPION_DIR = (
    PAPER_FLOW
    / "08_models"
    / "modern_tcn"
    / "modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101"
)
DATASET_JSON = ROOT / "data" / "tcn" / "CURRENT_ModernTCN_DATASET.json"
CONTRACT_JSON = (
    ROOT
    / "data"
    / "tcn"
    / "ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_contract.json"
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Exp1 grouped-FFN ablation helper")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("snapshot")
    sub.add_parser("metrics")
    sub.add_parser("default-report")
    sub.add_parser("baseline-regression")
    summarize = sub.add_parser("summarize")
    summarize.add_argument("--exp-dir", type=Path, default=EXP1_DIR)
    offline_stop = sub.add_parser("offline-stop-report")
    offline_stop.add_argument("--exp-dir", type=Path, default=EXP1_DIR)
    preflight = sub.add_parser("closed-loop-preflight")
    preflight.add_argument("--best-run", type=str, required=True)
    preflight.add_argument("--onnx-file", type=Path, required=True)
    preflight.add_argument("--dataset-file", type=Path, default=Path(""))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.cmd == "snapshot":
        write_snapshot()
    elif args.cmd == "metrics":
        write_metrics()
    elif args.cmd == "default-report":
        write_default_report()
    elif args.cmd == "baseline-regression":
        run_baseline_regression()
    elif args.cmd == "summarize":
        summarize_exp1(args.exp_dir)
    elif args.cmd == "offline-stop-report":
        write_offline_stop_report(args.exp_dir)
    elif args.cmd == "closed-loop-preflight":
        write_closed_loop_preflight(args.best_run, args.onnx_file, args.dataset_file)


def read_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    rows = list(rows)
    if not rows:
        return
    fieldnames = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def git_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(ROOT), text=True).strip()
    except Exception:
        return "unknown"


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except Exception:
        return str(path)


def write_snapshot() -> None:
    current = read_json(DATASET_JSON)
    contract = read_json(CONTRACT_JSON)
    default_cfg = ROOT / "src" / "ModernTCN" / "ModernTCN_default_config.m"
    champion_ckpt = CHAMPION_DIR / "modern_tcn_seed101.pt"
    champion_onnx = CHAMPION_DIR / "modern_tcn_seed101.onnx"
    champion_ref = CHAMPION_DIR / "modern_tcn_seed101_pytorch_reference.mat"
    required = [DATASET_JSON, CONTRACT_JSON, champion_ckpt, champion_onnx, champion_ref]
    missing = [rel(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError("Missing baseline artifacts: " + ", ".join(missing))
    if int(contract["input_dim"]) != 22 or int(contract["seq_len"]) != 128:
        raise RuntimeError("Baseline contract is not 22D seq128.")
    if contract.get("feature_contract") != "passive17_plus_all5":
        raise RuntimeError("Baseline feature contract is not passive17_plus_all5.")

    default_text = default_cfg.read_text(encoding="utf-8")
    default_points_old = "v3_passive17_plus_all5" in default_text or "node6_v3" in default_text
    manifest = {
        "git_hash": git_hash(),
        "repository": str(ROOT),
        "plant_revision": "agv_physics_v2_plantfix",
        "feature_contract": contract["feature_contract"],
        "input_dim": contract["input_dim"],
        "seq_len": contract["seq_len"],
        "feature_names": contract["feature_names"],
        "window_counts": {
            "train": contract["train_windows"],
            "val": contract["val_windows"],
            "test": contract["test_windows"],
        },
        "dataset": current["canonical_files"]["dataset"],
        "dataset_contract": str(CONTRACT_JSON),
        "checkpoint": str(champion_ckpt),
        "onnx": str(champion_onnx),
        "pytorch_reference": str(champion_ref),
        "matlab_default_config": str(default_cfg),
        "matlab_default_points_to_old_baseline": default_points_old,
        "default_config_strategy": "Do not modify by default; exp1 closed-loop must pass modern_tcn_sim_cfg.onnx_file and dataset_file explicitly.",
    }
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    (SNAPSHOT_DIR / "baseline_artifact_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    with (SNAPSHOT_DIR / "baseline_identity.md").open("w", encoding="utf-8") as f:
        f.write("# Baseline Identity Snapshot\n\n")
        f.write(f"- git_hash: `{manifest['git_hash']}`\n")
        f.write(f"- plant_revision: `{manifest['plant_revision']}`\n")
        f.write(f"- feature_contract: `{manifest['feature_contract']}`\n")
        f.write(f"- input_dim: `{manifest['input_dim']}`\n")
        f.write(f"- seq_len: `{manifest['seq_len']}`\n")
        f.write(f"- train/val/test windows: `{contract['train_windows']}/{contract['val_windows']}/{contract['test_windows']}`\n")
        f.write(f"- checkpoint: `{rel(champion_ckpt)}`\n")
        f.write(f"- onnx: `{rel(champion_onnx)}`\n")
        f.write(f"- MATLAB default points to old baseline: `{int(default_points_old)}`\n\n")
        f.write("## Feature Names\n\n")
        for i, name in enumerate(contract["feature_names"], start=1):
            f.write(f"{i}. `{name}`\n")
    print(SNAPSHOT_DIR / "baseline_identity.md")


def write_metrics() -> None:
    summary = read_csv_rows(CHAMPION_DIR / "modern_tcn_seed101_summary.csv")[0]
    onnx_meta = read_json(CHAMPION_DIR / "modern_tcn_seed101_onnx_export.json")
    offline_keys = [
        "acc_main",
        "acc_turn",
        "acc_turn_transition",
        "theta_mae_deg",
        "theta_abs_le_10_p95_abs_err_deg",
        "flat_recall",
        "stall_recall",
        "slope_recall",
        "turn_right_recall",
        "turn_straight_recall",
        "turn_left_recall",
    ]
    offline = {k: summary.get(k, "") for k in offline_keys}
    offline.update(
        {
            "model": "ModernTCN_turn_l020_tt25_seed101",
            "checkpoint_file": str(CHAMPION_DIR / "modern_tcn_seed101.pt"),
            "onnx_file": str(CHAMPION_DIR / "modern_tcn_seed101.onnx"),
            "onnx_input_shape": json.dumps(onnx_meta.get("input_shape", [])),
            "source": str(CHAMPION_DIR / "modern_tcn_seed101_summary.csv"),
        }
    )
    write_csv(SNAPSHOT_DIR / "baseline_offline_metrics.csv", [offline])

    aggregate_file = PAPER_FLOW / "09_closed_loop" / "dual_modern_seed101_full" / "dual_modern_aggregate.csv"
    agg_rows = read_csv_rows(aggregate_file)
    champion_agg = next(r for r in agg_rows if r["controller"] == "ModernTCN_turn_l020_tt25_seed101")
    path_rows = []
    path_tags = [
        "path_factory_logistics_showcase_theta10_v3",
        "path_closed_loop_long_updown_theta10_v1",
        "path_closed_loop_sharp_turn_transition_theta10_v1",
    ]
    for tag in path_tags:
        path_file = PAPER_FLOW / "09_closed_loop" / "dual_modern_seed101_full" / tag / "dual_modern_closed_loop_summary.csv"
        if path_file.exists():
            rows = read_csv_rows(path_file)
            row = next((r for r in rows if r["controller"] == "ModernTCN_turn_l020_tt25_seed101"), None)
            if row:
                row = dict(row)
                row["path_tag"] = tag
                row["source"] = str(path_file)
                path_rows.append(row)
    closed = {"controller": "ModernTCN_turn_l020_tt25_seed101", "scope": "aggregate", **champion_agg, "source": str(aggregate_file)}
    write_csv(SNAPSHOT_DIR / "baseline_closed_loop_metrics.csv", [closed, *path_rows])

    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    (SCHEMA_DIR / "ablation_metrics_schema.md").write_text(
        "# Ablation Metrics Schema\n\n"
        "Offline required columns: acc_main, acc_turn, acc_turn_transition, theta_mae_deg, "
        "flat_recall, stall_recall, slope_recall, turn_right_recall, turn_straight_recall, turn_left_recall.\n\n"
        "Closed-loop required columns: ey_rmse, xy_rmse, theta_mae_deg, main_acc_pct, turn_acc_pct, "
        "omega_cmd_rms, j_du, rank_ey or rank table.\n",
        encoding="utf-8",
    )
    with (SNAPSHOT_DIR / "baseline_summary.md").open("w", encoding="utf-8") as f:
        f.write("# Baseline Summary\n\n")
        f.write("All values below are read from existing plantfix artifacts. No baseline retraining or Simulink run was triggered.\n\n")
        f.write(f"- offline summary: `{rel(CHAMPION_DIR / 'modern_tcn_seed101_summary.csv')}`\n")
        f.write(f"- closed-loop aggregate: `{rel(aggregate_file)}`\n")
        f.write(f"- acc_main: `{summary['acc_main']}`\n")
        f.write(f"- acc_turn: `{summary['acc_turn']}`\n")
        f.write(f"- acc_turn_transition: `{summary['acc_turn_transition']}`\n")
        f.write(f"- theta_mae_deg: `{summary['theta_mae_deg']}`\n")
        f.write(f"- aggregate ey_rmse_mean: `{champion_agg['ey_rmse_mean']}`\n")
        f.write(f"- aggregate xy_rmse_mean: `{champion_agg['xy_rmse_mean']}`\n")
    print(SNAPSHOT_DIR / "baseline_summary.md")


def write_default_report() -> None:
    default_cfg = ROOT / "src" / "ModernTCN" / "ModernTCN_default_config.m"
    text = default_cfg.read_text(encoding="utf-8")
    default_points_old = "v3_passive17_plus_all5" in text or "node6_v3" in text
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    with (SNAPSHOT_DIR / "default_path_alignment_report.md").open("w", encoding="utf-8") as f:
        f.write("# Default Path Alignment Report\n\n")
        f.write("- action: `no global default edit`\n")
        f.write(f"- default_points_to_old_baseline: `{int(default_points_old)}`\n")
        f.write("- reason: exp1 closed-loop runners must pass `modern_tcn_sim_cfg.onnx_file` and `dataset_file` explicitly.\n")
        f.write("- current champion remains available through the baseline snapshot manifest.\n")
        f.write("- old v3/seed21 artifacts were not deleted, moved, or overwritten.\n")
    print(SNAPSHOT_DIR / "default_path_alignment_report.md")


def run_baseline_regression() -> None:
    sys.path.insert(0, str(ROOT / "src" / "ModernTCN"))
    import torch
    from modern_tcn_model import build_model_from_checkpoint_dict

    ckpt_file = CHAMPION_DIR / "modern_tcn_seed101.pt"
    ckpt = torch.load(ckpt_file, map_location="cpu", weights_only=False)
    model = build_model_from_checkpoint_dict(ckpt)
    model.eval()
    x = torch.zeros(2, int(ckpt["model_config"]["seq_len"]), int(ckpt["model_config"]["input_dim"]))
    with torch.no_grad():
        out = model(x)
    shapes = [list(t.shape) for t in out]
    ok = shapes == [[2, 3], [2, 3], [2, 1]]
    out_dir = EXP1_DIR / "_engineering_preflight"
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "baseline_small_regression.md").open("w", encoding="utf-8") as f:
        f.write("# Baseline Small Regression\n\n")
        f.write(f"- checkpoint: `{rel(ckpt_file)}`\n")
        f.write(f"- model_family: `{ckpt.get('model_family')}`\n")
        f.write(f"- input_shape: `[2,128,22]`\n")
        f.write(f"- output_shapes: `{shapes}`\n")
        f.write(f"- pass: `{int(ok)}`\n")
    if not ok:
        raise RuntimeError(f"Unexpected baseline output shapes: {shapes}")
    print(out_dir / "baseline_small_regression.md")


def to_float(row: Dict[str, str], key: str) -> float:
    try:
        return float(row.get(key, "nan"))
    except Exception:
        return float("nan")


def summarize_exp1(exp_dir: Path) -> None:
    baseline = read_csv_rows(SNAPSHOT_DIR / "baseline_offline_metrics.csv")[0]
    baseline_f = {k: to_float(baseline, k) for k in baseline}
    rows = []
    for summary in sorted(exp_dir.glob("*/modern_tcn_gffn_seed*_summary.csv")):
        row = read_csv_rows(summary)[0]
        run_dir = summary.parent
        cfg_file = run_dir / "config.json"
        cfg = read_json(cfg_file) if cfg_file.exists() else {}
        run_tag = run_dir.name
        group = run_tag.rsplit("_seed", 1)[0]
        out = dict(row)
        out["run_tag"] = run_tag
        out["config_name"] = group
        out["summary_file"] = str(summary)
        out["param_count"] = count_params(run_dir / f"modern_tcn_gffn_seed{row['seed']}.pt")
        failures = offline_gate_failures(out, baseline_f)
        out["offline_gate"] = int(not failures)
        out["offline_gate_failures"] = "; ".join(failures)
        rows.append(out)
    if not rows:
        raise FileNotFoundError(f"No grouped-FFN summaries found under {exp_dir}")
    write_csv(exp_dir / "grouped_ffn_offline_summary.csv", rows)

    groups = {}
    for row in rows:
        groups.setdefault(row["config_name"], []).append(row)
    group_summary = []
    for name, items in groups.items():
        item = {"config_name": name, "n": len(items)}
        for key in ["acc_main", "acc_turn", "acc_turn_transition", "theta_mae_deg", "flat_recall", "stall_recall", "slope_recall"]:
            values = [to_float(r, key) for r in items]
            item[key + "_mean"] = sum(values) / len(values)
            item[key + "_std"] = stdev(values)
        group_summary.append(item)

    passing = [r for r in rows if int(r["offline_gate"]) == 1]
    best = sorted(
        passing or rows,
        key=lambda r: (
            -to_float(r, "acc_turn_transition"),
            to_float(r, "theta_mae_deg"),
            -to_float(r, "acc_turn"),
            to_float(r, "param_count"),
        ),
    )[0]
    k51_reason = k51_decision(rows, groups, baseline_f, bool(passing))
    with (exp_dir / "grouped_ffn_offline_summary.md").open("w", encoding="utf-8") as f:
        f.write("# grouped_ffn Offline Summary\n\n")
        f.write(f"- baseline: `{baseline['model']}`\n")
        f.write(f"- runs: `{len(rows)}`\n")
        f.write(f"- passing_offline_gate: `{len(passing)}`\n")
        f.write(f"- best_run: `{best['run_tag']}`\n")
        f.write(f"- k51_decision: `{k51_reason['decision']}`\n")
        f.write(f"- k51_reason: {k51_reason['reason']}\n")
    with (exp_dir / "best_run_selection.md").open("w", encoding="utf-8") as f:
        f.write("# Best Run Selection\n\n")
        f.write(f"- best_run: `{best['run_tag']}`\n")
        f.write(f"- offline_gate: `{best['offline_gate']}`\n")
        f.write(f"- checkpoint: `{best.get('checkpoint_file', '')}`\n")
        f.write(f"- k51_decision: `{k51_reason['decision']}`\n")
        f.write(f"- k51_reason: {k51_reason['reason']}\n")
    print(exp_dir / "grouped_ffn_offline_summary.md")


def count_params(checkpoint: Path) -> int:
    if not checkpoint.exists():
        return -1
    try:
        sys.path.insert(0, str(ROOT / "src" / "ModernTCN"))
        import torch
        from modern_tcn_model import build_model_from_checkpoint_dict

        ckpt = torch.load(checkpoint, map_location="cpu", weights_only=False)
        model = build_model_from_checkpoint_dict(ckpt)
        return int(sum(p.numel() for p in model.parameters()))
    except Exception:
        return -1


def offline_gate(row: Dict[str, object], baseline: Dict[str, float]) -> bool:
    return not offline_gate_failures(row, baseline)


def offline_gate_failures(row: Dict[str, object], baseline: Dict[str, float]) -> List[str]:
    checks = [
        ("acc_main", to_float(row, "acc_main"), ">=", baseline["acc_main"] - 0.003),
        ("acc_turn", to_float(row, "acc_turn"), ">=", baseline["acc_turn"] - 0.005),
        ("acc_turn_transition", to_float(row, "acc_turn_transition"), ">=", baseline["acc_turn_transition"]),
        ("theta_mae_deg", to_float(row, "theta_mae_deg"), "<=", baseline["theta_mae_deg"] + 0.01),
        ("slope_recall", to_float(row, "slope_recall"), ">=", baseline["slope_recall"] - 0.005),
        ("flat_recall", to_float(row, "flat_recall"), ">=", baseline["flat_recall"] - 0.01),
        ("stall_recall", to_float(row, "stall_recall"), ">=", baseline["stall_recall"] - 0.05),
    ]
    failures = []
    for key, value, op, threshold in checks:
        ok = value >= threshold if op == ">=" else value <= threshold
        if not ok:
            failures.append(f"{key} {value:.6g} {op} {threshold:.6g} failed")
    return failures


def write_offline_stop_report(exp_dir: Path) -> None:
    summary_file = exp_dir / "grouped_ffn_offline_summary.csv"
    if not summary_file.exists():
        summarize_exp1(exp_dir)
    rows = read_csv_rows(summary_file)
    if not rows:
        raise RuntimeError(f"No rows in {summary_file}")
    baseline = read_csv_rows(SNAPSHOT_DIR / "baseline_offline_metrics.csv")[0]
    best = sorted(
        rows,
        key=lambda r: (
            -to_float(r, "acc_turn_transition"),
            to_float(r, "theta_mae_deg"),
            -to_float(r, "acc_turn"),
            to_float(r, "param_count"),
        ),
    )[0]
    passing = [r for r in rows if str(r.get("offline_gate", "0")) == "1"]
    top_rows = sorted(
        rows,
        key=lambda r: (
            -to_float(r, "acc_turn_transition"),
            to_float(r, "theta_mae_deg"),
            -to_float(r, "acc_turn"),
        ),
    )[:5]

    report = exp_dir / "grouped_ffn_final_report.md"
    decision = exp_dir / "promote_decision.json"
    with report.open("w", encoding="utf-8") as f:
        f.write("# grouped_ffn Final Report\n\n")
        f.write("## Decision\n\n")
        f.write("- decision: `NO_PROMOTION`\n")
        f.write("- stop_node: `node8_offline_gate`\n")
        f.write("- reason: no grouped_ffn run passed the quantified offline promotion gate; ONNX, MATLAB, and closed-loop nodes were not executed.\n")
        f.write("- attribution_boundary: same 22D plantfix dataset and near-baseline training recipe; conclusion is limited to this grouped FFN structure/recipe combination.\n\n")
        f.write("## Baseline\n\n")
        for key in ["acc_main", "acc_turn", "acc_turn_transition", "theta_mae_deg", "flat_recall", "stall_recall", "slope_recall"]:
            f.write(f"- {key}: `{baseline[key]}`\n")
        f.write("\n## Best Offline Candidate\n\n")
        f.write(f"- run_tag: `{best['run_tag']}`\n")
        f.write(f"- checkpoint: `{best.get('checkpoint_file', '')}`\n")
        f.write(f"- offline_gate: `{best.get('offline_gate', '0')}`\n")
        f.write(f"- offline_gate_failures: `{best.get('offline_gate_failures', '')}`\n")
        for key in ["acc_main", "acc_turn", "acc_turn_transition", "theta_mae_deg", "flat_recall", "stall_recall", "slope_recall", "param_count"]:
            f.write(f"- {key}: `{best.get(key, '')}`\n")
        f.write("\n## Top Offline Runs\n\n")
        f.write("| run_tag | acc_main | acc_turn | acc_turn_transition | theta_mae_deg | failures |\n")
        f.write("|---|---:|---:|---:|---:|---|\n")
        for row in top_rows:
            f.write(
                f"| `{row['run_tag']}` | {to_float(row, 'acc_main'):.6f} | {to_float(row, 'acc_turn'):.6f} | "
                f"{to_float(row, 'acc_turn_transition'):.6f} | {to_float(row, 'theta_mae_deg'):.6f} | "
                f"{row.get('offline_gate_failures', '')} |\n"
            )
        f.write("\n## Evidence Files\n\n")
        f.write(f"- offline summary csv: `{summary_file}`\n")
        f.write(f"- offline summary md: `{exp_dir / 'grouped_ffn_offline_summary.md'}`\n")
        f.write(f"- best selection: `{exp_dir / 'best_run_selection.md'}`\n")
        f.write(f"- baseline snapshot: `{SNAPSHOT_DIR / 'baseline_offline_metrics.csv'}`\n")
        f.write("\n## Not Executed\n\n")
        f.write("- ONNX export: not executed because node8 gate failed.\n")
        f.write("- ONNXRuntime latency: not executed because node8 gate failed.\n")
        f.write("- MATLAB ONNX consistency: not executed because node8 gate failed.\n")
        f.write("- closed-loop preflight and Simulink runs: not executed because node8 gate failed.\n")

    payload = {
        "decision": "NO_PROMOTION",
        "stop_node": "node8_offline_gate",
        "passing_offline_gate": len(passing),
        "runs": len(rows),
        "best_run": best["run_tag"],
        "best_checkpoint": best.get("checkpoint_file", ""),
        "best_offline_gate_failures": best.get("offline_gate_failures", ""),
        "onnx_executed": False,
        "matlab_executed": False,
        "closed_loop_executed": False,
    }
    decision.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(report)


def k51_decision(rows: List[Dict[str, object]], groups: Dict[str, List[Dict[str, object]]], baseline: Dict[str, float], has_passing: bool) -> Dict[str, str]:
    if has_passing:
        return {"decision": "skip", "reason": "At least one run already passes the full offline gate."}
    for row in rows:
        disaster = (
            to_float(row, "acc_main") < 0.94
            or to_float(row, "acc_turn") < 0.50
            or to_float(row, "acc_turn_transition") < 0.40
            or to_float(row, "theta_mae_deg") > 0.90
        )
        near = sum(
            [
                to_float(row, "acc_turn_transition") >= baseline["acc_turn_transition"] - 0.015,
                to_float(row, "acc_turn") >= baseline["acc_turn"] - 0.015,
                to_float(row, "theta_mae_deg") <= baseline["theta_mae_deg"] + 0.04,
                to_float(row, "acc_main") >= baseline["acc_main"] - 0.008,
            ]
        )
        if near >= 2 and not disaster:
            return {"decision": "run_gffn_d4_k51", "reason": f"{row['run_tag']} has {near} near-threshold core metrics and no disaster regression."}
    return {"decision": "skip", "reason": "No candidate is close enough to the offline gate without disaster regression."}


def stdev(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    return math.sqrt(sum((v - mean) ** 2 for v in values) / (len(values) - 1))


def write_closed_loop_preflight(best_run: str, onnx_file: Path, dataset_file: Path) -> None:
    if not onnx_file.is_absolute():
        onnx_file = ROOT / onnx_file
    if not dataset_file:
        contract = read_json(CONTRACT_JSON)
        dataset_file = Path(contract["output_file"])
    elif not dataset_file.is_absolute():
        dataset_file = ROOT / dataset_file
    out_root = ROOT / "results" / "compare" / "modern_tcn_ablation_closed_loop" / "exp1_grouped_ffn" / best_run
    path_tags = ["p01", "p02", "p03"]
    mat_names = ["m01_out.mat", "m02_out.mat", "m03_out.mat"]
    planned_paths = [out_root / tag / mat for tag, mat in zip(path_tags, mat_names)]
    lengths = {str(p): len(str(p)) for p in planned_paths}
    preflight = {
        "best_run": best_run,
        "onnx_file": str(onnx_file),
        "dataset_file": str(dataset_file),
        "explicit_modern_tcn_sim_cfg_required": True,
        "uses_matlab_default_config_for_candidate": False,
        "output_root": str(out_root),
        "short_path_policy": {"path_dirs": path_tags, "mat_files": mat_names, "max_path_length": max(lengths.values())},
        "path_lengths": lengths,
        "checks": {
            "onnx_exists": onnx_file.exists(),
            "dataset_exists": dataset_file.exists(),
            "output_does_not_overlap_stage1": "dual_modern_seed101_full" not in str(out_root) and "stage1_closed_loop" not in str(out_root),
            "path_length_ok": max(lengths.values()) < 240,
        },
        "mpc_maps": str(PAPER_FLOW / "06_mpc_retuning" / "maps_best_agv_physics_v2_plantfix_stage1.mat"),
    }
    preflight["pass"] = all(bool(v) for v in preflight["checks"].values())
    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "closed_loop_preflight.json").write_text(json.dumps(preflight, indent=2, ensure_ascii=False), encoding="utf-8")
    with (out_root / "closed_loop_preflight.md").open("w", encoding="utf-8") as f:
        f.write("# Closed-loop Preflight\n\n")
        f.write(f"- best_run: `{best_run}`\n")
        f.write(f"- onnx_file: `{onnx_file}`\n")
        f.write(f"- dataset_file: `{dataset_file}`\n")
        f.write("- candidate loading: explicit `modern_tcn_sim_cfg.onnx_file` / `dataset_file`\n")
        f.write(f"- output_root: `{out_root}`\n")
        f.write(f"- max_path_length: `{max(lengths.values())}`\n")
        f.write(f"- pass: `{int(preflight['pass'])}`\n")
    if not preflight["pass"]:
        raise RuntimeError("Closed-loop preflight failed; see closed_loop_preflight.json")
    print(out_root / "closed_loop_preflight.md")


if __name__ == "__main__":
    main()
