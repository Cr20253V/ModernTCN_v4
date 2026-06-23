from __future__ import annotations

import argparse
import csv
import json
import math
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent.parent
OUT_ROOT = ROOT / "05_sandbox_closed_loop_if_needed"
EXPORT_ROOT = OUT_ROOT / "00_exported_onnx"

CLASS_FILE = ROOT / "04_candidate_decision" / "candidate_classes.csv"
REGISTRY_FILE = ROOT / "03_rerank_existing_experiments" / "candidate_registry.csv"
BASELINE_OFFLINE = PROJECT_ROOT / "results" / "modern_tcn_sci_innovation" / "00_baseline_lock" / "baseline_offline_metrics.csv"
BASELINE_DATASET = PROJECT_ROOT / "data" / "tcn" / "ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat"

EXPORT_SCRIPT = PROJECT_ROOT / "src" / "ModernTCN" / "export_modern_tcn_onnx.py"
ORT_SCRIPT = PROJECT_ROOT / "src" / "ModernTCN" / "check_onnxruntime_consistency.py"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: format_value(row.get(k, "")) for k in fieldnames})


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def format_value(value: object) -> str:
    if value is None:
        return "NaN"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"
        return f"{value:.15g}"
    return str(value)


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def parse_rank(value: object) -> int:
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return 10**9
    return int(float(text))


def resolve_path(path_text: str) -> Path:
    path = Path(str(path_text))
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def load_config(checkpoint: Path) -> dict[str, object]:
    cfg_file = checkpoint.parent / "config.json"
    if cfg_file.exists():
        return json.loads(cfg_file.read_text(encoding="utf-8"))
    return {}


def parse_seed(candidate_id: str, cfg: dict[str, object]) -> int:
    cli = cfg.get("cli_args", {})
    if isinstance(cli, dict) and cli.get("seed") is not None:
        return int(cli["seed"])
    if cfg.get("seed") is not None:
        return int(cfg["seed"])
    match = re.search(r"seed(\d+)", candidate_id)
    return int(match.group(1)) if match else 21


def baseline_info() -> dict[str, object]:
    rows = read_csv(BASELINE_OFFLINE)
    if not rows:
        raise RuntimeError(f"baseline offline metrics has no rows: {BASELINE_OFFLINE}")
    row = rows[0]
    return {
        "candidate_id": "baseline_lock",
        "run_tag": "baseline_lock",
        "seed": 101,
        "dataset_file": str(BASELINE_DATASET),
        "checkpoint_file": row.get("checkpoint_file", ""),
        "onnx_file": row.get("onnx_file", ""),
        "source_file": str(BASELINE_OFFLINE),
    }


def run_command(args: list[str], log_file: Path) -> tuple[bool, str]:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        args,
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    log_file.write_text(proc.stdout, encoding="utf-8")
    return proc.returncode == 0, proc.stdout


def consistency_pass(json_file: Path) -> bool:
    if not json_file.exists():
        return False
    try:
        data = json.loads(json_file.read_text(encoding="utf-8"))
        return bool(data.get("pass", False))
    except Exception:
        return False


