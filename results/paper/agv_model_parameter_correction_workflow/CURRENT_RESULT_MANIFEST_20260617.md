# Current Result Manifest - 2026-06-17

This manifest records the artifact set that should be kept to support the
current paper-ready comparison under the repaired plant pipeline.

## Scope

- Plant revision: `agv_physics_v2_plantfix`
- Dataset contract: `passive17_plus_all5`
- Input dimension: `22`
- Main comparison: `ModernTCN > GRU > TCN` in the three-path closed-loop
  aggregate.
- Do not mix this artifact set with older `v2`, `v3`, `v4`, `weakcombo`,
  command-response, or E-distillation experiments.

## Dataset Artifacts

- `data/tcn/CURRENT_ModernTCN_DATASET.json`
- `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_contract.json`
- `data/tcn/ModernTCN_prepare_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_report.md`
- `data/tcn/ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_report.md`

## Source Files Needed For Reproduction

- `src/core/agv_plant_revision.m`
- `src/core/parameters.m`
- `src/core/state_eq.m`
- `src/core/state_eq_ref.m`
- `src/core/state_eq_ref_train_data.m`
- `src/core/extract_passive_features.m`
- `src/ModernTCN/train_modern_tcn.py`
- `src/ModernTCN/modern_tcn_model.py`
- `src/ModernTCN/modern_tcn_data.py`
- `src/ModernTCN/modern_tcn_metrics.py`
- `src/ModernTCN/export_modern_tcn_onnx.py`
- `src/gru/GRU_default_config.m`
- `src/TCN/TCN_gen_train_data.m`
- `src/TCN/TCN_prepare_dataset.m`
- `src/Compare/run_closed_loop_model_once.m`
- `src/Compare/compare_tcn_gru_modern_closed_loop_out.m`

## Model Artifacts

ModernTCN closed-loop champion:

- `results/paper/agv_model_parameter_correction_workflow/08_models/modern_tcn/modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101/`

ModernTCN stage-2 offline ablation:

- `results/paper/agv_model_parameter_correction_workflow/08_models/modern_tcn_stage2_targeted/`

GRU and TCN closed-loop baselines:

- `results/paper/agv_model_parameter_correction_workflow/08_models/models/GRU_model_full_gru_v5_plantfix_passive17_plus_all5_seed101.mat`
- `results/paper/agv_model_parameter_correction_workflow/08_models/models/TCN_model_full_tcn_v5_plantfix_passive17_plus_all5_seed101.mat`
- `results/paper/agv_model_parameter_correction_workflow/08_models/matlab_logs/full_gru_v5_plantfix_passive17_plus_all5_seed101/`
- `results/paper/agv_model_parameter_correction_workflow/08_models/matlab_logs/full_tcn_v5_plantfix_passive17_plus_all5_seed101/`

## Closed-Loop Artifacts

Main three-algorithm comparison:

- `results/paper/agv_model_parameter_correction_workflow/09_closed_loop/dual_modern_seed101_full/dual_modern_report.md`
- `results/paper/agv_model_parameter_correction_workflow/09_closed_loop/dual_modern_seed101_full/dual_modern_aggregate.csv`

ModernTCN multiseed and stage-2 checks:

- `results/paper/agv_model_parameter_correction_workflow/09_closed_loop/modern_multiseed_l020_tt25_full/`
- `results/paper/agv_model_parameter_correction_workflow/09_closed_loop/modern_stage2_targeted_full/`

## Plant And Controller Support

- `results/paper/agv_model_parameter_correction_workflow/03_open_loop/`
- `results/paper/agv_model_parameter_correction_workflow/04_lpv_database/`
- `results/paper/agv_model_parameter_correction_workflow/06_mpc_retuning/`
- `results/paper/agv_model_parameter_correction_workflow/11_figures_tables/`
- `results/paper/agv_model_parameter_correction_workflow/15_final_handoff/`

## Cleanup Rule

Artifacts outside this manifest can be archived first. They should not be
deleted until the main paper tables and closed-loop figures have been rebuilt
from the retained artifact set.
