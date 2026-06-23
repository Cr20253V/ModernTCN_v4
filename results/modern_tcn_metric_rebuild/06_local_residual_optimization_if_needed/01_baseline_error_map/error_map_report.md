# Phase B1 Baseline Error Map

- checkpoint: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.pt`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- samples: `3602`
- flat_peak_cutoff_deg: `1.8001`

## Recomputed Aggregate Metrics

- acc_main: `0.966963`
- acc_turn: `0.578845`
- acc_turn_transition: `0.497765`
- theta_mae_deg: `0.679494`
- flat_recall: `0.969577`
- stall_recall: `0.718750`
- slope_recall: `0.974909`
- theta_edge_p95_abs_err_deg: `2.755614`
- flat_peak_theta_error_deg: `5.336414`

## Error Concentration

- overall main error rate: `0.0330`
- overall turn error rate: `0.4212`
- transition window share: `0.1863`
- slope-edge share: `0.1918`
- flat-peak share: `0.0105`
- top-50 transition share: `0.1000`
- top-50 slope-edge share: `0.0600`
- top-50 flat-peak share: `0.0200`

## Top Theta Errors

| sample_id | run_id | theta_abs_err_deg | transition | slope_edge | flat_peak | main_err | turn_err |
|---|---|---:|---:|---:|---:|---:|---:|
| test_02532 | 27 | 8.6007 | 0 | 0 | 0 | 0 | 0 |
| test_00026 | 27 | 8.4785 | 0 | 0 | 0 | 0 | 0 |
| test_00737 | 27 | 8.3705 | 0 | 0 | 0 | 0 | 0 |
| test_02436 | 27 | 8.0568 | 0 | 0 | 0 | 0 | 0 |
| test_01367 | 3 | 7.9311 | 1 | 0 | 0 | 1 | 1 |
| test_02673 | 3 | 7.7296 | 0 | 0 | 0 | 1 | 0 |
| test_01117 | 3 | 7.6867 | 0 | 0 | 0 | 1 | 1 |
| test_01028 | 3 | 7.6108 | 0 | 0 | 0 | 1 | 0 |
| test_02294 | 3 | 7.5806 | 0 | 0 | 0 | 1 | 0 |
| test_02180 | 27 | 7.4134 | 0 | 0 | 0 | 0 | 0 |

## Initial Read

- B1 is ready for residual design only if the top-error mass is concentrated in one or two flags.
- If transition windows dominate, residual turn correction is the primary branch.
- If slope-edge or flat-peak windows dominate, residual theta correction is the primary branch.
- If both patterns remain strong, a head-specific physics residual is the better next step.