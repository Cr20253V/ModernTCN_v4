# Node 6 Full-Route Oracle-Slope MPC Validation

- Timestamp: `2026-05-31 17:39:42`
- Scope: `Np=30`, `Nc=10`, oracle slope from `ref.theta_ref`.
- Node 7 status: skipped; no training data regeneration was run.
- LPV database: `E:\Matlab\Simulink\S-Function_16\data\models\lin_agv_db.mat`
- Node 6 maps: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\06_mpc_retuning\maps_best_agv_physics_v2_node06.mat`
- Summary CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\06_mpc_retuning\node06_full_route_oracle_summary_20260531_173941.csv`
- MAT result: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\06_mpc_retuning\node06_full_route_oracle_validation_20260531_173941.mat`

| path | status | fail | completion | J | e_y RMSE | e_psi RMSE | e_v RMSE | e_omega RMSE | cons Linf | F peak | omega peak | F sat % | omega sat % | avg solve ms | elapsed s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `path_closed_loop_long_updown_theta10_v1` | ok | 0 | 1.0000 | 56.3789 | 0.952183 | 0.146699 | 0.119901 | 0.0824108 | 1.04234 | 660.272 | 0.534626 | 0.500 | 0.000 | 8.545 | 103.0 |
