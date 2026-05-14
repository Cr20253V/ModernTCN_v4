# ModernTCN Theta Sweep Plot Report

- Path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_modern_tcn_theta_sweep_multicond_v4_theta0p2.mat`
- Data file: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v4_theta0p2\ModernTCN_theta_sweep_multicond_v4_theta0p2_data.mat`
- Model seed: `21`
- ONNX file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta10_uniform_h0_v2_seed21\modern_tcn_seed21.onnx`
- Sweep: -10.0 to 10.0 deg, step 0.2 deg, segment 3.20 s, v=1.00 m/s
- Scatter metric source: `window`; show segment median: `0`
- Path repeats: `4`; v variants: `1`; omega variants: `0`; duration variants: `3.2`
- Evaluation windows: tail 1.20 s, stride 0.100 s, margin 0.10 s
- Note: held-out paper plotting set; not added to training data.

## Segment median, all theta

| metric | value |
|---|---:|
| n | 404 |
| MAE (deg) | 0.407795 |
| RMSE (deg) | 0.595338 |
| P95 abs error (deg) | 1.082926 |
| Peak abs error (deg) | 2.814495 |
| Bias (deg) | 0.032673 |
| Fit slope | 0.964693 |
| Fit intercept (deg) | 0.032673 |
| Pearson r | 0.995122 |
| R2 identity | 0.989576 |

## Segment median, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 328 |
| MAE (deg) | 0.410116 |
| RMSE (deg) | 0.619877 |
| P95 abs error (deg) | 1.229351 |
| Peak abs error (deg) | 2.814495 |
| Bias (deg) | 0.011540 |
| Fit slope | 0.965180 |
| Fit intercept (deg) | 0.011540 |
| Pearson r | 0.995722 |
| R2 identity | 0.990763 |

## Segment median, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 324 |
| MAE (deg) | 0.353472 |
| RMSE (deg) | 0.438936 |
| P95 abs error (deg) | 0.908182 |
| Peak abs error (deg) | 1.106275 |
| Bias (deg) | 0.172547 |
| Fit slope | 0.993870 |
| Fit intercept (deg) | 0.172547 |
| Pearson r | 0.996269 |
| R2 identity | 0.991189 |

## Segment median, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 404 |
| MAE (deg) | 0.407795 |
| RMSE (deg) | 0.595338 |
| P95 abs error (deg) | 1.082926 |
| Peak abs error (deg) | 2.814495 |
| Bias (deg) | 0.032673 |
| Fit slope | 0.964693 |
| Fit intercept (deg) | 0.032673 |
| Pearson r | 0.995122 |
| R2 identity | 0.989576 |

## Window-level, all theta

| metric | value |
|---|---:|
| n | 5252 |
| MAE (deg) | 0.525567 |
| RMSE (deg) | 0.742899 |
| P95 abs error (deg) | 1.505588 |
| Peak abs error (deg) | 3.429401 |
| Bias (deg) | 0.005621 |
| Fit slope | 0.958805 |
| Fit intercept (deg) | 0.005621 |
| Pearson r | 0.992187 |
| R2 identity | 0.983768 |

## Window-level, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 4264 |
| MAE (deg) | 0.522434 |
| RMSE (deg) | 0.763536 |
| P95 abs error (deg) | 1.594166 |
| Peak abs error (deg) | 3.429401 |
| Bias (deg) | -0.021317 |
| Fit slope | 0.959072 |
| Fit intercept (deg) | -0.021317 |
| Pearson r | 0.993365 |
| R2 identity | 0.985986 |

## Window-level, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 4212 |
| MAE (deg) | 0.481626 |
| RMSE (deg) | 0.625163 |
| P95 abs error (deg) | 1.258869 |
| Peak abs error (deg) | 2.906109 |
| Bias (deg) | 0.145810 |
| Fit slope | 0.986601 |
| Fit intercept (deg) | 0.145810 |
| Pearson r | 0.991520 |
| R2 identity | 0.982127 |

## Window-level, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 5252 |
| MAE (deg) | 0.525567 |
| RMSE (deg) | 0.742899 |
| P95 abs error (deg) | 1.505588 |
| Peak abs error (deg) | 3.429401 |
| Bias (deg) | 0.005621 |
| Fit slope | 0.958805 |
| Fit intercept (deg) | 0.005621 |
| Pearson r | 0.992187 |
| R2 identity | 0.983768 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v4_theta0p2\modern_tcn_theta_sweep_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v4_theta0p2\modern_tcn_theta_sweep_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v4_theta0p2\modern_tcn_theta_sweep_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v4_theta0p2\modern_tcn_theta_sweep_residual.pdf`
- Segment CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v4_theta0p2\modern_tcn_theta_sweep_segment_summary.csv`
- Window CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v4_theta0p2\modern_tcn_theta_sweep_window_predictions.csv`
- Result MAT: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v4_theta0p2\modern_tcn_theta_sweep_eval_result.mat`

## Path Meta

- Path type: `path_modern_tcn_theta_sweep_plot_v1`
- Samples: `129280`
- Stop time: `1292.79 s`
