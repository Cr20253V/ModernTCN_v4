# ModernTCN Theta Sweep Plot Report

- Path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_modern_tcn_theta_sweep_plot_v1.mat`
- Data file: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\ModernTCN_theta_sweep_plot_data.mat`
- Model seed: `21`
- ONNX file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta10_uniform_h0_v2_seed21\modern_tcn_seed21.onnx`
- Sweep: -10.0 to 10.0 deg, step 0.1 deg, segment 5.00 s, v=0.90 m/s
- Scatter metric source: `segment`; show segment median: `1`
- Path repeats: `1`; v variants: `0.9`; omega variants: `0`; duration variants: `5`
- Evaluation windows: tail 1.00 s, stride 0.100 s, margin 0.10 s
- Note: held-out paper plotting set; not added to training data.

## Segment median, all theta

| metric | value |
|---|---:|
| n | 201 |
| MAE (deg) | 0.117589 |
| RMSE (deg) | 0.173201 |
| P95 abs error (deg) | 0.479864 |
| Peak abs error (deg) | 0.552534 |
| Bias (deg) | -0.062774 |
| Fit slope | 0.981901 |
| Fit intercept (deg) | -0.062774 |
| Pearson r | 0.999769 |
| R2 identity | 0.999109 |

## Segment median, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 162 |
| MAE (deg) | 0.126110 |
| RMSE (deg) | 0.187536 |
| P95 abs error (deg) | 0.493489 |
| Peak abs error (deg) | 0.552534 |
| Bias (deg) | -0.072223 |
| Fit slope | 0.982187 |
| Fit intercept (deg) | -0.072223 |
| Pearson r | 0.999790 |
| R2 identity | 0.999152 |

## Segment median, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 161 |
| MAE (deg) | 0.081601 |
| RMSE (deg) | 0.099304 |
| P95 abs error (deg) | 0.198906 |
| Peak abs error (deg) | 0.248694 |
| Bias (deg) | -0.020319 |
| Fit slope | 0.988223 |
| Fit intercept (deg) | -0.020319 |
| Pearson r | 0.999847 |
| R2 identity | 0.999543 |

## Segment median, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 201 |
| MAE (deg) | 0.117589 |
| RMSE (deg) | 0.173201 |
| P95 abs error (deg) | 0.479864 |
| Peak abs error (deg) | 0.552534 |
| Bias (deg) | -0.062774 |
| Fit slope | 0.981901 |
| Fit intercept (deg) | -0.062774 |
| Pearson r | 0.999769 |
| R2 identity | 0.999109 |

## Window-level, all theta

| metric | value |
|---|---:|
| n | 2211 |
| MAE (deg) | 0.117794 |
| RMSE (deg) | 0.173243 |
| P95 abs error (deg) | 0.476042 |
| Peak abs error (deg) | 0.555966 |
| Bias (deg) | -0.062682 |
| Fit slope | 0.981862 |
| Fit intercept (deg) | -0.062682 |
| Pearson r | 0.999769 |
| R2 identity | 0.999109 |

## Window-level, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 1782 |
| MAE (deg) | 0.126351 |
| RMSE (deg) | 0.187580 |
| P95 abs error (deg) | 0.492990 |
| Peak abs error (deg) | 0.555966 |
| Bias (deg) | -0.072097 |
| Fit slope | 0.982148 |
| Fit intercept (deg) | -0.072097 |
| Pearson r | 0.999790 |
| R2 identity | 0.999151 |

## Window-level, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 1771 |
| MAE (deg) | 0.081640 |
| RMSE (deg) | 0.099325 |
| P95 abs error (deg) | 0.199722 |
| Peak abs error (deg) | 0.249193 |
| Bias (deg) | -0.020403 |
| Fit slope | 0.988223 |
| Fit intercept (deg) | -0.020403 |
| Pearson r | 0.999847 |
| R2 identity | 0.999543 |

## Window-level, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 2211 |
| MAE (deg) | 0.117794 |
| RMSE (deg) | 0.173243 |
| P95 abs error (deg) | 0.476042 |
| Peak abs error (deg) | 0.555966 |
| Bias (deg) | -0.062682 |
| Fit slope | 0.981862 |
| Fit intercept (deg) | -0.062682 |
| Pearson r | 0.999769 |
| R2 identity | 0.999109 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_legacy_data\modern_tcn_theta_sweep_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_legacy_data\modern_tcn_theta_sweep_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_legacy_data\modern_tcn_theta_sweep_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_legacy_data\modern_tcn_theta_sweep_residual.pdf`
- Segment CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_legacy_data\modern_tcn_theta_sweep_segment_summary.csv`
- Window CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_legacy_data\modern_tcn_theta_sweep_window_predictions.csv`
- Result MAT: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_legacy_data\modern_tcn_theta_sweep_eval_result.mat`

## Path Meta

- Path type: `path_modern_tcn_theta_sweep_plot_v1`
- Samples: `100501`
- Stop time: `1005.00 s`
