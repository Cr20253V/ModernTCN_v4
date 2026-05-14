# ModernTCN Theta Scatter Report

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v6_longrun_diag2steer.mat`
- Prediction file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\matlab_full_testset_modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select_scale1p02\modern_tcn_seed42_matlab_full_testset_outputs.mat`
- ONNX file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select_scale1p02\modern_tcn_seed42.onnx`
- Samples: theta-mask test split only, raw network output before closed-loop scheduling protection.
- Plot range: `[-8.0, 8.0] deg`

## Metrics, all test theta

| metric | value |
|---|---:|
| n | 1840 |
| MAE (deg) | 0.250743 |
| RMSE (deg) | 0.539398 |
| P95 abs error (deg) | 0.986479 |
| Peak abs error (deg) | 4.547840 |
| Bias (deg) | -0.019789 |
| Fit slope | 0.982335 |
| Fit intercept (deg) | -0.015099 |
| Pearson r | 0.979892 |
| R2 identity | 0.959624 |

## Metrics, plotted range

| metric | value |
|---|---:|
| n | 1840 |
| MAE (deg) | 0.250743 |
| RMSE (deg) | 0.539398 |
| P95 abs error (deg) | 0.986479 |
| Peak abs error (deg) | 4.547840 |
| Bias (deg) | -0.019789 |
| Fit slope | 0.982335 |
| Fit intercept (deg) | -0.015099 |
| Pearson r | 0.979892 |
| R2 identity | 0.959624 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select_scale1p02\modern_tcn_theta_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select_scale1p02\modern_tcn_theta_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select_scale1p02\modern_tcn_theta_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select_scale1p02\modern_tcn_theta_residual.pdf`
- Metrics CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select_scale1p02\modern_tcn_theta_metrics.csv`
- Binned metrics CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select_scale1p02\modern_tcn_theta_binned_metrics.csv`

## Binned Metrics

| theta bin (deg) | n | MAE (deg) | RMSE (deg) | Bias (deg) |
|---|---:|---:|---:|---:|
| [-10.0, -8.0] | 0 | NaN | NaN | NaN |
| [-8.0, -6.0] | 55 | 0.333127 | 0.392856 | -0.213460 |
| [-6.0, -4.0] | 91 | 0.282338 | 0.362623 | -0.208962 |
| [-4.0, -2.0] | 82 | 1.244057 | 1.859599 | 0.891425 |
| [-2.0, 0.0] | 55 | 0.653791 | 0.849046 | 0.631011 |
| [0.0, 2.0] | 1254 | 0.146417 | 0.282855 | -0.082790 |
| [2.0, 4.0] | 51 | 0.357039 | 0.623800 | -0.150533 |
| [4.0, 6.0] | 184 | 0.288407 | 0.534296 | -0.027034 |
| [6.0, 8.0] | 68 | 0.360270 | 0.528312 | 0.044304 |
| [8.0, 10.0] | 0 | NaN | NaN | NaN |
