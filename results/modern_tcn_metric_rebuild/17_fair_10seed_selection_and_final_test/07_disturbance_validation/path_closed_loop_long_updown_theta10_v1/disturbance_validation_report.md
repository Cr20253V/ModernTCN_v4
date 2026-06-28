# Fair 10-seed closed-loop: path_closed_loop_long_updown_theta10_v1

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_long_updown_theta10_v1\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\07_disturbance_validation\path_closed_loop_long_updown_theta10_v1\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed340: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\07_disturbance_validation\path_closed_loop_long_updown_theta10_v1\uncertainty_weighted_seed340_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_long_updown_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 6.0000 | 5.0000 | 6.0000 | 17.0000 | 1.0000 |
| modern_fixed_seed101 | 12.0000 | 6.0000 | 8.0000 | 26.0000 | 2.0000 |
| uncertainty_weighted_seed340 | 18.0000 | 7.0000 | 10.0000 | 35.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0353 | 0.0881 | 0.0438 | 0.0566 | 0.0296 | 0.7594 | 322.8705 | 0.2188 | 7.7862 | 0.0000 | 0.7947 | 1.1614 | 90.9906 | 46.6789 |
| modern_fixed_seed101 | 0.0474 | 0.1400 | 0.0467 | 0.0604 | 0.0298 | 0.8904 | 325.8510 | 0.4594 | 7.0138 | 0.0000 | 0.9037 | 1.2331 | 91.7950 | 43.6222 |
| uncertainty_weighted_seed340 | 0.0640 | 0.2127 | 0.0501 | 0.0628 | 0.0298 | 0.9855 | 307.6933 | 0.6354 | 26.1253 | 0.0000 | 0.9670 | 1.3479 | 89.7954 | 50.6091 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0210 | 0.0457 | 0.0497 | 0.7124 | 0.0000 |
| modern_fixed_seed101 | 0.0216 | 0.0246 | 0.0271 | 3.2708 | 0.0000 |
| uncertainty_weighted_seed340 | 0.0235 | 0.0304 | 0.1312 | 0.4862 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed340 | 0.0000 | 0.0000 | 0.0230 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0353 | 0.0881 | 0.0438 | 0.0566 | 0.0296 | 0.2188 | 7.7862 | 0.7947 | 1.1614 | 90.9906 | 46.6789 |
| ModernTCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN | uphill_long_entry | 0.0299 | 0.0566 | 0.0520 | 0.0739 | 0.0237 | 0.1107 | 12.1779 | 0.9282 | 1.3464 | 88.4615 | 77.6154 |
| ModernTCN | downhill_transition | 0.0302 | 0.0507 | 0.0337 | 0.0474 | 0.0208 | 0.1171 | 5.5542 | 0.8060 | 1.1330 | 93.5385 | 32.3846 |
| ModernTCN | uphill_return | 0.0518 | 0.0881 | 0.0407 | 0.0571 | 0.0304 | 0.1020 | 3.1918 | 0.9406 | 1.4046 | 87.6000 | 28.1000 |
| ModernTCN | flat_recovery | 0.0285 | 0.0521 | 0.0583 | 0.0288 | 0.0565 | 0.2188 | 14.5651 | 0.5255 | 0.8510 | 93.2000 | 13.8000 |
| modern_fixed_seed101 | all | 0.0474 | 0.1400 | 0.0467 | 0.0604 | 0.0298 | 0.4594 | 7.0138 | 0.9037 | 1.2331 | 91.7950 | 43.6222 |
| modern_fixed_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| modern_fixed_seed101 | uphill_long_entry | 0.0336 | 0.0640 | 0.0552 | 0.0761 | 0.0245 | 0.1256 | 9.2516 | 1.1363 | 1.5131 | 87.2308 | 80.6154 |
| modern_fixed_seed101 | downhill_transition | 0.0327 | 0.0538 | 0.0367 | 0.0479 | 0.0189 | 0.1267 | 7.4058 | 0.7087 | 0.9609 | 96.4615 | 27.6923 |
| modern_fixed_seed101 | uphill_return | 0.0642 | 0.1314 | 0.0372 | 0.0701 | 0.0300 | 0.0882 | 3.1923 | 1.3125 | 1.8112 | 87.7000 | 17.3000 |
| modern_fixed_seed101 | flat_recovery | 0.0749 | 0.1400 | 0.0694 | 0.0220 | 0.0585 | 0.4594 | 10.6317 | 0.4423 | 0.6758 | 95.6000 | 13.4000 |
| uncertainty_weighted_seed340 | all | 0.0640 | 0.2127 | 0.0501 | 0.0628 | 0.0298 | 0.6354 | 26.1253 | 0.9670 | 1.3479 | 89.7954 | 50.6091 |
| uncertainty_weighted_seed340 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| uncertainty_weighted_seed340 | uphill_long_entry | 0.0522 | 0.1104 | 0.0532 | 0.0806 | 0.0207 | 0.1084 | 58.6729 | 1.4198 | 1.8878 | 85.0769 | 82.3077 |
| uncertainty_weighted_seed340 | downhill_transition | 0.0284 | 0.0513 | 0.0473 | 0.0429 | 0.0244 | 0.2686 | 5.7093 | 0.5888 | 0.8941 | 94.3846 | 24.9231 |
| uncertainty_weighted_seed340 | uphill_return | 0.0755 | 0.2022 | 0.0377 | 0.0756 | 0.0347 | 0.1228 | 24.7234 | 1.3352 | 1.8249 | 89.0000 | 49.1000 |
| uncertainty_weighted_seed340 | flat_recovery | 0.1226 | 0.2127 | 0.0767 | 0.0283 | 0.0515 | 0.6354 | 9.8866 | 0.5226 | 0.8463 | 86.6000 | 13.4000 |
