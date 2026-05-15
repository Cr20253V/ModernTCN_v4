# Robustness nominal comparison: path_closed_loop_long_updown_theta10_v1_d0_seed0

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\compare\multipath_closed_loop\path_closed_loop_long_updown_theta10_v1\ModernTCN_out.mat`
  - GRU: `E:\Matlab\Simulink\S-Function_16\results\compare\multipath_closed_loop\path_closed_loop_long_updown_theta10_v1\GRU_out.mat`
  - TCN: `E:\Matlab\Simulink\S-Function_16\results\compare\multipath_closed_loop\path_closed_loop_long_updown_theta10_v1\TCN_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_long_updown_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 6.0000 | 6.0000 | 6.0000 | 18.0000 | 1.0000 |
| GRU | 13.0000 | 6.0000 | 6.0000 | 25.0000 | 2.0000 |
| TCN | 17.0000 | 6.0000 | 12.0000 | 35.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0334 | 0.0899 | 0.0207 | 0.0637 | 0.0181 | 0.3157 | 272.7438 | 0.1523 | 14.2368 | 0.0000 | 0.7748 | 1.0376 | 93.1740 | 77.4764 |
| GRU | 0.0442 | 0.1218 | 0.0366 | 0.0970 | 0.0512 | 0.5972 | 272.1952 | 0.9641 | 1.6069 | 0.0000 | 0.3770 | 0.6672 | 85.9113 | 66.8352 |
| TCN | 0.0487 | 0.1122 | 0.0453 | 0.1315 | 0.0570 | 0.8547 | 377.5943 | 1.3050 | 46.7564 | 0.0000 | 0.5716 | 1.8113 | 75.1322 | 78.2809 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0241 | 0.0353 | 0.0462 | 2.0725 | 0.0000 |
| GRU | 0.0125 | 0.0186 | 0.0227 | 0.4005 | 0.0000 |
| TCN | 0.0114 | 0.0169 | 0.0217 | 0.5055 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| GRU | 0.0000 | 0.0000 | 0.6435 | 0.0000 | 0.0000 |
| TCN | 0.0000 | 0.0000 | 0.8274 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0334 | 0.0899 | 0.0207 | 0.0637 | 0.0181 | 0.1523 | 14.2368 | 0.7748 | 1.0376 | 93.1740 | 77.4764 |
| ModernTCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.2215 | 0.0000 | 0.0002577 | 94.2247 | 0.0090 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN | uphill_long_entry | 0.0446 | 0.0899 | 0.0198 | 0.0562 | 0.0157 | 0.1295 | 2.5075 | 1.0268 | 1.4363 | 94.2308 | 66.2308 |
| ModernTCN | downhill_transition | 0.0331 | 0.0665 | 0.0201 | 0.0776 | 0.0192 | 0.1523 | 37.8321 | 0.5544 | 0.8263 | 93.0769 | 87.8462 |
| ModernTCN | uphill_return | 0.0223 | 0.0566 | 0.0264 | 0.0727 | 0.0196 | 0.1283 | 2.3006 | 0.8707 | 1.1881 | 89.0000 | 68.4000 |
| ModernTCN | flat_recovery | 0.0266 | 0.0480 | 0.0165 | 0.0171 | 0.0222 | 0.1211 | 13.6889 | 0.8843 | 0.7702 | 95.6000 | 86.6000 |
| GRU | all | 0.0442 | 0.1218 | 0.0366 | 0.0970 | 0.0512 | 0.9641 | 1.6069 | 0.3770 | 0.6672 | 85.9113 | 66.8352 |
| GRU | startup | 0.0000 | 0.0000 | 0.0000 | 0.2215 | 0.0000 | 0.0002577 | 94.2247 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| GRU | uphill_long_entry | 0.0457 | 0.0998 | 0.0271 | 0.1022 | 0.0520 | 0.5807 | 0.8181 | 0.5004 | 0.6820 | 91.5385 | 82.0000 |
| GRU | downhill_transition | 0.0587 | 0.1218 | 0.0451 | 0.0853 | 0.0578 | 0.9641 | 2.7851 | 0.3705 | 0.6906 | 91.1538 | 89.3077 |
| GRU | uphill_return | 0.0303 | 0.0656 | 0.0326 | 0.1069 | 0.0512 | 0.4231 | 1.3904 | 0.4023 | 0.7435 | 85.7000 | 33.7000 |
| GRU | flat_recovery | 0.0283 | 0.0621 | 0.0487 | 0.1118 | 0.0427 | 0.1280 | 1.0508 | 0.2116 | 0.7503 | 51.2000 | 18.6000 |
| TCN | all | 0.0487 | 0.1122 | 0.0453 | 0.1315 | 0.0570 | 1.3050 | 46.7564 | 0.5716 | 1.8113 | 75.1322 | 78.2809 |
| TCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.2215 | 0.0000 | 0.0002577 | 94.2247 | 0.0198 | 0.0000 | 100.0000 | 100.0000 |
| TCN | uphill_long_entry | 0.0458 | 0.0885 | 0.0200 | 0.1202 | 0.0353 | 0.7337 | 41.0682 | 0.3165 | 1.5844 | 79.0000 | 80.8462 |
| TCN | downhill_transition | 0.0553 | 0.1122 | 0.0448 | 0.1453 | 0.0599 | 1.3050 | 66.8326 | 0.6383 | 2.7437 | 60.7692 | 79.8462 |
| TCN | uphill_return | 0.0499 | 0.1109 | 0.0520 | 0.1381 | 0.0671 | 0.7933 | 43.3738 | 0.8347 | 1.7750 | 75.0000 | 68.4000 |
| TCN | flat_recovery | 0.0472 | 0.1076 | 0.0788 | 0.1391 | 0.0821 | 0.4080 | 39.0563 | 0.8099 | 0.9588 | 90.2000 | 76.4000 |
