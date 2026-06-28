# Fair 10-seed closed-loop: agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06\baseline_lock_out.mat`
  - modern_fixed_seed1: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\04_validation_sentinel_closed_loop\agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06\modern_fixed_seed1_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\04_validation_sentinel_closed_loop\agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed7: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\04_validation_sentinel_closed_loop\agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06\uncertainty_weighted_seed7_out.mat`
  - uncertainty_weighted_seed340: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\04_validation_sentinel_closed_loop\agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06\uncertainty_weighted_seed340_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\agv_theta10_uniform_v2\agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| uncertainty_weighted_seed340 | 6.0000 | 9.0000 | 18.0000 | 33.0000 | 1.0000 |
| modern_fixed_seed1 | 15.0000 | 11.0000 | 11.0000 | 37.0000 | 2.0000 |
| uncertainty_weighted_seed7 | 23.0000 | 4.0000 | 14.0000 | 41.0000 | 3.0000 |
| ModernTCN | 23.0000 | 10.0000 | 9.0000 | 42.0000 | 4.0000 |
| modern_fixed_seed101 | 23.0000 | 11.0000 | 8.0000 | 42.0000 | 5.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0590 | 0.1299 | 0.0554 | 0.0475 | 0.0288 | 0.4245 | 97.1514 | 0.7257 | 19.5407 | 0.0000 | 1.2641 | 1.2230 | 69.7424 | 52.4798 |
| modern_fixed_seed1 | 0.0536 | 0.1208 | 0.0505 | 0.0442 | 0.0259 | 0.3448 | 97.1514 | 0.7011 | 44.4021 | 0.0000 | 1.2370 | 1.0974 | 56.7474 | 54.8635 |
| modern_fixed_seed101 | 0.0557 | 0.1197 | 0.0499 | 0.0516 | 0.0325 | 0.4441 | 97.1514 | 0.6848 | 5.7178 | 0.0000 | 1.3988 | 1.3306 | 57.2472 | 55.9400 |
| uncertainty_weighted_seed7 | 0.0555 | 0.1195 | 0.0558 | 0.0484 | 0.0310 | 0.4533 | 97.1514 | 1.1876 | 6.9236 | 0.0000 | 1.2230 | 1.2522 | 71.8570 | 66.2053 |
| uncertainty_weighted_seed340 | 0.0483 | 0.0983 | 0.0399 | 0.0421 | 0.0155 | 0.1756 | 97.1514 | 1.1969 | 14.0070 | 0.0000 | 1.1412 | 1.0983 | 60.8612 | 49.3272 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0268 | 0.0483 | 0.0708 | 0.8593 | 0.0000 |
| modern_fixed_seed1 | 0.0245 | 0.0325 | 0.0435 | 0.5480 | 0.0000 |
| modern_fixed_seed101 | 0.0244 | 0.0297 | 0.0315 | 0.2894 | 0.0000 |
| uncertainty_weighted_seed7 | 0.0240 | 0.0293 | 0.0569 | 0.2895 | 0.0000 |
| uncertainty_weighted_seed340 | 0.0237 | 0.0286 | 0.0299 | 0.2689 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0384 | 0.0000 | 0.0000 |
| modern_fixed_seed1 | 0.0000 | 0.0000 | 0.0384 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0384 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed7 | 0.0000 | 0.0000 | 0.0769 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed340 | 0.0000 | 0.0000 | 0.0769 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0590 | 0.1299 | 0.0554 | 0.0475 | 0.0288 | 0.7257 | 19.5407 | 1.2641 | 1.2230 | 69.7424 | 52.4798 |
| ModernTCN | all | 0.0585 | 0.1299 | 0.0549 | 0.0817 | 0.0285 | 0.7257 | 29.8327 | 1.2754 | 1.2350 | 70.3019 | 53.3962 |
| modern_fixed_seed1 | all | 0.0536 | 0.1208 | 0.0505 | 0.0442 | 0.0259 | 0.7011 | 44.4021 | 1.2370 | 1.0974 | 56.7474 | 54.8635 |
| modern_fixed_seed1 | all | 0.0531 | 0.1208 | 0.0500 | 0.0799 | 0.0256 | 0.7011 | 54.2341 | 1.2488 | 1.1117 | 57.5472 | 55.6981 |
| modern_fixed_seed101 | all | 0.0557 | 0.1197 | 0.0499 | 0.0516 | 0.0325 | 0.6848 | 5.7178 | 1.3988 | 1.3306 | 57.2472 | 55.9400 |
| modern_fixed_seed101 | all | 0.0552 | 0.1197 | 0.0494 | 0.0841 | 0.0322 | 0.6848 | 16.2654 | 1.4076 | 1.3406 | 58.0377 | 56.7925 |
| uncertainty_weighted_seed7 | all | 0.0555 | 0.1195 | 0.0558 | 0.0484 | 0.0310 | 1.1876 | 6.9236 | 1.2230 | 1.2522 | 71.8570 | 66.2053 |
| uncertainty_weighted_seed7 | all | 0.0550 | 0.1195 | 0.0552 | 0.0822 | 0.0307 | 1.1876 | 17.4489 | 1.2350 | 1.2637 | 72.3774 | 66.8679 |
| uncertainty_weighted_seed340 | all | 0.0483 | 0.0983 | 0.0399 | 0.0421 | 0.0155 | 1.1969 | 14.0070 | 1.1412 | 1.0983 | 60.8612 | 49.3272 |
| uncertainty_weighted_seed340 | all | 0.0478 | 0.0983 | 0.0395 | 0.0788 | 0.0154 | 1.1969 | 24.4012 | 1.1548 | 1.1126 | 61.5849 | 50.3019 |
