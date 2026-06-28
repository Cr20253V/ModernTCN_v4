# Fair 10-seed closed-loop: agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16\baseline_lock_out.mat`
  - modern_fixed_seed1: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\04_validation_sentinel_closed_loop\agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16\modern_fixed_seed1_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\04_validation_sentinel_closed_loop\agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed7: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\04_validation_sentinel_closed_loop\agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16\uncertainty_weighted_seed7_out.mat`
  - uncertainty_weighted_seed340: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\04_validation_sentinel_closed_loop\agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16\uncertainty_weighted_seed340_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\agv_theta10_uniform_v2\agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 9.0000 | 6.0000 | 10.0000 | 25.0000 | 1.0000 |
| modern_fixed_seed1 | 14.0000 | 7.0000 | 11.0000 | 32.0000 | 2.0000 |
| modern_fixed_seed101 | 19.0000 | 11.0000 | 10.0000 | 40.0000 | 3.0000 |
| uncertainty_weighted_seed7 | 20.0000 | 10.0000 | 17.0000 | 47.0000 | 4.0000 |
| uncertainty_weighted_seed340 | 28.0000 | 11.0000 | 12.0000 | 51.0000 | 5.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0590 | 0.0000 | 0.1270 | 197.1527 | 0.0001546 | 1.9540 | 0.0000 | 0.9594 | 0.9737 | 92.4260 | 100.0000 |
| modern_fixed_seed1 | 0.0000 | 0.0000 | 0.0000 | 0.0570 | 0.0000 | 0.2786 | 197.3181 | 0.0001546 | 1.9138 | 0.0000 | 0.6307 | 0.6696 | 92.4260 | 100.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0598 | 0.0000 | 0.1344 | 195.7180 | 0.0001546 | 1.8945 | 0.0000 | 1.0051 | 1.0354 | 92.4260 | 100.0000 |
| uncertainty_weighted_seed7 | 0.0000 | 0.0000 | 0.0000 | 0.0570 | 0.0000 | 0.2720 | 199.2318 | 0.0001546 | 1.9226 | 0.0000 | 0.6195 | 0.6640 | 92.4260 | 100.0000 |
| uncertainty_weighted_seed340 | 0.0000 | 0.0000 | 0.0000 | 0.0573 | 0.0000 | 0.2952 | 195.5562 | 0.0001546 | 1.8893 | 0.0000 | 0.6111 | 0.6601 | 92.4260 | 100.0000 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0305 | 0.0627 | 0.0772 | 6.6768 | 0.0000 |
| modern_fixed_seed1 | 0.0283 | 0.0493 | 0.0643 | 3.5022 | 0.0000 |
| modern_fixed_seed101 | 0.0280 | 0.0477 | 0.0622 | 0.6071 | 0.0000 |
| uncertainty_weighted_seed7 | 0.0236 | 0.1369 | 0.1578 | 0.4060 | 0.0000 |
| uncertainty_weighted_seed340 | 0.0240 | 0.0294 | 0.0315 | 0.3084 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed7 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed340 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0000 | 0.0000 | 0.0000 | 0.0590 | 0.0000 | 0.0001546 | 1.9540 | 0.9594 | 0.9737 | 92.4260 | 100.0000 |
| ModernTCN | all | 0.0000 | 0.0000 | 0.0000 | 0.0959 | 0.0000 | 0.0003013 | 17.2038 | 1.0321 | 1.0462 | 90.7170 | 100.0000 |
| modern_fixed_seed1 | all | 0.0000 | 0.0000 | 0.0000 | 0.0570 | 0.0000 | 0.0001546 | 1.9138 | 0.6307 | 0.6696 | 92.4260 | 100.0000 |
| modern_fixed_seed1 | all | 0.0000 | 0.0000 | 0.0000 | 0.0946 | 0.0000 | 0.0003013 | 17.1642 | 0.7096 | 0.7478 | 90.7170 | 100.0000 |
| modern_fixed_seed101 | all | 0.0000 | 0.0000 | 0.0000 | 0.0598 | 0.0000 | 0.0001546 | 1.8945 | 1.0051 | 1.0354 | 92.4260 | 100.0000 |
| modern_fixed_seed101 | all | 0.0000 | 0.0000 | 0.0000 | 0.0963 | 0.0000 | 0.0003013 | 17.1453 | 1.0769 | 1.1066 | 90.7170 | 100.0000 |
| uncertainty_weighted_seed7 | all | 0.0000 | 0.0000 | 0.0000 | 0.0570 | 0.0000 | 0.0001546 | 1.9226 | 0.6195 | 0.6640 | 92.4260 | 100.0000 |
| uncertainty_weighted_seed7 | all | 0.0000 | 0.0000 | 0.0000 | 0.0946 | 0.0000 | 0.0003013 | 17.1730 | 0.6986 | 0.7423 | 90.7170 | 100.0000 |
| uncertainty_weighted_seed340 | all | 0.0000 | 0.0000 | 0.0000 | 0.0573 | 0.0000 | 0.0001546 | 1.8893 | 0.6111 | 0.6601 | 92.4260 | 100.0000 |
| uncertainty_weighted_seed340 | all | 0.0000 | 0.0000 | 0.0000 | 0.0948 | 0.0000 | 0.0003013 | 17.1402 | 0.6904 | 0.7384 | 90.7170 | 100.0000 |
