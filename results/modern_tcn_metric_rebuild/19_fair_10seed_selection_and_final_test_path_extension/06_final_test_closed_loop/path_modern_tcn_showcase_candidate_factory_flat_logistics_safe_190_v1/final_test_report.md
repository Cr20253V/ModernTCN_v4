# Fair 10-seed closed-loop: path_modern_tcn_showcase_candidate_factory_flat_logistics_safe_190_v1

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_modern_tcn_showcase_candidate_factory_flat_logistics_safe_190_v1\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\06_final_test_closed_loop\path_modern_tcn_showcase_candidate_factory_flat_logistics_safe_190_v1\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\06_final_test_closed_loop\path_modern_tcn_showcase_candidate_factory_flat_logistics_safe_190_v1\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\modern_tcn_showcase\candidates\path_modern_tcn_showcase_candidate_factory_flat_logistics_safe_190_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| modern_fixed_seed101 | 9.0000 | 7.0000 | 6.0000 | 22.0000 | 1.0000 |
| uncertainty_weighted_seed101 | 9.0000 | 7.0000 | 10.0000 | 26.0000 | 2.0000 |
| ModernTCN | 18.0000 | 4.0000 | 8.0000 | 30.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0142 | 0.0758 | 0.0104 | 0.0035 | 0.0088 | 0.2499 | 155.6001 | 0.3520 | 0.0304 | 0.0000 | 0.0000 | 0.0000 | 99.8417 | 51.5118 |
| modern_fixed_seed101 | 0.0069 | 0.0317 | 0.0088 | 0.0035 | 0.0067 | 0.2426 | 155.6001 | 0.2767 | 0.0224 | 0.0000 | 0.0000 | 0.0000 | 99.8364 | 39.2380 |
| uncertainty_weighted_seed101 | 0.0089 | 0.0347 | 0.0080 | 0.0035 | 0.0054 | 0.2395 | 155.6001 | 0.3034 | 0.0234 | 0.0000 | 0.0000 | 0.0000 | 100.0000 | 13.8726 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0205 | 0.0253 | 0.0441 | 7.0758 | 0.0000 |
| modern_fixed_seed101 | 0.0264 | 0.0462 | 0.0551 | 4.2522 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0219 | 0.0373 | 0.0498 | 0.6090 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0142 | 0.0758 | 0.0104 | 0.0035 | 0.0088 | 0.3520 | 0.0304 | 0.0000 | 0.0000 | 99.8417 | 51.5118 |
| ModernTCN | all | 0.0142 | 0.0758 | 0.0104 | 0.0267 | 0.0088 | 0.3520 | 1.5421 | 0.0000 | 0.0000 | 99.8421 | 51.6368 |
| modern_fixed_seed101 | all | 0.0069 | 0.0317 | 0.0088 | 0.0035 | 0.0067 | 0.2767 | 0.0224 | 0.0000 | 0.0000 | 99.8364 | 39.2380 |
| modern_fixed_seed101 | all | 0.0069 | 0.0317 | 0.0088 | 0.0267 | 0.0067 | 0.2767 | 1.5341 | 0.0000 | 0.0000 | 99.8368 | 39.3947 |
| uncertainty_weighted_seed101 | all | 0.0089 | 0.0347 | 0.0080 | 0.0035 | 0.0054 | 0.3034 | 0.0234 | 0.0000 | 0.0000 | 100.0000 | 13.8726 |
| uncertainty_weighted_seed101 | all | 0.0089 | 0.0347 | 0.0080 | 0.0267 | 0.0054 | 0.3034 | 1.5351 | 0.0000 | 0.0000 | 100.0000 | 14.1000 |
