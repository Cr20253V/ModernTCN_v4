# ModernTCN Theta Sweep Plot Report

- Path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_modern_tcn_theta_sweep_plot_v1.mat`
- Data file: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\ModernTCN_theta_sweep_plot_data.mat`
- Model seed: `21`
- ONNX file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta_calib_uflast_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_seed21.onnx`
- Sweep: -10.0 to 10.0 deg, step 0.1 deg, segment 5.00 s, v=0.90 m/s
- Note: held-out paper plotting set; not added to training data.

## Segment median, all theta

| metric | value |
|---|---:|
| n | 201 |
| MAE (deg) | 0.635929 |
| RMSE (deg) | 0.841135 |
| P95 abs error (deg) | 2.106813 |
| Peak abs error (deg) | 2.581054 |
| Bias (deg) | -0.269605 |
| Fit slope | 0.884067 |
| Fit intercept (deg) | -0.269605 |
| Pearson r | 0.996553 |
| R2 identity | 0.978985 |

## Segment median, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 162 |
| MAE (deg) | 0.668671 |
| RMSE (deg) | 0.892060 |
| P95 abs error (deg) | 2.243343 |
| Peak abs error (deg) | 2.581054 |
| Bias (deg) | -0.355000 |
| Fit slope | 0.886195 |
| Fit intercept (deg) | -0.355000 |
| Pearson r | 0.997969 |
| R2 identity | 0.980809 |

## Segment median, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 161 |
| MAE (deg) | 0.506426 |
| RMSE (deg) | 0.578558 |
| P95 abs error (deg) | 1.097058 |
| Peak abs error (deg) | 1.424223 |
| Bias (deg) | -0.112425 |
| Fit slope | 0.895764 |
| Fit intercept (deg) | -0.112425 |
| Pearson r | 0.997488 |
| R2 identity | 0.984503 |

## Segment median, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 201 |
| MAE (deg) | 0.635929 |
| RMSE (deg) | 0.841135 |
| P95 abs error (deg) | 2.106813 |
| Peak abs error (deg) | 2.581054 |
| Bias (deg) | -0.269605 |
| Fit slope | 0.884067 |
| Fit intercept (deg) | -0.269605 |
| Pearson r | 0.996553 |
| R2 identity | 0.978985 |

## Window-level, all theta

| metric | value |
|---|---:|
| n | 2211 |
| MAE (deg) | 0.635910 |
| RMSE (deg) | 0.840982 |
| P95 abs error (deg) | 2.075245 |
| Peak abs error (deg) | 2.584246 |
| Bias (deg) | -0.269613 |
| Fit slope | 0.884139 |
| Fit intercept (deg) | -0.269613 |
| Pearson r | 0.996548 |
| R2 identity | 0.978993 |

## Window-level, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 1782 |
| MAE (deg) | 0.668707 |
| RMSE (deg) | 0.891919 |
| P95 abs error (deg) | 2.227689 |
| Peak abs error (deg) | 2.584246 |
| Bias (deg) | -0.355022 |
| Fit slope | 0.886265 |
| Fit intercept (deg) | -0.355022 |
| Pearson r | 0.997963 |
| R2 identity | 0.980815 |

## Window-level, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 1771 |
| MAE (deg) | 0.506272 |
| RMSE (deg) | 0.578380 |
| P95 abs error (deg) | 1.094833 |
| Peak abs error (deg) | 1.429169 |
| Bias (deg) | -0.112252 |
| Fit slope | 0.895788 |
| Fit intercept (deg) | -0.112252 |
| Pearson r | 0.997490 |
| R2 identity | 0.984513 |

## Window-level, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 2211 |
| MAE (deg) | 0.635910 |
| RMSE (deg) | 0.840982 |
| P95 abs error (deg) | 2.075245 |
| Peak abs error (deg) | 2.584246 |
| Bias (deg) | -0.269613 |
| Fit slope | 0.884139 |
| Fit intercept (deg) | -0.269613 |
| Pearson r | 0.996548 |
| R2 identity | 0.978993 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_uflast_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_theta_sweep_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_uflast_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_theta_sweep_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_uflast_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_theta_sweep_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_uflast_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_theta_sweep_residual.pdf`
- Segment CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_uflast_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_theta_sweep_segment_summary.csv`
- Window CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_uflast_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_theta_sweep_window_predictions.csv`
- Result MAT: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_uflast_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_theta_sweep_eval_result.mat`

## Path Meta

- Path type: `path_modern_tcn_theta_sweep_plot_v1`
- Samples: `100501`
- Stop time: `1005.00 s`
