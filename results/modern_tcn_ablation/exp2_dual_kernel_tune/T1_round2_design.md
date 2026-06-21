# exp2 dual_kernel tuning round2 design

## Round1 conclusion

Best screening area is `small_kernel=7`, `dual_branch_scale=0.35`. It keeps `acc_main`, `theta_mae_deg`, `slope_recall`, and `false_turn_straight` usable, but still fails:

- `acc_turn_transition`: slightly below baseline gate.
- `flat_recall`: slightly below baseline gate.
- `stall_recall`: below baseline gate.
- `theta_edge_p95_abs_err` and `flat_peak_theta_error`: clear boundary/peak regressions.

Other directions in round1 caused larger theta or false-turn regressions, so round2 stays local.

## Round2 candidates

1. `tune_r2_scale030_s7_seed21`: reduce dual branch scale from `0.35` to `0.30`.
2. `tune_r2_zero035_s7_seed21`: keep scale `0.35`, initialize small branch as zero to test whether early small-branch perturbation is the source.
3. `tune_r2_mainstall035_s7_seed21`: keep scale `0.35`, add mild main class multipliers and stall-aware selection.
4. `tune_r2_edgeflat035_s7_seed21`: keep scale `0.35`, add moderate edge/flat-peak selection without changing loss.

All candidates remain seed21 screening only, use the fixed 22D plantfix dataset, and write only under `results/modern_tcn_ablation/exp2_dual_kernel_tune/`.
