# ModernTCN 与 GRU 闭环仿真对比报告

- ModernTCN 输出文件：`E:\Matlab\Simulink\S-Function_16\results\compare\modern_tcn_gru_closed_loop\factory_showcase_theta10_v10\ModernTCN_factory_showcase_theta10_v10_out.mat`
- GRU 输出文件：`E:\Matlab\Simulink\S-Function_16\results\compare\modern_tcn_gru_closed_loop\factory_showcase_theta10_v10\GRU_factory_showcase_theta10_v10_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v10.mat`

## 指标说明

- 跟踪误差：`ey_rmse/peak`、`epsi_rmse/peak`、`ev_rmse/peak`、`eomega_rmse/peak`、`xy_rmse/peak`，数值越小越好。
- 控制性能：`F_rms/peak`、`omega_cmd_rms/peak`、`j_du`、`F_sat595_pct`、`omega_sat060_pct`、主动约束触碰率和 `viol_rate`，用于检查控制幅值、平滑性和约束安全性。
- 处理用时：输出文件中记录了 `diag_solve_time_ms`，本报告统计 p50/p95/p99/max 和 10 ms 阈值下的超时率 `timeout_rate`。
- AI/调度：`theta_mae_deg`、`theta_sched_mae_deg`、主状态准确率 `main_acc_pct`、转向准确率 `turn_acc_pct`。
- 表格列名保留脚本中的指标变量名，便于和 CSV/MAT 结果一一对应。

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0275 | 0.2742 | 0.1044 | 0.0517 | 0.0280 | 2.4412 | 221.1340 | 1.2141 | 0.9263 | 0.0000 | 0.3789 | 0.4208 | 98.0516 | 95.3002 |
| GRU | 0.0193 | 0.1982 | 0.0799 | 0.0404 | 0.0186 | 1.8724 | 218.4360 | 0.9662 | 1.0090 | 0.0000 | 0.5079 | 0.5075 | 95.3247 | 97.5380 |

## 处理用时统计

处理用时信号来自 `diag_solve_time_ms`。`timeout_rate` 使用 10 ms 作为阈值。

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0216 | 0.0244 | 0.0265 | 1.6941 | 0.0000 |
| GRU | 0.0101 | 0.0118 | 0.0127 | 2.8566 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.6236 | 0.0000 | 0.0000 |
| GRU | 0.0000 | 0.0000 | 0.0611 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0275 | 0.2742 | 0.1044 | 0.0517 | 0.0280 | 1.2141 | 0.9263 | 0.3789 | 0.4208 | 98.0516 | 95.3002 |
| ModernTCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.1084 | 0.0000 | 0.0002519 | 22.4312 | 0.0762 | 0.0537 | 100.0000 | 100.0000 |
| ModernTCN | outbound_rack_aisle | 0.0000 | 0.0000 | 0.0000 | 0.0616 | 0.0000 | 7.585e-05 | 0.1407 | 0.2192 | 0.3509 | 97.9103 | 100.0000 |
| ModernTCN | approach_to_u_turn | 0.0000 | 0.0000 | 0.0000 | 0.0395 | 0.0000 | 4.679e-05 | 3.1943 | 0.1712 | 0.4044 | 99.1000 | 100.0000 |
| ModernTCN | adjacent_aisle_u_turn | 0.0619 | 0.2742 | 0.2410 | 0.0290 | 0.0573 | 1.2141 | 1.8895 | 1.0842 | 0.5991 | 97.8830 | 76.6914 |
| ModernTCN | return_recovery_aisle | 0.0283 | 0.0972 | 0.0323 | 0.0370 | 0.0590 | 0.7891 | 4.4224 | 0.3629 | 0.8970 | 100.0000 | 93.0213 |
| ModernTCN | return_slope_aisle | 0.0005221 | 0.0020 | 0.0004312 | 0.0611 | 0.0007339 | 0.0070 | 0.1412 | 0.2362 | 0.4154 | 97.4459 | 100.0000 |
| ModernTCN | shipping_return_aisle | 0.0005708 | 0.0009087 | 0.0001354 | 0.0264 | 0.0001282 | 0.0013 | 2.1617 | 0.1205 | 0.1502 | 98.5528 | 100.0000 |
| GRU | all | 0.0193 | 0.1982 | 0.0799 | 0.0404 | 0.0186 | 0.9662 | 1.0090 | 0.5079 | 0.5075 | 95.3247 | 97.5380 |
| GRU | startup | 0.0000 | 0.0000 | 0.0000 | 0.1084 | 0.0000 | 0.0002519 | 22.4312 | 0.0537 | 0.0537 | 100.0000 | 100.0000 |
| GRU | outbound_rack_aisle | 0.0000 | 0.0000 | 0.0000 | 0.0465 | 0.0000 | 3.552e-05 | 0.0676 | 0.5194 | 0.5345 | 94.7564 | 100.0000 |
| GRU | approach_to_u_turn | 0.0000 | 0.0000 | 0.0000 | 0.0302 | 0.0000 | 1.775e-05 | 0.3462 | 0.4211 | 0.3015 | 86.6000 | 100.0000 |
| GRU | adjacent_aisle_u_turn | 0.0433 | 0.1982 | 0.1846 | 0.0285 | 0.0379 | 0.9662 | 4.9017 | 0.5984 | 0.5989 | 100.0000 | 88.6949 |
| GRU | return_recovery_aisle | 0.0216 | 0.0748 | 0.0228 | 0.0311 | 0.0396 | 0.6689 | 0.1039 | 0.7778 | 0.7607 | 100.0000 | 92.9392 |
| GRU | return_slope_aisle | 0.0004687 | 0.0010 | 0.0002592 | 0.0470 | 0.0003767 | 0.0035 | 0.0840 | 0.5412 | 0.5570 | 93.3784 | 100.0000 |
| GRU | shipping_return_aisle | 0.0004862 | 0.0008343 | 0.0001492 | 0.0227 | 0.0001368 | 0.0013 | 0.2246 | 0.1660 | 0.0884 | 91.7511 | 100.0000 |
