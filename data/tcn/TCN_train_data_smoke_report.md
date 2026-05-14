# TCN Training Data Generation Report

- Generated: 2026-04-24 20:08:57
- Output: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_train_data_smoke.mat`
- Model: `GRU_DataGen`
- Valid runs: 1
- Failed runs: 0
- Total samples: 1801

## Label Distribution

| label | count | ratio |
|---|---:|---:|
| flat | 1637 | 0.9089 |
| stall | 164 | 0.0911 |
| slope | 0 | 0.0000 |
| turn right | 0 | 0.0000 |
| turn straight | 1801 | 1.0000 |
| turn left | 0 | 0.0000 |
| slip aux | 0 | 0.0000 |
| stall aux | 164 | 0.0911 |
| load_change aux | 0 | 0.0000 |

## Transition Coverage

- Runs with dynamic windows: 1
- Dynamic window hits: 2

## Event Coverage

- Runs with slip labels: 0
- Runs with stall labels: 1
- Runs with load-change labels: 0

## Paths

- `path_train_tcn_01_flat_speed_variation`
