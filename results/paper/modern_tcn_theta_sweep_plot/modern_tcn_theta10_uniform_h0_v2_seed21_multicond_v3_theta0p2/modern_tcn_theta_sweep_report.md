# ModernTCN Theta Sweep Plot Report

- Path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_modern_tcn_theta_sweep_multicond_v3_theta0p2.mat`
- Data file: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v3_theta0p2\ModernTCN_theta_sweep_multicond_v3_theta0p2_data.mat`
- Model seed: `21`
- ONNX file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta10_uniform_h0_v2_seed21\modern_tcn_seed21.onnx`
- Sweep: -10.0 to 10.0 deg, step 0.2 deg, segment 3.20 s, v=0.95 m/s
- Scatter metric source: `window`; show segment median: `0`
- Path repeats: `5`; v variants: `0.95`; omega variants: `0`; duration variants: `3.2`
- Evaluation windows: tail 1.20 s, stride 0.100 s, margin 0.10 s
- Note: held-out paper plotting set; not added to training data.

## Segment median, all theta

| metric | value |
|---|---:|
| n | 505 |
| MAE (deg) | 0.297920 |
| RMSE (deg) | 0.425769 |
| P95 abs error (deg) | 0.774559 |
| Peak abs error (deg) | 3.336958 |
| Bias (deg) | 0.017898 |
| Fit slope | 0.983374 |
| Fit intercept (deg) | 0.017898 |
| Pearson r | 0.997401 |
| R2 identity | 0.994668 |

## Segment median, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 410 |
| MAE (deg) | 0.299281 |
| RMSE (deg) | 0.427818 |
| P95 abs error (deg) | 0.803603 |
| Peak abs error (deg) | 3.336958 |
| Bias (deg) | 0.027756 |
| Fit slope | 0.982986 |
| Fit intercept (deg) | 0.027756 |
| Pearson r | 0.997889 |
| R2 identity | 0.995600 |

## Segment median, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 405 |
| MAE (deg) | 0.297906 |
| RMSE (deg) | 0.426623 |
| P95 abs error (deg) | 0.749969 |
| Peak abs error (deg) | 3.336958 |
| Bias (deg) | 0.080507 |
| Fit slope | 0.994332 |
| Fit intercept (deg) | 0.080507 |
| Pearson r | 0.995981 |
| R2 identity | 0.991677 |

## Segment median, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 505 |
| MAE (deg) | 0.297920 |
| RMSE (deg) | 0.425769 |
| P95 abs error (deg) | 0.774559 |
| Peak abs error (deg) | 3.336958 |
| Bias (deg) | 0.017898 |
| Fit slope | 0.983374 |
| Fit intercept (deg) | 0.017898 |
| Pearson r | 0.997401 |
| R2 identity | 0.994668 |

## Window-level, all theta

| metric | value |
|---|---:|
| n | 6565 |
| MAE (deg) | 0.338298 |
| RMSE (deg) | 0.470761 |
| P95 abs error (deg) | 0.957990 |
| Peak abs error (deg) | 3.770817 |
| Bias (deg) | 0.026448 |
| Fit slope | 0.983877 |
| Fit intercept (deg) | 0.026448 |
| Pearson r | 0.996794 |
| R2 identity | 0.993482 |

## Window-level, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 5330 |
| MAE (deg) | 0.337001 |
| RMSE (deg) | 0.469023 |
| P95 abs error (deg) | 0.958837 |
| Peak abs error (deg) | 3.770817 |
| Bias (deg) | 0.036737 |
| Fit slope | 0.983568 |
| Fit intercept (deg) | 0.036737 |
| Pearson r | 0.997433 |
| R2 identity | 0.994712 |

## Window-level, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 5265 |
| MAE (deg) | 0.338962 |
| RMSE (deg) | 0.472456 |
| P95 abs error (deg) | 0.959098 |
| Peak abs error (deg) | 3.770817 |
| Bias (deg) | 0.088396 |
| Fit slope | 0.994864 |
| Fit intercept (deg) | 0.088396 |
| Pearson r | 0.995074 |
| R2 identity | 0.989792 |

## Window-level, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 6565 |
| MAE (deg) | 0.338298 |
| RMSE (deg) | 0.470761 |
| P95 abs error (deg) | 0.957990 |
| Peak abs error (deg) | 3.770817 |
| Bias (deg) | 0.026448 |
| Fit slope | 0.983877 |
| Fit intercept (deg) | 0.026448 |
| Pearson r | 0.996794 |
| R2 identity | 0.993482 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v3_theta0p2\modern_tcn_theta_sweep_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v3_theta0p2\modern_tcn_theta_sweep_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v3_theta0p2\modern_tcn_theta_sweep_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v3_theta0p2\modern_tcn_theta_sweep_residual.pdf`
- Segment CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v3_theta0p2\modern_tcn_theta_sweep_segment_summary.csv`
- Window CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v3_theta0p2\modern_tcn_theta_sweep_window_predictions.csv`
- Result MAT: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v3_theta0p2\modern_tcn_theta_sweep_eval_result.mat`

## Path Meta

- Path type: `path_modern_tcn_theta_sweep_plot_v1`
- Samples: `161600`
- Stop time: `1615.99 s`
