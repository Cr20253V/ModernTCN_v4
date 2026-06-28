# BI-BU sentinel closed-loop: path_closed_loop_long_updown_theta10_v1

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\15_bi_bu_uncertainty_stabilization\06_sentinel_closed_loop\path_closed_loop_long_updown_theta10_v1\baseline_lock_out.mat`
  - a2_freeze_early_seed21: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\15_bi_bu_uncertainty_stabilization\06_sentinel_closed_loop\path_closed_loop_long_updown_theta10_v1\a2_freeze_early_seed21_out.mat`
  - a2_freeze_early_seed42: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\15_bi_bu_uncertainty_stabilization\06_sentinel_closed_loop\path_closed_loop_long_updown_theta10_v1\a2_freeze_early_seed42_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_long_updown_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| a2_freeze_early_seed42 | 7.0000 | 7.0000 | 8.0000 | 22.0000 | 1.0000 |
| baseline_lock | 15.0000 | 4.0000 | 6.0000 | 25.0000 | 2.0000 |
| a2_freeze_early_seed21 | 14.0000 | 7.0000 | 10.0000 | 31.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0353 | 0.0881 | 0.0438 | 0.0566 | 0.0296 | 0.7594 | 322.8705 | 0.2188 | 7.7862 | 0.0000 | 0.7947 | 1.1614 | 90.9906 | 46.6789 |
| a2_freeze_early_seed21 | 0.0348 | 0.1197 | 0.0354 | 0.0662 | 0.0282 | 0.5315 | 367.3490 | 0.2038 | 46.5680 | 0.0000 | 0.9970 | 1.4471 | 87.2903 | 47.3914 |
| a2_freeze_early_seed42 | 0.0208 | 0.0549 | 0.0259 | 0.0616 | 0.0186 | 0.4182 | 349.7414 | 0.1855 | 33.7538 | 0.0000 | 0.9441 | 1.3713 | 88.3015 | 46.2652 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0202 | 0.0224 | 0.0254 | 0.3574 | 0.0000 |
| a2_freeze_early_seed21 | 0.0196 | 0.0223 | 0.0235 | 0.2695 | 0.0000 |
| a2_freeze_early_seed42 | 0.0193 | 0.0216 | 0.0227 | 0.3017 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| a2_freeze_early_seed21 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| a2_freeze_early_seed42 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | all | 0.0353 | 0.0881 | 0.0438 | 0.0566 | 0.0296 | 0.2188 | 7.7862 | 0.7947 | 1.1614 | 90.9906 | 46.6789 |
| baseline_lock | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| baseline_lock | uphill_long_entry | 0.0299 | 0.0566 | 0.0520 | 0.0739 | 0.0237 | 0.1107 | 12.1779 | 0.9282 | 1.3464 | 88.4615 | 77.6154 |
| baseline_lock | downhill_transition | 0.0302 | 0.0507 | 0.0337 | 0.0474 | 0.0208 | 0.1171 | 5.5542 | 0.8060 | 1.1330 | 93.5385 | 32.3846 |
| baseline_lock | uphill_return | 0.0518 | 0.0881 | 0.0407 | 0.0571 | 0.0304 | 0.1020 | 3.1918 | 0.9406 | 1.4046 | 87.6000 | 28.1000 |
| baseline_lock | flat_recovery | 0.0285 | 0.0521 | 0.0583 | 0.0288 | 0.0565 | 0.2188 | 14.5651 | 0.5255 | 0.8510 | 93.2000 | 13.8000 |
| a2_freeze_early_seed21 | all | 0.0348 | 0.1197 | 0.0354 | 0.0662 | 0.0282 | 0.2038 | 46.5680 | 0.9970 | 1.4471 | 87.2903 | 47.3914 |
| a2_freeze_early_seed21 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| a2_freeze_early_seed21 | uphill_long_entry | 0.0277 | 0.0539 | 0.0497 | 0.0737 | 0.0308 | 0.1288 | 83.7798 | 0.9109 | 1.4414 | 87.3846 | 67.9231 |
| a2_freeze_early_seed21 | downhill_transition | 0.0133 | 0.0254 | 0.0235 | 0.0585 | 0.0280 | 0.1855 | 6.8157 | 1.2032 | 1.4889 | 92.0000 | 31.6923 |
| a2_freeze_early_seed21 | uphill_return | 0.0520 | 0.1197 | 0.0198 | 0.0793 | 0.0198 | 0.0443 | 73.9923 | 1.1250 | 1.8528 | 74.4000 | 45.0000 |
| a2_freeze_early_seed21 | flat_recovery | 0.0519 | 0.1146 | 0.0474 | 0.0454 | 0.0402 | 0.2038 | 21.2184 | 0.9290 | 1.2685 | 94.2000 | 13.4000 |
| a2_freeze_early_seed42 | all | 0.0208 | 0.0549 | 0.0259 | 0.0616 | 0.0186 | 0.1855 | 33.7538 | 0.9441 | 1.3713 | 88.3015 | 46.2652 |
| a2_freeze_early_seed42 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| a2_freeze_early_seed42 | uphill_long_entry | 0.0284 | 0.0549 | 0.0383 | 0.0663 | 0.0211 | 0.1000 | 53.9490 | 0.8795 | 1.3667 | 88.8462 | 80.0000 |
| a2_freeze_early_seed42 | downhill_transition | 0.0198 | 0.0368 | 0.0131 | 0.0584 | 0.0171 | 0.1855 | 9.0371 | 1.1960 | 1.4602 | 91.8462 | 27.6923 |
| a2_freeze_early_seed42 | uphill_return | 0.0142 | 0.0295 | 0.0236 | 0.0709 | 0.0151 | 0.1004 | 49.7656 | 0.8982 | 1.6661 | 76.6000 | 30.5000 |
| a2_freeze_early_seed42 | flat_recovery | 0.0157 | 0.0286 | 0.0220 | 0.0472 | 0.0253 | 0.1005 | 29.8854 | 1.0230 | 1.2508 | 95.2000 | 11.6000 |
