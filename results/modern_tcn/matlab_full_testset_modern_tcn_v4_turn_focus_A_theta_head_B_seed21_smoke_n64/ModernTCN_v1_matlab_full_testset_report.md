# ModernTCN v1 MATLAB Full Test Set Evaluation

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- Mode: smoke test, first 64 test windows only.
- Metric diff tolerance vs Python summary: 1.0e-04

## Per-Seed MATLAB Metrics

| seed | main | turn | turnT | theta deg | flat | stall | slope | uphill | downhill | seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 21 | 0.9531 | 0.9375 | 0.8333 | 0.5021 | 0.9268 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 12.1 |

## MATLAB Summary Across Requested Seeds

| metric | mean | std | min | max |
|---|---:|---:|---:|---:|
| acc_main | 0.9531 | 0.0000 | 0.9531 | 0.9531 |
| acc_turn | 0.9375 | 0.0000 | 0.9375 | 0.9375 |
| acc_turn_pure | 0.9483 | 0.0000 | 0.9483 | 0.9483 |
| acc_turn_transition | 0.8333 | 0.0000 | 0.8333 | 0.8333 |
| theta_mae_deg | 0.5021 | 0.0000 | 0.5021 | 0.5021 |
| flat_recall | 0.9268 | 0.0000 | 0.9268 | 0.9268 |
| stall_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| slope_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| uphill_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| downhill_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |

## MATLAB vs Python Summary Diff

Smoke mode does not compare metrics with full Python summary.

## Decision

This is a smoke test only. Run `ModernTCN_matlab_full_testset_eval()` for the full decision.
