# UpdatePlantModel Hardcoded BO vs Frozen/P0 Oracle-MPC

Date: 2026-06-02

## Scope

This report adds the currently hardcoded BO weights in `src/core/UpdatePlantModel.m` to the repaired oracle-MPC replay comparison.

Common replay conditions:

- 7 full routes with `ref.meta.zones`
- repaired offline oracle replay in `Cost_Function.m`
- oracle slope `ref.theta_ref`
- `Nominal.U(2)=omega_ref`
- no Node 7 run
- no overwrite of canonical `data/models/maps_best.mat`

Note: this comparison evaluates the hardcoded `UpdatePlantModel.m` BO maps as controller weight/constraint maps. The Mamba label-driven stall/slip override logic is not activated in this oracle-slope route replay.

## Candidate Definitions

| candidate | source | Np | Nc | Q center | R center | dR center |
|---|---|---:|---:|---|---|---|
| `updateplantmodel_hardcoded_bo` | `src/core/UpdatePlantModel.m` | 150 | 50 | `[131.0462, 16.3368, 36.7978, 0.8321]` | `[3.05e-3, 1.155e-2]` | `[3.35e-3, 2.618e-1]` |
| `frozen_maps_best` | `data/models/maps_best.mat` | 150 | 50 | `[63.0542, 48.0671, 29.5106, 1.2320]` | `[7.3636e-4, 5.2020e-4]` | `[3.4362e-3, 2.2119e-1]` |
| `p0_selected` | `p0_oracle_retuning_20260602_033639` | 150 | 30 | `[100, 100, 15, 3]` | `[3e-5, 3e-5]` | `[1e-3, 1e-3]` |

## Overall Summary

| candidate | pass <0.1 | fail | min completion | max e_y RMSE | mean e_y RMSE | max e_y peak | max cons Linf | max omega sat rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `updateplantmodel_hardcoded_bo` | 0 | 0 | 1.000 | 0.296274 | 0.103576 | 0.861889 | 0.030840 | 0.141770 |
| `frozen_maps_best` | 1 | 0 | 1.000 | 0.071500 | 0.039330 | 0.168291 | 0 | 0 |
| `p0_selected` | 1 | 0 | 1.000 | 0.062131 | 0.037755 | 0.152033 | 0 | 0 |

## Per-Path e_y RMSE

| path | UpdatePlantModel hardcoded BO | frozen maps_best | P0 selected |
|---|---:|---:|---:|
| `path_closed_loop_long_updown_theta10_v1` | 0.053279 | 0.063499 | 0.016110 |
| `path_closed_loop_sharp_turn_transition_theta10_v1` | 0.065880 | 0.022268 | 0.062131 |
| `path_factory_logistics_showcase_theta10_v10` | 0.024841 | 0.033836 | 0.044613 |
| `path_factory_logistics_showcase_theta10_v3` | 0.167783 | 0.026938 | 0.031946 |
| `path_industrial_lite` | 0.052305 | 0.016700 | 0.020223 |
| `path_modern_tcn_demo_loop_v1` | 0.296274 | 0.040570 | 0.043314 |
| `path_modern_tcn_demo_loop_v2` | 0.064670 | 0.071500 | 0.045947 |

## Diagnostics

`UpdatePlantModel.m` hardcoded BO did not fail at the QP level, but it no longer satisfies the oracle ceiling criterion:

- worst route: `path_modern_tcn_demo_loop_v1`, `e_y RMSE = 0.296274 m`
- second worst: `path_factory_logistics_showcase_theta10_v3`, `e_y RMSE = 0.167783 m`
- max peak lateral error: `0.861889 m`
- max constraint violation: `0.030840`
- max omega saturation rate: `0.141770`

The frozen and P0 candidates both keep constraint violation and omega saturation at zero in the same replay.

## Interpretation

The current `UpdatePlantModel.m` hardcoded BO maps are not suitable as the oracle-MPC ceiling after the replay/workpoint fixes. They solve numerically, but the closed-loop behavior is not robust enough on the 7-route validation set.

The likely culprit is not horizon length, because `UpdatePlantModel.m` uses the longer `Np=150/Nc=50`. The issue is the hardcoded weight/map profile:

- very low `q_psi` relative to P0 and frozen maps
- high `R_omega` and very high `dR_omega`, which can slow yaw-rate correction
- strong adaptive `q_y_gain_max` that does not prevent large route-specific peak errors

For Node 7, the current evidence supports using P0 selected as the safer worst-case candidate, while keeping frozen `maps_best.mat` as a strong baseline. The hardcoded `UpdatePlantModel.m` BO maps should not be used unchanged for the paper oracle ceiling.

## Source Artifacts

UpdatePlantModel hardcoded BO replay:

- `updateplantmodel_hardcoded_bo_oracle_20260602/frozen_vs_p0_candidate_summary.csv`
- `updateplantmodel_hardcoded_bo_oracle_20260602/frozen_vs_p0_path_summary.csv`
- `updateplantmodel_hardcoded_bo_oracle_20260602/frozen_vs_p0_oracle_comparison_report.md`

Previous frozen/P0 comparison:

- `frozen_vs_p0_oracle_comparison_summary_20260602.md`
- `p0_oracle_retuning_20260602_033639/stageC/stageC_path_summary.csv`
