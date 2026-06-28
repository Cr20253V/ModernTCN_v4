# ModernTCN small base recipe: path_factory_logistics_showcase_theta10_v3

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_logistics_showcase_theta10_v3\baseline_lock_out.mat`
  - modern_base_seed21: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\16_recipe_vs_deployment_comparison\09_modern_base_closed_loop\01_closed_loop_runs\path_factory_logistics_showcase_theta10_v3\modern_base_seed21_out.mat`
  - modern_base_seed42: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\16_recipe_vs_deployment_comparison\09_modern_base_closed_loop\01_closed_loop_runs\path_factory_logistics_showcase_theta10_v3\modern_base_seed42_out.mat`
  - modern_base_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\16_recipe_vs_deployment_comparison\09_modern_base_closed_loop\01_closed_loop_runs\path_factory_logistics_showcase_theta10_v3\modern_base_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v3.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| baseline_lock | 6.0000 | 3.0000 | 7.0000 | 16.0000 | 1.0000 |
| modern_base_seed21 | 12.0000 | 6.0000 | 5.0000 | 23.0000 | 2.0000 |
| modern_base_seed42 | 21.0000 | 11.0000 | 13.0000 | 45.0000 | 3.0000 |
| modern_base_seed101 | 21.0000 | 10.0000 | 15.0000 | 46.0000 | 4.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0262 | 0.0882 | 0.0332 | 0.0261 | 0.0080 | 0.5292 | 286.5869 | 0.4144 | 1.0902 | 0.0000 | 0.4618 | 0.4922 | 98.2059 | 65.3211 |
| modern_base_seed21 | 0.0384 | 0.1347 | 0.0568 | 0.0298 | 0.0131 | 0.7668 | 285.9454 | 0.3140 | 1.0601 | 0.0000 | 0.4925 | 0.5094 | 97.8629 | 62.5191 |
| modern_base_seed42 | 0.7408 | 2.1461 | 0.3549 | 0.3940 | 0.0602 | 11.5870 | 706.3969 | 1.6387 | 1046 | 0.0000 | 0.9287 | 0.7087 | 91.3514 | 36.0139 |
| modern_base_seed101 | 0.9227 | 2.4815 | 0.2567 | 0.2827 | 0.0985 | 6.3873 | 720.0000 | 1.6560 | 666.5613 | 0.0000 | 0.6686 | 0.6968 | 96.5701 | 31.9878 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0214 | 0.0437 | 0.0466 | 2.9849 | 0.0000 |
| modern_base_seed21 | 0.0207 | 0.0529 | 0.0582 | 6.7773 | 0.0000 |
| modern_base_seed42 | 0.0247 | 0.0388 | 0.0505 | 0.6102 | 0.0000 |
| modern_base_seed101 | 0.0255 | 0.0386 | 0.0492 | 0.3562 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_base_seed21 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_base_seed42 | 17.0809 | 16.9754 | 29.3283 | 9.8834 | 0.0000 |
| modern_base_seed101 | 8.5220 | 7.0761 | 28.1990 | 13.8568 | 0.0000 |

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
| modern_base_seed21 | all | 0.0384 | 0.1347 | 0.0568 | 0.0298 | 0.0131 | 0.3140 | 1.0601 | 0.4925 | 0.5094 | 97.8629 | 62.5191 |
| modern_base_seed21 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| modern_base_seed21 | receiving_aisle_right_entry | 0.0111 | 0.0211 | 0.0174 | 0.0029 | 0.0077 | 0.3108 | 0.0255 | 0.0000 | 0.0000 | 100.0000 | 42.0000 |
| modern_base_seed21 | main_aisle_to_ramp | 0.0323 | 0.0730 | 0.0126 | 0.0506 | 0.0096 | 0.3140 | 0.6488 | 1.0704 | 1.0622 | 96.7000 | 45.5500 |
| modern_base_seed21 | extended_uphill_left_ramp_transfer | 0.0703 | 0.1347 | 0.1089 | 0.0198 | 0.0179 | 0.2166 | 0.1620 | 0.4056 | 0.4289 | 100.0000 | 38.0750 |
| modern_base_seed21 | upper_pickup_straight | 0.0093 | 0.0316 | 0.0167 | 0.0432 | 0.0220 | 0.0687 | 1.0191 | 0.8825 | 0.7830 | 93.8333 | 40.5000 |
| modern_base_seed21 | slope_reversal_right_transfer | 0.0443 | 0.0757 | 0.0659 | 0.0280 | 0.0176 | 0.2609 | 3.8788 | 0.5153 | 0.6056 | 98.5357 | 84.3571 |
| modern_base_seed21 | downhill_delivery_aisle | 0.0034 | 0.0099 | 0.0026 | 0.0219 | 0.0038 | 0.0141 | 0.7843 | 0.4095 | 0.4751 | 98.4444 | 72.3889 |
| modern_base_seed21 | shipping_cross_aisle | 0.0013 | 0.0021 | 0.0003606 | 0.0437 | 0.0028 | 0.0032 | 1.7832 | 0.9713 | 0.9680 | 96.3333 | 100.0000 |
| modern_base_seed21 | dock_approach_straight | 0.0117 | 0.0499 | 0.0119 | 0.0022 | 0.0118 | 0.0545 | 0.0073 | 1.515e-07 | 1.539e-07 | 91.0833 | 58.7500 |
| modern_base_seed42 | all | 0.7408 | 2.1461 | 0.3549 | 0.3940 | 0.0602 | 1.6387 | 1046 | 0.9287 | 0.7087 | 91.3514 | 36.0139 |
| modern_base_seed42 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| modern_base_seed42 | receiving_aisle_right_entry | 0.0094 | 0.0184 | 0.0178 | 0.0028 | 0.0078 | 0.2888 | 0.0158 | 0.0000 | 0.0000 | 100.0000 | 80.0000 |
| modern_base_seed42 | main_aisle_to_ramp | 0.0328 | 0.0778 | 0.0135 | 0.0502 | 0.0114 | 0.4347 | 1.5010 | 0.9984 | 1.0842 | 94.5000 | 47.2000 |
| modern_base_seed42 | extended_uphill_left_ramp_transfer | 0.1262 | 0.1855 | 0.1746 | 0.0343 | 0.0297 | 0.6048 | 0.8523 | 0.9384 | 0.9065 | 100.0000 | 42.9750 |
| modern_base_seed42 | upper_pickup_straight | 0.0744 | 0.1826 | 0.0833 | 0.0358 | 0.1060 | 1.3502 | 35.9091 | 0.5875 | 0.7379 | 88.2500 | 4.0000 |
| modern_base_seed42 | slope_reversal_right_transfer | 0.5921 | 1.1856 | 0.3164 | 0.0257 | 0.0238 | 1.0849 | 1.9976 | 0.3807 | 0.3469 | 98.1429 | 8.3571 |
| modern_base_seed42 | downhill_delivery_aisle | 1.5781 | 2.1461 | 0.4713 | 0.3615 | 0.1507 | 1.6337 | 7037 | 0.9928 | 0.8777 | 87.5000 | 35.6111 |
| modern_base_seed42 | shipping_cross_aisle | 1.1448 | 1.2170 | 0.7381 | 0.8811 | 0.0583 | 1.6387 | 2908 | 1.5174 | 1.7500 | 53.7083 | 7.0417 |
| modern_base_seed42 | dock_approach_straight | 1.1961 | 1.1974 | 0.4719 | 0.8309 | 0.0221 | 1.1571 | 9.147e-09 | 3.8722 | 1.515e-07 | 100.0000 | 0.0000 |
| modern_base_seed101 | all | 0.9227 | 2.4815 | 0.2567 | 0.2827 | 0.0985 | 1.6560 | 666.5613 | 0.6686 | 0.6968 | 96.5701 | 31.9878 |
| modern_base_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| modern_base_seed101 | receiving_aisle_right_entry | 0.0065 | 0.0149 | 0.0174 | 0.0028 | 0.0075 | 0.3754 | 0.0298 | 0.0000 | 0.0000 | 99.1667 | 31.7917 |
| modern_base_seed101 | main_aisle_to_ramp | 0.0455 | 0.0754 | 0.0189 | 0.0564 | 0.0133 | 0.2606 | 0.5894 | 1.0145 | 1.1122 | 98.7500 | 10.0500 |
| modern_base_seed101 | extended_uphill_left_ramp_transfer | 0.1214 | 0.1902 | 0.1766 | 0.0254 | 0.0288 | 0.4442 | 2.1019 | 0.6606 | 0.6328 | 100.0000 | 37.3000 |
| modern_base_seed101 | upper_pickup_straight | 0.0907 | 0.2201 | 0.0899 | 0.0434 | 0.1087 | 1.4241 | 26.0355 | 0.8782 | 0.8164 | 91.7500 | 5.2500 |
| modern_base_seed101 | slope_reversal_right_transfer | 0.5433 | 1.0432 | 0.2510 | 0.0375 | 0.0204 | 0.8815 | 2.3916 | 0.7494 | 0.8123 | 98.2143 | 8.1429 |
| modern_base_seed101 | downhill_delivery_aisle | 0.7161 | 1.1820 | 0.3946 | 0.1487 | 0.2136 | 1.6560 | 5332 | 0.6092 | 0.6333 | 93.9444 | 50.4444 |
| modern_base_seed101 | shipping_cross_aisle | 1.7785 | 2.4815 | 0.4471 | 0.5123 | 0.1849 | 1.6560 | 1247 | 1.5625 | 1.6899 | 85.5417 | 52.3750 |
| modern_base_seed101 | dock_approach_straight | 2.3653 | 2.3664 | 0.3834 | 0.8309 | 0.0234 | 1.5344 | 0.0020 | 1.515e-07 | 1.515e-07 | 100.0000 | 0.0000 |
