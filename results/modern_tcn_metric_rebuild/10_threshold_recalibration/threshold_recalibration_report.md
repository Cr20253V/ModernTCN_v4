# Hard Threshold Recalibration v2 Proposal

## Method

- Keep the frozen v1 thresholds unchanged; write v2 proposals in this node only.
- Treat `baseline_lock`, the two rerun ModernTCN candidates, and `GRU_seed101` as accepted anchors for threshold calibration.
- Treat `TCN_seed101` as the rejected anchor because the strict closed-loop comparison showed materially worse behavior.
- For each hard metric, check whether a single threshold can pass accepted anchors and reject TCN.
- Metrics that cannot separate GRU from TCN are not used as decisive hard gates; they remain broad instability ceilings or scored penalties.

## Proposed Closed-Loop v2 Thresholds

| threshold | v1 | proposed v2 | reason |
|---|---:|---:|---|
| `acc_main_min_drop` | 0.010 | 0.030 | passes GRU and uncertainty; still rejects TCN by a wide margin |
| `omega_cmd_rms_max_ratio` | 1.10 | 5.00 | not discriminative; use as broad ceiling, not as main evidence |
| `delta_u_proxy_max_ratio` | 1.10 | 45.00 | passes GRU but rejects TCN; ratio is high because baseline `j_du` is very small |

## Proposed Full v2 Additions

| threshold | v1 | proposed v2 | reason |
|---|---:|---:|---|
| `stall_recall_min_drop` | 0.050 | 0.100 | passes GRU while rejecting TCN |
| `slope_recall_min_drop` | 0.010 | 0.030 | modest relaxation; TCN remains failed |
| `theta_edge_p95_max_ratio` | 1.05 | 1.05 | unchanged; already separates GRU from TCN |
| `flat_peak_theta_error_max_ratio` | 1.05 | 1.15 | passes GRU/mode-theta range, still rejects TCN |

## Reclassification Under v2

| algorithm | old hard | closed-loop v2 | full v2 | J_control | J < baseline |
|---|---|---|---|---:|---|
| `baseline_lock` | pass | pass | pass | 1.000000 | False |
| `uncertainty_seed101_rerun_20260622` | fail | pass | pass | 0.944117 | True |
| `mode_theta_detach_flatreg001_seed21_rerun_20260622` | fail | pass | pass | 1.106111 | False |
| `GRU_seed101` | fail | pass | pass | 14.261040 | False |
| `TCN_seed101` | fail | fail | fail | 18.250409 | False |

## Recommendation

- Adopt `hard_constraint_thresholds_v2_closed_loop_proposed.json` first if the immediate goal is to make the closed-loop gate match visual/engineering acceptability.
- Do not overwrite the v1 frozen file; freeze v2 only after naming a new metric version and rerunning the comparison reports.
- `GRU_seed101` passes the proposed closed-loop v2 and full v2 hard gates, but its `J_control` remains much worse than baseline, so this does not make it a Class C replacement.
- `TCN_seed101` remains failed under both v2 profiles.
- The full v2 profile would also make `uncertainty_seed101_rerun_20260622` pass hard gates while retaining `J_control < baseline`; this is a promotion side effect that should be reviewed before any formal freeze.
