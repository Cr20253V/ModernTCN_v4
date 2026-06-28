# Fair 10-seed closed-loop: agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06\baseline_lock_out.mat`
  - modern_fixed_seed42: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\04_validation_sentinel_closed_loop\agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06\modern_fixed_seed42_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\04_validation_sentinel_closed_loop\agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\04_validation_sentinel_closed_loop\agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\agv_theta10_uniform_v2\agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| uncertainty_weighted_seed101 | 8.0000 | 8.0000 | 14.0000 | 30.0000 | 1.0000 |
| ModernTCN | 15.0000 | 8.0000 | 8.0000 | 31.0000 | 2.0000 |
| modern_fixed_seed101 | 14.0000 | 5.0000 | 12.0000 | 31.0000 | 3.0000 |
| modern_fixed_seed42 | 23.0000 | 9.0000 | 6.0000 | 38.0000 | 4.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0590 | 0.1299 | 0.0554 | 0.0475 | 0.0288 | 0.4245 | 97.1514 | 0.7257 | 19.5407 | 0.0000 | 1.2641 | 1.2230 | 69.7424 | 52.4798 |
| modern_fixed_seed42 | 0.0623 | 0.1247 | 0.0566 | 0.0520 | 0.0345 | 0.4856 | 97.1514 | 0.7251 | 1.1396 | 0.0000 | 1.3890 | 1.3595 | 49.9808 | 61.9377 |
| modern_fixed_seed101 | 0.0557 | 0.1201 | 0.0513 | 0.0505 | 0.0343 | 0.4343 | 97.1514 | 1.0249 | 10.4792 | 0.0000 | 1.2357 | 1.3012 | 75.0481 | 58.9773 |
| uncertainty_weighted_seed101 | 0.0539 | 0.1208 | 0.0498 | 0.0476 | 0.0278 | 0.3811 | 97.1514 | 0.7751 | 12.2960 | 0.0000 | 1.2187 | 1.1996 | 65.0135 | 50.9804 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0268 | 0.0483 | 0.0708 | 0.8593 | 0.0000 |
| modern_fixed_seed42 | 0.0212 | 0.0242 | 0.0272 | 0.3705 | 0.0000 |
| modern_fixed_seed101 | 0.0212 | 0.0233 | 0.0249 | 0.3064 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0212 | 0.0237 | 0.0259 | 0.2464 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0384 | 0.0000 | 0.0000 |
| modern_fixed_seed42 | 0.0000 | 0.0000 | 0.0384 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0769 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0769 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0590 | 0.1299 | 0.0554 | 0.0475 | 0.0288 | 0.7257 | 19.5407 | 1.2641 | 1.2230 | 69.7424 | 52.4798 |
| ModernTCN | all | 0.0585 | 0.1299 | 0.0549 | 0.0817 | 0.0285 | 0.7257 | 29.8327 | 1.2754 | 1.2350 | 70.3019 | 53.3962 |
| modern_fixed_seed42 | all | 0.0623 | 0.1247 | 0.0566 | 0.0520 | 0.0345 | 0.7251 | 1.1396 | 1.3890 | 1.3595 | 49.9808 | 61.9377 |
| modern_fixed_seed42 | all | 0.0617 | 0.1247 | 0.0561 | 0.0844 | 0.0341 | 0.7251 | 11.7719 | 1.3980 | 1.3690 | 50.9057 | 62.6792 |
| modern_fixed_seed101 | all | 0.0557 | 0.1201 | 0.0513 | 0.0505 | 0.0343 | 1.0249 | 10.4792 | 1.2357 | 1.3012 | 75.0481 | 58.9773 |
| modern_fixed_seed101 | all | 0.0552 | 0.1201 | 0.0508 | 0.0835 | 0.0339 | 1.0249 | 20.9388 | 1.2475 | 1.3118 | 75.5094 | 59.7736 |
| uncertainty_weighted_seed101 | all | 0.0539 | 0.1208 | 0.0498 | 0.0476 | 0.0278 | 0.7751 | 12.2960 | 1.2187 | 1.1996 | 65.0135 | 50.9804 |
| uncertainty_weighted_seed101 | all | 0.0534 | 0.1208 | 0.0493 | 0.0818 | 0.0276 | 0.7751 | 22.7219 | 1.2308 | 1.2121 | 65.6604 | 51.9245 |
