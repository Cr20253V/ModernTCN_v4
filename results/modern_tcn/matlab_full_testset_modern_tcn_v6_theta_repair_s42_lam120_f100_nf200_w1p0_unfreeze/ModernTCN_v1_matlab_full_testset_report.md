# ModernTCN v1 MATLAB Full Test Set Evaluation

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v6_longrun_diag2steer.mat`
- Mode: full X_test.
- Metric diff tolerance vs Python summary: 5.0e-04

## Per-Seed MATLAB Metrics

| seed | main | turn | turnT | theta deg | flat | stall | slope | uphill | downhill | seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 42 | 0.9783 | 0.9408 | 0.6989 | 0.4906 | 0.9939 | 0.9038 | 0.9473 | 0.8264 | 0.7208 | 37.9 |

## MATLAB Summary Across Requested Seeds

| metric | mean | std | min | max |
|---|---:|---:|---:|---:|
| acc_main | 0.9783 | 0.0000 | 0.9783 | 0.9783 |
| acc_turn | 0.9408 | 0.0000 | 0.9408 | 0.9408 |
| acc_turn_pure | 0.9533 | 0.0000 | 0.9533 | 0.9533 |
| acc_turn_transition | 0.6989 | 0.0000 | 0.6989 | 0.6989 |
| theta_mae_deg | 0.4906 | 0.0000 | 0.4906 | 0.4906 |
| flat_recall | 0.9939 | 0.0000 | 0.9939 | 0.9939 |
| stall_recall | 0.9038 | 0.0000 | 0.9038 | 0.9038 |
| slope_recall | 0.9473 | 0.0000 | 0.9473 | 0.9473 |
| uphill_recall | 0.8264 | 0.0000 | 0.8264 | 0.8264 |
| downhill_recall | 0.7208 | 0.0000 | 0.7208 | 0.7208 |
| theta_abs_le_8_mae_deg | 0.4906 | 0.0000 | 0.4906 | 0.4906 |
| theta_abs_le_10_mae_deg | 0.4906 | 0.0000 | 0.4906 | 0.4906 |
| theta_pos_6_8_mae_deg | 0.5308 | 0.0000 | 0.5308 | 0.5308 |
| theta_pos_6_8_bias_deg | -0.1827 | 0.0000 | -0.1827 | -0.1827 |
| theta_neg_8_6_mae_deg | 0.3882 | 0.0000 | 0.3882 | 0.3882 |
| theta_neg_8_6_bias_deg | 0.2578 | 0.0000 | 0.2578 | 0.2578 |

## MATLAB vs Python Summary Diff

| seed | metric | MATLAB | Python | abs error | pass |
|---:|---|---:|---:|---:|---:|
| 42 | acc_main | 0.97832981 | 0.97832981 | 0 | 1 |
| 42 | acc_turn | 0.94080338 | 0.94080338 | 0 | 1 |
| 42 | acc_turn_pure | 0.95330739 | 0.95330739 | 0 | 1 |
| 42 | acc_turn_transition | 0.69892473 | 0.69892473 | 0 | 1 |
| 42 | theta_mae_deg | 0.49064011 | 0.49064422 | 4.11e-06 | 1 |
| 42 | flat_recall | 0.99388846 | 0.99388846 | 0 | 1 |
| 42 | stall_recall | 0.90384615 | 0.90384615 | 0 | 1 |
| 42 | slope_recall | 0.94726930 | 0.94726930 | 0 | 1 |
| 42 | uphill_recall | 0.82644628 | 0.82644628 | 0 | 1 |
| 42 | downhill_recall | 0.72084806 | 0.72084806 | 0 | 1 |
| 42 | theta_abs_le_8_mae_deg | 0.49064011 | 0.49064425 | 4.14e-06 | 1 |
| 42 | theta_abs_le_10_mae_deg | 0.49064011 | 0.49064425 | 4.14e-06 | 1 |
| 42 | theta_pos_6_8_mae_deg | 0.53078298 | 0.53098679 | 0.000204 | 1 |
| 42 | theta_pos_6_8_bias_deg | -0.18265508 | -0.18251365 | 0.000141 | 1 |
| 42 | theta_neg_8_6_mae_deg | 0.38823996 | 0.38798389 | 0.000256 | 1 |
| 42 | theta_neg_8_6_bias_deg | 0.25779991 | 0.25775376 | 4.62e-05 | 1 |

## Decision

MATLAB full test set metrics match Python summary within tolerance. The offline MATLAB inference path is ready for MATLAB wrapper design.
