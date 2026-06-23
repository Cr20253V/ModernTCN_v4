# Window 2 Execution Summary

- Scope executed: rerun candidate check, sandbox closed-loop, post-sandbox formal validation, and Phase B1 baseline error map.
- Rerun candidates checked:
  - `uncertainty_seed101_rerun_20260622`
  - `mode_theta_detach_flatreg001_seed21_rerun_20260622`
- Sandbox result: both rerun candidates were executable and improved the single sharp-turn sandbox path versus `baseline_lock`.
- Formal validation result: no strict Class C candidate after validating on the frozen three-path baseline set.

## Formal Validation Decision

| controller | J_control | hard_constraint_status | eligible_for_class_c | reason |
|---|---:|---|---:|---|
| `baseline_lock` | 1.000000 | pass | 0 | reference_baseline |
| `mode_theta_detach_flatreg001_seed21_rerun_20260622` | 1.106111 | pass | 0 | J_control_not_better_than_baseline |
| `uncertainty_seed101_rerun_20260622` | 0.944117 | fail | 0 | main_acc_drop=0.0200623 |

## Key Outputs

- `results/modern_tcn_metric_rebuild/05_sandbox_closed_loop_if_needed/03_formal_validation/formal_validation_aggregate_report.md`
- `results/modern_tcn_metric_rebuild/05_sandbox_closed_loop_if_needed/03_formal_validation/formal_validation_class_c_decision.csv`
- `results/modern_tcn_metric_rebuild/06_local_residual_optimization_if_needed/01_baseline_error_map/error_map_report.md`

## Phase B1 Read

- Baseline error map generated over 3602 test windows.
- Top-50 theta-error concentration:
  - transition share: 0.1000
  - slope-edge share: 0.0600
  - flat-peak share: 0.0200
- Initial interpretation: top theta errors concentrate mostly in stall-like windows rather than clean transition/edge/flat-peak flags; residual design should be conservative and head-specific.

## Stop Point

- No Class C global candidate was promoted.
- Residual training was not started in this window.
- Next window should decide whether to enter local residual correction using the B1 error map, or stop and keep `ModernTCN_small` as current best.
