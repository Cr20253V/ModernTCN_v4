# TCN Prepare Dataset Report

- Generated: 2026-06-15 22:35:47
- Source: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- Output: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- Split file: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_shared_run_split_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- Contract file: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_contract.json`
- Split strategy: `stratified_run_level_v2_theta_nonstall_full_range_1deg`
- Split balance score: 217.240929
- Feature contract: `passive17_plus_all5`
- Plant revision: `agv_physics_v2_plantfix`
- Vehicle: `diagonal_dual_steer_drive_agv`, active wheels=`LF,RR`, passive wheels=`RF,LR`
- Input policy: `imu_free_passive17_plus_all5`, input_dim=22, no_new_inputs=1
- Label time policy: `current_window_end`, horizon_steps=0, horizon_seconds=0.000
- Confidence policy: `derive_classification_confidence_from_softmax_and_export`
- theta_mask_strategy: `nonstall_full_range`
- seq_len: 128
- stride: 64
- transition_rich: 1
- steady_stride: 96
- transition_stride: 16
- transition_context_sec: 1.25
- skip_initial_sec: 1.00
- turn_label_strategy: `tail_majority`
- turn_tail_sec: 0.50
- turn_min_purity: 0.70
- turn_ambiguous_weight: 0.60

## Window Counts

| split | windows |
|---|---:|
| train | 16529 |
| val | 3695 |
| test | 3602 |

## Main Labels

| split | flat | stall | slope |
|---|---:|---:|---:|
| train | 3283 | 432 | 12814 |
| val | 657 | 42 | 2996 |
| test | 756 | 96 | 2750 |

## Turn Labels

| split | right | straight | left |
|---|---:|---:|---:|
| train | 3463 | 9219 | 3847 |
| val | 844 | 1924 | 927 |
| test | 799 | 1933 | 870 |

## Main Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.9772 | 0.0356 | 0.0498 | 0.0356 |
| val | 0.9843 | 0.0241 | 0.0376 | 0.0241 |
| test | 0.9756 | 0.0380 | 0.0525 | 0.0380 |

## Turn Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.9402 | 0.1053 | 0.1732 | 0.0883 |
| val | 0.9402 | 0.1045 | 0.1743 | 0.0871 |
| test | 0.9348 | 0.1163 | 0.1863 | 0.0958 |

### Turn Purity By Label

| split | label | windows | mean purity | low purity `<0.8` | transition ratio |
|---|---|---:|---:|---:|---:|
| train | right | 3463 | 0.9330 | 0.1195 | 0.1938 |
| train | straight | 9219 | 0.9457 | 0.0949 | 0.1579 |
| train | left | 3847 | 0.9334 | 0.1175 | 0.1913 |
| val | right | 844 | 0.9385 | 0.1066 | 0.1836 |
| val | straight | 1924 | 0.9434 | 0.0988 | 0.1637 |
| val | left | 927 | 0.9351 | 0.1143 | 0.1877 |
| test | right | 799 | 0.9272 | 0.1314 | 0.2015 |
| test | straight | 1933 | 0.9417 | 0.1024 | 0.1728 |
| test | left | 870 | 0.9267 | 0.1333 | 0.2023 |

## Theta Transition Windows

| split | range mean deg | range p95 deg | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.2409 | 0.9927 | 0.1288 | 0.0000 |
| val | 0.3090 | 1.0000 | 0.1521 | 0.0000 |
| test | 0.2410 | 1.0000 | 0.1399 | 0.0000 |

## Auxiliary Labels

| split | slip | stall | load_change |
|---|---:|---:|---:|
| train | 117 | 432 | 230 |
| val | 17 | 42 | 66 |
| test | 28 | 96 | 21 |

## Slope Sign Coverage

| split | negative slope | zero slope | positive slope |
|---|---:|---:|---:|
| train | 7929 | 190 | 7978 |
| val | 1798 | 0 | 1855 |
| test | 1762 | 0 | 1744 |

## Theta Supervision Bins

| split | `<-8` | `[-8,-6)` | `[-6,-4)` | `[-4,-2)` | `[-2,0)` | `[0,2)` | `[2,4)` | `[4,6)` | `[6,8)` | `>=8` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 1588 | 1607 | 1719 | 1473 | 1542 | 1741 | 1554 | 1723 | 1434 | 1716 |
| val | 347 | 379 | 351 | 364 | 357 | 300 | 382 | 410 | 410 | 353 |
| test | 363 | 378 | 313 | 330 | 378 | 378 | 330 | 330 | 378 | 328 |
