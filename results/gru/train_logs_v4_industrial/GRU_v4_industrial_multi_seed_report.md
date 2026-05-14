# GRU V4 Industrial Multi-Seed Report

- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- run_tag: `gru_v4_industrial`
- seeds: `101`
- per-seed CSV: `E:\Matlab\Simulink\S-Function_16\results\gru\train_logs_v4_industrial\GRU_v4_industrial_multi_seed_summary.csv`
- group CSV: `E:\Matlab\Simulink\S-Function_16\results\gru\train_logs_v4_industrial\GRU_v4_industrial_group_summary.csv`

## Group Summary

| case_name | n | acc_main_mean | acc_main_std | acc_turn_mean | acc_turn_std | acc_turn_pure_mean | acc_turn_pure_std | acc_turn_transition_mean | acc_turn_transition_std | theta_mae_deg_mean | theta_mae_deg_std | flat_recall_mean | flat_recall_std | stall_recall_mean | stall_recall_std | slope_recall_mean | slope_recall_std | uphill_recall_mean | uphill_recall_std | downhill_recall_mean | downhill_recall_std | flat_as_slope_mean | flat_as_slope_std |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| inputstats_hidden96 | 1 | 0.970874 | 0 | 0.94469 | 0 | 0.977379 | 0 | 0.729504 | 0 | 0.327752 | 0 | 0.965896 | 0 | 0.977814 | 0 | 0.977813 | 0 | 0.976279 | 0 | 0.979239 | 0 | 0.0287988 | 0 |

## Per Seed

| model | case_name | seed | status | best_epoch | train_seconds | acc_main | acc_turn | acc_turn_pure | acc_turn_transition | theta_mae_deg | flat_recall | stall_recall | slope_recall | uphill_recall | downhill_recall | flat_as_slope | hidden_size | num_layers | head_pooling | turn_head_type | turn_head_source | lambda_turn | model_file | meta_file | report_file | error_message |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GRU | inputstats_hidden96 | 101 | ok | 59 | 11500.9 | 0.970874 | 0.94469 | 0.977379 | 0.729504 | 0.327752 | 0.965896 | 0.977814 | 0.977813 | 0.976279 | 0.979239 | 0.0287988 | 96 | 1 | last_mean_inputstats | mlp | inputstats | 0.08 | E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_v4_industrial_inputstats_hidden96_seed101.mat | E:\Matlab\Simulink\S-Function_16\data\models\GRU_meta_gru_v4_industrial_inputstats_hidden96_seed101.mat | E:\Matlab\Simulink\S-Function_16\results\gru\train_logs_v4_industrial\inputstats_hidden96_seed101\GRU_train_report.md |  |

## ModernTCN V4 Reference

| model | seed | acc_main | acc_turn | acc_turn_pure | acc_turn_transition | theta_mae_deg | flat_recall | stall_recall | slope_recall | uphill_recall | downhill_recall |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 21 | 0.986687 | 0.952927 | 0.981869 | 0.762409 | 0.486828 | 0.987622 | 0.972062 | 0.989018 | 0.994419 | 0.983997 |
