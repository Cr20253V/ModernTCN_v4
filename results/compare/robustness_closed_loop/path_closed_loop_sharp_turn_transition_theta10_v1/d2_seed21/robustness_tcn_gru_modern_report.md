# Robustness closed-loop comparison: path_closed_loop_sharp_turn_transition_theta10_v1_d2_seed21

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\compare\robustness_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\d2_seed21\ModernTCN_out.mat`
  - GRU: `E:\Matlab\Simulink\S-Function_16\results\compare\robustness_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\d2_seed21\GRU_out.mat`
  - TCN: `E:\Matlab\Simulink\S-Function_16\results\compare\robustness_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\d2_seed21\TCN_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_sharp_turn_transition_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 9.0000 | 5.0000 | 10.0000 | 24.0000 | 1.0000 |
| GRU | 15.0000 | 7.0000 | 5.0000 | 27.0000 | 2.0000 |
| TCN | 12.0000 | 6.0000 | 9.0000 | 27.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.1130 | 0.5099 | 0.1986 | 0.1006 | 0.1102 | 1.8304 | 720.0000 | 1.4400 | 1373 | 0.0000 | 0.8199 | 1.3139 | 86.2163 | 62.1821 |
| GRU | 0.1516 | 0.5346 | 0.2075 | 0.1762 | 0.1077 | 1.9636 | 718.6617 | 1.4400 | 573.5052 | 0.0000 | 0.9517 | 0.9634 | 91.4580 | 50.3203 |
| TCN | 0.1075 | 0.5065 | 0.2036 | 0.1686 | 0.1136 | 2.1984 | 720.0000 | 1.4400 | 818.6660 | 0.0000 | 0.6062 | 3.6749 | 30.3436 | 58.9400 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0236 | 0.0351 | 0.0483 | 0.3103 | 0.0000 |
| GRU | 0.0123 | 0.0193 | 0.0250 | 0.3375 | 0.0000 |
| TCN | 0.0112 | 0.0172 | 0.0229 | 0.2219 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 1.5919 | 1.4172 | 4.8146 | 1.8831 | 0.0000 |
| GRU | 2.2132 | 2.1743 | 11.1629 | 1.6890 | 0.0000 |
| TCN | 1.2813 | 1.2036 | 4.8923 | 0.7765 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.1130 | 0.5099 | 0.1986 | 0.1006 | 0.1102 | 1.4400 | 1373 | 0.8199 | 1.3139 | 86.2163 | 62.1821 |
| ModernTCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.1822 | 0.0000 | 0.0002407 | 62.1324 | 0.0721 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN | uphill_left_transition | 0.0559 | 0.1180 | 0.1294 | 0.1093 | 0.0699 | 0.7022 | 83.1059 | 0.9876 | 2.4335 | 70.5556 | 55.0556 |
| ModernTCN | downhill_right_transition | 0.0540 | 0.1651 | 0.1693 | 0.0685 | 0.0838 | 0.5534 | 199.1307 | 0.5825 | 0.7709 | 94.0500 | 67.9000 |
| ModernTCN | flat_left_exit | 0.2326 | 0.5099 | 0.3400 | 0.1447 | 0.1992 | 1.4400 | 6524 | 1.2481 | 0.8458 | 93.9000 | 50.3000 |
| GRU | all | 0.1516 | 0.5346 | 0.2075 | 0.1762 | 0.1077 | 1.4400 | 573.5052 | 0.9517 | 0.9634 | 91.4580 | 50.3203 |
| GRU | startup | 0.0000 | 0.0000 | 0.0000 | 0.1822 | 0.0000 | 0.0002407 | 62.1324 | 0.0000 | 0.0000 | 100.0000 | 65.2500 |
| GRU | uphill_left_transition | 0.0808 | 0.1484 | 0.1090 | 0.1684 | 0.0807 | 0.9293 | 0.7996 | 1.2674 | 1.1398 | 85.8889 | 38.1111 |
| GRU | downhill_right_transition | 0.2204 | 0.5346 | 0.2929 | 0.1452 | 0.1134 | 1.4400 | 855.7338 | 0.8631 | 1.0762 | 97.6000 | 59.5500 |
| GRU | flat_left_exit | 0.0969 | 0.2320 | 0.1696 | 0.2576 | 0.1493 | 1.4135 | 1241 | 0.8944 | 0.7586 | 86.2000 | 50.3000 |
| TCN | all | 0.1075 | 0.5065 | 0.2036 | 0.1686 | 0.1136 | 1.4400 | 818.6660 | 0.6062 | 3.6749 | 30.3436 | 58.9400 |
| TCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.1822 | 0.0000 | 0.0002407 | 62.1324 | 0.2121 | 0.0000 | 100.0000 | 100.0000 |
| TCN | uphill_left_transition | 0.1101 | 0.4965 | 0.2808 | 0.1836 | 0.0912 | 1.4400 | 1440 | 0.6490 | 3.9981 | 30.1111 | 55.0556 |
| TCN | downhill_right_transition | 0.1346 | 0.5065 | 0.1870 | 0.1802 | 0.1533 | 1.4400 | 811.1843 | 0.6167 | 4.5572 | 11.0500 | 59.5500 |
| TCN | flat_left_exit | 0.0382 | 0.0679 | 0.0400 | 0.1431 | 0.0667 | 0.4850 | 0.0807 | 0.6355 | 2.6182 | 44.9000 | 50.3000 |
