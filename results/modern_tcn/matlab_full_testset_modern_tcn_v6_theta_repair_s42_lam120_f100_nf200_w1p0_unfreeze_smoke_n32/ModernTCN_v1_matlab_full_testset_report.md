# ModernTCN v1 MATLAB Full Test Set Evaluation

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v6_longrun_diag2steer.mat`
- Mode: smoke test, first 32 test windows only.
- Metric diff tolerance vs Python summary: 1.0e-04

## Per-Seed MATLAB Metrics

| seed | main | turn | turnT | theta deg | flat | stall | slope | uphill | downhill | seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 42 | 0.9375 | 0.9375 | 1.0000 | 0.7352 | 1.0000 | 1.0000 | 0.8333 | 1.0000 | 0.2500 | 21.8 |

## MATLAB Summary Across Requested Seeds

| metric | mean | std | min | max |
|---|---:|---:|---:|---:|
| acc_main | 0.9375 | 0.0000 | 0.9375 | 0.9375 |
| acc_turn | 0.9375 | 0.0000 | 0.9375 | 0.9375 |
| acc_turn_pure | 0.9333 | 0.0000 | 0.9333 | 0.9333 |
| acc_turn_transition | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| theta_mae_deg | 0.7352 | 0.0000 | 0.7352 | 0.7352 |
| flat_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| stall_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| slope_recall | 0.8333 | 0.0000 | 0.8333 | 0.8333 |
| uphill_recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| downhill_recall | 0.2500 | 0.0000 | 0.2500 | 0.2500 |
| theta_abs_le_8_mae_deg | 0.7352 | 0.0000 | 0.7352 | 0.7352 |
| theta_abs_le_10_mae_deg | 0.7352 | 0.0000 | 0.7352 | 0.7352 |
| theta_pos_6_8_mae_deg | 0.8043 | 0.0000 | 0.8043 | 0.8043 |
| theta_pos_6_8_bias_deg | -0.6986 | 0.0000 | -0.6986 | -0.6986 |
| theta_neg_8_6_mae_deg | NaN | NaN | NaN | NaN |
| theta_neg_8_6_bias_deg | NaN | NaN | NaN | NaN |

## MATLAB vs Python Summary Diff

Smoke mode does not compare metrics with full Python summary.

## Decision

This is a smoke test only. Run `ModernTCN_matlab_full_testset_eval()` for the full decision.
