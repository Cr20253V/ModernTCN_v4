# Stage 1 Open-Loop Smoke Report

- plant_revision: `agv_physics_v2_plantfix`
- pass: `1`

| case | pass | beta peak deg | omega peak | v min | v max |
|---|---:|---:|---:|---:|---:|
| `straight_flat` | 1 | 0.0000 | 0.0000 | 0.6000 | 0.8000 |
| `turn_flat` | 1 | 0.0219 | 0.0071 | 0.6000 | 0.8000 |
| `straight_slope` | 1 | 0.0000 | 0.0000 | 0.6000 | 0.8000 |
| `turn_slope` | 1 | 0.0231 | 0.0061 | 0.6000 | 0.8000 |

No NaN/Inf, bounded beta, bounded omega, and plausible velocity are required before full raw regeneration.
