# ModernTCN Theta Scatter Report

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v6_longrun_diag2steer.mat`
- Prediction file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\matlab_full_testset_modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select\modern_tcn_seed42_matlab_full_testset_outputs.mat`
- ONNX file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select\modern_tcn_seed42.onnx`
- Samples: theta-mask test split only, raw network output before closed-loop scheduling protection.
- Plot range: `[-8.0, 8.0] deg`

## Metrics, all test theta

| metric | value |
|---|---:|
| n | 1840 |
| MAE (deg) | 0.243995 |
| RMSE (deg) | 0.536233 |
| P95 abs error (deg) | 1.005783 |
| Peak abs error (deg) | 4.537102 |
| Bias (deg) | -0.024605 |
| Fit slope | 0.963073 |
| Fit intercept (deg) | -0.014803 |
| Pearson r | 0.979892 |
| R2 identity | 0.960096 |

## Metrics, plotted range

| metric | value |
|---|---:|
| n | 1840 |
| MAE (deg) | 0.243995 |
| RMSE (deg) | 0.536233 |
| P95 abs error (deg) | 1.005783 |
| Peak abs error (deg) | 4.537102 |
| Bias (deg) | -0.024605 |
| Fit slope | 0.963073 |
| Fit intercept (deg) | -0.014803 |
| Pearson r | 0.979892 |
| R2 identity | 0.960096 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select\modern_tcn_theta_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select\modern_tcn_theta_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select\modern_tcn_theta_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select\modern_tcn_theta_residual.pdf`
- Metrics CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select\modern_tcn_theta_metrics.csv`
- Binned metrics CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select\modern_tcn_theta_binned_metrics.csv`

## Binned Metrics

| theta bin (deg) | n | MAE (deg) | RMSE (deg) | Bias (deg) |
|---|---:|---:|---:|---:|
| [-10.0, -8.0] | 0 | NaN | NaN | NaN |
| [-8.0, -6.0] | 55 | 0.276819 | 0.338245 | -0.089140 |
| [-6.0, -4.0] | 91 | 0.213032 | 0.313461 | -0.114476 |
| [-4.0, -2.0] | 82 | 1.224214 | 1.860416 | 0.939330 |
| [-2.0, 0.0] | 55 | 0.657055 | 0.852273 | 0.634988 |
| [0.0, 2.0] | 1254 | 0.144310 | 0.280422 | -0.081935 |
| [2.0, 4.0] | 51 | 0.365735 | 0.626603 | -0.204979 |
| [4.0, 6.0] | 184 | 0.300199 | 0.534674 | -0.118011 |
| [6.0, 8.0] | 68 | 0.337696 | 0.526516 | -0.102776 |
| [8.0, 10.0] | 0 | NaN | NaN | NaN |
