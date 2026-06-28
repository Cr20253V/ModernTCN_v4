# Probe closed-loop: path_modern_tcn_showcase_candidate_factory_like_buffered_lr_190_v1

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_modern_tcn_showcase_candidate_factory_like_buffered_lr_190_v1\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\tmp_path_probe\path_modern_tcn_showcase_candidate_factory_like_buffered_lr_190_v1\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\tmp_path_probe\path_modern_tcn_showcase_candidate_factory_like_buffered_lr_190_v1\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:/Matlab/Simulink/S-Function_16/data/paths/modern_tcn_showcase/candidates/path_modern_tcn_showcase_candidate_factory_like_buffered_lr_190_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| uncertainty_weighted_seed101 | 6.0000 | 7.0000 | 8.0000 | 21.0000 | 1.0000 |
| modern_fixed_seed101 | 12.0000 | 6.0000 | 6.0000 | 24.0000 | 2.0000 |
| ModernTCN | 18.0000 | 5.0000 | 10.0000 | 33.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0601 | 0.2751 | 0.0510 | 0.0277 | 0.0167 | 1.4318 | 160.5411 | 1.4943 | 1.3792 | 0.0000 | 0.4627 | 0.4562 | 98.7072 | 51.5223 |
| modern_fixed_seed101 | 0.0271 | 0.1242 | 0.0309 | 0.0238 | 0.0120 | 0.9072 | 157.7830 | 1.0212 | 0.4221 | 0.0000 | 0.3576 | 0.3545 | 98.5278 | 47.3220 |
| uncertainty_weighted_seed101 | 0.0220 | 0.1050 | 0.0287 | 0.0193 | 0.0101 | 0.8651 | 159.8652 | 0.9858 | 0.9991 | 0.0000 | 0.2769 | 0.2854 | 98.1531 | 40.7630 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0206 | 0.0220 | 0.0230 | 0.2993 | 0.0000 |
| modern_fixed_seed101 | 0.0205 | 0.0222 | 0.0239 | 3.2266 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0206 | 0.0221 | 0.0232 | 0.4431 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.2163 | 0.0739 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0528 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0950 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0601 | 0.2751 | 0.0510 | 0.0277 | 0.0167 | 1.4943 | 1.3792 | 0.4627 | 0.4562 | 98.7072 | 51.5223 |
| ModernTCN | all | 0.0601 | 0.2751 | 0.0509 | 0.0383 | 0.0167 | 1.4943 | 2.8875 | 0.4615 | 0.4550 | 98.7105 | 51.6474 |
| modern_fixed_seed101 | all | 0.0271 | 0.1242 | 0.0309 | 0.0238 | 0.0120 | 1.0212 | 0.4221 | 0.3576 | 0.3545 | 98.5278 | 47.3220 |
| modern_fixed_seed101 | all | 0.0271 | 0.1242 | 0.0309 | 0.0356 | 0.0120 | 1.0212 | 1.9328 | 0.3567 | 0.3536 | 98.5316 | 47.4579 |
| uncertainty_weighted_seed101 | all | 0.0220 | 0.1050 | 0.0287 | 0.0193 | 0.0101 | 0.9858 | 0.9991 | 0.2769 | 0.2854 | 98.1531 | 40.7630 |
| uncertainty_weighted_seed101 | all | 0.0220 | 0.1050 | 0.0287 | 0.0327 | 0.0100 | 0.9858 | 2.5083 | 0.2762 | 0.2847 | 98.1579 | 40.9211 |
