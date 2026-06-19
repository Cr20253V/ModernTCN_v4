# Stage 2 ModernTCN Targeted Search Report

- generated: `2026-06-17 05:12:54`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- preflight_pass: `1`
- fixed: architecture, input_dim=22, passive17_plus_all5, plantfix raw/dataset

## Candidate Space

| case | lambda_turn | transition_weight | multipliers | note |
|---|---:|---:|---|---|
| l018_tt22_bal | 0.18 | 2.2 | [1.35, 0.85, 1.35] | slightly softer than champion |
| l020_tt25_bal | 0.2 | 2.5 | [1.4, 0.8, 1.4] | current champion neighborhood |
| l022_tt28_turn | 0.22 | 2.8 | [1.45, 0.75, 1.45] | stronger turn transition focus |
| l020_tt30_lr | 0.2 | 3 | [1.5, 0.75, 1.5] | strongest L/R balance focus |

## Offline Ranking

| stage2_rank | case | seed | stage2_gate | stage2_offline_score | acc_main | acc_turn_transition | turn_lr_ratio | theta_mae_deg | theta_abs_le_10_p95_abs_err_deg | flat_recall | slope_recall |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | l020_tt30_lr | 303 | 1 | 0.0417574 | 0.966685 | 0.566319 | 0.965075 | 0.708034 | 1.91314 | 0.965608 | 0.978545 |
| 2 | l020_tt30_lr | 101 | 1 | 0.0708406 | 0.956691 | 0.542474 | 0.918391 | 0.624571 | 1.6794 | 0.931217 | 0.972364 |
| 3 | l018_tt22_bal | 303 | 1 | 0.0776353 | 0.956968 | 0.539493 | 0.934217 | 0.676194 | 1.89606 | 0.929894 | 0.975273 |
| 4 | l022_tt28_turn | 303 | 1 | 0.0896063 | 0.961966 | 0.511177 | 0.884574 | 0.626781 | 1.75393 | 0.94709 | 0.977455 |
| 5 | l020_tt25_bal | 101 | 1 | 0.090459 | 0.966963 | 0.497765 | 0.905244 | 0.679395 | 1.82747 | 0.969577 | 0.974909 |
| 6 | l018_tt22_bal | 101 | 1 | 0.122859 | 0.965575 | 0.493294 | 0.987522 | 0.708195 | 1.88805 | 0.956349 | 0.976727 |
| 7 | l020_tt25_bal | 303 | 0 | 0.147866 | 0.955858 | 0.52608 | 0.832548 | 0.70472 | 2.11365 | 0.951058 | 0.968 |
| 8 | l022_tt28_turn | 101 | 0 | 0.17626 | 0.955303 | 0.512668 | 0.992554 | 0.760907 | 2.05612 | 0.928571 | 0.972727 |

## Selected For Closed Loop

| stage2_rank | case | seed | stage2_offline_score | checkpoint_file | onnx_file |
|---|---|---|---|---|---|
| 1 | l020_tt30_lr | 303 | 0.0417574 | E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn_stage2_targeted\modern_tcn_v5_plantfix_stage2_l020_tt30_lr_seed303\modern_tcn_seed303.pt | E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn_stage2_targeted\modern_tcn_v5_plantfix_stage2_l020_tt30_lr_seed303\modern_tcn_seed303.onnx |
| 2 | l020_tt30_lr | 101 | 0.0708406 | E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn_stage2_targeted\modern_tcn_v5_plantfix_stage2_l020_tt30_lr_seed101\modern_tcn_seed101.pt | E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn_stage2_targeted\modern_tcn_v5_plantfix_stage2_l020_tt30_lr_seed101\modern_tcn_seed101.onnx |
