# ModernTCN y_raw Replay Diagnostic

- out file: `out.mat`
- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_kinTurnD_seed73\modern_tcn_seed73.onnx`
- turn truth thresholds: `0.02` and `0.05` rad/s; training labels use `0.05` rad/s.

| zone | theta MAE deg | main acc | turn acc 0.05 | left recall 0.05 | raw left recall 0.05 | pred main 3 | pred turn 1 | raw pred turn 1 | left p90 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| startup | 0.000 | 100.0 | 100.0 | NaN | NaN | 0.0 | 0.0 | 0.0 | 0.003 |
| golden_test | 0.000 | 100.0 | 100.0 | NaN | NaN | 0.0 | 0.0 | 0.0 | 0.002 |
| pure_turn | 2.466 | 99.2 | 98.3 | 98.2 | 99.7 | 0.8 | 93.8 | 95.2 | 0.974 |
| pure_slope | 0.994 | 93.9 | 93.6 | 100.0 | 83.3 | 58.8 | 5.2 | 3.2 | 0.074 |
| composite | 0.587 | 94.2 | 88.6 | NaN | NaN | 46.9 | 1.1 | 4.0 | 0.425 |
| closed_loop | 1.645 | 100.0 | 86.1 | 96.9 | 97.0 | 0.0 | 71.1 | 68.4 | 0.939 |
| closure | 1.645 | 100.0 | 86.1 | 96.9 | 97.0 | 0.0 | 71.1 | 68.4 | 0.939 |

## Full Zone Table

Saved in `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\closed_loop_replay\out_modern_tcn_replay_transition_rich_v3_kinTurnD_seed73.mat` as `result.zone_table`.
