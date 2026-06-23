# Uncertainty seed101 rerun sandbox closed-loop screening

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\02_uncertainty_seed101_rerun_20260622\baseline_lock_out.mat`
  - uncertainty_seed101_rerun_20260622: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\02_uncertainty_seed101_rerun_20260622\uncertainty_seed101_rerun_20260622_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_sharp_turn_transition_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| uncertainty_seed101_rerun_20260622 | 6.0000 | 4.0000 | 6.0000 | 16.0000 | 1.0000 |
| baseline_lock | 12.0000 | 5.0000 | 6.0000 | 23.0000 | 2.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 0.5137 | 224.7044 | 1.3509 | 5.3237 | 0.0000 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| uncertainty_seed101_rerun_20260622 | 0.0292 | 0.0854 | 0.0342 | 0.0319 | 0.0162 | 0.4383 | 224.8288 | 0.2875 | 2.1621 | 0.0000 | 0.4830 | 0.6209 | 91.9821 | 62.7063 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0228 | 0.0352 | 0.0466 | 5.7513 | 0.0000 |
| uncertainty_seed101_rerun_20260622 | 0.0230 | 0.0343 | 0.0470 | 0.4752 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0777 | 0.0000 | 0.0000 |
| uncertainty_seed101_rerun_20260622 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | all | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 1.3509 | 5.3237 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| baseline_lock | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| baseline_lock | uphill_left_transition | 0.0371 | 0.0676 | 0.0542 | 0.0372 | 0.0259 | 0.1441 | 0.9621 | 0.5676 | 0.7060 | 93.9444 | 63.6111 |
| baseline_lock | downhill_right_transition | 0.0200 | 0.0391 | 0.0304 | 0.0299 | 0.0229 | 0.1301 | 3.4855 | 0.5232 | 0.6685 | 96.6000 | 36.9500 |
| baseline_lock | flat_left_exit | 0.0722 | 0.1269 | 0.0421 | 0.0451 | 0.0147 | 1.3509 | 18.4221 | 1.0234 | 1.0628 | 87.5000 | 28.2000 |
| uncertainty_seed101_rerun_20260622 | all | 0.0292 | 0.0854 | 0.0342 | 0.0319 | 0.0162 | 0.2875 | 2.1621 | 0.4830 | 0.6209 | 91.9821 | 62.7063 |
| uncertainty_seed101_rerun_20260622 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| uncertainty_seed101_rerun_20260622 | uphill_left_transition | 0.0479 | 0.0854 | 0.0509 | 0.0392 | 0.0194 | 0.2164 | 1.2078 | 0.6210 | 0.7419 | 93.0000 | 88.2222 |
| uncertainty_seed101_rerun_20260622 | downhill_right_transition | 0.0073 | 0.0237 | 0.0196 | 0.0299 | 0.0136 | 0.1484 | 3.6535 | 0.5072 | 0.6987 | 95.9000 | 48.8000 |
| uncertainty_seed101_rerun_20260622 | flat_left_exit | 0.0122 | 0.0192 | 0.0247 | 0.0224 | 0.0176 | 0.2875 | 1.3455 | 0.3558 | 0.4656 | 79.5000 | 31.6000 |
