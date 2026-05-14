# ModernTCN vs GRU Closed-Loop Comparison

- ModernTCN file: `results/compare/modern_tcn_gru_closed_loop/ModernTCN_v2_out.mat`
- GRU file: `results/compare/modern_tcn_gru_closed_loop/GRU_v2_out.mat`
- Path file: `data/paths/path_modern_tcn_demo_loop_v2.mat`

## Metric Set

- Tracking: `ey_rmse/peak`, `epsi_rmse/peak`, `ev_rmse/peak`, `eomega_rmse/peak`, `xy_rmse/peak`.
- Control: `F_rms/peak`, `omega_cmd_rms/peak`, legacy `F_sat595_pct`, legacy `omega_sat060_pct`, active-limit hit rate, `viol_rate`, `j_du`.
- Runtime: solver p50/p95/p99/max and timeout rate with a 10 ms threshold.
- AI/scheduling: `theta_mae_deg`, `theta_sched_mae_deg`, main/turn accuracy when the labels are logged.

## Summary

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0170 | 0.0549 | 0.0496 | 0.0407 | 0.0109 | 0.9184 | 222.7020 | 0.9907 | 1.2709 | 0.0000 | 0.6394 | 0.6472 | 96.1729 | 80.8701 |
| GRU | 0.0203 | 0.0549 | 0.0575 | 0.0716 | 0.0147 | 1.1595 | 234.2016 | 0.5008 | 0.5537 | 0.0000 | 0.9768 | 0.9716 | 83.1987 | 82.3798 |

## Runtime And Limits

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | solve_time_p95_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0111 | 0.0000 | 0.0222 | 1.5597 | 0.0000 |
| GRU | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0120 | 0.9955 | 0.0000 |

## Per-Zone Key Metrics

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0170 | 0.0549 | 0.0496 | 0.0407 | 0.0109 | 0.9907 | 1.2709 | 0.6394 | 0.6472 | 96.1729 | 80.8701 |
| ModernTCN | startup | 0.0032 | 0.0062 | 0.0013 | 0.1126 | 0.0002714 | 0.0078 | 24.2060 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN | flat_right_turn | 0.0346 | 0.0549 | 0.0187 | 0.0019 | 0.0200 | 0.9907 | 0.0177 | 0.0000 | 0.0000 | 100.0000 | 58.6111 |
| ModernTCN | low_speed_flat_turn | 0.0147 | 0.0225 | 0.0216 | 0.0051 | 0.0038 | 0.1830 | 0.0195 | 0.0000 | 0.0000 | 100.0000 | 28.8571 |
| ModernTCN | pure_slope | 0.0037 | 0.0125 | 0.0066 | 0.0502 | 0.0012 | 0.0329 | 4.4600 | 1.8214 | 1.8578 | 91.7826 | 95.9348 |
| ModernTCN | slope_left_turn_composite | 0.0112 | 0.0228 | 0.1071 | 0.0718 | 0.0137 | 0.1562 | 0.5391 | 0.6573 | 0.6832 | 99.3125 | 82.0312 |
| ModernTCN | bumpy_theta_closure | 0.0045 | 0.0083 | 0.0363 | 0.0273 | 0.0038 | 0.0579 | 0.0429 | 0.5289 | 0.4895 | 89.3333 | 100.0000 |
| ModernTCN | closure | 0.0011 | 0.0026 | 0.0058 | 0.0036 | 0.0011 | 0.0098 | 0.0083 | 0.0000 | 1.409e-27 | 100.0000 | 100.0000 |
| GRU | all | 0.0203 | 0.0549 | 0.0575 | 0.0716 | 0.0147 | 0.5008 | 0.5537 | 0.9768 | 0.9716 | 83.1987 | 82.3798 |
| GRU | startup | 0.0032 | 0.0062 | 0.0013 | 0.1126 | 0.0002714 | 0.0078 | 24.2060 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| GRU | flat_right_turn | 0.0349 | 0.0549 | 0.0171 | 0.0034 | 0.0202 | 0.4705 | 0.3457 | 0.0149 | 0.0151 | 100.0000 | 51.8333 |
| GRU | low_speed_flat_turn | 0.0152 | 0.0235 | 0.0187 | 0.0051 | 0.0052 | 0.3247 | 0.0195 | 0.0000 | 9.798e-10 | 100.0000 | 85.8571 |
| GRU | pure_slope | 0.0044 | 0.0127 | 0.0156 | 0.0652 | 0.0020 | 0.0322 | 1.1547 | 1.3179 | 1.3130 | 64.6739 | 100.0000 |
| GRU | slope_left_turn_composite | 0.0274 | 0.0462 | 0.1262 | 0.1487 | 0.0265 | 0.5008 | 0.8973 | 3.2931 | 3.2704 | 56.5312 | 71.6875 |
| GRU | bumpy_theta_closure | 0.0039 | 0.0082 | 0.0274 | 0.0273 | 0.0034 | 0.0394 | 0.0430 | 0.4895 | 0.4895 | 100.0000 | 100.0000 |
| GRU | closure | 0.0010 | 0.0014 | 0.0047 | 0.0036 | 0.0009132 | 0.0057 | 0.0084 | 0.0000 | 1.046e-37 | 100.0000 | 100.0000 |
