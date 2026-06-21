# exp2 dual_kernel tuning stop before multi-seed

## Decision

`STOP_NO_MULTISEED`

## Reason

Two seed21 screening rounds were completed under the isolated tuning root. No candidate passed the exp2 offline gate, so seeds `42` and `101` were not launched.

This is a gate stop, not a runtime failure. Starting multi-seed from the current candidates would measure seed variance around a failing recipe rather than validate a promotable candidate.

## Evidence

- Summary CSV: `results/modern_tcn_ablation/exp2_dual_kernel_tune/tuning_all_summary.csv`
- Summary Markdown: `results/modern_tcn_ablation/exp2_dual_kernel_tune/tuning_all_summary.md`
- Best candidate: `tune_r1_scale035_s7_seed21`
- Best candidate status: `FAIL`

## Best candidate failures

- `acc_turn_transition 0.494784 >= 0.497765` failed.
- `flat_recall 0.955026 >= 0.959577` failed.
- `stall_recall 0.645833 >= 0.668750` failed.
- `theta_edge_p95_abs_err 3.556906 <= 2.805057` failed.
- `flat_peak_theta_error 7.179438 <= 5.585740` failed.
