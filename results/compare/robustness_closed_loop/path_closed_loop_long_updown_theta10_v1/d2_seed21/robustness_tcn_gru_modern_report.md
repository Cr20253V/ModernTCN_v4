# Robustness closed-loop comparison: path_closed_loop_long_updown_theta10_v1_d2_seed21

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\compare\robustness_closed_loop\path_closed_loop_long_updown_theta10_v1\d2_seed21\ModernTCN_out.mat`
  - GRU: `E:\Matlab\Simulink\S-Function_16\results\compare\robustness_closed_loop\path_closed_loop_long_updown_theta10_v1\d2_seed21\GRU_out.mat`
  - TCN: `E:\Matlab\Simulink\S-Function_16\results\compare\robustness_closed_loop\path_closed_loop_long_updown_theta10_v1\d2_seed21\TCN_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_long_updown_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 6.0000 | 5.0000 | 6.0000 | 17.0000 | 1.0000 |
| GRU | 13.0000 | 7.0000 | 6.0000 | 26.0000 | 2.0000 |
| TCN | 17.0000 | 6.0000 | 12.0000 | 35.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0509 | 0.1444 | 0.1052 | 0.1076 | 0.0761 | 1.4871 | 406.5831 | 0.5765 | 46.7042 | 0.0000 | 0.7592 | 1.6007 | 79.3381 | 79.1083 |
| GRU | 0.0824 | 0.2390 | 0.1153 | 0.1458 | 0.0826 | 1.8047 | 291.6001 | 1.2855 | 10.8562 | 0.0000 | 0.9987 | 1.1213 | 88.7842 | 51.6203 |
| TCN | 0.0838 | 0.3300 | 0.1279 | 0.1854 | 0.0859 | 1.5210 | 720.0000 | 1.4400 | 1385 | 0.0000 | 0.6590 | 3.9781 | 38.1292 | 69.2484 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0232 | 0.0334 | 0.0473 | 0.3582 | 0.0000 |
| GRU | 0.0121 | 0.0180 | 0.0230 | 0.0901 | 0.0000 |
| TCN | 0.0109 | 0.0176 | 0.0355 | 0.3809 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| GRU | 0.0000 | 0.0000 | 1.4479 | 0.0000 | 0.0000 |
| TCN | 1.9536 | 1.7697 | 2.5741 | 0.6435 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0509 | 0.1444 | 0.1052 | 0.1076 | 0.0761 | 0.5765 | 46.7042 | 0.7592 | 1.6007 | 79.3381 | 79.1083 |
| ModernTCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.2255 | 0.0000 | 0.0002582 | 95.3354 | 0.0679 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN | uphill_long_entry | 0.0460 | 0.1174 | 0.0720 | 0.1145 | 0.0625 | 0.5357 | 52.9778 | 0.9399 | 2.3981 | 74.0769 | 66.2308 |
| ModernTCN | downhill_transition | 0.0378 | 0.1063 | 0.0976 | 0.0965 | 0.0603 | 0.3944 | 50.8849 | 0.5652 | 0.6670 | 96.3077 | 83.8462 |
| ModernTCN | uphill_return | 0.0586 | 0.1252 | 0.1471 | 0.1438 | 0.0884 | 0.4437 | 53.8485 | 0.7134 | 2.6742 | 60.6000 | 80.7000 |
| ModernTCN | flat_recovery | 0.0801 | 0.1444 | 0.1220 | 0.0230 | 0.1232 | 0.5765 | 27.9207 | 1.2253 | 0.6111 | 76.0000 | 86.6000 |
| GRU | all | 0.0824 | 0.2390 | 0.1153 | 0.1458 | 0.0826 | 1.2855 | 10.8562 | 0.9987 | 1.1213 | 88.7842 | 51.6203 |
| GRU | startup | 0.0000 | 0.0000 | 0.0000 | 0.2255 | 0.0000 | 0.0002582 | 95.3354 | 0.0000 | 0.0000 | 100.0000 | 63.0000 |
| GRU | uphill_long_entry | 0.0656 | 0.1412 | 0.0552 | 0.1752 | 0.0699 | 0.8629 | 1.0336 | 1.1462 | 1.1240 | 85.8462 | 35.2308 |
| GRU | downhill_transition | 0.0977 | 0.2390 | 0.1599 | 0.0968 | 0.0780 | 1.2855 | 11.3601 | 0.9128 | 1.2489 | 97.4615 | 65.4615 |
| GRU | uphill_return | 0.0934 | 0.1675 | 0.1118 | 0.1659 | 0.0971 | 0.9754 | 29.4636 | 1.2791 | 1.1271 | 77.9000 | 36.4000 |
| GRU | flat_recovery | 0.0752 | 0.1223 | 0.1272 | 0.1587 | 0.1095 | 0.8601 | 2.4847 | 0.7780 | 1.3334 | 90.2000 | 86.6000 |
| TCN | all | 0.0838 | 0.3300 | 0.1279 | 0.1854 | 0.0859 | 1.4400 | 1385 | 0.6590 | 3.9781 | 38.1292 | 69.2484 |
| TCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.2255 | 0.0000 | 0.0002582 | 95.3354 | 0.0736 | 0.0000 | 100.0000 | 100.0000 |
| TCN | uphill_long_entry | 0.0821 | 0.3178 | 0.1895 | 0.1896 | 0.0924 | 1.4400 | 2233 | 0.6522 | 4.2984 | 53.6923 | 66.2308 |
| TCN | downhill_transition | 0.1165 | 0.3300 | 0.0988 | 0.1986 | 0.1020 | 1.4400 | 2179 | 0.5051 | 4.6876 | 12.1538 | 65.4615 |
| TCN | uphill_return | 0.0370 | 0.1175 | 0.0717 | 0.1963 | 0.0460 | 0.4190 | 189.1599 | 0.9297 | 4.2840 | 26.5000 | 61.7000 |
| TCN | flat_recovery | 0.0749 | 0.1234 | 0.1153 | 0.1591 | 0.1032 | 0.8019 | 100.7928 | 0.8213 | 2.6857 | 57.4000 | 86.6000 |
