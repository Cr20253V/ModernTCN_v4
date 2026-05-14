# ModernTCN y_raw Replay Diagnostic

- out file: `out.mat`
- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_clean_turnC_seed73\modern_tcn_seed73.onnx`
- turn truth thresholds: `0.02` and `0.05` rad/s; training labels use `0.05` rad/s.

| zone | theta MAE deg | main acc | turn acc 0.05 | left recall 0.05 | raw left recall 0.05 | pred main 3 | pred turn 1 | raw pred turn 1 | left p90 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| startup | 0.000 | 100.0 | 100.0 | NaN | NaN | 0.0 | 0.0 | 0.0 | 0.000 |
| golden_test | 0.000 | 100.0 | 100.0 | NaN | NaN | 0.0 | 0.0 | 0.0 | 0.000 |
| pure_turn | 0.027 | 100.0 | 21.9 | 18.2 | 17.4 | 0.0 | 17.4 | 16.6 | 0.947 |
| pure_slope | 0.620 | 94.5 | 92.7 | 0.0 | 0.0 | 59.7 | 3.4 | 3.3 | 0.151 |
| composite | 0.407 | 95.5 | 94.2 | NaN | NaN | 48.4 | 0.0 | 0.0 | 0.000 |
| closed_loop | 0.542 | 100.0 | 34.8 | 0.0 | 0.0 | 0.0 | 1.6 | 1.6 | 0.002 |
| closure | 0.542 | 100.0 | 34.8 | 0.0 | 0.0 | 0.0 | 1.6 | 1.6 | 0.002 |

## Full Zone Table

Saved in `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\closed_loop_replay\out_modern_tcn_replay_transition_rich_v3_clean_turnC_seed73.mat` as `result.zone_table`.
