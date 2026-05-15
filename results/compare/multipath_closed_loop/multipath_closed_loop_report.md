# Multi-Path Closed-Loop Benchmark

- timestamp: `2026-05-15 16:10:46`
- output root: `E:\Matlab\Simulink\S-Function_16\results\compare\multipath_closed_loop`
- paths: `3`

## Path Runs

| path | role | status | report |
|---|---|---|---|
| path_factory_logistics_showcase_theta10_v3 | industrial_factory_logistics_transport | reused | `E:\Matlab\Simulink\S-Function_16\results\compare\lpvmpc_theta_baseline\path_factory_logistics_showcase_theta10_v3\tcn_gru_modern_lpvmpc_theta_baseline_report.md` |
| path_closed_loop_long_updown_theta10_v1 | long_updown | reused | `E:\Matlab\Simulink\S-Function_16\results\compare\multipath_closed_loop\path_closed_loop_long_updown_theta10_v1\tcn_gru_modern_lpvmpc_theta_baseline_report.md` |
| path_closed_loop_sharp_turn_transition_theta10_v1 | sharp_turn_transition | reused | `E:\Matlab\Simulink\S-Function_16\results\compare\multipath_closed_loop\path_closed_loop_sharp_turn_transition_theta10_v1\tcn_gru_modern_lpvmpc_theta_baseline_report.md` |

## Aggregate Summary

| controller | paths | rank mean | ey rmse mean | xy rmse mean | j_du mean | viol mean | main acc | turn acc |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ModernTCN | 3 | 1.000 | 0.031894 | 0.48889 | 13.313 | 0 | 94.424 | 79.288 |
| LPV-MPC_oracle_theta | 3 | 2.000 | 0.034735 | 0.39514 | 0.43855 | 0 | 29.057 | 63.294 |
| GRU | 3 | 3.333 | 0.04828 | 0.93575 | 3.3528 | 0 | 90.108 | 72.776 |
| TCN | 3 | 3.667 | 0.048932 | 1.0695 | 313.92 | 1.7589e-05 | 73.937 | 80.177 |
| LPV-MPC_IMU_theta | 3 | 5.000 | 8.893 | 12.178 | 579.76 | 0.035781 | 29.057 | 63.294 |
| LPV-MPC_theta0 | 3 | 6.000 | 8.8276 | 12.253 | 644.06 | 0.035652 | 29.057 | 63.294 |

## ModernTCN Check

- ModernTCN better than both GRU and TCN by per-path overall rank: `3/3` paths.
- Oracle theta is allowed to rank above ModernTCN because it uses true slope.
