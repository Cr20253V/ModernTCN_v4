# ModernTCN theta10 V2 multi-seed report

- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`
- seeds: `[11, 21, 42, 73, 101]`
- epochs: `180`, batch_size: `256`
- theta_gate_mode: `none`
- theta_flat_loss_mode: `near_zero`, zero_tol_deg: `0.3`
- lambda_theta: `0.55`, lambda_turn: `0.08`

- turn_lr_target: `0.88`, turn_lr_weight: `0.2`

## Aggregate

| metric | mean | std |
|---|---:|---:|
| acc_main | 0.9786 | 0.0022 |
| flat_recall | 0.9643 | 0.0037 |
| slope_recall | 0.9952 | 0.0022 |
| acc_turn | 0.8871 | 0.0125 |
| acc_turn_transition | 0.7421 | 0.0238 |
| turn_right_recall | 0.8748 | 0.0252 |
| turn_left_recall | 0.8817 | 0.0127 |
| theta_mae_deg | 0.2950 | 0.0347 |
| theta_abs_le_10_p95_abs_err_deg | 0.8937 | 0.0604 |
| theta_neg_10_8_p95_abs_err_deg | 0.9624 | 0.2650 |
| theta_pos_8_10_p95_abs_err_deg | 1.1289 | 0.1847 |
| theta_neg_8_6_p95_abs_err_deg | 0.9013 | 0.1870 |
| theta_pos_6_8_p95_abs_err_deg | 0.4910 | 0.0825 |
| theta_neg_2_0p5_p95_abs_err_deg | 0.7088 | 0.1159 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.2954 | 0.2268 |
| theta_flat_abs_p95_deg | 2.1689 | 0.0490 |
| theta_flat_bias_deg | 0.0694 | 0.0613 |

## Per seed

| seed | acc_main | acc_turn_transition | turn_L/R | theta_mae | theta_10_p95 | edge_neg_p95 | edge_pos_p95 | checkpoint |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 11 | 0.9794 | 0.7551 | 0.9680 | 0.2700 | 0.8306 | 0.7964 | 1.1338 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta10_uniform_h0_v2_seed11\modern_tcn_seed11.pt` |
| 21 | 0.9807 | 0.7757 | 0.9969 | 0.2519 | 0.8194 | 0.6371 | 0.7922 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta10_uniform_h0_v2_seed21\modern_tcn_seed21.pt` |
| 42 | 0.9788 | 0.7121 | 0.9542 | 0.3428 | 0.9799 | 1.2814 | 1.1387 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta10_uniform_h0_v2_seed42\modern_tcn_seed42.pt` |
| 73 | 0.9796 | 0.7178 | 0.9761 | 0.3281 | 0.9201 | 1.2732 | 1.3413 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta10_uniform_h0_v2_seed73\modern_tcn_seed73.pt` |
| 101 | 0.9743 | 0.7495 | 0.9946 | 0.2820 | 0.9187 | 0.8238 | 1.2384 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta10_uniform_h0_v2_seed101\modern_tcn_seed101.pt` |
