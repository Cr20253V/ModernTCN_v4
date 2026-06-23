# Window 2 Formal Validation Aggregate Report

- scope: formal validation over the frozen baseline path set
- output root: `results/modern_tcn_metric_rebuild/05_sandbox_closed_loop_if_needed/03_formal_validation/`
- strict Class C requires hard-constraint pass and aggregate J_control below baseline.

## Aggregate Means

| controller | ey_rmse | xy_rmse | epsi_rmse | j_du | omega_cmd_rms | viol_rate | theta_mae_deg | main_acc_pct | turn_acc_pct |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `baseline_lock` | 0.034054 | 0.600747 | 0.039528 | 4.733363 | 0.072576 | 0.000000 | 0.618880 | 94.4445 | 53.6150 |
| `mode_theta_detach_flatreg001_seed21_rerun_20260622` | 0.046238 | 0.658360 | 0.041831 | 4.867199 | 0.071877 | 0.000000 | 0.706280 | 95.4346 | 59.0982 |
| `uncertainty_seed101_rerun_20260622` | 0.029627 | 0.553891 | 0.037921 | 4.687868 | 0.071042 | 0.000000 | 0.552765 | 92.4383 | 53.9767 |

## Class C Gate

| controller | J_control | hard_constraint_status | eligible_for_class_c | reason |
|---|---:|---|---:|---|
| `baseline_lock` | 1.000000 | pass | 0 | reference_baseline |
| `mode_theta_detach_flatreg001_seed21_rerun_20260622` | 1.106111 | pass | 0 | J_control_not_better_than_baseline |
| `uncertainty_seed101_rerun_20260622` | 0.944117 | fail | 0 | main_acc_drop=0.0200623 |

## Decision

- no strict Class C candidate after formal validation.
- sandbox gains do not survive the full frozen path-set validation.
