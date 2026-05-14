# Mamba2-GRU-IMU Comparison Statistical Report

- Generated: 2026-04-17 21:44:41
- Input: E:\Matlab\Simulink\S-Function_16\results\compare\mamba2_gru_imu\compare_20260417_210620\raw\case_rows.mat
- Valid cases: 18

## Controller Summary

| controller | n_cases | ey_rmse_mean | ey_rmse_std | ey_rmse_median | ey_rmse_p25 | ey_rmse_p75 | epsi_rmse_mean | epsi_rmse_std | epsi_rmse_median | epsi_rmse_p25 | epsi_rmse_p75 | ev_rmse_mean | ev_rmse_std | ev_rmse_median | ev_rmse_p25 | ev_rmse_p75 | eomega_rmse_mean | eomega_rmse_std | eomega_rmse_median | eomega_rmse_p25 | eomega_rmse_p75 | j_du_mean | j_du_std | j_du_median | j_du_p25 | j_du_p75 | viol_rate_mean | viol_rate_std | viol_rate_median | viol_rate_p25 | viol_rate_p75 | timeout_rate_mean | timeout_rate_std | timeout_rate_median | timeout_rate_p25 | timeout_rate_p75 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Mamba2 | 0 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| GRU | 9 | 0.0194202 | 0.0195285 | 0.0141095 | 0 | 0.044151 | 0.0306726 | 0.0235066 | 0.0404287 | 0 | 0.0515891 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 7683.42 | 5196.61 | 7401.32 | 1828.91 | 13820 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| IMU | 9 | 0.0257008 | 0.0234218 | 0.0182874 | 0 | 0.0526032 | 0.0422941 | 0.0495181 | 0.0413789 | 0 | 0.0454513 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 196947 | 585324 | 911.227 | 648.237 | 5015.36 | 0.000746981 | 0.00205426 | 0 | 0 | 0.000167364 | 0 | 0 | 0 | 0 | 0 |

## Friedman Test

| metric | n_paired_cases | friedman_p |
|---|---|---|
| ey_rmse | 0 | NaN |
| epsi_rmse | 0 | NaN |
| ev_rmse | 0 | NaN |
| eomega_rmse | 0 | NaN |
| j_du | 0 | NaN |
| viol_rate | 0 | NaN |
| timeout_rate | 0 | NaN |

## Pairwise Wilcoxon + Holm

| metric | ctrl_a | ctrl_b | n | p_raw | p_holm | cohen_d_paired | cliff_delta | median_diff_a_minus_b |
|---|---|---|---|---|---|---|---|---|
| ey_rmse | Mamba2 | GRU | 0 | NaN | NaN | NaN | NaN | NaN |
| ey_rmse | Mamba2 | IMU | 0 | NaN | NaN | NaN | NaN | NaN |
| ey_rmse | GRU | IMU | 0 | NaN | NaN | NaN | NaN | NaN |
| epsi_rmse | Mamba2 | GRU | 0 | NaN | NaN | NaN | NaN | NaN |
| epsi_rmse | Mamba2 | IMU | 0 | NaN | NaN | NaN | NaN | NaN |
| epsi_rmse | GRU | IMU | 0 | NaN | NaN | NaN | NaN | NaN |
| ev_rmse | Mamba2 | GRU | 0 | NaN | NaN | NaN | NaN | NaN |
| ev_rmse | Mamba2 | IMU | 0 | NaN | NaN | NaN | NaN | NaN |
| ev_rmse | GRU | IMU | 0 | NaN | NaN | NaN | NaN | NaN |
| eomega_rmse | Mamba2 | GRU | 0 | NaN | NaN | NaN | NaN | NaN |
| eomega_rmse | Mamba2 | IMU | 0 | NaN | NaN | NaN | NaN | NaN |
| eomega_rmse | GRU | IMU | 0 | NaN | NaN | NaN | NaN | NaN |
| j_du | Mamba2 | GRU | 0 | NaN | NaN | NaN | NaN | NaN |
| j_du | Mamba2 | IMU | 0 | NaN | NaN | NaN | NaN | NaN |
| j_du | GRU | IMU | 0 | NaN | NaN | NaN | NaN | NaN |
| viol_rate | Mamba2 | GRU | 0 | NaN | NaN | NaN | NaN | NaN |
| viol_rate | Mamba2 | IMU | 0 | NaN | NaN | NaN | NaN | NaN |
| viol_rate | GRU | IMU | 0 | NaN | NaN | NaN | NaN | NaN |
| timeout_rate | Mamba2 | GRU | 0 | NaN | NaN | NaN | NaN | NaN |
| timeout_rate | Mamba2 | IMU | 0 | NaN | NaN | NaN | NaN | NaN |
| timeout_rate | GRU | IMU | 0 | NaN | NaN | NaN | NaN | NaN |
