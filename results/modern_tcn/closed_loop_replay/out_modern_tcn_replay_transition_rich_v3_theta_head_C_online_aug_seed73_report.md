# ModernTCN y_raw Replay Diagnostic

- out file: `out.mat`
- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_theta_head_C_online_aug_seed73\modern_tcn_seed73.onnx`
- turn truth thresholds: `0.02` and `0.05` rad/s; training labels use `0.05` rad/s.

| zone | theta MAE deg | main acc | turn acc 0.05 | left recall 0.05 | raw left recall 0.05 | pred main 3 | pred turn 1 | raw pred turn 1 | left p90 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| startup | 0.000 | 100.0 | 100.0 | NaN | NaN | 0.0 | 0.0 | 0.0 | 0.003 |
| golden_test | 0.000 | 100.0 | 100.0 | NaN | NaN | 0.0 | 0.0 | 0.0 | 0.002 |
| pure_turn | 0.000 | 100.0 | 98.3 | 98.2 | 99.7 | 0.0 | 93.8 | 95.2 | 0.973 |
| pure_slope | 1.080 | 93.9 | 92.4 | 100.0 | 84.6 | 58.8 | 5.2 | 3.3 | 0.079 |
| composite | 0.731 | 94.2 | 88.8 | NaN | NaN | 46.9 | 1.1 | 3.5 | 0.420 |
| closed_loop | 0.001 | 100.0 | 86.3 | 98.0 | 97.9 | 0.0 | 71.7 | 68.7 | 0.942 |
| closure | 0.001 | 100.0 | 86.3 | 98.0 | 97.9 | 0.0 | 71.7 | 68.7 | 0.942 |

## Full Zone Table

Saved in `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\closed_loop_replay\out_modern_tcn_replay_transition_rich_v3_theta_head_C_online_aug_seed73.mat` as `result.zone_table`.
