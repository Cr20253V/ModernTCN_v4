# GRU State Classifier Standalone Test

- seed: `101`
- run_id: `1`
- scene: `path_modern_tcn_v4_01_v4_flat_straight_v08`
- model: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_v4_industrial_inputstats_hidden96_seed101.mat`
- raw data: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_train_data_v4_industrial.mat`
- steps: `420`
- seq_len: `128`
- pass: `1`

| check | pass |
|---|---:|
| labels in valid ranges | 1 |
| finite outputs | 1 |
| buffer reached seq_len | 1 |

- online main acc after warmup: `0.8601`
- online turn acc after warmup: `1.0000`

## Last Samples

| step | t | main | turn | conf | theta deg | buffer | truth main | truth turn |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 411 | 4.10 | 1 | 0 | 0.9906 | 0.0000 | 128 | 1 | 0 |
| 412 | 4.11 | 1 | 0 | 0.9906 | 0.0000 | 128 | 1 | 0 |
| 413 | 4.12 | 1 | 0 | 0.9906 | 0.0000 | 128 | 1 | 0 |
| 414 | 4.13 | 1 | 0 | 0.9906 | 0.0000 | 128 | 1 | 0 |
| 415 | 4.14 | 1 | 0 | 0.9906 | 0.0000 | 128 | 1 | 0 |
| 416 | 4.15 | 1 | 0 | 0.9906 | 0.0000 | 128 | 1 | 0 |
| 417 | 4.16 | 1 | 0 | 0.9906 | 0.0000 | 128 | 1 | 0 |
| 418 | 4.17 | 1 | 0 | 0.9906 | 0.0000 | 128 | 1 | 0 |
| 419 | 4.18 | 1 | 0 | 0.9906 | 0.0000 | 128 | 1 | 0 |
| 420 | 4.19 | 1 | 0 | 0.9906 | 0.0000 | 128 | 1 | 0 |
