# Uncertainty tuning Top5: path_factory_logistics_showcase_theta10_v3

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_logistics_showcase_theta10_v3\baseline_lock_out.mat`
  - u06_lr0013_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\01_closed_loop_runs\path_factory_logistics_showcase_theta10_v3\u06_lr0013_seed101_out.mat`
  - u04_lwlr0030_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\01_closed_loop_runs\path_factory_logistics_showcase_theta10_v3\u04_lwlr0030_seed101_out.mat`
  - u17_ltheta050_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\01_closed_loop_runs\path_factory_logistics_showcase_theta10_v3\u17_ltheta050_seed101_out.mat`
  - u23_turn_protect_mix_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\01_closed_loop_runs\path_factory_logistics_showcase_theta10_v3\u23_turn_protect_mix_seed101_out.mat`
  - u18_ltheta065_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\01_closed_loop_runs\path_factory_logistics_showcase_theta10_v3\u18_ltheta065_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v3.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| u04_lwlr0030_seed101 | 15.0000 | 10.0000 | 7.0000 | 32.0000 | 1.0000 |
| u18_ltheta065_seed101 | 14.0000 | 9.0000 | 12.0000 | 35.0000 | 2.0000 |
| u23_turn_protect_mix_seed101 | 15.0000 | 8.0000 | 15.0000 | 38.0000 | 3.0000 |
| baseline_lock | 23.0000 | 9.0000 | 12.0000 | 44.0000 | 4.0000 |
| u17_ltheta050_seed101 | 23.0000 | 9.0000 | 18.0000 | 50.0000 | 5.0000 |
| u06_lr0013_seed101 | 36.0000 | 18.0000 | 20.0000 | 74.0000 | 6.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0262 | 0.0882 | 0.0332 | 0.0261 | 0.0080 | 0.5292 | 286.5869 | 0.4144 | 1.0902 | 0.0000 | 0.4618 | 0.4922 | 98.2059 | 65.3211 |
| u06_lr0013_seed101 | 0.7699 | 2.6541 | 0.3252 | 0.3910 | 0.0550 | 11.2895 | 708.0284 | 1.6285 | 233.5304 | 0.0000 | 0.9239 | 0.6816 | 89.1246 | 33.3597 |
| u04_lwlr0030_seed101 | 0.0253 | 0.0937 | 0.0286 | 0.0214 | 0.0091 | 0.4646 | 285.5973 | 0.2353 | 0.9678 | 0.0000 | 0.2795 | 0.3203 | 97.3458 | 44.5676 |
| u17_ltheta050_seed101 | 0.0406 | 0.2112 | 0.0294 | 0.0251 | 0.0129 | 0.3586 | 286.3081 | 0.4461 | 2.1233 | 0.0000 | 0.4498 | 0.4727 | 98.6439 | 58.3083 |
| u23_turn_protect_mix_seed101 | 0.0254 | 0.0829 | 0.0317 | 0.0227 | 0.0102 | 0.3462 | 286.0825 | 0.3250 | 1.9103 | 0.0000 | 0.4045 | 0.4506 | 98.3800 | 58.8940 |
| u18_ltheta065_seed101 | 0.0245 | 0.0856 | 0.0317 | 0.0242 | 0.0088 | 0.3744 | 285.2432 | 0.2902 | 1.6890 | 0.0000 | 0.3900 | 0.4299 | 94.4858 | 61.0047 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0214 | 0.0437 | 0.0466 | 2.9849 | 0.0000 |
| u06_lr0013_seed101 | 0.0207 | 0.0279 | 0.0366 | 8.0724 | 0.0000 |
| u04_lwlr0030_seed101 | 0.0251 | 0.0343 | 0.0468 | 0.6452 | 0.0000 |
| u17_ltheta050_seed101 | 0.0223 | 0.0273 | 0.0358 | 3.4422 | 0.0000 |
| u23_turn_protect_mix_seed101 | 0.0212 | 0.0241 | 0.0336 | 0.4593 | 0.0000 |
| u18_ltheta065_seed101 | 0.0211 | 0.0234 | 0.0312 | 0.3038 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| u06_lr0013_seed101 | 16.2524 | 16.2155 | 29.4655 | 10.6538 | 0.0000 |
| u04_lwlr0030_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| u17_ltheta050_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| u23_turn_protect_mix_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| u18_ltheta065_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

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
| u06_lr0013_seed101 | all | 0.7699 | 2.6541 | 0.3252 | 0.3910 | 0.0550 | 1.6285 | 233.5304 | 0.9239 | 0.6816 | 89.1246 | 33.3597 |
| u06_lr0013_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| u06_lr0013_seed101 | receiving_aisle_right_entry | 0.0083 | 0.0156 | 0.0173 | 0.0029 | 0.0072 | 0.3241 | 0.0267 | 0.0000 | 0.0000 | 100.0000 | 40.4583 |
| u06_lr0013_seed101 | main_aisle_to_ramp | 0.0295 | 0.0566 | 0.0178 | 0.0439 | 0.0157 | 0.3552 | 0.5737 | 0.8214 | 0.9163 | 84.1000 | 57.6500 |
| u06_lr0013_seed101 | extended_uphill_left_ramp_transfer | 0.1094 | 0.1731 | 0.1562 | 0.0226 | 0.0273 | 0.3668 | 1.2568 | 0.5733 | 0.5571 | 100.0000 | 38.6250 |
| u06_lr0013_seed101 | upper_pickup_straight | 0.0571 | 0.1729 | 0.0562 | 0.0717 | 0.0567 | 0.3794 | 12.9874 | 1.7256 | 1.6695 | 96.0000 | 6.2500 |
| u06_lr0013_seed101 | slope_reversal_right_transfer | 0.5803 | 1.1575 | 0.2705 | 0.0295 | 0.0215 | 0.9753 | 3.0431 | 0.5310 | 0.6073 | 98.5000 | 9.5714 |
| u06_lr0013_seed101 | downhill_delivery_aisle | 1.9642 | 2.6541 | 0.4606 | 0.4600 | 0.1462 | 1.4392 | 885.6542 | 0.5960 | 0.6581 | 75.6111 | 49.6667 |
| u06_lr0013_seed101 | shipping_cross_aisle | 1.0081 | 2.3488 | 0.6840 | 0.8347 | 0.0628 | 1.6285 | 1168 | 1.6517 | 1.6530 | 49.4167 | 11.0833 |
| u06_lr0013_seed101 | dock_approach_straight | 0.8428 | 0.8439 | 0.4002 | 0.8309 | 0.0238 | 0.9675 | 5.084e-09 | 4.1458 | 1.515e-07 | 100.0000 | 0.0000 |
| u04_lwlr0030_seed101 | all | 0.0253 | 0.0937 | 0.0286 | 0.0214 | 0.0091 | 0.2353 | 0.9678 | 0.2795 | 0.3203 | 97.3458 | 44.5676 |
| u04_lwlr0030_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| u04_lwlr0030_seed101 | receiving_aisle_right_entry | 0.0066 | 0.0126 | 0.0172 | 0.0029 | 0.0070 | 0.1360 | 0.0155 | 0.0000 | 0.0000 | 100.0000 | 20.3750 |
| u04_lwlr0030_seed101 | main_aisle_to_ramp | 0.0339 | 0.0744 | 0.0129 | 0.0321 | 0.0116 | 0.1920 | 0.5807 | 0.4793 | 0.5326 | 95.7000 | 32.5500 |
| u04_lwlr0030_seed101 | extended_uphill_left_ramp_transfer | 0.0286 | 0.0456 | 0.0542 | 0.0093 | 0.0106 | 0.1433 | 0.0481 | 0.1965 | 0.2259 | 100.0000 | 16.7500 |
| u04_lwlr0030_seed101 | upper_pickup_straight | 0.0057 | 0.0150 | 0.0103 | 0.0322 | 0.0140 | 0.0453 | 1.2053 | 0.6577 | 0.5991 | 98.5000 | 35.8333 |
| u04_lwlr0030_seed101 | slope_reversal_right_transfer | 0.0242 | 0.0392 | 0.0274 | 0.0207 | 0.0090 | 0.2353 | 1.1343 | 0.2219 | 0.3526 | 98.1071 | 85.0357 |
| u04_lwlr0030_seed101 | downhill_delivery_aisle | 0.0506 | 0.0937 | 0.0133 | 0.0174 | 0.0077 | 0.0611 | 2.5700 | 0.3194 | 0.4057 | 96.0556 | 37.7778 |
| u04_lwlr0030_seed101 | shipping_cross_aisle | 0.0014 | 0.0021 | 0.0006263 | 0.0355 | 0.0029 | 0.0094 | 3.0804 | 0.6530 | 0.6934 | 95.3750 | 76.1250 |
| u04_lwlr0030_seed101 | dock_approach_straight | 0.0124 | 0.0528 | 0.0126 | 0.0021 | 0.0114 | 0.0611 | 0.0074 | 1.515e-07 | 1.626e-07 | 86.4167 | 14.0000 |
| u17_ltheta050_seed101 | all | 0.0406 | 0.2112 | 0.0294 | 0.0251 | 0.0129 | 0.4461 | 2.1233 | 0.4498 | 0.4727 | 98.6439 | 58.3083 |
| u17_ltheta050_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| u17_ltheta050_seed101 | receiving_aisle_right_entry | 0.0082 | 0.0174 | 0.0175 | 0.0029 | 0.0069 | 0.2952 | 0.0223 | 0.0000 | 0.0000 | 100.0000 | 56.4583 |
| u17_ltheta050_seed101 | main_aisle_to_ramp | 0.0331 | 0.0757 | 0.0122 | 0.0288 | 0.0079 | 0.4174 | 0.5433 | 0.3505 | 0.4618 | 96.2500 | 46.9000 |
| u17_ltheta050_seed101 | extended_uphill_left_ramp_transfer | 0.0220 | 0.0730 | 0.0313 | 0.0324 | 0.0137 | 0.1490 | 0.1026 | 0.9092 | 0.9253 | 100.0000 | 13.9750 |
| u17_ltheta050_seed101 | upper_pickup_straight | 0.0165 | 0.0672 | 0.0175 | 0.0228 | 0.0201 | 0.0651 | 4.1043 | 0.3888 | 0.4429 | 99.5000 | 50.8333 |
| u17_ltheta050_seed101 | slope_reversal_right_transfer | 0.0962 | 0.2112 | 0.0610 | 0.0189 | 0.0180 | 0.4461 | 9.5208 | 0.4916 | 0.4280 | 99.7500 | 83.7500 |
| u17_ltheta050_seed101 | downhill_delivery_aisle | 0.0144 | 0.0628 | 0.0149 | 0.0223 | 0.0180 | 0.0658 | 2.5696 | 0.4267 | 0.5037 | 96.5000 | 40.2222 |
| u17_ltheta050_seed101 | shipping_cross_aisle | 0.0009296 | 0.0016 | 0.0003317 | 0.0374 | 0.0028 | 0.0040 | 0.9078 | 0.6564 | 0.7067 | 95.5833 | 100.0000 |
| u17_ltheta050_seed101 | dock_approach_straight | 0.0156 | 0.0624 | 0.0137 | 0.0022 | 0.0112 | 0.0697 | 0.0074 | 1.515e-07 | 1.598e-07 | 100.0000 | 80.7500 |
| u23_turn_protect_mix_seed101 | all | 0.0254 | 0.0829 | 0.0317 | 0.0227 | 0.0102 | 0.3250 | 1.9103 | 0.4045 | 0.4506 | 98.3800 | 58.8940 |
| u23_turn_protect_mix_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| u23_turn_protect_mix_seed101 | receiving_aisle_right_entry | 0.0078 | 0.0146 | 0.0168 | 0.0029 | 0.0058 | 0.3250 | 0.0252 | 0.0000 | 0.0000 | 100.0000 | 42.4583 |
| u23_turn_protect_mix_seed101 | main_aisle_to_ramp | 0.0283 | 0.0579 | 0.0167 | 0.0320 | 0.0153 | 0.1591 | 0.5437 | 0.4790 | 0.5846 | 93.6500 | 44.0500 |
| u23_turn_protect_mix_seed101 | extended_uphill_left_ramp_transfer | 0.0301 | 0.0498 | 0.0457 | 0.0202 | 0.0079 | 0.1467 | 0.1048 | 0.5983 | 0.6225 | 100.0000 | 20.5000 |
| u23_turn_protect_mix_seed101 | upper_pickup_straight | 0.0078 | 0.0271 | 0.0052 | 0.0257 | 0.0058 | 0.0213 | 13.2789 | 0.5816 | 0.6267 | 98.0000 | 76.6667 |
| u23_turn_protect_mix_seed101 | slope_reversal_right_transfer | 0.0406 | 0.0829 | 0.0567 | 0.0250 | 0.0133 | 0.2996 | 2.0716 | 0.5315 | 0.5788 | 99.2143 | 81.5714 |
| u23_turn_protect_mix_seed101 | downhill_delivery_aisle | 0.0341 | 0.0756 | 0.0151 | 0.0252 | 0.0153 | 0.0587 | 0.9410 | 0.4956 | 0.5579 | 98.8889 | 39.8333 |
| u23_turn_protect_mix_seed101 | shipping_cross_aisle | 0.0016 | 0.0030 | 0.000645 | 0.0303 | 0.0028 | 0.0043 | 4.5450 | 0.5155 | 0.6266 | 95.2500 | 100.0000 |
| u23_turn_protect_mix_seed101 | dock_approach_straight | 0.0064 | 0.0174 | 0.0062 | 0.0020 | 0.0132 | 0.1084 | 0.0094 | 1.515e-07 | 1.904e-07 | 100.0000 | 80.8333 |
| u18_ltheta065_seed101 | all | 0.0245 | 0.0856 | 0.0317 | 0.0242 | 0.0088 | 0.2902 | 1.6890 | 0.3900 | 0.4299 | 94.4858 | 61.0047 |
| u18_ltheta065_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002397 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| u18_ltheta065_seed101 | receiving_aisle_right_entry | 0.0091 | 0.0169 | 0.0172 | 0.0029 | 0.0073 | 0.2902 | 0.0257 | 0.0000 | 0.0000 | 67.9167 | 36.4167 |
| u18_ltheta065_seed101 | main_aisle_to_ramp | 0.0508 | 0.0856 | 0.0164 | 0.0353 | 0.0134 | 0.2069 | 0.5711 | 0.4960 | 0.6073 | 96.7500 | 27.0000 |
| u18_ltheta065_seed101 | extended_uphill_left_ramp_transfer | 0.0332 | 0.0562 | 0.0589 | 0.0221 | 0.0091 | 0.1567 | 0.0782 | 0.4337 | 0.4549 | 100.0000 | 42.4750 |
| u18_ltheta065_seed101 | upper_pickup_straight | 0.0031 | 0.0085 | 0.0029 | 0.0222 | 0.0047 | 0.0165 | 10.3694 | 0.3787 | 0.4134 | 99.0000 | 93.1667 |
| u18_ltheta065_seed101 | slope_reversal_right_transfer | 0.0230 | 0.0531 | 0.0370 | 0.0325 | 0.0112 | 0.2069 | 1.1707 | 0.7880 | 0.8275 | 98.3214 | 75.2143 |
| u18_ltheta065_seed101 | downhill_delivery_aisle | 0.0083 | 0.0355 | 0.0065 | 0.0213 | 0.0090 | 0.0502 | 0.7731 | 0.4344 | 0.4887 | 98.0556 | 73.7778 |
| u18_ltheta065_seed101 | shipping_cross_aisle | 0.0018 | 0.0029 | 0.0005083 | 0.0296 | 0.0028 | 0.0038 | 5.4502 | 0.5092 | 0.5917 | 95.1667 | 100.0000 |
| u18_ltheta065_seed101 | dock_approach_straight | 0.0030 | 0.0068 | 0.0036 | 0.0020 | 0.0095 | 0.0336 | 0.0074 | 1.515e-07 | 1.82e-07 | 100.0000 | 28.8333 |
