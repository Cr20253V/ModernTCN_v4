# Strict GRU/TCN New Metric Evaluation

- Scope: GRU/TCN re-run under the Window 2 closed-loop shell and frozen three-path set.
- Output root: `results/modern_tcn_metric_rebuild/09_strict_gru_tcn_validation/`
- Missing policy: no zero fill, no baseline fill; unavailable metrics remain NaN and are counted.

## Final Five-Algorithm Results

| algorithm | J_control | hard status | rank J | ey | xy | epsi | j_du | omega_rms | offline vFinal | decision |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| `uncertainty_seed101_rerun_20260622` | 0.944117 | fail | 1 | 0.029627 | 0.553891 | 0.037921 | 4.687868 | 0.071042 | 0.363054 | no_promotion_hard_constraint_fail |
| `baseline_lock` | 1.000000 | pass | 2 | 0.034054 | 0.600747 | 0.039528 | 4.733363 | 0.072576 | 0.000000 | reference_kept |
| `mode_theta_detach_flatreg001_seed21_rerun_20260622` | 1.106111 | fail | 3 | 0.046238 | 0.658360 | 0.041831 | 4.867199 | 0.071877 | 0.406913 | no_promotion_hard_constraint_fail |
| `GRU_seed101` | 14.261040 | fail | 4 | 0.705280 | 1.905364 | 0.148762 | 183.810097 | 0.350302 | 0.456922 | no_promotion_hard_constraint_fail |
| `TCN_seed101` | 18.250409 | fail | 5 | 0.552568 | 2.233446 | 0.143574 | 302.924743 | 0.266945 | 0.653576 | no_promotion_hard_constraint_fail |

## Hard-Constraint Detail

| algorithm | hard status | failures | unavailable |
|---|---|---|---|
| `baseline_lock` | pass | reference_baseline | none |
| `uncertainty_seed101_rerun_20260622` | fail | closed_loop_main_acc=0.0200623 | none |
| `mode_theta_detach_flatreg001_seed21_rerun_20260622` | fail | stall_recall=0.0520833; flat_peak_theta_error=1.13741 | none |
| `GRU_seed101` | fail | closed_loop_main_acc=0.01153; stall_recall=0.0833333; flat_peak_theta_error=1.0911; omega_cmd_rms=4.82669; delta_u_proxy=38.8329 | none |
| `TCN_seed101` | fail | closed_loop_main_acc=0.188679; offline_acc_main=0.222932; stall_recall=0.1875; slope_recall=0.144364; theta_edge_p95=1.48084; flat_peak_theta_error=1.22281; omega_cmd_rms=3.67813; delta_u_proxy=63.9978 | none |

## Parameter Snapshot

| algorithm | family | seed | role | key parameters | artifact |
|---|---|---:|---|---|---|
| `baseline_lock` | ModernTCN_small | 101 | reference_baseline | channels=64; blocks=5; kernel_size=31; dropout=0.15; lambda_turn=0.20; lambda_theta=0.55; lambda_theta_flat=0.12; turn_transition_weight=2.5; turn_class_multipliers=[1.4,0.8,1.4] | `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.pt` |
| `uncertainty_seed101_rerun_20260622` | ModernTCN_small | 101 | rerun_candidate | loss_mode=uncertainty_weighting; channels=64; blocks=5; kernel_size=31; dropout=0.15; lambda_turn=0.2; lambda_theta=0.55; lambda_theta_flat=0.12; turn_transition_weight=2.5; main_neg_slope_weight=2.0; turn_class_multipliers=[1.4, 0.8, 1.4]; weight_main=26.0... | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_sci_innovation\01_loss_optimization\uncertainty_seed101_rerun_20260622\modern_tcn_seed101.pt` |
| `mode_theta_detach_flatreg001_seed21_rerun_20260622` | ModernTCNModeTheta | 21 | rerun_candidate | loss_mode=fixed; channels=64; blocks=5; kernel_size=31; dropout=0.15; lambda_turn=0.2; lambda_theta=0.55; lambda_theta_flat=0.12; turn_transition_weight=2.5; main_neg_slope_weight=2.0; turn_class_multipliers=[1.4, 0.8, 1.4]; weight_main=NaN; weight_turn=NaN... | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_sci_innovation\04_mode_conditioned_theta\mode_theta_detach_flatreg001_seed21_rerun_20260622\modern_tcn_mode_theta_seed21.pt` |
| `GRU_seed101` | GRU | 101 | strict_closed_loop_comparator | mode=physics_guided; max_epochs=140; batch_size=128; dropout=0.2; best_metric=composite; base_best_metric=composite; lambda_turn=0.08; lambda_theta=0.55; lambda_theta_flat=0.12; turn_head=mlp/inputstats; turn_head_hidden=64; turn_class_multipliers=[1.08 1. ... | `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\models\GRU_model_full_gru_v5_plantfix_passive17_plus_all5_seed101.mat` |
| `TCN_seed101` | TCN | 101 | strict_closed_loop_comparator | mode=physics_guided; max_epochs=140; batch_size=128; dropout=0.15; best_metric=turn_priority; base_best_metric=composite; lambda_turn=0.08; lambda_theta=0.55; lambda_theta_flat=0.12; turn_head=mlp/inputstats; turn_head_hidden=64; turn_class_multipliers=[1.0... | `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\models\TCN_model_full_tcn_v5_plantfix_passive17_plus_all5_seed101.mat` |

## Interpretation

- No candidate satisfies strict Class C after applying frozen hard constraints.
- GRU/TCN are now strict same-shell comparators, not legacy-only evidence.
- Removing hard status changes promotion eligibility only; the J_control ordering itself is independent of hard gates.
