# Rerank With v2 Thresholds

## Rule

- Numeric `J_control` ranking is unchanged by threshold changes.
- Engineering ranking uses `closed_loop_v2_status` first, then `J_control`.
- `baseline_lock` is kept as a reference row, not a candidate promotion.
- `full_v2` is reported as a secondary view because it includes offline protection metrics.

## Primary Ranking: Closed-Loop v2 Gate + J_control

| rank | algorithm | hard v2 | J_control | J < baseline | decision | main acc | xy | j_du | omega |
|---:|---|---|---:|---|---|---:|---:|---:|---:|
| 1 | `uncertainty_seed101_rerun_20260622` | pass | 0.944117 | True | promote_candidate_under_v2 | 92.438 | 0.553891 | 4.687868 | 0.071042 |
| 2 | `baseline_lock` | pass | 1.000000 | False | reference_baseline | 94.445 | 0.600747 | 4.733363 | 0.072576 |
| 3 | `mode_theta_detach_flatreg001_seed21_rerun_20260622` | pass | 1.106111 | False | hard_pass_but_not_better_than_baseline | 95.435 | 0.658360 | 4.867199 | 0.071877 |
| 4 | `GRU_seed101` | pass | 14.261040 | False | hard_pass_but_not_better_than_baseline | 93.292 | 1.905364 | 183.810097 | 0.350302 |
| 5 | `TCN_seed101` | fail | 18.250409 | False | reject_hard_fail | 75.577 | 2.233446 | 302.924743 | 0.266945 |

## Numeric Ranking Only

| rank | algorithm | J_control | old hard | closed-loop v2 | full v2 |
|---:|---|---:|---|---|---|
| 1 | `uncertainty_seed101_rerun_20260622` | 0.944117 | fail | pass | pass |
| 2 | `baseline_lock` | 1.000000 | pass | pass | pass |
| 3 | `mode_theta_detach_flatreg001_seed21_rerun_20260622` | 1.106111 | fail | pass | pass |
| 4 | `GRU_seed101` | 14.261040 | fail | pass | pass |
| 5 | `TCN_seed101` | 18.250409 | fail | fail | fail |

## Full v2 Gate View

| rank | algorithm | full v2 | J_control | decision | failures |
|---:|---|---|---:|---|---|
| 1 | `uncertainty_seed101_rerun_20260622` | pass | 0.944117 | promote_candidate_under_v2 | none |
| 2 | `baseline_lock` | pass | 1.000000 | reference_baseline | none |
| 3 | `mode_theta_detach_flatreg001_seed21_rerun_20260622` | pass | 1.106111 | hard_pass_but_not_better_than_baseline | none |
| 4 | `GRU_seed101` | pass | 14.261040 | hard_pass_but_not_better_than_baseline | none |
| 5 | `TCN_seed101` | fail | 18.250409 | reject_hard_fail | closed_loop_main_acc_drop=0.188679>0.03; delta_u_proxy_ratio=63.9978>45; offline_acc_main_drop=0.222932>0.03; stall_recall_drop=0.1875>0.1; slope_recall_drop=0.144364>0.03; theta_edge_p95_ratio=1.48084>1.05; flat_peak_theta_error_ratio=1.22281>1.15 |

## Interpretation

- Under v2, `uncertainty_seed101_rerun_20260622` becomes the only non-reference candidate that both passes hard gates and has `J_control < baseline`.
- `GRU_seed101` now passes the v2 hard gate, matching the visual closed-loop acceptability judgment, but its aggregate `J_control` is still far worse than baseline.
- `mode_theta_detach_flatreg001_seed21_rerun_20260622` also passes v2 hard gates, but it remains worse than baseline by `J_control`.
- `TCN_seed101` remains rejected because closed-loop main accuracy and delta-u proxy remain beyond the proposed v2 limits.
