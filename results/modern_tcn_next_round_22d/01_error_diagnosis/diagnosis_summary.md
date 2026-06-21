# Phase 1 Diagnosis Summary

No baseline retraining was performed. The diagnosis used the frozen retained champion checkpoint and current seq128 test set.

## Questions

1. stall_recall sample sparsity: `YES`. Window counts train/val/test stall = `432/42/96`.
2. slope boundary concentration: `YES`. Boundary share among slope errors = `0.754`.
3. theta/main trade-off signal: `YES`. Theta MAE main-correct/error = `0.7482/2.1159` deg.
4. transition vs stable main accuracy: transition/non-transition = `0.9762/0.9649`.
5. seq256 necessity: `REASONABLE_TO_TEST`, because longer context can be evaluated without changing 22D features and may clarify boundary/transition sensitivity; Phase 3 remains deferred until Phase 2 validation passes.

## Core Baseline Metrics Recomputed

- acc_main: `0.966963`
- acc_turn_transition: `0.497765`
- theta_mae_deg: `0.679494`
- flat/stall/slope recall: `0.969577/0.718750/0.974909`
