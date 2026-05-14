# ModernTCN v1 MATLAB Full Test Set Evaluation

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`
- Mode: smoke test, first 16 test windows only.
- Metric diff tolerance vs Python summary: 1.0e-04

## Per-Seed MATLAB Metrics

| seed | main | turn | turnT | theta deg | flat | stall | slope | uphill | downhill | seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 73 | 1.0000 | 0.8750 | 0.6667 | 0.2407 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 10.8 |

## MATLAB Summary Across Requested Seeds

| metric | mean | std | min | max |
|---|---:|---:|---:|---:|
| acc_main | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| acc_turn | 0.8750 | 0.0000 | 0.8750 | 0.8750 |
| acc_turn_pure | 0.9231 | 0.0000 | 0.9231 | 0.9231 |
| acc_turn_transition | 0.6667 | 0.0000 | 0.6667 | 0.6667 |
| theta_mae_deg | 0.2407 | 0.0000 | 0.2407 | 0.2407 |
| flat_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| stall_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| slope_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| uphill_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| downhill_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |

## MATLAB vs Python Summary Diff

Smoke mode does not compare metrics with full Python summary.

## Decision

This is a smoke test only. Run `ModernTCN_matlab_full_testset_eval()` for the full decision.
