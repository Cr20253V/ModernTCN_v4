# ModernTCN v1 MATLAB Full Test Set Evaluation

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`
- Mode: smoke test, first 4 test windows only.
- Metric diff tolerance vs Python summary: 1.0e-04

## Per-Seed MATLAB Metrics

| seed | main | turn | turnT | theta deg | flat | stall | slope | uphill | downhill | seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 73 | 1.0000 | 0.7500 | 0.0000 | 0.1469 | 1.0000 | 0.0000 | 1.0000 | 1.0000 | NaN | 10.8 |

## MATLAB Summary Across Requested Seeds

| metric | mean | std | min | max |
|---|---:|---:|---:|---:|
| acc_main | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| acc_turn | 0.7500 | 0.0000 | 0.7500 | 0.7500 |
| acc_turn_pure | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| acc_turn_transition | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| theta_mae_deg | 0.1469 | 0.0000 | 0.1469 | 0.1469 |
| flat_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| stall_recall | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| slope_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| uphill_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| downhill_recall | NaN | NaN | NaN | NaN |

## MATLAB vs Python Summary Diff

Smoke mode does not compare metrics with full Python summary.

## Decision

This is a smoke test only. Run `ModernTCN_matlab_full_testset_eval()` for the full decision.
