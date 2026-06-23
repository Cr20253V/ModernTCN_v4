from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent.parent
SCI_ROOT = PROJECT_ROOT / "results" / "modern_tcn_sci_innovation"
OUT_ROOT = ROOT / "05_sandbox_closed_loop_if_needed"

BASELINE_OFFLINE = SCI_ROOT / "00_baseline_lock" / "baseline_offline_metrics.csv"
BASELINE_DATASET = PROJECT_ROOT / "data" / "tcn" / "ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: format_value(row.get(key, "")) for key in fieldnames})


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def format_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "NaN"
    text = str(value)
    return text if text else "NaN"


def must_exist(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"missing {label}: {path}")


def consistency_pass(path: Path) -> bool:
    if not path.exists():
        return False
    data = json.loads(path.read_text(encoding="utf-8"))
    return bool(data.get("pass", False))


def baseline_info() -> dict[str, object]:
    rows = read_csv(BASELINE_OFFLINE)
    if not rows:
        raise RuntimeError(f"baseline offline metrics has no rows: {BASELINE_OFFLINE}")
    row = rows[0]
    onnx_file = Path(row.get("onnx_file", ""))
    checkpoint_file = Path(row.get("checkpoint_file", ""))
    must_exist(onnx_file, "baseline ONNX")
    must_exist(checkpoint_file, "baseline checkpoint")
    must_exist(BASELINE_DATASET, "baseline dataset")
    return {
        "candidate_id": "baseline_lock",
        "run_tag": "baseline_lock",
        "seed": 101,
        "dataset_file": str(BASELINE_DATASET),
        "checkpoint_file": str(checkpoint_file),
        "onnx_file": str(onnx_file),
        "source_file": str(BASELINE_OFFLINE),
    }


def rerun_candidates() -> list[dict[str, object]]:
    e1_dir = SCI_ROOT / "01_loss_optimization" / "uncertainty_seed101_rerun_20260622"
    e1_export_dir = OUT_ROOT / "00_exported_onnx" / "uncertainty_seed101_rerun_20260622"
    e4_dir = SCI_ROOT / "04_mode_conditioned_theta" / "mode_theta_detach_flatreg001_seed21_rerun_20260622"
    e4_export_dir = e4_dir / "onnx_sandbox"
    return [
        {
            "selected_order": 1,
            "candidate_id": "uncertainty_seed101_rerun_20260622",
            "source_phase": "E1_loss_optimization",
            "source_historical_candidate": "uncertainty_seed101",
            "model_family": "ModernTCN_small",
            "class_label": "Class B rerun sandbox",
            "proxy_rank": 1,
            "seed": 101,
            "checkpoint_path": e1_dir / "modern_tcn_seed101.pt",
            "onnx_file": e1_export_dir / "uncertainty_seed101_rerun_20260622.onnx",
            "sample_file": e1_export_dir / "uncertainty_seed101_rerun_20260622_pytorch_reference.mat",
            "onnxruntime_json": e1_export_dir / "uncertainty_seed101_rerun_20260622_onnxruntime_consistency.json",
            "export_log": e1_export_dir / "export_onnx.log",
            "onnxruntime_log": e1_export_dir / "onnxruntime_consistency.log",
            "existing_sandbox_summary": OUT_ROOT / "02_uncertainty_seed101_rerun_20260622" / "execution_summary.md",
            "boundary_note": "new executable rerun; not a restored historical uncertainty_seed101 checkpoint",
        },
        {
            "selected_order": 2,
            "candidate_id": "mode_theta_detach_flatreg001_seed21_rerun_20260622",
            "source_phase": "E4_mode_conditioned_theta",
            "source_historical_candidate": "mode_theta_detach_flatreg001_seed21",
            "model_family": "ModernTCNModeTheta",
            "class_label": "Class B rerun sandbox",
            "proxy_rank": 2,
            "seed": 21,
            "checkpoint_path": e4_dir / "modern_tcn_mode_theta_seed21.pt",
            "onnx_file": e4_export_dir / "mode_theta_detach_flatreg001_seed21_rerun_20260622.onnx",
            "sample_file": e4_export_dir / "mode_theta_detach_flatreg001_seed21_rerun_20260622_pytorch_reference.mat",
            "onnxruntime_json": e4_export_dir / "mode_theta_detach_flatreg001_seed21_rerun_20260622_onnxruntime_consistency.json",
            "export_log": e4_export_dir / "export_onnx.log",
            "onnxruntime_log": e4_export_dir / "onnxruntime_consistency.log",
            "existing_sandbox_summary": e4_dir / "rerun_training_closed_loop_summary.md",
            "boundary_note": "new executable rerun; not a restored historical mode_theta_detach_flatreg001_seed21 checkpoint",
        },
    ]


