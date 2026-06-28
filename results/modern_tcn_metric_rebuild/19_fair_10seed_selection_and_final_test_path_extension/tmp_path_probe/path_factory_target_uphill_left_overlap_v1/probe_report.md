# Probe closed-loop: path_factory_target_uphill_left_overlap_v1

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_target_uphill_left_overlap_v1\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\tmp_path_probe\path_factory_target_uphill_left_overlap_v1\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\tmp_path_probe\path_factory_target_uphill_left_overlap_v1\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:/Matlab/Simulink/S-Function_16/data/paths/factory_targeted_eval/path_factory_target_uphill_left_overlap_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 8.0000 | 7.0000 | 5.0000 | 20.0000 | 1.0000 |
| uncertainty_weighted_seed101 | 12.0000 | 5.0000 | 10.0000 | 27.0000 | 2.0000 |
| modern_fixed_seed101 | 16.0000 | 6.0000 | 9.0000 | 31.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0200 | 0.0360 | 0.0278 | 0.0283 | 0.0037 | 0.4739 | 287.1585 | 0.1390 | 0.6944 | 0.0000 | 0.5635 | 0.6392 | 97.7706 | 46.0354 |
| modern_fixed_seed101 | 0.0362 | 0.0567 | 0.0531 | 0.0271 | 0.0043 | 0.6514 | 287.3103 | 0.8251 | 0.8905 | 0.0000 | 0.4174 | 0.4894 | 96.1388 | 56.0331 |
| uncertainty_weighted_seed101 | 0.0324 | 0.0548 | 0.0469 | 0.0272 | 0.0041 | 0.6221 | 286.9026 | 1.0078 | 2.7158 | 0.0000 | 0.4181 | 0.5110 | 96.8283 | 74.1439 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0274 | 0.0478 | 0.0562 | 0.5749 | 0.0000 |
| modern_fixed_seed101 | 0.0250 | 0.0418 | 0.0503 | 4.0016 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0208 | 0.0288 | 0.0470 | 0.4574 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0460 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0460 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0200 | 0.0360 | 0.0278 | 0.0283 | 0.0037 | 0.1390 | 0.6944 | 0.5635 | 0.6392 | 97.7706 | 46.0354 |
| ModernTCN | all | 0.0199 | 0.0360 | 0.0276 | 0.0640 | 0.0037 | 0.1390 | 7.8228 | 0.5573 | 0.6322 | 97.7955 | 46.6591 |
| modern_fixed_seed101 | all | 0.0362 | 0.0567 | 0.0531 | 0.0271 | 0.0043 | 0.8251 | 0.8905 | 0.4174 | 0.4894 | 96.1388 | 56.0331 |
| modern_fixed_seed101 | all | 0.0360 | 0.0567 | 0.0528 | 0.0636 | 0.0043 | 0.8251 | 8.0167 | 0.4129 | 0.4840 | 96.1818 | 56.5227 |
| uncertainty_weighted_seed101 | all | 0.0324 | 0.0548 | 0.0469 | 0.0272 | 0.0041 | 1.0078 | 2.7158 | 0.4181 | 0.5110 | 96.8283 | 74.1439 |
| uncertainty_weighted_seed101 | all | 0.0322 | 0.0548 | 0.0466 | 0.0636 | 0.0040 | 1.0078 | 9.8217 | 0.4136 | 0.5054 | 96.8636 | 74.4545 |
