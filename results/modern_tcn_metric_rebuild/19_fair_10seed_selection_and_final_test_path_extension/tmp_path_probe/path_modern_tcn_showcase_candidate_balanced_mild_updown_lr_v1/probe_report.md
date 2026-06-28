# Probe closed-loop: path_modern_tcn_showcase_candidate_balanced_mild_updown_lr_v1

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_modern_tcn_showcase_candidate_balanced_mild_updown_lr_v1\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\tmp_path_probe\path_modern_tcn_showcase_candidate_balanced_mild_updown_lr_v1\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\tmp_path_probe\path_modern_tcn_showcase_candidate_balanced_mild_updown_lr_v1\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:/Matlab/Simulink/S-Function_16/data/paths/modern_tcn_showcase/candidates/path_modern_tcn_showcase_candidate_balanced_mild_updown_lr_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 13.0000 | 5.0000 | 7.0000 | 25.0000 | 1.0000 |
| modern_fixed_seed101 | 13.0000 | 4.0000 | 9.0000 | 26.0000 | 2.0000 |
| uncertainty_weighted_seed101 | 10.0000 | 9.0000 | 8.0000 | 27.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0124 | 0.0394 | 0.0091 | 0.0130 | 0.0067 | 0.2678 | 271.2028 | 0.4135 | 0.4349 | 0.0000 | 0.0308 | 0.0308 | 98.8350 | 61.2589 |
| modern_fixed_seed101 | 0.0039 | 0.0119 | 0.0109 | 0.0130 | 0.0073 | 0.2737 | 271.2028 | 0.3558 | 0.4391 | 0.0000 | 0.0308 | 0.0308 | 99.2001 | 61.5545 |
| uncertainty_weighted_seed101 | 0.0056 | 0.0146 | 0.0101 | 0.0130 | 0.0065 | 0.2713 | 271.2028 | 0.2980 | 0.4343 | 0.0000 | 0.0308 | 0.0308 | 98.7654 | 40.4278 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0206 | 0.0226 | 0.0239 | 0.4408 | 0.0000 |
| modern_fixed_seed101 | 0.0220 | 0.0271 | 0.0317 | 3.3002 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0208 | 0.0228 | 0.0258 | 0.4414 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0124 | 0.0394 | 0.0091 | 0.0130 | 0.0067 | 0.4135 | 0.4349 | 0.0308 | 0.0308 | 98.8350 | 61.2589 |
| ModernTCN | all | 0.0123 | 0.0394 | 0.0091 | 0.0522 | 0.0067 | 0.4135 | 5.0127 | 0.0551 | 0.0551 | 98.2586 | 61.5862 |
| modern_fixed_seed101 | all | 0.0039 | 0.0119 | 0.0109 | 0.0130 | 0.0073 | 0.3558 | 0.4391 | 0.0308 | 0.0308 | 99.2001 | 61.5545 |
| modern_fixed_seed101 | all | 0.0039 | 0.0119 | 0.0108 | 0.0522 | 0.0073 | 0.3558 | 5.0168 | 0.0551 | 0.0551 | 98.6207 | 61.8793 |
| uncertainty_weighted_seed101 | all | 0.0056 | 0.0146 | 0.0101 | 0.0130 | 0.0065 | 0.2980 | 0.4343 | 0.0308 | 0.0308 | 98.7654 | 40.4278 |
| uncertainty_weighted_seed101 | all | 0.0056 | 0.0146 | 0.0101 | 0.0522 | 0.0065 | 0.2980 | 5.0121 | 0.0551 | 0.0551 | 98.1897 | 40.9483 |
