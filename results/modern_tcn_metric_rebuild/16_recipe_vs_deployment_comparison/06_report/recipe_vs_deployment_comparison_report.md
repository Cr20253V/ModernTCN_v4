# Recipe vs Deployment Comparison

## Core Decision

1. Deployment champion replacement: `uncertainty_seed101_rerun_20260622` has `J_control=0.944117` versus locked champion `1.000000`; status is `pass`. BI-BU A2 seed21/42 remain deployment-gate failures.
2. Recipe-level multiseed comparison: complete. Lower mean J_control is better; winner by mean J_control is `Uncertainty_weighted_same_recipe` (ModernTCN_small_base=11.457102, Uncertainty_weighted_same_recipe=4.665332).
3. Selected-best comparison: diagnostic selected-best table is available: ModernTCN_small_base `modern_base_seed21` J=1.005784; Uncertainty_weighted_same_recipe `uncertainty_seed101_rerun_20260622` J=0.944117. Paper-valid selected-best claims still require a common validation/offline selection protocol.

## A2 Required Status Fields

| algorithm_recipe | seed | J_control | deployment_champion_gate_status | recipe_multiseed_status | selected_model_status | deployment_champion_gate_reason |
| --- | --- | --- | --- | --- | --- | --- |
| BI_BU_A2_freeze_early | 21 | 2.12081830264372 | fail | sentinel_failed_no_full_recipe_claim | not_applicable_for_individual_seed | mean_J_control=2.12082>baseline=1;path_catastrophic_count=2>0 |
| BI_BU_A2_freeze_early | 42 | 1.61319158327678 | fail | sentinel_failed_no_full_recipe_claim | not_applicable_for_individual_seed | mean_J_control=1.61319>baseline=1;path_catastrophic_count=2>0 |

## Deployment Champion Comparison

| algorithm_recipe | candidate_id | seed | evidence_scope | J_control | worst_path_J | path_catastrophic_count | deployment_champion_gate_status | deployment_champion_gate_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BI_BU_A2_freeze_early | a2_freeze_early_seed42 | 42 | sentinel_three_path | 1.61319158327678 | 2.58736013155446 | 2 | fail | mean_J_control=1.61319>baseline=1;path_catastrophic_count=2>0 |
| BI_BU_A2_freeze_early | a2_freeze_early_seed21 | 21 | sentinel_three_path | 2.12081830264372 | 3.57242748906417 | 2 | fail | mean_J_control=2.12082>baseline=1;path_catastrophic_count=2>0 |
| ModernTCN_small_base | modern_base_seed21 | 21 | current_v2_three_path_node16 | 1.00578398807548 | 1.33073819193599 | 0 | fail | mean_J_control=1.00578>baseline=1 |
| ModernTCN_small_base | modern_base_seed101 | 101 | current_v2_three_path_node16 | 13.7637421354444 | 135.079575090136 | 1 | fail | mean_J_control=13.7637>baseline=1;path_catastrophic_count=1>0 |
| ModernTCN_small_base | modern_base_seed42 | 42 | current_v2_three_path_node16 | 19.6017807316235 | 205.78872834781 | 1 | fail | mean_J_control=19.6018>baseline=1;path_catastrophic_count=1>0 |
| ModernTCN_small_locked_champion | baseline_lock | 101 | current_v2_three_path | 1 | 1 | 0 | reference | locked ModernTCN_small champion baseline |
| Uncertainty_stability_s01 | s01_lr13_select_edges_flat_seed101 | 101 | current_v2_three_path | 1.10544617766553 | 1.4139186311548 | 0 | fail | mean_J_control=1.10545>baseline=1 |
| Uncertainty_stability_s01 | s01_lr13_select_edges_flat_seed21 | 21 | current_v2_three_path | 1.14311774157566 | 2.21613537740415 | 1 | fail | mean_J_control=1.14312>baseline=1;path_catastrophic_count=1>0 |
| Uncertainty_stability_s01 | s01_lr13_select_edges_flat_seed42 | 42 | current_v2_three_path | 1.17496689656309 | 2.37202879808951 | 1 | fail | mean_J_control=1.17497>baseline=1;path_catastrophic_count=1>0 |
| Uncertainty_weighted_same_recipe | uncertainty_seed101_rerun_20260622 | 101 | current_v2_three_path | 0.94411711953914 | 1.06346989562921 | 0 | pass | mean_J_control<=baseline and no path catastrophic failure |
| Uncertainty_weighted_same_recipe | uncertainty_anchor_same_recipe_seed21 | 21 | current_v2_three_path | 1.13638158707013 | 1.31925951475442 | 0 | fail | mean_J_control=1.13638>baseline=1 |
| Uncertainty_weighted_same_recipe | uncertainty_anchor_same_recipe_seed42 | 42 | current_v2_three_path | 11.9154967909798 | 113.779469042867 | 1 | fail | mean_J_control=11.9155>baseline=1;path_catastrophic_count=1>0 |

