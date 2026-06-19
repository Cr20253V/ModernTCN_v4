# ModernTCN l020 tt25 Multiseed Closed-Loop Report

- generated: `2026-06-17 01:00:34`
- output_dir: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\modern_multiseed_l020_tt25_full`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`

## Models

- ModernTCN_turn_seed101_champion: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.onnx`
- ModernTCN_turn_seed101_multiseed: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_multiseed_seed101\modern_tcn_seed101.onnx`
- ModernTCN_turn_seed202_multiseed: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_multiseed_seed202\modern_tcn_seed202.onnx`
- ModernTCN_turn_seed303_multiseed: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_multiseed_seed303\modern_tcn_seed303.onnx`

## Aggregate

| controller | n_paths | ey_rmse_mean | ey_peak_worst | xy_rmse_mean | j_du_mean | theta_mae_mean | main_acc_mean | turn_acc_mean | rank_ey |
|---|---|---|---|---|---|---|---|---|---|
| ModernTCN_turn_seed101_champion | 3 | 0.0293881 | 0.0852651 | 0.599794 | 3.68078 | 0.528034 | 94.7623 | 54.319 | 1 |
| ModernTCN_turn_seed303_multiseed | 3 | 0.0294623 | 0.0873085 | 0.62834 | 8.12496 | 0.643644 | 92.2607 | 52.56 | 2 |
| ModernTCN_turn_seed101_multiseed | 3 | 0.0404156 | 0.232829 | 0.527668 | 7.68622 | 0.72384 | 93.0552 | 52.4461 | 3 |
| ModernTCN_turn_seed202_multiseed | 3 | 0.251289 | 1.91837 | 3.66289 | 279.34 | 0.72935 | 90.8022 | 48.9604 | 4 |


## Per-Path Summary

| controller | path_tag | ey_rmse | ey_peak | xy_rmse | theta_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|
| ModernTCN_turn_seed101_champion | path_factory_logistics_showcase_theta10_v3 | 0.0273817 | 0.0813942 | 0.575138 | 0.444974 | 98.1901 | 67.0519 |
| ModernTCN_turn_seed101_multiseed | path_factory_logistics_showcase_theta10_v3 | 0.0452726 | 0.232829 | 0.430592 | 0.534127 | 96.6598 | 56.8202 |
| ModernTCN_turn_seed202_multiseed | path_factory_logistics_showcase_theta10_v3 | 0.68204 | 1.91837 | 9.638 | 0.694238 | 91.325 | 49.475 |
| ModernTCN_turn_seed303_multiseed | path_factory_logistics_showcase_theta10_v3 | 0.0316331 | 0.0873085 | 0.736648 | 0.373713 | 96.4435 | 55.4272 |
| ModernTCN_turn_seed101_champion | path_closed_loop_long_updown_theta10_v1 | 0.0336777 | 0.0852651 | 0.714726 | 0.705796 | 91.1055 | 47.7591 |
| ModernTCN_turn_seed101_multiseed | path_closed_loop_long_updown_theta10_v1 | 0.0377398 | 0.0934862 | 0.784465 | 0.959389 | 89.3588 | 47.4604 |
| ModernTCN_turn_seed202_multiseed | path_closed_loop_long_updown_theta10_v1 | 0.0406357 | 0.0862668 | 0.867661 | 0.864555 | 86.4399 | 42.1742 |
| ModernTCN_turn_seed303_multiseed | path_closed_loop_long_updown_theta10_v1 | 0.0302423 | 0.0862072 | 0.715807 | 0.933022 | 88.5314 | 49.5059 |
| ModernTCN_turn_seed101_champion | path_closed_loop_sharp_turn_transition_theta10_v1 | 0.0271049 | 0.0631645 | 0.509519 | 0.433332 | 94.9913 | 48.146 |
| ModernTCN_turn_seed101_multiseed | path_closed_loop_sharp_turn_transition_theta10_v1 | 0.0382344 | 0.0977951 | 0.367947 | 0.678004 | 93.147 | 53.0577 |
| ModernTCN_turn_seed202_multiseed | path_closed_loop_sharp_turn_transition_theta10_v1 | 0.0311905 | 0.0801719 | 0.483007 | 0.629258 | 94.6418 | 55.232 |
| ModernTCN_turn_seed303_multiseed | path_closed_loop_sharp_turn_transition_theta10_v1 | 0.0265115 | 0.0834472 | 0.432564 | 0.624197 | 91.8074 | 52.747 |

