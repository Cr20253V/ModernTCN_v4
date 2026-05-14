# ModernTCN Theta Sweep Plot Report

- Path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_modern_tcn_theta_sweep_plot_v1.mat`
- Data file: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\ModernTCN_theta_sweep_plot_data.mat`
- Model seed: `21`
- ONNX file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta_calib_w1p0_lam100_f100_nf200_seed21\modern_tcn_seed21.onnx`
- Sweep: -10.0 to 10.0 deg, step 0.1 deg, segment 5.00 s, v=0.90 m/s
- Note: held-out paper plotting set; not added to training data.

## Segment median, all theta

| metric | value |
|---|---:|
| n | 201 |
| MAE (deg) | 0.660349 |
| RMSE (deg) | 0.945399 |
| P95 abs error (deg) | 2.388174 |
| Peak abs error (deg) | 2.932481 |
| Bias (deg) | -0.426822 |
| Fit slope | 0.873963 |
| Fit intercept (deg) | -0.426822 |
| Pearson r | 0.996580 |
| R2 identity | 0.973452 |

## Segment median, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 162 |
| MAE (deg) | 0.725507 |
| RMSE (deg) | 1.028770 |
| P95 abs error (deg) | 2.549798 |
| Peak abs error (deg) | 2.932481 |
| Bias (deg) | -0.505472 |
| Fit slope | 0.875365 |
| Fit intercept (deg) | -0.505472 |
| Pearson r | 0.997512 |
| R2 identity | 0.974477 |

## Segment median, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 161 |
| MAE (deg) | 0.510366 |
| RMSE (deg) | 0.637659 |
| P95 abs error (deg) | 1.325528 |
| Peak abs error (deg) | 1.697928 |
| Bias (deg) | -0.261468 |
| Fit slope | 0.887275 |
| Fit intercept (deg) | -0.261468 |
| Pearson r | 0.998130 |
| R2 identity | 0.981176 |

## Segment median, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 201 |
| MAE (deg) | 0.660349 |
| RMSE (deg) | 0.945399 |
| P95 abs error (deg) | 2.388174 |
| Peak abs error (deg) | 2.932481 |
| Bias (deg) | -0.426822 |
| Fit slope | 0.873963 |
| Fit intercept (deg) | -0.426822 |
| Pearson r | 0.996580 |
| R2 identity | 0.973452 |

## Window-level, all theta

| metric | value |
|---|---:|
| n | 2211 |
| MAE (deg) | 0.660181 |
| RMSE (deg) | 0.945219 |
| P95 abs error (deg) | 2.353949 |
| Peak abs error (deg) | 2.936966 |
| Bias (deg) | -0.426675 |
| Fit slope | 0.873989 |
| Fit intercept (deg) | -0.426675 |
| Pearson r | 0.996580 |
| R2 identity | 0.973462 |

## Window-level, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 1782 |
| MAE (deg) | 0.725338 |
| RMSE (deg) | 1.028586 |
| P95 abs error (deg) | 2.523743 |
| Peak abs error (deg) | 2.936966 |
| Bias (deg) | -0.505285 |
| Fit slope | 0.875390 |
| Fit intercept (deg) | -0.505285 |
| Pearson r | 0.997511 |
| R2 identity | 0.974486 |

## Window-level, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 1771 |
| MAE (deg) | 0.510204 |
| RMSE (deg) | 0.637448 |
| P95 abs error (deg) | 1.314500 |
| Peak abs error (deg) | 1.704244 |
| Bias (deg) | -0.261306 |
| Fit slope | 0.887305 |
| Fit intercept (deg) | -0.261306 |
| Pearson r | 0.998131 |
| R2 identity | 0.981188 |

## Window-level, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 2211 |
| MAE (deg) | 0.660181 |
| RMSE (deg) | 0.945219 |
| P95 abs error (deg) | 2.353949 |
| Peak abs error (deg) | 2.936966 |
| Bias (deg) | -0.426675 |
| Fit slope | 0.873989 |
| Fit intercept (deg) | -0.426675 |
| Pearson r | 0.996580 |
| R2 identity | 0.973462 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_sweep_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_sweep_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_sweep_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_sweep_residual.pdf`
- Segment CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_sweep_segment_summary.csv`
- Window CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_sweep_window_predictions.csv`
- Result MAT: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_sweep_eval_result.mat`

## Path Meta

- Path type: `path_modern_tcn_theta_sweep_plot_v1`
- Samples: `100501`
- Stop time: `1005.00 s`
