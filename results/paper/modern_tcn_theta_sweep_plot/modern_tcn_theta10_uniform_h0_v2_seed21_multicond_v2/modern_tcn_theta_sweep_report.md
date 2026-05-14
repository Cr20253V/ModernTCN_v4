# ModernTCN Theta Sweep Plot Report

- Path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_modern_tcn_theta_sweep_multicond_v2.mat`
- Data file: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v2\ModernTCN_theta_sweep_multicond_v2_data.mat`
- Model seed: `21`
- ONNX file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta10_uniform_h0_v2_seed21\modern_tcn_seed21.onnx`
- Sweep: -10.0 to 10.0 deg, step 0.1 deg, segment 3.20 s, v=0.95 m/s
- Scatter metric source: `window`; show segment median: `0`
- Path repeats: `7`; v variants: `0.95`; omega variants: `0`; duration variants: `3.2`
- Evaluation windows: tail 1.20 s, stride 0.100 s, margin 0.10 s
- Note: held-out paper plotting set; not added to training data.

## Segment median, all theta

| metric | value |
|---|---:|
| n | 1407 |
| MAE (deg) | 1.070660 |
| RMSE (deg) | 2.061142 |
| P95 abs error (deg) | 5.503037 |
| Peak abs error (deg) | 7.207400 |
| Bias (deg) | 0.856726 |
| Fit slope | 0.930376 |
| Fit intercept (deg) | 0.856726 |
| Pearson r | 0.947030 |
| R2 identity | 0.873813 |

## Segment median, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 1134 |
| MAE (deg) | 0.947295 |
| RMSE (deg) | 1.972191 |
| P95 abs error (deg) | 5.946026 |
| Peak abs error (deg) | 7.207400 |
| Bias (deg) | 0.692058 |
| Fit slope | 0.931778 |
| Fit intercept (deg) | 0.692058 |
| Pearson r | 0.958102 |
| R2 identity | 0.906201 |

## Segment median, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 1127 |
| MAE (deg) | 1.255480 |
| RMSE (deg) | 2.289413 |
| P95 abs error (deg) | 5.949514 |
| Peak abs error (deg) | 7.207400 |
| Bias (deg) | 1.094775 |
| Fit slope | 0.890198 |
| Fit intercept (deg) | 1.094775 |
| Pearson r | 0.904995 |
| R2 identity | 0.757342 |

## Segment median, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 1407 |
| MAE (deg) | 1.070660 |
| RMSE (deg) | 2.061142 |
| P95 abs error (deg) | 5.503037 |
| Peak abs error (deg) | 7.207400 |
| Bias (deg) | 0.856726 |
| Fit slope | 0.930376 |
| Fit intercept (deg) | 0.856726 |
| Pearson r | 0.947030 |
| R2 identity | 0.873813 |

## Window-level, all theta

| metric | value |
|---|---:|
| n | 18291 |
| MAE (deg) | 1.076348 |
| RMSE (deg) | 2.062241 |
| P95 abs error (deg) | 5.434510 |
| Peak abs error (deg) | 7.212360 |
| Bias (deg) | 0.855710 |
| Fit slope | 0.930700 |
| Fit intercept (deg) | 0.855710 |
| Pearson r | 0.946951 |
| R2 identity | 0.873678 |

## Window-level, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 14742 |
| MAE (deg) | 0.953894 |
| RMSE (deg) | 1.973512 |
| P95 abs error (deg) | 5.947328 |
| Peak abs error (deg) | 7.212360 |
| Bias (deg) | 0.691052 |
| Fit slope | 0.932094 |
| Fit intercept (deg) | 0.691052 |
| Pearson r | 0.958026 |
| R2 identity | 0.906075 |

## Window-level, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 14651 |
| MAE (deg) | 1.259428 |
| RMSE (deg) | 2.290062 |
| P95 abs error (deg) | 5.949542 |
| Peak abs error (deg) | 7.212360 |
| Bias (deg) | 1.093858 |
| Fit slope | 0.890469 |
| Fit intercept (deg) | 1.093858 |
| Pearson r | 0.904909 |
| R2 identity | 0.757205 |

## Window-level, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 18291 |
| MAE (deg) | 1.076348 |
| RMSE (deg) | 2.062241 |
| P95 abs error (deg) | 5.434510 |
| Peak abs error (deg) | 7.212360 |
| Bias (deg) | 0.855710 |
| Fit slope | 0.930700 |
| Fit intercept (deg) | 0.855710 |
| Pearson r | 0.946951 |
| R2 identity | 0.873678 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v2\modern_tcn_theta_sweep_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v2\modern_tcn_theta_sweep_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v2\modern_tcn_theta_sweep_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v2\modern_tcn_theta_sweep_residual.pdf`
- Segment CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v2\modern_tcn_theta_sweep_segment_summary.csv`
- Window CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v2\modern_tcn_theta_sweep_window_predictions.csv`
- Result MAT: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v2\modern_tcn_theta_sweep_eval_result.mat`

## Path Meta

- Path type: `path_modern_tcn_theta_sweep_plot_v1`
- Samples: `450240`
- Stop time: `4502.39 s`
