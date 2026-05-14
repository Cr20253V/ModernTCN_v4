# ModernTCN 与 GRU 闭环仿真对比报告

- ModernTCN 输出文件：`E:\Matlab\Simulink\S-Function_16\results\compare\modern_tcn_gru_closed_loop\ModernTCN_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21_out.mat`
- GRU 输出文件：`E:\Matlab\Simulink\S-Function_16\results\compare\modern_tcn_gru_closed_loop\GRU_v2_shared_dataset_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_modern_tcn_demo_loop_v2.mat`

## 指标说明

- 跟踪误差：`ey_rmse/peak`、`epsi_rmse/peak`、`ev_rmse/peak`、`eomega_rmse/peak`、`xy_rmse/peak`，数值越小越好。
- 控制性能：`F_rms/peak`、`omega_cmd_rms/peak`、`j_du`、`F_sat595_pct`、`omega_sat060_pct`、主动约束触碰率和 `viol_rate`，用于检查控制幅值、平滑性和约束安全性。
- 处理用时：输出文件中记录了 `diag_solve_time_ms`，本报告统计 p50/p95/p99/max 和 10 ms 阈值下的超时率 `timeout_rate`。
- AI/调度：`theta_mae_deg`、`theta_sched_mae_deg`、主状态准确率 `main_acc_pct`、转向准确率 `turn_acc_pct`。
- 表格列名保留脚本中的指标变量名，便于和 CSV/MAT 结果一一对应。

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0170 | 0.0549 | 0.0417 | 0.0403 | 0.0106 | 0.7901 | 225.3290 | 0.9907 | 1.1890 | 0.0000 | 0.6167 | 0.6262 | 96.7133 | 80.8200 |
| GRU | 0.0231 | 0.0769 | 0.2063 | 0.0680 | 0.0201 | 3.3648 | 240.6715 | 0.5426 | 2.2471 | 0.0000 | 0.4082 | 0.4691 | 95.0643 | 76.9929 |

## 处理用时统计

处理用时信号来自 `diag_solve_time_ms`。`timeout_rate` 使用 10 ms 作为阈值。

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0207 | 0.0228 | 0.0246 | 3.1071 | 0.0000 |
| GRU | 0.0099 | 0.0117 | 0.0125 | 0.6697 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0111 | 0.0000 | 0.0000 |
| GRU | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0170 | 0.0549 | 0.0417 | 0.0403 | 0.0106 | 0.9907 | 1.1890 | 0.6167 | 0.6262 | 96.7133 | 80.8200 |
| ModernTCN | startup | 0.0032 | 0.0062 | 0.0013 | 0.1126 | 0.0002714 | 0.0078 | 24.2060 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN | flat_right_turn | 0.0346 | 0.0549 | 0.0187 | 0.0019 | 0.0200 | 0.9907 | 0.0177 | 0.0000 | 0.0000 | 100.0000 | 58.6111 |
| ModernTCN | low_speed_flat_turn | 0.0147 | 0.0225 | 0.0216 | 0.0051 | 0.0038 | 0.1830 | 0.0195 | 0.0000 | 0.0000 | 100.0000 | 28.8571 |
| ModernTCN | pure_slope | 0.0037 | 0.0125 | 0.0064 | 0.0485 | 0.0013 | 0.0329 | 4.0029 | 1.7333 | 1.7647 | 91.5652 | 96.6087 |
| ModernTCN | slope_left_turn_composite | 0.0110 | 0.0186 | 0.0889 | 0.0721 | 0.0127 | 0.1422 | 0.7360 | 0.6695 | 0.6983 | 99.0000 | 80.7812 |
| ModernTCN | bumpy_theta_closure | 0.0039 | 0.0067 | 0.0306 | 0.0273 | 0.0032 | 0.0557 | 0.0429 | 0.5302 | 0.4895 | 90.5556 | 100.0000 |
| ModernTCN | closure | 0.0009236 | 0.0023 | 0.0048 | 0.0036 | 0.0009196 | 0.0093 | 0.0083 | 0.0000 | 1.312e-27 | 100.0000 | 100.0000 |
| GRU | all | 0.0231 | 0.0769 | 0.2063 | 0.0680 | 0.0201 | 0.5426 | 2.2471 | 0.4082 | 0.4691 | 95.0643 | 76.9929 |
| GRU | startup | 0.0032 | 0.0062 | 0.0013 | 0.1126 | 0.0002714 | 0.0078 | 24.2060 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| GRU | flat_right_turn | 0.0341 | 0.0548 | 0.0185 | 0.0019 | 0.0167 | 0.5240 | 0.0087 | 0.0000 | 0.0000 | 100.0000 | 80.7778 |
| GRU | low_speed_flat_turn | 0.0137 | 0.0210 | 0.0215 | 0.0051 | 0.0048 | 0.1866 | 0.0208 | 0.0000 | 0.0000 | 100.0000 | 57.7857 |
| GRU | pure_slope | 0.0037 | 0.0118 | 0.0086 | 0.0922 | 0.0021 | 0.0329 | 0.4984 | 0.9723 | 1.1225 | 84.6957 | 100.0000 |
| GRU | slope_left_turn_composite | 0.0303 | 0.0615 | 0.4497 | 0.1012 | 0.0326 | 0.2449 | 3.5671 | 0.4117 | 0.5050 | 98.9375 | 18.4688 |
| GRU | bumpy_theta_closure | 0.0199 | 0.0471 | 0.1618 | 0.0700 | 0.0210 | 0.1201 | 0.4983 | 0.8513 | 0.8754 | 91.7778 | 100.0000 |
| GRU | closure | 0.0051 | 0.0092 | 0.0276 | 0.0036 | 0.0055 | 0.0234 | 0.0083 | 0.0000 | 3.355e-06 | 100.0000 | 100.0000 |
