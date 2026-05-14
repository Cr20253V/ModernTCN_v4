# ModernTCN v1 MATLAB Full Test Set Evaluation

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich_clean_turn_aug.mat`
- Mode: full X_test.
- Metric diff tolerance vs Python summary: 1.0e-04

## Per-Seed MATLAB Metrics

| seed | main | turn | turnT | theta deg | flat | stall | slope | uphill | downhill | seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 73 | 0.9752 | 0.7894 | 0.5944 | 0.3931 | 0.9867 | 0.8852 | 0.9776 | 0.9669 | 0.9933 | 55.3 |

## MATLAB Summary Across Requested Seeds

| metric | mean | std | min | max |
|---|---:|---:|---:|---:|
| acc_main | 0.9752 | 0.0000 | 0.9752 | 0.9752 |
| acc_turn | 0.7894 | 0.0000 | 0.7894 | 0.7894 |
| acc_turn_pure | 0.8298 | 0.0000 | 0.8298 | 0.8298 |
| acc_turn_transition | 0.5944 | 0.0000 | 0.5944 | 0.5944 |
| theta_mae_deg | 0.3931 | 0.0000 | 0.3931 | 0.3931 |
| flat_recall | 0.9867 | 0.0000 | 0.9867 | 0.9867 |
| stall_recall | 0.8852 | 0.0000 | 0.8852 | 0.8852 |
| slope_recall | 0.9776 | 0.0000 | 0.9776 | 0.9776 |
| uphill_recall | 0.9669 | 0.0000 | 0.9669 | 0.9669 |
| downhill_recall | 0.9933 | 0.0000 | 0.9933 | 0.9933 |

## MATLAB vs Python Summary Diff

| seed | metric | MATLAB | Python | abs error | pass |
|---:|---|---:|---:|---:|---:|
| 73 | acc_main | 0.97519030 | 0.97519030 | 0 | 1 |
| 73 | acc_turn | 0.78939949 | 0.78939949 | 0 | 1 |
| 73 | acc_turn_pure | 0.82981620 | 0.82981620 | 0 | 1 |
| 73 | acc_turn_transition | 0.59441708 | 0.59441708 | 0 | 1 |
| 73 | theta_mae_deg | 0.39310208 | 0.39310202 | 6.35e-08 | 1 |
| 73 | flat_recall | 0.98671832 | 0.98671832 | 0 | 1 |
| 73 | stall_recall | 0.88518519 | 0.88518519 | 0 | 1 |
| 73 | slope_recall | 0.97755102 | 0.97755102 | 0 | 1 |
| 73 | uphill_recall | 0.96693273 | 0.96693273 | 0 | 1 |
| 73 | downhill_recall | 0.99325464 | 0.99325464 | 0 | 1 |

## Decision

MATLAB full test set metrics match Python summary within tolerance. The offline MATLAB inference path is ready for MATLAB wrapper design.
