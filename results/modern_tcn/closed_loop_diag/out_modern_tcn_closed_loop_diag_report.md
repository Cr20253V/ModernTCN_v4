# ModernTCN Closed-loop Diagnostic

- out file: `E:\Matlab\Simulink\S-Function_16\out.mat`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`

## Decision Summary

- Keep ModernTCN output diagnostic-only for now; do not feed `theta_hat` or labels into MPC scheduling yet.
- The controller is not the current bottleneck: tracking errors stay small in the neutral-control run, while classifier errors concentrate in path zones.
- Main data gap: low-load flat turns are being confused with slope, and turn labels are missed in flat/composite turn zones.
- Next training revision should add targeted short samples for flat low-load turns and mild slope-turn composites, then rerun full-test and this closed-loop diagnostic.

## Readiness Checks

| check | value | threshold | pass | comment |
|---|---:|---:|---:|---|
| pure_turn_false_slope_pct | 39.107 | <= 5 | no | Flat turn should not be classified as slope. |
| pure_turn_left_recall_pct | 0.000 | >= 80 | no | Flat left turn should be detected before labels are used by MPC. |
| pure_turn_theta_mae_deg | 1.107 | <= 2 | yes | Theta estimate should stay near zero on flat turns. |
| pure_slope_main_acc_pct | 93.300 | >= 90 | yes | Pure slope segment should be recognized consistently. |
| pure_slope_theta_mae_deg | 0.847 | <= 2 | yes | Slope magnitude error should remain below controller-use tolerance. |
| composite_turn_recall_pct | 0.000 | >= 60 | no | Composite slope-turn segment should preserve turn information. |
| closure_main_acc_pct | 68.562 | >= 90 | no | Low-speed closure should not collapse into false slope labels. |
| closure_v_hat_ood_pct | 0.000 | <= 5 | yes | High low-speed OOD rate means the dataset needs low-speed closure samples. |
| closure_accel_per_current_ood_pct | 0.000 | <= 5 | yes | Large accel/current ratio OOD points to low-load sample coverage gap. |

## Per-zone Metrics

| zone | ey rmse | epsi rmse | ev rmse | theta MAE deg | main acc | turn acc | pred main 1/2/3 | pred turn -1/0/1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| startup | 0.0025 | 0.0012 | 0.1208 | 0.000 | 100.0 | 100.0 | 100.0/0.0/0.0 | 0.0/100.0/0.0 |
| golden_test | 0.0321 | 0.0184 | 0.0020 | 0.712 | 100.0 | 36.9 | 100.0/0.0/0.0 | 6.0/94.0/0.0 |
| pure_turn | 0.0116 | 0.0142 | 0.0601 | 1.107 | 97.9 | 29.6 | 60.9/0.0/39.1 | 0.0/100.0/0.0 |
| pure_slope | 0.0022 | 0.0059 | 0.0774 | 0.847 | 93.3 | 100.0 | 28.0/0.0/72.0 | 0.0/100.0/0.0 |
| composite | 0.0020 | 0.0055 | 0.0729 | 0.738 | 97.5 | 68.3 | 49.5/0.0/50.5 | 7.0/93.0/0.0 |
| closed_loop | 0.0473 | 0.1040 | 0.0706 | 1.846 | 68.6 | 60.0 | 52.4/0.0/47.6 | 0.0/40.0/60.0 |
| closure | 0.0473 | 0.1040 | 0.0706 | 1.846 | 68.6 | 60.0 | 52.4/0.0/47.6 | 0.0/40.0/60.0 |

## Top Feature Z-score by Zone

### startup

| feature | median z | p95 abs z | max abs z | pct abs z > 3 |
|---|---:|---:|---:|---:|
| accel_per_current | -0.259 | 1.292 | 1.745 | 0.0 |
| I_sum | -1.084 | 1.087 | 1.087 | 0.0 |
| ws_imbalance | -0.768 | 0.824 | 0.824 | 0.0 |
| omega_wheel_rr | -0.609 | 0.784 | 0.790 | 0.0 |
| v_hat | -0.610 | 0.781 | 0.786 | 0.0 |
| omega_wheel_lf | -0.593 | 0.755 | 0.759 | 0.0 |
| accel_x_lp | -0.086 | 0.649 | 1.147 | 0.0 |
| dv_hat_dt | -0.088 | 0.218 | 0.323 | 0.0 |

### golden_test

| feature | median z | p95 abs z | max abs z | pct abs z > 3 |
|---|---:|---:|---:|---:|
| gyro_z | -0.601 | 2.368 | 4.035 | 0.9 |
| delta_rr | 0.649 | 2.242 | 2.249 | 0.0 |
| ws_imbalance | -0.050 | 2.185 | 4.169 | 0.8 |
| kappa_proxy | -0.662 | 2.146 | 2.152 | 0.0 |
| delta_lf | -0.681 | 2.037 | 2.043 | 0.0 |
| I_sum | -1.058 | 1.072 | 1.701 | 0.0 |
| omega_wheel_lf | -0.165 | 0.808 | 0.993 | 0.0 |
| omega_wheel_rr | -0.361 | 0.766 | 0.791 | 0.0 |

### pure_turn

| feature | median z | p95 abs z | max abs z | pct abs z > 3 |
|---|---:|---:|---:|---:|
| delta_rr | 0.532 | 1.856 | 2.037 | 0.0 |
| gyro_z | -0.469 | 1.829 | 2.227 | 0.0 |
| pitch_angle_est | -0.003 | 1.794 | 1.911 | 0.0 |
| kappa_proxy | -0.550 | 1.793 | 1.959 | 0.0 |
| delta_lf | -0.572 | 1.729 | 1.875 | 0.0 |
| ws_imbalance | -0.224 | 1.510 | 2.010 | 0.0 |
| omega_wheel_rr | -0.617 | 1.140 | 1.142 | 0.0 |
| I_sum | -0.806 | 1.078 | 1.099 | 0.0 |

### pure_slope

| feature | median z | p95 abs z | max abs z | pct abs z > 3 |
|---|---:|---:|---:|---:|
| gyro_y | -0.000 | 6.981 | 8.448 | 9.6 |
| pitch_angle_est | -0.927 | 1.910 | 1.972 | 0.0 |
| I_sum | -0.241 | 1.162 | 1.291 | 0.0 |
| I_rr | -0.143 | 1.057 | 1.068 | 0.0 |
| I_lf | -0.173 | 1.019 | 1.030 | 0.0 |
| v_hat | -0.026 | 0.881 | 0.925 | 0.0 |
| omega_wheel_lf | -0.029 | 0.877 | 0.920 | 0.0 |
| omega_wheel_rr | -0.022 | 0.857 | 0.900 | 0.0 |

### composite

| feature | median z | p95 abs z | max abs z | pct abs z > 3 |
|---|---:|---:|---:|---:|
| gyro_y | -0.000 | 4.283 | 8.448 | 6.0 |
| pitch_angle_est | 0.216 | 1.837 | 1.908 | 0.0 |
| accel_per_current | 0.085 | 1.363 | 3.548 | 2.2 |
| omega_wheel_lf | -0.908 | 1.185 | 1.195 | 0.0 |
| v_hat | -0.894 | 1.185 | 1.195 | 0.0 |
| I_sum | -0.914 | 1.161 | 1.250 | 0.0 |
| omega_wheel_rr | -0.852 | 1.147 | 1.158 | 0.0 |
| I_rr | -0.394 | 1.054 | 1.055 | 0.0 |

### closed_loop

| feature | median z | p95 abs z | max abs z | pct abs z > 3 |
|---|---:|---:|---:|---:|
| gyro_y | -0.000 | 6.290 | 13.824 | 8.2 |
| pitch_angle_est | 0.099 | 2.888 | 3.132 | 3.4 |
| gyro_z | 1.363 | 2.754 | 3.605 | 1.1 |
| ws_imbalance | 0.927 | 2.679 | 3.716 | 1.0 |
| delta_lf | 1.524 | 2.229 | 2.234 | 0.0 |
| kappa_proxy | 1.487 | 2.134 | 2.139 | 0.0 |
| delta_rr | -1.454 | 2.028 | 2.032 | 0.0 |
| omega_wheel_rr | 0.423 | 1.576 | 1.846 | 0.0 |

### closure

| feature | median z | p95 abs z | max abs z | pct abs z > 3 |
|---|---:|---:|---:|---:|
| gyro_y | -0.000 | 6.290 | 13.824 | 8.2 |
| pitch_angle_est | 0.099 | 2.888 | 3.132 | 3.4 |
| gyro_z | 1.363 | 2.754 | 3.605 | 1.1 |
| ws_imbalance | 0.927 | 2.679 | 3.716 | 1.0 |
| delta_lf | 1.524 | 2.229 | 2.234 | 0.0 |
| kappa_proxy | 1.487 | 2.134 | 2.139 | 0.0 |
| delta_rr | -1.454 | 2.028 | 2.032 | 0.0 |
| omega_wheel_rr | 0.423 | 1.576 | 1.846 | 0.0 |

## Feature Distribution Compare

### train_flat_straight

| feature | median z | p95 abs z | max abs z |
|---|---:|---:|---:|
| pitch_angle_est | -0.003 | 2.471 | 3.515 |
| gyro_y | -0.000 | 2.259 | 3.687 |
| I_diff_signed | -0.002 | 2.018 | 2.321 |
| gyro_z | -0.003 | 1.997 | 2.392 |
| delta_rr | -0.023 | 1.796 | 3.398 |
| ws_imbalance | -0.824 | 1.792 | 2.942 |
| kappa_proxy | -0.006 | 1.791 | 3.187 |
| delta_lf | -0.035 | 1.780 | 2.920 |

### train_flat_left

| feature | median z | p95 abs z | max abs z |
|---|---:|---:|---:|
| I_diff_abs | 0.420 | 2.414 | 5.281 |
| delta_lf | 1.459 | 2.374 | 3.366 |
| gyro_z | 1.428 | 2.309 | 2.326 |
| I_diff_signed | 1.411 | 2.282 | 2.333 |
| kappa_proxy | 1.426 | 2.267 | 3.159 |
| delta_rr | -1.398 | 2.141 | 2.874 |
| ws_imbalance | 0.998 | 2.124 | 2.146 |
| I_lf | 1.062 | 1.971 | 3.235 |

### train_slope_straight

| feature | median z | p95 abs z | max abs z |
|---|---:|---:|---:|
| gyro_y | -0.000 | 2.880 | 3.687 |
| pitch_angle_est | -0.002 | 2.502 | 3.516 |
| accel_x_lp | 0.017 | 2.283 | 21.602 |
| dv_hat_dt | 0.009 | 2.244 | 23.370 |
| I_diff_abs | 0.006 | 2.204 | 5.519 |
| I_rr | 0.140 | 1.904 | 3.384 |
| I_diff_signed | -0.002 | 1.892 | 2.344 |
| gyro_z | -0.003 | 1.884 | 2.359 |

### sim_pure_turn

| feature | median z | p95 abs z | max abs z |
|---|---:|---:|---:|
| delta_rr | 0.532 | 1.856 | 2.037 |
| gyro_z | -0.469 | 1.829 | 2.227 |
| pitch_angle_est | -0.003 | 1.794 | 1.911 |
| kappa_proxy | -0.550 | 1.793 | 1.959 |
| delta_lf | -0.572 | 1.729 | 1.875 |
| ws_imbalance | -0.224 | 1.510 | 2.010 |
| omega_wheel_rr | -0.617 | 1.140 | 1.142 |
| I_sum | -0.806 | 1.078 | 1.099 |

### sim_pure_slope

| feature | median z | p95 abs z | max abs z |
|---|---:|---:|---:|
| gyro_y | -0.000 | 6.981 | 8.448 |
| pitch_angle_est | -0.927 | 1.910 | 1.972 |
| I_sum | -0.241 | 1.162 | 1.291 |
| I_rr | -0.143 | 1.057 | 1.068 |
| I_lf | -0.173 | 1.019 | 1.030 |
| v_hat | -0.026 | 0.881 | 0.925 |
| omega_wheel_lf | -0.029 | 0.877 | 0.920 |
| omega_wheel_rr | -0.022 | 0.857 | 0.900 |

### sim_composite

| feature | median z | p95 abs z | max abs z |
|---|---:|---:|---:|
| gyro_y | -0.000 | 4.283 | 8.448 |
| pitch_angle_est | 0.216 | 1.837 | 1.908 |
| accel_per_current | 0.085 | 1.363 | 3.548 |
| omega_wheel_lf | -0.908 | 1.185 | 1.195 |
| v_hat | -0.894 | 1.185 | 1.195 |
| I_sum | -0.914 | 1.161 | 1.250 |
| omega_wheel_rr | -0.852 | 1.147 | 1.158 |
| I_rr | -0.394 | 1.054 | 1.055 |

