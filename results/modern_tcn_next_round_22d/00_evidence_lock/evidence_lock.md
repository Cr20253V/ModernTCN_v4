# Phase 0 Evidence Lock

- generated_at: `2026-06-21 13:15:17`
- current_git_hash: `4abb19583b524424c7d7aec4061c101fcba6da55`
- baseline_snapshot_dir: `results/modern_tcn_ablation/_baseline_snapshot`
- baseline_dataset: `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- baseline_dataset_contract: `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_contract.json`
- baseline_checkpoint: `results/paper/agv_model_parameter_correction_workflow/08_models/modern_tcn/modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101/modern_tcn_seed101.pt`
- baseline_onnx: `results/paper/agv_model_parameter_correction_workflow/08_models/modern_tcn/modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101/modern_tcn_seed101.onnx`
- fixed_contract: `agv_physics_v2_plantfix / passive17_plus_all5 / input_dim=22 / seq_len=128`
- retained_champion: `turn_l020_tt25_tcm14_stw055_slrw060_seed101`

## Baseline Offline Metrics

- acc_main: `0.9669627984453082`
- acc_turn: `0.5788450860632982`
- acc_turn_transition: `0.4977645305514158`
- theta_mae_deg: `0.6793947815895081`
- flat_recall: `0.9695767195767195`
- stall_recall: `0.71875`
- slope_recall: `0.974909090909091`
- theta_abs_le_10_p95_abs_err_deg: `1.8274656534194946`

## Previous Ablation Decisions

- `exp1_grouped_ffn`: NO_PROMOTION; do not expand failed seeds.
- `exp2_dual_kernel`: NO_PROMOTION / STOP_NO_MULTISEED; do not reuse failed checkpoints.
- `exp3_patch_full`: NO_PROMOTION; full128/densepatch evidence remains offline-only.

## Isolation Statement

- This first round writes new evidence under `results/modern_tcn_next_round_22d/` plus the explicit seq256 dataset files.
- No baseline retraining, ONNX export, MATLAB import, Simulink, or closed-loop execution is permitted in this round.
- `.pt/.onnx/.mat/log/cache` artifacts are not intended for commit by default.

## Git Status At Lock

```text
M src/ModernTCN/modern_tcn_data.py
?? results/modern_tcn_ablation/ModernTCN_v4_next_round_22D_technical_plan_for_CODEX.md
?? results/modern_tcn_next_round_22d/
?? src/ModernTCN/run_next_round_22d_phase0_2.py
?? src/ModernTCN/test_modern_tcn_contracts.py
```
