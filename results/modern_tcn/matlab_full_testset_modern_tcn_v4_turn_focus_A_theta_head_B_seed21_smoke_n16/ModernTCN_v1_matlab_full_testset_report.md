# ModernTCN v1 MATLAB Full Test Set Evaluation

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- Mode: smoke test, first 16 test windows only.
- Metric diff tolerance vs Python summary: 1.0e-04

## Per-Seed MATLAB Metrics

| seed | main | turn | turnT | theta deg | flat | stall | slope | uphill | downhill | seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 21 | 1.0000 | 0.9375 | 1.0000 | 0.6031 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 4.1 |

## MATLAB Summary Across Requested Seeds

| metric | mean | std | min | max |
|---|---:|---:|---:|---:|
| acc_main | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| acc_turn | 0.9375 | 0.0000 | 0.9375 | 0.9375 |
| acc_turn_pure | 0.9286 | 0.0000 | 0.9286 | 0.9286 |
| acc_turn_transition | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| theta_mae_deg | 0.6031 | 0.0000 | 0.6031 | 0.6031 |
| flat_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| stall_recall | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| slope_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| uphill_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| downhill_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |

## MATLAB vs Python Summary Diff

Smoke mode does not compare metrics with full Python summary.

## Decision

This is a smoke test only. Run `ModernTCN_matlab_full_testset_eval()` for the full decision.
