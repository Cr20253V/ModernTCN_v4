# Replay Contract Audit

- generated_at: 2026-06-22T01:32:31
- dataset_file: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- repair_status: `PASS_CONTRACT_LIMITED`
- metric_rebuild_can_continue: True

## Split Metadata Levels

| split | metadata_level | rows | reason |
|---|---|---:|---|
| train | `level0_invalid` | 16529 | run_id exists, but window_start_idx/window_end_idx are absent |
| val | `level0_invalid` | 3695 | run_id exists, but window_start_idx/window_end_idx are absent |
| test | `level0_invalid` | 3602 | run_id exists, but window_start_idx/window_end_idx are absent |

## Missing Or Non-Per-Window Fields

| split | field | repair_needed | notes |
|---|---|---|---|
| train | `sample_id` | True | missing from current dataset contract |
| train | `segment_id` | True | missing from current dataset contract |
| train | `window_start_idx` | True | missing from current dataset contract |
| train | `window_end_idx` | True | missing from current dataset contract |
| train | `global_time_idx` | True | missing from current dataset contract |
| train | `sample_time` | True | missing from current dataset contract |
| train | `split` | True | split is implicit in *_train/val/test arrays, not stored as per-window metadata |
| train | `path_id` | True | run-level source exists, but no per-window replay metadata links it safely |
| train | `scenario_id` | True | run-level source exists, but no per-window replay metadata links it safely |
| train | `is_contiguous_next` | True | missing from current dataset contract |
| val | `sample_id` | True | missing from current dataset contract |
| val | `segment_id` | True | missing from current dataset contract |
| val | `window_start_idx` | True | missing from current dataset contract |
| val | `window_end_idx` | True | missing from current dataset contract |
| val | `global_time_idx` | True | missing from current dataset contract |
| val | `sample_time` | True | missing from current dataset contract |
| val | `split` | True | split is implicit in *_train/val/test arrays, not stored as per-window metadata |
| val | `path_id` | True | run-level source exists, but no per-window replay metadata links it safely |
| val | `scenario_id` | True | run-level source exists, but no per-window replay metadata links it safely |
| val | `is_contiguous_next` | True | missing from current dataset contract |
| test | `sample_id` | True | missing from current dataset contract |
| test | `segment_id` | True | missing from current dataset contract |
| test | `window_start_idx` | True | missing from current dataset contract |
| test | `window_end_idx` | True | missing from current dataset contract |
| test | `global_time_idx` | True | missing from current dataset contract |
| test | `sample_time` | True | missing from current dataset contract |
| test | `split` | True | split is implicit in *_train/val/test arrays, not stored as per-window metadata |
| test | `path_id` | True | run-level source exists, but no per-window replay metadata links it safely |
| test | `scenario_id` | True | run-level source exists, but no per-window replay metadata links it safely |
| test | `is_contiguous_next` | True | missing from current dataset contract |
