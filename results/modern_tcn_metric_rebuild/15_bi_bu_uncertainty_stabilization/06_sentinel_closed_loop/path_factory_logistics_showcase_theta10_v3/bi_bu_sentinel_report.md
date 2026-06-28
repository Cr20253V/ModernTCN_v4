# BI-BU sentinel closed-loop: path_factory_logistics_showcase_theta10_v3

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\15_bi_bu_uncertainty_stabilization\06_sentinel_closed_loop\path_factory_logistics_showcase_theta10_v3\baseline_lock_out.mat`
  - a2_freeze_early_seed21: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\15_bi_bu_uncertainty_stabilization\06_sentinel_closed_loop\path_factory_logistics_showcase_theta10_v3\a2_freeze_early_seed21_out.mat`
  - a2_freeze_early_seed42: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\15_bi_bu_uncertainty_stabilization\06_sentinel_closed_loop\path_factory_logistics_showcase_theta10_v3\a2_freeze_early_seed42_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v3.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| baseline_lock | 6.0000 | 4.0000 | 5.0000 | 15.0000 | 1.0000 |
| a2_freeze_early_seed42 | 16.0000 | 5.0000 | 10.0000 | 31.0000 | 2.0000 |
| a2_freeze_early_seed21 | 14.0000 | 9.0000 | 9.0000 | 32.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0262 | 0.0882 | 0.0332 | 0.0261 | 0.0080 | 0.5292 | 286.5869 | 0.4144 | 1.0902 | 0.0000 | 0.4618 | 0.4922 | 98.2059 | 65.3211 |
| a2_freeze_early_seed21 | 0.0347 | 0.1204 | 0.0444 | 0.0299 | 0.0142 | 0.5362 | 286.0215 | 0.6497 | 14.1797 | 0.0000 | 0.5393 | 0.5647 | 98.0423 | 54.8573 |
| a2_freeze_early_seed42 | 0.0337 | 0.1585 | 0.0467 | 0.0266 | 0.0144 | 0.6393 | 286.7303 | 0.5603 | 8.5156 | 0.0000 | 0.4655 | 0.5282 | 98.6228 | 65.3000 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0207 | 0.0249 | 0.0350 | 6.1242 | 0.0000 |
| a2_freeze_early_seed21 | 0.0204 | 0.0224 | 0.0244 | 3.2384 | 0.0000 |
| a2_freeze_early_seed42 | 0.0203 | 0.0222 | 0.0237 | 0.4338 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| a2_freeze_early_seed21 | 0.0000 | 0.0000 | 0.0106 | 0.0000 | 0.0000 |
| a2_freeze_early_seed42 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

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
| a2_freeze_early_seed21 | all | 0.0347 | 0.1204 | 0.0444 | 0.0299 | 0.0142 | 0.6497 | 14.1797 | 0.5393 | 0.5647 | 98.0423 | 54.8573 |
| a2_freeze_early_seed21 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| a2_freeze_early_seed21 | receiving_aisle_right_entry | 0.0082 | 0.0253 | 0.0184 | 0.0028 | 0.0079 | 0.3663 | 0.0200 | 0.0000 | 0.0000 | 100.0000 | 77.5833 |
| a2_freeze_early_seed21 | main_aisle_to_ramp | 0.0349 | 0.0811 | 0.0123 | 0.0321 | 0.0094 | 0.2576 | 0.5570 | 0.4660 | 0.5819 | 95.4000 | 42.9000 |
| a2_freeze_early_seed21 | extended_uphill_left_ramp_transfer | 0.0339 | 0.0522 | 0.0415 | 0.0229 | 0.0087 | 0.1490 | 0.1080 | 0.6930 | 0.6955 | 100.0000 | 16.6500 |
| a2_freeze_early_seed21 | upper_pickup_straight | 0.0107 | 0.0391 | 0.0088 | 0.0304 | 0.0104 | 0.0365 | 4.4929 | 0.6293 | 0.5674 | 95.7500 | 54.5000 |
| a2_freeze_early_seed21 | slope_reversal_right_transfer | 0.0695 | 0.1204 | 0.1008 | 0.0530 | 0.0269 | 0.6497 | 91.0622 | 1.1814 | 1.2781 | 98.6786 | 76.6429 |
| a2_freeze_early_seed21 | downhill_delivery_aisle | 0.0331 | 0.0842 | 0.0211 | 0.0222 | 0.0228 | 0.1064 | 0.8236 | 0.4946 | 0.4850 | 96.8333 | 21.1667 |
| a2_freeze_early_seed21 | shipping_cross_aisle | 0.0014 | 0.0045 | 0.0007628 | 0.0338 | 0.0028 | 0.0220 | 2.1028 | 0.6514 | 0.6767 | 94.4167 | 90.2500 |
| a2_freeze_early_seed21 | dock_approach_straight | 0.0032 | 0.0082 | 0.0047 | 0.0020 | 0.0095 | 0.0176 | 0.0074 | 1.515e-07 | 1.592e-07 | 100.0000 | 42.7500 |
| a2_freeze_early_seed42 | all | 0.0337 | 0.1585 | 0.0467 | 0.0266 | 0.0144 | 0.5603 | 8.5156 | 0.4655 | 0.5282 | 98.6228 | 65.3000 |
| a2_freeze_early_seed42 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| a2_freeze_early_seed42 | receiving_aisle_right_entry | 0.0071 | 0.0177 | 0.0181 | 0.0028 | 0.0067 | 0.3751 | 0.0241 | 0.0000 | 0.0000 | 100.0000 | 72.5417 |
| a2_freeze_early_seed42 | main_aisle_to_ramp | 0.0069 | 0.0171 | 0.0015 | 0.0275 | 0.0035 | 0.0825 | 0.8191 | 0.2861 | 0.4509 | 96.4500 | 74.8500 |
| a2_freeze_early_seed42 | extended_uphill_left_ramp_transfer | 0.0208 | 0.0596 | 0.0276 | 0.0242 | 0.0108 | 0.1405 | 0.0926 | 0.7574 | 0.7754 | 100.0000 | 15.7500 |
| a2_freeze_early_seed42 | upper_pickup_straight | 0.0142 | 0.0563 | 0.0149 | 0.0315 | 0.0178 | 0.0600 | 13.1957 | 0.5800 | 0.7397 | 96.8333 | 49.4167 |
| a2_freeze_early_seed42 | slope_reversal_right_transfer | 0.0788 | 0.1585 | 0.1135 | 0.0423 | 0.0285 | 0.5603 | 46.6780 | 0.9042 | 0.9760 | 99.8929 | 79.3214 |
| a2_freeze_early_seed42 | downhill_delivery_aisle | 0.0320 | 0.1068 | 0.0232 | 0.0236 | 0.0171 | 0.1119 | 0.7938 | 0.5399 | 0.5462 | 97.6667 | 58.9444 |
| a2_freeze_early_seed42 | shipping_cross_aisle | 0.0012 | 0.0020 | 0.0004001 | 0.0299 | 0.0028 | 0.0042 | 4.6213 | 0.4251 | 0.5847 | 95.5417 | 100.0000 |
| a2_freeze_early_seed42 | dock_approach_straight | 0.0087 | 0.0401 | 0.0105 | 0.0020 | 0.0110 | 0.0515 | 0.0075 | 1.515e-07 | 1.723e-07 | 100.0000 | 90.1667 |
