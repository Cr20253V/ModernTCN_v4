# ModernTCN、GRU、TCN 与 LPV-MPC theta 基线闭环对比报告

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\compare\multipath_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\ModernTCN_out.mat`
  - GRU: `E:\Matlab\Simulink\S-Function_16\results\compare\multipath_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\GRU_out.mat`
  - TCN: `E:\Matlab\Simulink\S-Function_16\results\compare\multipath_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\TCN_out.mat`
  - LPV-MPC_theta0: `E:\Matlab\Simulink\S-Function_16\results\compare\multipath_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\lpvmpc_theta0_out.mat`
  - LPV-MPC_IMU_theta: `E:\Matlab\Simulink\S-Function_16\results\compare\multipath_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\lpvmpc_imu_theta_out.mat`
  - LPV-MPC_oracle_theta: `E:\Matlab\Simulink\S-Function_16\results\compare\multipath_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\lpvmpc_oracle_theta_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_sharp_turn_transition_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 11.0000 | 6.0000 | 10.0000 | 27.0000 | 1.0000 |
| LPV-MPC_oracle_theta | 9.0000 | 13.0000 | 7.0000 | 29.0000 | 2.0000 |
| GRU | 16.0000 | 7.0000 | 8.0000 | 31.0000 | 3.0000 |
| TCN | 24.0000 | 8.0000 | 15.0000 | 47.0000 | 4.0000 |
| LPV-MPC_IMU_theta | 30.0000 | 15.0000 | 23.0000 | 68.0000 | 5.0000 |
| LPV-MPC_theta0 | 36.0000 | 14.0000 | 21.0000 | 71.0000 | 6.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0377 | 0.1039 | 0.0318 | 0.0664 | 0.0500 | 0.3474 | 320.1627 | 0.7956 | 25.1041 | 0.0000 | 0.8176 | 0.9286 | 95.9619 | 78.9944 |
| GRU | 0.0383 | 0.1199 | 0.0474 | 0.0700 | 0.0310 | 0.5459 | 264.3291 | 0.7295 | 1.4217 | 0.0000 | 0.3054 | 0.3833 | 92.1957 | 71.4230 |
| TCN | 0.0617 | 0.1794 | 0.0929 | 0.1090 | 0.0650 | 1.0000 | 717.0488 | 1.4321 | 659.3289 | 0.0000 | 0.4404 | 1.8116 | 71.9666 | 76.1600 |
| LPV-MPC_theta0 | 0.1282 | 0.5341 | 0.2420 | 0.1632 | 0.1114 | 2.6472 | 720.0000 | 1.4400 | 939.0447 | 0.0012 | 3.9210 | 3.9210 | 23.3159 | 58.9400 |
| LPV-MPC_IMU_theta | 0.1119 | 0.4600 | 0.2224 | 0.1534 | 0.1013 | 2.4908 | 720.0000 | 1.4400 | 814.1368 | 0.0016 | 3.6779 | 3.6782 | 23.3159 | 58.9400 |
| LPV-MPC_oracle_theta | 0.0403 | 0.1050 | 0.0267 | 0.0149 | 0.0195 | 0.3212 | 222.7421 | 0.2227 | 0.3546 | 0.0000 | 0.0042 | 0.1537 | 23.3159 | 58.9400 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0245 | 0.0445 | 0.0496 | 2.1766 | 0.0000 |
| GRU | 0.0146 | 0.0229 | 0.0258 | 0.4621 | 0.0000 |
| TCN | 0.0119 | 0.0177 | 0.0221 | 0.3826 | 0.0000 |
| LPV-MPC_theta0 | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_IMU_theta | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_oracle_theta | NaN | NaN | NaN | NaN | NaN |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.6212 | 0.0000 | 0.0000 |
| GRU | 0.0000 | 0.0000 | 0.1941 | 0.0000 | 0.0000 |
| TCN | 0.5436 | 0.4853 | 1.9414 | 0.1747 | 0.0000 |
| LPV-MPC_theta0 | 0.9901 | 0.8736 | 4.9699 | 0.4465 | 0.0012 |
| LPV-MPC_IMU_theta | 1.2813 | 1.0872 | 4.0769 | 0.4659 | 0.0016 |
| LPV-MPC_oracle_theta | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0377 | 0.1039 | 0.0318 | 0.0664 | 0.0500 | 0.7956 | 25.1041 | 0.8176 | 0.9286 | 95.9619 | 78.9944 |
| ModernTCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.1790 | 0.0000 | 0.0002402 | 61.3786 | 0.0304 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN | uphill_left_transition | 0.0557 | 0.1039 | 0.0257 | 0.0446 | 0.0657 | 0.7956 | 6.7432 | 1.0050 | 1.3143 | 95.3333 | 73.4444 |
| ModernTCN | downhill_right_transition | 0.0278 | 0.0654 | 0.0264 | 0.0692 | 0.0432 | 0.5449 | 15.8327 | 0.7381 | 0.9808 | 96.1500 | 80.0500 |
| ModernTCN | flat_left_exit | 0.0133 | 0.0338 | 0.0511 | 0.0965 | 0.0376 | 0.1704 | 85.2547 | 0.9131 | 0.4560 | 95.3000 | 79.5000 |
| GRU | all | 0.0383 | 0.1199 | 0.0474 | 0.0700 | 0.0310 | 0.7295 | 1.4217 | 0.3054 | 0.3833 | 92.1957 | 71.4230 |
| GRU | startup | 0.0000 | 0.0000 | 0.0000 | 0.1790 | 0.0000 | 0.0002402 | 61.3786 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| GRU | uphill_left_transition | 0.0449 | 0.0909 | 0.0333 | 0.0739 | 0.0302 | 0.4970 | 1.4330 | 0.4133 | 0.5247 | 93.6667 | 84.0556 |
| GRU | downhill_right_transition | 0.0428 | 0.1199 | 0.0673 | 0.0778 | 0.0368 | 0.7295 | 2.0996 | 0.2625 | 0.4175 | 92.2500 | 80.5500 |
| GRU | flat_left_exit | 0.0160 | 0.0369 | 0.0232 | 0.0553 | 0.0243 | 0.1585 | 0.2135 | 0.3044 | 0.1949 | 86.7000 | 20.4000 |
| TCN | all | 0.0617 | 0.1794 | 0.0929 | 0.1090 | 0.0650 | 1.4321 | 659.3289 | 0.4404 | 1.8116 | 71.9666 | 76.1600 |
| TCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.1790 | 0.0000 | 0.0002402 | 61.3786 | 0.0365 | 0.0000 | 100.0000 | 100.0000 |
| TCN | uphill_left_transition | 0.0508 | 0.1058 | 0.0243 | 0.1011 | 0.0498 | 0.7223 | 49.0153 | 0.3509 | 1.5216 | 82.8333 | 74.0000 |
| TCN | downhill_right_transition | 0.0538 | 0.1106 | 0.0950 | 0.1419 | 0.0628 | 0.8654 | 45.3687 | 0.5456 | 2.7687 | 51.6500 | 88.8000 |
| TCN | flat_left_exit | 0.0959 | 0.1794 | 0.1592 | 0.0483 | 0.0969 | 1.4321 | 3220 | 0.5305 | 1.0555 | 83.2000 | 46.4000 |
| LPV-MPC_theta0 | all | 0.1282 | 0.5341 | 0.2420 | 0.1632 | 0.1114 | 1.4400 | 939.0447 | 3.9210 | 3.9210 | 23.3159 | 58.9400 |
| LPV-MPC_theta0 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1790 | 0.0000 | 0.0002402 | 61.3786 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| LPV-MPC_theta0 | uphill_left_transition | 0.1214 | 0.5080 | 0.3134 | 0.1877 | 0.0932 | 1.0716 | 642.9342 | 4.5726 | 4.5726 | 13.6667 | 55.0556 |
| LPV-MPC_theta0 | downhill_right_transition | 0.1661 | 0.5341 | 0.2369 | 0.1677 | 0.1486 | 1.4400 | 1840 | 4.6741 | 4.6741 | 7.7500 | 59.5500 |
| LPV-MPC_theta0 | flat_left_exit | 0.0544 | 0.0966 | 0.1124 | 0.1310 | 0.0640 | 0.2217 | 0.1266 | 2.6182 | 2.6182 | 44.9000 | 50.3000 |
| LPV-MPC_IMU_theta | all | 0.1119 | 0.4600 | 0.2224 | 0.1534 | 0.1013 | 1.4400 | 814.1368 | 3.6779 | 3.6782 | 23.3159 | 58.9400 |
| LPV-MPC_IMU_theta | startup | 0.0000 | 0.0000 | 0.0000 | 0.1790 | 0.0000 | 0.0002402 | 61.3786 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| LPV-MPC_IMU_theta | uphill_left_transition | 0.1114 | 0.4517 | 0.2850 | 0.1766 | 0.0912 | 0.9376 | 673.7052 | 4.3033 | 4.3105 | 13.6667 | 55.0556 |
| LPV-MPC_IMU_theta | downhill_right_transition | 0.1402 | 0.4600 | 0.2201 | 0.1580 | 0.1305 | 1.4400 | 1411 | 4.3718 | 4.3732 | 7.7500 | 59.5500 |
| LPV-MPC_IMU_theta | flat_left_exit | 0.0537 | 0.0951 | 0.1076 | 0.1222 | 0.0616 | 0.2193 | 0.1102 | 2.4552 | 2.4412 | 44.9000 | 50.3000 |
| LPV-MPC_oracle_theta | all | 0.0403 | 0.1050 | 0.0267 | 0.0149 | 0.0195 | 0.2227 | 0.3546 | 0.0042 | 0.1537 | 23.3159 | 58.9400 |
| LPV-MPC_oracle_theta | startup | 0.0000 | 0.0000 | 0.0000 | 0.1790 | 0.0000 | 0.0002402 | 61.3786 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| LPV-MPC_oracle_theta | uphill_left_transition | 0.0512 | 0.1050 | 0.0321 | 0.0096 | 0.0198 | 0.2227 | 0.2107 | 0.0031 | 0.1131 | 13.6667 | 55.0556 |
| LPV-MPC_oracle_theta | downhill_right_transition | 0.0340 | 0.0819 | 0.0210 | 0.0163 | 0.0169 | 0.1766 | 0.4488 | 0.0053 | 0.1980 | 7.7500 | 59.5500 |
| LPV-MPC_oracle_theta | flat_left_exit | 0.0364 | 0.0549 | 0.0306 | 0.0143 | 0.0260 | 0.1402 | 0.2172 | 0.0052 | 0.1924 | 44.9000 | 50.3000 |
