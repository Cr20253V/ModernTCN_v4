# Fair 10-seed closed-loop: path_modern_tcn_showcase_candidate_flat_clean_s_turn_v1

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_modern_tcn_showcase_candidate_flat_clean_s_turn_v1\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\06_final_test_closed_loop\path_modern_tcn_showcase_candidate_flat_clean_s_turn_v1\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\06_final_test_closed_loop\path_modern_tcn_showcase_candidate_flat_clean_s_turn_v1\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\modern_tcn_showcase\candidates\path_modern_tcn_showcase_candidate_flat_clean_s_turn_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 11.0000 | 4.0000 | 4.0000 | 19.0000 | 1.0000 |
| modern_fixed_seed101 | 10.0000 | 5.0000 | 10.0000 | 25.0000 | 2.0000 |
| uncertainty_weighted_seed101 | 15.0000 | 9.0000 | 10.0000 | 34.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0055 | 0.0129 | 0.0102 | 0.0072 | 0.0072 | 0.2585 | 158.5363 | 0.2697 | 0.0837 | 0.0000 | 0.0000 | 0.0000 | 100.0000 | 52.0105 |
| modern_fixed_seed101 | 0.0046 | 0.0122 | 0.0107 | 0.0072 | 0.0071 | 0.2612 | 158.5363 | 0.3237 | 0.0916 | 0.0000 | 0.0000 | 0.0000 | 100.0000 | 55.0209 |
| uncertainty_weighted_seed101 | 0.0097 | 0.0257 | 0.0098 | 0.0072 | 0.0081 | 0.2603 | 158.5363 | 0.3187 | 0.0879 | 0.0000 | 0.0311 | 0.0000 | 100.0000 | 35.5526 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0207 | 0.0230 | 0.0247 | 0.4412 | 0.0000 |
| modern_fixed_seed101 | 0.0210 | 0.0230 | 0.0245 | 0.3042 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0208 | 0.0229 | 0.0247 | 0.2567 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0055 | 0.0129 | 0.0102 | 0.0072 | 0.0072 | 0.2697 | 0.0837 | 0.0000 | 0.0000 | 100.0000 | 52.0105 |
| ModernTCN | all | 0.0055 | 0.0129 | 0.0101 | 0.0555 | 0.0072 | 0.2697 | 6.6162 | 0.0000 | 0.0000 | 100.0000 | 52.5217 |
| modern_fixed_seed101 | all | 0.0046 | 0.0122 | 0.0107 | 0.0072 | 0.0071 | 0.3237 | 0.0916 | 0.0000 | 0.0000 | 100.0000 | 55.0209 |
| modern_fixed_seed101 | all | 0.0045 | 0.0122 | 0.0106 | 0.0555 | 0.0071 | 0.3237 | 6.6240 | 0.0000 | 0.0000 | 100.0000 | 55.5000 |
| uncertainty_weighted_seed101 | all | 0.0097 | 0.0257 | 0.0098 | 0.0072 | 0.0081 | 0.3187 | 0.0879 | 0.0311 | 0.0000 | 100.0000 | 35.5526 |
| uncertainty_weighted_seed101 | all | 0.0097 | 0.0257 | 0.0098 | 0.0555 | 0.0081 | 0.3187 | 6.6203 | 0.0308 | 0.0000 | 100.0000 | 36.2609 |
