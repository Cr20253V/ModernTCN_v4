# ModernTCN y_raw Replay Diagnostic

- out file: `E:\Matlab\Simulink\S-Function_16\out.mat`
- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v4_turn_focus_A_theta_head_B_seed21\modern_tcn_seed21.onnx`
- turn truth thresholds: `0.02` and `0.05` rad/s; training labels use `0.05` rad/s.

| zone | theta MAE deg | main acc | turn acc 0.05 | left recall 0.05 | raw left recall 0.05 | pred main 3 | pred turn 1 | raw pred turn 1 | left p90 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| startup | 0.000 | 100.0 | 100.0 | NaN | NaN | 0.0 | 0.0 | 0.0 | 0.000 |
| golden_test | 0.712 | 100.0 | 59.4 | NaN | NaN | 0.0 | 0.0 | 0.0 | 0.000 |
| pure_turn | 1.107 | 97.9 | 68.7 | NaN | NaN | 39.1 | 0.0 | 0.0 | 0.000 |
| pure_slope | 0.847 | 93.3 | 100.0 | NaN | NaN | 72.0 | 0.0 | 0.0 | 0.000 |
| composite | 0.738 | 97.5 | 93.0 | NaN | NaN | 50.5 | 0.0 | 0.0 | 0.009 |
| closed_loop | 1.846 | 68.6 | 72.4 | 68.5 | 64.6 | 47.6 | 60.0 | 56.6 | 1.000 |
| closure | 1.846 | 68.6 | 72.4 | 68.5 | 64.6 | 47.6 | 60.0 | 56.6 | 1.000 |

## Full Zone Table

Saved in `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\closed_loop_replay\out_modern_tcn_replay_modern_tcn_v4_turn_focus_A_theta_head_B_seed21.mat` as `result.zone_table`.
