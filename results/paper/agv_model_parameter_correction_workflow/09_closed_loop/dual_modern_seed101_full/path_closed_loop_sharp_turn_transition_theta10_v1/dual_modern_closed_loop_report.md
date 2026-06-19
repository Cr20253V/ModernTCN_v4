# Dual ModernTCN seed101 plantfix closed-loop comparison

- 输出文件：
  - ModernTCN_slope_seed101: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\dual_modern_seed101_full\path_closed_loop_sharp_turn_transition_theta10_v1\ModernTCN_slope_seed101_out.mat`
  - GRU: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\dual_modern_seed101_full\path_closed_loop_sharp_turn_transition_theta10_v1\GRU_seed101_out.mat`
  - TCN: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\dual_modern_seed101_full\path_closed_loop_sharp_turn_transition_theta10_v1\TCN_seed101_out.mat`
  - ModernTCN_turn_l020_tt25_seed101: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\dual_modern_seed101_full\path_closed_loop_sharp_turn_transition_theta10_v1\ModernTCN_turn_l020_tt25_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_sharp_turn_transition_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN_turn_l020_tt25_seed101 | 9.0000 | 6.0000 | 9.0000 | 24.0000 | 1.0000 |
| GRU | 12.0000 | 7.0000 | 8.0000 | 27.0000 | 2.0000 |
| ModernTCN_slope_seed101 | 15.0000 | 6.0000 | 9.0000 | 30.0000 | 3.0000 |
| TCN | 24.0000 | 11.0000 | 14.0000 | 49.0000 | 4.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN_slope_seed101 | 0.0648 | 0.1914 | 0.0563 | 0.0355 | 0.0238 | 0.7223 | 224.5991 | 1.4763 | 3.1661 | 0.0000 | 0.6220 | 0.7460 | 94.1953 | 61.5220 |
| GRU | 0.0764 | 0.2317 | 0.0398 | 0.0399 | 0.0211 | 0.3464 | 223.0829 | 0.9401 | 6.7454 | 0.0000 | 0.6625 | 0.7635 | 92.6034 | 76.5871 |
| TCN | 0.1603 | 0.3297 | 0.1413 | 0.0932 | 0.0574 | 1.6273 | 354.3902 | 1.4693 | 54.1710 | 0.0000 | 0.9088 | 1.6902 | 83.0907 | 59.6583 |
| ModernTCN_turn_l020_tt25_seed101 | 0.0271 | 0.0632 | 0.0409 | 0.0284 | 0.0235 | 0.5095 | 225.0703 | 0.8204 | 2.2462 | 0.0000 | 0.4333 | 0.5409 | 94.9913 | 48.1460 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN_slope_seed101 | 0.0235 | 0.0485 | 0.0530 | 0.4598 | 0.0000 |
| GRU | 0.0103 | 0.0145 | 0.0201 | 0.0281 | 0.0000 |
| TCN | 0.0099 | 0.0117 | 0.0139 | 0.0763 | 0.0000 |
| ModernTCN_turn_l020_tt25_seed101 | 0.0212 | 0.0233 | 0.0423 | 0.2456 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN_slope_seed101 | 0.0000 | 0.0000 | 0.0971 | 0.0388 | 0.0000 |
| GRU | 0.0000 | 0.0000 | 0.0194 | 0.0000 | 0.0000 |
| TCN | 0.0000 | 0.0000 | 0.2912 | 0.0582 | 0.0000 |
| ModernTCN_turn_l020_tt25_seed101 | 0.0000 | 0.0000 | 0.0194 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN_slope_seed101 | all | 0.0648 | 0.1914 | 0.0563 | 0.0355 | 0.0238 | 1.4763 | 3.1661 | 0.6220 | 0.7460 | 94.1953 | 61.5220 |
| ModernTCN_slope_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002448 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN_slope_seed101 | uphill_left_transition | 0.0600 | 0.1094 | 0.0623 | 0.0432 | 0.0155 | 0.1994 | 1.1750 | 0.8648 | 0.9923 | 93.4444 | 88.9444 |
| ModernTCN_slope_seed101 | downhill_right_transition | 0.0363 | 0.0587 | 0.0490 | 0.0321 | 0.0195 | 0.1683 | 3.5175 | 0.5389 | 0.7087 | 96.0000 | 36.0500 |
| ModernTCN_slope_seed101 | flat_left_exit | 0.1118 | 0.1914 | 0.0675 | 0.0292 | 0.0416 | 1.4763 | 6.8517 | 0.5695 | 0.6390 | 89.9000 | 49.7000 |
| GRU | all | 0.0764 | 0.2317 | 0.0398 | 0.0399 | 0.0211 | 0.9401 | 6.7454 | 0.6625 | 0.7635 | 92.6034 | 76.5871 |
| GRU | startup | 0.0000 | 0.0000 | 0.0000 | 0.1833 | 0.0000 | 0.0002448 | 66.5816 | 1.2893 | 1.0357 | 100.0000 | 100.0000 |
| GRU | uphill_left_transition | 0.0192 | 0.0497 | 0.0131 | 0.0325 | 0.0125 | 0.1791 | 0.1877 | 0.6062 | 0.6545 | 94.7778 | 87.0000 |
| GRU | downhill_right_transition | 0.1194 | 0.2317 | 0.0568 | 0.0448 | 0.0199 | 0.4482 | 16.6614 | 0.6267 | 0.8246 | 94.9500 | 76.6000 |
| GRU | flat_left_exit | 0.0288 | 0.0474 | 0.0373 | 0.0309 | 0.0349 | 0.9401 | 0.6912 | 0.5518 | 0.6907 | 81.4000 | 49.7000 |
| TCN | all | 0.1603 | 0.3297 | 0.1413 | 0.0932 | 0.0574 | 1.4693 | 54.1710 | 0.9088 | 1.6902 | 83.0907 | 59.6583 |
| TCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002448 | 66.3593 | 0.7888 | 0.0000 | 100.0000 | 100.0000 |
| TCN | uphill_left_transition | 0.1716 | 0.3297 | 0.1418 | 0.1213 | 0.0304 | 0.5836 | 77.6261 | 0.9848 | 2.5797 | 81.7222 | 81.3333 |
| TCN | downhill_right_transition | 0.1324 | 0.2725 | 0.1528 | 0.0923 | 0.0732 | 1.0614 | 60.0843 | 0.9487 | 1.8043 | 88.0000 | 42.0000 |
| TCN | flat_left_exit | 0.2104 | 0.2841 | 0.1415 | 0.0319 | 0.0678 | 1.4693 | 18.9271 | 0.6952 | 0.4544 | 69.9000 | 41.9000 |
| ModernTCN_turn_l020_tt25_seed101 | all | 0.0271 | 0.0632 | 0.0409 | 0.0284 | 0.0235 | 0.8204 | 2.2462 | 0.4333 | 0.5409 | 94.9913 | 48.1460 |
| ModernTCN_turn_l020_tt25_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002448 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN_turn_l020_tt25_seed101 | uphill_left_transition | 0.0353 | 0.0632 | 0.0543 | 0.0373 | 0.0266 | 0.1416 | 0.9639 | 0.5754 | 0.7132 | 93.9444 | 61.6111 |
| ModernTCN_turn_l020_tt25_seed101 | downhill_right_transition | 0.0238 | 0.0373 | 0.0341 | 0.0223 | 0.0257 | 0.1568 | 3.8771 | 0.3616 | 0.5344 | 97.4500 | 40.4500 |
| ModernTCN_turn_l020_tt25_seed101 | flat_left_exit | 0.0204 | 0.0365 | 0.0316 | 0.0216 | 0.0158 | 0.8204 | 1.7706 | 0.4733 | 0.4336 | 90.2000 | 21.2000 |
