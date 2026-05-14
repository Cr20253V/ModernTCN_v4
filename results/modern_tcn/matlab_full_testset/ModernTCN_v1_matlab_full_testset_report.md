# ModernTCN v1 MATLAB Full Test Set Evaluation

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`
- Mode: full X_test.
- Metric diff tolerance vs Python summary: 1.0e-04

## Per-Seed MATLAB Metrics

| seed | main | turn | turnT | theta deg | flat | stall | slope | uphill | downhill | seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 73 | 0.9632 | 0.8981 | 0.7076 | 0.5015 | 0.9563 | 0.8612 | 0.9893 | 0.9859 | 0.9948 | 49.5 |

## MATLAB Summary Across Requested Seeds

| metric | mean | std | min | max |
|---|---:|---:|---:|---:|
| acc_main | 0.9632 | 0.0000 | 0.9632 | 0.9632 |
| acc_turn | 0.8981 | 0.0000 | 0.8981 | 0.8981 |
| acc_turn_pure | 0.9310 | 0.0000 | 0.9310 | 0.9310 |
| acc_turn_transition | 0.7076 | 0.0000 | 0.7076 | 0.7076 |
| theta_mae_deg | 0.5015 | 0.0000 | 0.5015 | 0.5015 |
| flat_recall | 0.9563 | 0.0000 | 0.9563 | 0.9563 |
| stall_recall | 0.8612 | 0.0000 | 0.8612 | 0.8612 |
| slope_recall | 0.9893 | 0.0000 | 0.9893 | 0.9893 |
| uphill_recall | 0.9859 | 0.0000 | 0.9859 | 0.9859 |
| downhill_recall | 0.9948 | 0.0000 | 0.9948 | 0.9948 |

## MATLAB vs Python Summary Diff

| seed | metric | MATLAB | Python | abs error | pass |
|---:|---|---:|---:|---:|---:|
| 73 | acc_main | 0.96320869 | 0.96320869 | 0 | 1 |
| 73 | acc_turn | 0.89806996 | 0.89806996 | 0 | 1 |
| 73 | acc_turn_pure | 0.93102229 | 0.93102229 | 0 | 1 |
| 73 | acc_turn_transition | 0.70756646 | 0.70756646 | 0 | 1 |
| 73 | theta_mae_deg | 0.50151363 | 0.50151354 | 8.54e-08 | 1 |
| 73 | flat_recall | 0.95629485 | 0.95629485 | 0 | 1 |
| 73 | stall_recall | 0.86120996 | 0.86120996 | 0 | 1 |
| 73 | slope_recall | 0.98934754 | 0.98934754 | 0 | 1 |
| 73 | uphill_recall | 0.98590022 | 0.98590022 | 0 | 1 |
| 73 | downhill_recall | 0.99482759 | 0.99482759 | 0 | 1 |

## Decision

MATLAB full test set metrics match Python summary within tolerance. The offline MATLAB inference path is ready for MATLAB wrapper design.
