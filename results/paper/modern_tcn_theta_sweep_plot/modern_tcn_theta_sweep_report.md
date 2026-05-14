# ModernTCN Theta Sweep Plot Report

- Path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_modern_tcn_theta_sweep_plot_v1.mat`
- Data file: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\ModernTCN_theta_sweep_plot_data.mat`
- Model seed: `21`
- Sweep: -10.0 to 10.0 deg, step 0.1 deg, segment 5.00 s, v=0.90 m/s
- Note: held-out paper plotting set; not added to training data.

## Segment median, all theta

| metric | value |
|---|---:|
| n | 201 |
| MAE (deg) | 0.772138 |
| RMSE (deg) | 1.064655 |
| P95 abs error (deg) | 2.593141 |
| Peak abs error (deg) | 3.094353 |
| Bias (deg) | -0.475475 |
| Fit slope | 0.854273 |
| Fit intercept (deg) | -0.475475 |
| Pearson r | 0.996106 |
| R2 identity | 0.966332 |

## Segment median, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 162 |
| MAE (deg) | 0.842223 |
| RMSE (deg) | 1.154566 |
| P95 abs error (deg) | 2.738621 |
| Peak abs error (deg) | 3.094353 |
| Bias (deg) | -0.568567 |
| Fit slope | 0.855968 |
| Fit intercept (deg) | -0.568567 |
| Pearson r | 0.997548 |
| R2 identity | 0.967853 |

## Window-level, all theta

| metric | value |
|---|---:|
| n | 2211 |
| MAE (deg) | 0.771928 |
| RMSE (deg) | 1.064494 |
| P95 abs error (deg) | 2.562209 |
| Peak abs error (deg) | 3.098840 |
| Bias (deg) | -0.475418 |
| Fit slope | 0.854324 |
| Fit intercept (deg) | -0.475418 |
| Pearson r | 0.996103 |
| R2 identity | 0.966342 |

## Window-level, |theta| >= 2 deg

| metric | value |
|---|---:|
| n | 1782 |
| MAE (deg) | 0.842005 |
| RMSE (deg) | 1.154404 |
| P95 abs error (deg) | 2.712932 |
| Peak abs error (deg) | 3.098840 |
| Bias (deg) | -0.568506 |
| Fit slope | 0.856018 |
| Fit intercept (deg) | -0.568506 |
| Pearson r | 0.997544 |
| R2 identity | 0.967862 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_sweep_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_sweep_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_sweep_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_sweep_residual.pdf`
- Segment CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_sweep_segment_summary.csv`
- Window CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_sweep_window_predictions.csv`
- Result MAT: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta_sweep_eval_result.mat`

## Path Meta

- Path type: `path_modern_tcn_theta_sweep_plot_v1`
- Samples: `100501`
- Stop time: `1005.00 s`
