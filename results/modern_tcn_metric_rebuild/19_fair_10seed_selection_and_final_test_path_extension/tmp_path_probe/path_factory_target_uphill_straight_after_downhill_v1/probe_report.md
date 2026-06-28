# Probe closed-loop: path_factory_target_uphill_straight_after_downhill_v1

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_target_uphill_straight_after_downhill_v1\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\tmp_path_probe\path_factory_target_uphill_straight_after_downhill_v1\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\tmp_path_probe\path_factory_target_uphill_straight_after_downhill_v1\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:/Matlab/Simulink/S-Function_16/data/paths/factory_targeted_eval/path_factory_target_uphill_straight_after_downhill_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 10.0000 | 6.0000 | 7.0000 | 23.0000 | 1.0000 |
| modern_fixed_seed101 | 11.0000 | 4.0000 | 8.0000 | 23.0000 | 2.0000 |
| uncertainty_weighted_seed101 | 15.0000 | 8.0000 | 9.0000 | 32.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0362 | 0.0000 | 0.4792 | 213.9822 | 7.531e-05 | 2.4936 | 0.0000 | 0.7453 | 0.8212 | 93.4700 | 100.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0325 | 0.0000 | 0.2631 | 211.5563 | 8.447e-05 | 1.3238 | 0.0000 | 0.5334 | 0.6530 | 94.0521 | 100.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0312 | 0.0000 | 0.3825 | 211.3771 | 8.317e-05 | 3.2642 | 0.0000 | 0.5621 | 0.6685 | 93.0144 | 100.0000 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0279 | 0.0455 | 0.0537 | 0.4606 | 0.0000 |
| modern_fixed_seed101 | 0.0210 | 0.0230 | 0.0244 | 0.2534 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0212 | 0.0306 | 0.0458 | 0.2422 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0000 | 0.0000 | 0.0000 | 0.0362 | 0.0000 | 7.531e-05 | 2.4936 | 0.7453 | 0.8212 | 93.4700 | 100.0000 |
| ModernTCN | all | 0.0000 | 0.0000 | 0.0000 | 0.0732 | 0.0000 | 0.0002847 | 11.1971 | 0.7363 | 0.8112 | 93.5500 | 100.0000 |
| modern_fixed_seed101 | all | 0.0000 | 0.0000 | 0.0000 | 0.0325 | 0.0000 | 8.447e-05 | 1.3238 | 0.5334 | 0.6530 | 94.0521 | 100.0000 |
| modern_fixed_seed101 | all | 0.0000 | 0.0000 | 0.0000 | 0.0714 | 0.0000 | 0.0002847 | 10.0417 | 0.5270 | 0.6452 | 94.1250 | 100.0000 |
| uncertainty_weighted_seed101 | all | 0.0000 | 0.0000 | 0.0000 | 0.0312 | 0.0000 | 8.317e-05 | 3.2642 | 0.5621 | 0.6685 | 93.0144 | 100.0000 |
| uncertainty_weighted_seed101 | all | 0.0000 | 0.0000 | 0.0000 | 0.0708 | 0.0000 | 0.0002847 | 11.9584 | 0.5554 | 0.6604 | 93.1000 | 100.0000 |
