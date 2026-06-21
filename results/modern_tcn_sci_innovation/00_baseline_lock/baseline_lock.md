# E0 Baseline Lock

- E0 decision: PASS
- can enter E1: True
- scope: Baseline review and freeze only. No training, no ONNX export, no Simulink closed-loop run.
- output root: results/modern_tcn_sci_innovation/00_baseline_lock/

## Git State

- current git commit hash: 4abb19583b524424c7d7aec4061c101fcba6da55
- historical baseline snapshot git hash: b0217f9149e8616a4a276cab48820373acaed963
- git status summary:

```text
 M src/ModernTCN/modern_tcn_data.py
?? data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_seq256_contract.json
?? data/tcn/ModernTCN_prepare_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_seq256_report.md
?? results/modern_tcn_ablation/ModernTCN_v4_next_round_22D_technical_plan_for_CODEX.md
?? results/modern_tcn_next_round_22d/
?? results/modern_tcn_sci_innovation/
?? src/ModernTCN/run_next_round_22d_phase0_2.py
?? src/ModernTCN/run_next_round_22d_phase3A.py
?? src/ModernTCN/test_modern_tcn_contracts.py
```

## Baseline Identity

- model: ModernTCN_small
- champion branch: turn_l020_tt25_tcm14_stw055_slrw060_seed101
- plant_revision: agv_physics_v2_plantfix
- feature_contract: passive17_plus_all5
- input_dim: 22
- seq_len: 128
- train/val/test windows: 16529/3695/3602
- baseline checkpoint exists: True
- baseline checkpoint path: E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.pt
- baseline ONNX exists: True
- baseline ONNX path: E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.onnx
- baseline dataset path: E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat
- baseline dataset contract path: E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_contract.json

## Feature Names

1. `gyro_z`
2. `I_lf`
3. `I_rr`
4. `omega_wheel_lf`
5. `omega_wheel_rr`
6. `delta_lf`
7. `delta_rr`
8. `v_hat`
9. `dv_hat_dt`
10. `ws_imbalance`
11. `I_sum`
12. `I_diff_signed`
13. `I_diff_abs`
14. `kappa_proxy`
15. `accel_per_current`
16. `dv_hat_dt_lp`
17. `accel_x_wheel`
18. `I_drive_signed`
19. `current_per_accel`
20. `drive_load_proxy`
21. `a_hp`
22. `yaw_consistency_error`

## Offline Baseline Metrics

- source: E:\Matlab\Simulink\S-Function_16\results\modern_tcn_ablation\_baseline_snapshot\baseline_offline_metrics.csv
- model: ModernTCN_turn_l020_tt25_seed101
- acc_main: 0.9669627984453082
- acc_turn: 0.5788450860632982
- acc_turn_transition: 0.4977645305514158
- theta_mae_deg: 0.6793947815895081
- theta_abs_le_10_p95_abs_err_deg: 1.8274656534194946
- flat_recall: 0.9695767195767195
- stall_recall: 0.71875
- slope_recall: 0.974909090909091

## Closed-Loop Baseline Metrics

- source: E:\Matlab\Simulink\S-Function_16\results\modern_tcn_ablation\_baseline_snapshot\baseline_closed_loop_metrics.csv
- aggregate controller: ModernTCN_turn_l020_tt25_seed101
- n_paths: 3
- ey_rmse_mean: 0.0293881212343404
- ey_peak_worst: 0.0852651182592324
- xy_rmse_mean: 0.599794482657117
- j_du_mean: 3.6807764852036
- rank_ey: 1

## Previous Ablation Result Directories

- `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_ablation\_baseline_snapshot`
- `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_ablation\exp1_grouped_ffn`
- `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_ablation\exp1_grouped_ffn_tune`
- `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_ablation\exp2_dual_kernel`
- `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_ablation\exp2_dual_kernel_tune`
- `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_ablation\exp3_patch_full`
- `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_ablation\exp3_patch_full_densepatch_continuation`
- `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_ablation\exp3_patch_full_rescue`

## Interpretation

- The offline-only best `ModernTCN_stage2_l020_tt30_lr_seed303` is not promoted because prior handoff evidence reports closed-loop degradation.
- The closed-loop champion remains `turn_l020_tt25_tcm14_stw055_slrw060_seed101`. Offline-only improvement must not replace it without closed-loop promotion evidence.
- E0 generated reports only under `results/modern_tcn_sci_innovation/00_baseline_lock/`. No training, ONNX export, or Simulink closed-loop execution was performed.

## E0 Decision

E0 PASS. Baseline is locked and E1 may proceed from this frozen baseline.
