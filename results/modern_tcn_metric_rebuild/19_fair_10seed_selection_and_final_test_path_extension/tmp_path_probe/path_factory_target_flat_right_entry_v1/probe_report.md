# Probe closed-loop: path_factory_target_flat_right_entry_v1

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_target_flat_right_entry_v1\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\tmp_path_probe\path_factory_target_flat_right_entry_v1\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\tmp_path_probe\path_factory_target_flat_right_entry_v1\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:/Matlab/Simulink/S-Function_16/data/paths/factory_targeted_eval/path_factory_target_flat_right_entry_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 13.0000 | 3.0000 | 6.0000 | 22.0000 | 1.0000 |
| modern_fixed_seed101 | 14.0000 | 6.0000 | 6.0000 | 26.0000 | 2.0000 |
| uncertainty_weighted_seed101 | 9.0000 | 9.0000 | 12.0000 | 30.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0073 | 0.0193 | 0.0147 | 0.0086 | 0.0050 | 0.2641 | 158.5363 | 0.3280 | 0.1182 | 0.0000 | 0.0000 | 0.0000 | 100.0000 | 68.6766 |
| modern_fixed_seed101 | 0.0107 | 0.0252 | 0.0119 | 0.0086 | 0.0050 | 0.2604 | 158.5363 | 0.3279 | 0.1166 | 0.0000 | 0.0000 | 0.0000 | 100.0000 | 39.3843 |
| uncertainty_weighted_seed101 | 0.0029 | 0.0057 | 0.0132 | 0.0086 | 0.0026 | 0.2623 | 158.5363 | 0.3672 | 0.1253 | 0.0000 | 0.0000 | 0.0000 | 100.0000 | 38.3053 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0353 | 0.0534 | 0.0586 | 4.5832 | 0.0000 |
| modern_fixed_seed101 | 0.0280 | 0.0492 | 0.0559 | 3.9144 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0250 | 0.0419 | 0.0522 | 0.5922 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0073 | 0.0193 | 0.0147 | 0.0086 | 0.0050 | 0.3280 | 0.1182 | 0.0000 | 0.0000 | 100.0000 | 68.6766 |
| ModernTCN | all | 0.0073 | 0.0193 | 0.0146 | 0.0665 | 0.0049 | 0.3280 | 9.5089 | 0.0000 | 0.0000 | 100.0000 | 69.1562 |
| modern_fixed_seed101 | all | 0.0107 | 0.0252 | 0.0119 | 0.0086 | 0.0050 | 0.3279 | 0.1166 | 0.0000 | 0.0000 | 100.0000 | 39.3843 |
| modern_fixed_seed101 | all | 0.0106 | 0.0252 | 0.0118 | 0.0665 | 0.0050 | 0.3279 | 9.5074 | 0.0000 | 0.0000 | 100.0000 | 40.3438 |
| uncertainty_weighted_seed101 | all | 0.0029 | 0.0057 | 0.0132 | 0.0086 | 0.0026 | 0.3672 | 0.1253 | 0.0000 | 0.0000 | 100.0000 | 38.3053 |
| uncertainty_weighted_seed101 | all | 0.0028 | 0.0057 | 0.0131 | 0.0665 | 0.0026 | 0.3672 | 9.5159 | 0.0000 | 0.0000 | 100.0000 | 39.2812 |
