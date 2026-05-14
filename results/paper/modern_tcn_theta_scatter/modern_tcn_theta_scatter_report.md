# ModernTCN Theta Scatter Report

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- Prediction file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\matlab_full_testset_modern_tcn_v4_turn_focus_A_theta_head_B_seed21\modern_tcn_seed21_matlab_full_testset_outputs.mat`
- ONNX file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v4_turn_focus_A_theta_head_B_seed21\modern_tcn_seed21.onnx`
- Samples: theta-mask test split only, raw network output before closed-loop scheduling protection.

## Metrics

| metric | value |
|---|---:|
| n | 4462 |
| MAE (deg) | 0.486846 |
| RMSE (deg) | 0.711324 |
| P95 abs error (deg) | 1.404569 |
| Peak abs error (deg) | 4.547475 |
| Bias (deg) | -0.064947 |
| Fit slope | 0.915576 |
| Fit intercept (deg) | -0.077008 |
| Pearson r | 0.987431 |
| R2 identity | 0.971155 |
| Truth range (deg) | [-8.000, 7.000] |
| Prediction range (deg) | [-7.984, 7.323] |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_residual.pdf`
- Metrics CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_metrics.csv`
- Binned metrics CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_binned_metrics.csv`

## Binned Metrics

| theta bin (deg) | n | MAE (deg) | RMSE (deg) | Bias (deg) |
|---|---:|---:|---:|---:|
| [-10.0, -8.0] | 0 | NaN | NaN | NaN |
| [-8.0, -6.0] | 175 | 0.653454 | 0.841580 | 0.616412 |
| [-6.0, -4.0] | 799 | 0.430481 | 0.722480 | 0.193519 |
| [-4.0, -2.0] | 1248 | 0.429339 | 0.673090 | 0.224548 |
| [-2.0, 0.0] | 90 | 0.402866 | 0.497833 | -0.002668 |
| [0.0, 2.0] | 0 | NaN | NaN | NaN |
| [2.0, 4.0] | 1061 | 0.345864 | 0.459033 | -0.135603 |
| [4.0, 6.0] | 778 | 0.520125 | 0.641813 | -0.408874 |
| [6.0, 8.0] | 311 | 1.190692 | 1.371427 | -1.190692 |
| [8.0, 10.0] | 0 | NaN | NaN | NaN |
