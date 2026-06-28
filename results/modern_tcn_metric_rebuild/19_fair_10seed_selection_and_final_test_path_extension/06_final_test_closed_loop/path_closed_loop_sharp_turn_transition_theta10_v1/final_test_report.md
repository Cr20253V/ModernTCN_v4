# Fair 10-seed closed-loop: path_closed_loop_sharp_turn_transition_theta10_v1

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_sharp_turn_transition_theta10_v1\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\06_final_test_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\06_final_test_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_sharp_turn_transition_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| uncertainty_weighted_seed101 | 8.0000 | 5.0000 | 8.0000 | 21.0000 | 1.0000 |
| modern_fixed_seed101 | 11.0000 | 5.0000 | 7.0000 | 23.0000 | 2.0000 |
| ModernTCN | 17.0000 | 8.0000 | 9.0000 | 34.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 0.5137 | 224.7044 | 1.3509 | 5.3237 | 0.0000 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| modern_fixed_seed101 | 0.0258 | 0.0632 | 0.0375 | 0.0333 | 0.0225 | 0.4875 | 223.2985 | 0.4781 | 2.5259 | 0.0000 | 0.5813 | 0.6967 | 95.5348 | 51.1163 |
| uncertainty_weighted_seed101 | 0.0292 | 0.0854 | 0.0342 | 0.0319 | 0.0162 | 0.4383 | 224.8288 | 0.2875 | 2.1621 | 0.0000 | 0.4830 | 0.6209 | 91.9821 | 62.7063 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0209 | 0.0226 | 0.0239 | 0.2452 | 0.0000 |
| modern_fixed_seed101 | 0.0210 | 0.0231 | 0.0246 | 0.3938 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0210 | 0.0230 | 0.0247 | 0.2548 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0777 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 1.3509 | 5.3237 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| ModernTCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN | uphill_left_transition | 0.0371 | 0.0676 | 0.0542 | 0.0372 | 0.0259 | 0.1441 | 0.9621 | 0.5676 | 0.7060 | 93.9444 | 63.6111 |
| ModernTCN | downhill_right_transition | 0.0200 | 0.0391 | 0.0304 | 0.0299 | 0.0229 | 0.1301 | 3.4855 | 0.5232 | 0.6685 | 96.6000 | 36.9500 |
| ModernTCN | flat_left_exit | 0.0722 | 0.1269 | 0.0421 | 0.0451 | 0.0147 | 1.3509 | 18.4221 | 1.0234 | 1.0628 | 87.5000 | 28.2000 |
| modern_fixed_seed101 | all | 0.0258 | 0.0632 | 0.0375 | 0.0333 | 0.0225 | 0.4781 | 2.5259 | 0.5813 | 0.6967 | 95.5348 | 51.1163 |
| modern_fixed_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| modern_fixed_seed101 | uphill_left_transition | 0.0364 | 0.0632 | 0.0556 | 0.0411 | 0.0264 | 0.1397 | 0.7122 | 0.7514 | 0.8607 | 93.5556 | 61.2222 |
| modern_fixed_seed101 | downhill_right_transition | 0.0148 | 0.0370 | 0.0262 | 0.0333 | 0.0252 | 0.1569 | 4.9309 | 0.6481 | 0.8586 | 97.0000 | 40.4500 |
| modern_fixed_seed101 | flat_left_exit | 0.0244 | 0.0416 | 0.0172 | 0.0160 | 0.0094 | 0.4781 | 1.5570 | 0.3455 | 0.3219 | 94.6000 | 37.2000 |
| uncertainty_weighted_seed101 | all | 0.0292 | 0.0854 | 0.0342 | 0.0319 | 0.0162 | 0.2875 | 2.1621 | 0.4830 | 0.6209 | 91.9821 | 62.7063 |
| uncertainty_weighted_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| uncertainty_weighted_seed101 | uphill_left_transition | 0.0479 | 0.0854 | 0.0509 | 0.0392 | 0.0194 | 0.2164 | 1.2078 | 0.6210 | 0.7419 | 93.0000 | 88.2222 |
| uncertainty_weighted_seed101 | downhill_right_transition | 0.0073 | 0.0237 | 0.0196 | 0.0299 | 0.0136 | 0.1484 | 3.6535 | 0.5072 | 0.6987 | 95.9000 | 48.8000 |
| uncertainty_weighted_seed101 | flat_left_exit | 0.0122 | 0.0192 | 0.0247 | 0.0224 | 0.0176 | 0.2875 | 1.3455 | 0.3558 | 0.4656 | 79.5000 | 31.6000 |
