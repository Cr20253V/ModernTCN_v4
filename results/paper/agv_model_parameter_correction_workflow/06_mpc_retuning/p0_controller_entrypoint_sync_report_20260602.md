# P0 Controller Entrypoint Sync Report

Date: 2026-06-02

## Goal

Unify the offline oracle-MPC retuning path and Simulink real-time entrypoints so that closed-loop experiments use the same controller contract.

## Selected Controller

The synchronized controller is the P0 selected candidate:

- `Np = 150`
- `Nc = 30`
- `Q = [100, 100, 15, 3]`
- `R = [3e-5, 3e-5]`
- `dR = [1e-3, 1e-3]`
- source artifact: `p0_oracle_retuning_20260602_033639/maps_best_agv_physics_v2_p0_oracle.mat`

## Code Changes

### `src/core/UpdatePlantModel.m`

- Replaced the old hardcoded phase1/phase2 BO maps with the P0 oracle maps.
- Removed the additional internal omega LPF so the Simulink entrypoint uses the same one-stage scheduling filter as the offline replay.
- Set `plant.U = [F_eq; rho_upd(2); theta_meas]`, aligning the nominal input with the LPV linearization workpoint.

### `src/core/UpdatePlantModel_gru.m`

- Applied the same P0 map replacement.
- Removed the additional internal omega LPF.
- Set `plant.U = [F_eq; rho_upd(2); theta_meas]`.

### `src/core/preloadfcn_v2.m`

- Changed target horizon from `Np=150/Nc=50` to `Np=150/Nc=30`.
- Added the P0 maps artifact as the first-priority map source.
- Changed `ctrl.mat` cache validation to check both `meta.Np` and `meta.Nc`.
- Changed fallback weights to the P0 selected `Q/R/dR`.
- After map injection, forces `ctrl.opts`, `ctrl.mpcobj.Weights`, and `ctrl.meta` back to the P0 contract and saves `ctrl.mat`.

### `src/core/preloadfcn_gru.m`

- Applied the same horizon, map source, cache validation, fallback weight, and post-injection save changes as `preloadfcn_v2.m`.

### `src/mpc/Cost_Function.m`

- Changed the standalone fallback controller from `Np=150/Nc=50` default weights to the P0 selected `Np=150/Nc=30` and `Q/R/dR`.

## Canonical Cache Update

The cached controller was rebuilt:

- updated: `data/models/ctrl.mat`
- backup: `data/models/ctrl_pre_p0_sync_20260602_153224.mat`

The rebuilt `ctrl.mat` reports:

- `ctrl.meta.Np = 150`
- `ctrl.meta.Nc = 30`
- `ctrl.opts.Q = [100, 100, 15, 3]`
- `ctrl.opts.R = [3e-5, 3e-5]`
- `ctrl.opts.dR = [1e-3, 1e-3]`
- `mean(ctrl.maps.Q_range,1) = [100, 100, 15, 3]`
- `mean(ctrl.maps.R_range,1) = [3e-5, 3e-5]`
- `mean(ctrl.maps.dR_range,1) = [1e-3, 1e-3]`

## Verification

Static check:

- `checkcode` reported no syntax errors for:
  - `src/core/UpdatePlantModel.m`
  - `src/core/UpdatePlantModel_gru.m`
  - `src/core/preloadfcn_v2.m`
  - `src/core/preloadfcn_gru.m`
  - `src/mpc/Cost_Function.m`

Runtime smoke:

- `UpdatePlantModel` and `UpdatePlantModel_gru` returned identical P0-scheduled weights for the same test `rho`.
- Both returned `plant.U = [F_eq; rho(2); theta]`, confirming nominal omega alignment.

Cache check:

- `data/models/ctrl.mat` now reports `Np=150`, `Nc=30`, and the P0 `Q/R/dR`.

Residual search:

- No old hardcoded BO maps remain in `src/core/UpdatePlantModel.m` or `src/core/UpdatePlantModel_gru.m`.
- The old BO values remain only in the comparison script/report artifacts as historical candidates.

## Decision

The offline oracle retuning path and Simulink real-time update path are now synchronized to the P0 selected controller. The current hardcoded BO maps in `UpdatePlantModel*.m` have been removed from active control code.

Node 7 was not run in this sync step.
