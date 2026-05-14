# TCN Training Data Generation Report

- Generated: 2026-05-13 17:19:49
- Output: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_probe\ModernTCN_theta_sweep_multicond_probe_data.mat`
- Model: `GRU_DataGen`
- Valid runs: 1
- Failed runs: 0
- Total samples: 78720

## Label Distribution

| label | count | ratio |
|---|---:|---:|
| flat | 13440 | 0.1707 |
| stall | 0 | 0.0000 |
| slope | 65280 | 0.8293 |
| turn right | 26240 | 0.3333 |
| turn straight | 26240 | 0.3333 |
| turn left | 26240 | 0.3333 |
| slip aux | 0 | 0.0000 |
| stall aux | 0 | 0.0000 |
| load_change aux | 0 | 0.0000 |

## Transition Coverage

- Runs with dynamic windows: 1
- Dynamic window hits: 245

## Event Coverage

- Runs with slip labels: 0
- Runs with stall labels: 0
- Runs with load-change labels: 0

## Paths

- `path_modern_tcn_theta_sweep_multicond_probe`
