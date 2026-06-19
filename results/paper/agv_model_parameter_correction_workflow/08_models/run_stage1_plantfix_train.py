"""Stage 1 plantfix model training runner.

This is a workflow-local wrapper. It reuses the existing ModernTCN Python
trainer and the existing MATLAB GRU/TCN trainers, while forcing the v5
plantfix passive17_plus_all5 dataset.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import h5py


ROOT = Path(__file__).resolve().parents[4]
NODE_DIR = ROOT / "results" / "paper" / "agv_model_parameter_correction_workflow" / "08_models"
TAG = "agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5"
DATASET_FILE = ROOT / "data" / "tcn" / f"ModernTCN_dataset_{TAG}.mat"
CONTRACT_FILE = ROOT / "data" / "tcn" / f"ModernTCN_dataset_{TAG}_contract.json"
MODERN_SRC = ROOT / "src" / "ModernTCN"
if str(MODERN_SRC) not in sys.path:
    sys.path.insert(0, str(MODERN_SRC))

from train_modern_tcn import train_one_seed  # noqa: E402


MODERN_FULL_SEEDS = [21, 73, 101]


@dataclass
class CommandResult:
    name: str
    command: List[str]
    returncode: int
    stdout_file: str
    stderr_file: str
    seconds: float


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Stage 1 plantfix model training")
    p.add_argument("--mode", choices=["preflight", "smoke", "full", "onnx", "summarize", "all"], default="preflight")
    p.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    p.add_argument("--matlab-command", default="matlab")
    p.add_argument("--matlab-use-gpu", action="store_true", default=True)
    p.add_argument("--matlab-no-gpu", action="store_false", dest="matlab_use_gpu")
    p.add_argument("--skip-existing", action="store_true", default=True)
    p.add_argument("--no-skip-existing", action="store_false", dest="skip_existing")
    p.add_argument("--modern-epochs", type=int, default=180)
    p.add_argument("--matlab-epochs", type=int, default=140)
    p.add_argument("--sample-count", type=int, default=16)
    p.add_argument("--skip-modern", action="store_true", default=False)
    p.add_argument("--skip-matlab", action="store_true", default=False)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    NODE_DIR.mkdir(parents=True, exist_ok=True)
    (NODE_DIR / "logs").mkdir(exist_ok=True)
    (NODE_DIR / "modern_tcn").mkdir(exist_ok=True)
    preflight = run_preflight()
    command_results: List[CommandResult] = []

    if args.mode == "preflight":
        metrics = write_metrics(preflight, command_results)
        write_report(metrics)
        return

    if args.mode in {"smoke", "all"}:
        if not args.skip_modern:
            run_modern_tcn_seeds([21], args, phase="smoke")
        if not args.skip_matlab:
            command_results.extend(run_matlab_train(args, mode="smoke"))

    if args.mode in {"full", "all"}:
        if not args.skip_modern:
            run_modern_tcn_seeds(MODERN_FULL_SEEDS, args, phase="full")
        if not args.skip_matlab:
            command_results.extend(run_matlab_train(args, mode="full"))

    if args.mode in {"onnx", "all"}:
        command_results.extend(run_modern_tcn_onnx_checks(args))

    metrics = write_metrics(preflight, command_results)
    write_report(metrics)
    print(f"[stage1 train] report: {NODE_DIR / 'stage1_model_retraining_report.md'}")


def run_preflight() -> Dict[str, Any]:
    if not DATASET_FILE.exists():
        raise FileNotFoundError(DATASET_FILE)
    if not CONTRACT_FILE.exists():
        raise FileNotFoundError(CONTRACT_FILE)
    contract = json.loads(CONTRACT_FILE.read_text(encoding="utf-8"))
    with h5py.File(DATASET_FILE, "r") as f:
        d = f["dataset"]
        train_shape = list(d["X_train"].shape)
        val_shape = list(d["X_val"].shape)
        test_shape = list(d["X_test"].shape)
    observed = {
        "input_dim": int(train_shape[0]),
        "train_windows": int(train_shape[2]),
        "val_windows": int(val_shape[2]),
        "test_windows": int(test_shape[2]),
    }
    checks = {
        "dataset_exists": DATASET_FILE.exists(),
        "contract_exists": CONTRACT_FILE.exists(),
        "input_dim_22": observed["input_dim"] == 22,
        "has_windows": observed["train_windows"] > 0 and observed["val_windows"] > 0 and observed["test_windows"] > 0,
        "feature_contract": contract.get("feature_contract") == "passive17_plus_all5",
        "plant_revision": contract.get("plant_revision", {}).get("id") == "agv_physics_v2_plantfix",
        "output_file_matches": Path(contract.get("output_file", "")).resolve() == DATASET_FILE.resolve(),
    }
    preflight = {
        "dataset_file": str(DATASET_FILE),
        "contract_file": str(CONTRACT_FILE),
        "observed": observed,
        "contract": contract,
        "checks": checks,
        "pass": all(checks.values()),
    }
    (NODE_DIR / "stage1_train_preflight.json").write_text(json.dumps(preflight, indent=2), encoding="utf-8")
    if not preflight["pass"]:
        raise RuntimeError(f"Stage 1 train preflight failed: {checks}")
    return preflight


def run_modern_tcn_seeds(seeds: List[int], args: argparse.Namespace, phase: str) -> None:
    for seed in seeds:
        out_dir = NODE_DIR / "modern_tcn" / f"modern_tcn_v5_plantfix_passive17_plus_all5_seed{seed}"
        checkpoint = out_dir / f"modern_tcn_seed{seed}.pt"
        summary = out_dir / f"modern_tcn_seed{seed}_summary.csv"
        marker = out_dir / f"modern_tcn_seed{seed}_stage1_marker.json"
        if args.skip_existing and checkpoint.exists() and summary.exists():
            marker_data = read_json(marker)
            marker_ok = (
                marker_data is not None
                and marker_data.get("phase") == phase
                and int(marker_data.get("epochs", 0)) >= int(args.modern_epochs)
                and marker_data.get("dataset_file") == str(DATASET_FILE)
            )
            legacy_smoke_ok = phase == "smoke" and marker_data is None
            if marker_ok or legacy_smoke_ok:
                print(f"[ModernTCN] reuse seed={seed}: {checkpoint}")
                continue
        train_args = argparse.Namespace(
            seed=seed,
            model_family="small",
            dataset_file=str(DATASET_FILE),
            run_tag=str(out_dir),
            epochs=args.modern_epochs,
            batch_size=256,
            lr=1e-3,
            weight_decay=1e-4,
            patience=35,
            min_epochs=50,
            channels=64,
            blocks=5,
            kernel_size=31,
            temporal_padding="same",
            dropout=0.15,
            turn_head_source="full",
            lambda_turn=0.08,
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
            turn_transition_weight=1.4,
            turn_class_multipliers=[1.08, 1.00, 1.08],
            select_turn_weight=0.30,
            select_turn_transition_weight=1.20,
            select_turn_transition_target=0.82,
            select_turn_left_weight=0.0,
            select_turn_left_target=0.88,
            select_turn_lr_weight=0.20,
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
        print(f"[ModernTCN] phase={phase} seed={seed}")
        train_one_seed(train_args)
        marker.write_text(
            json.dumps(
                {
                    "phase": phase,
                    "seed": seed,
                    "epochs": int(args.modern_epochs),
                    "dataset_file": str(DATASET_FILE),
                    "checkpoint_file": str(checkpoint),
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                },
                indent=2,
            ),
            encoding="utf-8",
        )


def run_matlab_train(args: argparse.Namespace, mode: str) -> List[CommandResult]:
    matlab_bool = "true" if args.matlab_use_gpu else "false"
    skip_bool = "true" if args.skip_existing else "false"
    cmd_text = (
        "init_project; "
        "addpath(fullfile(project_root(),'results','paper','agv_model_parameter_correction_workflow','08_models')); "
        f"cfg=struct('mode','{mode}','dataset_file','{matlab_path(DATASET_FILE)}',"
        f"'node_dir','{matlab_path(NODE_DIR)}','use_gpu',{matlab_bool},"
        f"'skip_existing',{skip_bool},'max_epochs',{args.matlab_epochs}); "
        "summary=run_stage1_gru_tcn_train(cfg);"
    )
    return [run_command(f"matlab_{mode}_gru_tcn", [args.matlab_command, "-batch", cmd_text])]


def run_modern_tcn_onnx_checks(args: argparse.Namespace) -> List[CommandResult]:
    checkpoint = NODE_DIR / "modern_tcn" / "modern_tcn_v5_plantfix_passive17_plus_all5_seed21" / "modern_tcn_seed21.pt"
    if not checkpoint.exists():
        raise FileNotFoundError(checkpoint)
    export_cmd = [
        sys.executable,
        str(MODERN_SRC / "export_modern_tcn_onnx.py"),
        "--checkpoint",
        str(checkpoint),
        "--sample-count",
        str(args.sample_count),
    ]
    export_result = run_command("modern_tcn_export_onnx", export_cmd)
    onnx_file = checkpoint.with_suffix(".onnx")
    sample_file = checkpoint.with_name(checkpoint.stem + "_pytorch_reference.mat")
    ort_result = run_command(
        "modern_tcn_onnxruntime_consistency",
        [
            sys.executable,
            str(MODERN_SRC / "check_onnxruntime_consistency.py"),
            "--onnx-file",
            str(onnx_file),
            "--sample-file",
            str(sample_file),
        ],
    )
    matlab_cmd_text = (
        "init_project; addpath(fullfile(project_root(),'src','ModernTCN')); "
        f"result=ModernTCN_check_matlab_onnx('{matlab_path(onnx_file)}','{matlab_path(sample_file)}'); "
        "if ~result.pass, error('stage1:MatlabOnnxConsistencyFailed','MATLAB ONNX consistency failed'); end"
    )
    matlab_result = run_command(
        "modern_tcn_matlab_onnx_consistency",
        [args.matlab_command, "-batch", matlab_cmd_text],
    )
    return [export_result, ort_result, matlab_result]


def run_command(name: str, command: List[str]) -> CommandResult:
    logs_dir = NODE_DIR / "logs"
    logs_dir.mkdir(exist_ok=True)
    stdout_file = logs_dir / f"{name}.stdout.log"
    stderr_file = logs_dir / f"{name}.stderr.log"
    print(f"[stage1 command] {name}")
    t0 = time.time()
    with stdout_file.open("w", encoding="utf-8", errors="replace") as out, stderr_file.open(
        "w", encoding="utf-8", errors="replace"
    ) as err:
        proc = subprocess.run(command, cwd=ROOT, stdout=out, stderr=err, text=True)
    result = CommandResult(name, command, proc.returncode, str(stdout_file), str(stderr_file), time.time() - t0)
    if proc.returncode != 0:
        raise RuntimeError(f"{name} failed with exit code {proc.returncode}; see {stdout_file} and {stderr_file}")
    return result


def read_json(path: Path) -> Dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_metrics(preflight: Dict[str, Any], command_results: List[CommandResult]) -> Dict[str, Any]:
    metrics = {
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "dataset_file": str(DATASET_FILE),
        "contract_file": str(CONTRACT_FILE),
        "preflight": preflight,
        "modern_tcn": read_modern_rows(),
        "matlab": read_matlab_rows(),
        "commands": [r.__dict__ for r in command_results],
    }
    (NODE_DIR / "stage1_model_retraining_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def read_modern_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for seed in MODERN_FULL_SEEDS:
        out_dir = NODE_DIR / "modern_tcn" / f"modern_tcn_v5_plantfix_passive17_plus_all5_seed{seed}"
        summary_file = out_dir / f"modern_tcn_seed{seed}_summary.csv"
        checkpoint = out_dir / f"modern_tcn_seed{seed}.pt"
        row: Dict[str, Any] = {"model": "ModernTCN", "seed": seed, "summary_file": str(summary_file)}
        if summary_file.exists() and checkpoint.exists():
            row["status"] = "ok"
            row["checkpoint_file"] = str(checkpoint)
        else:
            row["status"] = "missing"
        rows.append(row)
    return rows


def read_matlab_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for name in ["stage1_smoke_gru_tcn_summary.csv", "stage1_full_gru_tcn_summary.csv"]:
        path = NODE_DIR / name
        if not path.exists():
            continue
        with path.open("r", newline="", encoding="utf-8-sig") as f:
            rows.extend(dict(r) for r in csv.DictReader(f))
    return rows


def write_report(metrics: Dict[str, Any]) -> None:
    report = NODE_DIR / "stage1_model_retraining_report.md"
    with report.open("w", encoding="utf-8") as f:
        f.write("# Stage 1 Plantfix Model Retraining Report\n\n")
        f.write(f"- dataset: `{DATASET_FILE}`\n")
        f.write(f"- contract: `{CONTRACT_FILE}`\n")
        f.write(f"- plant_revision: `{metrics['preflight']['contract'].get('plant_revision', {}).get('id', '')}`\n")
        f.write(f"- preflight_pass: `{metrics['preflight']['pass']}`\n\n")
        f.write("## ModernTCN\n\n")
        f.write("| seed | status | checkpoint |\n|---:|---|---|\n")
        for row in metrics["modern_tcn"]:
            f.write(f"| {row['seed']} | {row['status']} | `{row.get('checkpoint_file', '')}` |\n")
        f.write("\n## MATLAB GRU/TCN\n\n")
        f.write(f"- rows: `{len(metrics['matlab'])}`\n")


def matlab_path(path: Path) -> str:
    return str(path).replace("'", "''")


if __name__ == "__main__":
    main()
