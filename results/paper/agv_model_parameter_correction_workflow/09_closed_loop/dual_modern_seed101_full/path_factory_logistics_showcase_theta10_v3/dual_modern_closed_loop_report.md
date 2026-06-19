# Dual ModernTCN seed101 plantfix closed-loop comparison

- 输出文件：
  - ModernTCN_slope_seed101: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\dual_modern_seed101_full\path_factory_logistics_showcase_theta10_v3\ModernTCN_slope_seed101_out.mat`
  - GRU: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\dual_modern_seed101_full\path_factory_logistics_showcase_theta10_v3\GRU_seed101_out.mat`
  - TCN: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\dual_modern_seed101_full\path_factory_logistics_showcase_theta10_v3\TCN_seed101_out.mat`
  - ModernTCN_turn_l020_tt25_seed101: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\dual_modern_seed101_full\path_factory_logistics_showcase_theta10_v3\ModernTCN_turn_l020_tt25_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v3.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN_turn_l020_tt25_seed101 | 6.0000 | 3.0000 | 7.0000 | 16.0000 | 1.0000 |
| ModernTCN_slope_seed101 | 12.0000 | 10.0000 | 9.0000 | 31.0000 | 2.0000 |
| GRU | 18.0000 | 7.0000 | 11.0000 | 36.0000 | 3.0000 |
| TCN | 24.0000 | 10.0000 | 13.0000 | 47.0000 | 4.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN_slope_seed101 | 0.5099 | 1.4668 | 0.1774 | 0.4100 | 0.0473 | 11.1323 | 720.0000 | 1.6560 | 181.2437 | 0.0000 | 1.0514 | 0.7034 | 91.5572 | 32.7212 |
| GRU | 2.7028 | 8.4086 | 0.5157 | 0.4358 | 0.0953 | 14.0067 | 720.0000 | 1.6560 | 1973 | 0.0000 | 0.7971 | 0.8080 | 91.6258 | 44.9422 |
| TCN | 15.4697 | 27.6947 | 0.7977 | 1.1059 | 0.1167 | 23.8856 | 863.6720 | 1.6560 | 2594 | 0.0000 | 1.2770 | 1.4131 | 78.5658 | 54.8150 |
| ModernTCN_turn_l020_tt25_seed101 | 0.0274 | 0.0814 | 0.0358 | 0.0254 | 0.0086 | 0.5751 | 288.1106 | 0.3509 | 1.1828 | 0.0000 | 0.4450 | 0.4760 | 98.1901 | 67.0519 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN_slope_seed101 | 0.0390 | 0.0453 | 0.0477 | 3.2445 | 0.0000 |
| GRU | 0.0189 | 0.0214 | 0.0247 | 0.4851 | 0.0000 |
| TCN | 0.0169 | 0.0203 | 0.0253 | 0.4488 | 0.0000 |
| ModernTCN_turn_l020_tt25_seed101 | 0.0431 | 0.0459 | 0.0480 | 0.8224 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN_slope_seed101 | 19.7034 | 19.6929 | 29.4866 | 3.2769 | 0.0000 |
| GRU | 21.7508 | 21.6400 | 69.9910 | 35.8187 | 0.0000 |
| TCN | 32.8004 | 32.6262 | 55.7913 | 48.8312 | 0.0000 |
| ModernTCN_turn_l020_tt25_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN_slope_seed101 | all | 0.5099 | 1.4668 | 0.1774 | 0.4100 | 0.0473 | 1.6560 | 181.2437 | 1.0514 | 0.7034 | 91.5572 | 32.7212 |
| ModernTCN_slope_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002388 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN_slope_seed101 | receiving_aisle_right_entry | 0.0045 | 0.0106 | 0.0170 | 0.0029 | 0.0075 | 0.3702 | 0.0993 | 0.0000 | 0.0000 | 99.1667 | 50.2500 |
| ModernTCN_slope_seed101 | main_aisle_to_ramp | 0.0026 | 0.0073 | 0.0012 | 0.0378 | 0.0034 | 0.0109 | 0.6890 | 0.7085 | 0.8114 | 96.3000 | 50.3000 |
| ModernTCN_slope_seed101 | extended_uphill_left_ramp_transfer | 0.0825 | 0.1399 | 0.1274 | 0.0202 | 0.0150 | 0.2694 | 0.3938 | 0.4866 | 0.4468 | 100.0000 | 47.9250 |
| ModernTCN_slope_seed101 | upper_pickup_straight | 0.0566 | 0.1473 | 0.0396 | 0.0685 | 0.0535 | 0.3770 | 4.9524 | 1.5582 | 1.5387 | 88.6667 | 0.0000 |
| ModernTCN_slope_seed101 | slope_reversal_right_transfer | 0.5139 | 0.9283 | 0.2198 | 0.0348 | 0.0209 | 0.7896 | 1.4787 | 0.7254 | 0.7825 | 97.5714 | 8.0714 |
| ModernTCN_slope_seed101 | downhill_delivery_aisle | 0.9600 | 1.4668 | 0.4036 | 0.2890 | 0.1386 | 1.6560 | 1902 | 0.8912 | 0.9340 | 90.2222 | 28.0556 |
| ModernTCN_slope_seed101 | shipping_cross_aisle | 0.8328 | 0.8348 | 0.1376 | 0.9557 | 0.0248 | 1.4972 | 0.0040 | 2.4832 | 1.7508 | 53.0833 | 7.9583 |
| ModernTCN_slope_seed101 | dock_approach_straight | 0.8326 | 0.8332 | 0.2134 | 0.8309 | 0.0243 | 0.7442 | 2.697e-09 | 4.2430 | 1.515e-07 | 100.0000 | 0.0000 |
| GRU | all | 2.7028 | 8.4086 | 0.5157 | 0.4358 | 0.0953 | 1.6560 | 1973 | 0.7971 | 0.8080 | 91.6258 | 44.9422 |
| GRU | startup | 0.0000 | 0.0000 | 0.0000 | 0.1311 | 0.0000 | 0.0002388 | 21.1368 | 2.2613 | 2.1716 | 100.0000 | 100.0000 |
| GRU | receiving_aisle_right_entry | 0.2886 | 0.4884 | 0.1344 | 0.0480 | 0.0362 | 1.6256 | 85.6646 | 0.6529 | 0.6981 | 100.0000 | 84.9167 |
| GRU | main_aisle_to_ramp | 0.4614 | 0.7874 | 0.3032 | 0.0856 | 0.2146 | 1.6560 | 2698 | 0.2658 | 0.2282 | 99.2500 | 13.4500 |
| GRU | extended_uphill_left_ramp_transfer | 2.2722 | 3.4984 | 0.1705 | 0.1377 | 0.0446 | 1.4040 | 727.3166 | 0.5656 | 0.5242 | 100.0000 | 13.7750 |
| GRU | upper_pickup_straight | 1.9273 | 2.9783 | 0.8090 | 0.5592 | 0.1197 | 1.6544 | 6485 | 0.9013 | 0.8395 | 74.7500 | 52.4167 |
| GRU | slope_reversal_right_transfer | 5.9536 | 8.4086 | 0.9098 | 0.2730 | 0.0195 | 1.3932 | 112.4303 | 0.3711 | 0.5265 | 97.4286 | 18.2500 |
| GRU | downhill_delivery_aisle | 2.1192 | 4.9757 | 0.8247 | 0.2568 | 0.1463 | 1.6560 | 9646 | 0.3421 | 0.4364 | 93.7778 | 8.0000 |
| GRU | shipping_cross_aisle | 1.2098 | 1.2543 | 0.3882 | 0.9044 | 0.0692 | 1.6560 | 1424 | 0.9468 | 0.9119 | 54.7917 | 84.3333 |
| GRU | dock_approach_straight | 1.2443 | 1.2445 | 0.0793 | 0.8309 | 0.0231 | 0.9355 | 3.711e-09 | 2.5169 | 2.5169 | 100.0000 | 100.0000 |
| TCN | all | 15.4697 | 27.6947 | 0.7977 | 1.1059 | 0.1167 | 1.6560 | 2594 | 1.2770 | 1.4131 | 78.5658 | 54.8150 |
| TCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002388 | 21.0478 | 1.6747 | 0.0000 | 100.0000 | 100.0000 |
| TCN | receiving_aisle_right_entry | 0.0088 | 0.0163 | 0.0156 | 0.0036 | 0.0075 | 0.4474 | 0.6682 | 1.3712 | 0.0119 | 46.5000 | 85.3333 |
| TCN | main_aisle_to_ramp | 0.0201 | 0.0807 | 0.0126 | 0.1238 | 0.0114 | 0.1179 | 0.0233 | 1.1273 | 2.4662 | 76.9000 | 46.0500 |
| TCN | extended_uphill_left_ramp_transfer | 0.8923 | 1.6571 | 0.6818 | 0.1102 | 0.0350 | 1.4193 | 1492 | 1.0845 | 2.9895 | 90.7000 | 47.6500 |
| TCN | upper_pickup_straight | 1.7171 | 2.6684 | 0.5450 | 0.4155 | 0.2451 | 1.6560 | 1.731e+04 | 0.9237 | 0.7203 | 69.9167 | 17.4167 |
| TCN | slope_reversal_right_transfer | 14.2416 | 24.9563 | 1.4091 | 2.6028 | 0.2015 | 1.4400 | 3422 | 0.3724 | 0.5899 | 94.7857 | 16.7857 |
| TCN | downhill_delivery_aisle | 25.8133 | 27.6947 | 1.5246 | 0.7066 | 0.1900 | 1.5699 | 7145 | 3.0741 | 1.7470 | 80.4444 | 4.6111 |
| TCN | shipping_cross_aisle | 27.6912 | 27.6941 | 0.1751 | 0.9557 | 0.0237 | 1.3354 | 8.686e-06 | 1.0515 | 1.7501 | 54.7917 | 100.0000 |
| TCN | dock_approach_straight | 27.6898 | 27.6903 | 0.1471 | 0.8309 | 0.0237 | 1.3342 | 0.0000 | 1.7479 | 1.515e-07 | 100.0000 | 100.0000 |
| ModernTCN_turn_l020_tt25_seed101 | all | 0.0274 | 0.0814 | 0.0358 | 0.0254 | 0.0086 | 0.3509 | 1.1828 | 0.4450 | 0.4760 | 98.1901 | 67.0519 |
| ModernTCN_turn_l020_tt25_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.0988 | 0.0000 | 0.0002388 | 21.0478 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN_turn_l020_tt25_seed101 | receiving_aisle_right_entry | 0.0081 | 0.0250 | 0.0184 | 0.0028 | 0.0079 | 0.3509 | 0.0189 | 0.0000 | 0.0000 | 100.0000 | 74.8333 |
| ModernTCN_turn_l020_tt25_seed101 | main_aisle_to_ramp | 0.0357 | 0.0814 | 0.0127 | 0.0375 | 0.0129 | 0.3082 | 2.3220 | 0.5769 | 0.7032 | 95.9000 | 49.2500 |
| ModernTCN_turn_l020_tt25_seed101 | extended_uphill_left_ramp_transfer | 0.0522 | 0.0786 | 0.0724 | 0.0134 | 0.0100 | 0.1586 | 0.2098 | 0.4078 | 0.4166 | 100.0000 | 14.8500 |
| ModernTCN_turn_l020_tt25_seed101 | upper_pickup_straight | 0.0047 | 0.0133 | 0.0072 | 0.0367 | 0.0099 | 0.0320 | 4.3809 | 0.8541 | 0.7438 | 98.4167 | 69.9167 |
| ModernTCN_turn_l020_tt25_seed101 | slope_reversal_right_transfer | 0.0140 | 0.0222 | 0.0274 | 0.0276 | 0.0081 | 0.3063 | 0.5256 | 0.5578 | 0.6463 | 97.6429 | 89.4286 |
| ModernTCN_turn_l020_tt25_seed101 | downhill_delivery_aisle | 0.0032 | 0.0054 | 0.0008767 | 0.0295 | 0.0034 | 0.0093 | 3.0759 | 0.6672 | 0.7428 | 97.6111 | 83.5000 |
| ModernTCN_turn_l020_tt25_seed101 | shipping_cross_aisle | 0.0009035 | 0.0021 | 0.0003931 | 0.0366 | 0.0027 | 0.0037 | 1.7984 | 0.7750 | 0.7952 | 94.4583 | 100.0000 |
| ModernTCN_turn_l020_tt25_seed101 | dock_approach_straight | 0.0040 | 0.0116 | 0.0054 | 0.0021 | 0.0117 | 0.0315 | 0.0076 | 1.515e-07 | 1.546e-07 | 100.0000 | 78.0000 |
