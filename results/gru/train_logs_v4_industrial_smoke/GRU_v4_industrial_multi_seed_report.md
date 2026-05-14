# GRU V4 Industrial Multi-Seed Report

- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- run_tag: `gru_v4_industrial_smoke`
- seeds: `42`
- per-seed CSV: `E:\Matlab\Simulink\S-Function_16\results\gru\train_logs_v4_industrial_smoke\GRU_v4_industrial_multi_seed_summary.csv`
- group CSV: `E:\Matlab\Simulink\S-Function_16\results\gru\train_logs_v4_industrial_smoke\GRU_v4_industrial_group_summary.csv`

## Group Summary

| case_name | n | acc_main_mean | acc_main_std | acc_turn_mean | acc_turn_std | acc_turn_pure_mean | acc_turn_pure_std | acc_turn_transition_mean | acc_turn_transition_std | theta_mae_deg_mean | theta_mae_deg_std | flat_recall_mean | flat_recall_std | stall_recall_mean | stall_recall_std | slope_recall_mean | slope_recall_std | uphill_recall_mean | uphill_recall_std | downhill_recall_mean | downhill_recall_std | flat_as_slope_mean | flat_as_slope_std |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 1 | 0.894969 | 0 | 0.85128 | 0 | 0.926459 | 0 | 0.356386 | 0 | 0.694032 | 0 | 0.913983 | 0 | 0.974528 | 0 | 0.839534 | 0 | 0.751628 | 0 | 0.92128 | 0 | 0.0668182 | 0 |

## Per Seed

| model | case_name | seed | status | best_epoch | train_seconds | acc_main | acc_turn | acc_turn_pure | acc_turn_transition | theta_mae_deg | flat_recall | stall_recall | slope_recall | uphill_recall | downhill_recall | flat_as_slope | hidden_size | num_layers | head_pooling | turn_head_type | turn_head_source | lambda_turn | model_file | meta_file | report_file | error_message |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GRU | baseline | 42 | ok | 1 | 174.89 | 0.894969 | 0.85128 | 0.926459 | 0.356386 | 0.694032 | 0.913983 | 0.974528 | 0.839534 | 0.751628 | 0.92128 | 0.0668182 | 64 | 1 | last_mean | linear | readout | 0.08 | E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_v4_industrial_smoke_baseline_seed42.mat | E:\Matlab\Simulink\S-Function_16\data\models\GRU_meta_gru_v4_industrial_smoke_baseline_seed42.mat | E:\Matlab\Simulink\S-Function_16\results\gru\train_logs_v4_industrial_smoke\baseline_seed42\GRU_train_report.md |  |

## ModernTCN V4 Reference

| model | seed | acc_main | acc_turn | acc_turn_pure | acc_turn_transition | theta_mae_deg | flat_recall | stall_recall | slope_recall | uphill_recall | downhill_recall |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 21 | 0.986687 | 0.952927 | 0.981869 | 0.762409 | 0.486828 | 0.987622 | 0.972062 | 0.989018 | 0.994419 | 0.983997 |
