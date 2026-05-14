# TCN Training Data Generation Report

- Generated: 2026-05-03 22:28:32
- Output: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_train_data_v3_clean_turn_aug.mat`
- Model: `GRU_DataGen`
- Valid runs: 16
- Failed runs: 0
- Total samples: 47216

## Label Distribution

| label | count | ratio |
|---|---:|---:|
| flat | 47216 | 1.0000 |
| stall | 0 | 0.0000 |
| slope | 0 | 0.0000 |
| turn right | 0 | 0.0000 |
| turn straight | 31308 | 0.6631 |
| turn left | 15908 | 0.3369 |
| slip aux | 0 | 0.0000 |
| stall aux | 0 | 0.0000 |
| load_change aux | 0 | 0.0000 |

## Transition Coverage

- Runs with dynamic windows: 16
- Dynamic window hits: 40

## Event Coverage

- Runs with slip labels: 0
- Runs with stall labels: 0
- Runs with load-change labels: 0

## Paths

- `path_train_tcn_v3_01_flat_speed_variation`
- `path_train_tcn_v3_33_v3_flat_low_load_left_turn`
- `path_train_tcn_v3_36_v3_flat_left_turn_speed_sweep`
- `path_train_tcn_v3_40_v3_flat_low_speed_closure_turn`
