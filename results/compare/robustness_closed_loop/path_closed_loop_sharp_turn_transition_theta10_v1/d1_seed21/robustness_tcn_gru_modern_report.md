# Robustness closed-loop comparison: path_closed_loop_sharp_turn_transition_theta10_v1_d1_seed21

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\compare\robustness_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\d1_seed21\ModernTCN_out.mat`
  - GRU: `E:\Matlab\Simulink\S-Function_16\results\compare\robustness_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\d1_seed21\GRU_out.mat`
  - TCN: `E:\Matlab\Simulink\S-Function_16\results\compare\robustness_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\d1_seed21\TCN_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_sharp_turn_transition_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 9.0000 | 6.0000 | 4.0000 | 19.0000 | 1.0000 |
| GRU | 10.0000 | 6.0000 | 9.0000 | 25.0000 | 2.0000 |
| TCN | 17.0000 | 6.0000 | 11.0000 | 34.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0787 | 0.3491 | 0.1512 | 0.0902 | 0.0908 | 1.3695 | 716.1214 | 1.4400 | 376.6974 | 0.0000 | 0.9032 | 1.2285 | 89.5554 | 63.2887 |
| GRU | 0.0898 | 0.3313 | 0.1458 | 0.1120 | 0.0756 | 1.4688 | 720.0000 | 1.4400 | 612.0422 | 0.0000 | 0.5941 | 0.6124 | 91.2056 | 50.0291 |
| TCN | 0.0871 | 0.3803 | 0.1648 | 0.1592 | 0.0949 | 1.8704 | 720.0000 | 1.4400 | 1289 | 0.0000 | 0.4827 | 3.5657 | 36.4978 | 58.9400 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0235 | 0.0334 | 0.0471 | 0.2487 | 0.0000 |
| GRU | 0.0120 | 0.0185 | 0.0244 | 0.2296 | 0.0000 |
| TCN | 0.0112 | 0.0174 | 0.0256 | 0.3048 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.4659 | 0.4271 | 3.3780 | 0.4271 | 0.0000 |
| GRU | 1.1260 | 1.0483 | 3.5527 | 1.0678 | 0.0000 |
| TCN | 1.3784 | 1.1648 | 2.9897 | 0.6407 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0787 | 0.3491 | 0.1512 | 0.0902 | 0.0908 | 1.4400 | 376.6974 | 0.9032 | 1.2285 | 89.5554 | 63.2887 |
| ModernTCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.1806 | 0.0000 | 0.0002404 | 61.7529 | 0.0990 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN | uphill_left_transition | 0.0579 | 0.1246 | 0.0881 | 0.0770 | 0.0689 | 0.8131 | 65.9065 | 1.1991 | 2.1037 | 82.0000 | 55.0556 |
| ModernTCN | downhill_right_transition | 0.0278 | 0.0809 | 0.1070 | 0.0647 | 0.0574 | 0.3484 | 54.9445 | 0.5724 | 0.7857 | 93.5000 | 70.8000 |
| ModernTCN | flat_left_exit | 0.1558 | 0.3491 | 0.2843 | 0.1503 | 0.1654 | 1.4400 | 1704 | 1.3052 | 0.9697 | 91.6000 | 50.2000 |
| GRU | all | 0.0898 | 0.3313 | 0.1458 | 0.1120 | 0.0756 | 1.4400 | 612.0422 | 0.5941 | 0.6124 | 91.2056 | 50.0291 |
| GRU | startup | 0.0000 | 0.0000 | 0.0000 | 0.1806 | 0.0000 | 0.0002404 | 61.7529 | 0.0000 | 0.0000 | 100.0000 | 63.0000 |
| GRU | uphill_left_transition | 0.0619 | 0.1214 | 0.0836 | 0.1306 | 0.0567 | 0.7240 | 0.7421 | 0.6709 | 0.6362 | 86.5000 | 37.7778 |
| GRU | downhill_right_transition | 0.1253 | 0.3313 | 0.2059 | 0.1004 | 0.0915 | 1.4400 | 1304 | 0.5820 | 0.7695 | 99.6500 | 59.5500 |
| GRU | flat_left_exit | 0.0567 | 0.1687 | 0.1101 | 0.1162 | 0.0830 | 1.4310 | 542.5357 | 0.6884 | 0.4701 | 79.7000 | 50.3000 |
| TCN | all | 0.0871 | 0.3803 | 0.1648 | 0.1592 | 0.0949 | 1.4400 | 1289 | 0.4827 | 3.5657 | 36.4978 | 58.9400 |
| TCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.1806 | 0.0000 | 0.0002404 | 61.7529 | 0.1479 | 0.0000 | 100.0000 | 100.0000 |
| TCN | uphill_left_transition | 0.0977 | 0.3803 | 0.2290 | 0.1621 | 0.0852 | 1.4400 | 3382 | 0.4510 | 3.6207 | 46.8889 | 55.0556 |
| TCN | downhill_right_transition | 0.0984 | 0.3800 | 0.1482 | 0.1783 | 0.1177 | 1.4400 | 276.0495 | 0.4990 | 4.6156 | 11.5000 | 59.5500 |
| TCN | flat_left_exit | 0.0502 | 0.0901 | 0.0382 | 0.1391 | 0.0752 | 0.7451 | 0.1027 | 0.6172 | 2.6182 | 45.5000 | 50.3000 |
