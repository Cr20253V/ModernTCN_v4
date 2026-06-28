# ModernTCN small base recipe: path_closed_loop_long_updown_theta10_v1

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_long_updown_theta10_v1\baseline_lock_out.mat`
  - modern_base_seed21: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\16_recipe_vs_deployment_comparison\09_modern_base_closed_loop\01_closed_loop_runs\path_closed_loop_long_updown_theta10_v1\modern_base_seed21_out.mat`
  - modern_base_seed42: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\16_recipe_vs_deployment_comparison\09_modern_base_closed_loop\01_closed_loop_runs\path_closed_loop_long_updown_theta10_v1\modern_base_seed42_out.mat`
  - modern_base_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\16_recipe_vs_deployment_comparison\09_modern_base_closed_loop\01_closed_loop_runs\path_closed_loop_long_updown_theta10_v1\modern_base_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_long_updown_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| baseline_lock | 9.0000 | 7.0000 | 10.0000 | 26.0000 | 1.0000 |
| modern_base_seed21 | 13.0000 | 7.0000 | 6.0000 | 26.0000 | 2.0000 |
| modern_base_seed42 | 18.0000 | 7.0000 | 10.0000 | 35.0000 | 3.0000 |
| modern_base_seed101 | 20.0000 | 9.0000 | 14.0000 | 43.0000 | 4.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0353 | 0.0881 | 0.0438 | 0.0566 | 0.0296 | 0.7594 | 322.8705 | 0.2188 | 7.7862 | 0.0000 | 0.7947 | 1.1614 | 90.9906 | 46.6789 |
| modern_base_seed21 | 0.0370 | 0.0924 | 0.0441 | 0.0602 | 0.0290 | 0.7805 | 317.4525 | 0.1918 | 6.3862 | 0.0000 | 0.8259 | 1.1992 | 90.4849 | 48.4946 |
| modern_base_seed42 | 0.0498 | 0.1538 | 0.0429 | 0.0688 | 0.0263 | 0.9004 | 285.3875 | 0.4803 | 6.8025 | 0.0000 | 1.1956 | 1.5048 | 91.9329 | 47.5523 |
| modern_base_seed101 | 0.0474 | 0.1400 | 0.0467 | 0.0604 | 0.0298 | 0.8904 | 325.8510 | 0.4594 | 7.0138 | 0.0000 | 0.9037 | 1.2331 | 91.7950 | 43.6222 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0210 | 0.0457 | 0.0497 | 0.7124 | 0.0000 |
| modern_base_seed21 | 0.0238 | 0.0342 | 0.0475 | 0.5474 | 0.0000 |
| modern_base_seed42 | 0.0240 | 0.0338 | 0.0444 | 0.3955 | 0.0000 |
| modern_base_seed101 | 0.0243 | 0.0345 | 0.0454 | 0.2749 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_base_seed21 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_base_seed42 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_base_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | all | 0.0353 | 0.0881 | 0.0438 | 0.0566 | 0.0296 | 0.2188 | 7.7862 | 0.7947 | 1.1614 | 90.9906 | 46.6789 |
| baseline_lock | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| baseline_lock | uphill_long_entry | 0.0299 | 0.0566 | 0.0520 | 0.0739 | 0.0237 | 0.1107 | 12.1779 | 0.9282 | 1.3464 | 88.4615 | 77.6154 |
| baseline_lock | downhill_transition | 0.0302 | 0.0507 | 0.0337 | 0.0474 | 0.0208 | 0.1171 | 5.5542 | 0.8060 | 1.1330 | 93.5385 | 32.3846 |
| baseline_lock | uphill_return | 0.0518 | 0.0881 | 0.0407 | 0.0571 | 0.0304 | 0.1020 | 3.1918 | 0.9406 | 1.4046 | 87.6000 | 28.1000 |
| baseline_lock | flat_recovery | 0.0285 | 0.0521 | 0.0583 | 0.0288 | 0.0565 | 0.2188 | 14.5651 | 0.5255 | 0.8510 | 93.2000 | 13.8000 |
| modern_base_seed21 | all | 0.0370 | 0.0924 | 0.0441 | 0.0602 | 0.0290 | 0.1918 | 6.3862 | 0.8259 | 1.1992 | 90.4849 | 48.4946 |
| modern_base_seed21 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| modern_base_seed21 | uphill_long_entry | 0.0459 | 0.0924 | 0.0527 | 0.0830 | 0.0200 | 0.1119 | 9.2778 | 1.1305 | 1.5717 | 88.2308 | 68.7692 |
| modern_base_seed21 | downhill_transition | 0.0186 | 0.0349 | 0.0340 | 0.0454 | 0.0208 | 0.1839 | 5.5124 | 0.7160 | 1.0274 | 93.7692 | 46.5385 |
| modern_base_seed21 | uphill_return | 0.0491 | 0.0891 | 0.0416 | 0.0586 | 0.0311 | 0.0875 | 3.5569 | 0.9384 | 1.3997 | 89.0000 | 31.1000 |
| modern_base_seed21 | flat_recovery | 0.0269 | 0.0461 | 0.0569 | 0.0304 | 0.0570 | 0.1918 | 9.2870 | 0.5095 | 0.8784 | 86.0000 | 9.8000 |
| modern_base_seed42 | all | 0.0498 | 0.1538 | 0.0429 | 0.0688 | 0.0263 | 0.4803 | 6.8025 | 1.1956 | 1.5048 | 91.9329 | 47.5523 |
| modern_base_seed42 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| modern_base_seed42 | uphill_long_entry | 0.0427 | 0.0888 | 0.0453 | 0.0694 | 0.0214 | 0.0942 | 5.3952 | 1.2123 | 1.4968 | 91.6923 | 75.9231 |
| modern_base_seed42 | downhill_transition | 0.0214 | 0.0330 | 0.0348 | 0.0512 | 0.0203 | 0.2455 | 5.7919 | 0.8172 | 1.0673 | 92.7692 | 26.5385 |
| modern_base_seed42 | uphill_return | 0.0657 | 0.1430 | 0.0410 | 0.0964 | 0.0267 | 0.0896 | 4.1392 | 2.0439 | 2.4778 | 89.0000 | 42.0000 |
| modern_base_seed42 | flat_recovery | 0.0838 | 0.1538 | 0.0648 | 0.0535 | 0.0483 | 0.4803 | 21.1323 | 1.0400 | 1.4723 | 92.2000 | 13.4000 |
| modern_base_seed101 | all | 0.0474 | 0.1400 | 0.0467 | 0.0604 | 0.0298 | 0.4594 | 7.0138 | 0.9037 | 1.2331 | 91.7950 | 43.6222 |
| modern_base_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| modern_base_seed101 | uphill_long_entry | 0.0336 | 0.0640 | 0.0552 | 0.0761 | 0.0245 | 0.1256 | 9.2516 | 1.1363 | 1.5131 | 87.2308 | 80.6154 |
| modern_base_seed101 | downhill_transition | 0.0327 | 0.0538 | 0.0367 | 0.0479 | 0.0189 | 0.1267 | 7.4058 | 0.7087 | 0.9609 | 96.4615 | 27.6923 |
| modern_base_seed101 | uphill_return | 0.0642 | 0.1314 | 0.0372 | 0.0701 | 0.0300 | 0.0882 | 3.1923 | 1.3125 | 1.8112 | 87.7000 | 17.3000 |
| modern_base_seed101 | flat_recovery | 0.0749 | 0.1400 | 0.0694 | 0.0220 | 0.0585 | 0.4594 | 10.6317 | 0.4423 | 0.6758 | 95.6000 | 13.4000 |
