# Causal ModernTCN、ModernTCN、GRU 与 TCN 闭环仿真对比报告

- base three-algorithm summary: `E:\Matlab\Simulink\S-Function_16\results\compare\tcn_gru_modern_closed_loop\path_factory_logistics_showcase_theta10_v3\tcn_gru_modern_closed_loop_summary.csv`
- causal summary source: `E:\Matlab\Simulink\S-Function_16\results\compare\causal_modern_tcn_closed_loop\path_factory_logistics_showcase_theta10_v3\tcn_gru_modern_closed_loop_summary.csv`
- path: `data/paths/path_factory_logistics_showcase_theta10_v3.mat`

## Rank

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---:|---:|---:|---:|---:|
| ModernTCN | 6 | 6 | 4 | 16 | 1 |
| TCN | 13 | 6 | 14 | 33 | 2 |
| GRU | 17 | 7 | 11 | 35 | 3 |
| ModernTCN_causal | 24 | 11 | 11 | 46 | 4 |

## Summary

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.02459 | 0.09399 | 0.04375 | 0.05348 | 0.03069 | 0.8036 | 285.7 | 0.886 | 0.5991 | 0 | 0.8974 | 0.9239 | 94.14 | 81.39 |
| ModernTCN_causal | 23.13 | 45.14 | 1.273 | 0.6595 | 0.06861 | 27.48 | 717.7 | 1.436 | 268.9 | 0 | 1.595 | 1.687 | 77.1 | 62.22 |
| GRU | 0.06233 | 0.3696 | 0.1714 | 0.07531 | 0.06527 | 1.664 | 325 | 1.554 | 7.03 | 0 | 0.3664 | 0.3415 | 92.22 | 80.07 |
| TCN | 0.0364 | 0.1862 | 0.1061 | 0.1154 | 0.0474 | 1.354 | 720 | 1.436 | 235.7 | 5.277e-05 | 0.259 | 1.708 | 74.71 | 86.09 |
