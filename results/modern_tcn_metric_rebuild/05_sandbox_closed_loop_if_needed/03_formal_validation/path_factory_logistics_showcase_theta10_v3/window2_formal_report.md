# Window 2 formal validation: path_factory_logistics_showcase_theta10_v3

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_logistics_showcase_theta10_v3\baseline_lock_out.mat`
  - uncertainty_seed101_rerun_20260622: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_logistics_showcase_theta10_v3\uncertainty_seed101_rerun_20260622_out.mat`
  - mode_theta_detach_flatreg001_seed21_rerun_20260622: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_logistics_showcase_theta10_v3\mode_theta_detach_flatreg001_seed21_rerun_20260622_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v3.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| baseline_lock | 10.0000 | 5.0000 | 6.0000 | 21.0000 | 1.0000 |
| uncertainty_seed101_rerun_20260622 | 10.0000 | 7.0000 | 10.0000 | 27.0000 | 2.0000 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | 16.0000 | 6.0000 | 8.0000 | 30.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0262 | 0.0882 | 0.0332 | 0.0261 | 0.0080 | 0.5292 | 286.5869 | 0.4144 | 1.0902 | 0.0000 | 0.4618 | 0.4922 | 98.2059 | 65.3211 |
| uncertainty_seed101_rerun_20260622 | 0.0277 | 0.0825 | 0.0345 | 0.0223 | 0.0087 | 0.4538 | 286.7149 | 0.5016 | 1.4905 | 0.0000 | 0.3583 | 0.3893 | 95.2615 | 56.5669 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | 0.0438 | 0.1346 | 0.0617 | 0.0216 | 0.0159 | 0.8590 | 286.1287 | 0.3491 | 3.9231 | 0.0000 | 0.3658 | 0.3812 | 97.8946 | 58.6935 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0214 | 0.0437 | 0.0466 | 2.9849 | 0.0000 |
| uncertainty_seed101_rerun_20260622 | 0.0217 | 0.0450 | 0.0479 | 0.4257 | 0.0000 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | 0.0213 | 0.0458 | 0.0498 | 0.6382 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| uncertainty_seed101_rerun_20260622 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

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
| uncertainty_seed101_rerun_20260622 | all | 0.0277 | 0.0825 | 0.0345 | 0.0223 | 0.0087 | 0.5016 | 1.4905 | 0.3583 | 0.3893 | 95.2615 | 56.5669 |
| uncertainty_seed101_rerun_20260622 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| uncertainty_seed101_rerun_20260622 | receiving_aisle_right_entry | 0.0068 | 0.0125 | 0.0185 | 0.0054 | 0.0079 | 0.4537 | 1.6406 | 0.0275 | 0.0259 | 90.2083 | 33.8750 |
| uncertainty_seed101_rerun_20260622 | main_aisle_to_ramp | 0.0361 | 0.0797 | 0.0149 | 0.0365 | 0.0123 | 0.5016 | 0.6669 | 0.5593 | 0.6605 | 78.6000 | 53.7000 |
| uncertainty_seed101_rerun_20260622 | extended_uphill_left_ramp_transfer | 0.0454 | 0.0674 | 0.0712 | 0.0127 | 0.0100 | 0.1535 | 0.1582 | 0.3657 | 0.3665 | 100.0000 | 38.4500 |
| uncertainty_seed101_rerun_20260622 | upper_pickup_straight | 0.0041 | 0.0110 | 0.0067 | 0.0251 | 0.0094 | 0.0305 | 6.7159 | 0.5811 | 0.5462 | 99.1667 | 50.7500 |
| uncertainty_seed101_rerun_20260622 | slope_reversal_right_transfer | 0.0087 | 0.0174 | 0.0145 | 0.0246 | 0.0093 | 0.1567 | 0.7706 | 0.3889 | 0.4965 | 98.4643 | 80.5357 |
| uncertainty_seed101_rerun_20260622 | downhill_delivery_aisle | 0.0431 | 0.0825 | 0.0152 | 0.0224 | 0.0080 | 0.0624 | 3.4067 | 0.5252 | 0.5505 | 96.2778 | 51.8333 |
| uncertainty_seed101_rerun_20260622 | shipping_cross_aisle | 0.0012 | 0.0029 | 0.0005757 | 0.0322 | 0.0028 | 0.0109 | 2.3719 | 0.5878 | 0.6213 | 95.2083 | 96.1667 |
| uncertainty_seed101_rerun_20260622 | dock_approach_straight | 0.0019 | 0.0065 | 0.0030 | 0.0021 | 0.0081 | 0.0274 | 0.0074 | 1.515e-07 | 1.69e-07 | 100.0000 | 3.3333 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | all | 0.0438 | 0.1346 | 0.0617 | 0.0216 | 0.0159 | 0.3491 | 3.9231 | 0.3658 | 0.3812 | 97.8946 | 58.6935 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | receiving_aisle_right_entry | 0.0079 | 0.0145 | 0.0167 | 0.0029 | 0.0057 | 0.2898 | 0.0233 | 0.0000 | 0.0000 | 100.0000 | 25.9583 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | main_aisle_to_ramp | 0.0021 | 0.0060 | 0.0014 | 0.0298 | 0.0033 | 0.0322 | 0.5684 | 0.3913 | 0.4982 | 96.3500 | 95.7500 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | extended_uphill_left_ramp_transfer | 0.0672 | 0.0919 | 0.1000 | 0.0211 | 0.0202 | 0.2746 | 0.3906 | 0.5475 | 0.5393 | 100.0000 | 14.9750 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | upper_pickup_straight | 0.0201 | 0.0797 | 0.0254 | 0.0203 | 0.0335 | 0.1008 | 4.0145 | 0.5304 | 0.4775 | 92.0833 | 18.8333 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | slope_reversal_right_transfer | 0.0769 | 0.1346 | 0.1043 | 0.0237 | 0.0223 | 0.3491 | 18.2694 | 0.4395 | 0.4674 | 98.6071 | 77.5000 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | downhill_delivery_aisle | 0.0242 | 0.0816 | 0.0120 | 0.0177 | 0.0111 | 0.1072 | 0.7797 | 0.3328 | 0.3580 | 97.3889 | 55.3889 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | shipping_cross_aisle | 0.0014 | 0.0023 | 0.000533 | 0.0320 | 0.0029 | 0.0041 | 5.8029 | 0.6224 | 0.6433 | 93.9583 | 100.0000 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | dock_approach_straight | 0.0025 | 0.0069 | 0.0043 | 0.0022 | 0.0091 | 0.0610 | 0.0078 | 1.515e-07 | 1.913e-07 | 100.0000 | 86.8333 |
