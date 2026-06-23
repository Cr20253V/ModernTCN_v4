# Strict GRU/TCN validation: path_factory_logistics_showcase_theta10_v3

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_logistics_showcase_theta10_v3\baseline_lock_out.mat`
  - GRU: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\09_strict_gru_tcn_validation\path_factory_logistics_showcase_theta10_v3\GRU_seed101_out.mat`
  - TCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\09_strict_gru_tcn_validation\path_factory_logistics_showcase_theta10_v3\TCN_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v3.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| baseline_lock | 6.0000 | 3.0000 | 4.0000 | 13.0000 | 1.0000 |
| TCN | 12.0000 | 8.0000 | 10.0000 | 30.0000 | 2.0000 |
| GRU | 18.0000 | 7.0000 | 10.0000 | 35.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0262 | 0.0882 | 0.0332 | 0.0261 | 0.0080 | 0.5292 | 286.5869 | 0.4144 | 1.0902 | 0.0000 | 0.4618 | 0.4922 | 98.2059 | 65.3211 |
| GRU | 2.0064 | 5.6074 | 0.3852 | 0.1522 | 0.0835 | 5.1855 | 720.0000 | 1.6560 | 545.5049 | 0.0000 | 0.8234 | 0.8396 | 96.4435 | 37.7236 |
| TCN | 1.2420 | 4.7805 | 0.2056 | 0.0698 | 0.0620 | 3.2989 | 720.0000 | 1.6319 | 448.5571 | 0.0000 | 0.9620 | 0.9640 | 71.7482 | 44.8578 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0214 | 0.0437 | 0.0466 | 2.9849 | 0.0000 |
| GRU | 0.0181 | 0.0209 | 0.0233 | 4.2039 | 0.0000 |
| TCN | 0.0130 | 0.0175 | 0.0204 | 3.6906 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| GRU | 2.0685 | 2.0263 | 45.0214 | 30.1514 | 0.0000 |
| TCN | 0.3535 | 0.3113 | 15.6298 | 10.1525 | 0.0000 |

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
| GRU | all | 2.0064 | 5.6074 | 0.3852 | 0.1522 | 0.0835 | 1.6560 | 545.5049 | 0.8234 | 0.8396 | 96.4435 | 37.7236 |
| GRU | startup | 0.0000 | 0.0000 | 0.0000 | 0.1311 | 0.0000 | 0.0002397 | 21.1368 | 2.2613 | 2.1716 | 100.0000 | 100.0000 |
| GRU | receiving_aisle_right_entry | 0.2828 | 0.4769 | 0.1339 | 0.0486 | 0.0366 | 1.6268 | 104.9454 | 0.6530 | 0.6979 | 100.0000 | 84.0000 |
| GRU | main_aisle_to_ramp | 0.4198 | 0.7215 | 0.2890 | 0.0728 | 0.2107 | 1.6221 | 367.8772 | 0.2592 | 0.2234 | 99.7500 | 7.8000 |
| GRU | extended_uphill_left_ramp_transfer | 2.5037 | 3.8481 | 0.1746 | 0.1223 | 0.0286 | 1.4041 | 857.0772 | 0.5610 | 0.5309 | 100.0000 | 10.4250 |
| GRU | upper_pickup_straight | 2.1889 | 3.5280 | 0.6964 | 0.3674 | 0.1188 | 1.6560 | 3928 | 0.5912 | 0.6418 | 85.8333 | 53.7500 |
| GRU | slope_reversal_right_transfer | 3.9088 | 5.6074 | 0.7200 | 0.2315 | 0.0195 | 1.5563 | 35.8045 | 0.4049 | 0.5244 | 94.3571 | 26.3929 |
| GRU | downhill_delivery_aisle | 1.0915 | 2.8175 | 0.4977 | 0.1126 | 0.1019 | 1.4544 | 592.7782 | 0.4358 | 0.4794 | 89.0556 | 0.0000 |
| GRU | shipping_cross_aisle | 0.0031 | 0.0104 | 0.0014 | 0.0513 | 0.0033 | 0.0224 | 0.0324 | 1.0654 | 1.0776 | 94.0000 | 84.4167 |
| GRU | dock_approach_straight | 0.0029 | 0.0035 | 0.0003152 | 0.1023 | 0.0027 | 0.0048 | 0.0245 | 2.8119 | 2.8071 | 100.0000 | 0.0000 |
| TCN | all | 1.2420 | 4.7805 | 0.2056 | 0.0698 | 0.0620 | 1.6319 | 448.5571 | 0.9620 | 0.9640 | 71.7482 | 44.8578 |
| TCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 1.6747 | 0.0000 | 100.0000 | 100.0000 |
| TCN | receiving_aisle_right_entry | 0.0093 | 0.0189 | 0.0152 | 0.0043 | 0.0078 | 0.4387 | 0.7791 | 1.4157 | 0.0186 | 43.5833 | 81.8333 |
| TCN | main_aisle_to_ramp | 0.0405 | 0.0844 | 0.0129 | 0.1099 | 0.0121 | 0.5265 | 326.5100 | 0.8382 | 2.1309 | 47.0000 | 39.4000 |
| TCN | extended_uphill_left_ramp_transfer | 0.5068 | 0.9121 | 0.3976 | 0.0917 | 0.0372 | 1.4225 | 433.2062 | 0.8415 | 1.6728 | 94.2000 | 43.8000 |
| TCN | upper_pickup_straight | 0.2720 | 0.5203 | 0.2249 | 0.0622 | 0.2243 | 1.6319 | 4973 | 0.9545 | 0.8983 | 65.0833 | 6.6667 |
| TCN | slope_reversal_right_transfer | 3.0775 | 4.7805 | 0.1490 | 0.0697 | 0.0240 | 1.2864 | 2.8524 | 0.2173 | 0.3366 | 97.6786 | 4.5357 |
| TCN | downhill_delivery_aisle | 0.9400 | 1.7219 | 0.1575 | 0.0335 | 0.0512 | 0.9264 | 3.5109 | 0.9725 | 0.7627 | 87.7222 | 0.0000 |
| TCN | shipping_cross_aisle | 0.0249 | 0.0872 | 0.0115 | 0.0765 | 0.0067 | 0.0755 | 56.0166 | 1.3320 | 1.6150 | 66.5833 | 59.9583 |
| TCN | dock_approach_straight | 0.0066 | 0.0088 | 0.0005751 | 0.0017 | 0.0083 | 0.0442 | 0.0072 | 0.8997 | 0.0018 | 0.0000 | 100.0000 |
