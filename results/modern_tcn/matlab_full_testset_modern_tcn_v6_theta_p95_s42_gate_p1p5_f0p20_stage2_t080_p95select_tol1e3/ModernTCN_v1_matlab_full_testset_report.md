# ModernTCN v1 MATLAB Full Test Set Evaluation

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v6_longrun_diag2steer.mat`
- Mode: full X_test.
- Metric diff tolerance vs Python summary: 1.0e-03

## Per-Seed MATLAB Metrics

| seed | main | turn | turnT | theta deg | flat | stall | slope | uphill | downhill | seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 42 | 0.9773 | 0.9387 | 0.6667 | 0.2440 | 0.9947 | 0.9038 | 0.9416 | 0.8264 | 0.7067 | 36.7 |

## MATLAB Summary Across Requested Seeds

| metric | mean | std | min | max |
|---|---:|---:|---:|---:|
| acc_main | 0.9773 | 0.0000 | 0.9773 | 0.9773 |
| acc_turn | 0.9387 | 0.0000 | 0.9387 | 0.9387 |
| acc_turn_pure | 0.9528 | 0.0000 | 0.9528 | 0.9528 |
| acc_turn_transition | 0.6667 | 0.0000 | 0.6667 | 0.6667 |
| theta_mae_deg | 0.2440 | 0.0000 | 0.2440 | 0.2440 |
| flat_recall | 0.9947 | 0.0000 | 0.9947 | 0.9947 |
| stall_recall | 0.9038 | 0.0000 | 0.9038 | 0.9038 |
| slope_recall | 0.9416 | 0.0000 | 0.9416 | 0.9416 |
| uphill_recall | 0.8264 | 0.0000 | 0.8264 | 0.8264 |
| downhill_recall | 0.7067 | 0.0000 | 0.7067 | 0.7067 |
| theta_abs_le_8_mae_deg | 0.2440 | 0.0000 | 0.2440 | 0.2440 |
| theta_abs_le_10_mae_deg | 0.2440 | 0.0000 | 0.2440 | 0.2440 |
| theta_pos_6_8_mae_deg | 0.3377 | 0.0000 | 0.3377 | 0.3377 |
| theta_pos_6_8_bias_deg | -0.1028 | 0.0000 | -0.1028 | -0.1028 |
| theta_neg_8_6_mae_deg | 0.2768 | 0.0000 | 0.2768 | 0.2768 |
| theta_neg_8_6_bias_deg | -0.0891 | 0.0000 | -0.0891 | -0.0891 |

## MATLAB vs Python Summary Diff

| seed | metric | MATLAB | Python | abs error | pass |
|---:|---|---:|---:|---:|---:|
| 42 | acc_main | 0.97727273 | 0.97727273 | 0 | 1 |
| 42 | acc_turn | 0.93868922 | 0.93868922 | 0 | 1 |
| 42 | acc_turn_pure | 0.95275153 | 0.95275153 | 0 | 1 |
| 42 | acc_turn_transition | 0.66666667 | 0.66666667 | 0 | 1 |
| 42 | theta_mae_deg | 0.24399530 | 0.24395493 | 4.04e-05 | 1 |
| 42 | flat_recall | 0.99465241 | 0.99465241 | 0 | 1 |
| 42 | stall_recall | 0.90384615 | 0.90384615 | 0 | 1 |
| 42 | slope_recall | 0.94161959 | 0.94161959 | 0 | 1 |
| 42 | uphill_recall | 0.82644628 | 0.82644628 | 0 | 1 |
| 42 | downhill_recall | 0.70671378 | 0.70671378 | 0 | 1 |
| 42 | theta_abs_le_8_mae_deg | 0.24399530 | 0.24395493 | 4.04e-05 | 1 |
| 42 | theta_abs_le_10_mae_deg | 0.24399530 | 0.24395493 | 4.04e-05 | 1 |
| 42 | theta_pos_6_8_mae_deg | 0.33769587 | 0.33759052 | 0.000105 | 1 |
| 42 | theta_pos_6_8_bias_deg | -0.10277587 | -0.10300011 | 0.000224 | 1 |
| 42 | theta_neg_8_6_mae_deg | 0.27681933 | 0.27679121 | 2.81e-05 | 1 |
| 42 | theta_neg_8_6_bias_deg | -0.08914039 | -0.08910891 | 3.15e-05 | 1 |

## Decision

MATLAB full test set metrics match Python summary within tolerance. The offline MATLAB inference path is ready for MATLAB wrapper design.
