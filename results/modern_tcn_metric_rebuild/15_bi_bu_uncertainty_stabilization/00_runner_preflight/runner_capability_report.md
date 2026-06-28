# BI-BU Runner Capability Preflight

- node_root: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\15_bi_bu_uncertainty_stabilization`
- can_start: `True`

## Required Paths

| label | exists | path | size_bytes | sha256 |
| --- | --- | --- | --- | --- |
| train_script | true | E:\Matlab\Simulink\S-Function_16\src\ModernTCN\train_modern_tcn.py | 102631 | 84a68e9da4ddeab9deaf77ec7c8b2c6572fc1400fab03d1e6f40e4070bbd3c82 |
| baseline_checkpoint | true | E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.pt | 521797 | e72f366f7378db9e7ced49fd950d6e5c8ec4d5e27d7d88e0bd9d19b4ee01f3e0 |
| anchor_checkpoint | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_sci_innovation\01_loss_optimization\uncertainty_seed101_rerun_20260622\modern_tcn_seed101.pt | 524622 | 6ace1ac60b6c3c1e606974b0f00e4f96489871e89d476bf204790447c84cb52d |
| baseline_matrix | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\03_rerank_existing_experiments\candidate_metric_matrix.csv | 6360 | 5a19fe837612e6547169e10f97b6243053f08741ca5de77535ad8d2341547daf |
| v2_full_thresholds | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\10_threshold_recalibration\hard_constraint_thresholds_v2_full_proposed.json | 381 | 9399406321b0edd3edfac1c95b45a356a61abb32c67c33f3581e430c626d6257 |
| v2_closed_thresholds | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\10_threshold_recalibration\hard_constraint_thresholds_v2_closed_loop_proposed.json | 382 | 3f5eb295c5bd45ccdfc1330012d185e063a179ebdf01bc578a773c853e0b2caa |
| formal_path_metrics | true | E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\formal_validation_path_metrics.csv | 7541 | 461f32982598e4e0dd212300d302d4ed0ddfabfd935353f66120a9963798126f |

## Capability Check

- `--init-checkpoint`: supported in `train_modern_tcn.py`.
- `--freeze-mode`: supported in `train_modern_tcn.py`.
- bounded uncertainty: supported in `train_modern_tcn.py`.
- preservation loss: supported in `train_modern_tcn.py`.
- `--no-overwrite`: supported in `train_modern_tcn.py`.
- zero-epoch equivalence: `True`.
