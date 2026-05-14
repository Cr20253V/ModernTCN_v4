# ModernTCN v1 MATLAB Full Test Set Evaluation

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- Mode: full X_test.
- Metric diff tolerance vs Python summary: 1.0e-04

## Per-Seed MATLAB Metrics

| seed | main | turn | turnT | theta deg | flat | stall | slope | uphill | downhill | seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 21 | 0.9867 | 0.9529 | 0.7624 | 0.4679 | 0.9876 | 0.9721 | 0.9890 | 0.9944 | 0.9840 | 159.6 |

## MATLAB Summary Across Requested Seeds

| metric | mean | std | min | max |
|---|---:|---:|---:|---:|
| acc_main | 0.9867 | 0.0000 | 0.9867 | 0.9867 |
| acc_turn | 0.9529 | 0.0000 | 0.9529 | 0.9529 |
| acc_turn_pure | 0.9819 | 0.0000 | 0.9819 | 0.9819 |
| acc_turn_transition | 0.7624 | 0.0000 | 0.7624 | 0.7624 |
| theta_mae_deg | 0.4679 | 0.0000 | 0.4679 | 0.4679 |
| flat_recall | 0.9876 | 0.0000 | 0.9876 | 0.9876 |
| stall_recall | 0.9721 | 0.0000 | 0.9721 | 0.9721 |
| slope_recall | 0.9890 | 0.0000 | 0.9890 | 0.9890 |
| uphill_recall | 0.9944 | 0.0000 | 0.9944 | 0.9944 |
| downhill_recall | 0.9840 | 0.0000 | 0.9840 | 0.9840 |
| theta_abs_le_8_mae_deg | 0.4679 | 0.0000 | 0.4679 | 0.4679 |
| theta_abs_le_10_mae_deg | 0.4679 | 0.0000 | 0.4679 | 0.4679 |
| theta_pos_6_8_mae_deg | 0.9696 | 0.0000 | 0.9696 | 0.9696 |
| theta_pos_6_8_bias_deg | -0.9600 | 0.0000 | -0.9600 | -0.9600 |
| theta_neg_8_6_mae_deg | 0.7362 | 0.0000 | 0.7362 | 0.7362 |
| theta_neg_8_6_bias_deg | 0.7110 | 0.0000 | 0.7110 | 0.7110 |

## MATLAB vs Python Summary Diff

| seed | metric | MATLAB | Python | abs error | pass |
|---:|---|---:|---:|---:|---:|
| 21 | acc_main | 0.98668726 | 0.98668726 | 0 | 1 |
| 21 | acc_turn | 0.95292733 | 0.95292733 | 0 | 1 |
| 21 | acc_turn_pure | 0.98186902 | 0.98186902 | 0 | 1 |
| 21 | acc_turn_transition | 0.76240937 | 0.76240937 | 0 | 1 |
| 21 | theta_mae_deg | 0.46788420 | 0.46788132 | 2.88e-06 | 1 |
| 21 | flat_recall | 0.98762157 | 0.98762157 | 0 | 1 |
| 21 | stall_recall | 0.97206245 | 0.97206245 | 0 | 1 |
| 21 | slope_recall | 0.98901838 | 0.98901838 | 0 | 1 |
| 21 | uphill_recall | 0.99441860 | 0.99441860 | 0 | 1 |
| 21 | downhill_recall | 0.98399654 | 0.98399654 | 0 | 1 |
| 21 | theta_abs_le_8_mae_deg | 0.46788420 | 0.46788132 | 2.88e-06 | 1 |
| 21 | theta_abs_le_10_mae_deg | 0.46788420 | 0.46788132 | 2.88e-06 | 1 |
| 21 | theta_pos_6_8_mae_deg | 0.96955839 | 0.96940225 | 0.000156 | 0 |
| 21 | theta_pos_6_8_bias_deg | -0.95998779 | -0.95980018 | 0.000188 | 0 |
| 21 | theta_neg_8_6_mae_deg | 0.73615553 | 0.73613244 | 2.31e-05 | 1 |
| 21 | theta_neg_8_6_bias_deg | 0.71097722 | 0.71095109 | 2.61e-05 | 1 |

## Decision

MATLAB full test set metrics do not match Python summary. Inspect the diff table before moving to Simulink.
