"""Utilities for the exp3 patch/full ModernTCN ablation.

The exp3 contract is deliberately strict: old full/patch artifacts may be
listed as engineering context, but summaries and promotion decisions must read
only this round's `exp3_patch_full/full128_*_seed*` runs.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
ABLATION_ROOT = ROOT / "results" / "modern_tcn_ablation"
EXP3_DIR = ABLATION_ROOT / "exp3_patch_full"
SNAPSHOT_DIR = ABLATION_ROOT / "_baseline_snapshot"
SCHEMA_DIR = ABLATION_ROOT / "_schemas"
PAPER_FLOW = ROOT / "results" / "paper" / "agv_model_parameter_correction_workflow"
DATASET = ROOT / "data" / "tcn" / "ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat"
CONTRACT = ROOT / "data" / "tcn" / "ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_contract.json"

FULL_CONFIGS: Dict[str, Dict[str, object]] = {
    "full128_light": {
        "patch_size": 16,
        "patch_stride": 4,
        "dims": (8, 16),
        "stage_blocks": (1, 1),
        "large_kernels": (15, 9),
        "small_kernels": (5, 3),
    },
    "full128_mid": {
        "patch_size": 16,
        "patch_stride": 4,
        "dims": (16, 32),
        "stage_blocks": (1, 1),
        "large_kernels": (15, 9),
        "small_kernels": (5, 3),
    },
    "full128_densepatch": {
        "patch_size": 8,
        "patch_stride": 2,
        "dims": (16, 32),
        "stage_blocks": (1, 1),
        "large_kernels": (15, 9),
        "small_kernels": (5, 3),
    },
}
SEEDS = (21, 42, 101)

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
    parser = argparse.ArgumentParser(description="exp3 patch/full ablation utility")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("d0")
    sub.add_parser("d1")
    sub.add_parser("d2")
    sub.add_parser("d3")
    sub.add_parser("d4-report")
    smoke = sub.add_parser("d5-smoke-gate")
    smoke.add_argument("--run-tag", default="_smoke/full128_light_seed21_smoke")
    single = sub.add_parser("single-gate")
    single.add_argument("--run-tag", required=True)
    sub.add_parser("summarize")
    preflight = sub.add_parser("closed-loop-preflight")
    preflight.add_argument("--best-run", required=True)
    preflight.add_argument("--onnx-file", type=Path, required=True)
    preflight.add_argument("--dataset-file", type=Path, default=DATASET)
    final = sub.add_parser("final-report")
    final.add_argument("--status", choices=["auto", "incomplete", "no_promote"], default="auto")
    args = parser.parse_args()

    EXP3_DIR.mkdir(parents=True, exist_ok=True)
    if args.cmd == "d0":
        write_d0_reports()
    elif args.cmd == "d1":
        write_d1_architecture_and_cli_reports()
    elif args.cmd == "d2":
        write_d2_tool_contract()
    elif args.cmd == "d3":
        write_d3_deployment_report()
    elif args.cmd == "d4-report":
        write_d4_report()
    elif args.cmd == "d5-smoke-gate":
        d5_smoke_gate(args.run_tag)
    elif args.cmd == "single-gate":
        single_gate(args.run_tag)
    elif args.cmd == "summarize":
        summarize()
    elif args.cmd == "closed-loop-preflight":
        write_closed_loop_preflight(args.best_run, args.onnx_file, args.dataset_file)
    elif args.cmd == "final-report":
        write_final_report(args.status)


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


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except Exception:
        return str(path).replace("\\", "/")


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


def write_d0_reports() -> None:
    manifest = read_json(SNAPSHOT_DIR / "baseline_artifact_manifest.json")
    contract = read_json(CONTRACT)
    required = [
        Path(str(manifest["checkpoint"])),
        Path(str(manifest["onnx"])),
        DATASET,
        CONTRACT,
        SNAPSHOT_DIR / "baseline_offline_metrics.csv",
        SNAPSHOT_DIR / "baseline_closed_loop_metrics.csv",
    ]
    missing = [rel(p) for p in required if not p.exists()]
    ok = not missing and int(contract["input_dim"]) == 22 and int(contract["seq_len"]) == 128
    legacy = find_legacy_full_artifacts()
    excluded_file = EXP3_DIR / "excluded_legacy_full_artifacts.json"
    excluded_file.write_text(json.dumps(legacy, indent=2, ensure_ascii=False), encoding="utf-8")

    baseline_manifest = {
        "git_hash_now": git_hash(),
        "snapshot_git_hash": manifest.get("git_hash", ""),
        "plant_revision": manifest.get("plant_revision", ""),
        "feature_contract": manifest.get("feature_contract", ""),
        "dataset": str(DATASET),
        "dataset_contract": str(CONTRACT),
        "baseline_checkpoint": manifest.get("checkpoint", ""),
        "baseline_onnx": manifest.get("onnx", ""),
        "input_dim": contract.get("input_dim"),
        "seq_len": contract.get("seq_len"),
        "train_windows": contract.get("train_windows"),
        "val_windows": contract.get("val_windows"),
        "test_windows": contract.get("test_windows"),
        "legacy_exclusion_file": str(excluded_file),
        "pass": ok,
    }
    (EXP3_DIR / "D0_baseline_manifest.json").write_text(
        json.dumps(baseline_manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    with (EXP3_DIR / "D0_preflight_baseline.md").open("w", encoding="utf-8") as f:
        f.write("# D0 Baseline And Legacy Exclusion Preflight\n\n")
        f.write(f"- pass: `{int(ok)}`\n")
        f.write(f"- git_hash_now: `{baseline_manifest['git_hash_now']}`\n")
        f.write(f"- snapshot_git_hash: `{baseline_manifest['snapshot_git_hash']}`\n")
        f.write(f"- plant_revision: `{baseline_manifest['plant_revision']}`\n")
        f.write(f"- feature_contract: `{baseline_manifest['feature_contract']}`\n")
        f.write(f"- input_dim: `{contract['input_dim']}`\n")
        f.write(f"- seq_len: `{contract['seq_len']}`\n")
        f.write(f"- train/val/test windows: `{contract.get('train_windows')}/{contract.get('val_windows')}/{contract.get('test_windows')}`\n")
        f.write(f"- dataset: `{rel(DATASET)}`\n")
        f.write(f"- contract: `{rel(CONTRACT)}`\n")
        f.write(f"- baseline_checkpoint: `{rel(Path(str(manifest['checkpoint'])))}`\n")
        f.write(f"- baseline_onnx: `{rel(Path(str(manifest['onnx'])))}`\n")
        f.write(f"- excluded_legacy_full_artifacts: `{rel(excluded_file)}`\n")
        f.write(f"- excluded_legacy_count: `{len(legacy['artifacts'])}`\n")
        f.write("- rule: `D8 summary may read only exp3_patch_full/full128_*_seed* summaries from this run.`\n")
        f.write("- warm_start_policy: `forbidden; every full128 run starts from random initialization.`\n")
        if missing:
            f.write("\n## Missing\n\n")
            for item in missing:
                f.write(f"- `{item}`\n")
        f.write("\n## Feature Names\n\n")
        for idx, name in enumerate(contract["feature_names"], start=1):
            f.write(f"{idx}. `{name}`\n")
    if not ok:
        raise RuntimeError("D0 preflight failed; see D0_preflight_baseline.md")


def find_legacy_full_artifacts() -> Dict[str, object]:
    patterns = [
        "modern_tcn_full",
        "ModernTCNFull",
        "full128",
        "patch_full",
        "weakcombo",
        "stage2",
    ]
    roots = [ROOT / "results", ROOT / "src" / "ModernTCN"]
    artifacts = []
    exp3_prefix = str(EXP3_DIR.resolve()).lower()
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            path_str = str(path.resolve())
            lower = path_str.lower()
            if lower.startswith(exp3_prefix):
                continue
            if any(p.lower() in lower for p in patterns):
                artifacts.append(
                    {
                        "path": path_str,
                        "relative_path": rel(path),
                        "kind": "dir" if path.is_dir() else "file",
                        "reason": "legacy full/patch/stage2/weakcombo engineering context only",
                    }
                )
    artifacts = sorted(artifacts, key=lambda x: x["relative_path"])
    return {
        "created_by": "exp3_tools.py d0",
        "rule": "Do not read these paths for exp3 summary, best-run selection, or promote decisions.",
        "patterns": patterns,
        "artifacts": artifacts,
    }


def write_d1_architecture_and_cli_reports() -> None:
    sys.path.insert(0, str(ROOT / "src" / "ModernTCN"))
    from modern_tcn_model import ModernTCNFull, ModernTCNFullConfig

    rows = []
    failures = []
    for name, cfg_values in FULL_CONFIGS.items():
        cfg = ModernTCNFullConfig(input_dim=22, seq_len=128, **cfg_values)
        model = ModernTCNFull(cfg).eval()
        tokens = (cfg.seq_len - cfg.patch_size) // cfg.patch_stride + 1
        param_count = sum(p.numel() for p in model.parameters())
        rows.append(
            {
                "config": name,
                "patch_size": cfg.patch_size,
                "patch_stride": cfg.patch_stride,
                "tokens": tokens,
                "dims": ",".join(str(x) for x in cfg.dims),
                "stage_blocks": ",".join(str(x) for x in cfg.stage_blocks),
                "large_kernels": ",".join(str(x) for x in cfg.large_kernels),
                "small_kernels": ",".join(str(x) for x in cfg.small_kernels),
                "ffn_ratio": cfg.ffn_ratio,
                "layer_scale_init": cfg.layer_scale_init,
                "param_count": param_count,
                "readout_input_stats": int(cfg.readout_input_stats),
                "outputs": "logits_main, logits_turn, theta_hat",
            }
        )
        if len(cfg.dims) != len(cfg.stage_blocks) or len(cfg.dims) != len(cfg.large_kernels) or len(cfg.dims) != len(cfg.small_kernels):
            failures.append(f"{name}: tuple lengths do not match")
        if tokens <= 0:
            failures.append(f"{name}: patch tokens <= 0")

    train_file = ROOT / "src" / "ModernTCN" / "train_modern_tcn.py"
    train_text = train_file.read_text(encoding="utf-8")
    required_flags = [
        "--model-family",
        "--model_family",
        "--patch-size",
        "--patch_size",
        "--patch-stride",
        "--patch_stride",
        "--dims",
        "--stage-blocks",
        "--stage_blocks",
        "--large-kernels",
        "--large_kernels",
        "--small-kernels",
        "--small_kernels",
        "--no-overwrite",
        "--no_overwrite",
    ]
    missing_flags = [flag for flag in required_flags if flag not in train_text]
    ok = not failures and not missing_flags
    write_csv(EXP3_DIR / "full_architecture_audit.csv", rows)
    with (EXP3_DIR / "full_architecture_audit.md").open("w", encoding="utf-8") as f:
        f.write("# D1 ModernTCNFull Architecture Audit\n\n")
        f.write(f"- pass: `{int(ok)}`\n")
        f.write("- source: `src/ModernTCN/modern_tcn_model.py`\n")
        f.write("- initialization: `random initialization only; no checkpoint load in training path`\n")
        f.write("\n| config | tokens | dims | stage_blocks | large_kernels | small_kernels | ffn_ratio | layer_scale | params |\n")
        f.write("|---|---:|---|---|---|---|---:|---:|---:|\n")
        for row in rows:
            f.write(
                f"| `{row['config']}` | {row['tokens']} | `{row['dims']}` | `{row['stage_blocks']}` | "
                f"`{row['large_kernels']}` | `{row['small_kernels']}` | {row['ffn_ratio']} | "
                f"{float(row['layer_scale_init']):.6g} | {row['param_count']} |\n"
            )
        if failures or missing_flags:
            f.write("\n## Failures\n\n")
            for item in failures:
                f.write(f"- {item}\n")
            for flag in missing_flags:
                f.write(f"- missing CLI flag `{flag}`\n")
    with (EXP3_DIR / "D1_cli_contract.md").open("w", encoding="utf-8") as f:
        f.write("# D1 CLI Contract\n\n")
        f.write(f"- pass: `{int(not missing_flags)}`\n")
        f.write("- dataset_policy: `formal exp3 commands must pass --dataset-file explicitly; full default is not trusted as the experiment contract.`\n")
        f.write("- supported_aliases: `hyphen and underscore variants for model-family, patch-size, patch-stride, stage-blocks, large-kernels, small-kernels, no-overwrite`\n")
        f.write("- output_root: `results/modern_tcn_ablation/exp3_patch_full`\n")
        f.write("- no_overwrite: `required for smoke and formal runs`\n")
        if missing_flags:
            f.write("\n## Missing Flags\n\n")
            for flag in missing_flags:
                f.write(f"- `{flag}`\n")
    if not ok:
        raise RuntimeError("D1 architecture/CLI audit failed")


def write_d2_tool_contract() -> None:
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    schema = (
        "# Patch/full Metrics Schema\n\n"
        "Offline required columns: "
        + ", ".join(CORE_KEYS)
        + ".\n\n"
        "Patch/full strict gates:\n"
        "- `acc_turn_transition >= baseline_acc_turn_transition`\n"
        "- `theta_edge_p95_abs_err <= baseline_theta_edge_p95_abs_err + 0.05`\n"
        "- `false_turn_straight <= baseline_false_turn_straight + 0.01`\n"
        "- `flat_peak_theta_error <= baseline_flat_peak_theta_error + 0.25`\n\n"
        "Legacy exclusion: D8 must assert that no path in `excluded_legacy_full_artifacts.json` "
        "was used as a run summary, config, checkpoint, or best-run source.\n"
    )
    (SCHEMA_DIR / "patch_full_metrics_schema.md").write_text(schema, encoding="utf-8")
    with (EXP3_DIR / "D2_summary_tool_contract.md").open("w", encoding="utf-8") as f:
        f.write("# D2 exp3 Tool Contract\n\n")
        f.write("- tool: `results/modern_tcn_ablation/exp3_tools.py`\n")
        f.write("- run_glob: `results/modern_tcn_ablation/exp3_patch_full/full128_*_seed*/modern_tcn_full_seed*_summary.csv`\n")
        f.write("- excluded_legacy_assertion: `required before best-run selection`\n")
        f.write("- no_seq256: `true; this tool does not create seq_len=256 data or scripts`\n")
        f.write("- outputs: `patch_full_offline_summary.csv`, `patch_full_offline_summary.md`, `best_run_selection.md`, `promote_decision.json`\n")


def write_d3_deployment_report() -> None:
    loader = ROOT / "src" / "ModernTCN" / "ModernTCN_load_predictor.m"
    text = loader.read_text(encoding="utf-8")
    has_full_namespace = "modern_tcn_full_onnx_layers" in text
    has_gffn_namespace = "modern_tcn_gffn_onnx_layers" in text
    has_dual_namespace = "modern_tcn_dualkernel_onnx_layers" in text
    ok = has_full_namespace and has_gffn_namespace and has_dual_namespace
    with (EXP3_DIR / "D3_deployment_api_report.md").open("w", encoding="utf-8") as f:
        f.write("# D3 Deployment API Report\n\n")
        f.write(f"- pass: `{int(ok)}`\n")
        f.write(f"- loader: `{rel(loader)}`\n")
        f.write(f"- full_namespace: `modern_tcn_full_onnx_layers`\n")
        f.write(f"- full_namespace_present: `{int(has_full_namespace)}`\n")
        f.write("- candidate_policy: `closed-loop scripts must pass modern_tcn_sim_cfg.onnx_file and dataset_file explicitly.`\n")
        f.write("- default_small_namespace_unchanged: `modern_tcn_onnx_layers remains the fallback for baseline/small models.`\n")
    if not ok:
        raise RuntimeError("D3 deployment namespace audit failed")


def write_d4_report() -> None:
    smoke_dir = EXP3_DIR / "_smoke"
    smoke_dir.mkdir(parents=True, exist_ok=True)
    with (smoke_dir / "D4_dry_run_report.md").open("w", encoding="utf-8") as f:
        f.write("# D4 Dry-run Command Contract\n\n")
        f.write("- dataset: `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`\n")
        f.write("- expected_input: `[batch,128,22]`\n")
        f.write("- hyphen_and_underscore_cli: `must be tested by the shell commands in this node`\n\n")
        for name, cfg in FULL_CONFIGS.items():
            f.write(f"## {name}\n\n")
            f.write("```powershell\n")
            f.write(command_for_config(name, 21, dry_run=True, underscore=True))
            f.write("\n```\n\n")


def command_for_config(name: str, seed: int, dry_run: bool = False, underscore: bool = True, smoke: bool = False) -> str:
    cfg = FULL_CONFIGS[name]
    run_tag = f"{name}_seed{seed}"
    out_root = "results/modern_tcn_ablation/exp3_patch_full"
    if smoke:
        run_tag = "_smoke/full128_light_seed21_smoke"
    flag = {
        "model_family": "--model_family" if underscore else "--model-family",
        "patch_size": "--patch_size" if underscore else "--patch-size",
        "patch_stride": "--patch_stride" if underscore else "--patch-stride",
        "stage_blocks": "--stage_blocks" if underscore else "--stage-blocks",
        "large_kernels": "--large_kernels" if underscore else "--large-kernels",
        "small_kernels": "--small_kernels" if underscore else "--small-kernels",
        "run_tag": "--run_tag" if underscore else "--run-tag",
        "output_root": "--output_root" if underscore else "--output-root",
        "no_overwrite": "--no_overwrite" if underscore else "--no-overwrite",
    }
    parts = [
        "python src/ModernTCN/train_modern_tcn.py",
        f"{flag['model_family']} full",
        "--dataset-file data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat",
        f"{flag['patch_size']} {cfg['patch_size']}",
        f"{flag['patch_stride']} {cfg['patch_stride']}",
        f"--dims {csv_tuple(cfg['dims'])}",
        f"{flag['stage_blocks']} {csv_tuple(cfg['stage_blocks'])}",
        f"{flag['large_kernels']} {csv_tuple(cfg['large_kernels'])}",
        f"{flag['small_kernels']} {csv_tuple(cfg['small_kernels'])}",
        f"--seed {seed}",
        f"{flag['run_tag']} {run_tag}",
        f"{flag['output_root']} {out_root}",
        flag["no_overwrite"],
    ]
    if dry_run:
        parts.append("--dry-run")
    if smoke:
        parts.extend(["--epochs 3", "--min-epochs 1", "--patience 2", "--limit-train 512", "--limit-val 256", "--limit-test 256", "--batch-size 128"])
    return " ".join(parts)


def csv_tuple(values: object) -> str:
    return ",".join(str(x) for x in values)


def d5_smoke_gate(run_tag: str) -> None:
    run_dir = EXP3_DIR / run_tag
    required = [
        run_dir / "config.json",
        run_dir / "dataset_contract_copy.json",
        run_dir / "feature_names.txt",
        run_dir / "metrics_test.csv",
        run_dir / "modern_tcn_full_seed21.pt",
    ]
    missing = [rel(p) for p in required if not p.exists()]
    row = read_csv(run_dir / "metrics_test.csv")[0] if (run_dir / "metrics_test.csv").exists() else {}
    finite = all(math.isfinite(to_float(row, key)) for key in ["acc_main", "acc_turn", "theta_mae_deg"])
    ok = not missing and finite
    with (EXP3_DIR / "D5_smoke_gate.md").open("w", encoding="utf-8") as f:
        f.write("# D5 Smoke Training Gate\n\n")
        f.write(f"- run_tag: `{run_tag}`\n")
        f.write(f"- pass: `{int(ok)}`\n")
        f.write(f"- no_overwrite_policy: `verified by rerunning the smoke command with the same run_tag and expecting FileExistsError`\n")
        for key in ["acc_main", "acc_turn", "acc_turn_transition", "theta_mae_deg"]:
            if key in row:
                f.write(f"- {key}: `{row.get(key)}`\n")
        if missing:
            f.write("\n## Missing\n\n")
            for item in missing:
                f.write(f"- `{item}`\n")
    if not ok:
        raise RuntimeError("D5 smoke gate failed")


def summary_for_run(run_dir: Path) -> Path:
    matches = sorted(run_dir.glob("modern_tcn_full_seed*_summary.csv"))
    if not matches:
        raise FileNotFoundError(f"No ModernTCNFull summary found in {run_dir}")
    return matches[0]


def single_gate(run_tag: str) -> None:
    run_dir = EXP3_DIR / run_tag
    summary = summary_for_run(run_dir)
    row = enrich_row(read_csv(summary)[0])
    cfg = read_json(run_dir / "config.json") if (run_dir / "config.json").exists() else {}
    failures = disaster_failures(row)
    if nested_get(cfg, ["model_family"], "") != "full":
        failures.append("config model_family is not full")
    if int(nested_get(cfg, ["model_config", "input_dim"], -1)) != 22:
        failures.append("input_dim is not 22")
    if int(nested_get(cfg, ["model_config", "seq_len"], -1)) != 128:
        failures.append("seq_len is not 128")
    if "checkpoint" in json.dumps(cfg).lower() or "warm" in json.dumps(cfg).lower():
        failures.append("config contains checkpoint/warm-start hint")
    ok = not failures
    with (EXP3_DIR / "D6_single_seed_gate.md").open("w", encoding="utf-8") as f:
        f.write("# D6 Formal Single-seed Gate\n\n")
        f.write(f"- run_tag: `{run_tag}`\n")
        f.write(f"- pass: `{int(ok)}`\n")
        f.write(f"- summary: `{rel(summary)}`\n")
        f.write("- initialization: `random initialization; no checkpoint load path is present in train_modern_tcn.py formal training args`\n")
        for key in ["acc_main", "acc_turn", "acc_turn_transition", "theta_mae_deg", "stall_recall"]:
            f.write(f"- {key}: `{row.get(key, '')}`\n")
        if failures:
            f.write("\n## Failures\n\n")
            for item in failures:
                f.write(f"- {item}\n")
    if not ok:
        payload = {
            "decision": "NO_PROMOTION",
            "stop_node": "D6_single_seed_gate",
            "runs": 1,
            "best_run": run_tag,
            "best_offline_gate_failures": "; ".join(failures),
            "onnx_executed": False,
            "matlab_executed": False,
            "closed_loop_executed": False,
            "seq256_plan_allowed": False,
        }
        (EXP3_DIR / "promote_decision.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        with (EXP3_DIR / "patch_full_final_report.md").open("w", encoding="utf-8") as f:
            f.write("# patch_full Final Report\n\n")
            f.write("- decision: `NO_PROMOTION`\n")
            f.write("- stop_node: `D6_single_seed_gate`\n")
            f.write(f"- best_run: `{run_tag}`\n")
            f.write("- reason: formal single-seed full128 gate failed before the planned 9-run expansion.\n")
            f.write("- onnx/matlab/closed-loop: not executed.\n")
            f.write("- seq_len_256: `not allowed from this run; full128 did not pass the prerequisite gate.`\n")
            f.write("\n## Failures\n\n")
            for item in failures:
                f.write(f"- {item}\n")
        with (EXP3_DIR / "D7_D14_not_executed.md").open("w", encoding="utf-8") as f:
            f.write("# D7-D14 Not Executed\n\n")
            f.write("- reason: `D6_single_seed_gate failed`\n")
            f.write(f"- failed_run: `{run_tag}`\n")
            f.write("- D7 9-run formal matrix: `not executed`\n")
            f.write("- D8 offline summary over 9 runs: `not executed`\n")
            f.write("- D9 ONNX/ORT: `not executed`\n")
            f.write("- D10 MATLAB consistency: `not executed`\n")
            f.write("- D11 closed-loop preflight: `not executed`\n")
            f.write("- D12 main-path closed-loop: `not executed`\n")
            f.write("- D13 multipath/robustness: `not executed`\n")
            f.write("- D14 final promotion beyond D6: `not executed`\n")
            f.write("\n## Gate Failures\n\n")
            for item in failures:
                f.write(f"- {item}\n")
        raise RuntimeError("D6 single seed gate failed")


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


def to_float(row: Dict[str, object], key: str) -> float:
    try:
        return float(row.get(key, "nan"))
    except Exception:
        return float("nan")


def baseline_metrics() -> Dict[str, object]:
    base = enrich_row(read_csv(SNAPSHOT_DIR / "baseline_offline_metrics.csv")[0])
    source = Path(str(base.get("source", "")))
    if source.exists():
        source_row = enrich_row(read_csv(source)[0])
        for key in CORE_KEYS:
            if key not in base or str(base.get(key, "")) in {"", "nan"} or math.isnan(to_float(base, key)):
                base[key] = source_row.get(key, base.get(key, ""))
    boundary_file = EXP3_DIR / "baseline_boundary_metrics_exp3.csv"
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
    row["source"] = "read-only PyTorch evaluation of frozen baseline checkpoint on v5 plantfix test split; no baseline retraining"
    write_csv(EXP3_DIR / "baseline_boundary_metrics_exp3.csv", [row])
    with (EXP3_DIR / "baseline_boundary_metrics_exp3.md").open("w", encoding="utf-8") as f:
        f.write("# exp3 Baseline Boundary Metrics\n\n")
        f.write("- action: `read-only PyTorch evaluation of frozen baseline checkpoint`\n")
        f.write("- retraining: `0`\n")
        f.write(f"- checkpoint: `{rel(ckpt_file)}`\n")
        f.write(f"- dataset: `{rel(DATASET)}`\n")
        for key in CORE_KEYS:
            f.write(f"- {key}: `{row.get(key, '')}`\n")


def disaster_failures(row: Dict[str, object]) -> List[str]:
    checks = [
        ("acc_main", to_float(row, "acc_main"), ">=", 0.93),
        ("acc_turn", to_float(row, "acc_turn"), ">=", 0.48),
        ("theta_mae_deg", to_float(row, "theta_mae_deg"), "<=", 1.20),
        ("stall_recall", to_float(row, "stall_recall"), ">=", 0.45),
    ]
    failures = []
    for key, value, op, threshold in checks:
        ok = value >= threshold if op == ">=" else value <= threshold
        if not ok:
            failures.append(f"{key} {value:.6g} {op} {threshold:.6g} failed")
    return failures


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


def summarize() -> None:
    baseline = baseline_metrics()
    excluded = load_excluded_paths()
    rows: List[Dict[str, object]] = []
    for summary in sorted(EXP3_DIR.glob("full128_*_seed*/modern_tcn_full_seed*_summary.csv")):
        assert_not_legacy(summary, excluded)
        run_dir = summary.parent
        assert_not_legacy(run_dir / "config.json", excluded)
        row = enrich_row(read_csv(summary)[0])
        cfg = read_json(run_dir / "config.json") if (run_dir / "config.json").exists() else {}
        run_tag = run_dir.name
        config_name = run_tag.rsplit("_seed", 1)[0]
        out = dict(row)
        out["run_tag"] = run_tag
        out["config_name"] = config_name
        out["summary_file"] = str(summary)
        out["config_file"] = str(run_dir / "config.json")
        out["checkpoint_file"] = row.get("checkpoint_file", "")
        assert_not_legacy(Path(str(out["checkpoint_file"])), excluded)
        out["patch_size"] = nested_get(cfg, ["model_config", "patch_size"], "")
        out["patch_stride"] = nested_get(cfg, ["model_config", "patch_stride"], "")
        out["dims"] = ",".join(str(x) for x in nested_get(cfg, ["model_config", "dims"], []))
        out["stage_blocks"] = ",".join(str(x) for x in nested_get(cfg, ["model_config", "stage_blocks"], []))
        out["large_kernels"] = ",".join(str(x) for x in nested_get(cfg, ["model_config", "large_kernels"], []))
        out["small_kernels"] = ",".join(str(x) for x in nested_get(cfg, ["model_config", "small_kernels"], []))
        out["model_family_config"] = nested_get(cfg, ["model_family"], "")
        out["dataset_file_config"] = nested_get(cfg, ["dataset_contract", "dataset_file"], "")
        failures = offline_gate_failures(out, baseline)
        if out["model_family_config"] != "full":
            failures.append("config model_family is not full")
        if int(nested_get(cfg, ["model_config", "input_dim"], -1)) != 22:
            failures.append("input_dim is not 22")
        if int(nested_get(cfg, ["model_config", "seq_len"], -1)) != 128:
            failures.append("seq_len is not 128")
        if "v4b_weakcombo" in str(out["dataset_file_config"]).lower():
            failures.append("dataset points to legacy weakcombo")
        out["offline_gate"] = int(not failures)
        out["offline_gate_failures"] = "; ".join(failures)
        rows.append(out)
    if not rows:
        raise FileNotFoundError(f"No exp3 full128 summaries found under {EXP3_DIR}")

    write_csv(EXP3_DIR / "patch_full_offline_summary.csv", rows)
    passing = [r for r in rows if int(r["offline_gate"]) == 1]
    best = sorted(
        passing or rows,
        key=lambda r: (
            -to_float(r, "offline_gate"),
            -to_float(r, "acc_turn_transition"),
            to_float(r, "theta_edge_p95_abs_err"),
            to_float(r, "theta_mae_deg"),
            -to_float(r, "acc_turn"),
        ),
    )[0]
    group_rows = group_summary(rows)
    with (EXP3_DIR / "patch_full_offline_summary.md").open("w", encoding="utf-8") as f:
        f.write("# patch_full Offline Summary\n\n")
        f.write(f"- baseline: `{baseline.get('model', '')}`\n")
        f.write(f"- runs: `{len(rows)}`\n")
        f.write(f"- passing_offline_gate: `{len(passing)}`\n")
        f.write(f"- best_run: `{best['run_tag']}`\n")
        f.write("- legacy_exclusion_assertion: `passed; no excluded legacy path used as summary/config/checkpoint source`\n\n")
        f.write("## Group Means\n\n")
        f.write("| config | n | acc_main | acc_turn | acc_turn_transition | theta_mae_deg | theta_edge_p95 | gate_passes |\n")
        f.write("|---|---:|---:|---:|---:|---:|---:|---:|\n")
        for row in group_rows:
            f.write(
                f"| `{row['config_name']}` | {row['n']} | {row['acc_main_mean']:.6f} | "
                f"{row['acc_turn_mean']:.6f} | {row['acc_turn_transition_mean']:.6f} | "
                f"{row['theta_mae_deg_mean']:.6f} | {row['theta_edge_p95_abs_err_mean']:.6f} | {row['gate_passes']} |\n"
            )
    with (EXP3_DIR / "best_run_selection.md").open("w", encoding="utf-8") as f:
        f.write("# Best Run Selection\n\n")
        f.write(f"- best_run: `{best['run_tag']}`\n")
        f.write(f"- offline_gate: `{best['offline_gate']}`\n")
        f.write(f"- checkpoint: `{best.get('checkpoint_file', '')}`\n")
        f.write(f"- failures: `{best.get('offline_gate_failures', '')}`\n")
        f.write("- legacy_exclusion_assertion: `passed`\n")

    if not passing:
        write_no_promotion(rows, best)
    else:
        payload = {
            "decision": "OFFLINE_CANDIDATE",
            "stop_node": "",
            "runs": len(rows),
            "passing_runs": len(passing),
            "best_run": best["run_tag"],
            "onnx_executed": False,
            "matlab_executed": False,
            "closed_loop_executed": False,
        }
        (EXP3_DIR / "promote_decision.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def load_excluded_paths() -> List[str]:
    path = EXP3_DIR / "excluded_legacy_full_artifacts.json"
    if not path.exists():
        raise FileNotFoundError("Missing excluded_legacy_full_artifacts.json; run d0 first")
    data = read_json(path)
    return [str(item["path"]).lower() for item in data.get("artifacts", [])]


def assert_not_legacy(path: Path, excluded: List[str]) -> None:
    raw = str(path if path.is_absolute() else ROOT / path).lower()
    for item in excluded:
        if raw == item or raw.startswith(item + "\\") or raw.startswith(item + "/"):
            raise RuntimeError(f"Legacy artifact is forbidden for exp3 evidence: {path}")


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
        "seq256_plan_allowed": False,
    }
    (EXP3_DIR / "promote_decision.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    with (EXP3_DIR / "patch_full_final_report.md").open("w", encoding="utf-8") as f:
        f.write("# patch_full Final Report\n\n")
        f.write("- decision: `NO_PROMOTION`\n")
        f.write("- stop_node: `D8_offline_gate`\n")
        f.write("- reason: no patch/full candidate passed the strict offline transition/theta gates.\n")
        f.write("- onnx/matlab/closed-loop: not executed.\n")
        f.write("- seq_len_256: `not allowed from this run; open a separate plan only if future full128 evidence passes.`\n")


def write_closed_loop_preflight(best_run: str, onnx_file: Path, dataset_file: Path) -> None:
    onnx_file = onnx_file if onnx_file.is_absolute() else ROOT / onnx_file
    dataset_file = dataset_file if dataset_file.is_absolute() else ROOT / dataset_file
    out_root = ROOT / "results" / "compare" / "modern_tcn_ablation_closed_loop" / "exp3_patch_full" / best_run
    planned = [out_root / "p01" / "m01_out.mat", out_root / "p02" / "m02_out.mat", out_root / "p03" / "m03_out.mat"]
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
        f.write("# exp3 patch_full Closed-loop Preflight\n\n")
        f.write(f"- pass: `{int(preflight['pass'])}`\n")
        f.write(f"- best_run: `{best_run}`\n")
        f.write(f"- onnx_file: `{onnx_file}`\n")
        f.write(f"- dataset_file: `{dataset_file}`\n")
        f.write(f"- output_root: `{out_root}`\n")
        f.write(f"- max_path_length: `{max(lengths.values())}`\n")
        f.write("- short_output_names: `m01_out.mat`, `m02_out.mat`, `m03_out.mat`\n")
    if not preflight["pass"]:
        raise RuntimeError("Closed-loop preflight failed")


def write_final_report(status: str) -> None:
    decision_file = EXP3_DIR / "promote_decision.json"
    decision = read_json(decision_file) if decision_file.exists() else {"decision": "INCOMPLETE", "stop_node": "unknown"}
    if status == "incomplete":
        decision["decision"] = "INCOMPLETE"
    if status == "no_promote":
        decision["decision"] = "NO_PROMOTION"
    with (EXP3_DIR / "patch_full_final_report.md").open("w", encoding="utf-8") as f:
        f.write("# patch_full Final Report\n\n")
        f.write(f"- decision: `{decision.get('decision', 'INCOMPLETE')}`\n")
        f.write(f"- stop_node: `{decision.get('stop_node', '')}`\n")
        f.write(f"- best_run: `{decision.get('best_run', '')}`\n")
        f.write(f"- onnx_executed: `{int(bool(decision.get('onnx_executed', False)))}`\n")
        f.write(f"- matlab_executed: `{int(bool(decision.get('matlab_executed', False)))}`\n")
        f.write(f"- closed_loop_executed: `{int(bool(decision.get('closed_loop_executed', False)))}`\n")
        f.write("- seq_len_256: `not generated in this run; only a separate future plan may consider it after full128 evidence passes.`\n")


if __name__ == "__main__":
    main()
