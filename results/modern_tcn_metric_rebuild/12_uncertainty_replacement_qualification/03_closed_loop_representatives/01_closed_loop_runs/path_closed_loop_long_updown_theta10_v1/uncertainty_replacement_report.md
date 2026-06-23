# Uncertainty replacement qualification: path_closed_loop_long_updown_theta10_v1

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_long_updown_theta10_v1\baseline_lock_out.mat`
  - ua_seed21: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\12_uncertainty_replacement_qualification\03_closed_loop_representatives\01_closed_loop_runs\path_closed_loop_long_updown_theta10_v1\ua_seed21_out.mat`
  - ua_seed42: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\12_uncertainty_replacement_qualification\03_closed_loop_representatives\01_closed_loop_runs\path_closed_loop_long_updown_theta10_v1\ua_seed42_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_long_updown_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| baseline_lock | 8.0000 | 6.0000 | 7.0000 | 21.0000 | 1.0000 |
| ua_seed21 | 12.0000 | 4.0000 | 11.0000 | 27.0000 | 2.0000 |
| ua_seed42 | 16.0000 | 8.0000 | 6.0000 | 30.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0353 | 0.0881 | 0.0438 | 0.0566 | 0.0296 | 0.7594 | 322.8705 | 0.2188 | 7.7862 | 0.0000 | 0.7947 | 1.1614 | 90.9906 | 46.6789 |
| ua_seed21 | 0.0529 | 0.1607 | 0.0381 | 0.0666 | 0.0302 | 0.5636 | 333.1707 | 0.3448 | 11.8016 | 0.0000 | 1.0525 | 1.3901 | 91.5422 | 52.7235 |
| ua_seed42 | 0.0372 | 0.0888 | 0.0516 | 0.0688 | 0.0353 | 0.8974 | 300.6330 | 0.2051 | 3.6148 | 0.0000 | 1.1651 | 1.4420 | 90.3241 | 47.1616 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0210 | 0.0457 | 0.0497 | 0.7124 | 0.0000 |
| ua_seed21 | 0.0213 | 0.0231 | 0.0251 | 0.3944 | 0.0000 |
| ua_seed42 | 0.0214 | 0.0231 | 0.0250 | 0.2610 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| ua_seed21 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| ua_seed42 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | all | 0.0353 | 0.0881 | 0.0438 | 0.0566 | 0.0296 | 0.2188 | 7.7862 | 0.7947 | 1.1614 | 90.9906 | 46.6789 |
| baseline_lock | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| baseline_lock | uphill_long_entry | 0.0299 | 0.0566 | 0.0520 | 0.0739 | 0.0237 | 0.1107 | 12.1779 | 0.9282 | 1.3464 | 88.4615 | 77.6154 |
| baseline_lock | downhill_transition | 0.0302 | 0.0507 | 0.0337 | 0.0474 | 0.0208 | 0.1171 | 5.5542 | 0.8060 | 1.1330 | 93.5385 | 32.3846 |
| baseline_lock | uphill_return | 0.0518 | 0.0881 | 0.0407 | 0.0571 | 0.0304 | 0.1020 | 3.1918 | 0.9406 | 1.4046 | 87.6000 | 28.1000 |
| baseline_lock | flat_recovery | 0.0285 | 0.0521 | 0.0583 | 0.0288 | 0.0565 | 0.2188 | 14.5651 | 0.5255 | 0.8510 | 93.2000 | 13.8000 |
| ua_seed21 | all | 0.0529 | 0.1607 | 0.0381 | 0.0666 | 0.0302 | 0.3448 | 11.8016 | 1.0525 | 1.3901 | 91.5422 | 52.7235 |
| ua_seed21 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ua_seed21 | uphill_long_entry | 0.0337 | 0.0674 | 0.0510 | 0.0776 | 0.0326 | 0.1397 | 18.9686 | 0.9340 | 1.3814 | 89.8462 | 82.1538 |
| ua_seed21 | downhill_transition | 0.0170 | 0.0373 | 0.0290 | 0.0638 | 0.0335 | 0.2535 | 6.0015 | 1.3494 | 1.6353 | 94.3077 | 31.3077 |
| ua_seed21 | uphill_return | 0.0833 | 0.1607 | 0.0239 | 0.0696 | 0.0187 | 0.0767 | 9.0758 | 1.1466 | 1.5101 | 89.4000 | 50.2000 |
| ua_seed21 | flat_recovery | 0.0825 | 0.1596 | 0.0504 | 0.0470 | 0.0392 | 0.3448 | 18.9451 | 0.9287 | 1.2330 | 88.8000 | 13.4000 |
| ua_seed42 | all | 0.0372 | 0.0888 | 0.0516 | 0.0688 | 0.0353 | 0.2051 | 3.6148 | 1.1651 | 1.4420 | 90.3241 | 47.1616 |
| ua_seed42 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ua_seed42 | uphill_long_entry | 0.0429 | 0.0888 | 0.0592 | 0.0929 | 0.0270 | 0.1332 | 2.7572 | 1.6442 | 1.8865 | 94.7692 | 78.3077 |
| ua_seed42 | downhill_transition | 0.0221 | 0.0490 | 0.0426 | 0.0584 | 0.0275 | 0.1837 | 2.6467 | 0.9978 | 1.2855 | 89.3077 | 24.8462 |
| ua_seed42 | uphill_return | 0.0491 | 0.0878 | 0.0469 | 0.0645 | 0.0330 | 0.1172 | 3.3482 | 1.3134 | 1.7029 | 89.0000 | 39.4000 |
| ua_seed42 | flat_recovery | 0.0338 | 0.0537 | 0.0704 | 0.0325 | 0.0694 | 0.2051 | 9.9805 | 0.6425 | 0.8951 | 79.2000 | 13.4000 |
