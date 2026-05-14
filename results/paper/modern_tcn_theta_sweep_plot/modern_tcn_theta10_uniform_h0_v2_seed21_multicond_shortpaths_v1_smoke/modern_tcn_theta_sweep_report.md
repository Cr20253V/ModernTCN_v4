# ModernTCN Theta Sweep Plot Report

- Path files: `3`
- First path file: `E:\Matlab\Simulink\S-Function_16\data\paths\modern_tcn_theta_sweep_multicond_shortpaths_v1_smoke\path_modern_tcn_theta_sweep_multicond_shortpaths_v1_smoke_001_p09p5_p09p6.mat`
- Last path file: `E:\Matlab\Simulink\S-Function_16\data\paths\modern_tcn_theta_sweep_multicond_shortpaths_v1_smoke\path_modern_tcn_theta_sweep_multicond_shortpaths_v1_smoke_003_p09p9_p10p0.mat`
- Data file: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_shortpaths_v1_smoke\ModernTCN_theta_sweep_smoke_shortpaths_v1_data.mat`
- Model seed: `21`
- Sweep: 9.5 to 10.0 deg, step 0.1 deg, segment 3.20 s, v=0.95 m/s
- Scatter metric source: `window`; show segment median: `0`
- Path repeats: `7`; explicit variants: `7`
- Evaluation windows: tail 1.20 s, stride 0.100 s, margin 0.10 s
- Note: held-out paper plotting set; not added to training data.

## Path Variants

| variant | v_ref (m/s) | omega_ref (rad/s) | radius (m) | segment (s) |
|---|---:|---:|---:|---:|
| straight_v080 | 0.800 | 0.000000 | Inf | 3.20 |
| straight_v095 | 0.950 | 0.000000 | Inf | 3.20 |
| straight_v115 | 1.150 | 0.000000 | Inf | 3.20 |
| left_R40_v095 | 0.950 | 0.023750 | 40.00 | 3.20 |
| right_R40_v095 | 0.950 | -0.023750 | 40.00 | 3.20 |
| left_R30_v105 | 1.050 | 0.035000 | 30.00 | 3.20 |
| right_R30_v105 | 1.050 | -0.035000 | 30.00 | 3.20 |

## Segment median, all theta

| metric | value |
|---|---:|
| n | 42 |
| MAE (deg) | 0.261068 |
| RMSE (deg) | 0.310722 |
| P95 abs error (deg) | 0.677457 |
| Peak abs error (deg) | 0.692334 |
| Bias (deg) | -0.222835 |
| Fit slope | 1.069372 |
| Fit intercept (deg) | -0.899210 |
| Pearson r | 0.645266 |
| R2 identity | -2.310221 |

## Segment median, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 42 |
| MAE (deg) | 0.261068 |
| RMSE (deg) | 0.310722 |
| P95 abs error (deg) | 0.677457 |
| Peak abs error (deg) | 0.692334 |
| Bias (deg) | -0.222835 |
| Fit slope | 1.069372 |
| Fit intercept (deg) | -0.899210 |
| Pearson r | 0.645266 |
| R2 identity | -2.310221 |

## Segment median, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 0 |
| MAE (deg) | NaN |
| RMSE (deg) | NaN |
| P95 abs error (deg) | NaN |
| Peak abs error (deg) | NaN |
| Bias (deg) | NaN |
| Fit slope | NaN |
| Fit intercept (deg) | NaN |
| Pearson r | NaN |
| R2 identity | NaN |

## Segment median, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 42 |
| MAE (deg) | 0.261068 |
| RMSE (deg) | 0.310722 |
| P95 abs error (deg) | 0.677457 |
| Peak abs error (deg) | 0.692334 |
| Bias (deg) | -0.222835 |
| Fit slope | 1.069372 |
| Fit intercept (deg) | -0.899210 |
| Pearson r | 0.645266 |
| R2 identity | -2.310221 |

## Window-level, all theta

| metric | value |
|---|---:|
| n | 546 |
| MAE (deg) | 0.261725 |
| RMSE (deg) | 0.314981 |
| P95 abs error (deg) | 0.658493 |
| Peak abs error (deg) | 0.829075 |
| Bias (deg) | -0.214721 |
| Fit slope | 1.035659 |
| Fit intercept (deg) | -0.562392 |
| Pearson r | 0.608983 |
| R2 identity | -2.401591 |

## Window-level, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 546 |
| MAE (deg) | 0.261725 |
| RMSE (deg) | 0.314981 |
| P95 abs error (deg) | 0.658493 |
| Peak abs error (deg) | 0.829075 |
| Bias (deg) | -0.214721 |
| Fit slope | 1.035659 |
| Fit intercept (deg) | -0.562392 |
| Pearson r | 0.608983 |
| R2 identity | -2.401591 |

## Window-level, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 0 |
| MAE (deg) | NaN |
| RMSE (deg) | NaN |
| P95 abs error (deg) | NaN |
| Peak abs error (deg) | NaN |
| Bias (deg) | NaN |
| Fit slope | NaN |
| Fit intercept (deg) | NaN |
| Pearson r | NaN |
| R2 identity | NaN |

## Window-level, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 546 |
| MAE (deg) | 0.261725 |
| RMSE (deg) | 0.314981 |
| P95 abs error (deg) | 0.658493 |
| Peak abs error (deg) | 0.829075 |
| Bias (deg) | -0.214721 |
| Fit slope | 1.035659 |
| Fit intercept (deg) | -0.562392 |
| Pearson r | 0.608983 |
| R2 identity | -2.401591 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_shortpaths_v1_smoke\modern_tcn_theta_sweep_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_shortpaths_v1_smoke\modern_tcn_theta_sweep_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_shortpaths_v1_smoke\modern_tcn_theta_sweep_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_shortpaths_v1_smoke\modern_tcn_theta_sweep_residual.pdf`
- Segment CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_shortpaths_v1_smoke\modern_tcn_theta_sweep_segment_summary.csv`
- Window CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_shortpaths_v1_smoke\modern_tcn_theta_sweep_window_predictions.csv`
- Result MAT: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_shortpaths_v1_smoke\modern_tcn_theta_sweep_eval_result.mat`

## Path Meta

- Path count: `3`
- Path type: `path_modern_tcn_theta_sweep_plot_v1`
- Total samples: `13440`
- Total stop time: `134.37 s`
