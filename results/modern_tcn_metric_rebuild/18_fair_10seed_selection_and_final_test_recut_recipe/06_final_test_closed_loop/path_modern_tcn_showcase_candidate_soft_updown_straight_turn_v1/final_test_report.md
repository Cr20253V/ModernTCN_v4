# Fair 10-seed closed-loop: path_modern_tcn_showcase_candidate_soft_updown_straight_turn_v1

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_modern_tcn_showcase_candidate_soft_updown_straight_turn_v1\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\06_final_test_closed_loop\path_modern_tcn_showcase_candidate_soft_updown_straight_turn_v1\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\06_final_test_closed_loop\path_modern_tcn_showcase_candidate_soft_updown_straight_turn_v1\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\modern_tcn_showcase\candidates\path_modern_tcn_showcase_candidate_soft_updown_straight_turn_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 9.0000 | 3.0000 | 7.0000 | 19.0000 | 1.0000 |
| uncertainty_weighted_seed101 | 12.0000 | 9.0000 | 8.0000 | 29.0000 | 2.0000 |
| modern_fixed_seed101 | 15.0000 | 6.0000 | 9.0000 | 30.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0033 | 0.0106 | 0.0081 | 0.0105 | 0.0067 | 0.2763 | 243.3561 | 0.2963 | 0.3033 | 0.0000 | 0.0167 | 0.0167 | 99.5496 | 73.5723 |
| modern_fixed_seed101 | 0.0034 | 0.0113 | 0.0083 | 0.0105 | 0.0072 | 0.2764 | 243.3561 | 0.2909 | 0.3035 | 0.0000 | 0.0167 | 0.0167 | 99.5496 | 66.0782 |
| uncertainty_weighted_seed101 | 0.0048 | 0.0149 | 0.0078 | 0.0105 | 0.0057 | 0.2766 | 243.3561 | 0.2553 | 0.3003 | 0.0000 | 0.0167 | 0.0167 | 99.5496 | 39.8847 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0354 | 0.0597 | 0.0737 | 0.3972 | 0.0000 |
| modern_fixed_seed101 | 0.0213 | 0.0229 | 0.0243 | 0.2453 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0212 | 0.0232 | 0.0248 | 0.2481 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0033 | 0.0106 | 0.0081 | 0.0105 | 0.0067 | 0.2963 | 0.3033 | 0.0167 | 0.0167 | 99.5496 | 73.5723 |
| ModernTCN | all | 0.0033 | 0.0106 | 0.0081 | 0.0528 | 0.0067 | 0.2963 | 5.2287 | 0.0376 | 0.0376 | 99.0179 | 73.8036 |
| modern_fixed_seed101 | all | 0.0034 | 0.0113 | 0.0083 | 0.0105 | 0.0072 | 0.2909 | 0.3035 | 0.0167 | 0.0167 | 99.5496 | 66.0782 |
| modern_fixed_seed101 | all | 0.0034 | 0.0113 | 0.0083 | 0.0528 | 0.0072 | 0.2909 | 5.2288 | 0.0376 | 0.0376 | 99.0179 | 66.3929 |
| uncertainty_weighted_seed101 | all | 0.0048 | 0.0149 | 0.0078 | 0.0105 | 0.0057 | 0.2553 | 0.3003 | 0.0167 | 0.0167 | 99.5496 | 39.8847 |
| uncertainty_weighted_seed101 | all | 0.0048 | 0.0149 | 0.0078 | 0.0528 | 0.0057 | 0.2553 | 5.2257 | 0.0376 | 0.0376 | 99.0179 | 40.4286 |
