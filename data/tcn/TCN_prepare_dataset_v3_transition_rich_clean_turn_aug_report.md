# TCN Prepare Dataset Report

- Generated: 2026-05-03 22:29:10
- Source: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_train_data_v3_transition_rich_clean_turn_aug_full.mat`
- Output: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich_clean_turn_aug.mat`
- Split file: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_GRU_shared_run_split_v3_transition_rich_clean_turn_aug.mat`
- Split strategy: `stratified_run_level_v1`
- Split balance score: 0.299801
- Feature contract: `GRU_compatible_observable_19`
- seq_len: 128
- stride: 64
- transition_rich: 1
- steady_stride: 128
- transition_stride: 12
- transition_context_sec: 1.50
- skip_initial_sec: 1.00
- turn_label_strategy: `tail_majority`
- turn_tail_sec: 0.50
- turn_min_purity: 0.70
- turn_ambiguous_weight: 0.60

## Window Counts

| split | windows |
|---|---:|
| train | 16630 |
| val | 3426 |
| test | 3547 |

## Main Labels

| split | flat | stall | slope |
|---|---:|---:|---:|
| train | 8502 | 1142 | 6986 |
| val | 1757 | 274 | 1395 |
| test | 1807 | 270 | 1470 |

## Turn Labels

| split | right | straight | left |
|---|---:|---:|---:|
| train | 3013 | 10517 | 3100 |
| val | 662 | 2030 | 734 |
| test | 735 | 2019 | 793 |

## Main Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.8788 | 0.2000 | 0.2396 | 0.2000 |
| val | 0.8582 | 0.2367 | 0.2790 | 0.2367 |
| test | 0.8905 | 0.1756 | 0.2137 | 0.1756 |

## Turn Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.9492 | 0.0888 | 0.1440 | 0.0745 |
| val | 0.9486 | 0.0905 | 0.1486 | 0.0747 |
| test | 0.9396 | 0.1063 | 0.1717 | 0.0894 |

### Turn Purity By Label

| split | label | windows | mean purity | low purity `<0.8` | transition ratio |
|---|---|---:|---:|---:|---:|
| train | right | 3013 | 0.9258 | 0.1291 | 0.2064 |
| train | straight | 10517 | 0.9635 | 0.0636 | 0.1045 |
| train | left | 3100 | 0.9232 | 0.1352 | 0.2171 |
| val | right | 662 | 0.9382 | 0.1088 | 0.1737 |
| val | straight | 2030 | 0.9591 | 0.0719 | 0.1212 |
| val | left | 734 | 0.9290 | 0.1253 | 0.2016 |
| test | right | 735 | 0.9340 | 0.1184 | 0.1891 |
| test | straight | 2019 | 0.9490 | 0.0896 | 0.1441 |
| test | left | 793 | 0.9207 | 0.1375 | 0.2257 |

## Theta Transition Windows

| split | range mean deg | range p95 deg | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.8102 | 4.4032 | 0.2709 | 0.0000 |
| val | 0.9665 | 5.0840 | 0.2980 | 0.0000 |
| test | 0.6595 | 2.9026 | 0.2783 | 0.0000 |

## Auxiliary Labels

| split | slip | stall | load_change |
|---|---:|---:|---:|
| train | 424 | 1142 | 728 |
| val | 96 | 274 | 144 |
| test | 94 | 270 | 133 |

## Slope Sign Coverage

| split | negative slope | zero slope | positive slope |
|---|---:|---:|---:|
| train | 2819 | 0 | 4167 |
| val | 517 | 0 | 878 |
| test | 593 | 0 | 877 |
