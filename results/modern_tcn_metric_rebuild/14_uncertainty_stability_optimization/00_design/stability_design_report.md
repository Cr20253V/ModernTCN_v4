# Uncertainty Stability Optimization Design

- scope: seed21/42 stability first; no architecture changes.
- primary failure targets: `flat_peak_theta_error`, `theta_edge_p95_abs_err`.
- closed-loop is gated by seed21/42 offline pass.

| run | description |
|---|---|
| `s01_lr13_select_edges_flat` | u06-like lr=0.0013 plus edge and flat peak checkpoint selection |
| `s02_flat_excess_loss` | reduce seed21 flat peak with flat excess loss and flat peak selection |
| `s03_edge_active_loss` | reduce seed42 edge error with active/error excess loss and positive theta weight |
| `s04_balanced_protect` | combine stronger uncertainty loss adaptation with main/turn protection |
| `s05_conservative_lr` | lower optimizer lr while selecting flat/edge protection |
| `s06_strong_flat_soft_edge` | stronger flat peak loss with soft edge selection |
| `s07_pos_edge_guard` | positive edge guard for seed42 while keeping flat peak selected |
| `s08_full_protect_mix` | u23-like main/turn protection plus flat/edge objectives |
