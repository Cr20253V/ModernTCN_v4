# TCN Prepare Dataset Report

- Generated: 2026-05-11 22:39:31
- Source: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v1.mat`
- Output: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v1_splitfix_probe.mat`
- Split file: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_shared_run_split_agv_dualsteer_theta10_uniform_conf_h0_v1_splitfix_probe.mat`
- Contract file: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v1_splitfix_probe_contract.json`
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
| train | 14816 |
| val | 4957 |
| test | 4568 |

## Main Labels

| split | flat | stall | slope |
|---|---:|---:|---:|
| train | 3049 | 527 | 11240 |
| val | 1001 | 42 | 3914 |
| test | 905 | 92 | 3571 |

## Turn Labels

| split | right | straight | left |
|---|---:|---:|---:|
| train | 3359 | 8458 | 2999 |
| val | 1133 | 2813 | 1011 |
| test | 871 | 2647 | 1050 |

## Main Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.9723 | 0.0437 | 0.0587 | 0.0437 |
| val | 0.9864 | 0.0210 | 0.0307 | 0.0210 |
| test | 0.9786 | 0.0333 | 0.0486 | 0.0333 |

## Turn Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.9368 | 0.1117 | 0.1839 | 0.0940 |
| val | 0.9460 | 0.0944 | 0.1569 | 0.0803 |
| test | 0.9493 | 0.0882 | 0.1493 | 0.0760 |

### Turn Purity By Label

| split | label | windows | mean purity | low purity `<0.8` | transition ratio |
|---|---|---:|---:|---:|---:|
| train | right | 3359 | 0.9263 | 0.1322 | 0.2096 |
| train | straight | 8458 | 0.9448 | 0.0962 | 0.1617 |
| train | left | 2999 | 0.9259 | 0.1324 | 0.2174 |
| val | right | 1133 | 0.9397 | 0.1059 | 0.1730 |
| val | straight | 2813 | 0.9537 | 0.0811 | 0.1365 |
| val | left | 1011 | 0.9317 | 0.1187 | 0.1958 |
| test | right | 871 | 0.9365 | 0.1102 | 0.1860 |
| test | straight | 2647 | 0.9570 | 0.0748 | 0.1269 |
| test | left | 1050 | 0.9407 | 0.1038 | 0.1752 |

## Theta Transition Windows

| split | range mean deg | range p95 deg | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.1828 | 0.8837 | 0.0921 | 0.0000 |
| val | 0.2635 | 1.0000 | 0.1664 | 0.0000 |
| test | 0.2956 | 1.0000 | 0.1565 | 0.0000 |

## Auxiliary Labels

| split | slip | stall | load_change |
|---|---:|---:|---:|
| train | 102 | 527 | 223 |
| val | 54 | 42 | 74 |
| test | 38 | 92 | 100 |

## Slope Sign Coverage

| split | negative slope | zero slope | positive slope |
|---|---:|---:|---:|
| train | 6990 | 220 | 7079 |
| val | 2347 | 0 | 2568 |
| test | 2337 | 0 | 2139 |

## Theta Supervision Bins

| split | `<-8` | `[-8,-6)` | `[-6,-4)` | `[-4,-2)` | `[-2,0)` | `[0,2)` | `[2,4)` | `[4,6)` | `[6,8)` | `>=8` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 1257 | 1382 | 1295 | 1566 | 1490 | 1559 | 1439 | 1546 | 1209 | 1546 |
| val | 417 | 495 | 679 | 348 | 408 | 593 | 557 | 339 | 573 | 506 |
| test | 558 | 469 | 409 | 417 | 484 | 421 | 424 | 417 | 585 | 292 |
