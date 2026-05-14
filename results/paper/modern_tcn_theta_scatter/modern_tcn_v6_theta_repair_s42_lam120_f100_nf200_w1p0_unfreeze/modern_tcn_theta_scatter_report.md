# ModernTCN Theta Scatter Report

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v6_longrun_diag2steer.mat`
- Prediction file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\matlab_full_testset_modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_seed42_matlab_full_testset_outputs.mat`
- ONNX file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_seed42.onnx`
- Samples: theta-mask test split only, raw network output before closed-loop scheduling protection.
- Plot range: `[-8.0, 8.0] deg`

## Metrics, all test theta

| metric | value |
|---|---:|
| n | 1840 |
| MAE (deg) | 0.490640 |
| RMSE (deg) | 1.053451 |
| P95 abs error (deg) | 2.088007 |
| Peak abs error (deg) | 9.264134 |
| Bias (deg) | -0.063489 |
| Fit slope | 0.978286 |
| Fit intercept (deg) | -0.057724 |
| Pearson r | 0.928541 |
| R2 identity | 0.845995 |

## Metrics, plotted range

| metric | value |
|---|---:|
| n | 1840 |
| MAE (deg) | 0.490640 |
| RMSE (deg) | 1.053451 |
| P95 abs error (deg) | 2.088007 |
| Peak abs error (deg) | 9.264134 |
| Bias (deg) | -0.063489 |
| Fit slope | 0.978286 |
| Fit intercept (deg) | -0.057724 |
| Pearson r | 0.928541 |
| R2 identity | 0.845995 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_theta_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_theta_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_theta_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_theta_residual.pdf`
- Metrics CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_theta_metrics.csv`
- Binned metrics CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_theta_binned_metrics.csv`

## Binned Metrics

| theta bin (deg) | n | MAE (deg) | RMSE (deg) | Bias (deg) |
|---|---:|---:|---:|---:|
| [-10.0, -8.0] | 0 | NaN | NaN | NaN |
| [-8.0, -6.0] | 55 | 0.388240 | 0.465384 | 0.257800 |
| [-6.0, -4.0] | 91 | 0.346645 | 0.533761 | -0.143651 |
| [-4.0, -2.0] | 82 | 1.305030 | 1.903653 | 0.146185 |
| [-2.0, 0.0] | 55 | 0.758434 | 1.200259 | 0.553780 |
| [0.0, 2.0] | 1254 | 0.458771 | 1.094444 | -0.097911 |
| [2.0, 4.0] | 51 | 0.401868 | 0.699419 | -0.270035 |
| [4.0, 6.0] | 184 | 0.376447 | 0.544132 | -0.061944 |
| [6.0, 8.0] | 68 | 0.530783 | 0.824683 | -0.182655 |
| [8.0, 10.0] | 0 | NaN | NaN | NaN |
