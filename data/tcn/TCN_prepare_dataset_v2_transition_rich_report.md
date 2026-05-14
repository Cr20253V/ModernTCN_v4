# TCN Prepare Dataset Report

- Generated: 2026-04-28 16:39:04
- Source: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_train_data_full.mat`
- Output: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v2_transition_rich.mat`
- Split file: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_GRU_shared_run_split_v2_transition_rich.mat`
- Split strategy: `stratified_run_level_v1`
- Split balance score: 1.356405
- Feature contract: `GRU_compatible_observable_19`
- seq_len: 128
- stride: 64
- transition_rich: 1
- steady_stride: 128
- transition_stride: 16
- transition_context_sec: 1.00
- skip_initial_sec: 1.00
- turn_label_strategy: `tail_majority`
- turn_tail_sec: 0.50
- turn_min_purity: 0.70
- turn_ambiguous_weight: 0.50

## Window Counts

| split | windows |
|---|---:|
| train | 3979 |
| val | 844 |
| test | 968 |

## Main Labels

| split | flat | stall | slope |
|---|---:|---:|---:|
| train | 2130 | 299 | 1550 |
| val | 467 | 65 | 312 |
| test | 573 | 78 | 317 |

## Turn Labels

| split | right | straight | left |
|---|---:|---:|---:|
| train | 758 | 2596 | 625 |
| val | 117 | 594 | 133 |
| test | 115 | 701 | 152 |

## Main Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.8818 | 0.2013 | 0.2380 | 0.2013 |
| val | 0.8495 | 0.2737 | 0.3092 | 0.2737 |
| test | 0.8593 | 0.2521 | 0.2882 | 0.2521 |

## Turn Window Purity

| split | mean purity | low purity `<0.8` | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.9491 | 0.0890 | 0.1458 | 0.0744 |
| val | 0.9577 | 0.0746 | 0.1220 | 0.0628 |
| test | 0.9536 | 0.0816 | 0.1250 | 0.0692 |

### Turn Purity By Label

| split | label | windows | mean purity | low purity `<0.8` | transition ratio |
|---|---|---:|---:|---:|---:|
| train | right | 758 | 0.9237 | 0.1332 | 0.2177 |
| train | straight | 2596 | 0.9643 | 0.0605 | 0.1029 |
| train | left | 625 | 0.9166 | 0.1536 | 0.2368 |
| val | right | 117 | 0.9276 | 0.1282 | 0.2051 |
| val | straight | 594 | 0.9716 | 0.0488 | 0.0825 |
| val | left | 133 | 0.9222 | 0.1429 | 0.2256 |
| test | right | 115 | 0.8997 | 0.1739 | 0.2696 |
| test | straight | 701 | 0.9715 | 0.0485 | 0.0742 |
| test | left | 152 | 0.9121 | 0.1645 | 0.2500 |

## Theta Transition Windows

| split | range mean deg | range p95 deg | transition ratio | downweighted ratio |
|---|---:|---:|---:|---:|
| train | 0.7901 | 4.9050 | 0.1915 | 0.1915 |
| val | 1.0167 | 5.6953 | 0.2429 | 0.2429 |
| test | 0.9848 | 5.6248 | 0.2242 | 0.2242 |

## Auxiliary Labels

| split | slip | stall | load_change |
|---|---:|---:|---:|
| train | 85 | 299 | 96 |
| val | 15 | 65 | 32 |
| test | 21 | 78 | 22 |

## Slope Sign Coverage

| split | negative slope | zero slope | positive slope |
|---|---:|---:|---:|
| train | 375 | 0 | 1175 |
| val | 68 | 0 | 244 |
| test | 94 | 0 | 223 |
