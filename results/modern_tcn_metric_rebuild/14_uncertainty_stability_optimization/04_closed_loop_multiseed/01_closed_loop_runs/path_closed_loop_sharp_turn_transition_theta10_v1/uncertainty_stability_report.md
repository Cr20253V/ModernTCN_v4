# Uncertainty stability optimization: path_closed_loop_sharp_turn_transition_theta10_v1

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_sharp_turn_transition_theta10_v1\baseline_lock_out.mat`
  - s01_lr13_select_edges_flat_seed21: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\14_uncertainty_stability_optimization\04_closed_loop_multiseed\01_closed_loop_runs\path_closed_loop_sharp_turn_transition_theta10_v1\s01_lr13_select_edges_flat_seed21_out.mat`
  - s01_lr13_select_edges_flat_seed42: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\14_uncertainty_stability_optimization\04_closed_loop_multiseed\01_closed_loop_runs\path_closed_loop_sharp_turn_transition_theta10_v1\s01_lr13_select_edges_flat_seed42_out.mat`
  - s01_lr13_select_edges_flat_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\14_uncertainty_stability_optimization\04_closed_loop_multiseed\01_closed_loop_runs\path_closed_loop_sharp_turn_transition_theta10_v1\s01_lr13_select_edges_flat_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_sharp_turn_transition_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| s01_lr13_select_edges_flat_seed21 | 9.0000 | 4.0000 | 5.0000 | 18.0000 | 1.0000 |
| s01_lr13_select_edges_flat_seed101 | 11.0000 | 7.0000 | 12.0000 | 30.0000 | 2.0000 |
| baseline_lock | 21.0000 | 8.0000 | 11.0000 | 40.0000 | 3.0000 |
| s01_lr13_select_edges_flat_seed42 | 19.0000 | 11.0000 | 12.0000 | 42.0000 | 4.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 0.5137 | 224.7044 | 1.3509 | 5.3237 | 0.0000 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| s01_lr13_select_edges_flat_seed21 | 0.0205 | 0.0551 | 0.0310 | 0.0323 | 0.0189 | 0.3707 | 223.9922 | 0.1510 | 2.2500 | 0.0000 | 0.5125 | 0.6059 | 94.9524 | 56.6492 |
| s01_lr13_select_edges_flat_seed42 | 0.0311 | 0.0720 | 0.0415 | 0.0396 | 0.0228 | 0.5329 | 226.7725 | 0.4920 | 2.3620 | 0.0000 | 0.6910 | 0.8312 | 92.8752 | 45.8358 |
| s01_lr13_select_edges_flat_seed101 | 0.0322 | 0.0795 | 0.0307 | 0.0297 | 0.0181 | 0.3748 | 226.7435 | 0.1536 | 2.7160 | 0.0000 | 0.4797 | 0.5909 | 92.5063 | 51.1939 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0209 | 0.0226 | 0.0239 | 0.2452 | 0.0000 |
| s01_lr13_select_edges_flat_seed21 | 0.0219 | 0.0438 | 0.0496 | 0.3789 | 0.0000 |
| s01_lr13_select_edges_flat_seed42 | 0.0233 | 0.0291 | 0.0398 | 0.3525 | 0.0000 |
| s01_lr13_select_edges_flat_seed101 | 0.0210 | 0.0325 | 0.0472 | 0.2648 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0777 | 0.0000 | 0.0000 |
| s01_lr13_select_edges_flat_seed21 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| s01_lr13_select_edges_flat_seed42 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| s01_lr13_select_edges_flat_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | all | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 1.3509 | 5.3237 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| baseline_lock | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| baseline_lock | uphill_left_transition | 0.0371 | 0.0676 | 0.0542 | 0.0372 | 0.0259 | 0.1441 | 0.9621 | 0.5676 | 0.7060 | 93.9444 | 63.6111 |
| baseline_lock | downhill_right_transition | 0.0200 | 0.0391 | 0.0304 | 0.0299 | 0.0229 | 0.1301 | 3.4855 | 0.5232 | 0.6685 | 96.6000 | 36.9500 |
| baseline_lock | flat_left_exit | 0.0722 | 0.1269 | 0.0421 | 0.0451 | 0.0147 | 1.3509 | 18.4221 | 1.0234 | 1.0628 | 87.5000 | 28.2000 |
| s01_lr13_select_edges_flat_seed21 | all | 0.0205 | 0.0551 | 0.0310 | 0.0323 | 0.0189 | 0.1510 | 2.2500 | 0.5125 | 0.6059 | 94.9524 | 56.6492 |
| s01_lr13_select_edges_flat_seed21 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| s01_lr13_select_edges_flat_seed21 | uphill_left_transition | 0.0298 | 0.0551 | 0.0486 | 0.0382 | 0.0236 | 0.1427 | 0.7207 | 0.6166 | 0.7241 | 93.8333 | 78.3889 |
| s01_lr13_select_edges_flat_seed21 | downhill_right_transition | 0.0118 | 0.0317 | 0.0163 | 0.0343 | 0.0188 | 0.1510 | 4.3530 | 0.6336 | 0.7703 | 97.7500 | 40.4500 |
| s01_lr13_select_edges_flat_seed21 | flat_left_exit | 0.0172 | 0.0246 | 0.0123 | 0.0137 | 0.0118 | 0.1286 | 1.2762 | 0.2628 | 0.2768 | 89.6000 | 34.8000 |
| s01_lr13_select_edges_flat_seed42 | all | 0.0311 | 0.0720 | 0.0415 | 0.0396 | 0.0228 | 0.4920 | 2.3620 | 0.6910 | 0.8312 | 92.8752 | 45.8358 |
| s01_lr13_select_edges_flat_seed42 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| s01_lr13_select_edges_flat_seed42 | uphill_left_transition | 0.0407 | 0.0720 | 0.0595 | 0.0441 | 0.0278 | 0.1526 | 0.9170 | 0.7967 | 0.9362 | 93.0000 | 52.8889 |
| s01_lr13_select_edges_flat_seed42 | downhill_right_transition | 0.0226 | 0.0572 | 0.0300 | 0.0420 | 0.0217 | 0.1746 | 4.2776 | 0.8510 | 1.0127 | 95.1500 | 35.8500 |
| s01_lr13_select_edges_flat_seed42 | flat_left_exit | 0.0312 | 0.0484 | 0.0269 | 0.0291 | 0.0184 | 0.4920 | 1.6504 | 0.4233 | 0.5711 | 85.6000 | 34.2000 |
| s01_lr13_select_edges_flat_seed101 | all | 0.0322 | 0.0795 | 0.0307 | 0.0297 | 0.0181 | 0.1536 | 2.7160 | 0.4797 | 0.5909 | 92.5063 | 51.1939 |
| s01_lr13_select_edges_flat_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| s01_lr13_select_edges_flat_seed101 | uphill_left_transition | 0.0282 | 0.0542 | 0.0458 | 0.0362 | 0.0218 | 0.1432 | 0.8876 | 0.5841 | 0.7272 | 93.8889 | 63.8333 |
| s01_lr13_select_edges_flat_seed101 | downhill_right_transition | 0.0125 | 0.0306 | 0.0171 | 0.0278 | 0.0188 | 0.1516 | 5.3977 | 0.4988 | 0.6523 | 97.1000 | 36.1000 |
| s01_lr13_select_edges_flat_seed101 | flat_left_exit | 0.0601 | 0.0795 | 0.0223 | 0.0207 | 0.0113 | 0.1536 | 1.2875 | 0.4218 | 0.4301 | 78.2000 | 41.6000 |
