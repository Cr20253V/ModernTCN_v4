# Uncertainty tuning Top5: path_closed_loop_long_updown_theta10_v1

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_long_updown_theta10_v1\baseline_lock_out.mat`
  - u06_lr0013_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\01_closed_loop_runs\path_closed_loop_long_updown_theta10_v1\u06_lr0013_seed101_out.mat`
  - u04_lwlr0030_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\01_closed_loop_runs\path_closed_loop_long_updown_theta10_v1\u04_lwlr0030_seed101_out.mat`
  - u17_ltheta050_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\01_closed_loop_runs\path_closed_loop_long_updown_theta10_v1\u17_ltheta050_seed101_out.mat`
  - u23_turn_protect_mix_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\01_closed_loop_runs\path_closed_loop_long_updown_theta10_v1\u23_turn_protect_mix_seed101_out.mat`
  - u18_ltheta065_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\01_closed_loop_runs\path_closed_loop_long_updown_theta10_v1\u18_ltheta065_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_long_updown_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| baseline_lock | 12.0000 | 5.0000 | 9.0000 | 26.0000 | 1.0000 |
| u06_lr0013_seed101 | 19.0000 | 5.0000 | 12.0000 | 36.0000 | 2.0000 |
| u23_turn_protect_mix_seed101 | 12.0000 | 10.0000 | 16.0000 | 38.0000 | 3.0000 |
| u18_ltheta065_seed101 | 17.0000 | 14.0000 | 20.0000 | 51.0000 | 4.0000 |
| u04_lwlr0030_seed101 | 31.0000 | 12.0000 | 11.0000 | 54.0000 | 5.0000 |
| u17_ltheta050_seed101 | 35.0000 | 17.0000 | 16.0000 | 68.0000 | 6.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0353 | 0.0881 | 0.0438 | 0.0566 | 0.0296 | 0.7594 | 322.8705 | 0.2188 | 7.7862 | 0.0000 | 0.7947 | 1.1614 | 90.9906 | 46.6789 |
| u06_lr0013_seed101 | 0.0467 | 0.1377 | 0.0449 | 0.0607 | 0.0296 | 0.8655 | 322.3060 | 0.3450 | 19.6441 | 0.0000 | 0.9177 | 1.2689 | 91.8869 | 48.6325 |
| u04_lwlr0030_seed101 | 0.0581 | 0.1871 | 0.0562 | 0.0744 | 0.0384 | 0.9797 | 308.6122 | 0.5613 | 6.9502 | 0.0000 | 1.1140 | 1.4335 | 88.2556 | 45.2080 |
| u17_ltheta050_seed101 | 0.0597 | 0.1411 | 0.0596 | 0.0753 | 0.0431 | 0.9832 | 326.7331 | 0.4389 | 15.0217 | 0.0000 | 1.1148 | 1.4928 | 87.7499 | 34.7736 |
| u23_turn_protect_mix_seed101 | 0.0312 | 0.0877 | 0.0430 | 0.0616 | 0.0314 | 0.7094 | 343.8762 | 0.1952 | 26.0256 | 0.0000 | 0.8019 | 1.2804 | 88.5084 | 37.2558 |
| u18_ltheta065_seed101 | 0.0280 | 0.0724 | 0.0484 | 0.0663 | 0.0372 | 0.7595 | 350.5474 | 0.2105 | 27.4300 | 0.0000 | 0.9289 | 1.3825 | 86.6927 | 42.0133 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0210 | 0.0457 | 0.0497 | 0.7124 | 0.0000 |
| u06_lr0013_seed101 | 0.0212 | 0.0256 | 0.0355 | 0.4273 | 0.0000 |
| u04_lwlr0030_seed101 | 0.0212 | 0.0232 | 0.0298 | 0.3198 | 0.0000 |
| u17_ltheta050_seed101 | 0.0213 | 0.0238 | 0.0324 | 0.2485 | 0.0000 |
| u23_turn_protect_mix_seed101 | 0.0213 | 0.0246 | 0.0331 | 0.2636 | 0.0000 |
| u18_ltheta065_seed101 | 0.0215 | 0.0263 | 0.0425 | 0.2803 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| u06_lr0013_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| u04_lwlr0030_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| u17_ltheta050_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| u23_turn_protect_mix_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| u18_ltheta065_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | all | 0.0353 | 0.0881 | 0.0438 | 0.0566 | 0.0296 | 0.2188 | 7.7862 | 0.7947 | 1.1614 | 90.9906 | 46.6789 |
| baseline_lock | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| baseline_lock | uphill_long_entry | 0.0299 | 0.0566 | 0.0520 | 0.0739 | 0.0237 | 0.1107 | 12.1779 | 0.9282 | 1.3464 | 88.4615 | 77.6154 |
| baseline_lock | downhill_transition | 0.0302 | 0.0507 | 0.0337 | 0.0474 | 0.0208 | 0.1171 | 5.5542 | 0.8060 | 1.1330 | 93.5385 | 32.3846 |
| baseline_lock | uphill_return | 0.0518 | 0.0881 | 0.0407 | 0.0571 | 0.0304 | 0.1020 | 3.1918 | 0.9406 | 1.4046 | 87.6000 | 28.1000 |
| baseline_lock | flat_recovery | 0.0285 | 0.0521 | 0.0583 | 0.0288 | 0.0565 | 0.2188 | 14.5651 | 0.5255 | 0.8510 | 93.2000 | 13.8000 |
| u06_lr0013_seed101 | all | 0.0467 | 0.1377 | 0.0449 | 0.0607 | 0.0296 | 0.3450 | 19.6441 | 0.9177 | 1.2689 | 91.8869 | 48.6325 |
| u06_lr0013_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| u06_lr0013_seed101 | uphill_long_entry | 0.0444 | 0.0891 | 0.0499 | 0.0764 | 0.0235 | 0.1054 | 52.7576 | 1.0543 | 1.4806 | 90.6154 | 81.0000 |
| u06_lr0013_seed101 | downhill_transition | 0.0224 | 0.0358 | 0.0377 | 0.0438 | 0.0247 | 0.2490 | 4.8744 | 0.6617 | 0.9536 | 94.3077 | 26.7692 |
| u06_lr0013_seed101 | uphill_return | 0.0597 | 0.1253 | 0.0368 | 0.0706 | 0.0272 | 0.1008 | 3.4315 | 1.3914 | 1.8528 | 89.0000 | 39.8000 |
| u06_lr0013_seed101 | flat_recovery | 0.0736 | 0.1377 | 0.0682 | 0.0382 | 0.0560 | 0.3450 | 13.5878 | 0.7412 | 1.0077 | 90.6000 | 13.4000 |
| u04_lwlr0030_seed101 | all | 0.0581 | 0.1871 | 0.0562 | 0.0744 | 0.0384 | 0.5613 | 6.9502 | 1.1140 | 1.4335 | 88.2556 | 45.2080 |
| u04_lwlr0030_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| u04_lwlr0030_seed101 | uphill_long_entry | 0.0526 | 0.1009 | 0.0675 | 0.1057 | 0.0351 | 0.1669 | 10.8388 | 1.7478 | 2.0281 | 80.8462 | 79.2308 |
| u04_lwlr0030_seed101 | downhill_transition | 0.0285 | 0.0583 | 0.0506 | 0.0502 | 0.0387 | 0.1723 | 2.5224 | 0.6629 | 1.0079 | 91.1538 | 31.3077 |
| u04_lwlr0030_seed101 | uphill_return | 0.0680 | 0.1794 | 0.0390 | 0.0739 | 0.0351 | 0.1252 | 3.4670 | 1.3621 | 1.8202 | 89.0000 | 21.3000 |
| u04_lwlr0030_seed101 | flat_recovery | 0.1040 | 0.1871 | 0.0769 | 0.0352 | 0.0572 | 0.5613 | 18.1038 | 0.7021 | 0.9398 | 92.6000 | 13.4000 |
| u17_ltheta050_seed101 | all | 0.0597 | 0.1411 | 0.0596 | 0.0753 | 0.0431 | 0.4389 | 15.0217 | 1.1148 | 1.4928 | 87.7499 | 34.7736 |
| u17_ltheta050_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| u17_ltheta050_seed101 | uphill_long_entry | 0.0521 | 0.1042 | 0.0758 | 0.1098 | 0.0424 | 0.2319 | 27.5618 | 1.6442 | 2.1620 | 79.4615 | 70.3846 |
| u17_ltheta050_seed101 | downhill_transition | 0.0648 | 0.1383 | 0.0562 | 0.0499 | 0.0482 | 0.2810 | 12.1546 | 0.7945 | 1.0977 | 91.6923 | 17.4615 |
| u17_ltheta050_seed101 | uphill_return | 0.0611 | 0.1317 | 0.0429 | 0.0701 | 0.0401 | 0.1651 | 3.4937 | 1.2695 | 1.7302 | 86.9000 | 10.3000 |
| u17_ltheta050_seed101 | flat_recovery | 0.0749 | 0.1411 | 0.0636 | 0.0361 | 0.0471 | 0.4389 | 19.7933 | 0.8217 | 1.0548 | 94.6000 | 3.6000 |
| u23_turn_protect_mix_seed101 | all | 0.0312 | 0.0877 | 0.0430 | 0.0616 | 0.0314 | 0.1952 | 26.0256 | 0.8019 | 1.2804 | 88.5084 | 37.2558 |
| u23_turn_protect_mix_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| u23_turn_protect_mix_seed101 | uphill_long_entry | 0.0315 | 0.0615 | 0.0553 | 0.0807 | 0.0300 | 0.1445 | 69.0752 | 0.8001 | 1.6066 | 81.6923 | 59.1538 |
| u23_turn_protect_mix_seed101 | downhill_transition | 0.0160 | 0.0305 | 0.0303 | 0.0519 | 0.0240 | 0.1520 | 8.6774 | 0.7840 | 1.0914 | 92.0000 | 27.7692 |
| u23_turn_protect_mix_seed101 | uphill_return | 0.0480 | 0.0877 | 0.0389 | 0.0578 | 0.0286 | 0.0857 | 3.3124 | 0.9784 | 1.4422 | 89.0000 | 13.1000 |
| u23_turn_protect_mix_seed101 | flat_recovery | 0.0251 | 0.0421 | 0.0525 | 0.0447 | 0.0555 | 0.1952 | 17.0781 | 0.9027 | 1.2426 | 90.4000 | 21.8000 |
| u18_ltheta065_seed101 | all | 0.0280 | 0.0724 | 0.0484 | 0.0663 | 0.0372 | 0.2105 | 27.4300 | 0.9289 | 1.3825 | 86.6927 | 42.0133 |
| u18_ltheta065_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| u18_ltheta065_seed101 | uphill_long_entry | 0.0368 | 0.0724 | 0.0606 | 0.0857 | 0.0376 | 0.1659 | 46.6851 | 1.1238 | 1.7230 | 84.3077 | 67.9231 |
| u18_ltheta065_seed101 | downhill_transition | 0.0182 | 0.0356 | 0.0377 | 0.0491 | 0.0345 | 0.1466 | 2.5068 | 0.8143 | 1.1525 | 91.1538 | 32.2308 |
| u18_ltheta065_seed101 | uphill_return | 0.0258 | 0.0604 | 0.0414 | 0.0717 | 0.0266 | 0.0867 | 43.3927 | 1.0207 | 1.6786 | 81.7000 | 20.9000 |
| u18_ltheta065_seed101 | flat_recovery | 0.0332 | 0.0607 | 0.0609 | 0.0467 | 0.0619 | 0.2105 | 23.4301 | 1.0032 | 1.1968 | 84.6000 | 13.4000 |
