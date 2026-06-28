# Fair 10-seed closed-loop: path_modern_tcn_showcase_candidate_positive_slope_lr_v1

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_modern_tcn_showcase_candidate_positive_slope_lr_v1\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\06_final_test_closed_loop\path_modern_tcn_showcase_candidate_positive_slope_lr_v1\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\06_final_test_closed_loop\path_modern_tcn_showcase_candidate_positive_slope_lr_v1\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\modern_tcn_showcase\candidates\path_modern_tcn_showcase_candidate_positive_slope_lr_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 9.0000 | 3.0000 | 4.0000 | 16.0000 | 1.0000 |
| modern_fixed_seed101 | 12.0000 | 6.0000 | 9.0000 | 27.0000 | 2.0000 |
| uncertainty_weighted_seed101 | 15.0000 | 9.0000 | 11.0000 | 35.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0061 | 0.0175 | 0.0123 | 0.0184 | 0.0071 | 0.3587 | 258.5162 | 0.3654 | 0.1301 | 0.0000 | 0.0262 | 0.0262 | 99.3011 | 58.2605 |
| modern_fixed_seed101 | 0.0046 | 0.0115 | 0.0136 | 0.0184 | 0.0090 | 0.3624 | 258.5162 | 0.4343 | 0.1419 | 0.0000 | 0.0262 | 0.0262 | 99.3011 | 53.0382 |
| uncertainty_weighted_seed101 | 0.0137 | 0.0406 | 0.0125 | 0.0184 | 0.0091 | 0.3586 | 258.5162 | 0.5317 | 0.1329 | 0.0000 | 0.1919 | 0.0262 | 99.3011 | 42.0501 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0205 | 0.0234 | 0.0286 | 3.4196 | 0.0000 |
| modern_fixed_seed101 | 0.0207 | 0.0245 | 0.0262 | 3.2510 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0207 | 0.0226 | 0.0241 | 0.4353 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0061 | 0.0175 | 0.0123 | 0.0184 | 0.0071 | 0.3654 | 0.1301 | 0.0262 | 0.0262 | 99.3011 | 58.2605 |
| ModernTCN | all | 0.0060 | 0.0175 | 0.0122 | 0.0570 | 0.0070 | 0.3654 | 5.4054 | 0.0510 | 0.0510 | 98.6538 | 58.6538 |
| modern_fixed_seed101 | all | 0.0046 | 0.0115 | 0.0136 | 0.0184 | 0.0090 | 0.4343 | 0.1419 | 0.0262 | 0.0262 | 99.3011 | 53.0382 |
| modern_fixed_seed101 | all | 0.0046 | 0.0115 | 0.0136 | 0.0570 | 0.0090 | 0.4343 | 5.4171 | 0.0510 | 0.0510 | 98.6538 | 53.4808 |
| uncertainty_weighted_seed101 | all | 0.0137 | 0.0406 | 0.0125 | 0.0184 | 0.0091 | 0.5317 | 0.1329 | 0.1919 | 0.0262 | 99.3011 | 42.0501 |
| uncertainty_weighted_seed101 | all | 0.0136 | 0.0406 | 0.0125 | 0.0570 | 0.0090 | 0.5317 | 5.4082 | 0.2152 | 0.0510 | 98.6538 | 42.6154 |
