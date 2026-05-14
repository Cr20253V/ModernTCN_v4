# ModernTCN y_raw Replay Diagnostic

- out file: `out.mat`
- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed73\modern_tcn_seed73.onnx`
- turn truth thresholds: `0.02` and `0.05` rad/s; training labels use `0.05` rad/s.

| zone | theta MAE deg | main acc | turn acc 0.05 | left recall 0.05 | raw left recall 0.05 | pred main 3 | pred turn 1 | raw pred turn 1 | left p90 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| startup | 0.000 | 100.0 | 100.0 | NaN | NaN | 0.0 | 0.0 | 0.0 | 0.001 |
| golden_test | 0.000 | 100.0 | 100.0 | NaN | NaN | 0.0 | 0.0 | 0.0 | 0.000 |
| pure_turn | 0.491 | 99.3 | 23.2 | 19.6 | 21.0 | 0.7 | 18.7 | 20.0 | 0.971 |
| pure_slope | 1.314 | 84.4 | 96.1 | 0.0 | 0.0 | 48.9 | 0.0 | 1.2 | 0.148 |
| composite | 0.919 | 94.3 | 100.0 | NaN | NaN | 46.1 | 0.0 | 0.0 | 0.000 |
| closed_loop | 0.462 | 100.0 | 34.2 | 0.0 | 0.0 | 0.0 | 2.2 | 2.2 | 0.124 |
| closure | 0.462 | 100.0 | 34.2 | 0.0 | 0.0 | 0.0 | 2.2 | 2.2 | 0.124 |

## Full Zone Table

Saved in `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\closed_loop_replay\out_modern_tcn_replay_current_model.mat` as `result.zone_table`.
