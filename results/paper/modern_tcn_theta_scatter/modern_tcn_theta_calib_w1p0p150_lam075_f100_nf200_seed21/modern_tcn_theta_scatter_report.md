# ModernTCN Theta Scatter Report

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- Prediction file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\matlab_full_testset_modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_seed21_matlab_full_testset_outputs.mat`
- ONNX file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_seed21.onnx`
- Samples: theta-mask test split only, raw network output before closed-loop scheduling protection.
- Plot range: `[-8.0, 8.0] deg`

## Metrics, all test theta

| metric | value |
|---|---:|
| n | 4462 |
| MAE (deg) | 0.541477 |
| RMSE (deg) | 0.768937 |
| P95 abs error (deg) | 1.670970 |
| Peak abs error (deg) | 4.821650 |
| Bias (deg) | 0.274820 |
| Fit slope | 0.919251 |
| Fit intercept (deg) | 0.263284 |
| Pearson r | 0.986730 |
| R2 identity | 0.966293 |

## Metrics, plotted range

| metric | value |
|---|---:|
| n | 4462 |
| MAE (deg) | 0.541477 |
| RMSE (deg) | 0.768937 |
| P95 abs error (deg) | 1.670970 |
| Peak abs error (deg) | 4.821650 |
| Bias (deg) | 0.274820 |
| Fit slope | 0.919251 |
| Fit intercept (deg) | 0.263284 |
| Pearson r | 0.986730 |
| R2 identity | 0.966293 |

## Outputs

- Scatter PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_theta_scatter.png`
- Scatter PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_theta_scatter.pdf`
- Residual PNG: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_theta_residual.png`
- Residual PDF: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_theta_residual.pdf`
- Metrics CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_theta_metrics.csv`
- Binned metrics CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_scatter\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_theta_binned_metrics.csv`

## Binned Metrics

| theta bin (deg) | n | MAE (deg) | RMSE (deg) | Bias (deg) |
|---|---:|---:|---:|---:|
| [-10.0, -8.0] | 0 | NaN | NaN | NaN |
| [-8.0, -6.0] | 175 | 0.856706 | 1.203006 | 0.839715 |
| [-6.0, -4.0] | 799 | 0.600467 | 0.879256 | 0.491728 |
| [-4.0, -2.0] | 1248 | 0.710729 | 0.934785 | 0.620830 |
| [-2.0, 0.0] | 90 | 0.426053 | 0.641373 | 0.388767 |
| [0.0, 2.0] | 0 | NaN | NaN | NaN |
| [2.0, 4.0] | 1061 | 0.330198 | 0.424980 | 0.082074 |
| [4.0, 6.0] | 778 | 0.384693 | 0.508373 | -0.019964 |
| [6.0, 8.0] | 311 | 0.679767 | 0.891207 | -0.626767 |
| [8.0, 10.0] | 0 | NaN | NaN | NaN |
