# dual_kernel Offline Summary

- baseline: `ModernTCN_turn_l020_tt25_seed101`
- runs: `9`
- passing_offline_gate: `0`
- best_run: `dual_k31_s7_seed42`
- default_k31_configs: `dual_k31_s3`, `dual_k31_s5`, `dual_k31_s7`
- extension_configs_are_separate: `1`

## Group Means

| config | n | acc_main | acc_turn | acc_turn_transition | theta_mae_deg | gate_passes |
|---|---:|---:|---:|---:|---:|---:|
| `dual_k31_s3` | 3 | 0.965205 | 0.550250 | 0.473423 | 0.997132 | 0 |
| `dual_k31_s5` | 3 | 0.959837 | 0.516935 | 0.446597 | 0.845044 | 0 |
| `dual_k31_s7` | 3 | 0.964649 | 0.560429 | 0.482365 | 0.760435 | 0 |
