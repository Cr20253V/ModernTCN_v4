# TCN Prepare Dataset Report

- Generated: 2026-05-12 10:34:51
- Source: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`
- Output: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`
- Split file: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_shared_run_split_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`
- Contract file: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2_contract.json`
- Split strategy: `stratified_run_level_v2_theta_nonstall_full_range_1deg`
- Split balance score: 176.626024
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
| train | 18302 |
| val | 2607 |
| test | 3733 |

## Main Labels

| split | flat | stall | slope |
|---|---:|---:|---:|
| train | 3739 | 339 | 14224 |
| val | 509 | 47 | 2051 |
| test | 757 | 117 | 2859 |

## Turn Labels

| split | right | straight | left |
|---|---:|---:|---:|
| train | 4013 | 9832 | 4457 |
| val | 468 | 1617 | 522 |
| test | 813 | 2188 | 732 |

## Main Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.9813 | 0.0290 | 0.0411 | 0.0290 |
| val | 0.9811 | 0.0288 | 0.0414 | 0.0288 |
| test | 0.9740 | 0.0413 | 0.0597 | 0.0413 |

## Turn Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.9352 | 0.1140 | 0.1872 | 0.0953 |
| val | 0.9434 | 0.0990 | 0.1611 | 0.0863 |
| test | 0.9498 | 0.0879 | 0.1433 | 0.0742 |

### Turn Purity By Label

| split | label | windows | mean purity | low purity `<0.8` | transition ratio |
|---|---|---:|---:|---:|---:|
| train | right | 4013 | 0.9307 | 0.1236 | 0.2011 |
| train | straight | 9832 | 0.9391 | 0.1065 | 0.1759 |
| train | left | 4457 | 0.9306 | 0.1218 | 0.1997 |
| val | right | 468 | 0.9315 | 0.1175 | 0.1859 |
| val | straight | 1617 | 0.9488 | 0.0897 | 0.1447 |
| val | left | 522 | 0.9375 | 0.1111 | 0.1897 |
| test | right | 813 | 0.9490 | 0.0849 | 0.1476 |
| test | straight | 2188 | 0.9544 | 0.0800 | 0.1303 |
| test | left | 732 | 0.9367 | 0.1148 | 0.1776 |

## Theta Transition Windows

| split | range mean deg | range p95 deg | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.2338 | 0.9927 | 0.1228 | 0.0000 |
| val | 0.2241 | 1.0000 | 0.1492 | 0.0000 |
| test | 0.3073 | 1.0000 | 0.1618 | 0.0000 |

## Auxiliary Labels

| split | slip | stall | load_change |
|---|---:|---:|---:|
| train | 152 | 339 | 276 |
| val | 31 | 47 | 29 |
| test | 31 | 117 | 65 |

## Slope Sign Coverage

| split | negative slope | zero slope | positive slope |
|---|---:|---:|---:|
| train | 8684 | 199 | 9080 |
| val | 1252 | 0 | 1308 |
| test | 1863 | 0 | 1753 |

## Theta Supervision Bins

| split | `<-8` | `[-8,-6)` | `[-6,-4)` | `[-4,-2)` | `[-2,0)` | `[0,2)` | `[2,4)` | `[4,6)` | `[6,8)` | `>=8` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 1559 | 1701 | 1772 | 1960 | 1692 | 2047 | 1706 | 1554 | 2090 | 1882 |
| val | 278 | 251 | 278 | 198 | 247 | 262 | 278 | 276 | 241 | 251 |
| test | 406 | 395 | 318 | 342 | 402 | 355 | 354 | 403 | 300 | 341 |
