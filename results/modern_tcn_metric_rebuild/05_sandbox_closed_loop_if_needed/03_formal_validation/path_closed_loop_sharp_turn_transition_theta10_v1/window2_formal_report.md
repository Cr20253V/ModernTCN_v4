# Window 2 formal validation: path_closed_loop_sharp_turn_transition_theta10_v1

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_sharp_turn_transition_theta10_v1\baseline_lock_out.mat`
  - uncertainty_seed101_rerun_20260622: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_sharp_turn_transition_theta10_v1\uncertainty_seed101_rerun_20260622_out.mat`
  - mode_theta_detach_flatreg001_seed21_rerun_20260622: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_sharp_turn_transition_theta10_v1\mode_theta_detach_flatreg001_seed21_rerun_20260622_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_sharp_turn_transition_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | 7.0000 | 4.0000 | 8.0000 | 19.0000 | 1.0000 |
| uncertainty_seed101_rerun_20260622 | 11.0000 | 6.0000 | 7.0000 | 24.0000 | 2.0000 |
| baseline_lock | 18.0000 | 8.0000 | 9.0000 | 35.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 0.5137 | 224.7044 | 1.3509 | 5.3237 | 0.0000 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| uncertainty_seed101_rerun_20260622 | 0.0292 | 0.0854 | 0.0342 | 0.0319 | 0.0162 | 0.4383 | 224.8288 | 0.2875 | 2.1621 | 0.0000 | 0.4830 | 0.6209 | 91.9821 | 62.7063 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | 0.0281 | 0.0573 | 0.0224 | 0.0335 | 0.0124 | 0.3120 | 223.9981 | 0.4453 | 2.4412 | 0.0000 | 0.5636 | 0.6442 | 96.0396 | 70.0835 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0209 | 0.0226 | 0.0239 | 0.2452 | 0.0000 |
| uncertainty_seed101_rerun_20260622 | 0.0209 | 0.0224 | 0.0236 | 0.2436 | 0.0000 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | 0.0425 | 0.0459 | 0.0482 | 0.2555 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0777 | 0.0000 | 0.0000 |
| uncertainty_seed101_rerun_20260622 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

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
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | all | 0.0281 | 0.0573 | 0.0224 | 0.0335 | 0.0124 | 0.4453 | 2.4412 | 0.5636 | 0.6442 | 96.0396 | 70.0835 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | uphill_left_transition | 0.0327 | 0.0573 | 0.0353 | 0.0365 | 0.0148 | 0.2242 | 1.1683 | 0.6969 | 0.7960 | 94.8889 | 76.0556 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | downhill_right_transition | 0.0247 | 0.0509 | 0.0090 | 0.0387 | 0.0109 | 0.1721 | 4.2794 | 0.6179 | 0.8076 | 95.8500 | 71.6500 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | flat_left_exit | 0.0302 | 0.0395 | 0.0136 | 0.0133 | 0.0126 | 0.4453 | 1.6029 | 0.4127 | 0.2706 | 97.1000 | 45.7000 |
