# Uncertainty replacement qualification: path_factory_logistics_showcase_theta10_v3

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_logistics_showcase_theta10_v3\baseline_lock_out.mat`
  - ua_seed21: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\12_uncertainty_replacement_qualification\03_closed_loop_representatives\01_closed_loop_runs\path_factory_logistics_showcase_theta10_v3\ua_seed21_out.mat`
  - ua_seed42: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\12_uncertainty_replacement_qualification\03_closed_loop_representatives\01_closed_loop_runs\path_factory_logistics_showcase_theta10_v3\ua_seed42_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v3.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| baseline_lock | 6.0000 | 4.0000 | 7.0000 | 17.0000 | 1.0000 |
| ua_seed21 | 12.0000 | 5.0000 | 5.0000 | 22.0000 | 2.0000 |
| ua_seed42 | 18.0000 | 9.0000 | 12.0000 | 39.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0262 | 0.0882 | 0.0332 | 0.0261 | 0.0080 | 0.5292 | 286.5869 | 0.4144 | 1.0902 | 0.0000 | 0.4618 | 0.4922 | 98.2059 | 65.3211 |
| ua_seed21 | 0.0405 | 0.1073 | 0.0634 | 0.0319 | 0.0190 | 0.6733 | 285.5779 | 0.3127 | 0.8749 | 0.0000 | 0.6390 | 0.5716 | 97.6941 | 69.7061 |
| ua_seed42 | 0.6918 | 2.1086 | 0.2388 | 0.3727 | 0.0771 | 9.3630 | 720.0000 | 1.6560 | 556.1849 | 0.0000 | 0.7612 | 0.7541 | 91.1931 | 41.2432 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0214 | 0.0437 | 0.0466 | 2.9849 | 0.0000 |
| ua_seed21 | 0.0207 | 0.0222 | 0.0244 | 5.2087 | 0.0000 |
| ua_seed42 | 0.0212 | 0.0227 | 0.0247 | 0.4386 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| ua_seed21 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| ua_seed42 | 17.6402 | 17.5822 | 32.3993 | 8.6433 | 0.0000 |

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
| ua_seed21 | all | 0.0405 | 0.1073 | 0.0634 | 0.0319 | 0.0190 | 0.3127 | 0.8749 | 0.6390 | 0.5716 | 97.6941 | 69.7061 |
| ua_seed21 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ua_seed21 | receiving_aisle_right_entry | 0.0078 | 0.0148 | 0.0174 | 0.0028 | 0.0071 | 0.3089 | 0.0253 | 0.1811 | 0.0000 | 100.0000 | 43.4583 |
| ua_seed21 | main_aisle_to_ramp | 0.0324 | 0.0752 | 0.0126 | 0.0414 | 0.0093 | 0.3127 | 0.5933 | 1.3198 | 0.7672 | 94.6000 | 47.0500 |
| ua_seed21 | extended_uphill_left_ramp_transfer | 0.0789 | 0.1073 | 0.1238 | 0.0183 | 0.0228 | 0.2467 | 0.2319 | 0.4547 | 0.4801 | 100.0000 | 65.4750 |
| ua_seed21 | upper_pickup_straight | 0.0226 | 0.0732 | 0.0361 | 0.0247 | 0.0507 | 0.1437 | 3.1845 | 0.5956 | 0.5512 | 96.0000 | 7.9167 |
| ua_seed21 | slope_reversal_right_transfer | 0.0329 | 0.0910 | 0.0657 | 0.0560 | 0.0203 | 0.2602 | 0.4859 | 1.3580 | 1.4562 | 98.8214 | 90.8571 |
| ua_seed21 | downhill_delivery_aisle | 0.0094 | 0.0374 | 0.0054 | 0.0166 | 0.0061 | 0.0322 | 3.4891 | 0.3084 | 0.3672 | 97.6667 | 74.4444 |
| ua_seed21 | shipping_cross_aisle | 0.0020 | 0.0032 | 0.0005335 | 0.0419 | 0.0028 | 0.0056 | 1.0980 | 0.7961 | 0.8242 | 91.4167 | 100.0000 |
| ua_seed21 | dock_approach_straight | 0.0100 | 0.0441 | 0.0106 | 0.0020 | 0.0110 | 0.0548 | 0.0073 | 0.1928 | 1.547e-07 | 100.0000 | 89.8333 |
| ua_seed42 | all | 0.6918 | 2.1086 | 0.2388 | 0.3727 | 0.0771 | 1.6560 | 556.1849 | 0.7612 | 0.7541 | 91.1931 | 41.2432 |
| ua_seed42 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ua_seed42 | receiving_aisle_right_entry | 0.0078 | 0.0143 | 0.0180 | 0.0028 | 0.0077 | 0.2793 | 0.0144 | 0.0000 | 0.0000 | 99.0833 | 63.2083 |
| ua_seed42 | main_aisle_to_ramp | 0.0054 | 0.0171 | 0.0033 | 0.0463 | 0.0053 | 0.0316 | 0.5421 | 0.8522 | 0.9445 | 96.0000 | 62.8500 |
| ua_seed42 | extended_uphill_left_ramp_transfer | 0.1526 | 0.2464 | 0.1918 | 0.0457 | 0.0254 | 0.5744 | 3.0065 | 1.2766 | 1.2196 | 100.0000 | 57.5750 |
| ua_seed42 | upper_pickup_straight | 0.1065 | 0.2644 | 0.0856 | 0.0495 | 0.1047 | 0.8002 | 104.0389 | 0.7604 | 0.9691 | 79.0833 | 8.3333 |
| ua_seed42 | slope_reversal_right_transfer | 0.8366 | 1.6125 | 0.3553 | 0.0257 | 0.0249 | 1.3063 | 5.7395 | 0.3671 | 0.3835 | 98.5714 | 14.7500 |
| ua_seed42 | downhill_delivery_aisle | 1.2455 | 2.1086 | 0.4269 | 0.1236 | 0.1974 | 1.6560 | 3048 | 0.8192 | 0.6036 | 89.3889 | 43.1111 |
| ua_seed42 | shipping_cross_aisle | 1.0579 | 1.1259 | 0.2222 | 0.8559 | 0.1001 | 1.6560 | 2043 | 1.7500 | 1.7500 | 54.7917 | 12.5000 |
| ua_seed42 | dock_approach_straight | 1.1266 | 1.1276 | 0.3215 | 0.8309 | 0.0239 | 0.7873 | 3.204e-09 | 1.515e-07 | 1.515e-07 | 100.0000 | 0.0000 |
