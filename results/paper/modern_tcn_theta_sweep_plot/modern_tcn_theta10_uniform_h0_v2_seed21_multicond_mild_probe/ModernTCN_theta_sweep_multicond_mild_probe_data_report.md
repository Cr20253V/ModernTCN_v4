# TCN Training Data Generation Report

- Generated: 2026-05-13 17:31:41
- Output: `E:\Matlab\Simulink\S-Function_16\results\paper\modern_tcn_theta_sweep_plot\modern_tcn_theta10_uniform_h0_v2_seed21_multicond_mild_probe\ModernTCN_theta_sweep_multicond_mild_probe_data.mat`
- Model: `GRU_DataGen`
- Valid runs: 1
- Failed runs: 0
- Total samples: 47040

## Label Distribution

| label | count | ratio |
|---|---:|---:|
| flat | 6720 | 0.1429 |
| stall | 0 | 0.0000 |
| slope | 40320 | 0.8571 |
| turn right | 0 | 0.0000 |
| turn straight | 47040 | 1.0000 |
| turn left | 0 | 0.0000 |
| slip aux | 0 | 0.0000 |
| stall aux | 0 | 0.0000 |
| load_change aux | 0 | 0.0000 |

## Transition Coverage

- Runs with dynamic windows: 1
- Dynamic window hits: 146

## Event Coverage

- Runs with slip labels: 0
- Runs with stall labels: 0
- Runs with load-change labels: 0

## Paths

- `path_modern_tcn_theta_sweep_multicond_mild_probe`
