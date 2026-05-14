# ModernTCN v1 MATLAB Full Test Set Evaluation

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- Mode: full X_test.
- Metric diff tolerance vs Python summary: 1.0e-04

## Per-Seed MATLAB Metrics

| seed | main | turn | turnT | theta deg | flat | stall | slope | uphill | downhill | seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 21 | 0.9867 | 0.9529 | 0.7624 | 0.4590 | 0.9876 | 0.9721 | 0.9890 | 0.9944 | 0.9840 | 175.6 |

## MATLAB Summary Across Requested Seeds

| metric | mean | std | min | max |
|---|---:|---:|---:|---:|
| acc_main | 0.9867 | 0.0000 | 0.9867 | 0.9867 |
| acc_turn | 0.9529 | 0.0000 | 0.9529 | 0.9529 |
| acc_turn_pure | 0.9819 | 0.0000 | 0.9819 | 0.9819 |
| acc_turn_transition | 0.7624 | 0.0000 | 0.7624 | 0.7624 |
| theta_mae_deg | 0.4590 | 0.0000 | 0.4590 | 0.4590 |
| flat_recall | 0.9876 | 0.0000 | 0.9876 | 0.9876 |
| stall_recall | 0.9721 | 0.0000 | 0.9721 | 0.9721 |
| slope_recall | 0.9890 | 0.0000 | 0.9890 | 0.9890 |
| uphill_recall | 0.9944 | 0.0000 | 0.9944 | 0.9944 |
| downhill_recall | 0.9840 | 0.0000 | 0.9840 | 0.9840 |
| theta_abs_le_8_mae_deg | 0.4590 | 0.0000 | 0.4590 | 0.4590 |
| theta_abs_le_10_mae_deg | 0.4590 | 0.0000 | 0.4590 | 0.4590 |
| theta_pos_6_8_mae_deg | 0.8530 | 0.0000 | 0.8530 | 0.8530 |
| theta_pos_6_8_bias_deg | -0.7050 | 0.0000 | -0.7050 | -0.7050 |
| theta_neg_8_6_mae_deg | 0.5433 | 0.0000 | 0.5433 | 0.5433 |
| theta_neg_8_6_bias_deg | 0.3768 | 0.0000 | 0.3768 | 0.3768 |

## MATLAB vs Python Summary Diff

| seed | metric | MATLAB | Python | abs error | pass |
|---:|---|---:|---:|---:|---:|
| 21 | acc_main | 0.98668726 | 0.98668726 | 0 | 1 |
| 21 | acc_turn | 0.95292733 | 0.95292733 | 0 | 1 |
| 21 | acc_turn_pure | 0.98186902 | 0.98186902 | 0 | 1 |
| 21 | acc_turn_transition | 0.76240937 | 0.76240937 | 0 | 1 |
| 21 | theta_mae_deg | 0.45898498 | 0.45897961 | 5.38e-06 | 1 |
| 21 | flat_recall | 0.98762157 | 0.98762157 | 0 | 1 |
| 21 | stall_recall | 0.97206245 | 0.97206245 | 0 | 1 |
| 21 | slope_recall | 0.98901838 | 0.98901838 | 0 | 1 |
| 21 | uphill_recall | 0.99441860 | 0.99441860 | 0 | 1 |
| 21 | downhill_recall | 0.98399654 | 0.98399654 | 0 | 1 |
| 21 | theta_abs_le_8_mae_deg | 0.45898498 | 0.45897961 | 5.38e-06 | 1 |
| 21 | theta_abs_le_10_mae_deg | 0.45898498 | 0.45897961 | 5.38e-06 | 1 |
| 21 | theta_pos_6_8_mae_deg | 0.85302150 | 0.85297340 | 4.81e-05 | 1 |
| 21 | theta_pos_6_8_bias_deg | -0.70495496 | -0.70478863 | 0.000166 | 0 |
| 21 | theta_neg_8_6_mae_deg | 0.54332369 | 0.54338920 | 6.55e-05 | 1 |
| 21 | theta_neg_8_6_bias_deg | 0.37683686 | 0.37676746 | 6.94e-05 | 1 |

## Decision

MATLAB full test set metrics do not match Python summary. Inspect the diff table before moving to Simulink.
