# Probe closed-loop: path_factory_target_downhill_straight_after_turn_v1

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_target_downhill_straight_after_turn_v1\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\tmp_path_probe\path_factory_target_downhill_straight_after_turn_v1\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\tmp_path_probe\path_factory_target_downhill_straight_after_turn_v1\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:/Matlab/Simulink/S-Function_16/data/paths/factory_targeted_eval/path_factory_target_downhill_straight_after_turn_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| uncertainty_weighted_seed101 | 7.0000 | 5.0000 | 10.0000 | 22.0000 | 1.0000 |
| modern_fixed_seed101 | 13.0000 | 4.0000 | 9.0000 | 26.0000 | 2.0000 |
| ModernTCN | 16.0000 | 9.0000 | 5.0000 | 30.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0138 | 0.0223 | 0.0163 | 0.0445 | 0.0039 | 0.6208 | 229.0215 | 0.1218 | 0.9111 | 0.0000 | 0.9628 | 1.0564 | 95.6812 | 58.1712 |
| modern_fixed_seed101 | 0.0115 | 0.0291 | 0.0109 | 0.0247 | 0.0032 | 0.1438 | 231.0156 | 0.1307 | 0.8880 | 0.0000 | 0.4337 | 0.5535 | 96.8542 | 69.9014 |
| uncertainty_weighted_seed101 | 0.0096 | 0.0227 | 0.0027 | 0.0213 | 0.0029 | 0.1260 | 230.5983 | 0.1231 | 1.8362 | 0.0000 | 0.3029 | 0.4273 | 96.2677 | 67.6620 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0257 | 0.0475 | 0.0583 | 0.3825 | 0.0000 |
| modern_fixed_seed101 | 0.0210 | 0.0230 | 0.0266 | 0.3104 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0213 | 0.0234 | 0.0248 | 0.2664 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0138 | 0.0223 | 0.0163 | 0.0445 | 0.0039 | 0.1218 | 0.9111 | 0.9628 | 1.0564 | 95.6812 | 58.1712 |
| ModernTCN | all | 0.0137 | 0.0223 | 0.0162 | 0.0777 | 0.0039 | 0.1218 | 9.7204 | 0.9507 | 1.0431 | 95.7368 | 58.7368 |
| modern_fixed_seed101 | all | 0.0115 | 0.0291 | 0.0109 | 0.0247 | 0.0032 | 0.1307 | 0.8880 | 0.4337 | 0.5535 | 96.8542 | 69.9014 |
| modern_fixed_seed101 | all | 0.0115 | 0.0291 | 0.0108 | 0.0685 | 0.0031 | 0.1307 | 9.6976 | 0.4284 | 0.5467 | 96.8947 | 70.2895 |
| uncertainty_weighted_seed101 | all | 0.0096 | 0.0227 | 0.0027 | 0.0213 | 0.0029 | 0.1231 | 1.8362 | 0.3029 | 0.4273 | 96.2677 | 67.6620 |
| uncertainty_weighted_seed101 | all | 0.0095 | 0.0227 | 0.0027 | 0.0674 | 0.0028 | 0.1231 | 10.6335 | 0.2993 | 0.4221 | 96.3158 | 68.0789 |
