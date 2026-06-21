# D9 Optional Extension Skip

- decision: `skip_dual_k51_s5`
- reason: default k31 dual-kernel branch did not produce a near-passing candidate.
- passing_offline_gate: `0`
- best_default_run: `dual_k31_s7_seed42`
- best_default_failures: `acc_main`, `theta_mae_deg`, `flat_recall`, `stall_recall`, `theta_edge_p95_abs_err`, `flat_peak_theta_error`
- extension_policy: `dual_k51_s5` is an independent extension because it changes large kernel, blocks, and dropout; it is not justified after the default branch failed the offline and boundary gates.
- not_executed: `dual_k51_s5_seed21/42/101`
