# exp2 dual_kernel Targeted Tuning Design

## Diagnosis

The default dual-kernel sweep is not a total failure: several runs kept or improved isolated signals.

- `dual_k31_s7_seed42` improved transition accuracy over baseline (`0.5052` vs `0.4978`) and kept `false_turn_straight` near baseline, but theta and flat/stall quality regressed.
- `dual_k31_s7_seed21` improved theta MAE (`0.5881` vs `0.6795`) while keeping main accuracy near baseline, but transition, stall, and flat peak failed.
- `dual_k31_s3_seed21` improved main and slope, but transition and theta failed.

The consistent weakness is not capacity alone. The dual branch increases local responsiveness, but it destabilizes flat/stall discrimination and theta peak/boundary behavior.

## Tuning Principles

- Keep 22D plantfix dataset fixed.
- Keep output root isolated under `results/modern_tcn_ablation/exp2_dual_kernel_tune/`.
- Use seed21 screening first; only run multi-seed if a seed21 candidate is near-passing.
- Do not export ONNX or run MATLAB/Simulink during tuning.
- Attribute results as recipe-tuned dual-kernel, not pure structure ablation.

## Round 1 Candidates

1. `tune_r1_scale035_s7_seed21`: reduce dual branch perturbation.
2. `tune_r1_scale025_s7_seed21`: stronger reduction of branch perturbation.
3. `tune_r1_stall_s7_seed21`: preserve main/stall with mild class and selection pressure.
4. `tune_r1_theta_s7_seed21`: select for theta edge and flat peak stability.
5. `tune_r1_guard_s7_seed21`: add mild theta/false-turn regularization.
6. `tune_r1_s5_bal_seed21`: recover the low-theta s5 behavior while adding main/stall and false-turn pressure.

Promotion from screening requires at least near-gate behavior, not just one isolated metric.
