# Fair 10-seed closed-loop: path_factory_logistics_showcase_theta10_v10

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_logistics_showcase_theta10_v10\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\06_final_test_closed_loop\path_factory_logistics_showcase_theta10_v10\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\06_final_test_closed_loop\path_factory_logistics_showcase_theta10_v10\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v10.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| uncertainty_weighted_seed101 | 7.0000 | 3.0000 | 9.0000 | 19.0000 | 1.0000 |
| modern_fixed_seed101 | 11.0000 | 7.0000 | 5.0000 | 23.0000 | 2.0000 |
| ModernTCN | 18.0000 | 8.0000 | 10.0000 | 36.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.9669 | 2.7381 | 0.3605 | 0.3304 | 0.0696 | 14.1572 | 720.0000 | 1.6204 | 503.4768 | 0.0000 | 0.9240 | 0.9086 | 89.7322 | 51.7181 |
| modern_fixed_seed101 | 0.0818 | 0.2782 | 0.0719 | 0.0496 | 0.0231 | 3.8266 | 217.8665 | 1.4816 | 3.9896 | 0.0000 | 0.9248 | 0.9279 | 93.5108 | 60.2576 |
| uncertainty_weighted_seed101 | 0.0643 | 0.2332 | 0.0644 | 0.0213 | 0.0232 | 2.2155 | 218.2634 | 1.4903 | 5.0405 | 0.0000 | 0.4425 | 0.4509 | 98.5856 | 72.6898 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0321 | 0.0555 | 0.0763 | 0.3454 | 0.0000 |
| modern_fixed_seed101 | 0.0208 | 0.0226 | 0.0246 | 3.2548 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0209 | 0.0224 | 0.0239 | 0.4326 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 12.8847 | 12.7746 | 36.1513 | 15.6116 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.3098 | 0.0897 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.1753 | 0.0408 | 0.0000 |

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
| modern_fixed_seed101 | all | 0.0818 | 0.2782 | 0.0719 | 0.0496 | 0.0231 | 1.4816 | 3.9896 | 0.9248 | 0.9279 | 93.5108 | 60.2576 |
| modern_fixed_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1062 | 0.0000 | 0.0002577 | 24.2442 | 0.0537 | 0.0537 | 100.0000 | 100.0000 |
| modern_fixed_seed101 | outbound_rack_aisle | 0.0000 | 0.0000 | 0.0000 | 0.0236 | 0.0000 | 7.95e-05 | 0.6546 | 0.3901 | 0.4083 | 98.8333 | 100.0000 |
| modern_fixed_seed101 | approach_to_u_turn | 0.0000 | 0.0000 | 0.0000 | 0.0259 | 0.0000 | 2.077e-05 | 1.1925 | 0.5197 | 0.4506 | 99.5000 | 100.0000 |
| modern_fixed_seed101 | adjacent_aisle_u_turn | 0.1157 | 0.2782 | 0.1527 | 0.0186 | 0.0130 | 1.4816 | 3.8242 | 0.5991 | 0.5991 | 99.5635 | 46.3990 |
| modern_fixed_seed101 | return_recovery_aisle | 0.1464 | 0.2542 | 0.1231 | 0.0329 | 0.0911 | 1.1162 | 56.8096 | 0.8879 | 0.8970 | 100.0000 | 11.0016 |
| modern_fixed_seed101 | return_slope_aisle | 0.0939 | 0.1164 | 0.0149 | 0.0825 | 0.0169 | 0.1980 | 0.4566 | 1.9483 | 1.9594 | 94.7432 | 22.8784 |
| modern_fixed_seed101 | shipping_return_aisle | 0.0905 | 0.0975 | 0.0027 | 0.0362 | 0.0083 | 0.0463 | 0.8632 | 0.5904 | 0.5268 | 21.4182 | 63.6035 |
| uncertainty_weighted_seed101 | all | 0.0643 | 0.2332 | 0.0644 | 0.0213 | 0.0232 | 1.4903 | 5.0405 | 0.4425 | 0.4509 | 98.5856 | 72.6898 |
| uncertainty_weighted_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1062 | 0.0000 | 0.0002577 | 24.2442 | 0.0537 | 0.0537 | 100.0000 | 100.0000 |
| uncertainty_weighted_seed101 | outbound_rack_aisle | 0.0000 | 0.0000 | 0.0000 | 0.0215 | 0.0000 | 6.62e-05 | 0.1212 | 0.4226 | 0.4372 | 98.6667 | 100.0000 |
| uncertainty_weighted_seed101 | approach_to_u_turn | 0.0000 | 0.0000 | 0.0000 | 0.0212 | 0.0000 | 1.725e-05 | 3.8400 | 0.4845 | 0.4175 | 96.7000 | 100.0000 |
| uncertainty_weighted_seed101 | adjacent_aisle_u_turn | 0.0808 | 0.2153 | 0.1367 | 0.0187 | 0.0151 | 1.4903 | 1.9991 | 0.5991 | 0.5991 | 99.5635 | 55.9581 |
| uncertainty_weighted_seed101 | return_recovery_aisle | 0.1232 | 0.2332 | 0.1129 | 0.0316 | 0.0963 | 0.5863 | 87.9856 | 0.8970 | 0.8970 | 100.0000 | 3.7767 |
| uncertainty_weighted_seed101 | return_slope_aisle | 0.0776 | 0.0922 | 0.0076 | 0.0225 | 0.0101 | 0.3717 | 0.1486 | 0.3894 | 0.4178 | 98.4459 | 54.9865 |
| uncertainty_weighted_seed101 | shipping_return_aisle | 0.0777 | 0.0814 | 0.0021 | 0.0128 | 0.0082 | 0.0417 | 0.8622 | 0.2105 | 0.1741 | 94.5731 | 87.0478 |
