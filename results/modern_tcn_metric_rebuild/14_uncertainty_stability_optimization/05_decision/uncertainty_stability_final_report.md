# Uncertainty Stability Optimization Final Report

- decision: `RobustOfflineNoClosedLoopPromotion`
- robust offline configs: 1
- promoted closed-loop candidates: 0

## Offline Final Summary

| run | label | pass | median score | seed status |
|---|---|---:|---:|---|
| `s01_lr13_select_edges_flat` | robust_pass | 3/3 | 0.532372 | seed21=pass(none);seed42=pass(none);seed101=pass(none) |

## Closed-loop Summary

| rank | candidate | J_control | status |
|---:|---|---:|---|
| 1 | `uncertainty_seed101_rerun_20260622` | 0.944117 | pass |
| 2 | `baseline_lock` | 1.000000 | pass |
| 3 | `s01_lr13_select_edges_flat_seed101` | 1.105446 | pass |
| 4 | `s01_lr13_select_edges_flat_seed21` | 1.143118 | pass |
| 5 | `s01_lr13_select_edges_flat_seed42` | 1.174967 | pass |

## Output Files

- design: `results/modern_tcn_metric_rebuild/14_uncertainty_stability_optimization/00_design/`
- seed21/42 metrics: `results/modern_tcn_metric_rebuild/14_uncertainty_stability_optimization/02_stability_screen/seed21_42_stability_metrics.csv`
- stability screen: `results/modern_tcn_metric_rebuild/14_uncertainty_stability_optimization/02_stability_screen/stability_screen_results.csv`
- final offline summary: `results/modern_tcn_metric_rebuild/14_uncertainty_stability_optimization/02_stability_screen/final_multiseed_offline_summary.csv`
- closed-loop outputs: `results/modern_tcn_metric_rebuild/14_uncertainty_stability_optimization/04_closed_loop_multiseed/`
