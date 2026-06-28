# Fair 10-seed closed-loop: path_closed_loop_sharp_turn_transition_theta10_v1

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_sharp_turn_transition_theta10_v1\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\06_final_test_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed340: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\06_final_test_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\uncertainty_weighted_seed340_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_sharp_turn_transition_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| modern_fixed_seed101 | 11.0000 | 5.0000 | 7.0000 | 23.0000 | 1.0000 |
| ModernTCN | 10.0000 | 7.0000 | 7.0000 | 24.0000 | 2.0000 |
| uncertainty_weighted_seed340 | 15.0000 | 6.0000 | 10.0000 | 31.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 0.5137 | 224.7044 | 1.3509 | 5.3237 | 0.0000 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| modern_fixed_seed101 | 0.0485 | 0.1094 | 0.0530 | 0.0351 | 0.0257 | 0.6839 | 224.0463 | 1.4409 | 1.8182 | 0.0000 | 0.5806 | 0.6863 | 92.7393 | 57.0763 |
| uncertainty_weighted_seed340 | 0.0488 | 0.0995 | 0.0637 | 0.0352 | 0.0344 | 0.8025 | 226.3932 | 1.4343 | 2.5916 | 0.0000 | 0.6075 | 0.7140 | 94.3506 | 52.0676 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0209 | 0.0226 | 0.0239 | 0.2452 | 0.0000 |
| modern_fixed_seed101 | 0.0233 | 0.0282 | 0.0301 | 0.4839 | 0.0000 |
| uncertainty_weighted_seed340 | 0.0233 | 0.0274 | 0.0292 | 0.2902 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0777 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0582 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed340 | 0.0000 | 0.0000 | 0.0582 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 1.3509 | 5.3237 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| ModernTCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN | uphill_left_transition | 0.0371 | 0.0676 | 0.0542 | 0.0372 | 0.0259 | 0.1441 | 0.9621 | 0.5676 | 0.7060 | 93.9444 | 63.6111 |
| ModernTCN | downhill_right_transition | 0.0200 | 0.0391 | 0.0304 | 0.0299 | 0.0229 | 0.1301 | 3.4855 | 0.5232 | 0.6685 | 96.6000 | 36.9500 |
| ModernTCN | flat_left_exit | 0.0722 | 0.1269 | 0.0421 | 0.0451 | 0.0147 | 1.3509 | 18.4221 | 1.0234 | 1.0628 | 87.5000 | 28.2000 |
| modern_fixed_seed101 | all | 0.0485 | 0.1094 | 0.0530 | 0.0351 | 0.0257 | 1.4409 | 1.8182 | 0.5806 | 0.6863 | 92.7393 | 57.0763 |
| modern_fixed_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| modern_fixed_seed101 | uphill_left_transition | 0.0598 | 0.1094 | 0.0615 | 0.0430 | 0.0222 | 0.1673 | 1.1297 | 0.8603 | 0.9868 | 93.4444 | 88.8889 |
| modern_fixed_seed101 | downhill_right_transition | 0.0390 | 0.0659 | 0.0475 | 0.0325 | 0.0247 | 0.2272 | 1.7958 | 0.4652 | 0.6091 | 92.2500 | 36.4000 |
| modern_fixed_seed101 | flat_left_exit | 0.0510 | 0.1033 | 0.0561 | 0.0267 | 0.0358 | 1.4409 | 3.4304 | 0.5117 | 0.5406 | 89.9000 | 26.2000 |
| uncertainty_weighted_seed340 | all | 0.0488 | 0.0995 | 0.0637 | 0.0352 | 0.0344 | 1.4343 | 2.5916 | 0.6075 | 0.7140 | 94.3506 | 52.0676 |
| uncertainty_weighted_seed340 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| uncertainty_weighted_seed340 | uphill_left_transition | 0.0526 | 0.0929 | 0.0730 | 0.0487 | 0.0328 | 0.2177 | 0.9424 | 1.0504 | 1.1827 | 93.3333 | 87.8333 |
| uncertainty_weighted_seed340 | downhill_right_transition | 0.0481 | 0.0844 | 0.0612 | 0.0290 | 0.0366 | 0.2458 | 4.1483 | 0.4840 | 0.6450 | 96.1000 | 26.6000 |
| uncertainty_weighted_seed340 | flat_left_exit | 0.0514 | 0.0995 | 0.0616 | 0.0145 | 0.0384 | 1.4343 | 3.0462 | 0.2707 | 0.2590 | 90.7000 | 21.9000 |
