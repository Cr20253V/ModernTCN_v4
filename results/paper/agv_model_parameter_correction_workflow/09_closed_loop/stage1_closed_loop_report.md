# Stage 1 Plantfix Closed-Loop Report

- status: `done`
- mode: `smoke`
- plant_revision: `agv_physics_v2_plantfix`

## Preflight

| check | pass |
|---|---:|
| `plant_revision` | 1 |
| `dataset` | 1 |
| `modern_onnx` | 1 |
| `gru_model` | 1 |
| `tcn_model` | 1 |
| `oracle_ref_shell` | 1 |
| `theta0_shell` | 1 |
| `learned_shells` | 1 |
| `three_paths` | 1 |
| `oracle_not_imu` | 1 |
| `maps_candidate` | 1 |

## Oracle Provenance

- oracle entrypoint: `LPVMPC_AGV_simulink_ref.slx`
- theta0 entrypoint: `LPVMPC_AGV_simulink_IMU.slx` with `theta_mode=1`
- these are recorded as separate controller rows and are not merged.
- model phase: `smoke`
- MPC runtime override: `stage1_plantfix_p0`
- MPC maps file: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\06_mpc_retuning\maps_best_agv_physics_v2_plantfix_stage1.mat`

## Aggregate Ranking

| rank | controller | ey_rmse_mean | ey_peak_worst | j_du_mean |
|---:|---|---:|---:|---:|
| 1 | `ModernTCN` | 0 | 0 | 6.4885 |
| 2 | `GRU` | 0 | 0 | 6.4885 |
| 3 | `TCN` | 0 | 0 | 6.4885 |
| 4 | `LPV-MPC_theta0` | 0 | 0 | 6.4885 |
| 5 | `LPV-MPC_oracle_theta` | 0 | 0 | 6.4885 |
