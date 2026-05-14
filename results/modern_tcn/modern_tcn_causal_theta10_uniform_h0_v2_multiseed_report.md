# ModernTCN theta10 V2 multi-seed report

- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`
- seeds: `[11, 21, 42, 73, 101]`
- epochs: `180`, batch_size: `256`
- temporal_padding: `causal`
- theta_gate_mode: `none`
- theta_flat_loss_mode: `near_zero`, zero_tol_deg: `0.3`
- lambda_theta: `0.55`, lambda_turn: `0.08`

- turn_lr_target: `0.88`, turn_lr_weight: `0.2`

## Aggregate

| metric | mean | std |
|---|---:|---:|
| acc_main | 0.9769 | 0.0009 |
| flat_recall | 0.9609 | 0.0051 |
| slope_recall | 0.9936 | 0.0025 |
| acc_turn | 0.8901 | 0.0129 |
| acc_turn_transition | 0.7615 | 0.0232 |
| turn_right_recall | 0.8689 | 0.0186 |
| turn_left_recall | 0.9085 | 0.0131 |
| theta_mae_deg | 0.3017 | 0.0416 |
| theta_abs_le_10_p95_abs_err_deg | 0.9233 | 0.0865 |
| theta_neg_10_8_p95_abs_err_deg | 0.9136 | 0.0702 |
| theta_pos_8_10_p95_abs_err_deg | 1.1876 | 0.5666 |
| theta_neg_8_6_p95_abs_err_deg | 0.8818 | 0.1374 |
| theta_pos_6_8_p95_abs_err_deg | 0.6311 | 0.2466 |
| theta_neg_2_0p5_p95_abs_err_deg | 0.6638 | 0.1560 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.3997 | 0.0677 |
| theta_flat_abs_p95_deg | 2.2513 | 0.0846 |
| theta_flat_bias_deg | 0.0803 | 0.0586 |

## Per seed

| seed | acc_main | acc_turn_transition | turn_L/R | theta_mae | theta_10_p95 | edge_neg_p95 | edge_pos_p95 | checkpoint |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 11 | 0.9783 | 0.7907 | 0.9740 | 0.2507 | 0.7995 | 0.8823 | 0.7723 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed11\modern_tcn_seed11.pt` |
| 21 | 0.9759 | 0.7477 | 0.9709 | 0.3624 | 1.0491 | 1.0001 | 2.2814 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed21\modern_tcn_seed21.pt` |
| 42 | 0.9759 | 0.7383 | 0.9275 | 0.3353 | 0.9870 | 0.8279 | 1.1743 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed42\modern_tcn_seed42.pt` |
| 73 | 0.9770 | 0.7888 | 0.9418 | 0.2682 | 0.8949 | 0.9937 | 0.7687 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed73\modern_tcn_seed73.pt` |
| 101 | 0.9772 | 0.7421 | 0.9681 | 0.2918 | 0.8860 | 0.8642 | 0.9415 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed101\modern_tcn_seed101.pt` |
