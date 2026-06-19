# Frozen maps_best vs P0 Oracle-MPC Comparison

Date: 2026-06-02

## Scope

This comparison re-evaluates the historical frozen MPC parameters and the P0 selected MPC candidate under the same repaired offline oracle replay.

Common replay fixes:

- `state_eq_ref` receives the current scalar `ref.v_ref/ref.omega_ref` during offline replay.
- `mpcmoveAdaptive` uses `Nominal.U(2)=omega_ref`, aligned with the LPV linearization work point.

Node 7 was not run. Canonical `data/models/maps_best.mat` was not overwritten.

## Candidates

| candidate | source | Np | Nc | Q center | R center | dR center |
|---|---|---:|---:|---|---|---|
| frozen maps_best | `data/models/maps_best.mat` | 150 | 50 | `[63.0542, 48.0671, 29.5106, 1.2320]` | `[7.3636e-4, 5.2020e-4]` | `[3.4362e-3, 2.2119e-1]` |
| P0 selected | `p0_oracle_retuning_20260602_033639` | 150 | 30 | `[100, 100, 15, 3]` | `[3e-5, 3e-5]` | `[1e-3, 1e-3]` |

The frozen candidate keeps the historical `maps_best.mat` adaptive map fields and fills missing modern interface fields from the current controller template only to make the old artifact runnable with the repaired replay.

## Overall

| candidate | fail | min completion | max e_y RMSE | mean e_y RMSE | max e_y peak | max cons Linf | max omega sat rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| frozen maps_best | 0 | 1.000 | 0.071500 | 0.039330 | 0.168291 | 0 | 0 |
| P0 selected | 0 | 1.000 | 0.062131 | 0.037755 | 0.152033 | 0 | 0 |

Both candidates pass the hard pre-Node-7 criterion `max e_y RMSE < 0.1 m`.

## Per-Path e_y RMSE

Positive delta means frozen is worse than P0.

| path | frozen maps_best | P0 selected | delta |
|---|---:|---:|---:|
| `path_closed_loop_long_updown_theta10_v1` | 0.063499 | 0.016110 | +0.047390 |
| `path_closed_loop_sharp_turn_transition_theta10_v1` | 0.022268 | 0.062131 | -0.039864 |
| `path_factory_logistics_showcase_theta10_v10` | 0.033836 | 0.044613 | -0.010776 |
| `path_factory_logistics_showcase_theta10_v3` | 0.026938 | 0.031946 | -0.005008 |
| `path_industrial_lite` | 0.016700 | 0.020223 | -0.003523 |
| `path_modern_tcn_demo_loop_v1` | 0.040570 | 0.043314 | -0.002744 |
| `path_modern_tcn_demo_loop_v2` | 0.071500 | 0.045947 | +0.025552 |

## Interpretation

The historical frozen `maps_best.mat` is still competitive after the oracle replay bug fix. It outperforms the P0 candidate on 5 of 7 routes, especially on `sharp_turn`, but it is clearly worse on `long_updown` and `demo_loop_v2`.

The P0 candidate is slightly better as a worst-case controller:

- max RMSE improves from `0.07150 m` to `0.06213 m`
- mean RMSE improves from `0.03933 m` to `0.03775 m`
- max peak error improves from `0.16829 m` to `0.15203 m`

Conclusion: the P0 candidate is not merely a random initial value, but the previous frozen maps are strong enough that they should remain a serious baseline. Before Node 7, it is reasonable to either use P0 for worst-case robustness or run a small final search initialized around both P0 and frozen `maps_best` to try to combine the sharper turn behavior of frozen maps with the better long-route robustness of P0.

## Source Artifacts

Frozen single-route replay outputs:

- `frozen_vs_p0_oracle_legacy_long_updown/`
- `frozen_vs_p0_oracle_legacy_path_closed_loop_sharp_turn_transition_theta10_v1/`
- `frozen_vs_p0_oracle_legacy_path_factory_logistics_showcase_theta10_v10/`
- `frozen_vs_p0_oracle_legacy_path_factory_logistics_showcase_theta10_v3/`
- `frozen_vs_p0_oracle_smoke_legacy_industrial/`
- `frozen_vs_p0_oracle_legacy_path_modern_tcn_demo_loop_v1/`
- `frozen_vs_p0_oracle_legacy_path_modern_tcn_demo_loop_v2/`

P0 source:

- `p0_oracle_retuning_20260602_033639/stageC/stageC_path_summary.csv`
- `p0_oracle_retuning_20260602_033639/stageC/stageC_candidate_summary.csv`
