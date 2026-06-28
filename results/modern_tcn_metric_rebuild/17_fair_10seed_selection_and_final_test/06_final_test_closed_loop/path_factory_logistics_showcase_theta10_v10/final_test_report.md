# Fair 10-seed closed-loop: path_factory_logistics_showcase_theta10_v10

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_logistics_showcase_theta10_v10\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\06_final_test_closed_loop\path_factory_logistics_showcase_theta10_v10\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed340: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\06_final_test_closed_loop\path_factory_logistics_showcase_theta10_v10\uncertainty_weighted_seed340_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v10.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| modern_fixed_seed101 | 6.0000 | 4.0000 | 5.0000 | 15.0000 | 1.0000 |
| uncertainty_weighted_seed340 | 12.0000 | 5.0000 | 10.0000 | 27.0000 | 2.0000 |
| ModernTCN | 18.0000 | 9.0000 | 9.0000 | 36.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.9669 | 2.7381 | 0.3605 | 0.3304 | 0.0696 | 14.1572 | 720.0000 | 1.6204 | 503.4768 | 0.0000 | 0.9240 | 0.9086 | 89.7322 | 51.7181 |
| modern_fixed_seed101 | 0.1344 | 0.5072 | 0.1006 | 0.0279 | 0.0290 | 3.5897 | 222.6668 | 1.4822 | 14.4309 | 0.0000 | 0.6248 | 0.6314 | 98.6956 | 56.6217 |
| uncertainty_weighted_seed340 | 0.2586 | 0.8928 | 0.1277 | 0.0321 | 0.0400 | 4.4946 | 719.8114 | 1.6374 | 105.5456 | 0.0000 | 0.6451 | 0.6482 | 97.7540 | 74.4711 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0321 | 0.0555 | 0.0763 | 0.3454 | 0.0000 |
| modern_fixed_seed101 | 0.0228 | 0.0248 | 0.0274 | 3.3126 | 0.0000 |
| uncertainty_weighted_seed340 | 0.0232 | 0.0255 | 0.0289 | 0.4945 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 12.8847 | 12.7746 | 36.1513 | 15.6116 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.4443 | 0.0571 | 0.0000 |
| uncertainty_weighted_seed340 | 0.0938 | 0.0938 | 4.6386 | 0.2323 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.9669 | 2.7381 | 0.3605 | 0.3304 | 0.0696 | 1.6204 | 503.4768 | 0.9240 | 0.9086 | 89.7322 | 51.7181 |
| ModernTCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.1062 | 0.0000 | 0.0002577 | 24.2442 | 0.0537 | 0.0537 | 100.0000 | 100.0000 |
| ModernTCN | outbound_rack_aisle | 0.0000 | 0.0000 | 0.0000 | 0.0304 | 0.0000 | 7.708e-05 | 3.3426 | 0.6848 | 0.7007 | 98.8205 | 100.0000 |
| ModernTCN | approach_to_u_turn | 0.0000 | 0.0000 | 0.0000 | 0.0321 | 0.0000 | 2.114e-05 | 1.1725 | 0.7407 | 0.6230 | 97.7000 | 100.0000 |
| ModernTCN | adjacent_aisle_u_turn | 0.5182 | 0.8335 | 0.2596 | 0.0232 | 0.0147 | 1.4946 | 19.7449 | 0.6543 | 0.5991 | 96.9446 | 44.7621 |
| ModernTCN | return_recovery_aisle | 0.5092 | 0.7917 | 0.2471 | 0.0717 | 0.1212 | 1.6204 | 231.4976 | 0.8970 | 0.8970 | 100.0000 | 3.2841 |
| ModernTCN | return_slope_aisle | 1.5820 | 2.7381 | 0.5803 | 0.4705 | 0.1157 | 1.6198 | 1615 | 1.5247 | 1.5070 | 73.4054 | 8.7432 |
| ModernTCN | shipping_return_aisle | 1.4406 | 1.4447 | 0.4753 | 0.8600 | 0.0225 | 1.3842 | 1.158e-08 | 0.8319 | 0.8319 | 78.5818 | 0.0000 |
| modern_fixed_seed101 | all | 0.1344 | 0.5072 | 0.1006 | 0.0279 | 0.0290 | 1.4822 | 14.4309 | 0.6248 | 0.6314 | 98.6956 | 56.6217 |
| modern_fixed_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1062 | 0.0000 | 0.0002577 | 24.2442 | 0.0537 | 0.0537 | 100.0000 | 100.0000 |
| modern_fixed_seed101 | outbound_rack_aisle | 0.0000 | 0.0000 | 0.0000 | 0.0281 | 0.0000 | 6.249e-05 | 0.1487 | 0.6318 | 0.6545 | 99.0385 | 100.0000 |
| modern_fixed_seed101 | approach_to_u_turn | 0.0000 | 0.0000 | 0.0000 | 0.0257 | 0.0000 | 2.037e-05 | 5.1361 | 0.5892 | 0.5420 | 97.1000 | 100.0000 |
| modern_fixed_seed101 | adjacent_aisle_u_turn | 0.2792 | 0.5072 | 0.2118 | 0.0187 | 0.0159 | 1.4822 | 3.6822 | 0.5991 | 0.5991 | 100.0000 | 32.8896 |
| modern_fixed_seed101 | return_recovery_aisle | 0.2366 | 0.3706 | 0.1671 | 0.0362 | 0.1034 | 1.2847 | 262.0128 | 0.8970 | 0.8970 | 100.0000 | 8.3744 |
| modern_fixed_seed101 | return_slope_aisle | 0.0463 | 0.1809 | 0.0340 | 0.0339 | 0.0290 | 0.5582 | 0.9496 | 0.7518 | 0.7641 | 97.6216 | 26.5270 |
| modern_fixed_seed101 | shipping_return_aisle | 0.0335 | 0.0680 | 0.0157 | 0.0147 | 0.0136 | 0.0788 | 3.3167 | 0.2507 | 0.2075 | 97.1056 | 26.7004 |
| uncertainty_weighted_seed340 | all | 0.2586 | 0.8928 | 0.1277 | 0.0321 | 0.0400 | 1.6374 | 105.5456 | 0.6451 | 0.6482 | 97.7540 | 74.4711 |
| uncertainty_weighted_seed340 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1062 | 0.0000 | 0.0002577 | 24.2442 | 0.0537 | 0.0537 | 100.0000 | 100.0000 |
| uncertainty_weighted_seed340 | outbound_rack_aisle | 0.0000 | 0.0000 | 0.0000 | 0.0316 | 0.0000 | 7.483e-05 | 0.6219 | 0.6933 | 0.7115 | 98.4103 | 100.0000 |
| uncertainty_weighted_seed340 | approach_to_u_turn | 0.0000 | 0.0000 | 0.0000 | 0.0250 | 0.0000 | 1.534e-05 | 1.1451 | 0.6012 | 0.5163 | 94.9000 | 100.0000 |
| uncertainty_weighted_seed340 | adjacent_aisle_u_turn | 0.5414 | 0.8928 | 0.2545 | 0.0244 | 0.0118 | 1.4988 | 28.5357 | 0.5991 | 0.5991 | 99.5635 | 43.5399 |
| uncertainty_weighted_seed340 | return_recovery_aisle | 0.4567 | 0.7762 | 0.2426 | 0.0478 | 0.1303 | 1.6374 | 310.0435 | 0.8970 | 0.8970 | 100.0000 | 11.2479 |
| uncertainty_weighted_seed340 | return_slope_aisle | 0.0762 | 0.2688 | 0.0655 | 0.0381 | 0.0492 | 1.2020 | 280.2644 | 0.7489 | 0.7629 | 95.9730 | 64.9324 |
| uncertainty_weighted_seed340 | shipping_return_aisle | 0.0015 | 0.0032 | 0.0006096 | 0.0152 | 0.0030 | 0.0036 | 0.8345 | 0.2694 | 0.2085 | 95.8032 | 100.0000 |
