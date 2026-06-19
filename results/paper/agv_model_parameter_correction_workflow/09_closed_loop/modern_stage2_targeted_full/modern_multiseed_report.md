# ModernTCN l020 tt25 Multiseed Closed-Loop Report

- generated: `2026-06-17 05:29:14`
- output_dir: `results\paper\agv_model_parameter_correction_workflow\09_closed_loop\modern_stage2_targeted_full`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`

## Models

- ModernTCN_turn_seed101_champion: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.onnx`
- ModernTCN_stage2_l020_tt30_lr_seed303: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn_stage2_targeted\modern_tcn_v5_plantfix_stage2_l020_tt30_lr_seed303\modern_tcn_seed303.onnx`
- ModernTCN_stage2_l020_tt30_lr_seed101: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn_stage2_targeted\modern_tcn_v5_plantfix_stage2_l020_tt30_lr_seed101\modern_tcn_seed101.onnx`

## Aggregate

| controller | n_paths | ey_rmse_mean | ey_peak_worst | xy_rmse_mean | j_du_mean | theta_mae_mean | main_acc_mean | turn_acc_mean | rank_ey |
|---|---|---|---|---|---|---|---|---|---|
| ModernTCN_turn_seed101_champion | 3 | 0.0293881 | 0.0852651 | 0.599794 | 3.68078 | 0.528034 | 94.7623 | 54.319 | 1 |
| ModernTCN_stage2_l020_tt30_lr_seed101 | 3 | 0.0417249 | 0.245376 | 0.461453 | 8.29038 | 0.735932 | 91.9632 | 55.3579 | 2 |
| ModernTCN_stage2_l020_tt30_lr_seed303 | 3 | 0.426678 | 2.26251 | 5.0791 | 128.483 | 0.835935 | 91.977 | 47.9062 | 3 |


## Per-Path Summary

| controller | path_tag | ey_rmse | ey_peak | xy_rmse | theta_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|
| ModernTCN_turn_seed101_champion | path_factory_logistics_showcase_theta10_v3 | 0.0273817 | 0.0813942 | 0.575138 | 0.444974 | 98.1901 | 67.0519 |
| ModernTCN_stage2_l020_tt30_lr_seed303 | path_factory_logistics_showcase_theta10_v3 | 1.1305 | 2.26251 | 13.3678 | 0.709196 | 91.1825 | 36.2408 |
| ModernTCN_stage2_l020_tt30_lr_seed101 | path_factory_logistics_showcase_theta10_v3 | 0.047773 | 0.245376 | 0.58913 | 0.523731 | 98.4645 | 61.0364 |
| ModernTCN_turn_seed101_champion | path_closed_loop_long_updown_theta10_v1 | 0.0336777 | 0.0852651 | 0.714726 | 0.705796 | 91.1055 | 47.7591 |
| ModernTCN_stage2_l020_tt30_lr_seed303 | path_closed_loop_long_updown_theta10_v1 | 0.0783202 | 0.264447 | 1.07803 | 1.01903 | 91.1744 | 53.0223 |
| ModernTCN_stage2_l020_tt30_lr_seed101 | path_closed_loop_long_updown_theta10_v1 | 0.041359 | 0.125397 | 0.481428 | 0.963204 | 86.6467 | 51.1836 |
| ModernTCN_turn_seed101_champion | path_closed_loop_sharp_turn_transition_theta10_v1 | 0.0271049 | 0.0631645 | 0.509519 | 0.433332 | 94.9913 | 48.146 |
| ModernTCN_stage2_l020_tt30_lr_seed303 | path_closed_loop_sharp_turn_transition_theta10_v1 | 0.0712179 | 0.223149 | 0.791409 | 0.779582 | 93.5741 | 54.4554 |
| ModernTCN_stage2_l020_tt30_lr_seed101 | path_closed_loop_sharp_turn_transition_theta10_v1 | 0.0360425 | 0.09161 | 0.3138 | 0.72086 | 90.7785 | 53.8536 |

