# ModernTCN State Classifier Standalone Test

- seed: `73`
- run_id: `25`
- scene: `path_train_tcn_v3_07_slope_left_turn_combo`
- data: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_train_data_v3_transition_rich_full.mat`
- steps: `900`
- warmup_steps: `228`
- pass: `1`

| check | pass |
|---|---:|
| labels in valid ranges | 1 |
| finite outputs | 1 |
| has post-warmup samples | 1 |
| ONNX inference observed | 1 |
| post-warmup output changed from default | 1 |

## Last Samples

| step | t | main | turn | conf | theta deg | predict | buffer | truth main | truth turn |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 891 | 8.90 | 3 | 0 | 1.0000 | 4.4834 | 1 | 128 | 3 | 1 |
| 892 | 8.91 | 3 | 0 | 1.0000 | 4.4769 | 1 | 128 | 3 | 1 |
| 893 | 8.92 | 3 | 0 | 1.0000 | 4.4708 | 1 | 128 | 3 | 1 |
| 894 | 8.93 | 3 | 0 | 1.0000 | 4.4653 | 1 | 128 | 3 | 1 |
| 895 | 8.94 | 3 | 0 | 1.0000 | 4.4598 | 1 | 128 | 3 | 1 |
| 896 | 8.95 | 3 | 0 | 1.0000 | 4.4545 | 1 | 128 | 3 | 1 |
| 897 | 8.96 | 3 | 0 | 1.0000 | 4.4488 | 1 | 128 | 3 | 1 |
| 898 | 8.97 | 3 | 0 | 1.0000 | 4.4433 | 1 | 128 | 3 | 1 |
| 899 | 8.98 | 3 | 0 | 1.0000 | 4.4379 | 1 | 128 | 3 | 1 |
| 900 | 8.99 | 3 | 0 | 1.0000 | 4.4331 | 1 | 128 | 3 | 1 |
