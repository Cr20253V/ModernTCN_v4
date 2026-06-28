# ModernTCN small base recipe: path_closed_loop_sharp_turn_transition_theta10_v1

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_sharp_turn_transition_theta10_v1\baseline_lock_out.mat`
  - modern_base_seed21: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\16_recipe_vs_deployment_comparison\09_modern_base_closed_loop\01_closed_loop_runs\path_closed_loop_sharp_turn_transition_theta10_v1\modern_base_seed21_out.mat`
  - modern_base_seed42: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\16_recipe_vs_deployment_comparison\09_modern_base_closed_loop\01_closed_loop_runs\path_closed_loop_sharp_turn_transition_theta10_v1\modern_base_seed42_out.mat`
  - modern_base_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\16_recipe_vs_deployment_comparison\09_modern_base_closed_loop\01_closed_loop_runs\path_closed_loop_sharp_turn_transition_theta10_v1\modern_base_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_sharp_turn_transition_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| modern_base_seed21 | 6.0000 | 7.0000 | 9.0000 | 22.0000 | 1.0000 |
| baseline_lock | 14.0000 | 8.0000 | 9.0000 | 31.0000 | 2.0000 |
| modern_base_seed101 | 16.0000 | 7.0000 | 9.0000 | 32.0000 | 3.0000 |
| modern_base_seed42 | 24.0000 | 8.0000 | 13.0000 | 45.0000 | 4.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 0.5137 | 224.7044 | 1.3509 | 5.3237 | 0.0000 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| modern_base_seed21 | 0.0345 | 0.0948 | 0.0384 | 0.0343 | 0.0173 | 0.4656 | 225.8834 | 0.2854 | 2.0506 | 0.0000 | 0.5907 | 0.6588 | 93.5741 | 54.2613 |
| modern_base_seed42 | 0.0649 | 0.1809 | 0.0665 | 0.0451 | 0.0339 | 0.8733 | 224.2631 | 1.4792 | 6.7011 | 0.0000 | 0.8874 | 1.0080 | 93.4382 | 61.8132 |
| modern_base_seed101 | 0.0485 | 0.1094 | 0.0530 | 0.0351 | 0.0257 | 0.6839 | 224.0463 | 1.4409 | 1.8182 | 0.0000 | 0.5806 | 0.6863 | 92.7393 | 57.0763 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0209 | 0.0226 | 0.0239 | 0.2452 | 0.0000 |
| modern_base_seed21 | 0.0246 | 0.0370 | 0.0491 | 0.2744 | 0.0000 |
| modern_base_seed42 | 0.0260 | 0.0379 | 0.0493 | 0.2859 | 0.0000 |
| modern_base_seed101 | 0.0264 | 0.0386 | 0.0481 | 0.3295 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0777 | 0.0000 | 0.0000 |
| modern_base_seed21 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_base_seed42 | 0.0000 | 0.0000 | 0.0971 | 0.0388 | 0.0000 |
| modern_base_seed101 | 0.0000 | 0.0000 | 0.0582 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | all | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 1.3509 | 5.3237 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| baseline_lock | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| baseline_lock | uphill_left_transition | 0.0371 | 0.0676 | 0.0542 | 0.0372 | 0.0259 | 0.1441 | 0.9621 | 0.5676 | 0.7060 | 93.9444 | 63.6111 |
| baseline_lock | downhill_right_transition | 0.0200 | 0.0391 | 0.0304 | 0.0299 | 0.0229 | 0.1301 | 3.4855 | 0.5232 | 0.6685 | 96.6000 | 36.9500 |
| baseline_lock | flat_left_exit | 0.0722 | 0.1269 | 0.0421 | 0.0451 | 0.0147 | 1.3509 | 18.4221 | 1.0234 | 1.0628 | 87.5000 | 28.2000 |
| modern_base_seed21 | all | 0.0345 | 0.0948 | 0.0384 | 0.0343 | 0.0173 | 0.2854 | 2.0506 | 0.5907 | 0.6588 | 93.5741 | 54.2613 |
| modern_base_seed21 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| modern_base_seed21 | uphill_left_transition | 0.0528 | 0.0948 | 0.0587 | 0.0434 | 0.0222 | 0.1964 | 1.3123 | 0.7998 | 0.9044 | 94.8889 | 69.9444 |
| modern_base_seed21 | downhill_right_transition | 0.0219 | 0.0589 | 0.0227 | 0.0335 | 0.0145 | 0.2393 | 3.2493 | 0.6049 | 0.7901 | 94.6000 | 47.3500 |
| modern_base_seed21 | flat_left_exit | 0.0118 | 0.0185 | 0.0188 | 0.0158 | 0.0152 | 0.2854 | 1.3913 | 0.3932 | 0.1853 | 86.9000 | 23.9000 |
| modern_base_seed42 | all | 0.0649 | 0.1809 | 0.0665 | 0.0451 | 0.0339 | 1.4792 | 6.7011 | 0.8874 | 1.0080 | 93.4382 | 61.8132 |
| modern_base_seed42 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| modern_base_seed42 | uphill_left_transition | 0.0679 | 0.1228 | 0.0691 | 0.0510 | 0.0279 | 0.1757 | 0.8382 | 1.1050 | 1.2321 | 93.2222 | 87.2778 |
| modern_base_seed42 | downhill_right_transition | 0.0489 | 0.0873 | 0.0577 | 0.0446 | 0.0272 | 0.4273 | 3.9983 | 0.9261 | 1.0835 | 94.2500 | 38.3000 |
| modern_base_seed42 | flat_left_exit | 0.0929 | 0.1809 | 0.0866 | 0.0399 | 0.0551 | 1.4792 | 24.7206 | 0.7297 | 0.8071 | 89.9000 | 49.7000 |
| modern_base_seed101 | all | 0.0485 | 0.1094 | 0.0530 | 0.0351 | 0.0257 | 1.4409 | 1.8182 | 0.5806 | 0.6863 | 92.7393 | 57.0763 |
| modern_base_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| modern_base_seed101 | uphill_left_transition | 0.0598 | 0.1094 | 0.0615 | 0.0430 | 0.0222 | 0.1673 | 1.1297 | 0.8603 | 0.9868 | 93.4444 | 88.8889 |
| modern_base_seed101 | downhill_right_transition | 0.0390 | 0.0659 | 0.0475 | 0.0325 | 0.0247 | 0.2272 | 1.7958 | 0.4652 | 0.6091 | 92.2500 | 36.4000 |
| modern_base_seed101 | flat_left_exit | 0.0510 | 0.1033 | 0.0561 | 0.0267 | 0.0358 | 1.4409 | 3.4304 | 0.5117 | 0.5406 | 89.9000 | 26.2000 |
