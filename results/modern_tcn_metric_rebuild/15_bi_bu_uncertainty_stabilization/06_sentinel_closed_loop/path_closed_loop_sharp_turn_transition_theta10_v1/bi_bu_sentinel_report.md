# BI-BU sentinel closed-loop: path_closed_loop_sharp_turn_transition_theta10_v1

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\15_bi_bu_uncertainty_stabilization\06_sentinel_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\baseline_lock_out.mat`
  - a2_freeze_early_seed21: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\15_bi_bu_uncertainty_stabilization\06_sentinel_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\a2_freeze_early_seed21_out.mat`
  - a2_freeze_early_seed42: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\15_bi_bu_uncertainty_stabilization\06_sentinel_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\a2_freeze_early_seed42_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_sharp_turn_transition_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| a2_freeze_early_seed21 | 13.0000 | 6.0000 | 6.0000 | 25.0000 | 1.0000 |
| a2_freeze_early_seed42 | 10.0000 | 7.0000 | 8.0000 | 25.0000 | 2.0000 |
| baseline_lock | 13.0000 | 5.0000 | 10.0000 | 28.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 0.5137 | 224.7044 | 1.3509 | 5.3237 | 0.0000 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| a2_freeze_early_seed21 | 0.0560 | 0.1692 | 0.0338 | 0.0363 | 0.0180 | 0.3558 | 223.8523 | 1.1080 | 2.4098 | 0.0000 | 0.6568 | 0.7896 | 93.2634 | 54.9408 |
| a2_freeze_early_seed42 | 0.0413 | 0.1029 | 0.0328 | 0.0397 | 0.0188 | 0.3183 | 224.3162 | 0.8907 | 2.9483 | 0.0000 | 0.6978 | 0.8604 | 91.3803 | 62.3957 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0194 | 0.0214 | 0.0222 | 0.2290 | 0.0000 |
| a2_freeze_early_seed21 | 0.0194 | 0.0214 | 0.0224 | 0.2394 | 0.0000 |
| a2_freeze_early_seed42 | 0.0194 | 0.0217 | 0.0229 | 0.2412 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0777 | 0.0000 | 0.0000 |
| a2_freeze_early_seed21 | 0.0000 | 0.0000 | 0.0388 | 0.0000 | 0.0000 |
| a2_freeze_early_seed42 | 0.0000 | 0.0000 | 0.0194 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | all | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 1.3509 | 5.3237 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| baseline_lock | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| baseline_lock | uphill_left_transition | 0.0371 | 0.0676 | 0.0542 | 0.0372 | 0.0259 | 0.1441 | 0.9621 | 0.5676 | 0.7060 | 93.9444 | 63.6111 |
| baseline_lock | downhill_right_transition | 0.0200 | 0.0391 | 0.0304 | 0.0299 | 0.0229 | 0.1301 | 3.4855 | 0.5232 | 0.6685 | 96.6000 | 36.9500 |
| baseline_lock | flat_left_exit | 0.0722 | 0.1269 | 0.0421 | 0.0451 | 0.0147 | 1.3509 | 18.4221 | 1.0234 | 1.0628 | 87.5000 | 28.2000 |
| a2_freeze_early_seed21 | all | 0.0560 | 0.1692 | 0.0338 | 0.0363 | 0.0180 | 1.1080 | 2.4098 | 0.6568 | 0.7896 | 93.2634 | 54.9408 |
| a2_freeze_early_seed21 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| a2_freeze_early_seed21 | uphill_left_transition | 0.0299 | 0.0572 | 0.0452 | 0.0359 | 0.0218 | 0.1453 | 0.9122 | 0.5669 | 0.7046 | 93.7778 | 72.3333 |
| a2_freeze_early_seed21 | downhill_right_transition | 0.0184 | 0.0459 | 0.0221 | 0.0396 | 0.0192 | 0.1643 | 4.1697 | 0.8438 | 1.0308 | 97.3000 | 36.7000 |
| a2_freeze_early_seed21 | flat_left_exit | 0.1178 | 0.1692 | 0.0354 | 0.0334 | 0.0086 | 1.1080 | 2.1214 | 0.6749 | 0.7372 | 81.9000 | 44.4000 |
| a2_freeze_early_seed42 | all | 0.0413 | 0.1029 | 0.0328 | 0.0397 | 0.0188 | 0.8907 | 2.9483 | 0.6978 | 0.8604 | 91.3803 | 62.3957 |
| a2_freeze_early_seed42 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| a2_freeze_early_seed42 | uphill_left_transition | 0.0239 | 0.0478 | 0.0361 | 0.0348 | 0.0172 | 0.1438 | 1.3241 | 0.6030 | 0.7780 | 94.0000 | 77.9444 |
| a2_freeze_early_seed42 | downhill_right_transition | 0.0428 | 0.0888 | 0.0352 | 0.0448 | 0.0211 | 0.2912 | 5.4972 | 0.9153 | 1.0906 | 95.9500 | 48.2000 |
| a2_freeze_early_seed42 | flat_left_exit | 0.0639 | 0.1029 | 0.0269 | 0.0415 | 0.0201 | 0.8907 | 1.4995 | 0.6786 | 0.8505 | 74.5000 | 49.7000 |
