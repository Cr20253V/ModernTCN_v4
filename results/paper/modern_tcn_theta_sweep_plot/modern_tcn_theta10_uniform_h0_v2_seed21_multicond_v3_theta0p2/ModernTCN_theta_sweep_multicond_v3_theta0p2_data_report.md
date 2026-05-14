# TCN Training Data Generation Report

- Generated: 2026-05-13 20:18:37
- Output: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_v3_theta0p2\ModernTCN_theta_sweep_multicond_v3_theta0p2_data.mat`
- Model: `GRU_DataGen`
- Valid runs: 1
- Failed runs: 0
- Total samples: 161600

## Label Distribution

| label | count | ratio |
|---|---:|---:|
| flat | 30400 | 0.1881 |
| stall | 0 | 0.0000 |
| slope | 131200 | 0.8119 |
| turn right | 0 | 0.0000 |
| turn straight | 161600 | 1.0000 |
| turn left | 0 | 0.0000 |
| slip aux | 0 | 0.0000 |
| stall aux | 0 | 0.0000 |
| load_change aux | 0 | 0.0000 |

## Transition Coverage

- Runs with dynamic windows: 1
- Dynamic window hits: 504

## Event Coverage

- Runs with slip labels: 0
- Runs with stall labels: 0
- Runs with load-change labels: 0

## Paths

- `path_modern_tcn_theta_sweep_multicond_v3_theta0p2`
