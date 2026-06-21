"""Utilities for the exp2 dual-kernel ModernTCN ablation.

This file is intentionally independent from exp1_tools.py. It reads the shared
baseline snapshot but does not assume exp1 file names or directory structure.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
ABLATION_ROOT = ROOT / "results" / "modern_tcn_ablation"
EXP2_DIR = ABLATION_ROOT / "exp2_dual_kernel"
SNAPSHOT_DIR = ABLATION_ROOT / "_baseline_snapshot"
SCHEMA_DIR = ABLATION_ROOT / "_schemas"
PAPER_FLOW = ROOT / "results" / "paper" / "agv_model_parameter_correction_workflow"
DATASET = ROOT / "data" / "tcn" / "ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat"
CONTRACT = ROOT / "data" / "tcn" / "ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_contract.json"

CORE_KEYS = [
    "acc_main",
    "acc_turn",
    "acc_turn_transition",
    "theta_mae_deg",
    "flat_recall",
    "stall_recall",
    "slope_recall",
    "theta_edge_p95_abs_err",
    "false_turn_straight",
    "flat_peak_theta_error",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="exp2 dual-kernel ablation utility")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("d0")
    sub.add_parser("schema")
    sub.add_parser("baseline-boundary")
    sub.add_parser("summarize")
    single = sub.add_parser("single-gate")
    single.add_argument("--run-tag", required=True)
    preflight = sub.add_parser("closed-loop-preflight")
    preflight.add_argument("--best-run", required=True)
    preflight.add_argument("--onnx-file", type=Path, required=True)
    preflight.add_argument("--dataset-file", type=Path, default=DATASET)
    args = parser.parse_args()

    EXP2_DIR.mkdir(parents=True, exist_ok=True)
    if args.cmd == "d0":
        write_d0_reports()
    elif args.cmd == "schema":
        write_schema()
    elif args.cmd == "baseline-boundary":
        compute_baseline_boundary_metrics()
    elif args.cmd == "summarize":
        summarize()
    elif args.cmd == "single-gate":
        single_gate(args.run_tag)
    elif args.cmd == "closed-loop-preflight":
        write_closed_loop_preflight(args.best_run, args.onnx_file, args.dataset_file)


def read_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    rows = list(rows)
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    keys: List[str] = []
    for row in rows:
        for key in row.keys():
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def git_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(ROOT), text=True).strip()
    except Exception:
        return "unknown"


def git_status_short() -> str:
    try:
        return subprocess.check_output(["git", "status", "--short"], cwd=str(ROOT), text=True).strip()
    except Exception as exc:
        return f"git status failed: {exc}"


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except Exception:
        return str(path)


def write_d0_reports() -> None:
    manifest = read_json(SNAPSHOT_DIR / "baseline_artifact_manifest.json")
    contract = read_json(CONTRACT)
    default_cfg = ROOT / "src" / "ModernTCN" / "ModernTCN_default_config.m"
    default_text = default_cfg.read_text(encoding="utf-8")
    default_points_old = "v3_passive17_plus_all5" in default_text or "node6_v3" in default_text
    required = [
        Path(str(manifest["checkpoint"])),
        Path(str(manifest["onnx"])),
        DATASET,
        CONTRACT,
        PAPER_FLOW / "09_closed_loop" / "dual_modern_seed101_full" / "dual_modern_aggregate.csv",
    ]
    missing = [rel(p) for p in required if not p.exists()]
    ok = not missing and int(contract["input_dim"]) == 22 and int(contract["seq_len"]) == 128

    with (EXP2_DIR / "D0_preflight_baseline.md").open("w", encoding="utf-8") as f:
        f.write("# D0 Baseline Preflight\n\n")
        f.write(f"- pass: `{int(ok)}`\n")
        f.write(f"- git_hash_now: `{git_hash()}`\n")
        f.write(f"- snapshot_git_hash: `{manifest.get('git_hash', '')}`\n")
        f.write(f"- plant_revision: `{manifest.get('plant_revision', '')}`\n")
        f.write(f"- feature_contract: `{manifest.get('feature_contract', '')}`\n")
        f.write(f"- input_dim: `{contract['input_dim']}`\n")
        f.write(f"- seq_len: `{contract['seq_len']}`\n")
        f.write(f"- train/val/test windows: `{contract['train_windows']}/{contract['val_windows']}/{contract['test_windows']}`\n")
        f.write(f"- dataset: `{rel(DATASET)}`\n")
        f.write(f"- contract: `{rel(CONTRACT)}`\n")
        f.write(f"- baseline_checkpoint: `{rel(Path(str(manifest['checkpoint'])))}`\n")
        f.write(f"- baseline_onnx: `{rel(Path(str(manifest['onnx'])))}`\n")
        f.write("- closed_loop_baseline: `results/paper/agv_model_parameter_correction_workflow/09_closed_loop/dual_modern_seed101_full/`\n")
        f.write(f"- matlab_default_points_to_old_baseline: `{int(default_points_old)}`\n")
        if missing:
            f.write("\n## Missing\n\n")
            for item in missing:
                f.write(f"- `{item}`\n")
        f.write("\n## Feature Names\n\n")
        for idx, name in enumerate(contract["feature_names"], start=1):
            f.write(f"{idx}. `{name}`\n")

    with (EXP2_DIR / "default_path_alignment_exp2.md").open("w", encoding="utf-8") as f:
        f.write("# exp2 Default Path Alignment\n\n")
        f.write("- action: `no global default edit`\n")
        f.write(f"- matlab_default_config: `{rel(default_cfg)}`\n")
        f.write(f"- default_points_to_old_baseline: `{int(default_points_old)}`\n")
        f.write("- candidate_policy: pass ONNX and dataset explicitly in closed-loop scripts.\n")
        f.write("- old baseline artifacts: not deleted, moved, or overwritten.\n")
    if not ok:
        raise RuntimeError("D0 preflight failed; see D0_preflight_baseline.md")


def write_schema() -> None:
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    text = (
        "# Dual-kernel Metrics Schema\n\n"
        "Offline required columns: "
        + ", ".join(CORE_KEYS)
        + ".\n\n"
        "Boundary gate aliases:\n"
        "- theta_edge_p95_abs_err = max(theta_neg_10_8_p95_abs_err_deg, theta_pos_8_10_p95_abs_err_deg)\n"
        "- flat_peak_theta_error = theta_flat_abs_max_deg\n"
        "- false_turn_straight = ratio of true-straight turn labels predicted as left/right\n\n"
        "Closed-loop required columns: ey_rmse, xy_rmse, theta_mae_deg, main_acc_pct, "
        "turn_acc_pct, omega_cmd_rms, j_du or delta_u proxy, rank_ey.\n"
    )
    (SCHEMA_DIR / "dual_kernel_metrics_schema.md").write_text(text, encoding="utf-8")
    (EXP2_DIR / "D4_summary_tool_contract.md").write_text(
        "# D4 Summary Tool Contract\n\n"
        "- tool: `results/modern_tcn_ablation/exp2_tools.py`\n"
        "- exp1_dependency: `none required`\n"
        "- summary_outputs: `dual_kernel_offline_summary.csv`, `dual_kernel_offline_summary.md`, `best_run_selection.md`\n"
        "- gate_inputs: baseline snapshot CSV and exp2 run summaries.\n",
        encoding="utf-8",
    )


def to_float(row: Dict[str, object], key: str) -> float:
    try:
        return float(row.get(key, "nan"))
    except Exception:
        return float("nan")


def enrich_row(row: Dict[str, object]) -> Dict[str, object]:
    out = dict(row)
    out["theta_edge_p95_abs_err"] = max(
        to_float(out, "theta_neg_10_8_p95_abs_err_deg"),
        to_float(out, "theta_pos_8_10_p95_abs_err_deg"),
    )
    out["flat_peak_theta_error"] = to_float(out, "theta_flat_abs_max_deg")
    if "false_turn_straight" not in out:
        out["false_turn_straight"] = float("nan")
    return out


def baseline_metrics() -> Dict[str, object]:
    base = enrich_row(read_csv(SNAPSHOT_DIR / "baseline_offline_metrics.csv")[0])
    source = Path(str(base.get("source", "")))
    if source.exists():
        source_row = enrich_row(read_csv(source)[0])
        for key in CORE_KEYS:
            if key not in base or str(base.get(key, "")) in {"", "nan"}:
                base[key] = source_row.get(key, base.get(key, ""))
    boundary_file = EXP2_DIR / "baseline_boundary_metrics_exp2.csv"
    if not boundary_file.exists() or any(math.isnan(to_float(base, key)) for key in CORE_KEYS):
        compute_baseline_boundary_metrics()
    if boundary_file.exists():
        boundary = enrich_row(read_csv(boundary_file)[0])
        for key in CORE_KEYS:
            if key not in base or str(base.get(key, "")) in {"", "nan"} or math.isnan(to_float(base, key)):
                base[key] = boundary.get(key, base.get(key, ""))
    return base


def compute_baseline_boundary_metrics() -> None:
    sys.path.insert(0, str(ROOT / "src" / "ModernTCN"))
    import torch
    from torch.utils.data import DataLoader

    from modern_tcn_data import AGVWindowDataset, load_modern_tcn_dataset
    from modern_tcn_metrics import compute_metrics, metric_row, multitask_loss
    from modern_tcn_model import build_model_from_checkpoint_dict

    baseline = read_csv(SNAPSHOT_DIR / "baseline_offline_metrics.csv")[0]
    ckpt_file = Path(str(baseline["checkpoint_file"]))
    ckpt = torch.load(ckpt_file, map_location="cpu", weights_only=False)
    model = build_model_from_checkpoint_dict(ckpt).eval()
    data = load_modern_tcn_dataset(DATASET)
    split = data["test"]
    loader = DataLoader(AGVWindowDataset(split), batch_size=512, shuffle=False, num_workers=0)
    logits_main = []
    logits_turn = []
    theta_hat = []
    loss_sum = 0.0
    n_sum = 0
    cfg = model.cfg
    class_w_main = torch.ones(3, dtype=torch.float32)
    class_w_turn = torch.ones(3, dtype=torch.float32)
    with torch.no_grad():
        for batch in loader:
            lm, lt, th = model(batch["X"].float())
            loss, _ = multitask_loss(lm, lt, th, batch, class_w_main, class_w_turn, cfg)
            n = int(batch["X"].shape[0])
            loss_sum += float(loss.detach().cpu()) * n
            n_sum += n
            logits_main.append(lm.detach().cpu())
            logits_turn.append(lt.detach().cpu())
            theta_hat.append(th.detach().cpu())
    metrics = compute_metrics(
        torch.cat(logits_main, dim=0).numpy(),
        torch.cat(logits_turn, dim=0).numpy(),
        torch.cat(theta_hat, dim=0).numpy().reshape(-1),
        split,
        loss_sum / max(n_sum, 1),
    )
    row = metric_row(int(ckpt.get("seed", 101)), int(ckpt.get("best_epoch", 0)), metrics, {"checkpoint_file": str(ckpt_file)})
    row["model"] = "ModernTCN_turn_l020_tt25_seed101"
    row = enrich_row(row)
    row["source"] = "computed from frozen baseline checkpoint and v5 plantfix test split; no baseline retraining"
    write_csv(EXP2_DIR / "baseline_boundary_metrics_exp2.csv", [row])
    with (EXP2_DIR / "baseline_boundary_metrics_exp2.md").open("w", encoding="utf-8") as f:
        f.write("# exp2 Baseline Boundary Metrics\n\n")
        f.write("- action: `read-only PyTorch evaluation of frozen baseline checkpoint`\n")
        f.write("- retraining: `0`\n")
        f.write(f"- checkpoint: `{rel(ckpt_file)}`\n")
        f.write(f"- dataset: `{rel(DATASET)}`\n")
        for key in CORE_KEYS:
            f.write(f"- {key}: `{row.get(key, '')}`\n")


def offline_gate_failures(row: Dict[str, object], baseline: Dict[str, object]) -> List[str]:
    b = {key: to_float(baseline, key) for key in CORE_KEYS}
    checks = [
        ("acc_main", to_float(row, "acc_main"), ">=", b["acc_main"] - 0.003),
        ("acc_turn", to_float(row, "acc_turn"), ">=", b["acc_turn"] - 0.005),
        ("acc_turn_transition", to_float(row, "acc_turn_transition"), ">=", b["acc_turn_transition"]),
        ("theta_mae_deg", to_float(row, "theta_mae_deg"), "<=", b["theta_mae_deg"] + 0.01),
        ("slope_recall", to_float(row, "slope_recall"), ">=", b["slope_recall"] - 0.005),
        ("flat_recall", to_float(row, "flat_recall"), ">=", b["flat_recall"] - 0.01),
        ("stall_recall", to_float(row, "stall_recall"), ">=", b["stall_recall"] - 0.05),
        ("theta_edge_p95_abs_err", to_float(row, "theta_edge_p95_abs_err"), "<=", b["theta_edge_p95_abs_err"] + 0.05),
        ("false_turn_straight", to_float(row, "false_turn_straight"), "<=", b["false_turn_straight"] + 0.01),
        ("flat_peak_theta_error", to_float(row, "flat_peak_theta_error"), "<=", b["flat_peak_theta_error"] + 0.25),
    ]
    failures: List[str] = []
    for key, value, op, threshold in checks:
        if math.isnan(value) or math.isnan(threshold):
            failures.append(f"{key} missing for gate")
            continue
        ok = value >= threshold if op == ">=" else value <= threshold
        if not ok:
            failures.append(f"{key} {value:.6g} {op} {threshold:.6g} failed")
    return failures


def disaster_failures(row: Dict[str, object]) -> List[str]:
    checks = [
        ("acc_main", to_float(row, "acc_main"), ">=", 0.94),
        ("acc_turn", to_float(row, "acc_turn"), ">=", 0.50),
        ("theta_mae_deg", to_float(row, "theta_mae_deg"), "<=", 0.90),
        ("stall_recall", to_float(row, "stall_recall"), ">=", 0.55),
    ]
    failures = []
    for key, value, op, threshold in checks:
        ok = value >= threshold if op == ">=" else value <= threshold
        if not ok:
            failures.append(f"{key} {value:.6g} {op} {threshold:.6g} failed")
    return failures


def summary_for_run(run_dir: Path) -> Path:
    matches = sorted(run_dir.glob("modern_tcn_dualkernel_seed*_summary.csv"))
    if not matches:
        raise FileNotFoundError(f"No dual-kernel summary found in {run_dir}")
    return matches[0]


def single_gate(run_tag: str) -> None:
    run_dir = EXP2_DIR / run_tag
    row = enrich_row(read_csv(summary_for_run(run_dir))[0])
    failures = disaster_failures(row)
    ok = not failures
    with (EXP2_DIR / "D6_single_seed_gate.md").open("w", encoding="utf-8") as f:
        f.write("# D6 Single-seed Gate\n\n")
        f.write(f"- run_tag: `{run_tag}`\n")
        f.write(f"- pass: `{int(ok)}`\n")
        f.write(f"- summary: `{rel(summary_for_run(run_dir))}`\n")
        for key in ["acc_main", "acc_turn", "theta_mae_deg", "stall_recall", "acc_turn_transition"]:
            f.write(f"- {key}: `{row.get(key, '')}`\n")
        if failures:
            f.write("\n## Failures\n\n")
            for item in failures:
                f.write(f"- {item}\n")
    if not ok:
        raise RuntimeError("D6 single seed gate failed")


def summarize() -> None:
    baseline = baseline_metrics()
    rows: List[Dict[str, object]] = []
    for summary in sorted(EXP2_DIR.glob("dual_k*_seed*/modern_tcn_dualkernel_seed*_summary.csv")):
        run_dir = summary.parent
        row = enrich_row(read_csv(summary)[0])
        cfg = read_json(run_dir / "config.json") if (run_dir / "config.json").exists() else {}
        run_tag = run_dir.name
        config_name = run_tag.rsplit("_seed", 1)[0]
        out = dict(row)
        out["run_tag"] = run_tag
        out["config_name"] = config_name
        out["summary_file"] = str(summary)
        out["config_file"] = str(run_dir / "config.json")
        out["branch_group"] = "k31_default" if config_name in {"dual_k31_s3", "dual_k31_s5", "dual_k31_s7"} else "extension"
        out["large_kernel"] = nested_get(cfg, ["model_config", "large_kernel"], "")
        out["small_kernel"] = nested_get(cfg, ["model_config", "small_kernel"], "")
        out["dual_branch_scale"] = nested_get(cfg, ["model_config", "dual_branch_scale"], "")
        out["small_branch_init"] = nested_get(cfg, ["model_config", "small_branch_init"], "")
        failures = offline_gate_failures(out, baseline)
        out["offline_gate"] = int(not failures)
        out["offline_gate_failures"] = "; ".join(failures)
        rows.append(out)
    if not rows:
        raise FileNotFoundError(f"No dual-kernel summaries found under {EXP2_DIR}")

    write_csv(EXP2_DIR / "dual_kernel_offline_summary.csv", rows)
    passing = [r for r in rows if int(r["offline_gate"]) == 1]
    best = sorted(
        passing or rows,
        key=lambda r: (
            int(r.get("branch_group") == "extension"),
            -to_float(r, "offline_gate"),
            -to_float(r, "acc_turn_transition"),
            to_float(r, "theta_mae_deg"),
            -to_float(r, "acc_turn"),
        ),
    )[0]

    group_rows = group_summary(rows)
    with (EXP2_DIR / "dual_kernel_offline_summary.md").open("w", encoding="utf-8") as f:
        f.write("# dual_kernel Offline Summary\n\n")
        f.write(f"- baseline: `{baseline.get('model', '')}`\n")
        f.write(f"- runs: `{len(rows)}`\n")
        f.write(f"- passing_offline_gate: `{len(passing)}`\n")
        f.write(f"- best_run: `{best['run_tag']}`\n")
        f.write("- default_k31_configs: `dual_k31_s3`, `dual_k31_s5`, `dual_k31_s7`\n")
        f.write("- extension_configs_are_separate: `1`\n\n")
        f.write("## Group Means\n\n")
        f.write("| config | n | acc_main | acc_turn | acc_turn_transition | theta_mae_deg | gate_passes |\n")
        f.write("|---|---:|---:|---:|---:|---:|---:|\n")
        for row in group_rows:
            f.write(
                f"| `{row['config_name']}` | {row['n']} | {row['acc_main_mean']:.6f} | "
                f"{row['acc_turn_mean']:.6f} | {row['acc_turn_transition_mean']:.6f} | "
                f"{row['theta_mae_deg_mean']:.6f} | {row['gate_passes']} |\n"
            )

    with (EXP2_DIR / "best_run_selection.md").open("w", encoding="utf-8") as f:
        f.write("# Best Run Selection\n\n")
        f.write(f"- best_run: `{best['run_tag']}`\n")
        f.write(f"- offline_gate: `{best['offline_gate']}`\n")
        f.write(f"- branch_group: `{best['branch_group']}`\n")
        f.write(f"- checkpoint: `{best.get('checkpoint_file', '')}`\n")
        f.write(f"- failures: `{best.get('offline_gate_failures', '')}`\n")

    if not passing:
        write_no_promotion(rows, best)


def nested_get(obj: Dict[str, object], keys: List[str], default: object) -> object:
    cur: object = obj
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def group_summary(rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    groups: Dict[str, List[Dict[str, object]]] = {}
    for row in rows:
        groups.setdefault(str(row["config_name"]), []).append(row)
    out = []
    for name, items in sorted(groups.items()):
        row: Dict[str, object] = {"config_name": name, "n": len(items), "gate_passes": sum(int(x["offline_gate"]) for x in items)}
        for key in ["acc_main", "acc_turn", "acc_turn_transition", "theta_mae_deg", "stall_recall", "theta_edge_p95_abs_err"]:
            values = [to_float(x, key) for x in items]
            row[key + "_mean"] = sum(values) / len(values)
            row[key + "_std"] = stdev(values)
        out.append(row)
    return out


def stdev(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    return math.sqrt(sum((x - mean) ** 2 for x in values) / (len(values) - 1))


def write_no_promotion(rows: List[Dict[str, object]], best: Dict[str, object]) -> None:
    payload = {
        "decision": "NO_PROMOTION",
        "stop_node": "D8_offline_gate",
        "runs": len(rows),
        "best_run": best["run_tag"],
        "best_offline_gate_failures": best.get("offline_gate_failures", ""),
        "onnx_executed": False,
        "matlab_executed": False,
        "closed_loop_executed": False,
    }
    (EXP2_DIR / "promote_decision.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    with (EXP2_DIR / "dual_kernel_final_report.md").open("w", encoding="utf-8") as f:
        f.write("# dual_kernel Final Report\n\n")
        f.write("- decision: `NO_PROMOTION`\n")
        f.write("- stop_node: `D8_offline_gate`\n")
        f.write("- reason: no default dual-kernel candidate passed the offline and boundary gates.\n")
        f.write("- onnx/matlab/closed-loop: not executed.\n")


def write_closed_loop_preflight(best_run: str, onnx_file: Path, dataset_file: Path) -> None:
    onnx_file = onnx_file if onnx_file.is_absolute() else ROOT / onnx_file
    dataset_file = dataset_file if dataset_file.is_absolute() else ROOT / dataset_file
    out_root = ROOT / "results" / "compare" / "modern_tcn_ablation_closed_loop" / "exp2_dual_kernel" / best_run
    planned = [out_root / f"p{i:02d}" / f"m{i:02d}_out.mat" for i in range(1, 4)]
    lengths = {str(p): len(str(p)) for p in planned}
    preflight = {
        "best_run": best_run,
        "onnx_file": str(onnx_file),
        "dataset_file": str(dataset_file),
        "explicit_modern_tcn_sim_cfg_required": True,
        "uses_matlab_default_config_for_candidate": False,
        "output_root": str(out_root),
        "short_names": [p.name for p in planned],
        "path_lengths": lengths,
        "git_status_short": git_status_short(),
        "checks": {
            "onnx_exists": onnx_file.exists(),
            "dataset_exists": dataset_file.exists(),
            "output_does_not_overlap_baseline_compare": "dual_modern_seed101_full" not in str(out_root),
            "path_length_ok": max(lengths.values()) < 240,
        },
    }
    preflight["pass"] = all(bool(x) for x in preflight["checks"].values())
    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "closed_loop_preflight.json").write_text(json.dumps(preflight, indent=2, ensure_ascii=False), encoding="utf-8")
    with (out_root / "closed_loop_preflight.md").open("w", encoding="utf-8") as f:
        f.write("# exp2 dual_kernel Closed-loop Preflight\n\n")
        f.write(f"- pass: `{int(preflight['pass'])}`\n")
        f.write(f"- best_run: `{best_run}`\n")
        f.write(f"- onnx_file: `{onnx_file}`\n")
        f.write(f"- dataset_file: `{dataset_file}`\n")
        f.write(f"- output_root: `{out_root}`\n")
        f.write(f"- max_path_length: `{max(lengths.values())}`\n")
    if not preflight["pass"]:
        raise RuntimeError("Closed-loop preflight failed")


if __name__ == "__main__":
    main()
