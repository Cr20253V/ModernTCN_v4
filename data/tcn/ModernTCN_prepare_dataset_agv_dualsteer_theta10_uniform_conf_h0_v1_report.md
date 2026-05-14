# TCN Prepare Dataset Report

- Generated: 2026-05-11 20:57:18
- Source: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v1.mat`
- Output: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v1.mat`
- Split file: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_shared_run_split_agv_dualsteer_theta10_uniform_conf_h0_v1.mat`
- Contract file: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v1_contract.json`
- Split strategy: `stratified_run_level_v1_theta_nonstall_full_range`
- Split balance score: 5.426019
- Feature contract: `GRU_compatible_observable_19`
- Vehicle: `diagonal_dual_steer_drive_agv`, active wheels=`LF,RR`, passive wheels=`RF,LR`
- Input policy: `keep_current_algorithm_inputs_unchanged`, input_dim=19, no_new_inputs=1
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
| train | 17497 |
| val | 3333 |
| test | 3511 |

## Main Labels

| split | flat | stall | slope |
|---|---:|---:|---:|
| train | 3694 | 478 | 13325 |
| val | 649 | 78 | 2606 |
| test | 612 | 105 | 2794 |

## Turn Labels

| split | right | straight | left |
|---|---:|---:|---:|
| train | 3990 | 9789 | 3718 |
| val | 665 | 2079 | 589 |
| test | 708 | 2050 | 753 |

## Main Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.9758 | 0.0379 | 0.0520 | 0.0379 |
| val | 0.9807 | 0.0297 | 0.0432 | 0.0297 |
| test | 0.9746 | 0.0402 | 0.0544 | 0.0402 |

## Turn Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.9396 | 0.1059 | 0.1758 | 0.0900 |
| val | 0.9424 | 0.1023 | 0.1659 | 0.0849 |
| test | 0.9465 | 0.0946 | 0.1581 | 0.0800 |

### Turn Purity By Label

| split | label | windows | mean purity | low purity `<0.8` | transition ratio |
|---|---|---:|---:|---:|---:|
| train | right | 3990 | 0.9314 | 0.1213 | 0.1957 |
| train | straight | 9789 | 0.9466 | 0.0929 | 0.1568 |
| train | left | 3718 | 0.9300 | 0.1237 | 0.2044 |
| val | right | 665 | 0.9210 | 0.1414 | 0.2241 |
| val | straight | 2079 | 0.9542 | 0.0803 | 0.1328 |
| val | left | 589 | 0.9251 | 0.1358 | 0.2173 |
| test | right | 708 | 0.9367 | 0.1158 | 0.1864 |
| test | straight | 2050 | 0.9543 | 0.0800 | 0.1351 |
| test | left | 753 | 0.9346 | 0.1142 | 0.1939 |

## Theta Transition Windows

| split | range mean deg | range p95 deg | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.2213 | 0.9888 | 0.1217 | 0.0000 |
| val | 0.2152 | 0.9720 | 0.1089 | 0.0000 |
| test | 0.2210 | 0.9636 | 0.1171 | 0.0000 |

## Auxiliary Labels

| split | slip | stall | load_change |
|---|---:|---:|---:|
| train | 130 | 478 | 258 |
| val | 34 | 78 | 44 |
| test | 30 | 105 | 95 |

## Slope Sign Coverage

| split | negative slope | zero slope | positive slope |
|---|---:|---:|---:|
| train | 8344 | 220 | 8455 |
| val | 1657 | 0 | 1598 |
| test | 1673 | 0 | 1733 |

## Theta Supervision Bins

| split | `<-8` | `[-8,-6)` | `[-6,-4)` | `[-4,-2)` | `[-2,0)` | `[0,2)` | `[2,4)` | `[4,6)` | `[6,8)` | `>=8` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 1553 | 1579 | 1479 | 1933 | 1800 | 1894 | 1995 | 1510 | 1976 | 1300 |
| val | 430 | 334 | 320 | 261 | 312 | 337 | 262 | 270 | 126 | 603 |
| test | 249 | 433 | 584 | 137 | 270 | 342 | 163 | 522 | 265 | 441 |
