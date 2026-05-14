# ModernTCN Theta Sweep Plot Report

- Path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_modern_tcn_theta_sweep_plot_v1.mat`
- Data file: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\ModernTCN_theta_sweep_plot_data.mat`
- Model seed: `21`
- ONNX file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta_calib_w1p0_lam055_f100_nf200_seed21\modern_tcn_seed21.onnx`
- Sweep: -10.0 to 10.0 deg, step 0.1 deg, segment 5.00 s, v=0.90 m/s
- Note: held-out paper plotting set; not added to training data.

## Segment median, all theta

| metric | value |
|---|---:|
| n | 201 |
| MAE (deg) | 0.680273 |
| RMSE (deg) | 0.920381 |
| P95 abs error (deg) | 2.281269 |
| Peak abs error (deg) | 2.794839 |
| Bias (deg) | -0.356921 |
| Fit slope | 0.873117 |
| Fit intercept (deg) | -0.356921 |
| Pearson r | 0.996556 |
| R2 identity | 0.974839 |

## Segment median, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 162 |
| MAE (deg) | 0.732643 |
| RMSE (deg) | 0.990722 |
| P95 abs error (deg) | 2.430444 |
| Peak abs error (deg) | 2.794839 |
| Bias (deg) | -0.439632 |
| Fit slope | 0.874913 |
| Fit intercept (deg) | -0.439632 |
| Pearson r | 0.997811 |
| R2 identity | 0.976330 |

## Segment median, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 161 |
| MAE (deg) | 0.539285 |
| RMSE (deg) | 0.639625 |
| P95 abs error (deg) | 1.248172 |
| Peak abs error (deg) | 1.613241 |
| Bias (deg) | -0.197736 |
| Fit slope | 0.883914 |
| Fit intercept (deg) | -0.197736 |
| Pearson r | 0.997669 |
| R2 identity | 0.981059 |

## Segment median, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 201 |
| MAE (deg) | 0.680273 |
| RMSE (deg) | 0.920381 |
| P95 abs error (deg) | 2.281269 |
| Peak abs error (deg) | 2.794839 |
| Bias (deg) | -0.356921 |
| Fit slope | 0.873117 |
| Fit intercept (deg) | -0.356921 |
| Pearson r | 0.996556 |
| R2 identity | 0.974839 |

## Window-level, all theta

| metric | value |
|---|---:|
| n | 2211 |
| MAE (deg) | 0.680051 |
| RMSE (deg) | 0.920212 |
| P95 abs error (deg) | 2.249417 |
| Peak abs error (deg) | 2.799200 |
| Bias (deg) | -0.356844 |
| Fit slope | 0.873163 |
| Fit intercept (deg) | -0.356844 |
| Pearson r | 0.996554 |
| R2 identity | 0.974848 |

## Window-level, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 1782 |
| MAE (deg) | 0.732412 |
| RMSE (deg) | 0.990553 |
| P95 abs error (deg) | 2.406900 |
| Peak abs error (deg) | 2.799200 |
| Bias (deg) | -0.439544 |
| Fit slope | 0.874958 |
| Fit intercept (deg) | -0.439544 |
| Pearson r | 0.997808 |
| R2 identity | 0.976338 |

## Window-level, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 1771 |
| MAE (deg) | 0.539157 |
| RMSE (deg) | 0.639460 |
| P95 abs error (deg) | 1.237046 |
| Peak abs error (deg) | 1.619049 |
| Bias (deg) | -0.197559 |
| Fit slope | 0.883934 |
| Fit intercept (deg) | -0.197559 |
| Pearson r | 0.997671 |
| R2 identity | 0.981069 |

## Window-level, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 2211 |
| MAE (deg) | 0.680051 |
| RMSE (deg) | 0.920212 |
| P95 abs error (deg) | 2.249417 |
| Peak abs error (deg) | 2.799200 |
| Bias (deg) | -0.356844 |
| Fit slope | 0.873163 |
| Fit intercept (deg) | -0.356844 |
| Pearson r | 0.996554 |
| R2 identity | 0.974848 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0_lam055_f100_nf200_seed21\modern_tcn_theta_sweep_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0_lam055_f100_nf200_seed21\modern_tcn_theta_sweep_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0_lam055_f100_nf200_seed21\modern_tcn_theta_sweep_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0_lam055_f100_nf200_seed21\modern_tcn_theta_sweep_residual.pdf`
- Segment CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0_lam055_f100_nf200_seed21\modern_tcn_theta_sweep_segment_summary.csv`
- Window CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0_lam055_f100_nf200_seed21\modern_tcn_theta_sweep_window_predictions.csv`
- Result MAT: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_calib_w1p0_lam055_f100_nf200_seed21\modern_tcn_theta_sweep_eval_result.mat`

## Path Meta

- Path type: `path_modern_tcn_theta_sweep_plot_v1`
- Samples: `100501`
- Stop time: `1005.00 s`
