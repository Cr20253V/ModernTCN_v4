# Fair 10-seed closed-loop: path_closed_loop_long_updown_theta10_v1

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_long_updown_theta10_v1\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\06_final_test_closed_loop\path_closed_loop_long_updown_theta10_v1\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\06_final_test_closed_loop\path_closed_loop_long_updown_theta10_v1\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_long_updown_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 10.0000 | 4.0000 | 7.0000 | 21.0000 | 1.0000 |
| uncertainty_weighted_seed101 | 12.0000 | 7.0000 | 7.0000 | 26.0000 | 2.0000 |
| modern_fixed_seed101 | 14.0000 | 7.0000 | 10.0000 | 31.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0353 | 0.0881 | 0.0438 | 0.0566 | 0.0296 | 0.7594 | 322.8705 | 0.2188 | 7.7862 | 0.0000 | 0.7947 | 1.1614 | 90.9906 | 46.6789 |
| modern_fixed_seed101 | 0.0350 | 0.0877 | 0.0461 | 0.0643 | 0.0297 | 0.8045 | 330.6927 | 0.1600 | 17.5881 | 0.0000 | 0.8581 | 1.2839 | 89.4507 | 50.3103 |
| uncertainty_weighted_seed101 | 0.0320 | 0.0880 | 0.0450 | 0.0618 | 0.0310 | 0.7696 | 318.8595 | 0.1543 | 10.4110 | 0.0000 | 0.8170 | 1.2035 | 90.0712 | 42.6569 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0210 | 0.0457 | 0.0497 | 0.7124 | 0.0000 |
| modern_fixed_seed101 | 0.0210 | 0.0230 | 0.0241 | 0.3165 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0212 | 0.0230 | 0.0243 | 0.2459 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0353 | 0.0881 | 0.0438 | 0.0566 | 0.0296 | 0.2188 | 7.7862 | 0.7947 | 1.1614 | 90.9906 | 46.6789 |
| ModernTCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN | uphill_long_entry | 0.0299 | 0.0566 | 0.0520 | 0.0739 | 0.0237 | 0.1107 | 12.1779 | 0.9282 | 1.3464 | 88.4615 | 77.6154 |
| ModernTCN | downhill_transition | 0.0302 | 0.0507 | 0.0337 | 0.0474 | 0.0208 | 0.1171 | 5.5542 | 0.8060 | 1.1330 | 93.5385 | 32.3846 |
| ModernTCN | uphill_return | 0.0518 | 0.0881 | 0.0407 | 0.0571 | 0.0304 | 0.1020 | 3.1918 | 0.9406 | 1.4046 | 87.6000 | 28.1000 |
| ModernTCN | flat_recovery | 0.0285 | 0.0521 | 0.0583 | 0.0288 | 0.0565 | 0.2188 | 14.5651 | 0.5255 | 0.8510 | 93.2000 | 13.8000 |
| modern_fixed_seed101 | all | 0.0350 | 0.0877 | 0.0461 | 0.0643 | 0.0297 | 0.1600 | 17.5881 | 0.8581 | 1.2839 | 89.4507 | 50.3103 |
| modern_fixed_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| modern_fixed_seed101 | uphill_long_entry | 0.0427 | 0.0863 | 0.0590 | 0.0914 | 0.0278 | 0.1270 | 46.4550 | 1.1065 | 1.7969 | 82.0000 | 73.2308 |
| modern_fixed_seed101 | downhill_transition | 0.0171 | 0.0409 | 0.0371 | 0.0511 | 0.0214 | 0.1600 | 5.8896 | 0.9327 | 1.2360 | 93.1538 | 35.4615 |
| modern_fixed_seed101 | uphill_return | 0.0477 | 0.0877 | 0.0395 | 0.0580 | 0.0291 | 0.0982 | 3.3870 | 0.8989 | 1.3441 | 89.0000 | 46.5000 |
| modern_fixed_seed101 | flat_recovery | 0.0242 | 0.0405 | 0.0523 | 0.0184 | 0.0530 | 0.1359 | 9.5187 | 0.3678 | 0.5992 | 94.8000 | 12.2000 |
| uncertainty_weighted_seed101 | all | 0.0320 | 0.0880 | 0.0450 | 0.0618 | 0.0310 | 0.1543 | 10.4110 | 0.8170 | 1.2035 | 90.0712 | 42.6569 |
| uncertainty_weighted_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| uncertainty_weighted_seed101 | uphill_long_entry | 0.0328 | 0.0632 | 0.0585 | 0.0841 | 0.0320 | 0.1543 | 20.3247 | 1.0879 | 1.6177 | 84.5385 | 66.0769 |
| uncertainty_weighted_seed101 | downhill_transition | 0.0187 | 0.0317 | 0.0324 | 0.0516 | 0.0232 | 0.1358 | 7.1533 | 0.7372 | 1.0117 | 93.0769 | 26.0000 |
| uncertainty_weighted_seed101 | uphill_return | 0.0482 | 0.0880 | 0.0411 | 0.0580 | 0.0289 | 0.0962 | 3.0969 | 0.9137 | 1.3846 | 89.0000 | 34.2000 |
| uncertainty_weighted_seed101 | flat_recovery | 0.0238 | 0.0370 | 0.0514 | 0.0280 | 0.0514 | 0.1348 | 12.2656 | 0.5368 | 0.8674 | 93.8000 | 13.4000 |
