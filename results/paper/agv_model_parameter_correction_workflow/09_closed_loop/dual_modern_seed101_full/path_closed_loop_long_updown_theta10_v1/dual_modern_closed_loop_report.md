# Dual ModernTCN seed101 plantfix closed-loop comparison

- 输出文件：
  - ModernTCN_slope_seed101: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\dual_modern_seed101_full\path_closed_loop_long_updown_theta10_v1\ModernTCN_slope_seed101_out.mat`
  - GRU: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\dual_modern_seed101_full\path_closed_loop_long_updown_theta10_v1\GRU_seed101_out.mat`
  - TCN: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\dual_modern_seed101_full\path_closed_loop_long_updown_theta10_v1\TCN_seed101_out.mat`
  - ModernTCN_turn_l020_tt25_seed101: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\dual_modern_seed101_full\path_closed_loop_long_updown_theta10_v1\ModernTCN_turn_l020_tt25_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_long_updown_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| GRU | 8.0000 | 3.0000 | 6.0000 | 17.0000 | 1.0000 |
| ModernTCN_turn_l020_tt25_seed101 | 11.0000 | 6.0000 | 9.0000 | 26.0000 | 2.0000 |
| ModernTCN_slope_seed101 | 17.0000 | 9.0000 | 10.0000 | 36.0000 | 3.0000 |
| TCN | 24.0000 | 12.0000 | 15.0000 | 51.0000 | 4.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN_slope_seed101 | 0.0448 | 0.1303 | 0.0423 | 0.0596 | 0.0267 | 0.8434 | 325.8510 | 0.4296 | 7.8324 | 0.0000 | 0.8746 | 1.2181 | 91.0825 | 44.5875 |
| GRU | 0.0379 | 0.1090 | 0.0189 | 0.0437 | 0.0150 | 0.2064 | 263.1554 | 0.2555 | 0.6778 | 0.0000 | 0.6832 | 0.9209 | 91.1055 | 59.7564 |
| TCN | 0.1614 | 0.4647 | 0.0806 | 0.1219 | 0.0427 | 1.6340 | 424.8203 | 1.4987 | 439.0723 | 0.0000 | 1.2364 | 2.5506 | 74.8793 | 36.2216 |
| ModernTCN_turn_l020_tt25_seed101 | 0.0337 | 0.0853 | 0.0390 | 0.0545 | 0.0268 | 0.7147 | 322.8705 | 0.2219 | 7.6134 | 0.0000 | 0.7058 | 1.0659 | 91.1055 | 47.7591 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN_slope_seed101 | 0.0420 | 0.0462 | 0.0495 | 0.7427 | 0.0000 |
| GRU | 0.0177 | 0.0206 | 0.0232 | 0.1197 | 0.0000 |
| TCN | 0.0131 | 0.0175 | 0.0189 | 0.1591 | 0.0000 |
| ModernTCN_turn_l020_tt25_seed101 | 0.0418 | 0.0474 | 0.0516 | 0.4370 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN_slope_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| GRU | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| TCN | 0.0000 | 0.0000 | 0.2528 | 0.0460 | 0.0000 |
| ModernTCN_turn_l020_tt25_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN_slope_seed101 | all | 0.0448 | 0.1303 | 0.0423 | 0.0596 | 0.0267 | 0.4296 | 7.8324 | 0.8746 | 1.2181 | 91.0825 | 44.5875 |
| ModernTCN_slope_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002627 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN_slope_seed101 | uphill_long_entry | 0.0426 | 0.0872 | 0.0482 | 0.0755 | 0.0226 | 0.1118 | 9.2555 | 1.0891 | 1.4823 | 87.2308 | 84.2308 |
| ModernTCN_slope_seed101 | downhill_transition | 0.0186 | 0.0316 | 0.0331 | 0.0468 | 0.0173 | 0.1939 | 7.7214 | 0.6632 | 0.9569 | 93.7692 | 27.6154 |
| ModernTCN_slope_seed101 | uphill_return | 0.0593 | 0.1200 | 0.0361 | 0.0691 | 0.0261 | 0.0813 | 3.1527 | 1.3090 | 1.8099 | 88.2000 | 16.9000 |
| ModernTCN_slope_seed101 | flat_recovery | 0.0694 | 0.1303 | 0.0639 | 0.0211 | 0.0522 | 0.4296 | 17.0130 | 0.4372 | 0.6379 | 95.4000 | 13.4000 |
| GRU | all | 0.0379 | 0.1090 | 0.0189 | 0.0437 | 0.0150 | 0.2555 | 0.6778 | 0.6832 | 0.9209 | 91.1055 | 59.7564 |
| GRU | startup | 0.0000 | 0.0000 | 0.0000 | 0.2201 | 0.0000 | 0.0002627 | 102.0977 | 0.8666 | 0.5652 | 100.0000 | 100.0000 |
| GRU | uphill_long_entry | 0.0103 | 0.0260 | 0.0123 | 0.0316 | 0.0084 | 0.1174 | 0.1493 | 0.5011 | 0.5675 | 93.5385 | 81.5385 |
| GRU | downhill_transition | 0.0537 | 0.1090 | 0.0221 | 0.0566 | 0.0116 | 0.2555 | 1.0320 | 0.8704 | 1.2234 | 91.8462 | 74.8462 |
| GRU | uphill_return | 0.0477 | 0.0790 | 0.0244 | 0.0246 | 0.0218 | 0.1563 | 0.7599 | 0.2767 | 0.7130 | 85.7000 | 25.0000 |
| GRU | flat_recovery | 0.0149 | 0.0261 | 0.0162 | 0.0568 | 0.0216 | 0.1548 | 0.3936 | 1.3008 | 1.5873 | 89.2000 | 13.4000 |
| TCN | all | 0.1614 | 0.4647 | 0.0806 | 0.1219 | 0.0427 | 1.4987 | 439.0723 | 1.2364 | 2.5506 | 74.8793 | 36.2216 |
| TCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002627 | 101.8309 | 0.3538 | 0.0000 | 100.0000 | 100.0000 |
| TCN | uphill_long_entry | 0.1398 | 0.2983 | 0.0799 | 0.1468 | 0.0222 | 0.4116 | 884.5676 | 0.9985 | 3.4332 | 72.0000 | 71.1538 |
| TCN | downhill_transition | 0.0757 | 0.1611 | 0.0838 | 0.0760 | 0.0422 | 0.2973 | 202.8594 | 1.6549 | 1.6727 | 91.1538 | 17.8462 |
| TCN | uphill_return | 0.1479 | 0.3678 | 0.0752 | 0.1493 | 0.0683 | 0.4745 | 442.9311 | 0.9259 | 3.4260 | 73.1000 | 15.2000 |
| TCN | flat_recovery | 0.3424 | 0.4647 | 0.1019 | 0.1151 | 0.0244 | 1.4987 | 109.2595 | 1.7951 | 2.0677 | 31.2000 | 3.4000 |
| ModernTCN_turn_l020_tt25_seed101 | all | 0.0337 | 0.0853 | 0.0390 | 0.0545 | 0.0268 | 0.2219 | 7.6134 | 0.7058 | 1.0659 | 91.1055 | 47.7591 |
| ModernTCN_turn_l020_tt25_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002627 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN_turn_l020_tt25_seed101 | uphill_long_entry | 0.0406 | 0.0815 | 0.0443 | 0.0736 | 0.0210 | 0.0974 | 12.1809 | 0.9158 | 1.3340 | 88.4615 | 80.0769 |
| ModernTCN_turn_l020_tt25_seed101 | downhill_transition | 0.0180 | 0.0297 | 0.0316 | 0.0426 | 0.0197 | 0.2219 | 5.8513 | 0.6178 | 0.9251 | 92.6923 | 33.8462 |
| ModernTCN_turn_l020_tt25_seed101 | uphill_return | 0.0459 | 0.0853 | 0.0399 | 0.0532 | 0.0289 | 0.0997 | 3.1934 | 0.7806 | 1.2445 | 89.0000 | 28.7000 |
| ModernTCN_turn_l020_tt25_seed101 | flat_recovery | 0.0228 | 0.0369 | 0.0490 | 0.0313 | 0.0494 | 0.1224 | 12.2720 | 0.5934 | 0.9127 | 93.6000 | 12.0000 |
