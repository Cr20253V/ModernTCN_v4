# BI-BU sentinel closed-loop report

## Candidate aggregates

| run_id | seed | n_paths | mean_J_control | worst_J_control | mean_j_du_ratio | mean_omega_cmd_rms_ratio | path_catastrophic_count |
|---|---:|---:|---:|---:|---:|---:|---:|
| `a2_freeze_early_seed21` | 21 | 3 | 2.120818 | 3.572427 | 6.479890 | 1.105942 | 2 |
| `a2_freeze_early_seed42` | 42 | 3 | 1.613192 | 2.587360 | 4.233231 | 1.147548 | 2 |

## Path detail

| phase_label | seed | run_id | path_tag | J_control | j_du_ratio | omega_cmd_rms_ratio | path_catastrophic |
|---|---:|---|---|---:|---:|---:|---:|
| `sentinel` | 21 | `a2_freeze_early_seed21` | `path_factory_logistics_showcase_theta10_v3` | 3.572427 | 13.006150 | 1.179934 | 1 |
| `sentinel` | 42 | `a2_freeze_early_seed42` | `path_factory_logistics_showcase_theta10_v3` | 2.587360 | 7.810785 | 1.227740 | 1 |
| `sentinel` | 21 | `a2_freeze_early_seed21` | `path_closed_loop_long_updown_theta10_v1` | 1.884466 | 5.980870 | 0.949503 | 1 |
| `sentinel` | 42 | `a2_freeze_early_seed42` | `path_closed_loop_long_updown_theta10_v1` | 1.414851 | 4.335109 | 1.007885 | 1 |
| `sentinel` | 21 | `a2_freeze_early_seed21` | `path_closed_loop_sharp_turn_transition_theta10_v1` | 0.905561 | 0.452650 | 1.188390 | 0 |
| `sentinel` | 42 | `a2_freeze_early_seed42` | `path_closed_loop_sharp_turn_transition_theta10_v1` | 0.837363 | 0.553798 | 1.207018 | 0 |
