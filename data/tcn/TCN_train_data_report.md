# TCN Training Data Generation Report

- Generated: 2026-04-24 21:10:46
- Output: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_train_data_full.mat`
- Model: `GRU_DataGen`
- Valid runs: 72
- Failed runs: 0
- Total samples: 189672

## Label Distribution

| label | count | ratio |
|---|---:|---:|
| flat | 126145 | 0.6651 |
| stall | 7001 | 0.0369 |
| slope | 56526 | 0.2980 |
| turn right | 29296 | 0.1545 |
| turn straight | 129732 | 0.6840 |
| turn left | 30644 | 0.1616 |
| slip aux | 5291 | 0.0279 |
| stall aux | 7001 | 0.0369 |
| load_change aux | 6469 | 0.0341 |

## Transition Coverage

- Runs with dynamic windows: 72
- Dynamic window hits: 168

## Event Coverage

- Runs with slip labels: 28
- Runs with stall labels: 31
- Runs with load-change labels: 30

## Paths

- `path_train_tcn_01_flat_speed_variation`
- `path_train_tcn_02_left_turn_entry_exit`
- `path_train_tcn_03_right_turn_entry_exit`
- `path_train_tcn_04_slope_up_down`
- `path_train_tcn_05_down_slope_recovery`
- `path_train_tcn_06_s_curve_balanced`
- `path_train_tcn_07_slope_left_turn_combo`
- `path_train_tcn_08_slope_right_turn_combo`
- `path_train_tcn_09_load_change_candidate`
- `path_train_tcn_10_stall_candidate_low_speed`
- `path_train_tcn_11_multi_turn_left_variable_radius`
- `path_train_tcn_12_multi_turn_right_variable_radius`
- `path_train_tcn_13_steep_slope_transition`
- `path_train_tcn_14_downhill_turn_transition`
- `path_train_tcn_15_bumpy_theta_local`
- `path_train_tcn_16_disturbance_transition_meta`
- `path_train_tcn_17_challenge_fast_s_curve`
- `path_train_tcn_18_challenge_steep_combo`
