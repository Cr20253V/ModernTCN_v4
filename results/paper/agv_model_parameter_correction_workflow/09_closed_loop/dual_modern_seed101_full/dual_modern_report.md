# Dual ModernTCN Seed101 Closed-Loop Report

- generated: `2026-06-16 22:20:22`
- output_dir: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\dual_modern_seed101_full`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- ModernTCN slope ONNX: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_passive17_plus_all5_seed101\modern_tcn_seed101.onnx`
- ModernTCN turn ONNX: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.onnx`
- GRU model: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\models\GRU_model_full_gru_v5_plantfix_passive17_plus_all5_seed101.mat`
- TCN model: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\models\TCN_model_full_tcn_v5_plantfix_passive17_plus_all5_seed101.mat`

## Aggregate

| controller | n_paths | ey_rmse_mean | ey_peak_worst | xy_rmse_mean | j_du_mean | rank_ey |
|---|---|---|---|---|---|---|
| ModernTCN_turn_l020_tt25_seed101 | 3 | 0.0293881 | 0.0852651 | 0.599794 | 3.68078 | 1 |
| ModernTCN_slope_seed101 | 3 | 0.20648 | 1.46677 | 4.23266 | 64.0807 | 2 |
| GRU | 3 | 0.939034 | 8.40855 | 4.85317 | 659.981 | 3 |
| TCN | 3 | 5.26379 | 27.6947 | 9.04896 | 1029.16 | 4 |


## Per-Path Summary

| controller | path_tag | ey_rmse | ey_peak | xy_rmse | theta_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|
| ModernTCN_slope_seed101 | path_factory_logistics_showcase_theta10_v3 | 0.509868 | 1.46677 | 11.1323 | 1.05135 | 91.5572 | 32.7212 |
| GRU | path_factory_logistics_showcase_theta10_v3 | 2.7028 | 8.40855 | 14.0067 | 0.797102 | 91.6258 | 44.9422 |
| TCN | path_factory_logistics_showcase_theta10_v3 | 15.4697 | 27.6947 | 23.8856 | 1.277 | 78.5658 | 54.815 |
| ModernTCN_turn_l020_tt25_seed101 | path_factory_logistics_showcase_theta10_v3 | 0.0273817 | 0.0813942 | 0.575138 | 0.444974 | 98.1901 | 67.0519 |
| ModernTCN_slope_seed101 | path_closed_loop_long_updown_theta10_v1 | 0.0447946 | 0.13034 | 0.843353 | 0.874645 | 91.0825 | 44.5875 |
| GRU | path_closed_loop_long_updown_theta10_v1 | 0.0379474 | 0.109024 | 0.206448 | 0.683198 | 91.1055 | 59.7564 |
| TCN | path_closed_loop_long_updown_theta10_v1 | 0.161391 | 0.464665 | 1.63397 | 1.23635 | 74.8793 | 36.2216 |
| ModernTCN_turn_l020_tt25_seed101 | path_closed_loop_long_updown_theta10_v1 | 0.0336777 | 0.0852651 | 0.714726 | 0.705796 | 91.1055 | 47.7591 |
| ModernTCN_slope_seed101 | path_closed_loop_sharp_turn_transition_theta10_v1 | 0.0647756 | 0.191388 | 0.722347 | 0.622 | 94.1953 | 61.522 |
| GRU | path_closed_loop_sharp_turn_transition_theta10_v1 | 0.0763529 | 0.231654 | 0.346351 | 0.662546 | 92.6034 | 76.5871 |
| TCN | path_closed_loop_sharp_turn_transition_theta10_v1 | 0.160291 | 0.329661 | 1.62726 | 0.908756 | 83.0907 | 59.6583 |
| ModernTCN_turn_l020_tt25_seed101 | path_closed_loop_sharp_turn_transition_theta10_v1 | 0.0271049 | 0.0631645 | 0.509519 | 0.433332 | 94.9913 | 48.146 |

