# ModernTCN v1 MATLAB Full Test Set Evaluation

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich_clean_turn_aug.mat`
- Mode: full X_test.
- Metric diff tolerance vs Python summary: 1.0e-04

## Per-Seed MATLAB Metrics

| seed | main | turn | turnT | theta deg | flat | stall | slope | uphill | downhill | seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 73 | 0.9752 | 0.7894 | 0.5944 | 0.6062 | 0.9867 | 0.8852 | 0.9776 | 0.9669 | 0.9933 | 57.9 |

## MATLAB Summary Across Requested Seeds

| metric | mean | std | min | max |
|---|---:|---:|---:|---:|
| acc_main | 0.9752 | 0.0000 | 0.9752 | 0.9752 |
| acc_turn | 0.7894 | 0.0000 | 0.7894 | 0.7894 |
| acc_turn_pure | 0.8298 | 0.0000 | 0.8298 | 0.8298 |
| acc_turn_transition | 0.5944 | 0.0000 | 0.5944 | 0.5944 |
| theta_mae_deg | 0.6062 | 0.0000 | 0.6062 | 0.6062 |
| flat_recall | 0.9867 | 0.0000 | 0.9867 | 0.9867 |
| stall_recall | 0.8852 | 0.0000 | 0.8852 | 0.8852 |
| slope_recall | 0.9776 | 0.0000 | 0.9776 | 0.9776 |
| uphill_recall | 0.9669 | 0.0000 | 0.9669 | 0.9669 |
| downhill_recall | 0.9933 | 0.0000 | 0.9933 | 0.9933 |

## MATLAB vs Python Summary Diff

Smoke mode does not compare metrics with full Python summary.

## Decision

MATLAB full test set metrics do not match Python summary. Inspect the diff table before moving to Simulink.
