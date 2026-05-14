# ModernTCN Theta Scatter Report

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- Prediction file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\matlab_full_testset_modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_seed21_matlab_full_testset_outputs.mat`
- ONNX file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_seed21.onnx`
- Samples: theta-mask test split only, raw network output before closed-loop scheduling protection.
- Plot range: `[-8.0, 8.0] deg`

## Metrics, all test theta

| metric | value |
|---|---:|
| n | 4462 |
| MAE (deg) | 0.418461 |
| RMSE (deg) | 0.621289 |
| P95 abs error (deg) | 1.239804 |
| Peak abs error (deg) | 4.796340 |
| Bias (deg) | 0.029275 |
| Fit slope | 0.945007 |
| Fit intercept (deg) | 0.021418 |
| Pearson r | 0.989566 |
| R2 identity | 0.977995 |

## Metrics, plotted range

| metric | value |
|---|---:|
| n | 4462 |
| MAE (deg) | 0.418461 |
| RMSE (deg) | 0.621289 |
| P95 abs error (deg) | 1.239804 |
| Peak abs error (deg) | 4.796340 |
| Bias (deg) | 0.029275 |
| Fit slope | 0.945007 |
| Fit intercept (deg) | 0.021418 |
| Pearson r | 0.989566 |
| R2 identity | 0.977995 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_residual.pdf`
- Metrics CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_metrics.csv`
- Binned metrics CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_theta_binned_metrics.csv`

## Binned Metrics

| theta bin (deg) | n | MAE (deg) | RMSE (deg) | Bias (deg) |
|---|---:|---:|---:|---:|
| [-10.0, -8.0] | 0 | NaN | NaN | NaN |
| [-8.0, -6.0] | 175 | 0.542268 | 0.723366 | 0.500372 |
| [-6.0, -4.0] | 799 | 0.390023 | 0.667382 | 0.182869 |
| [-4.0, -2.0] | 1248 | 0.428008 | 0.660755 | 0.223103 |
| [-2.0, 0.0] | 90 | 0.291634 | 0.448084 | 0.142331 |
| [0.0, 2.0] | 0 | NaN | NaN | NaN |
| [2.0, 4.0] | 1061 | 0.322854 | 0.448722 | -0.035834 |
| [4.0, 6.0] | 778 | 0.387102 | 0.483124 | -0.140495 |
| [6.0, 8.0] | 311 | 0.824862 | 1.009150 | -0.794115 |
| [8.0, 10.0] | 0 | NaN | NaN | NaN |
