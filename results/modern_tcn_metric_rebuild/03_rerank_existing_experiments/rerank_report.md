# Official Rerank Report

## Freeze order

- metric_dictionary.csv was frozen before reranking.
- hard_constraint_thresholds.json was frozen before reranking.
- vFinal_control_oriented_frozen.json was frozen before reranking.

## Scope

- This window reranks historical offline candidates only.
- E5 remains advisory_only and is excluded from formal J_control / J_smooth_event ranking.
- No candidate in this window has new closed-loop evidence, so hard_constraint_status is offline_only for historical candidates.

## Proxy top-3

- 1. uncertainty_seed101
- 2. mode_theta_detach_flatreg001_seed21
- 3. mode_theta_detach_flatreg003_seed21

## Caveats

- Missing closed-loop metrics are not fabricated.
- Missing ratio is reported on the offline/core score set used for class B gating.
- E2 smoothness evidence is degraded and cannot support theta_smoothness_loss claims.
- E5 scheduled metrics are advisory_only and should not be treated as formal replay evidence.
