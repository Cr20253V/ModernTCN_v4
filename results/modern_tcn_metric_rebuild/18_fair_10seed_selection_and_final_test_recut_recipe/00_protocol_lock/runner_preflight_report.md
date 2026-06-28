# Runner Preflight

- can_start: `True`
- validation_paths_disjoint: `True`
- seeds: `1, 7, 11, 21, 42, 73, 101, 202, 340, 520`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`

## Required Paths

| label | exists | path | size_bytes | sha256 |
| --- | --- | --- | --- | --- |
| train_script | true | E:\Matlab\Simulink\S-Function_16\src\ModernTCN\train_modern_tcn.py | 102631 | 84a68e9da4ddeab9deaf77ec7c8b2c6572fc1400fab03d1e6f40e4070bbd3c82 |
| export_script | true | E:\Matlab\Simulink\S-Function_16\src\ModernTCN\export_modern_tcn_onnx.py | 4999 | 467374076babe6e3643ffed36f0e2aae3fb18352dd0cbbde9b7e12677fd278bb |
| check_onnx_script | true | E:\Matlab\Simulink\S-Function_16\src\ModernTCN\check_onnxruntime_consistency.py | 4198 | 688889b4d36ce5127a9152074c363763ea3f77728bea95f8015481d507ce318f |
| run_closed_loop_m | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\run_fair10_closed_loop.m | 10410 | c7e923b989adf447d4da4f15f50dbcb687e839c4d4f0388f1b22c4d931142055 |
| robustness_m | true | E:\Matlab\Simulink\S-Function_16\src\Compare\run_closed_loop_robustness_experiment.m | 20213 | 1a9736f8c2a18761a1181bef106c3bc550dd46453806bf2c23bef33e2eded430 |
| baseline_matrix | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\03_rerank_existing_experiments\candidate_metric_matrix.csv | 6360 | 5a19fe837612e6547169e10f97b6243053f08741ca5de77535ad8d2341547daf |
| dataset_file | true | E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat | 446285336 | ab5dde32ef3627aa7032a3b4f7632c87cb471287a638f2b14a25a179a660196f |

## Validation Paths

| path_file | exists | baseline_out | baseline_out_exists |
| --- | --- | --- | --- |
| E:\Matlab\Simulink\S-Function_16\data\paths\agv_theta10_uniform_v2\agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16.mat | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16\baseline_lock_out.mat | true |
| E:\Matlab\Simulink\S-Function_16\data\paths\agv_theta10_uniform_v2\agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06.mat | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06\baseline_lock_out.mat | true |

## Final Paths

| path_file | exists | baseline_out | baseline_out_exists |
| --- | --- | --- | --- |
| E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v10.mat | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_logistics_showcase_theta10_v10\baseline_lock_out.mat | true |
| E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_sharp_turn_transition_theta10_v1.mat | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_sharp_turn_transition_theta10_v1\baseline_lock_out.mat | true |
| E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_long_updown_theta10_v1.mat | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_long_updown_theta10_v1\baseline_lock_out.mat | true |
| E:\Matlab\Simulink\S-Function_16\data\paths\modern_tcn_showcase\candidates\path_modern_tcn_showcase_candidate_soft_updown_straight_turn_v1.mat | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_modern_tcn_showcase_candidate_soft_updown_straight_turn_v1\baseline_lock_out.mat | true |

## Missing Baseline Outputs

- none
