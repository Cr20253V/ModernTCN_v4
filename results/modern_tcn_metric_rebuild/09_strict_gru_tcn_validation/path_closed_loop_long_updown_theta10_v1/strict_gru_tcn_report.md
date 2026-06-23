# Strict GRU/TCN validation: path_closed_loop_long_updown_theta10_v1

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_long_updown_theta10_v1\baseline_lock_out.mat`
  - GRU: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\09_strict_gru_tcn_validation\path_closed_loop_long_updown_theta10_v1\GRU_seed101_out.mat`
  - TCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\09_strict_gru_tcn_validation\path_closed_loop_long_updown_theta10_v1\TCN_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_long_updown_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| GRU | 8.0000 | 4.0000 | 6.0000 | 18.0000 | 1.0000 |
| baseline_lock | 11.0000 | 5.0000 | 6.0000 | 22.0000 | 2.0000 |
| TCN | 17.0000 | 9.0000 | 12.0000 | 38.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0353 | 0.0881 | 0.0438 | 0.0566 | 0.0296 | 0.7594 | 322.8705 | 0.2188 | 7.7862 | 0.0000 | 0.7947 | 1.1614 | 90.9906 | 46.6789 |
| GRU | 0.0376 | 0.1078 | 0.0189 | 0.0436 | 0.0150 | 0.2054 | 263.5009 | 0.2554 | 0.6837 | 0.0000 | 0.6822 | 0.9193 | 90.6918 | 59.4576 |
| TCN | 0.2258 | 0.6671 | 0.0736 | 0.1242 | 0.0295 | 1.7072 | 419.4103 | 1.4919 | 423.5212 | 0.0000 | 1.1386 | 2.5685 | 75.6378 | 34.3140 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0210 | 0.0457 | 0.0497 | 0.7124 | 0.0000 |
| GRU | 0.0123 | 0.0193 | 0.0224 | 0.1686 | 0.0000 |
| TCN | 0.0170 | 0.0202 | 0.0226 | 0.2414 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| GRU | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| TCN | 0.0000 | 0.0000 | 0.6205 | 0.0230 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | all | 0.0353 | 0.0881 | 0.0438 | 0.0566 | 0.0296 | 0.2188 | 7.7862 | 0.7947 | 1.1614 | 90.9906 | 46.6789 |
| baseline_lock | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| baseline_lock | uphill_long_entry | 0.0299 | 0.0566 | 0.0520 | 0.0739 | 0.0237 | 0.1107 | 12.1779 | 0.9282 | 1.3464 | 88.4615 | 77.6154 |
| baseline_lock | downhill_transition | 0.0302 | 0.0507 | 0.0337 | 0.0474 | 0.0208 | 0.1171 | 5.5542 | 0.8060 | 1.1330 | 93.5385 | 32.3846 |
| baseline_lock | uphill_return | 0.0518 | 0.0881 | 0.0407 | 0.0571 | 0.0304 | 0.1020 | 3.1918 | 0.9406 | 1.4046 | 87.6000 | 28.1000 |
| baseline_lock | flat_recovery | 0.0285 | 0.0521 | 0.0583 | 0.0288 | 0.0565 | 0.2188 | 14.5651 | 0.5255 | 0.8510 | 93.2000 | 13.8000 |
| GRU | all | 0.0376 | 0.1078 | 0.0189 | 0.0436 | 0.0150 | 0.2554 | 0.6837 | 0.6822 | 0.9193 | 90.6918 | 59.4576 |
| GRU | startup | 0.0000 | 0.0000 | 0.0000 | 0.2201 | 0.0000 | 0.0002637 | 102.0977 | 0.8666 | 0.5652 | 100.0000 | 100.0000 |
| GRU | uphill_long_entry | 0.0100 | 0.0253 | 0.0122 | 0.0316 | 0.0072 | 0.1166 | 0.1493 | 0.4985 | 0.5650 | 93.5385 | 80.2308 |
| GRU | downhill_transition | 0.0532 | 0.1078 | 0.0216 | 0.0565 | 0.0119 | 0.2554 | 1.0518 | 0.8705 | 1.2247 | 91.8462 | 74.7692 |
| GRU | uphill_return | 0.0472 | 0.0783 | 0.0247 | 0.0240 | 0.0219 | 0.1577 | 0.7598 | 0.2712 | 0.7047 | 84.0000 | 25.5000 |
| GRU | flat_recovery | 0.0157 | 0.0273 | 0.0169 | 0.0570 | 0.0221 | 0.1526 | 0.3940 | 1.3089 | 1.5931 | 89.0000 | 13.4000 |
| TCN | all | 0.2258 | 0.6671 | 0.0736 | 0.1242 | 0.0295 | 1.4919 | 423.5212 | 1.1386 | 2.5685 | 75.6378 | 34.3140 |
| TCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.2170 | 0.0000 | 0.0002637 | 101.8309 | 0.3538 | 0.0000 | 100.0000 | 100.0000 |
| TCN | uphill_long_entry | 0.1398 | 0.2983 | 0.0801 | 0.1470 | 0.0223 | 0.4114 | 867.4112 | 1.0001 | 3.4515 | 72.0000 | 71.1538 |
| TCN | downhill_transition | 0.1345 | 0.2831 | 0.0597 | 0.0721 | 0.0362 | 0.4669 | 319.6698 | 1.4013 | 1.5068 | 93.8462 | 5.0769 |
| TCN | uphill_return | 0.1998 | 0.5653 | 0.0477 | 0.1629 | 0.0304 | 0.7466 | 152.6791 | 0.9292 | 3.8098 | 69.7000 | 25.2000 |
| TCN | flat_recovery | 0.5157 | 0.6671 | 0.1291 | 0.1051 | 0.0314 | 1.4919 | 295.2810 | 1.5894 | 1.8397 | 37.4000 | 0.0000 |
