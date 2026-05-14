# ModernTCN Theta Sweep Plot Report

- Path files: `101`
- First path file: `E:\Matlab\Simulink\S-Function_16\data\paths\modern_tcn_theta_sweep_multicond_shortpaths_v1_theta0p1\path_modern_tcn_theta_sweep_multicond_shortpaths_v1_theta0p1_001_m10p0_m09p9.mat`
- Last path file: `E:\Matlab\Simulink\S-Function_16\data\paths\modern_tcn_theta_sweep_multicond_shortpaths_v1_theta0p1\path_modern_tcn_theta_sweep_multicond_shortpaths_v1_theta0p1_101_p10p0_p10p0.mat`
- Data file: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_shortpaths_v1_theta0p1\ModernTCN_theta_sweep_full_shortpaths_v1_data.mat`
- Model seed: `21`
- Sweep: -10.0 to 10.0 deg, step 0.1 deg, segment 3.20 s, v=0.95 m/s
- Scatter metric source: `window`; show segment median: `0`
- Path repeats: `7`; explicit variants: `7`
- Evaluation windows: tail 0.70 s, stride 0.100 s, margin 0.10 s
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
| n | 1407 |
| MAE (deg) | 0.138687 |
| RMSE (deg) | 0.202392 |
| P95 abs error (deg) | 0.404840 |
| Peak abs error (deg) | 0.891443 |
| Bias (deg) | -0.023727 |
| Fit slope | 0.984626 |
| Fit intercept (deg) | -0.023727 |
| Pearson r | 0.999503 |
| R2 identity | 0.998783 |

## Segment median, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 1134 |
| MAE (deg) | 0.148414 |
| RMSE (deg) | 0.216217 |
| P95 abs error (deg) | 0.417504 |
| Peak abs error (deg) | 0.891443 |
| Bias (deg) | -0.035355 |
| Fit slope | 0.984631 |
| Fit intercept (deg) | -0.035355 |
| Pearson r | 0.999556 |
| R2 identity | 0.998873 |

## Segment median, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 1127 |
| MAE (deg) | 0.124122 |
| RMSE (deg) | 0.187018 |
| P95 abs error (deg) | 0.343278 |
| Peak abs error (deg) | 0.891443 |
| Bias (deg) | -0.008415 |
| Fit slope | 0.984452 |
| Fit intercept (deg) | -0.008415 |
| Pearson r | 0.999292 |
| R2 identity | 0.998381 |

## Segment median, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 1407 |
| MAE (deg) | 0.138687 |
| RMSE (deg) | 0.202392 |
| P95 abs error (deg) | 0.404840 |
| Peak abs error (deg) | 0.891443 |
| Bias (deg) | -0.023727 |
| Fit slope | 0.984626 |
| Fit intercept (deg) | -0.023727 |
| Pearson r | 0.999503 |
| R2 identity | 0.998783 |

## Window-level, all theta

| metric | value |
|---|---:|
| n | 11256 |
| MAE (deg) | 0.142796 |
| RMSE (deg) | 0.207324 |
| P95 abs error (deg) | 0.410543 |
| Peak abs error (deg) | 0.915568 |
| Bias (deg) | -0.023677 |
| Fit slope | 0.984671 |
| Fit intercept (deg) | -0.023677 |
| Pearson r | 0.999472 |
| R2 identity | 0.998723 |

## Window-level, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 9072 |
| MAE (deg) | 0.152080 |
| RMSE (deg) | 0.220588 |
| P95 abs error (deg) | 0.436815 |
| Peak abs error (deg) | 0.915568 |
| Bias (deg) | -0.034670 |
| Fit slope | 0.984665 |
| Fit intercept (deg) | -0.034670 |
| Pearson r | 0.999531 |
| R2 identity | 0.998827 |

## Window-level, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 9016 |
| MAE (deg) | 0.128958 |
| RMSE (deg) | 0.192762 |
| P95 abs error (deg) | 0.375727 |
| Peak abs error (deg) | 0.915568 |
| Bias (deg) | -0.008675 |
| Fit slope | 0.984727 |
| Fit intercept (deg) | -0.008675 |
| Pearson r | 0.999236 |
| R2 identity | 0.998280 |

## Window-level, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 11256 |
| MAE (deg) | 0.142796 |
| RMSE (deg) | 0.207324 |
| P95 abs error (deg) | 0.410543 |
| Peak abs error (deg) | 0.915568 |
| Bias (deg) | -0.023677 |
| Fit slope | 0.984671 |
| Fit intercept (deg) | -0.023677 |
| Pearson r | 0.999472 |
| R2 identity | 0.998723 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_shortpaths_v1_theta0p1\modern_tcn_theta_sweep_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_shortpaths_v1_theta0p1\modern_tcn_theta_sweep_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_shortpaths_v1_theta0p1\modern_tcn_theta_sweep_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_shortpaths_v1_theta0p1\modern_tcn_theta_sweep_residual.pdf`
- Segment CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_shortpaths_v1_theta0p1\modern_tcn_theta_sweep_segment_summary.csv`
- Window CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_shortpaths_v1_theta0p1\modern_tcn_theta_sweep_window_predictions.csv`
- Result MAT: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_shortpaths_v1_theta0p1\modern_tcn_theta_sweep_eval_result.mat`

## Path Meta

- Path count: `101`
- Path type: `path_modern_tcn_theta_sweep_plot_v1`
- Total samples: `450240`
- Total stop time: `4501.39 s`
