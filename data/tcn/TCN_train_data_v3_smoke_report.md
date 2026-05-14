# TCN Training Data Generation Report

- Generated: 2026-05-03 16:04:07
- Output: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\retrain_v3_low_load\TCN_train_data_v3_smoke.mat`
- Model: `GRU_DataGen`
- Valid runs: 1
- Failed runs: 0
- Total samples: 1801

## Label Distribution

| label | count | ratio |
|---|---:|---:|
| flat | 1801 | 1.0000 |
| stall | 0 | 0.0000 |
| slope | 0 | 0.0000 |
| turn right | 0 | 0.0000 |
| turn straight | 1801 | 1.0000 |
| turn left | 0 | 0.0000 |
| slip aux | 0 | 0.0000 |
| stall aux | 0 | 0.0000 |
| load_change aux | 289 | 0.1605 |

## Transition Coverage

- Runs with dynamic windows: 1
- Dynamic window hits: 2

## Event Coverage

- Runs with slip labels: 0
- Runs with stall labels: 0
- Runs with load-change labels: 1

## Paths

- `path_train_tcn_v3_01_flat_speed_variation`
