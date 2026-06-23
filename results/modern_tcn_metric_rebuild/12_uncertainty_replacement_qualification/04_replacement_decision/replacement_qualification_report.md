# Uncertainty Anchor Replacement Qualification

- decision: `AnchorOnlyNotFullReplacement`
- offline stability: `reject_seed_fragile` (1/3 pass)
- median tested closed-loop J_control: 1.136382
- anchor: `uncertainty_seed101_rerun_20260622`
- baseline: `baseline_lock`

| rank | candidate | role | J_control | v2 status |
|---:|---|---|---:|---|
| 1 | `uncertainty_seed101_rerun_20260622` | seed101_anchor | 0.944117 | pass |
| 2 | `baseline_lock` | ModernTCN_small_baseline | 1.000000 | pass |
| 3 | `ua_seed21` | same_recipe_non101_seed | 1.136382 | pass |
| 4 | `ua_seed42` | same_recipe_non101_seed | 11.915497 | pass |

## Interpretation

- `ReplacementQualified` means the uncertainty-weighted recipe can be used as the selected replacement for the original ModernTCN_small baseline under the current v2 gates.
- `AnchorOnlyNotFullReplacement` means seed101 remains the best anchor, but the recipe is not yet robust enough to replace the baseline generally.
