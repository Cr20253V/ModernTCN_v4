# ModernTCN Theta Sweep Plot Report

- Path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_modern_tcn_theta_sweep_multicond_paper_v1.mat`
- Data file: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_paper_v1\ModernTCN_theta_sweep_multicond_paper_v1_data.mat`
- Model seed: `21`
- Sweep: -10.0 to 10.0 deg, step 1.0 deg, segment 3.20 s, v=0.95 m/s
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
| n | 147 |
| MAE (deg) | 0.182957 |
| RMSE (deg) | 0.231739 |
| P95 abs error (deg) | 0.437748 |
| Peak abs error (deg) | 0.818016 |
| Bias (deg) | -0.001205 |
| Fit slope | 0.991014 |
| Fit intercept (deg) | -0.001205 |
| Pearson r | 0.999296 |
| R2 identity | 0.998535 |

## Segment median, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 126 |
| MAE (deg) | 0.173772 |
| RMSE (deg) | 0.225191 |
| P95 abs error (deg) | 0.461558 |
| Peak abs error (deg) | 0.818016 |
| Bias (deg) | -0.040912 |
| Fit slope | 0.990873 |
| Fit intercept (deg) | -0.040912 |
| Pearson r | 0.999458 |
| R2 identity | 0.998811 |

## Segment median, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 119 |
| MAE (deg) | 0.186334 |
| RMSE (deg) | 0.238671 |
| P95 abs error (deg) | 0.448931 |
| Peak abs error (deg) | 0.818016 |
| Bias (deg) | -0.003404 |
| Fit slope | 0.994598 |
| Fit intercept (deg) | -0.003404 |
| Pearson r | 0.998817 |
| R2 identity | 0.997627 |

## Segment median, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 147 |
| MAE (deg) | 0.182957 |
| RMSE (deg) | 0.231739 |
| P95 abs error (deg) | 0.437748 |
| Peak abs error (deg) | 0.818016 |
| Bias (deg) | -0.001205 |
| Fit slope | 0.991014 |
| Fit intercept (deg) | -0.001205 |
| Pearson r | 0.999296 |
| R2 identity | 0.998535 |

## Window-level, all theta

| metric | value |
|---|---:|
| n | 1911 |
| MAE (deg) | 0.184349 |
| RMSE (deg) | 0.234259 |
| P95 abs error (deg) | 0.450765 |
| Peak abs error (deg) | 0.855499 |
| Bias (deg) | -0.000797 |
| Fit slope | 0.990742 |
| Fit intercept (deg) | -0.000797 |
| Pearson r | 0.999282 |
| R2 identity | 0.998503 |

## Window-level, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 1638 |
| MAE (deg) | 0.175969 |
| RMSE (deg) | 0.228573 |
| P95 abs error (deg) | 0.459380 |
| Peak abs error (deg) | 0.855499 |
| Bias (deg) | -0.039554 |
| Fit slope | 0.990600 |
| Fit intercept (deg) | -0.039554 |
| Pearson r | 0.999440 |
| R2 identity | 0.998775 |

## Window-level, |theta| <= 8 deg

| metric | value |
|---|---:|
| n | 1547 |
| MAE (deg) | 0.186009 |
| RMSE (deg) | 0.238709 |
| P95 abs error (deg) | 0.457643 |
| Peak abs error (deg) | 0.855499 |
| Bias (deg) | -0.004182 |
| Fit slope | 0.994436 |
| Fit intercept (deg) | -0.004182 |
| Pearson r | 0.998818 |
| R2 identity | 0.997626 |

## Window-level, |theta| <= 10 deg

| metric | value |
|---|---:|
| n | 1911 |
| MAE (deg) | 0.184349 |
| RMSE (deg) | 0.234259 |
| P95 abs error (deg) | 0.450765 |
| Peak abs error (deg) | 0.855499 |
| Bias (deg) | -0.000797 |
| Fit slope | 0.990742 |
| Fit intercept (deg) | -0.000797 |
| Pearson r | 0.999282 |
| R2 identity | 0.998503 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_paper_v1\modern_tcn_theta_sweep_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_paper_v1\modern_tcn_theta_sweep_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_paper_v1\modern_tcn_theta_sweep_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_paper_v1\modern_tcn_theta_sweep_residual.pdf`
- Segment CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_paper_v1\modern_tcn_theta_sweep_segment_summary.csv`
- Window CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_paper_v1\modern_tcn_theta_sweep_window_predictions.csv`
- Result MAT: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_paper_v1\modern_tcn_theta_sweep_eval_result.mat`

## Path Meta

- Path type: `path_modern_tcn_theta_sweep_plot_v1`
- Samples: `47040`
- Stop time: `470.39 s`
