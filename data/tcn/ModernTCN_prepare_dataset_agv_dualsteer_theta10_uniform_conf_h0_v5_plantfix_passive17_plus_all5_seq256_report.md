# ModernTCN seq256 Prepare Dataset Report

- Generated: 2026-06-21 13:16:05
- Source: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- Output: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_seq256.mat`
- Split file reused: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_shared_run_split_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- Contract file: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_seq256_contract.json`
- Split strategy: `reuse baseline run-level split ids`
- Scaler policy: `fit seq256 train windows only; apply val/test/online`
- Feature contract: `passive17_plus_all5`
- Plant revision: `agv_physics_v2_plantfix`
- Label time policy: `current_window_end`, horizon_steps=0
- seq_len: 256
- steady_stride: 96
- transition_stride: 16
- transition_context_sec: 1.25
- theta_balance_after_split: `1`
- turn_balance_after_split: `1`
- Python builder note: split-level balancing policy was reimplemented from `TCN_prepare_dataset.m`; MATLAB/Simulink was not invoked.

## Window Counts

| split | windows |
|---|---:|
| train | 18210 |
| val | 4209 |
| test | 3684 |

## Balance Drops

| split | theta dropped | turn dropped | theta rebalance dropped |
|---|---:|---:|---:|
| train | 907 | 138 | 3 |
| val | 952 | 0 | 0 |
| test | 1902 | 0 | 0 |