def build_manifest_rows(candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for cand in candidates:
        checkpoint = Path(cand["checkpoint_path"])
        onnx_file = Path(cand["onnx_file"])
        sample_file = Path(cand["sample_file"])
        ort_json = Path(cand["onnxruntime_json"])
        notes: list[str] = []
        for path, label in [
            (checkpoint, "checkpoint"),
            (onnx_file, "ONNX"),
            (sample_file, "sample file"),
            (ort_json, "ONNXRuntime consistency JSON"),
        ]:
            if not path.exists():
                notes.append(f"missing {label}: {path}")
        ort_ok = consistency_pass(ort_json) if ort_json.exists() else False
        if not ort_ok:
            notes.append("ONNXRuntime consistency did not pass")
        selected = not notes
        rows.append({
            **cand,
            "checkpoint_path": str(checkpoint),
            "onnx_file": str(onnx_file),
            "sample_file": str(sample_file),
            "onnxruntime_json": str(ort_json),
            "export_log": str(cand["export_log"]),
            "onnxruntime_log": str(cand["onnxruntime_log"]),
            "export_status": "reused_existing" if onnx_file.exists() else "missing_onnx",
            "onnxruntime_status": "reused_existing" if ort_ok else "failed_or_missing",
            "consistency_pass": ort_ok,
            "eligible_for_sandbox": True,
            "selected_for_sandbox": selected,
            "notes": "; ".join(notes) if notes else cand["boundary_note"],
        })
    return rows


def write_reports(rows: list[dict[str, object]], baseline: dict[str, object]) -> None:
    all_ready = all(bool(row["selected_for_sandbox"]) for row in rows) and bool(rows)
    status = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "scope": "Window 2 rerun sandbox preflight",
        "selected_candidates": [row["candidate_id"] for row in rows],
        "all_selected_ready": all_ready,
        "baseline": baseline,
        "manifest_file": str(OUT_ROOT / "sandbox_candidate_manifest.csv"),
        "sandbox_output_root": str(OUT_ROOT),
        "rules": {
            "sandbox_only": True,
            "formal_compare_write": False,
            "no_historical_result_overwrite": True,
            "rerun_candidates_are_new_ids": True,
            "do_not_relabel_as_historical": True,
        },
    }
    write_json(OUT_ROOT / "sandbox_preflight_status.json", status)

    lines = [
        "# Window 2 Rerun Sandbox Preflight",
        "",
        "- scope: sandbox-only closed-loop screening",
        "- formal validation: not executed",
        "- historical Class B IDs remain unchanged; rerun IDs are registered as new executable sandbox candidates",
        f"- selected candidates: {', '.join(status['selected_candidates'])}",
        f"- all selected ready: {all_ready}",
        f"- baseline ONNX: `{baseline['onnx_file']}`",
        f"- dataset: `{baseline['dataset_file']}`",
        "",
        "## Candidate Readiness",
        "",
        "| order | candidate | source historical candidate | export | onnxruntime | ready | boundary |",
        "|---:|---|---|---|---|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['selected_order']} | `{row['candidate_id']}` | `{row['source_historical_candidate']}` | "
            f"{row['export_status']} | {row['onnxruntime_status']} | {int(bool(row['selected_for_sandbox']))} | {row['notes']} |"
        )
    write_text(OUT_ROOT / "sandbox_preflight_report.md", "\n".join(lines) + "\n")

    reg_lines = [
        "# Rerun Sandbox Registration Boundary",
        "",
        "These candidates are registered for sandbox closed-loop only. They do not restore or overwrite the historical Class B records selected in Window 1.",
        "",
        "| rerun candidate | source historical candidate | checkpoint | ONNX | existing evidence |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        reg_lines.append(
            f"| `{row['candidate_id']}` | `{row['source_historical_candidate']}` | "
            f"`{row['checkpoint_path']}` | `{row['onnx_file']}` | `{row['existing_sandbox_summary']}` |"
        )
    reg_lines.extend([
        "",
        "Boundary rules:",
        "",
        "- Do not relabel a rerun as the deleted historical checkpoint.",
        "- Do not promote a rerun to formal Class C from sandbox evidence alone.",
        "- Use formal validation before any replacement claim.",
    ])
    write_text(OUT_ROOT / "rerun_sandbox_registration_report.md", "\n".join(reg_lines) + "\n")

    blocked = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "status": "SUPERSEDED_BY_RERUN_CANDIDATES",
        "previous_blocker": "exact historical checkpoints missing",
        "new_boundary": "rerun candidates registered with new IDs for sandbox only",
        "selected_candidates": [row["candidate_id"] for row in rows],
        "formal_validation": False,
    }
    write_json(OUT_ROOT / "sandbox_blocked_status.json", blocked)
    write_text(
        OUT_ROOT / "sandbox_blocked_report.md",
        "\n".join([
            "# Window 2 Sandbox Blocked Report",
            "",
            "Status: `SUPERSEDED_BY_RERUN_CANDIDATES`",
            "",
            "The earlier blocker remains true for the exact historical checkpoints, but Window 2 is now continuing with new rerun candidate IDs.",
            "",
            "- `uncertainty_seed101_rerun_20260622` replaces no historical artifact; it is a new executable rerun.",
            "- `mode_theta_detach_flatreg001_seed21_rerun_20260622` replaces no historical artifact; it is a new executable rerun.",
            "- Sandbox evidence remains non-formal and cannot promote either candidate to strict Class C.",
            "",
        ])
    )


def main() -> int:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    baseline = baseline_info()
    rows = build_manifest_rows(rerun_candidates())
    write_csv(
        OUT_ROOT / "sandbox_candidate_manifest.csv",
        rows,
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
    write_reports(rows, baseline)
    print(json.dumps({
        "selected_candidates": [row["candidate_id"] for row in rows],
        "all_selected_ready": all(bool(row["selected_for_sandbox"]) for row in rows),
        "manifest_file": str(OUT_ROOT / "sandbox_candidate_manifest.csv"),
    }, indent=2, ensure_ascii=False))
    return 0 if all(bool(row["selected_for_sandbox"]) for row in rows) else 2


if __name__ == "__main__":
    raise SystemExit(main())
