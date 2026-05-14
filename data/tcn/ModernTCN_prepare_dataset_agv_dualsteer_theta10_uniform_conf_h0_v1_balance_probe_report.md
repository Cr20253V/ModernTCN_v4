# TCN Prepare Dataset Report

- Generated: 2026-05-11 22:43:19
- Source: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v1.mat`
- Output: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v1_balance_probe.mat`
- Split file: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_shared_run_split_agv_dualsteer_theta10_uniform_conf_h0_v1_balance_probe.mat`
- Contract file: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v1_balance_probe_contract.json`
- Split strategy: `stratified_run_level_v2_theta_nonstall_full_range_1deg`
- Split balance score: 313.012561
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
| train | 12259 |
| val | 4268 |
| test | 3698 |

## Main Labels

| split | flat | stall | slope |
|---|---:|---:|---:|
| train | 2436 | 527 | 9296 |
| val | 888 | 42 | 3338 |
| test | 741 | 92 | 2865 |

## Turn Labels

| split | right | straight | left |
|---|---:|---:|---:|
| train | 2727 | 7074 | 2458 |
| val | 952 | 2408 | 908 |
| test | 756 | 2127 | 815 |

## Main Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.9692 | 0.0482 | 0.0643 | 0.0482 |
| val | 0.9867 | 0.0206 | 0.0309 | 0.0206 |
| test | 0.9763 | 0.0362 | 0.0533 | 0.0362 |

## Turn Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.9360 | 0.1134 | 0.1836 | 0.0958 |
| val | 0.9458 | 0.0951 | 0.1563 | 0.0806 |
| test | 0.9507 | 0.0860 | 0.1460 | 0.0738 |

### Turn Purity By Label

| split | label | windows | mean purity | low purity `<0.8` | transition ratio |
|---|---|---:|---:|---:|---:|
| train | right | 2727 | 0.9239 | 0.1364 | 0.2127 |
| train | straight | 7074 | 0.9445 | 0.0975 | 0.1603 |
| train | left | 2458 | 0.9250 | 0.1334 | 0.2185 |
| val | right | 952 | 0.9424 | 0.0987 | 0.1660 |
| val | straight | 2408 | 0.9524 | 0.0847 | 0.1404 |
| val | left | 908 | 0.9317 | 0.1189 | 0.1883 |
| test | right | 756 | 0.9370 | 0.1098 | 0.1839 |
| test | straight | 2127 | 0.9572 | 0.0752 | 0.1265 |
| test | left | 815 | 0.9464 | 0.0920 | 0.1620 |

## Theta Transition Windows

| split | range mean deg | range p95 deg | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.1862 | 0.8837 | 0.0925 | 0.0000 |
| val | 0.2808 | 1.0000 | 0.1724 | 0.0000 |
| test | 0.3229 | 1.0000 | 0.1633 | 0.0000 |

## Auxiliary Labels

| split | slip | stall | load_change |
|---|---:|---:|---:|
| train | 77 | 527 | 183 |
| val | 42 | 42 | 63 |
| test | 29 | 92 | 86 |

## Slope Sign Coverage

| split | negative slope | zero slope | positive slope |
|---|---:|---:|---:|
| train | 5799 | 144 | 5789 |
| val | 2047 | 0 | 2179 |
| test | 1840 | 0 | 1766 |

## Theta Supervision Bins

| split | `<-8` | `[-8,-6)` | `[-6,-4)` | `[-4,-2)` | `[-2,0)` | `[0,2)` | `[2,4)` | `[4,6)` | `[6,8)` | `>=8` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 1116 | 1218 | 1029 | 1218 | 1218 | 1218 | 1218 | 1218 | 1061 | 1218 |
| val | 417 | 423 | 451 | 348 | 408 | 480 | 450 | 339 | 443 | 467 |
| test | 396 | 367 | 346 | 335 | 396 | 345 | 362 | 371 | 396 | 292 |
