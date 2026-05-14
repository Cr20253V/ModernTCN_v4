# TCN Prepare Dataset Report

- Generated: 2026-04-26 01:19:17
- Source: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_train_data_full.mat`
- Output: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- Split file: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_GRU_shared_run_split.mat`
- Split strategy: `stratified_run_level_v1`
- Split balance score: 0.872160
- Feature contract: `GRU_compatible_observable_19`
- seq_len: 128
- stride: 64
- skip_initial_sec: 1.00
- turn_label_strategy: `tail_majority`
- turn_tail_sec: 0.50
- turn_min_purity: 0.70
- turn_ambiguous_weight: 0.50

## Window Counts

| split | windows |
|---|---:|
| train | 1875 |
| val | 424 |
| test | 445 |

## Main Labels

| split | flat | stall | slope |
|---|---:|---:|---:|
| train | 1222 | 72 | 581 |
| val | 266 | 16 | 142 |
| test | 265 | 18 | 162 |

## Turn Labels

| split | right | straight | left |
|---|---:|---:|---:|
| train | 295 | 1278 | 302 |
| val | 89 | 243 | 92 |
| test | 72 | 291 | 82 |

## Turn Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.9758 | 0.0421 | 0.0699 | 0.0341 |
| val | 0.9692 | 0.0590 | 0.0755 | 0.0377 |
| test | 0.9658 | 0.0629 | 0.0921 | 0.0449 |

### Turn Purity By Label

| split | label | windows | mean purity | low purity `<0.8` | transition ratio |
|---|---|---:|---:|---:|---:|
| train | right | 295 | 0.9596 | 0.0712 | 0.1186 |
| train | straight | 1278 | 0.9822 | 0.0290 | 0.0516 |
| train | left | 302 | 0.9644 | 0.0695 | 0.0993 |
| val | right | 89 | 0.9700 | 0.0674 | 0.0674 |
| val | straight | 243 | 0.9715 | 0.0494 | 0.0700 |
| val | left | 92 | 0.9625 | 0.0761 | 0.0978 |
| test | right | 72 | 0.9377 | 0.1250 | 0.1528 |
| test | straight | 291 | 0.9793 | 0.0378 | 0.0584 |
| test | left | 82 | 0.9425 | 0.0976 | 0.1585 |

## Auxiliary Labels

| split | slip | stall | load_change |
|---|---:|---:|---:|
| train | 57 | 72 | 71 |
| val | 13 | 16 | 14 |
| test | 11 | 18 | 16 |

## Slope Sign Coverage

| split | negative slope | zero slope | positive slope |
|---|---:|---:|---:|
| train | 149 | 0 | 432 |
| val | 29 | 0 | 113 |
| test | 29 | 0 | 133 |
