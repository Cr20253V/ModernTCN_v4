from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[4]
BASE_SCRIPT = ROOT / "results" / "modern_tcn_metric_rebuild" / "17_fair_10seed_selection_and_final_test" / "tools" / "run_fair10_node.py"
if not BASE_SCRIPT.exists():
    raise FileNotFoundError(f"Missing base runner: {BASE_SCRIPT}")

_spec = importlib.util.spec_from_file_location("fair10_node_17_base", BASE_SCRIPT)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"Unable to load base runner: {BASE_SCRIPT}")
_base = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _base
_spec.loader.exec_module(_base)

NODE_ROOT = ROOT / "results" / "modern_tcn_metric_rebuild" / "18_fair_10seed_selection_and_final_test_recut_recipe"
MODERN_RECIPE = ROOT / "results" / "modern_tcn_metric_rebuild" / "16_recipe_vs_deployment_comparison" / "07_modern_base_seed42_training" / "modern_base_seed42" / "config.json"
UNCERTAINTY_RECIPE = ROOT / "results" / "modern_tcn_sci_innovation" / "01_loss_optimization" / "uncertainty_seed101_rerun_20260622" / "config.json"


def _patch_base_module() -> None:
    _base.NODE_ROOT = NODE_ROOT
    _base.RUN_CLOSED_LOOP_M = NODE_ROOT / "run_fair10_closed_loop.m"
    _base.TRAIN_OUTPUT_ROOTS = {
        "modern_fixed": NODE_ROOT / "01_train_modern_tcn_small_10seed",
        "uncertainty_weighted": NODE_ROOT / "02_train_uncertainty_weighted_10seed",
    }

    modern_fixed = dict(_base.TRAIN_REGISTRY["modern_fixed"])
    modern_fixed["output_root"] = _base.TRAIN_OUTPUT_ROOTS["modern_fixed"]
    modern_fixed["recipe_source_config"] = UNCERTAINTY_RECIPE

    uncertainty_weighted = dict(_base.TRAIN_REGISTRY["uncertainty_weighted"])
    uncertainty_weighted["output_root"] = _base.TRAIN_OUTPUT_ROOTS["uncertainty_weighted"]
    uncertainty_weighted["recipe_source_config"] = UNCERTAINTY_RECIPE

    _base.TRAIN_REGISTRY = {
        "modern_fixed": modern_fixed,
        "uncertainty_weighted": uncertainty_weighted,
    }


_patch_base_module()

_original_build_train_command = _base.build_train_command


def _build_train_command_cuda(algorithm_key: str, seed: int) -> list[str]:
    cmd = _original_build_train_command(algorithm_key, seed)
    patched: list[str] = []
    i = 0
    while i < len(cmd):
        if cmd[i] == "--device" and i + 1 < len(cmd):
            patched.extend(["--device", "cuda"])
            i += 2
            continue
        patched.append(cmd[i])
        i += 1
    return patched


_base.build_train_command = _build_train_command_cuda


_original_write_manual_scripts = _base.write_manual_scripts


def _write_manual_scripts_safe() -> None:
    _original_write_manual_scripts()
    protocol_dir = NODE_ROOT / "00_protocol_lock"
    for name in ["manual_train_modern_fixed.ps1", "manual_train_uncertainty.ps1"]:
        path = protocol_dir / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = text.replace("--baseline-checkpoint  --", '--baseline-checkpoint "" --')
        text = text.replace("--init-checkpoint  --", '--init-checkpoint "" --')
        path.write_text(text, encoding="utf-8")


_base.write_manual_scripts = _write_manual_scripts_safe


if __name__ == "__main__":
    raise SystemExit(_base.main())
