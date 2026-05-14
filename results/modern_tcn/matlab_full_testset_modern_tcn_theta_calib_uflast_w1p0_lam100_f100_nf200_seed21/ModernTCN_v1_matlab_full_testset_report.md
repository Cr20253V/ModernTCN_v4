# ModernTCN v1 MATLAB Full Test Set Evaluation

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- Mode: full X_test.
- Metric diff tolerance vs Python summary: 3.0e-04

## Per-Seed MATLAB Metrics

| seed | main | turn | turnT | theta deg | flat | stall | slope | uphill | downhill | seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 21 | 0.9870 | 0.9523 | 0.7624 | 0.4185 | 0.9900 | 0.9622 | 0.9883 | 0.9944 | 0.9827 | 344.3 |

## MATLAB Summary Across Requested Seeds

| metric | mean | std | min | max |
|---|---:|---:|---:|---:|
| acc_main | 0.9870 | 0.0000 | 0.9870 | 0.9870 |
| acc_turn | 0.9523 | 0.0000 | 0.9523 | 0.9523 |
| acc_turn_pure | 0.9811 | 0.0000 | 0.9811 | 0.9811 |
| acc_turn_transition | 0.7624 | 0.0000 | 0.7624 | 0.7624 |
| theta_mae_deg | 0.4185 | 0.0000 | 0.4185 | 0.4185 |
| flat_recall | 0.9900 | 0.0000 | 0.9900 | 0.9900 |
| stall_recall | 0.9622 | 0.0000 | 0.9622 | 0.9622 |
| slope_recall | 0.9883 | 0.0000 | 0.9883 | 0.9883 |
| uphill_recall | 0.9944 | 0.0000 | 0.9944 | 0.9944 |
| downhill_recall | 0.9827 | 0.0000 | 0.9827 | 0.9827 |
| theta_abs_le_8_mae_deg | 0.4185 | 0.0000 | 0.4185 | 0.4185 |
| theta_abs_le_10_mae_deg | 0.4185 | 0.0000 | 0.4185 | 0.4185 |
| theta_pos_6_8_mae_deg | 0.8249 | 0.0000 | 0.8249 | 0.8249 |
| theta_pos_6_8_bias_deg | -0.7941 | 0.0000 | -0.7941 | -0.7941 |
| theta_neg_8_6_mae_deg | 0.5423 | 0.0000 | 0.5423 | 0.5423 |
| theta_neg_8_6_bias_deg | 0.5004 | 0.0000 | 0.5004 | 0.5004 |

## MATLAB vs Python Summary Diff

| seed | metric | MATLAB | Python | abs error | pass |
|---:|---|---:|---:|---:|---:|
| 21 | acc_main | 0.98698147 | 0.98698147 | 0 | 1 |
| 21 | acc_turn | 0.95226537 | 0.95226537 | 0 | 1 |
| 21 | acc_turn_pure | 0.98110650 | 0.98110650 | 0 | 1 |
| 21 | acc_turn_transition | 0.76240937 | 0.76240937 | 0 | 1 |
| 21 | theta_mae_deg | 0.41846070 | 0.41843596 | 2.47e-05 | 1 |
| 21 | flat_recall | 0.99002147 | 0.99002147 | 0 | 1 |
| 21 | stall_recall | 0.96220214 | 0.96220214 | 0 | 1 |
| 21 | slope_recall | 0.98834603 | 0.98834603 | 0 | 1 |
| 21 | uphill_recall | 0.99441860 | 0.99441860 | 0 | 1 |
| 21 | downhill_recall | 0.98269896 | 0.98269896 | 0 | 1 |
| 21 | theta_abs_le_8_mae_deg | 0.41846070 | 0.41843596 | 2.47e-05 | 1 |
| 21 | theta_abs_le_10_mae_deg | 0.41846070 | 0.41843596 | 2.47e-05 | 1 |
| 21 | theta_pos_6_8_mae_deg | 0.82486206 | 0.82473511 | 0.000127 | 1 |
| 21 | theta_pos_6_8_bias_deg | -0.79411505 | -0.79393578 | 0.000179 | 1 |
| 21 | theta_neg_8_6_mae_deg | 0.54226838 | 0.54241973 | 0.000151 | 1 |
| 21 | theta_neg_8_6_bias_deg | 0.50037152 | 0.50058848 | 0.000217 | 1 |

## Decision

MATLAB full test set metrics match Python summary within tolerance. The offline MATLAB inference path is ready for MATLAB wrapper design.
