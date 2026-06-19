# Source Cleanup Audit - 2026-06-17

This note records the source-code cleanup state after archiving obsolete
experiment outputs.

## Keep For Current Plantfix Result

These files are required by the current `agv_physics_v2_plantfix` /
`passive17_plus_all5` workflow and should be reviewed for commit rather than
reverted blindly.

- `src/core/agv_plant_revision.m`
- `src/core/extract_passive_features.m`
- `src/core/steering_icr_source.m`
- `src/core/parameters.m`
- `src/core/state_eq.m`
- `src/core/state_eq_ref.m`
- `src/core/state_eq_ref_train_data.m`
- `src/lpv/lin_agv_at_point.m`
- `src/mpc/Cost_Function.m`
- `src/core/UpdatePlantModel.m`
- `src/core/UpdatePlantModel_gru.m`
- `src/core/preloadfcn_v2.m`
- `src/core/preloadfcn_gru.m`
- `src/ModernTCN/modern_tcn_model.py`
- `src/ModernTCN/modern_tcn_data.py`
- `src/ModernTCN/modern_tcn_metrics.py`
- `src/ModernTCN/train_modern_tcn.py`
- `src/ModernTCN/export_modern_tcn_onnx.py`
- `src/ModernTCN/finetune_modern_tcn_turn.py`
- `src/ModernTCN/test_modern_tcn_full.py`
- `src/Compare/run_closed_loop_model_once.m`
- `src/Compare/compare_tcn_gru_modern_closed_loop_out.m`
- `src/TCN/TCN_gen_train_data.m`
- `src/TCN/TCN_prepare_dataset.m`
- `src/gru/GRU_prepare_dataset.m`

## Archived Experimental Source

These files were moved to `archive/obsolete_experiments_20260617/` because they
belong to command-response, weak-combo, or showcase branches outside the current
paper result.

- `src/ModernTCN/build_modern_tcn_cmdresp_lite_dataset.m`
- `src/ModernTCN/check_modern_tcn_cmdresp_feature_parity.m`
- `src/core/extract_command_response_features.m`
- `src/paths/gen_modern_tcn_showcase_paths.m`
- `src/paths/gen_modern_tcn_weak_combo_paths.m`

Move log:

- `archive/obsolete_experiments_20260617/archive_move_log_src_experimental.json`

## Do Not Auto-Revert

The remaining tracked source diffs include plant physics, feature extraction,
model contract changes from `input_dim=19` to `input_dim=22`, MPC tuning, and
closed-loop provenance support. Reverting them without a file-by-file review can
break the current three-algorithm result.

Recommended next step:

1. Run a lightweight smoke check for dataset contract and Python import.
2. Use `git add -p` or explicit path staging to create a focused
   `plantfix-current-result` commit.
3. Leave archived experiment branches ignored unless they are intentionally
   restored.
