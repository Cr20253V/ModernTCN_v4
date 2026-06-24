# Seed21/42 Stability Screen

| rank | run | status | pass | median score | seed status |
|---:|---|---|---:|---:|---|
| 1 | `s01_lr13_select_edges_flat` | dual_seed_pass | 2/2 | 0.537121 | seed21=pass(none);seed42=pass(none) |
| 2 | `s04_balanced_protect` | partial_pass | 1/2 | 0.543240 | seed21=fail(flat_peak_theta_error_ratio=1.27165>1.15);seed42=pass(none) |
| 3 | `s03_edge_active_loss` | partial_pass | 1/2 | 0.547189 | seed21=fail(flat_peak_theta_error_ratio=1.17774>1.15);seed42=pass(none) |
| 4 | `s06_strong_flat_soft_edge` | partial_pass | 1/2 | 0.561548 | seed21=fail(theta_edge_p95_ratio=1.08246>1.05);seed42=pass(none) |
| 5 | `s08_full_protect_mix` | partial_pass | 1/2 | 0.599298 | seed21=pass(none);seed42=fail(theta_edge_p95_ratio=1.08541>1.05) |
| 6 | `s05_conservative_lr` | reject_offline | 0/2 | 0.638715 | seed21=fail(flat_peak_theta_error_ratio=1.27619>1.15);seed42=fail(theta_edge_p95_ratio=1.38373>1.05; flat_peak_theta_error_ratio=1.21949>1.15) |
| 7 | `s07_pos_edge_guard` | reject_offline | 0/2 | 0.691798 | seed21=fail(theta_edge_p95_ratio=1.17967>1.05; flat_peak_theta_error_ratio=1.36215>1.15);seed42=fail(theta_edge_p95_ratio=1.20992>1.05; flat_peak_theta_error_ratio=1.26005>1.15) |
| 8 | `s02_flat_excess_loss` | reject_offline | 0/2 | 0.691947 | seed21=fail(theta_edge_p95_ratio=1.1447>1.05; flat_peak_theta_error_ratio=1.16846>1.15);seed42=fail(flat_peak_theta_error_ratio=1.52994>1.15) |
