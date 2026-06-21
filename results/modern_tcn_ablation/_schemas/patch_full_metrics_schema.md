# Patch/full Metrics Schema

Offline required columns: acc_main, acc_turn, acc_turn_transition, theta_mae_deg, flat_recall, stall_recall, slope_recall, theta_edge_p95_abs_err, false_turn_straight, flat_peak_theta_error.

Patch/full strict gates:
- `acc_turn_transition >= baseline_acc_turn_transition`
- `theta_edge_p95_abs_err <= baseline_theta_edge_p95_abs_err + 0.05`
- `false_turn_straight <= baseline_false_turn_straight + 0.01`
- `flat_peak_theta_error <= baseline_flat_peak_theta_error + 0.25`

Legacy exclusion: D8 must assert that no path in `excluded_legacy_full_artifacts.json` was used as a run summary, config, checkpoint, or best-run source.
