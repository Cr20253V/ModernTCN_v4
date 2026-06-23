# Uncertainty replacement qualification: path_closed_loop_sharp_turn_transition_theta10_v1

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_sharp_turn_transition_theta10_v1\baseline_lock_out.mat`
  - ua_seed21: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\12_uncertainty_replacement_qualification\03_closed_loop_representatives\01_closed_loop_runs\path_closed_loop_sharp_turn_transition_theta10_v1\ua_seed21_out.mat`
  - ua_seed42: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\12_uncertainty_replacement_qualification\03_closed_loop_representatives\01_closed_loop_runs\path_closed_loop_sharp_turn_transition_theta10_v1\ua_seed42_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_sharp_turn_transition_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| baseline_lock | 11.0000 | 6.0000 | 8.0000 | 25.0000 | 1.0000 |
| ua_seed21 | 11.0000 | 7.0000 | 8.0000 | 26.0000 | 2.0000 |
| ua_seed42 | 14.0000 | 5.0000 | 8.0000 | 27.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 0.5137 | 224.7044 | 1.3509 | 5.3237 | 0.0000 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| ua_seed21 | 0.0463 | 0.1415 | 0.0402 | 0.0446 | 0.0213 | 0.4375 | 225.2537 | 0.9001 | 3.2187 | 0.0000 | 0.9585 | 0.9750 | 91.1862 | 64.8418 |
| ua_seed42 | 0.0404 | 0.1022 | 0.0590 | 0.0453 | 0.0312 | 0.7373 | 226.1688 | 0.8186 | 2.9716 | 0.0000 | 0.9204 | 0.9945 | 94.5059 | 50.4368 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0209 | 0.0226 | 0.0239 | 0.2452 | 0.0000 |
| ua_seed21 | 0.0212 | 0.0228 | 0.0247 | 0.3159 | 0.0000 |
| ua_seed42 | 0.0247 | 0.0452 | 0.0534 | 0.4763 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0777 | 0.0000 | 0.0000 |
| ua_seed21 | 0.0000 | 0.0000 | 0.0388 | 0.0000 | 0.0000 |
| ua_seed42 | 0.0000 | 0.0000 | 0.0388 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | all | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 1.3509 | 5.3237 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| baseline_lock | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| baseline_lock | uphill_left_transition | 0.0371 | 0.0676 | 0.0542 | 0.0372 | 0.0259 | 0.1441 | 0.9621 | 0.5676 | 0.7060 | 93.9444 | 63.6111 |
| baseline_lock | downhill_right_transition | 0.0200 | 0.0391 | 0.0304 | 0.0299 | 0.0229 | 0.1301 | 3.4855 | 0.5232 | 0.6685 | 96.6000 | 36.9500 |
| baseline_lock | flat_left_exit | 0.0722 | 0.1269 | 0.0421 | 0.0451 | 0.0147 | 1.3509 | 18.4221 | 1.0234 | 1.0628 | 87.5000 | 28.2000 |
| ua_seed21 | all | 0.0463 | 0.1415 | 0.0402 | 0.0446 | 0.0213 | 0.9001 | 3.2187 | 0.9585 | 0.9750 | 91.1862 | 64.8418 |
| ua_seed21 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ua_seed21 | uphill_left_transition | 0.0369 | 0.0704 | 0.0546 | 0.0437 | 0.0261 | 0.1518 | 0.8486 | 0.8359 | 0.9212 | 93.1667 | 84.2222 |
| ua_seed21 | downhill_right_transition | 0.0263 | 0.0580 | 0.0270 | 0.0561 | 0.0206 | 0.1673 | 4.2963 | 1.3012 | 1.4999 | 94.6000 | 48.8500 |
| ua_seed21 | flat_left_exit | 0.0850 | 0.1415 | 0.0384 | 0.0179 | 0.0160 | 0.9001 | 6.1529 | 0.8276 | 0.3642 | 77.7000 | 49.7000 |
| ua_seed42 | all | 0.0404 | 0.1022 | 0.0590 | 0.0453 | 0.0312 | 0.8186 | 2.9716 | 0.9204 | 0.9945 | 94.5059 | 50.4368 |
| ua_seed42 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ua_seed42 | uphill_left_transition | 0.0574 | 0.1022 | 0.0796 | 0.0566 | 0.0348 | 0.2386 | 0.9207 | 1.2836 | 1.3748 | 94.6667 | 73.0556 |
| ua_seed42 | downhill_right_transition | 0.0300 | 0.0630 | 0.0508 | 0.0449 | 0.0337 | 0.2083 | 5.7077 | 0.9374 | 1.0604 | 94.9500 | 35.4500 |
| ua_seed42 | flat_left_exit | 0.0260 | 0.0533 | 0.0367 | 0.0242 | 0.0236 | 0.8186 | 1.9044 | 0.5560 | 0.5276 | 91.4000 | 22.4000 |