def prepare_candidate(row: dict[str, str], registry: dict[str, dict[str, str]], order: int) -> dict[str, object]:
    cid = row["candidate_id"]
    reg = registry[cid]
    checkpoint = resolve_path(reg["checkpoint_path_if_available"])
    cfg = load_config(checkpoint)
    seed = parse_seed(cid, cfg)
    cand_dir = EXPORT_ROOT / cid
    onnx_file = cand_dir / f"{cid}.onnx"
    sample_file = cand_dir / f"{cid}_pytorch_reference.mat"
    ort_json = onnx_file.with_name(onnx_file.stem + "_onnxruntime_consistency.json")
    export_log = cand_dir / "export_onnx.log"
    ort_log = cand_dir / "onnxruntime_consistency.log"
    cand_dir.mkdir(parents=True, exist_ok=True)

    notes: list[str] = []
    export_status = "not_run"
    ort_status = "not_run"
    if not checkpoint.exists():
        export_status = "missing_checkpoint"
        notes.append(f"missing checkpoint: {checkpoint}")
    else:
        need_export = not (onnx_file.exists() and sample_file.exists() and onnx_file.with_name(onnx_file.stem + "_onnx_export.json").exists())
        if need_export:
            ok, _ = run_command(
                [
                    sys.executable,
                    str(EXPORT_SCRIPT),
                    "--checkpoint",
                    str(checkpoint),
                    "--onnx-file",
                    str(onnx_file),
                    "--sample-file",
                    str(sample_file),
                ],
                export_log,
            )
            export_status = "ok" if ok else "failed"
        else:
            export_status = "reused_existing"

        if export_status in {"ok", "reused_existing"}:
            need_ort = not consistency_pass(ort_json)
            if need_ort:
                ok, _ = run_command(
                    [
                        sys.executable,
                        str(ORT_SCRIPT),
                        "--onnx-file",
                        str(onnx_file),
                        "--sample-file",
                        str(sample_file),
                    ],
                    ort_log,
                )
                ort_status = "ok" if ok else "failed"
            else:
                ort_status = "reused_existing"
        else:
            ort_status = "skipped_export_failed"

    pass_ort = consistency_pass(ort_json)
    selected = export_status in {"ok", "reused_existing"} and pass_ort
    if not selected:
        notes.append("candidate not runnable until ONNX export and ONNXRuntime consistency pass")

    return {
        "selected_order": order,
        "candidate_id": cid,
        "source_phase": row.get("source_phase", ""),
        "model_family": reg.get("model_family", ""),
        "class_label": row.get("class_label", ""),
        "proxy_rank": row.get("proxy_rank", ""),
        "seed": seed,
        "checkpoint_path": str(checkpoint),
        "onnx_file": str(onnx_file),
        "sample_file": str(sample_file),
        "onnxruntime_json": str(ort_json),
        "export_log": str(export_log),
        "onnxruntime_log": str(ort_log),
        "export_status": export_status,
        "onnxruntime_status": ort_status,
        "consistency_pass": pass_ort,
        "eligible_for_sandbox": truthy(row.get("eligible_for_sandbox", "")),
        "selected_for_sandbox": selected,
        "notes": "; ".join(notes) if notes else "ready_for_sandbox_closed_loop",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare Window 2 Class-B sandbox candidates.")
    parser.add_argument("--max-candidates", type=int, default=2)
    args = parser.parse_args()

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    class_rows = read_csv(CLASS_FILE)
    registry_rows = read_csv(REGISTRY_FILE)
    registry = {r["candidate_id"]: r for r in registry_rows}

    selected_rows = [
        r
        for r in class_rows
        if r.get("class_label") == "Class B"
        and truthy(r.get("eligible_for_sandbox", ""))
        and not truthy(r.get("advisory_only", ""))
        and not truthy(r.get("is_reference_baseline", ""))
    ]
    selected_rows.sort(key=lambda r: (parse_rank(r.get("proxy_rank", "")), r.get("candidate_id", "")))
    selected_rows = selected_rows[: max(0, int(args.max_candidates))]

    baseline = baseline_info()
    candidate_rows = [prepare_candidate(row, registry, idx + 1) for idx, row in enumerate(selected_rows)]
    all_ready = all(bool(r["selected_for_sandbox"]) for r in candidate_rows) and bool(candidate_rows)

    manifest_file = OUT_ROOT / "sandbox_candidate_manifest.csv"
    write_csv(
        manifest_file,
        candidate_rows,
        [
            "selected_order",
            "candidate_id",
            "source_phase",
            "model_family",
            "class_label",
            "proxy_rank",
            "seed",
            "checkpoint_path",
            "onnx_file",
            "sample_file",
            "onnxruntime_json",
            "export_log",
            "onnxruntime_log",
            "export_status",
            "onnxruntime_status",
            "consistency_pass",
            "eligible_for_sandbox",
            "selected_for_sandbox",
            "notes",
        ],
    )
    status = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "scope": "Window 2 sandbox preflight",
        "max_candidates": int(args.max_candidates),
        "class_b_candidates_seen": len([r for r in class_rows if r.get("class_label") == "Class B"]),
        "selected_candidates": [r["candidate_id"] for r in candidate_rows],
        "all_selected_ready": all_ready,
        "baseline": baseline,
        "manifest_file": str(manifest_file),
        "sandbox_output_root": str(OUT_ROOT),
        "rules": {
            "sandbox_only": True,
            "formal_compare_write": False,
            "no_training": True,
            "no_historical_result_overwrite": True,
            "max_class_b_candidates": 2,
        },
    }
    write_json(OUT_ROOT / "sandbox_preflight_status.json", status)

    lines = [
        "# Window 2 Sandbox Preflight",
        "",
        f"- selected candidates: {', '.join(status['selected_candidates']) if status['selected_candidates'] else 'none'}",
        f"- all selected ready: {all_ready}",
        f"- baseline ONNX: `{baseline['onnx_file']}`",
        f"- dataset: `{baseline['dataset_file']}`",
        "- scope: sandbox-only closed-loop screening; not formal validation",
        "- no historical SCI result directory is written by this preflight",
        "",
        "## Candidate Readiness",
        "",
        "| order | candidate | export | onnxruntime | ready | notes |",
        "|---:|---|---|---|---:|---|",
    ]
    for r in candidate_rows:
        lines.append(
            f"| {r['selected_order']} | `{r['candidate_id']}` | {r['export_status']} | "
            f"{r['onnxruntime_status']} | {int(bool(r['selected_for_sandbox']))} | {r['notes']} |"
        )
    write_text(OUT_ROOT / "sandbox_preflight_report.md", "\n".join(lines) + "\n")
    print(json.dumps(status, indent=2, ensure_ascii=False))
    return 0 if all_ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
