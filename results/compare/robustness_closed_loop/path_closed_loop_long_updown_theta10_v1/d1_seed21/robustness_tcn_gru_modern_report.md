# Robustness closed-loop comparison: path_closed_loop_long_updown_theta10_v1_d1_seed21

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\compare\robustness_closed_loop\path_closed_loop_long_updown_theta10_v1\d1_seed21\ModernTCN_out.mat`
  - GRU: `E:\Matlab\Simulink\S-Function_16\results\compare\robustness_closed_loop\path_closed_loop_long_updown_theta10_v1\d1_seed21\GRU_out.mat`
  - TCN: `E:\Matlab\Simulink\S-Function_16\results\compare\robustness_closed_loop\path_closed_loop_long_updown_theta10_v1\d1_seed21\TCN_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_long_updown_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 11.0000 | 6.0000 | 6.0000 | 23.0000 | 1.0000 |
| TCN | 9.0000 | 6.0000 | 11.0000 | 26.0000 | 2.0000 |
| GRU | 16.0000 | 6.0000 | 7.0000 | 29.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0450 | 0.1245 | 0.0857 | 0.0913 | 0.0667 | 1.2066 | 376.0155 | 0.6224 | 34.8575 | 0.0000 | 0.8218 | 1.5460 | 80.3953 | 79.1542 |
| GRU | 0.0632 | 0.1838 | 0.0829 | 0.1259 | 0.0729 | 1.3060 | 286.6959 | 1.0925 | 2.5825 | 0.0000 | 0.7424 | 0.9779 | 88.1407 | 52.7925 |
| TCN | 0.0502 | 0.1227 | 0.0561 | 0.1672 | 0.0570 | 0.9784 | 587.4751 | 0.8836 | 49.5855 | 0.0000 | 0.6280 | 3.0786 | 50.4252 | 68.0533 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0239 | 0.0388 | 0.0485 | 1.8599 | 0.0000 |
| GRU | 0.0133 | 0.0209 | 0.0252 | 0.3485 | 0.0000 |
| TCN | 0.0106 | 0.0154 | 0.0200 | 0.3666 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0460 | 0.0000 | 0.0000 |
| GRU | 0.0000 | 0.0000 | 1.1262 | 0.0000 | 0.0000 |
| TCN | 0.0000 | 0.0000 | 0.6205 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0450 | 0.1245 | 0.0857 | 0.0913 | 0.0667 | 0.6224 | 34.8575 | 0.8218 | 1.5460 | 80.3953 | 79.1542 |
| ModernTCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.2235 | 0.0000 | 0.000258 | 94.7769 | 0.0259 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN | uphill_long_entry | 0.0423 | 0.0954 | 0.0453 | 0.0860 | 0.0315 | 0.1408 | 58.2935 | 1.0724 | 2.0735 | 82.3077 | 66.2308 |
| ModernTCN | downhill_transition | 0.0315 | 0.1002 | 0.0745 | 0.0784 | 0.0521 | 0.5394 | 44.7707 | 0.4207 | 0.7185 | 92.3846 | 78.6154 |
| ModernTCN | uphill_return | 0.0523 | 0.1066 | 0.1295 | 0.1348 | 0.0922 | 0.6224 | 12.6127 | 1.0639 | 2.7139 | 56.8000 | 87.7000 |
| ModernTCN | flat_recovery | 0.0700 | 0.1245 | 0.1031 | 0.0197 | 0.1097 | 0.4709 | 9.4574 | 1.1255 | 0.7663 | 81.6000 | 86.6000 |
| GRU | all | 0.0632 | 0.1838 | 0.0829 | 0.1259 | 0.0729 | 1.0925 | 2.5825 | 0.7424 | 0.9779 | 88.1407 | 52.7925 |
| GRU | startup | 0.0000 | 0.0000 | 0.0000 | 0.2235 | 0.0000 | 0.000258 | 94.7769 | 0.0000 | 0.0000 | 100.0000 | 57.6667 |
| GRU | uphill_long_entry | 0.0562 | 0.1224 | 0.0422 | 0.1467 | 0.0657 | 0.7105 | 0.8446 | 0.7889 | 0.8869 | 87.3846 | 37.4615 |
| GRU | downhill_transition | 0.0757 | 0.1838 | 0.1147 | 0.0884 | 0.0607 | 1.0925 | 4.6162 | 0.7658 | 1.1074 | 98.4615 | 65.4615 |
| GRU | uphill_return | 0.0660 | 0.1270 | 0.0764 | 0.1439 | 0.0850 | 0.7827 | 2.8095 | 0.8952 | 1.1242 | 75.9000 | 40.2000 |
| GRU | flat_recovery | 0.0536 | 0.1092 | 0.0961 | 0.1405 | 0.1051 | 0.6305 | 1.8257 | 0.6271 | 1.0760 | 82.0000 | 86.6000 |
| TCN | all | 0.0502 | 0.1227 | 0.0561 | 0.1672 | 0.0570 | 0.8836 | 49.5855 | 0.6280 | 3.0786 | 50.4252 | 68.0533 |
| TCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.2235 | 0.0000 | 0.000258 | 94.7769 | 0.0864 | 0.0000 | 100.0000 | 100.0000 |
| TCN | uphill_long_entry | 0.0401 | 0.1101 | 0.0582 | 0.1642 | 0.0511 | 0.6093 | 85.2862 | 0.4193 | 3.2351 | 58.0000 | 66.2308 |
| TCN | downhill_transition | 0.0588 | 0.1227 | 0.0397 | 0.1933 | 0.0506 | 0.7792 | 10.3627 | 0.5651 | 4.3845 | 22.4615 | 65.4615 |
| TCN | uphill_return | 0.0545 | 0.1209 | 0.0555 | 0.1780 | 0.0663 | 0.8836 | 11.9542 | 1.0262 | 2.7669 | 58.0000 | 56.5000 |
| TCN | flat_recovery | 0.0528 | 0.1187 | 0.0912 | 0.1101 | 0.0776 | 0.4434 | 158.4663 | 0.8006 | 1.4455 | 63.4000 | 86.6000 |
