# Legacy GRU/TCN New Metric Evaluation

- Scope: add previous GRU and TCN seed101 closed-loop comparators to the frozen metric rebuild view.
- Output root: `results/modern_tcn_metric_rebuild/08_legacy_tcn_gru_new_metric/`
- GRU/TCN source: legacy three-path closed-loop comparison `dual_modern_seed101_full`.
- ModernTCN rerun source: Window 2 formal validation over the frozen three-path set.
- Missing policy: no zero fill, no baseline fill; unavailable metrics remain NaN and are counted.
- Class C rule: legacy GRU/TCN have the same path set but not the same Window 2 formal protocol, so they are context comparators only.

## Final Five-Algorithm Results

| algorithm | J_control | hard status | rank J | closed-loop ey | xy | epsi | j_du | omega_rms | offline vFinal | decision |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| `uncertainty_seed101_rerun_20260622` | 0.944117 | fail | 1 | 0.029627 | 0.553891 | 0.037921 | 4.687868 | 0.071042 | 0.363054 | no_promotion_hard_constraint_fail |
| `baseline_lock` | 1.000000 | pass | 2 | 0.034054 | 0.600747 | 0.039528 | 4.733363 | 0.072576 | 0.000000 | reference_kept |
| `mode_theta_detach_flatreg001_seed21_rerun_20260622` | 1.106111 | fail | 3 | 0.046238 | 0.658360 | 0.041831 | 4.867199 | 0.071877 | 0.406913 | no_promotion_hard_constraint_fail |
| `GRU_seed101` | 37.084521 | fail | 4 | 0.939034 | 4.853168 | 0.191465 | 659.980603 | 0.398726 | 0.456922 | legacy_comparator_not_class_c; use_for_context_only |
| `TCN_seed101` | 80.285338 | fail | 5 | 5.263786 | 9.048955 | 0.339893 | 1029.155871 | 0.418630 | 0.653576 | legacy_comparator_not_class_c; use_for_context_only |

## Hard-Constraint Detail

| algorithm | hard status | failures | unavailable | same protocol |
|---|---|---|---|---:|
| `baseline_lock` | pass | reference_baseline | none | 1 |
| `uncertainty_seed101_rerun_20260622` | fail | closed_loop_main_acc_drop=0.0200623 | none | 1 |
| `mode_theta_detach_flatreg001_seed21_rerun_20260622` | fail | stall_recall_drop=0.0520833; flat_peak_theta_error_ratio=1.13741 | none | 1 |
| `GRU_seed101` | fail | closed_loop_main_acc_drop=0.026663; stall_recall_drop=0.0833333; flat_peak_theta_error_ratio=1.0911; omega_cmd_rms_ratio=5.4939; delta_u_proxy_ratio=139.432 | none | 0 |
| `TCN_seed101` | fail | closed_loop_main_acc_drop=0.155993; offline_acc_main_drop=0.222932; stall_recall_drop=0.1875; slope_recall_drop=0.144364; theta_edge_p95_ratio=1.48084; flat_peak_theta_error_ratio=1.22281; omega_cmd_rms_ratio=5.76814; delta_u_proxy_ratio=217.426 | none | 0 |

## Parameter Snapshot

| algorithm | family | seed | role | key parameters | artifact |
|---|---|---:|---|---|---|
| `baseline_lock` | ModernTCN_small | 101 | reference_baseline | channels=64; blocks=5; kernel_size=31; dropout=0.15; lambda_turn=0.20; lambda_theta=0.55; lambda_theta_flat=0.12; turn_transition_weight=2.5; turn_class_multipliers=[1.4,0.8,1.4] | `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.pt` |
| `uncertainty_seed101_rerun_20260622` | ModernTCN_small | 101 | rerun_candidate | loss_mode=uncertainty_weighting; channels=64; blocks=5; kernel_size=31; dropout=0.15; lambda_turn=0.2; lambda_theta=0.55; lambda_theta_flat=0.12; turn_transition_weight=2.5; main_neg_slope_weight=2.0; turn_class_multipliers=[1.4, 0.8, 1.4]; weight_main=26.0... | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_sci_innovation\01_loss_optimization\uncertainty_seed101_rerun_20260622\modern_tcn_seed101.pt` |
| `mode_theta_detach_flatreg001_seed21_rerun_20260622` | ModernTCNModeTheta | 21 | rerun_candidate | loss_mode=fixed; channels=64; blocks=5; kernel_size=31; dropout=0.15; lambda_turn=0.2; lambda_theta=0.55; lambda_theta_flat=0.12; turn_transition_weight=2.5; main_neg_slope_weight=2.0; turn_class_multipliers=[1.4, 0.8, 1.4]; weight_main=NaN; weight_turn=NaN... | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_sci_innovation\04_mode_conditioned_theta\mode_theta_detach_flatreg001_seed21_rerun_20260622\modern_tcn_mode_theta_seed21.pt` |
| `GRU_seed101` | GRU | 101 | legacy_closed_loop_comparator | mode=physics_guided; max_epochs=140; batch_size=128; dropout=0.2; best_metric=composite; base_best_metric=composite; lambda_turn=0.08; lambda_theta=0.55; lambda_theta_flat=0.12; turn_head=mlp/inputstats; turn_head_hidden=64; turn_class_multipliers=[1.08 1. ... | `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\models\GRU_model_full_gru_v5_plantfix_passive17_plus_all5_seed101.mat` |
| `TCN_seed101` | TCN | 101 | legacy_closed_loop_comparator | mode=physics_guided; max_epochs=140; batch_size=128; dropout=0.15; best_metric=turn_priority; base_best_metric=composite; lambda_turn=0.08; lambda_theta=0.55; lambda_theta_flat=0.12; turn_head=mlp/inputstats; turn_head_hidden=64; turn_class_multipliers=[1.0... | `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\models\TCN_model_full_tcn_v5_plantfix_passive17_plus_all5_seed101.mat` |

## Interpretation

- `uncertainty_seed101_rerun_20260622` has the best numeric J_control, but it fails hard protection through main-accuracy drop.
- `mode_theta_detach_flatreg001_seed21_rerun_20260622` passes the Window 2 control checks but is not better than baseline on J_control; under the fuller frozen hard-protection view it also shows offline protection failures.
- `GRU_seed101` and `TCN_seed101` remain useful historical comparators, but both fail the new hard constraints and are not eligible for Class C in this contract.
- `baseline_lock` remains the retained reference.
