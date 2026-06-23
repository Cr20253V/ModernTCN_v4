# Strict GRU/TCN validation: path_closed_loop_sharp_turn_transition_theta10_v1

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_sharp_turn_transition_theta10_v1\baseline_lock_out.mat`
  - GRU: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\09_strict_gru_tcn_validation\path_closed_loop_sharp_turn_transition_theta10_v1\GRU_seed101_out.mat`
  - TCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\09_strict_gru_tcn_validation\path_closed_loop_sharp_turn_transition_theta10_v1\TCN_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_sharp_turn_transition_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| baseline_lock | 7.0000 | 5.0000 | 7.0000 | 19.0000 | 1.0000 |
| GRU | 11.0000 | 5.0000 | 5.0000 | 21.0000 | 2.0000 |
| TCN | 18.0000 | 8.0000 | 12.0000 | 38.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 0.5137 | 224.7044 | 1.3509 | 5.3237 | 0.0000 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| GRU | 0.0718 | 0.2121 | 0.0422 | 0.0406 | 0.0238 | 0.3252 | 223.5488 | 0.7953 | 5.2417 | 0.0000 | 0.6323 | 0.7266 | 92.7393 | 71.0542 |
| TCN | 0.1899 | 0.3605 | 0.1515 | 0.0936 | 0.0588 | 1.6943 | 354.5615 | 1.4651 | 36.6960 | 0.0000 | 0.8689 | 1.6763 | 79.3438 | 61.8715 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0209 | 0.0226 | 0.0239 | 0.2452 | 0.0000 |
| GRU | 0.0127 | 0.0210 | 0.0232 | 0.1401 | 0.0000 |
| TCN | 0.0094 | 0.0125 | 0.0173 | 0.1197 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0777 | 0.0000 | 0.0000 |
| GRU | 0.0000 | 0.0000 | 0.0194 | 0.0000 | 0.0000 |
| TCN | 0.0000 | 0.0000 | 0.3494 | 0.0971 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | all | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 1.3509 | 5.3237 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| baseline_lock | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| baseline_lock | uphill_left_transition | 0.0371 | 0.0676 | 0.0542 | 0.0372 | 0.0259 | 0.1441 | 0.9621 | 0.5676 | 0.7060 | 93.9444 | 63.6111 |
| baseline_lock | downhill_right_transition | 0.0200 | 0.0391 | 0.0304 | 0.0299 | 0.0229 | 0.1301 | 3.4855 | 0.5232 | 0.6685 | 96.6000 | 36.9500 |
| baseline_lock | flat_left_exit | 0.0722 | 0.1269 | 0.0421 | 0.0451 | 0.0147 | 1.3509 | 18.4221 | 1.0234 | 1.0628 | 87.5000 | 28.2000 |
| GRU | all | 0.0718 | 0.2121 | 0.0422 | 0.0406 | 0.0238 | 0.7953 | 5.2417 | 0.6323 | 0.7266 | 92.7393 | 71.0542 |
| GRU | startup | 0.0000 | 0.0000 | 0.0000 | 0.1833 | 0.0000 | 0.0002457 | 66.5816 | 1.2893 | 1.0357 | 100.0000 | 100.0000 |
| GRU | uphill_left_transition | 0.0310 | 0.0593 | 0.0118 | 0.0323 | 0.0084 | 0.1666 | 0.0750 | 0.5174 | 0.5662 | 94.7778 | 82.1111 |
| GRU | downhill_right_transition | 0.1068 | 0.2121 | 0.0578 | 0.0458 | 0.0193 | 0.4274 | 12.9631 | 0.6392 | 0.8376 | 95.0000 | 66.7500 |
| GRU | flat_left_exit | 0.0448 | 0.0786 | 0.0475 | 0.0327 | 0.0452 | 0.7953 | 0.5438 | 0.5313 | 0.6344 | 82.0000 | 49.7000 |
| TCN | all | 0.1899 | 0.3605 | 0.1515 | 0.0936 | 0.0588 | 1.4651 | 36.6960 | 0.8689 | 1.6763 | 79.3438 | 61.8715 |
| TCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.7888 | 0.0000 | 100.0000 | 100.0000 |
| TCN | uphill_left_transition | 0.1719 | 0.3301 | 0.1424 | 0.1222 | 0.0281 | 0.5567 | 59.8308 | 0.9849 | 2.6025 | 81.0000 | 81.2778 |
| TCN | downhill_right_transition | 0.1886 | 0.3605 | 0.1691 | 0.0934 | 0.0757 | 0.7489 | 27.8290 | 0.9157 | 1.8197 | 78.4500 | 45.5000 |
| TCN | flat_left_exit | 0.2480 | 0.3469 | 0.1565 | 0.0252 | 0.0701 | 1.4651 | 25.4264 | 0.5550 | 0.3108 | 71.0000 | 46.4000 |
