# BI-BU Final Report

- decision_class: `Class 5`
- can_claim_recipe_level_replacement: `0`
- can_claim_paper_main_method: `0`
- best_candidate: `a2_freeze_early`
- baseline_J_control: `1.000000`
- anchor_seed101_J_control: `0.944117`
- multiseed_offline_pass_rate: `0.666667`
- multiseed_closed_loop_mean_J: `NaN`
- multiseed_closed_loop_worst_J: `NaN`
- stop_reason: Sentinel closed-loop did not meet the aggregate J_control and control-ratio thresholds.

## Phase 2

| run_id | seed | strict_offline_pass | acc_main | theta_edge_p95_abs_err | flat_peak_theta_error | stall_recall |
|---|---:|---:|---:|---:|---:|---:|
| `a2_freeze_early_seed21` | 21 | 1 | 0.964742 | 2.889292 | 5.486582 | 0.697917 |
| `a2_freeze_early_seed42` | 42 | 1 | 0.970572 | 2.862206 | 6.084842 | 0.708333 |
| `a2_freeze_early_seed101` | 101 | 1 | 0.964187 | 2.719172 | 6.113857 | 0.697917 |

## Recommendation

Offline-stable candidate, but closed-loop sentinel did not clear the promotion gate.
