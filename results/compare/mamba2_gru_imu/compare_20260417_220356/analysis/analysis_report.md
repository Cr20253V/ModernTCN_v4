# Mamba2-GRU-IMU Comparison Statistical Report

- Generated: 2026-04-18 01:14:27
- Input: E:\Matlab\Simulink\S-Function_16\results\compare\mamba2_gru_imu\compare_20260417_220356\raw\case_rows.mat
- Valid cases: 27

## Controller Summary

| controller | n_cases | ey_rmse_mean | ey_rmse_std | ey_rmse_median | ey_rmse_p25 | ey_rmse_p75 | epsi_rmse_mean | epsi_rmse_std | epsi_rmse_median | epsi_rmse_p25 | epsi_rmse_p75 | ev_rmse_mean | ev_rmse_std | ev_rmse_median | ev_rmse_p25 | ev_rmse_p75 | eomega_rmse_mean | eomega_rmse_std | eomega_rmse_median | eomega_rmse_p25 | eomega_rmse_p75 | j_du_mean | j_du_std | j_du_median | j_du_p25 | j_du_p75 | viol_rate_mean | viol_rate_std | viol_rate_median | viol_rate_p25 | viol_rate_p75 | timeout_rate_mean | timeout_rate_std | timeout_rate_median | timeout_rate_p25 | timeout_rate_p75 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Mamba2 | 9 | 0.0194523 | 0.0199404 | 0.013483 | 0 | 0.0448484 | 0.0277906 | 0.0209368 | 0.0394056 | 0 | 0.0438061 | 0.0498393 | 0.038773 | 0.0492033 | 0.00541754 | 0.0949251 | 0.0213363 | 0.0194211 | 0.0193512 | 0 | 0.0446104 | 6453.91 | 5195.25 | 6261.13 | 559.457 | 12503.8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| GRU | 9 | 0.0194202 | 0.0195285 | 0.0141095 | 0 | 0.044151 | 0.0306726 | 0.0235066 | 0.0404287 | 0 | 0.0515891 | 0.0302842 | 0.0201717 | 0.0326742 | 0.00588896 | 0.0522893 | 0.0218709 | 0.0183095 | 0.0234132 | 0 | 0.0421994 | 7683.42 | 5196.61 | 7401.32 | 1828.91 | 13820 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| IMU | 9 | 0.0257008 | 0.0234218 | 0.0182874 | 0 | 0.0526032 | 0.0422941 | 0.0495181 | 0.0413789 | 0 | 0.0454513 | 0.09547 | 0.080281 | 0.0884598 | 0.00535994 | 0.182366 | 0.0239426 | 0.0213696 | 0.017432 | 0 | 0.0431359 | 196947 | 585324 | 911.227 | 648.237 | 5015.36 | 0.000746981 | 0.00205426 | 0 | 0 | 0.000167364 | 0 | 0 | 0 | 0 | 0 |

## Friedman Test

| metric | n_paired_cases | friedman_p |
|---|---|---|
| ey_rmse | 9 | 0.011109 |
| epsi_rmse | 9 | 0.114559 |
| ev_rmse | 9 | 0.367879 |
| eomega_rmse | 9 | 0.606531 |
| j_du | 9 | 0.00482795 |
| viol_rate | 9 | 0.0183156 |
| timeout_rate | 9 | 1 |

## Pairwise Wilcoxon + Holm

| metric | ctrl_a | ctrl_b | n | p_raw | p_holm | cohen_d_paired | cliff_delta | median_diff_a_minus_b |
|---|---|---|---|---|---|---|---|---|
| ey_rmse | Mamba2 | GRU | 9 | 0.4375 | 0.4375 | 0.0548677 | 0 | 0 |
| ey_rmse | Mamba2 | IMU | 9 | 0.03125 | 0.09375 | -0.8587 | -0.666667 | -0.00480434 |
| ey_rmse | GRU | IMU | 9 | 0.03125 | 0.09375 | -0.872383 | -0.666667 | -0.00417794 |
| epsi_rmse | Mamba2 | GRU | 9 | 0.4375 | 0.875 | -0.403364 | 0 | 0 |
| epsi_rmse | Mamba2 | IMU | 9 | 0.03125 | 0.09375 | -0.358926 | -0.666667 | -0.00153333 |
| epsi_rmse | GRU | IMU | 9 | 0.84375 | 0.875 | -0.311199 | -0.222222 | 0 |
| ev_rmse | Mamba2 | GRU | 9 | 0.0546875 | 0.128906 | 1.0393 | 0.333333 | 0.0165291 |
| ev_rmse | Mamba2 | IMU | 9 | 0.0546875 | 0.128906 | -1.09588 | -0.333333 | -0.0392565 |
| ev_rmse | GRU | IMU | 9 | 0.0429688 | 0.128906 | -1.07957 | -0.333333 | -0.0557856 |
| eomega_rmse | Mamba2 | GRU | 9 | 0.4375 | 1 | -0.184351 | 0 | 0 |
| eomega_rmse | Mamba2 | IMU | 9 | 0.4375 | 1 | -0.234763 | 0.444444 | 0.00147442 |
| eomega_rmse | GRU | IMU | 9 | 0.84375 | 1 | -0.20611 | -0.222222 | 0 |
| j_du | Mamba2 | GRU | 9 | 0.00390625 | 0.0117188 | -16.216 | -1 | -1269.45 |
| j_du | Mamba2 | IMU | 9 | 0.425781 | 0.425781 | -0.326738 | 0.111111 | 5338.55 |
| j_du | GRU | IMU | 9 | 0.101562 | 0.203125 | -0.324622 | 0.777778 | 6478.74 |
| viol_rate | Mamba2 | GRU | 9 | 1 | 1 | NaN | 0 | 0 |
| viol_rate | Mamba2 | IMU | 9 | 0.125 | 0.375 | -0.363626 | -0.444444 | 0 |
| viol_rate | GRU | IMU | 9 | 0.125 | 0.375 | -0.363626 | -0.444444 | 0 |
| timeout_rate | Mamba2 | GRU | 9 | 1 | 1 | NaN | 0 | 0 |
| timeout_rate | Mamba2 | IMU | 9 | 1 | 1 | NaN | 0 | 0 |
| timeout_rate | GRU | IMU | 9 | 1 | 1 | NaN | 0 | 0 |
