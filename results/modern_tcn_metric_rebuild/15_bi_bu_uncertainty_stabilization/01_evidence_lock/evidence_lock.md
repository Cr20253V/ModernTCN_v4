# Evidence Lock

This node freezes the current comparison contract before any new training.

## Locked Facts

- baseline: `baseline_lock`
- anchor: `uncertainty_seed101_rerun_20260622`
- baseline J_control: `1.000000`
- anchor J_control: `0.944117`

## Evidence Inventory

| evidence_id | exists | path | size_bytes | sha256 | notes |
| --- | --- | --- | --- | --- | --- |
| baseline_lock_checkpoint | true | E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.pt | 521797 | e72f366f7378db9e7ced49fd950d6e5c8ec4d5e27d7d88e0bd9d19b4ee01f3e0 | frozen baseline checkpoint |
| anchor_checkpoint | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_sci_innovation\01_loss_optimization\uncertainty_seed101_rerun_20260622\modern_tcn_seed101.pt | 524622 | 6ace1ac60b6c3c1e606974b0f00e4f96489871e89d476bf204790447c84cb52d | seed101 anchor checkpoint |
| baseline_matrix | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\03_rerank_existing_experiments\candidate_metric_matrix.csv | 6360 | 5a19fe837612e6547169e10f97b6243053f08741ca5de77535ad8d2341547daf | offline reference metrics |
| stability_report | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\14_uncertainty_stability_optimization\05_decision\uncertainty_stability_final_report.md | 1478 | 6fa0da655afc7806b1b7bc5fbf5557d4ebf5753c32ad61f920888935749532f0 | stability optimization final report |
| tuning_report | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\05_decision\uncertainty_tuning_final_report.md | 758 | b80a75dc054bff7bbf8fdfc98e78dff98d62a1d881792727f10a62c5e3c659b3 | uncertainty tuning final report |
| multiseed_report | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\13_multiseed_algorithm_comparison\03_report\multiseed_algorithm_comparison_report.md | 9606 | 552f8179f8ed874b11c22fcc4cec09716d11641aa34b9e06adc0072225b3e8fd | multiseed comparison report |
| v2_full_thresholds | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\10_threshold_recalibration\hard_constraint_thresholds_v2_full_proposed.json | 381 | 9399406321b0edd3edfac1c95b45a356a61abb32c67c33f3581e430c626d6257 | offline v2 thresholds |
| v2_closed_thresholds | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\10_threshold_recalibration\hard_constraint_thresholds_v2_closed_loop_proposed.json | 382 | 3f5eb295c5bd45ccdfc1330012d185e063a179ebdf01bc578a773c853e0b2caa | closed-loop v2 thresholds |
| formal_path_metrics | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\formal_validation_path_metrics.csv | 7541 | 461f32982598e4e0dd212300d302d4ed0ddfabfd935353f66120a9963798126f | current path-level closed-loop metrics |

## Reference Metrics

| label | candidate_id | J_control | acc_main | acc_turn | acc_turn_transition | theta_mae_deg | theta_edge_p95_abs_err | flat_peak_theta_error | flat_recall | stall_recall | slope_recall | ey_rmse | xy_rmse | epsi_rmse | j_du | omega_cmd_rms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline_lock | baseline_lock | 1 | 0.966962798445308 | 0.578845086063298 | 0.497764530551416 | 0.679394781589508 | 2.75505685806274 | 5.3357400894165 | 0.96957671957672 | 0.71875 | 0.974909090909091 | 0.0340541598964198 | 0.600747319384481 | 0.0395281150431306 | 4.73336252454802 | 0.0725761346213963 |
| anchor_seed101 | uncertainty_seed101_rerun_20260622 | 0.94411711953914 | 0.967518045530261 | 0.58717379233759 | 0.491803278688525 | 0.609225153923035 | 2.27067041397095 | 5.24426937103271 | 0.958994708994709 | 0.697916666666667 | 0.979272727272727 | 0.0296269727303799 | 0.553890709479584 | 0.0379209992142139 | 4.68786764219691 | 0.0710415972600494 |
| stability_14_seed21 | s01_lr13_select_edges_flat_seed21 | 1.14311774157566 | 0.960022209883398 | 0.506662965019434 | 0.451564828614009 | 0.877005279064178 | 2.43688559532166 | 7.10931348800659 | 0.933862433862434 | 0.6875 | 0.976727272727273 | 0.0330587894326381 | 0.669326838938871 | 0.0422486992278023 | 7.32090196230489 | 0.0736774256778956 |
| stability_14_seed42 | s01_lr13_select_edges_flat_seed42 | 1.17496689656309 | 0.967240421987785 | 0.564408661854525 | 0.497764530551416 | 0.875044822692871 | 3.42140817642212 | 5.89323759078979 | 0.94047619047619 | 0.697916666666667 | 0.984 | 0.040252955137561 | 0.814128733685958 | 0.0533604549648976 | 4.40231959021702 | 0.0767576173370662 |
| stability_14_seed101 | uncertainty_seed101_rerun_20260622 | 0.94411711953914 | 0.967518045530261 | 0.58717379233759 | 0.491803278688525 | 0.609225153923035 | 2.27067041397095 | 5.24426937103271 | 0.958994708994709 | 0.697916666666667 | 0.979272727272727 | 0.0296269727303799 | 0.553890709479584 | 0.0379209992142139 | 4.68786764219691 | 0.0710415972600494 |