## Recipe Multiseed Summary

| algorithm_recipe | target_seed_set | available_seed_rows | missing_offline_target_seeds | missing_closed_loop_target_seeds | offline_pass_count | closed_loop_count | mean_J_control | median_J_control | best_J_control | worst_J_control | std_J_control | deployment_pass_rate_vs_champion | path_catastrophic_count | recipe_multiseed_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ModernTCN_small_base | 21/42/101 | 21/42/73/101 | none | none | 1 | 3 | 11.4571022850478 | 13.7637421354444 | 1.00578398807548 | 19.6017807316235 | 7.76501617388702 | 0 | 2 | complete_base_recipe_distribution_available |
| Uncertainty_weighted_same_recipe | 21/42/101 | 21/42/101 | none | none | 1 | 3 | 4.66533183252969 | 1.13638158707013 | 0.94411711953914 | 11.9154967909798 | 5.12724164633852 | 0.333333333333333 | 1 | complete_uncertainty_recipe_better_by_mean_J |
| Uncertainty_stability_s01 | 21/42/101 | 21/42/101 | none | none | 3 | 3 | 1.14117693860143 | 1.14311774157566 | 1.10544617766553 | 1.17496689656309 | 0.0284148743459827 | 0 | 2 | complete_secondary_recipe_distribution_available_but_fails_champion |
| BI_BU_A2_freeze_early | 21/42/101 | 21/42/101 | none | 101 | 3 | 2 | 1.86700494296025 | 1.86700494296025 | 1.61319158327678 | 2.12081830264372 | 0.25381335968347 | 0 | 4 | sentinel_failed_no_full_recipe_claim |

## Selected-best Comparison

| algorithm_recipe | selected_candidate_id | seed | selection_protocol | J_control | selected_model_status |
| --- | --- | --- | --- | --- | --- |
| ModernTCN_small_locked_champion | baseline_lock | 101 | already_locked_deployment_champion | 1 | reference |
| ModernTCN_small_base | modern_base_seed21 | 21 | same_target_seed_set_diagnostic_best | 1.00578398807548 | fail_vs_locked_champion |
| Uncertainty_weighted_same_recipe | uncertainty_seed101_rerun_20260622 | 101 | historical_anchor_seed101_selection | 0.94411711953914 | pass_vs_locked_champion |
| Uncertainty_stability_s01 | s01_lr13_select_edges_flat_seed101 | 101 | best_seed_after_robust_offline_recipe | 1.10544617766553 | fail_vs_locked_champion |
| BI_BU_A2_freeze_early | a2_freeze_early_seed42 | 42 | sentinel_best_seed_only | 1.61319158327678 | fail_sentinel_not_selectable |

## Missing Experiments

| algorithm_recipe | seed | checkpoint_exists | offline_status | closed_loop_status | required_action |
| --- | --- | --- | --- | --- | --- |

## Interpretation

- Do not use the locked ModernTCN_small champion alone to declare Uncertainty or BI-BU recipe-level failure.
- It is valid to say A2 seed21/42 failed the deployment champion replacement gate.
- Recipe-level claims use the identical seed set `21/42/101`, identical path set, and identical `J_control` definition.
- Selected-best claims are diagnostic unless the seed selection protocol is validation/offline-only and applied equally to every algorithm.

## Method Notes

- Deployment gate here is `mean J_control <= 1.0` and no path-level catastrophic failure.
- Path-level catastrophic failure uses the existing sentinel flag where available; otherwise it is counted when path-level `J_control > 1.5`.
- Recipe-level status remains pending whenever either ModernTCN_small base or Uncertainty-weighted seed21/42/101 closed-loop distribution is unavailable.

## Outputs

- Evidence inventory: `results/modern_tcn_metric_rebuild/16_recipe_vs_deployment_comparison/00_evidence_inventory/evidence_inventory.csv`
- Seed-level status table: `results/modern_tcn_metric_rebuild/16_recipe_vs_deployment_comparison/01_seed_level_status/seed_level_gate_status.csv`
- Deployment comparison: `results/modern_tcn_metric_rebuild/16_recipe_vs_deployment_comparison/02_deployment_champion/deployment_champion_comparison.csv`
- Recipe summary: `results/modern_tcn_metric_rebuild/16_recipe_vs_deployment_comparison/03_recipe_multiseed/recipe_multiseed_summary.csv`
- Selected-best comparison: `results/modern_tcn_metric_rebuild/16_recipe_vs_deployment_comparison/04_selected_best/selected_best_comparison.csv`
- Missing experiment manifest: `results/modern_tcn_metric_rebuild/16_recipe_vs_deployment_comparison/05_missing_experiments/modern_tcn_small_required_closed_loop.csv`
- ModernTCN base closed-loop aggregate: `results/modern_tcn_metric_rebuild/16_recipe_vs_deployment_comparison/09_modern_base_closed_loop/closed_loop_results.csv`
