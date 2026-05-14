# ModernTCN Theta Sweep Plot Report

- Path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_modern_tcn_theta_sweep_plot_v1.mat`
- Data file: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\ModernTCN_theta_sweep_plot_data.mat`
- Model seed: `21`
- ONNX file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_seed21.onnx`
- Sweep: -10.0 to 10.0 deg, step 0.1 deg, segment 5.00 s, v=0.90 m/s
- Note: held-out paper plotting set; not added to training data.

## Segment median, all theta

| metric | value |
|---|---:|
| n | 201 |
| MAE (deg) | 0.595210 |
| RMSE (deg) | 0.851487 |
| P95 abs error (deg) | 2.149365 |
| Peak abs error (deg) | 2.643990 |
| Bias (deg) | -0.377426 |
| Fit slope | 0.891602 |
| Fit intercept (deg) | -0.377426 |
| Pearson r | 0.996525 |
| R2 identity | 0.978464 |

## Segment median, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 162 |
| MAE (deg) | 0.618947 |
| RMSE (deg) | 0.904768 |
| P95 abs error (deg) | 2.280994 |
| Peak abs error (deg) | 2.643990 |
| Bias (deg) | -0.470795 |
| Fit slope | 0.893806 |
| Fit intercept (deg) | -0.470795 |
| Pearson r | 0.998054 |
| R2 identity | 0.980259 |

## Segment median, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 161 |
| MAE (deg) | 0.465715 |
| RMSE (deg) | 0.580293 |
| P95 abs error (deg) | 1.099361 |
| Peak abs error (deg) | 1.490002 |
| Bias (deg) | -0.222478 |
| Fit slope | 0.905519 |
| Fit intercept (deg) | -0.222478 |
| Pearson r | 0.997345 |
| R2 identity | 0.984410 |

## Segment median, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 201 |
| MAE (deg) | 0.595210 |
| RMSE (deg) | 0.851487 |
| P95 abs error (deg) | 2.149365 |
| Peak abs error (deg) | 2.643990 |
| Bias (deg) | -0.377426 |
| Fit slope | 0.891602 |
| Fit intercept (deg) | -0.377426 |
| Pearson r | 0.996525 |
| R2 identity | 0.978464 |

## Window-level, all theta

| metric | value |
|---|---:|
| n | 2211 |
| MAE (deg) | 0.595240 |
| RMSE (deg) | 0.851354 |
| P95 abs error (deg) | 2.118682 |
| Peak abs error (deg) | 2.647081 |
| Bias (deg) | -0.377454 |
| Fit slope | 0.891671 |
| Fit intercept (deg) | -0.377454 |
| Pearson r | 0.996521 |
| R2 identity | 0.978471 |

## Window-level, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 1782 |
| MAE (deg) | 0.619047 |
| RMSE (deg) | 0.904653 |
| P95 abs error (deg) | 2.265881 |
| Peak abs error (deg) | 2.647081 |
| Bias (deg) | -0.470845 |
| Fit slope | 0.893875 |
| Fit intercept (deg) | -0.470845 |
| Pearson r | 0.998049 |
| R2 identity | 0.980264 |

## Window-level, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 1771 |
| MAE (deg) | 0.465567 |
| RMSE (deg) | 0.580105 |
| P95 abs error (deg) | 1.086895 |
| Peak abs error (deg) | 1.494522 |
| Bias (deg) | -0.222334 |
| Fit slope | 0.905539 |
| Fit intercept (deg) | -0.222334 |
| Pearson r | 0.997347 |
| R2 identity | 0.984420 |

## Window-level, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 2211 |
| MAE (deg) | 0.595240 |
| RMSE (deg) | 0.851354 |
| P95 abs error (deg) | 2.118682 |
| Peak abs error (deg) | 2.647081 |
| Bias (deg) | -0.377454 |
| Fit slope | 0.891671 |
| Fit intercept (deg) | -0.377454 |
| Pearson r | 0.996521 |
| R2 identity | 0.978471 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_sweep_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_sweep_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_sweep_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_sweep_residual.pdf`
- Segment CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_sweep_segment_summary.csv`
- Window CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_sweep_window_predictions.csv`
- Result MAT: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_sweep_eval_result.mat`

## Path Meta

- Path type: `path_modern_tcn_theta_sweep_plot_v1`
- Samples: `100501`
- Stop time: `1005.00 s`
