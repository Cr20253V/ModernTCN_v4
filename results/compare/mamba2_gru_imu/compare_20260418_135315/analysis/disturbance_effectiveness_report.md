# Disturbance Effectiveness Check Report

- Generated: 2026-04-18 13:54:25
- Input: E:\Matlab\Simulink\S-Function_16\results\compare\mamba2_gru_imu\compare_20260418_135315\raw\case_rows.mat
- Group fields: controller, path_name, seed
- Metrics: ey_rmse, epsi_rmse, ev_rmse, eomega_rmse, j_du, viol_rate
- Thresholds: abs_tol=1.000e-12, rel_tol=1.000e-07
- Checked rows: 3
- Flagged invariant rows: 3

## Summary by Controller and Metric

| controller | metric | n_groups_checked | n_invariant | invariant_ratio |
|---|---|---|---|---|
| GRU | ey_rmse | 0.000000e+00 | 0.000000e+00 | NaN |
| GRU | epsi_rmse | 0.000000e+00 | 0.000000e+00 | NaN |
| GRU | ev_rmse | 1 | 1 | 1 |
| GRU | eomega_rmse | 0.000000e+00 | 0.000000e+00 | NaN |
| GRU | j_du | 1 | 1 | 1 |
| GRU | viol_rate | 1 | 1 | 1 |

## Flagged Rows (Top 30)

| controller | path_name | seed | metric | value_min | value_max | value_range | rel_range |
|---|---|---|---|---|---|---|---|
| GRU | tmp_path_straight_0p5s | 1 | ev_rmse | 0.605991 | 0.605991 | 0.000000e+00 | 0.000000e+00 |
| GRU | tmp_path_straight_0p5s | 1 | j_du | 7.140374e+06 | 7.140374e+06 | 0.000000e+00 | 0.000000e+00 |
| GRU | tmp_path_straight_0p5s | 1 | viol_rate | 0.0588235 | 0.0588235 | 0.000000e+00 | 0.000000e+00 |
