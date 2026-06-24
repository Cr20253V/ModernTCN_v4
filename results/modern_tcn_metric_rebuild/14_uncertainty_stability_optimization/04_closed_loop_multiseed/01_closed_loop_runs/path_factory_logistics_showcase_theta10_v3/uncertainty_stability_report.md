# Uncertainty stability optimization: path_factory_logistics_showcase_theta10_v3

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_logistics_showcase_theta10_v3\baseline_lock_out.mat`
  - s01_lr13_select_edges_flat_seed21: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\14_uncertainty_stability_optimization\04_closed_loop_multiseed\01_closed_loop_runs\path_factory_logistics_showcase_theta10_v3\s01_lr13_select_edges_flat_seed21_out.mat`
  - s01_lr13_select_edges_flat_seed42: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\14_uncertainty_stability_optimization\04_closed_loop_multiseed\01_closed_loop_runs\path_factory_logistics_showcase_theta10_v3\s01_lr13_select_edges_flat_seed42_out.mat`
  - s01_lr13_select_edges_flat_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\14_uncertainty_stability_optimization\04_closed_loop_multiseed\01_closed_loop_runs\path_factory_logistics_showcase_theta10_v3\s01_lr13_select_edges_flat_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v3.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| baseline_lock | 12.0000 | 5.0000 | 9.0000 | 26.0000 | 1.0000 |
| s01_lr13_select_edges_flat_seed101 | 9.0000 | 6.0000 | 11.0000 | 26.0000 | 2.0000 |
| s01_lr13_select_edges_flat_seed21 | 20.0000 | 11.0000 | 8.0000 | 39.0000 | 3.0000 |
| s01_lr13_select_edges_flat_seed42 | 19.0000 | 8.0000 | 12.0000 | 39.0000 | 4.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0262 | 0.0882 | 0.0332 | 0.0261 | 0.0080 | 0.5292 | 286.5869 | 0.4144 | 1.0902 | 0.0000 | 0.4618 | 0.4922 | 98.2059 | 65.3211 |
| s01_lr13_select_edges_flat_seed21 | 0.0499 | 0.1546 | 0.0676 | 0.0243 | 0.0181 | 1.1212 | 285.6837 | 0.3769 | 4.2683 | 0.0000 | 0.6311 | 0.4401 | 96.9870 | 57.5484 |
| s01_lr13_select_edges_flat_seed42 | 0.0529 | 0.1866 | 0.0732 | 0.0235 | 0.0176 | 1.0922 | 285.4446 | 0.4145 | 4.8586 | 0.0000 | 0.5305 | 0.4333 | 97.2930 | 58.0814 |
| s01_lr13_select_edges_flat_seed101 | 0.0265 | 0.0832 | 0.0321 | 0.0239 | 0.0111 | 0.3494 | 285.8836 | 0.3956 | 1.4252 | 0.0000 | 0.4178 | 0.4643 | 98.9763 | 48.5568 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0214 | 0.0437 | 0.0466 | 2.9849 | 0.0000 |
| s01_lr13_select_edges_flat_seed21 | 0.0208 | 0.0260 | 0.0346 | 3.5024 | 0.0000 |
| s01_lr13_select_edges_flat_seed42 | 0.0196 | 0.0209 | 0.0221 | 0.4119 | 0.0000 |
| s01_lr13_select_edges_flat_seed101 | 0.0205 | 0.0229 | 0.0242 | 3.3226 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| s01_lr13_select_edges_flat_seed21 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| s01_lr13_select_edges_flat_seed42 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| s01_lr13_select_edges_flat_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | all | 0.0262 | 0.0882 | 0.0332 | 0.0261 | 0.0080 | 0.4144 | 1.0902 | 0.4618 | 0.4922 | 98.2059 | 65.3211 |
| baseline_lock | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| baseline_lock | receiving_aisle_right_entry | 0.0060 | 0.0119 | 0.0169 | 0.0029 | 0.0060 | 0.4144 | 0.0695 | 0.0000 | 0.0000 | 100.0000 | 70.6250 |
| baseline_lock | main_aisle_to_ramp | 0.0027 | 0.0060 | 0.0018 | 0.0335 | 0.0039 | 0.0554 | 0.5186 | 0.5398 | 0.6474 | 96.4500 | 70.4500 |
| baseline_lock | extended_uphill_left_ramp_transfer | 0.0460 | 0.0711 | 0.0673 | 0.0136 | 0.0098 | 0.1541 | 0.1512 | 0.4061 | 0.4157 | 100.0000 | 14.6250 |
| baseline_lock | upper_pickup_straight | 0.0040 | 0.0160 | 0.0075 | 0.0363 | 0.0095 | 0.0336 | 6.1833 | 0.8595 | 0.7456 | 97.0000 | 70.5000 |
| baseline_lock | slope_reversal_right_transfer | 0.0177 | 0.0331 | 0.0231 | 0.0316 | 0.0110 | 0.2654 | 0.4388 | 0.6579 | 0.7521 | 97.8571 | 89.1071 |
| baseline_lock | downhill_delivery_aisle | 0.0445 | 0.0882 | 0.0161 | 0.0348 | 0.0088 | 0.0678 | 3.1403 | 0.7494 | 0.8135 | 97.5556 | 50.2222 |
| baseline_lock | shipping_cross_aisle | 0.0006739 | 0.0019 | 0.0007285 | 0.0365 | 0.0029 | 0.0055 | 1.7692 | 0.7604 | 0.7938 | 94.6250 | 100.0000 |
| baseline_lock | dock_approach_straight | 0.0023 | 0.0057 | 0.0033 | 0.0021 | 0.0097 | 0.0433 | 0.0075 | 1.515e-07 | 1.543e-07 | 100.0000 | 74.5833 |
| s01_lr13_select_edges_flat_seed21 | all | 0.0499 | 0.1546 | 0.0676 | 0.0243 | 0.0181 | 0.3769 | 4.2683 | 0.6311 | 0.4401 | 96.9870 | 57.5484 |
| s01_lr13_select_edges_flat_seed21 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| s01_lr13_select_edges_flat_seed21 | receiving_aisle_right_entry | 0.0074 | 0.0156 | 0.0174 | 0.0029 | 0.0070 | 0.2734 | 1.6922 | 1.6673 | 0.0000 | 94.6250 | 26.0417 |
| s01_lr13_select_edges_flat_seed21 | main_aisle_to_ramp | 0.0134 | 0.0351 | 0.0089 | 0.0352 | 0.0143 | 0.2033 | 0.5456 | 0.5326 | 0.6374 | 93.3500 | 64.9500 |
| s01_lr13_select_edges_flat_seed21 | extended_uphill_left_ramp_transfer | 0.0698 | 0.0974 | 0.1051 | 0.0157 | 0.0213 | 0.3251 | 0.8543 | 0.4005 | 0.4100 | 100.0000 | 30.8250 |
| s01_lr13_select_edges_flat_seed21 | upper_pickup_straight | 0.0226 | 0.0916 | 0.0265 | 0.0325 | 0.0337 | 0.1059 | 1.0509 | 0.7558 | 0.6574 | 99.5833 | 51.9167 |
| s01_lr13_select_edges_flat_seed21 | slope_reversal_right_transfer | 0.0869 | 0.1546 | 0.1193 | 0.0259 | 0.0221 | 0.3769 | 22.3678 | 0.6212 | 0.6276 | 98.4286 | 73.2857 |
| s01_lr13_select_edges_flat_seed21 | downhill_delivery_aisle | 0.0500 | 0.0934 | 0.0175 | 0.0279 | 0.0230 | 0.1343 | 3.2847 | 0.5799 | 0.6751 | 98.1667 | 32.1667 |
| s01_lr13_select_edges_flat_seed21 | shipping_cross_aisle | 0.0010 | 0.0032 | 0.0005514 | 0.0354 | 0.0028 | 0.0046 | 0.9256 | 0.6674 | 0.6932 | 94.1667 | 100.0000 |
| s01_lr13_select_edges_flat_seed21 | dock_approach_straight | 0.0286 | 0.0887 | 0.0166 | 0.0023 | 0.0128 | 0.2842 | 0.0107 | 1.515e-07 | 1.655e-07 | 92.7500 | 78.7500 |
| s01_lr13_select_edges_flat_seed42 | all | 0.0529 | 0.1866 | 0.0732 | 0.0235 | 0.0176 | 0.4145 | 4.8586 | 0.5305 | 0.4333 | 97.2930 | 58.0814 |
| s01_lr13_select_edges_flat_seed42 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| s01_lr13_select_edges_flat_seed42 | receiving_aisle_right_entry | 0.0077 | 0.0141 | 0.0163 | 0.0035 | 0.0065 | 0.3154 | 1.0962 | 0.9974 | 0.0097 | 97.1667 | 43.6667 |
| s01_lr13_select_edges_flat_seed42 | main_aisle_to_ramp | 0.0020 | 0.0054 | 0.0014 | 0.0352 | 0.0032 | 0.0235 | 0.6682 | 0.6189 | 0.7281 | 95.3000 | 96.4000 |
| s01_lr13_select_edges_flat_seed42 | extended_uphill_left_ramp_transfer | 0.0799 | 0.1080 | 0.1206 | 0.0170 | 0.0228 | 0.2692 | 0.3330 | 0.4148 | 0.4170 | 100.0000 | 14.9750 |
| s01_lr13_select_edges_flat_seed42 | upper_pickup_straight | 0.0237 | 0.0936 | 0.0270 | 0.0210 | 0.0354 | 0.1221 | 4.0082 | 0.4823 | 0.4720 | 91.7500 | 28.3333 |
| s01_lr13_select_edges_flat_seed42 | slope_reversal_right_transfer | 0.0873 | 0.1866 | 0.1214 | 0.0281 | 0.0229 | 0.4145 | 25.4201 | 0.6088 | 0.6089 | 98.3214 | 61.0357 |
| s01_lr13_select_edges_flat_seed42 | downhill_delivery_aisle | 0.0524 | 0.0946 | 0.0146 | 0.0285 | 0.0165 | 0.1068 | 2.4069 | 0.5811 | 0.6803 | 96.7778 | 46.3333 |
| s01_lr13_select_edges_flat_seed42 | shipping_cross_aisle | 0.0018 | 0.0063 | 0.0008564 | 0.0318 | 0.0029 | 0.0052 | 2.5718 | 0.5971 | 0.6531 | 93.8750 | 100.0000 |
| s01_lr13_select_edges_flat_seed42 | dock_approach_straight | 0.0167 | 0.0665 | 0.0148 | 0.0023 | 0.0118 | 0.0754 | 0.0075 | 1.515e-07 | 1.833e-07 | 100.0000 | 83.2500 |
| s01_lr13_select_edges_flat_seed101 | all | 0.0265 | 0.0832 | 0.0321 | 0.0239 | 0.0111 | 0.3956 | 1.4252 | 0.4178 | 0.4643 | 98.9763 | 48.5568 |
| s01_lr13_select_edges_flat_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| s01_lr13_select_edges_flat_seed101 | receiving_aisle_right_entry | 0.0065 | 0.0148 | 0.0174 | 0.0028 | 0.0074 | 0.3956 | 0.0216 | 0.0000 | 0.0000 | 100.0000 | 27.3750 |
| s01_lr13_select_edges_flat_seed101 | main_aisle_to_ramp | 0.0336 | 0.0592 | 0.0233 | 0.0265 | 0.0205 | 0.3398 | 0.5415 | 0.3216 | 0.4215 | 99.4500 | 25.4500 |
| s01_lr13_select_edges_flat_seed101 | extended_uphill_left_ramp_transfer | 0.0213 | 0.0342 | 0.0329 | 0.0189 | 0.0074 | 0.1436 | 0.0809 | 0.5424 | 0.5609 | 100.0000 | 8.6250 |
| s01_lr13_select_edges_flat_seed101 | upper_pickup_straight | 0.0077 | 0.0305 | 0.0070 | 0.0237 | 0.0080 | 0.0309 | 3.3487 | 0.4027 | 0.4642 | 99.2500 | 65.8333 |
| s01_lr13_select_edges_flat_seed101 | slope_reversal_right_transfer | 0.0472 | 0.0832 | 0.0675 | 0.0331 | 0.0164 | 0.3678 | 4.0413 | 0.7430 | 0.8052 | 99.6429 | 76.7143 |
| s01_lr13_select_edges_flat_seed101 | downhill_delivery_aisle | 0.0393 | 0.0727 | 0.0180 | 0.0315 | 0.0115 | 0.0714 | 2.6928 | 0.6695 | 0.7719 | 97.0000 | 40.3889 |
| s01_lr13_select_edges_flat_seed101 | shipping_cross_aisle | 0.0013 | 0.0026 | 0.000633 | 0.0307 | 0.0029 | 0.0040 | 2.1108 | 0.5569 | 0.6297 | 95.4167 | 100.0000 |
| s01_lr13_select_edges_flat_seed101 | dock_approach_straight | 0.0024 | 0.0037 | 0.0020 | 0.0020 | 0.0079 | 0.0220 | 0.0073 | 1.515e-07 | 1.729e-07 | 100.0000 | 39.6667 |
