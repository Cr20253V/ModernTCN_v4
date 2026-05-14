# ModernTCN y_raw Replay Diagnostic

- out file: `ModernTCN_out.mat`
- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v4_turn_focus_A_theta_head_B_seed21\modern_tcn_seed21.onnx`
- turn truth thresholds: `0.02` and `0.05` rad/s; training labels use `0.05` rad/s.

| zone | theta MAE deg | main acc | turn acc 0.05 | left recall 0.05 | raw left recall 0.05 | pred main 3 | pred turn 1 | raw pred turn 1 | left p90 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| startup | 0.000 | 100.0 | 100.0 | NaN | NaN | 0.0 | 0.0 | 0.0 | 0.000 |
| golden_test | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| pure_turn | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| pure_slope | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| composite | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| closed_loop | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| closure | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |

## Full Zone Table

Saved in `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\closed_loop_replay\ModernTCN_out_modern_tcn_replay_modern_tcn_v4_turn_focus_A_theta_head_B_seed21.mat` as `result.zone_table`.
