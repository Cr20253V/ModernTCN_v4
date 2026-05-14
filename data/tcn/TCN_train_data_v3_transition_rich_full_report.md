# TCN Training Data Generation Report

- Generated: 2026-05-03 17:26:36
- Output: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_train_data_v3_transition_rich_full.mat`
- Model: `GRU_DataGen`
- Valid runs: 160
- Failed runs: 0
- Total samples: 487360

## Label Distribution

| label | count | ratio |
|---|---:|---:|
| flat | 301171 | 0.6180 |
| stall | 18958 | 0.0389 |
| slope | 167231 | 0.3431 |
| turn right | 84536 | 0.1735 |
| turn straight | 319152 | 0.6549 |
| turn left | 83672 | 0.1717 |
| slip aux | 11255 | 0.0231 |
| stall aux | 18958 | 0.0389 |
| load_change aux | 17171 | 0.0352 |

## Transition Coverage

- Runs with dynamic windows: 160
- Dynamic window hits: 432

## Event Coverage

- Runs with slip labels: 58
- Runs with stall labels: 80
- Runs with load-change labels: 71

## Paths

- `path_train_tcn_v3_01_flat_speed_variation`
- `path_train_tcn_v3_02_left_turn_entry_exit`
- `path_train_tcn_v3_03_right_turn_entry_exit`
- `path_train_tcn_v3_04_slope_up_down`
- `path_train_tcn_v3_05_down_slope_recovery`
- `path_train_tcn_v3_06_s_curve_balanced`
- `path_train_tcn_v3_07_slope_left_turn_combo`
- `path_train_tcn_v3_08_slope_right_turn_combo`
- `path_train_tcn_v3_09_load_change_candidate`
- `path_train_tcn_v3_10_stall_candidate_low_speed`
- `path_train_tcn_v3_11_multi_turn_left_variable_radius`
- `path_train_tcn_v3_12_multi_turn_right_variable_radius`
- `path_train_tcn_v3_13_steep_slope_transition`
- `path_train_tcn_v3_14_downhill_turn_transition`
- `path_train_tcn_v3_15_bumpy_theta_local`
- `path_train_tcn_v3_16_disturbance_transition_meta`
- `path_train_tcn_v3_17_challenge_fast_s_curve`
- `path_train_tcn_v3_18_challenge_steep_combo`
- `path_train_tcn_v3_19_v3_uphill_left_overlap_entry`
- `path_train_tcn_v3_20_v3_uphill_right_overlap_entry`
- `path_train_tcn_v3_21_v3_downhill_left_overlap_entry`
- `path_train_tcn_v3_22_v3_downhill_right_overlap_entry`
- `path_train_tcn_v3_23_v3_uphill_left_overlap_exit`
- `path_train_tcn_v3_24_v3_downhill_right_overlap_exit`
- `path_train_tcn_v3_25_v3_long_ramp_up_left_turn`
- `path_train_tcn_v3_26_v3_long_ramp_down_right_turn`
- `path_train_tcn_v3_27_v3_theta_reversal_s_curve`
- `path_train_tcn_v3_28_v3_theta_sine_left_turn`
- `path_train_tcn_v3_29_v3_theta_sine_right_turn`
- `path_train_tcn_v3_30_v3_fast_slope_step_left`
- `path_train_tcn_v3_31_v3_slow_slope_step_right`
- `path_train_tcn_v3_32_v3_speed_slope_turn_coupled`
- `path_train_tcn_v3_33_v3_flat_low_load_left_turn`
- `path_train_tcn_v3_34_v3_flat_low_load_right_turn`
- `path_train_tcn_v3_35_v3_flat_low_load_s_curve`
- `path_train_tcn_v3_36_v3_flat_left_turn_speed_sweep`
- `path_train_tcn_v3_37_v3_flat_right_turn_speed_sweep`
- `path_train_tcn_v3_38_v3_mild_slope_low_load_left_turn`
- `path_train_tcn_v3_39_v3_mild_slope_low_load_right_turn`
- `path_train_tcn_v3_40_v3_flat_low_speed_closure_turn`
