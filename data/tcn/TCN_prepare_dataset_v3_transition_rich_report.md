# TCN Prepare Dataset Report

- Generated: 2026-05-03 18:49:10
- Source: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_train_data_v3_transition_rich_full.mat`
- Output: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`
- Split file: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_GRU_shared_run_split_v3_transition_rich.mat`
- Split strategy: `stratified_run_level_v1`
- Split balance score: 0.487638
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
| train | 15819 |
| val | 3280 |
| test | 3316 |

## Main Labels

| split | flat | stall | slope |
|---|---:|---:|---:|
| train | 7687 | 1119 | 7013 |
| val | 1658 | 286 | 1336 |
| test | 1533 | 281 | 1502 |

## Turn Labels

| split | right | straight | left |
|---|---:|---:|---:|
| train | 3050 | 9883 | 2886 |
| val | 791 | 1950 | 539 |
| test | 569 | 2081 | 666 |

## Main Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.8742 | 0.2080 | 0.2492 | 0.2080 |
| val | 0.8472 | 0.2527 | 0.2985 | 0.2527 |
| test | 0.8797 | 0.1930 | 0.2346 | 0.1930 |

## Turn Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.9489 | 0.0894 | 0.1444 | 0.0749 |
| val | 0.9502 | 0.0884 | 0.1433 | 0.0732 |
| test | 0.9482 | 0.0902 | 0.1475 | 0.0757 |

### Turn Purity By Label

| split | label | windows | mean purity | low purity `<0.8` | transition ratio |
|---|---|---:|---:|---:|---:|
| train | right | 3050 | 0.9270 | 0.1279 | 0.2043 |
| train | straight | 9883 | 0.9629 | 0.0649 | 0.1055 |
| train | left | 2886 | 0.9242 | 0.1331 | 0.2145 |
| val | right | 791 | 0.9384 | 0.1087 | 0.1745 |
| val | straight | 1950 | 0.9594 | 0.0723 | 0.1179 |
| val | left | 539 | 0.9342 | 0.1169 | 0.1892 |
| test | right | 569 | 0.9267 | 0.1265 | 0.2021 |
| test | straight | 2081 | 0.9629 | 0.0644 | 0.1091 |
| test | left | 666 | 0.9210 | 0.1396 | 0.2207 |

## Theta Transition Windows

| split | range mean deg | range p95 deg | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.8414 | 4.4486 | 0.2888 | 0.0000 |
| val | 1.0384 | 5.0662 | 0.3345 | 0.0000 |
| test | 0.7263 | 3.6392 | 0.2557 | 0.0000 |

## Auxiliary Labels

| split | slip | stall | load_change |
|---|---:|---:|---:|
| train | 415 | 1119 | 677 |
| val | 103 | 286 | 161 |
| test | 96 | 281 | 167 |

## Slope Sign Coverage

| split | negative slope | zero slope | positive slope |
|---|---:|---:|---:|
| train | 2804 | 0 | 4209 |
| val | 545 | 0 | 791 |
| test | 580 | 0 | 922 |
