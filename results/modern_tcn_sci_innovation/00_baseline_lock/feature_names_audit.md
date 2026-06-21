# E0 Feature Names Audit

- source contract: data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_contract.json
- source snapshot: results/modern_tcn_ablation/_baseline_snapshot/baseline_identity.md
- contract input_dim: 22
- snapshot feature count: 22
- contract feature count: 22
- feature order match: True

| index_1based | contract_feature | snapshot_feature | match |
|---:|---|---|---|
| 1 | `gyro_z` | `gyro_z` | True |
| 2 | `I_lf` | `I_lf` | True |
| 3 | `I_rr` | `I_rr` | True |
| 4 | `omega_wheel_lf` | `omega_wheel_lf` | True |
| 5 | `omega_wheel_rr` | `omega_wheel_rr` | True |
| 6 | `delta_lf` | `delta_lf` | True |
| 7 | `delta_rr` | `delta_rr` | True |
| 8 | `v_hat` | `v_hat` | True |
| 9 | `dv_hat_dt` | `dv_hat_dt` | True |
| 10 | `ws_imbalance` | `ws_imbalance` | True |
| 11 | `I_sum` | `I_sum` | True |
| 12 | `I_diff_signed` | `I_diff_signed` | True |
| 13 | `I_diff_abs` | `I_diff_abs` | True |
| 14 | `kappa_proxy` | `kappa_proxy` | True |
| 15 | `accel_per_current` | `accel_per_current` | True |
| 16 | `dv_hat_dt_lp` | `dv_hat_dt_lp` | True |
| 17 | `accel_x_wheel` | `accel_x_wheel` | True |
| 18 | `I_drive_signed` | `I_drive_signed` | True |
| 19 | `current_per_accel` | `current_per_accel` | True |
| 20 | `drive_load_proxy` | `drive_load_proxy` | True |
| 21 | `a_hp` | `a_hp` | True |
| 22 | `yaw_consistency_error` | `yaw_consistency_error` | True |

Decision: feature group/index audit PASS for E0 because the 22D contract and baseline snapshot feature order match exactly.
