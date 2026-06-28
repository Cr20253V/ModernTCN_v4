# Probe closed-loop: path_factory_target_downhill_right_reversal_v1

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_target_downhill_right_reversal_v1\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\tmp_path_probe\path_factory_target_downhill_right_reversal_v1\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\tmp_path_probe\path_factory_target_downhill_right_reversal_v1\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:/Matlab/Simulink/S-Function_16/data/paths/factory_targeted_eval/path_factory_target_downhill_right_reversal_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| modern_fixed_seed101 | 8.0000 | 7.0000 | 8.0000 | 23.0000 | 1.0000 |
| ModernTCN | 15.0000 | 5.0000 | 7.0000 | 27.0000 | 2.0000 |
| uncertainty_weighted_seed101 | 13.0000 | 6.0000 | 9.0000 | 28.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0146 | 0.0312 | 0.0290 | 0.0334 | 0.0061 | 0.4483 | 271.9753 | 0.3967 | 2.2046 | 0.0000 | 0.6226 | 0.7723 | 90.2192 | 91.6406 |
| modern_fixed_seed101 | 0.0082 | 0.0180 | 0.0094 | 0.0368 | 0.0034 | 0.3970 | 272.9327 | 0.3187 | 2.2786 | 0.0000 | 0.6796 | 0.9075 | 91.3997 | 84.6302 |
| uncertainty_weighted_seed101 | 0.0113 | 0.0239 | 0.0227 | 0.0337 | 0.0059 | 0.4528 | 271.7241 | 0.3266 | 3.2160 | 0.0000 | 0.5952 | 0.8127 | 88.9665 | 89.1833 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0305 | 0.0507 | 0.0583 | 0.3854 | 0.0000 |
| modern_fixed_seed101 | 0.0208 | 0.0229 | 0.0247 | 0.3956 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0210 | 0.0232 | 0.0251 | 0.2603 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0146 | 0.0312 | 0.0290 | 0.0334 | 0.0061 | 0.3967 | 2.2046 | 0.6226 | 0.7723 | 90.2192 | 91.6406 |
| ModernTCN | all | 0.0145 | 0.0312 | 0.0288 | 0.0659 | 0.0061 | 0.3967 | 9.1731 | 0.6155 | 0.7635 | 90.3333 | 91.7381 |
| modern_fixed_seed101 | all | 0.0082 | 0.0180 | 0.0094 | 0.0368 | 0.0034 | 0.3187 | 2.2786 | 0.6796 | 0.9075 | 91.3997 | 84.6302 |
| modern_fixed_seed101 | all | 0.0082 | 0.0180 | 0.0093 | 0.0677 | 0.0034 | 0.3187 | 9.2462 | 0.6718 | 0.8971 | 91.5000 | 84.8333 |
| uncertainty_weighted_seed101 | all | 0.0113 | 0.0239 | 0.0227 | 0.0337 | 0.0059 | 0.3266 | 3.2160 | 0.5952 | 0.8127 | 88.9665 | 89.1833 |
| uncertainty_weighted_seed101 | all | 0.0113 | 0.0239 | 0.0225 | 0.0661 | 0.0059 | 0.3266 | 10.1726 | 0.5885 | 0.8033 | 89.1190 | 89.3095 |
