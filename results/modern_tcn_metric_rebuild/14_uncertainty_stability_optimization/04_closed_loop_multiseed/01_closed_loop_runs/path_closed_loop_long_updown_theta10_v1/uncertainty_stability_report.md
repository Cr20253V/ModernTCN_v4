# Uncertainty stability optimization: path_closed_loop_long_updown_theta10_v1

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_long_updown_theta10_v1\baseline_lock_out.mat`
  - s01_lr13_select_edges_flat_seed21: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\14_uncertainty_stability_optimization\04_closed_loop_multiseed\01_closed_loop_runs\path_closed_loop_long_updown_theta10_v1\s01_lr13_select_edges_flat_seed21_out.mat`
  - s01_lr13_select_edges_flat_seed42: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\14_uncertainty_stability_optimization\04_closed_loop_multiseed\01_closed_loop_runs\path_closed_loop_long_updown_theta10_v1\s01_lr13_select_edges_flat_seed42_out.mat`
  - s01_lr13_select_edges_flat_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\14_uncertainty_stability_optimization\04_closed_loop_multiseed\01_closed_loop_runs\path_closed_loop_long_updown_theta10_v1\s01_lr13_select_edges_flat_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_long_updown_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| s01_lr13_select_edges_flat_seed21 | 8.0000 | 7.0000 | 8.0000 | 23.0000 | 1.0000 |
| baseline_lock | 16.0000 | 5.0000 | 10.0000 | 31.0000 | 2.0000 |
| s01_lr13_select_edges_flat_seed42 | 21.0000 | 8.0000 | 7.0000 | 36.0000 | 3.0000 |
| s01_lr13_select_edges_flat_seed101 | 15.0000 | 10.0000 | 15.0000 | 40.0000 | 4.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0353 | 0.0881 | 0.0438 | 0.0566 | 0.0296 | 0.7594 | 322.8705 | 0.2188 | 7.7862 | 0.0000 | 0.7947 | 1.1614 | 90.9906 | 46.6789 |
| s01_lr13_select_edges_flat_seed21 | 0.0287 | 0.0908 | 0.0282 | 0.0538 | 0.0206 | 0.5161 | 294.2506 | 0.1922 | 15.4444 | 0.0000 | 0.8372 | 1.1305 | 91.6341 | 46.0124 |
| s01_lr13_select_edges_flat_seed42 | 0.0368 | 0.0921 | 0.0453 | 0.0622 | 0.0283 | 0.8172 | 295.3108 | 0.1674 | 5.9864 | 0.0000 | 0.9643 | 1.2923 | 90.7148 | 50.0115 |
| s01_lr13_select_edges_flat_seed101 | 0.0743 | 0.2325 | 0.0328 | 0.0559 | 0.0185 | 0.5915 | 313.3740 | 0.8364 | 19.6485 | 0.0000 | 0.8075 | 1.1410 | 90.2321 | 45.1161 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0210 | 0.0457 | 0.0497 | 0.7124 | 0.0000 |
| s01_lr13_select_edges_flat_seed21 | 0.0255 | 0.0393 | 0.0488 | 3.5943 | 0.0000 |
| s01_lr13_select_edges_flat_seed42 | 0.0246 | 0.0443 | 0.0506 | 0.5448 | 0.0000 |
| s01_lr13_select_edges_flat_seed101 | 0.0231 | 0.0475 | 0.0533 | 0.6316 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| s01_lr13_select_edges_flat_seed21 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| s01_lr13_select_edges_flat_seed42 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| s01_lr13_select_edges_flat_seed101 | 0.0000 | 0.0000 | 0.0230 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | all | 0.0353 | 0.0881 | 0.0438 | 0.0566 | 0.0296 | 0.2188 | 7.7862 | 0.7947 | 1.1614 | 90.9906 | 46.6789 |
| baseline_lock | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| baseline_lock | uphill_long_entry | 0.0299 | 0.0566 | 0.0520 | 0.0739 | 0.0237 | 0.1107 | 12.1779 | 0.9282 | 1.3464 | 88.4615 | 77.6154 |
| baseline_lock | downhill_transition | 0.0302 | 0.0507 | 0.0337 | 0.0474 | 0.0208 | 0.1171 | 5.5542 | 0.8060 | 1.1330 | 93.5385 | 32.3846 |
| baseline_lock | uphill_return | 0.0518 | 0.0881 | 0.0407 | 0.0571 | 0.0304 | 0.1020 | 3.1918 | 0.9406 | 1.4046 | 87.6000 | 28.1000 |
| baseline_lock | flat_recovery | 0.0285 | 0.0521 | 0.0583 | 0.0288 | 0.0565 | 0.2188 | 14.5651 | 0.5255 | 0.8510 | 93.2000 | 13.8000 |
| s01_lr13_select_edges_flat_seed21 | all | 0.0287 | 0.0908 | 0.0282 | 0.0538 | 0.0206 | 0.1922 | 15.4444 | 0.8372 | 1.1305 | 91.6341 | 46.0124 |
| s01_lr13_select_edges_flat_seed21 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| s01_lr13_select_edges_flat_seed21 | uphill_long_entry | 0.0306 | 0.0627 | 0.0396 | 0.0622 | 0.0216 | 0.0961 | 24.2281 | 0.8530 | 1.1270 | 92.1538 | 76.1538 |
| s01_lr13_select_edges_flat_seed21 | downhill_transition | 0.0103 | 0.0267 | 0.0183 | 0.0474 | 0.0185 | 0.1922 | 5.6951 | 0.8031 | 1.1661 | 91.5385 | 31.7692 |
| s01_lr13_select_edges_flat_seed21 | uphill_return | 0.0464 | 0.0908 | 0.0243 | 0.0588 | 0.0196 | 0.0873 | 15.3137 | 1.0834 | 1.3516 | 91.9000 | 33.8000 |
| s01_lr13_select_edges_flat_seed21 | flat_recovery | 0.0126 | 0.0206 | 0.0276 | 0.0435 | 0.0284 | 0.0660 | 25.3204 | 0.8132 | 1.1724 | 85.8000 | 2.2000 |
| s01_lr13_select_edges_flat_seed42 | all | 0.0368 | 0.0921 | 0.0453 | 0.0622 | 0.0283 | 0.1674 | 5.9864 | 0.9643 | 1.2923 | 90.7148 | 50.0115 |
| s01_lr13_select_edges_flat_seed42 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| s01_lr13_select_edges_flat_seed42 | uphill_long_entry | 0.0433 | 0.0864 | 0.0499 | 0.0799 | 0.0160 | 0.0971 | 7.8603 | 1.1943 | 1.5108 | 90.6923 | 78.5385 |
| s01_lr13_select_edges_flat_seed42 | downhill_transition | 0.0189 | 0.0395 | 0.0341 | 0.0482 | 0.0178 | 0.1674 | 6.0033 | 0.8736 | 1.1444 | 96.3077 | 37.6154 |
| s01_lr13_select_edges_flat_seed42 | uphill_return | 0.0504 | 0.0921 | 0.0466 | 0.0715 | 0.0299 | 0.0957 | 6.2547 | 1.3622 | 1.8446 | 89.0000 | 34.9000 |
| s01_lr13_select_edges_flat_seed42 | flat_recovery | 0.0297 | 0.0473 | 0.0635 | 0.0203 | 0.0606 | 0.1653 | 2.8124 | 0.2902 | 0.6525 | 75.2000 | 13.4000 |
| s01_lr13_select_edges_flat_seed101 | all | 0.0743 | 0.2325 | 0.0328 | 0.0559 | 0.0185 | 0.8364 | 19.6485 | 0.8075 | 1.1410 | 90.2321 | 45.1161 |
| s01_lr13_select_edges_flat_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| s01_lr13_select_edges_flat_seed101 | uphill_long_entry | 0.0368 | 0.0740 | 0.0399 | 0.0668 | 0.0191 | 0.0957 | 41.3404 | 0.8907 | 1.2611 | 90.5385 | 76.1538 |
| s01_lr13_select_edges_flat_seed101 | downhill_transition | 0.0127 | 0.0301 | 0.0225 | 0.0445 | 0.0185 | 0.2377 | 7.1547 | 0.7532 | 1.0515 | 93.3077 | 27.1538 |
| s01_lr13_select_edges_flat_seed101 | uphill_return | 0.1034 | 0.2287 | 0.0240 | 0.0651 | 0.0185 | 0.0772 | 11.0200 | 0.9676 | 1.4260 | 81.6000 | 33.3000 |
| s01_lr13_select_edges_flat_seed101 | flat_recovery | 0.1509 | 0.2325 | 0.0526 | 0.0395 | 0.0215 | 0.8364 | 22.2207 | 0.8177 | 1.0642 | 93.8000 | 7.4000 |
