# ModernTCN Theta Sweep Plot Report

- Path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_modern_tcn_theta_sweep_multicond_probe.mat`
- Data file: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_probe\ModernTCN_theta_sweep_multicond_probe_data.mat`
- Model seed: `21`
- ONNX file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta10_uniform_h0_v2_seed21\modern_tcn_seed21.onnx`
- Sweep: -10.0 to 10.0 deg, step 0.5 deg, segment 3.20 s, v=0.90 m/s
- Scatter metric source: `window`; show segment median: `0`
- Path repeats: `6`; v variants: `0.9`; omega variants: `0`; duration variants: `3.2`
- Evaluation windows: tail 1.20 s, stride 0.100 s, margin 0.10 s
- Note: held-out paper plotting set; not added to training data.

## Segment median, all theta

| metric | value |
|---|---:|
| n | 246 |
| MAE (deg) | 0.935443 |
| RMSE (deg) | 1.643070 |
| P95 abs error (deg) | 4.173853 |
| Peak abs error (deg) | 5.578313 |
| Bias (deg) | 0.692963 |
| Fit slope | 0.965879 |
| Fit intercept (deg) | 0.692963 |
| Pearson r | 0.968219 |
| R2 identity | 0.922866 |

## Segment median, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 204 |
| MAE (deg) | 0.817124 |
| RMSE (deg) | 1.475552 |
| P95 abs error (deg) | 3.728131 |
| Peak abs error (deg) | 5.547449 |
| Bias (deg) | 0.527653 |
| Fit slope | 0.966384 |
| Fit intercept (deg) | 0.527653 |
| Pearson r | 0.977204 |
| R2 identity | 0.948161 |

## Segment median, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 198 |
| MAE (deg) | 1.074953 |
| RMSE (deg) | 1.811394 |
| P95 abs error (deg) | 4.700511 |
| Peak abs error (deg) | 5.578313 |
| Bias (deg) | 0.925963 |
| Fit slope | 0.949096 |
| Fit intercept (deg) | 0.925963 |
| Pearson r | 0.946675 |
| R2 identity | 0.855243 |

## Segment median, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 246 |
| MAE (deg) | 0.935443 |
| RMSE (deg) | 1.643070 |
| P95 abs error (deg) | 4.173853 |
| Peak abs error (deg) | 5.578313 |
| Bias (deg) | 0.692963 |
| Fit slope | 0.965879 |
| Fit intercept (deg) | 0.692963 |
| Pearson r | 0.968219 |
| R2 identity | 0.922866 |

## Window-level, all theta

| metric | value |
|---|---:|
| n | 3198 |
| MAE (deg) | 0.946291 |
| RMSE (deg) | 1.652779 |
| P95 abs error (deg) | 4.263239 |
| Peak abs error (deg) | 5.602408 |
| Bias (deg) | 0.695418 |
| Fit slope | 0.966139 |
| Fit intercept (deg) | 0.695418 |
| Pearson r | 0.967830 |
| R2 identity | 0.921952 |

## Window-level, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 2652 |
| MAE (deg) | 0.828950 |
| RMSE (deg) | 1.484997 |
| P95 abs error (deg) | 3.769870 |
| Peak abs error (deg) | 5.573485 |
| Bias (deg) | 0.529497 |
| Fit slope | 0.966633 |
| Fit intercept (deg) | 0.529497 |
| Pearson r | 0.976898 |
| R2 identity | 0.947495 |

## Window-level, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 2574 |
| MAE (deg) | 1.084404 |
| RMSE (deg) | 1.820698 |
| P95 abs error (deg) | 4.698476 |
| Peak abs error (deg) | 5.602408 |
| Bias (deg) | 0.929316 |
| Fit slope | 0.949508 |
| Fit intercept (deg) | 0.929316 |
| Pearson r | 0.946126 |
| R2 identity | 0.853753 |

## Window-level, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 3198 |
| MAE (deg) | 0.946291 |
| RMSE (deg) | 1.652779 |
| P95 abs error (deg) | 4.263239 |
| Peak abs error (deg) | 5.602408 |
| Bias (deg) | 0.695418 |
| Fit slope | 0.966139 |
| Fit intercept (deg) | 0.695418 |
| Pearson r | 0.967830 |
| R2 identity | 0.921952 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_probe\modern_tcn_theta_sweep_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_probe\modern_tcn_theta_sweep_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_probe\modern_tcn_theta_sweep_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_probe\modern_tcn_theta_sweep_residual.pdf`
- Segment CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_probe\modern_tcn_theta_sweep_segment_summary.csv`
- Window CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_probe\modern_tcn_theta_sweep_window_predictions.csv`
- Result MAT: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_probe\modern_tcn_theta_sweep_eval_result.mat`

## Path Meta

- Path type: `path_modern_tcn_theta_sweep_plot_v1`
- Samples: `78720`
- Stop time: `787.19 s`
