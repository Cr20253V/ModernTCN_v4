# ModernTCN v1 MATLAB Full Test Set Evaluation

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v6_longrun_diag2steer.mat`
- Mode: full X_test.
- Metric diff tolerance vs Python summary: 1.0e-03

## Per-Seed MATLAB Metrics

| seed | main | turn | turnT | theta deg | flat | stall | slope | uphill | downhill | seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 42 | 0.9773 | 0.9387 | 0.6667 | 0.2507 | 0.9947 | 0.9038 | 0.9416 | 0.8264 | 0.7067 | 37.8 |

## MATLAB Summary Across Requested Seeds

| metric | mean | std | min | max |
|---|---:|---:|---:|---:|
| acc_main | 0.9773 | 0.0000 | 0.9773 | 0.9773 |
| acc_turn | 0.9387 | 0.0000 | 0.9387 | 0.9387 |
| acc_turn_pure | 0.9528 | 0.0000 | 0.9528 | 0.9528 |
| acc_turn_transition | 0.6667 | 0.0000 | 0.6667 | 0.6667 |
| theta_mae_deg | 0.2507 | 0.0000 | 0.2507 | 0.2507 |
| flat_recall | 0.9947 | 0.0000 | 0.9947 | 0.9947 |
| stall_recall | 0.9038 | 0.0000 | 0.9038 | 0.9038 |
| slope_recall | 0.9416 | 0.0000 | 0.9416 | 0.9416 |
| uphill_recall | 0.8264 | 0.0000 | 0.8264 | 0.8264 |
| downhill_recall | 0.7067 | 0.0000 | 0.7067 | 0.7067 |
| theta_abs_le_8_mae_deg | 0.2507 | 0.0000 | 0.2507 | 0.2507 |
| theta_abs_le_10_mae_deg | 0.2507 | 0.0000 | 0.2507 | 0.2507 |
| theta_pos_6_8_mae_deg | 0.3603 | 0.0000 | 0.3603 | 0.3603 |
| theta_pos_6_8_bias_deg | 0.0443 | 0.0000 | 0.0443 | 0.0443 |
| theta_neg_8_6_mae_deg | 0.3331 | 0.0000 | 0.3331 | 0.3331 |
| theta_neg_8_6_bias_deg | -0.2135 | 0.0000 | -0.2135 | -0.2135 |

## MATLAB vs Python Summary Diff

| seed | metric | MATLAB | Python | abs error | pass |
|---:|---|---:|---:|---:|---:|
| 42 | acc_main | 0.97727273 | 0.97727273 | 0 | 1 |
| 42 | acc_turn | 0.93868922 | 0.93868922 | 0 | 1 |
| 42 | acc_turn_pure | 0.95275153 | 0.95275153 | 0 | 1 |
| 42 | acc_turn_transition | 0.66666667 | 0.66666667 | 0 | 1 |
| 42 | theta_mae_deg | 0.25074319 | 0.25070226 | 4.09e-05 | 1 |
| 42 | flat_recall | 0.99465241 | 0.99465241 | 0 | 1 |
| 42 | stall_recall | 0.90384615 | 0.90384615 | 0 | 1 |
| 42 | slope_recall | 0.94161959 | 0.94161959 | 0 | 1 |
| 42 | uphill_recall | 0.82644628 | 0.82644628 | 0 | 1 |
| 42 | downhill_recall | 0.70671378 | 0.70671378 | 0 | 1 |
| 42 | theta_abs_le_8_mae_deg | 0.25074319 | 0.25070223 | 4.1e-05 | 1 |
| 42 | theta_abs_le_10_mae_deg | 0.25074319 | 0.25070223 | 4.1e-05 | 1 |
| 42 | theta_pos_6_8_mae_deg | 0.36027028 | 0.36010602 | 0.000164 | 1 |
| 42 | theta_pos_6_8_bias_deg | 0.04430359 | 0.04407486 | 0.000229 | 1 |
| 42 | theta_neg_8_6_mae_deg | 0.33312673 | 0.33307749 | 4.92e-05 | 1 |
| 42 | theta_neg_8_6_bias_deg | -0.21345990 | -0.21342769 | 3.22e-05 | 1 |

## Decision

MATLAB full test set metrics match Python summary within tolerance. The offline MATLAB inference path is ready for MATLAB wrapper design.
