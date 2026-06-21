# E3 Feature Group Index Audit

- status: PASS
- index policy: 0-based indices are passed to PyTorch config; 1-based indices are reported for human audit.
- residual_group: `empty`
- group_names: `['yaw_steering', 'drive_current_load', 'velocity_acceleration', 'wheel_imbalance']`

| index_1based | index_0based | feature | group |
|---:|---:|---|---|
| 1 | 0 | `gyro_z` | `yaw_steering` |
| 2 | 1 | `I_lf` | `drive_current_load` |
| 3 | 2 | `I_rr` | `drive_current_load` |
| 4 | 3 | `omega_wheel_lf` | `wheel_imbalance` |
| 5 | 4 | `omega_wheel_rr` | `wheel_imbalance` |
| 6 | 5 | `delta_lf` | `yaw_steering` |
| 7 | 6 | `delta_rr` | `yaw_steering` |
| 8 | 7 | `v_hat` | `velocity_acceleration` |
| 9 | 8 | `dv_hat_dt` | `velocity_acceleration` |
| 10 | 9 | `ws_imbalance` | `wheel_imbalance` |
| 11 | 10 | `I_sum` | `drive_current_load` |
| 12 | 11 | `I_diff_signed` | `drive_current_load` |
| 13 | 12 | `I_diff_abs` | `drive_current_load` |
| 14 | 13 | `kappa_proxy` | `yaw_steering` |
| 15 | 14 | `accel_per_current` | `drive_current_load` |
| 16 | 15 | `dv_hat_dt_lp` | `velocity_acceleration` |
| 17 | 16 | `accel_x_wheel` | `velocity_acceleration` |
| 18 | 17 | `I_drive_signed` | `drive_current_load` |
| 19 | 18 | `current_per_accel` | `drive_current_load` |
| 20 | 19 | `drive_load_proxy` | `drive_current_load` |
| 21 | 20 | `a_hp` | `velocity_acceleration` |
| 22 | 21 | `yaw_consistency_error` | `yaw_steering` |
