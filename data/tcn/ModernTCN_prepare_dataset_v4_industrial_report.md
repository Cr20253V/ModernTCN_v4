# TCN Prepare Dataset Report

- Generated: 2026-05-05 03:26:01
- Source: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_train_data_v4_industrial.mat`
- Output: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- Split file: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_shared_run_split_v4_industrial.mat`
- Split strategy: `stratified_run_level_v1`
- Split balance score: 0.099242
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
| train | 63022 |
| val | 13141 |
| test | 13596 |

## Main Labels

| split | flat | stall | slope |
|---|---:|---:|---:|
| train | 36571 | 5947 | 20504 |
| val | 7578 | 1219 | 4344 |
| test | 7917 | 1217 | 4462 |

## Turn Labels

| split | right | straight | left |
|---|---:|---:|---:|
| train | 10133 | 42530 | 10359 |
| val | 2122 | 8814 | 2205 |
| test | 2261 | 9224 | 2111 |

## Main Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.9012 | 0.1583 | 0.1945 | 0.1583 |
| val | 0.8966 | 0.1655 | 0.2036 | 0.1655 |
| test | 0.9003 | 0.1595 | 0.1967 | 0.1595 |

## Turn Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.9540 | 0.0812 | 0.1296 | 0.0687 |
| val | 0.9551 | 0.0795 | 0.1260 | 0.0670 |
| test | 0.9531 | 0.0827 | 0.1319 | 0.0700 |

### Turn Purity By Label

| split | label | windows | mean purity | low purity `<0.8` | transition ratio |
|---|---|---:|---:|---:|---:|
| train | right | 10133 | 0.9265 | 0.1298 | 0.2063 |
| train | straight | 42530 | 0.9666 | 0.0589 | 0.0939 |
| train | left | 10359 | 0.9289 | 0.1251 | 0.2013 |
| val | right | 2122 | 0.9266 | 0.1291 | 0.2069 |
| val | straight | 8814 | 0.9677 | 0.0575 | 0.0908 |
| val | left | 2205 | 0.9320 | 0.1197 | 0.1891 |
| test | right | 2261 | 0.9275 | 0.1287 | 0.2048 |
| test | straight | 9224 | 0.9659 | 0.0596 | 0.0945 |
| test | left | 2111 | 0.9246 | 0.1345 | 0.2170 |

## Theta Transition Windows

| split | range mean deg | range p95 deg | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.5182 | 2.4456 | 0.2305 | 0.0000 |
| val | 0.5546 | 2.5240 | 0.2489 | 0.0000 |
| test | 0.4934 | 2.2684 | 0.2291 | 0.0000 |

## Auxiliary Labels

| split | slip | stall | load_change |
|---|---:|---:|---:|
| train | 2467 | 5947 | 4303 |
| val | 525 | 1219 | 1046 |
| test | 580 | 1217 | 1012 |

## Slope Sign Coverage

| split | negative slope | zero slope | positive slope |
|---|---:|---:|---:|
| train | 10227 | 0 | 10277 |
| val | 2047 | 0 | 2297 |
| test | 2312 | 0 | 2150 |
