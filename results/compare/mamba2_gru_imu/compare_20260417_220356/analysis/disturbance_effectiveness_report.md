# Disturbance Effectiveness Check Report

- Generated: 2026-04-18 01:25:52
- Input: e:/Matlab/Simulink/S-Function_16/results/compare/mamba2_gru_imu/compare_20260417_220356/raw/case_rows.mat
- Group fields: controller, path_name, seed
- Metrics: ey_rmse, epsi_rmse, ev_rmse, eomega_rmse, j_du, viol_rate
- Thresholds: abs_tol=1.000e-12, rel_tol=1.000e-07
- Checked rows: 38
- Flagged invariant rows: 18

## Summary by Controller and Metric

| controller | metric | n_groups_checked | n_invariant | invariant_ratio |
|---|---|---|---|---|
| Mamba2 | ey_rmse | 2 | 0.000000e+00 | 0.000000e+00 |
| Mamba2 | epsi_rmse | 2 | 0.000000e+00 | 0.000000e+00 |
| Mamba2 | ev_rmse | 3 | 0.000000e+00 | 0.000000e+00 |
| Mamba2 | eomega_rmse | 2 | 0.000000e+00 | 0.000000e+00 |
| Mamba2 | j_du | 3 | 0.000000e+00 | 0.000000e+00 |
| Mamba2 | viol_rate | 0.000000e+00 | 0.000000e+00 | NaN |
| GRU | ey_rmse | 2 | 2 | 1 |
| GRU | epsi_rmse | 2 | 2 | 1 |
| GRU | ev_rmse | 3 | 3 | 1 |
| GRU | eomega_rmse | 2 | 2 | 1 |
| GRU | j_du | 3 | 3 | 1 |
| GRU | viol_rate | 0.000000e+00 | 0.000000e+00 | NaN |
| IMU | ey_rmse | 2 | 1 | 0.5 |
| IMU | epsi_rmse | 2 | 1 | 0.5 |
| IMU | ev_rmse | 3 | 1 | 0.333333 |
| IMU | eomega_rmse | 2 | 1 | 0.5 |
| IMU | j_du | 3 | 1 | 0.333333 |
| IMU | viol_rate | 2 | 1 | 0.5 |

## Flagged Rows (Top 30)

| controller | path_name | seed | metric | value_min | value_max | value_range | rel_range |
|---|---|---|---|---|---|---|---|
| GRU | path_industrial | 1 | ey_rmse | 0.0141095 | 0.0141095 | 0.000000e+00 | 0.000000e+00 |
| GRU | path_industrial | 1 | epsi_rmse | 0.0515891 | 0.0515891 | 0.000000e+00 | 0.000000e+00 |
| GRU | path_industrial | 1 | ev_rmse | 0.0326742 | 0.0326742 | 0.000000e+00 | 0.000000e+00 |
| GRU | path_industrial | 1 | eomega_rmse | 0.0234132 | 0.0234132 | 0.000000e+00 | 0.000000e+00 |
| GRU | path_industrial | 1 | j_du | 1.382003e+04 | 1.382003e+04 | 0.000000e+00 | 0.000000e+00 |
| GRU | path_s_curve | 1 | ey_rmse | 0.044151 | 0.044151 | 0.000000e+00 | 0.000000e+00 |
| GRU | path_s_curve | 1 | epsi_rmse | 0.0404287 | 0.0404287 | 0.000000e+00 | 0.000000e+00 |
| GRU | path_s_curve | 1 | ev_rmse | 0.00588896 | 0.00588896 | 0.000000e+00 | 0.000000e+00 |
| GRU | path_s_curve | 1 | eomega_rmse | 0.0421994 | 0.0421994 | 0.000000e+00 | 0.000000e+00 |
| GRU | path_s_curve | 1 | j_du | 1828.91 | 1828.91 | 0.000000e+00 | 0.000000e+00 |
| GRU | path_slope | 1 | ev_rmse | 0.0522893 | 0.0522893 | 0.000000e+00 | 0.000000e+00 |
| GRU | path_slope | 1 | j_du | 7401.32 | 7401.32 | 0.000000e+00 | 0.000000e+00 |
| IMU | path_s_curve | 1 | ey_rmse | 0.0526032 | 0.0526032 | 0.000000e+00 | 0.000000e+00 |
| IMU | path_s_curve | 1 | epsi_rmse | 0.0454513 | 0.0454513 | 0.000000e+00 | 0.000000e+00 |
| IMU | path_s_curve | 1 | ev_rmse | 0.00535994 | 0.00535994 | 0.000000e+00 | 0.000000e+00 |
| IMU | path_s_curve | 1 | eomega_rmse | 0.0431359 | 0.0431359 | 0.000000e+00 | 0.000000e+00 |
| IMU | path_s_curve | 1 | j_du | 648.237 | 648.237 | 0.000000e+00 | 0.000000e+00 |
| IMU | path_s_curve | 1 | viol_rate | 1.673640e-04 | 1.673640e-04 | 0.000000e+00 | 0.000000e+00 |
