# Fair 10-seed closed-loop: agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16\baseline_lock_out.mat`
  - modern_fixed_seed42: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\04_validation_sentinel_closed_loop\agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16\modern_fixed_seed42_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\04_validation_sentinel_closed_loop\agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\04_validation_sentinel_closed_loop\agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\agv_theta10_uniform_v2\agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 9.0000 | 6.0000 | 6.0000 | 21.0000 | 1.0000 |
| modern_fixed_seed42 | 14.0000 | 5.0000 | 12.0000 | 31.0000 | 2.0000 |
| modern_fixed_seed101 | 16.0000 | 8.0000 | 8.0000 | 32.0000 | 3.0000 |
| uncertainty_weighted_seed101 | 21.0000 | 11.0000 | 14.0000 | 46.0000 | 4.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0590 | 0.0000 | 0.1270 | 197.1527 | 0.0001546 | 1.9540 | 0.0000 | 0.9594 | 0.9737 | 92.4260 | 100.0000 |
| modern_fixed_seed42 | 0.0000 | 0.0000 | 0.0000 | 0.0570 | 0.0000 | 0.2008 | 202.0774 | 0.0001546 | 1.9929 | 0.0000 | 0.6705 | 0.7036 | 92.4260 | 100.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0569 | 0.0000 | 0.1970 | 194.0246 | 0.0001546 | 1.8909 | 0.0000 | 0.6986 | 0.7259 | 92.4260 | 100.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0566 | 0.0000 | 0.2310 | 199.3378 | 0.0001546 | 1.9669 | 0.0000 | 0.7047 | 0.7271 | 92.4260 | 100.0000 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0305 | 0.0627 | 0.0772 | 6.6768 | 0.0000 |
| modern_fixed_seed42 | 0.0211 | 0.0255 | 0.0287 | 3.2728 | 0.0000 |
| modern_fixed_seed101 | 0.0210 | 0.0239 | 0.0262 | 0.4302 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0210 | 0.0230 | 0.0253 | 0.3011 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed42 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0000 | 0.0000 | 0.0000 | 0.0590 | 0.0000 | 0.0001546 | 1.9540 | 0.9594 | 0.9737 | 92.4260 | 100.0000 |
| ModernTCN | all | 0.0000 | 0.0000 | 0.0000 | 0.0959 | 0.0000 | 0.0003013 | 17.2038 | 1.0321 | 1.0462 | 90.7170 | 100.0000 |
| modern_fixed_seed42 | all | 0.0000 | 0.0000 | 0.0000 | 0.0570 | 0.0000 | 0.0001546 | 1.9929 | 0.6705 | 0.7036 | 92.4260 | 100.0000 |
| modern_fixed_seed42 | all | 0.0000 | 0.0000 | 0.0000 | 0.0946 | 0.0000 | 0.0003013 | 17.2420 | 0.7487 | 0.7812 | 90.7170 | 100.0000 |
| modern_fixed_seed101 | all | 0.0000 | 0.0000 | 0.0000 | 0.0569 | 0.0000 | 0.0001546 | 1.8909 | 0.6986 | 0.7259 | 92.4260 | 100.0000 |
| modern_fixed_seed101 | all | 0.0000 | 0.0000 | 0.0000 | 0.0946 | 0.0000 | 0.0003013 | 17.1418 | 0.7763 | 0.8031 | 90.7170 | 100.0000 |
| uncertainty_weighted_seed101 | all | 0.0000 | 0.0000 | 0.0000 | 0.0566 | 0.0000 | 0.0001546 | 1.9669 | 0.7047 | 0.7271 | 92.4260 | 100.0000 |
| uncertainty_weighted_seed101 | all | 0.0000 | 0.0000 | 0.0000 | 0.0944 | 0.0000 | 0.0003013 | 17.2164 | 0.7822 | 0.8042 | 90.7170 | 100.0000 |
