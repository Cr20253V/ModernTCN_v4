# Node 6 Full-Route Oracle-Slope MPC Validation

- Timestamp: `2026-05-31 18:22:28`
- Scope: `Np=30`, `Nc=10`, oracle slope from `ref.theta_ref`.
- Node 7 status: skipped; no training data regeneration was run.
- LPV database: `E:\Matlab\Simulink\S-Function_16\data\models\lin_agv_db.mat`
- Node 6 maps: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\06_mpc_retuning\maps_best_agv_physics_v2_node06.mat`
- Summary CSV: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\06_mpc_retuning\node06_full_route_oracle_summary_20260531_182228.csv`
- MAT result: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\06_mpc_retuning\node06_full_route_oracle_validation_20260531_182228.mat`

| path | status | fail | completion | J | e_y RMSE | e_psi RMSE | e_v RMSE | e_omega RMSE | cons Linf | F peak | omega peak | F sat % | omega sat % | avg solve ms | elapsed s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `path_closed_loop_long_updown_theta10_v1` | ok | 0 | 1.0000 | 56.3736 | 0.952183 | 0.146699 | 0.119901 | 0.0824108 | 1.04234 | 660.272 | 0.534626 | 0.500 | 0.000 | 8.519 | 102.9 |
| `path_closed_loop_sharp_turn_transition_theta10_v1` | ok | 0 | 1.0000 | 88.6412 | 1.30222 | 0.180022 | 0.111573 | 0.0596381 | 1.64325 | 660 | 0.91542 | 0.000 | 0.000 | 7.661 | 115.2 |
| `path_factory_logistics_showcase_theta10_v10` | ok | 0 | 1.0000 | 283.01 | 2.17547 | 0.0248411 | 0.0690864 | 0.0135181 | 5.42592 | 660 | 0.215501 | 0.041 | 0.000 | 7.989 | 544.7 |
| `path_factory_logistics_showcase_theta10_v3` | ok | 0 | 1.0000 | 279.752 | 2.57865 | 0.335001 | 0.117256 | 0.0870469 | 5.2607 | 665.25 | 1.3315 | 0.411 | 5.910 | 8.258 | 434.7 |
| `path_industrial_lite` | ok | 0 | 1.0000 | 57.4786 | 0.954058 | 0.0934106 | 0.0718286 | 0.0469595 | 1.06486 | 660.722 | 1.20505 | 0.340 | 0.000 | 7.985 | 335.5 |
| `path_modern_tcn_demo_loop_v1` | ok | 0 | 1.0000 | 160.7 | 1.86593 | 0.147124 | 0.0700351 | 0.0641578 | 3.00484 | 667.726 | 1.33551 | 0.067 | 1.839 | 8.254 | 412.7 |
| `path_modern_tcn_demo_loop_v2` | ok | 0 | 1.0000 | 200.857 | 1.93833 | 0.157655 | 0.0706914 | 0.0670762 | 3.77336 | 664.488 | 1.31104 | 0.161 | 0.000 | 8.275 | 413.6 |
