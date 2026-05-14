# ModernTCN Theta Sweep Plot Report

- Path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_modern_tcn_theta_sweep_plot_v1.mat`
- Data file: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\ModernTCN_theta_sweep_plot_data.mat`
- Model seed: `21`
- ONNX file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_seed21.onnx`
- Sweep: -10.0 to 10.0 deg, step 0.1 deg, segment 5.00 s, v=0.90 m/s
- Note: held-out paper plotting set; not added to training data.

## Segment median, all theta

| metric | value |
|---|---:|
| n | 201 |
| MAE (deg) | 0.574485 |
| RMSE (deg) | 0.741242 |
| P95 abs error (deg) | 1.798259 |
| Peak abs error (deg) | 2.414685 |
| Bias (deg) | -0.086024 |
| Fit slope | 0.897005 |
| Fit intercept (deg) | -0.086024 |
| Pearson r | 0.996604 |
| R2 identity | 0.983680 |

## Segment median, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 162 |
| MAE (deg) | 0.598878 |
| RMSE (deg) | 0.775121 |
| P95 abs error (deg) | 1.973437 |
| Peak abs error (deg) | 2.414685 |
| Bias (deg) | -0.147808 |
| Fit slope | 0.898995 |
| Fit intercept (deg) | -0.147808 |
| Pearson r | 0.997682 |
| R2 identity | 0.985511 |

## Segment median, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 161 |
| MAE (deg) | 0.457484 |
| RMSE (deg) | 0.515693 |
| P95 abs error (deg) | 0.952643 |
| Peak abs error (deg) | 1.218508 |
| Bias (deg) | 0.071432 |
| Fit slope | 0.909635 |
| Fit intercept (deg) | 0.071432 |
| Pearson r | 0.997646 |
| R2 identity | 0.987688 |

## Segment median, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 201 |
| MAE (deg) | 0.574485 |
| RMSE (deg) | 0.741242 |
| P95 abs error (deg) | 1.798259 |
| Peak abs error (deg) | 2.414685 |
| Bias (deg) | -0.086024 |
| Fit slope | 0.897005 |
| Fit intercept (deg) | -0.086024 |
| Pearson r | 0.996604 |
| R2 identity | 0.983680 |

## Window-level, all theta

| metric | value |
|---|---:|
| n | 2211 |
| MAE (deg) | 0.574321 |
| RMSE (deg) | 0.741104 |
| P95 abs error (deg) | 1.761371 |
| Peak abs error (deg) | 2.416962 |
| Bias (deg) | -0.085959 |
| Fit slope | 0.897036 |
| Fit intercept (deg) | -0.085959 |
| Pearson r | 0.996604 |
| R2 identity | 0.983686 |

## Window-level, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 1782 |
| MAE (deg) | 0.598710 |
| RMSE (deg) | 0.774986 |
| P95 abs error (deg) | 1.942346 |
| Peak abs error (deg) | 2.416962 |
| Bias (deg) | -0.147715 |
| Fit slope | 0.899025 |
| Fit intercept (deg) | -0.147715 |
| Pearson r | 0.997681 |
| R2 identity | 0.985516 |

## Window-level, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 1771 |
| MAE (deg) | 0.457367 |
| RMSE (deg) | 0.515585 |
| P95 abs error (deg) | 0.934767 |
| Peak abs error (deg) | 1.219111 |
| Bias (deg) | 0.071546 |
| Fit slope | 0.909656 |
| Fit intercept (deg) | 0.071546 |
| Pearson r | 0.997647 |
| R2 identity | 0.987693 |

## Window-level, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 2211 |
| MAE (deg) | 0.574321 |
| RMSE (deg) | 0.741104 |
| P95 abs error (deg) | 1.761371 |
| Peak abs error (deg) | 2.416962 |
| Bias (deg) | -0.085959 |
| Fit slope | 0.897036 |
| Fit intercept (deg) | -0.085959 |
| Pearson r | 0.996604 |
| R2 identity | 0.983686 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21_pm8\modern_tcn_theta_sweep_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21_pm8\modern_tcn_theta_sweep_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21_pm8\modern_tcn_theta_sweep_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21_pm8\modern_tcn_theta_sweep_residual.pdf`
- Segment CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21_pm8\modern_tcn_theta_sweep_segment_summary.csv`
- Window CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21_pm8\modern_tcn_theta_sweep_window_predictions.csv`
- Result MAT: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21_pm8\modern_tcn_theta_sweep_eval_result.mat`

## Path Meta

- Path type: `path_modern_tcn_theta_sweep_plot_v1`
- Samples: `100501`
- Stop time: `1005.00 s`
