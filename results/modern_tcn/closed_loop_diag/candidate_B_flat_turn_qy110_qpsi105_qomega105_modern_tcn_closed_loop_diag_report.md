# ModernTCN Closed-loop Diagnostic

- out file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\control_turn_tests\candidate_B_flat_turn_qy110_qpsi105_qomega105.mat`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`

## Decision Summary

- Keep ModernTCN output diagnostic-only for now; do not feed `theta_hat` or labels into MPC scheduling yet.
- The controller is not the current bottleneck: tracking errors stay small in the neutral-control run, while classifier errors concentrate in path zones.
- Main data gap: low-load flat turns are being confused with slope, and turn labels are missed in flat/composite turn zones.
- Next training revision should add targeted short samples for flat low-load turns and mild slope-turn composites, then rerun full-test and this closed-loop diagnostic.

## Readiness Checks

| check | value | threshold | pass | comment |
|---|---:|---:|---:|---|
| pure_turn_false_slope_pct | 0.786 | <= 5 | yes | Flat turn should not be classified as slope. |
| pure_turn_left_recall_pct | 93.786 | >= 80 | yes | Flat left turn should be detected before labels are used by MPC. |
| pure_turn_theta_mae_deg | 2.467 | <= 2 | no | Theta estimate should stay near zero on flat turns. |
| pure_slope_main_acc_pct | 93.900 | >= 90 | yes | Pure slope segment should be recognized consistently. |
| pure_slope_theta_mae_deg | 0.994 | <= 2 | yes | Slope magnitude error should remain below controller-use tolerance. |
| composite_turn_recall_pct | 1.100 | >= 60 | no | Composite slope-turn segment should preserve turn information. |
| closure_main_acc_pct | 100.000 | >= 90 | yes | Low-speed closure should not collapse into false slope labels. |
| closure_v_hat_ood_pct | 8.062 | <= 5 | no | High low-speed OOD rate means the dataset needs low-speed closure samples. |
| closure_accel_per_current_ood_pct | 21.781 | <= 5 | no | Large accel/current ratio OOD points to low-load sample coverage gap. |

## Per-zone Metrics

| zone | ey rmse | epsi rmse | ev rmse | theta MAE deg | main acc | turn acc | pred main 1/2/3 | pred turn -1/0/1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| startup | 0.0000 | 0.0000 | 0.0772 | 0.000 | 100.0 | 100.0 | 100.0/0.0/0.0 | 0.0/100.0/0.0 |
| golden_test | 0.0000 | 0.0000 | 0.0023 | 0.000 | 100.0 | 100.0 | 100.0/0.0/0.0 | 0.0/100.0/0.0 |
| pure_turn | 0.0284 | 0.0683 | 0.0192 | 2.467 | 99.2 | 96.8 | 99.2/0.0/0.8 | 0.0/6.2/93.8 |
| pure_slope | 0.0058 | 0.0191 | 0.1100 | 0.994 | 93.9 | 93.3 | 41.2/0.0/58.8 | 5.2/89.6/5.2 |
| composite | 0.0098 | 0.0218 | 0.0747 | 0.597 | 94.2 | 45.6 | 53.1/0.0/46.9 | 10.2/88.6/1.1 |
| closed_loop | 0.0060 | 0.0552 | 0.0112 | 1.647 | 100.0 | 91.1 | 100.0/0.0/0.0 | 2.6/26.3/71.1 |
| closure | 0.0060 | 0.0552 | 0.0112 | 1.647 | 100.0 | 91.1 | 100.0/0.0/0.0 | 2.6/26.3/71.1 |

## Top Feature Z-score by Zone

### startup

| feature | median z | p95 abs z | max abs z | pct abs z > 3 |
|---|---:|---:|---:|---:|
| v_hat | -1.841 | 1.849 | 1.889 | 0.0 |
| accel_per_current | 0.627 | 1.841 | 1.879 | 0.0 |
| omega_wheel_rr | -1.816 | 1.823 | 1.863 | 0.0 |
| omega_wheel_lf | -1.815 | 1.823 | 1.862 | 0.0 |
| I_sum | -1.328 | 1.354 | 1.354 | 0.0 |
| ws_imbalance | -1.103 | 1.103 | 1.103 | 0.0 |
| accel_x_lp | 0.166 | 0.925 | 0.932 | 0.0 |
| dv_hat_dt | 0.064 | 0.866 | 0.873 | 0.0 |

### golden_test

| feature | median z | p95 abs z | max abs z | pct abs z > 3 |
|---|---:|---:|---:|---:|
| I_sum | -1.353 | 1.353 | 1.353 | 0.0 |
| ws_imbalance | -1.103 | 1.103 | 1.103 | 0.0 |
| accel_per_current | 0.056 | 0.710 | 1.661 | 0.0 |
| accel_x_lp | -0.040 | 0.192 | 0.693 | 0.0 |
| dv_hat_dt | -0.046 | 0.154 | 0.618 | 0.0 |
| I_rr | -0.151 | 0.151 | 0.151 | 0.0 |
| I_lf | -0.135 | 0.135 | 0.135 | 0.0 |
| omega_wheel_rr | 0.076 | 0.076 | 0.340 | 0.0 |

### pure_turn

| feature | median z | p95 abs z | max abs z | pct abs z > 3 |
|---|---:|---:|---:|---:|
| delta_lf | 1.666 | 1.704 | 1.704 | 0.0 |
| kappa_proxy | 1.610 | 1.644 | 1.644 | 0.0 |
| delta_rr | -1.546 | 1.575 | 1.575 | 0.0 |
| accel_per_current | 0.050 | 1.574 | 8.929 | 2.7 |
| gyro_z | 1.166 | 1.418 | 2.477 | 0.0 |
| I_sum | -1.160 | 1.392 | 1.498 | 0.0 |
| omega_wheel_lf | -1.190 | 1.242 | 1.285 | 0.0 |
| ws_imbalance | 0.605 | 1.103 | 2.420 | 0.0 |

### pure_slope

| feature | median z | p95 abs z | max abs z | pct abs z > 3 |
|---|---:|---:|---:|---:|
| gyro_y | 0.000 | 7.022 | 16.408 | 7.8 |
| pitch_angle_est | -0.008 | 3.952 | 4.390 | 25.4 |
| accel_per_current | 0.057 | 3.050 | 11.877 | 5.2 |
| v_hat | -0.317 | 1.415 | 1.455 | 0.0 |
| omega_wheel_lf | -0.313 | 1.396 | 1.435 | 0.0 |
| omega_wheel_rr | -0.314 | 1.395 | 1.434 | 0.0 |
| I_sum | -0.149 | 1.356 | 1.540 | 0.0 |
| accel_x_lp | -0.039 | 1.296 | 1.357 | 0.0 |

### composite

| feature | median z | p95 abs z | max abs z | pct abs z > 3 |
|---|---:|---:|---:|---:|
| gyro_y | 0.000 | 5.310 | 14.831 | 7.0 |
| pitch_angle_est | 0.676 | 3.227 | 3.571 | 7.0 |
| accel_per_current | 0.054 | 2.219 | 3.786 | 0.6 |
| omega_wheel_rr | -0.325 | 1.420 | 1.456 | 0.0 |
| v_hat | -0.342 | 1.404 | 1.443 | 0.0 |
| I_sum | -0.896 | 1.388 | 1.505 | 0.0 |
| omega_wheel_lf | -0.362 | 1.350 | 1.390 | 0.0 |
| accel_x_lp | -0.043 | 1.087 | 1.151 | 0.0 |

### closed_loop

| feature | median z | p95 abs z | max abs z | pct abs z > 3 |
|---|---:|---:|---:|---:|
| accel_per_current | -0.002 | 10.135 | 12.300 | 21.8 |
| v_hat | -1.189 | 3.382 | 3.850 | 8.1 |
| omega_wheel_rr | -1.065 | 3.341 | 3.799 | 7.8 |
| omega_wheel_lf | -1.278 | 3.328 | 3.800 | 7.7 |
| I_sum | -1.346 | 1.495 | 1.505 | 0.0 |
| ws_imbalance | -0.170 | 1.078 | 1.103 | 0.0 |
| accel_x_lp | -0.058 | 0.974 | 1.003 | 0.0 |
| delta_rr | -0.928 | 0.931 | 1.389 | 0.0 |

### closure

| feature | median z | p95 abs z | max abs z | pct abs z > 3 |
|---|---:|---:|---:|---:|
| accel_per_current | -0.002 | 10.135 | 12.300 | 21.8 |
| v_hat | -1.189 | 3.382 | 3.850 | 8.1 |
| omega_wheel_rr | -1.065 | 3.341 | 3.799 | 7.8 |
| omega_wheel_lf | -1.278 | 3.328 | 3.800 | 7.7 |
| I_sum | -1.346 | 1.495 | 1.505 | 0.0 |
| ws_imbalance | -0.170 | 1.078 | 1.103 | 0.0 |
| accel_x_lp | -0.058 | 0.974 | 1.003 | 0.0 |
| delta_rr | -0.928 | 0.931 | 1.389 | 0.0 |

## Feature Distribution Compare

### train_flat_straight

| feature | median z | p95 abs z | max abs z |
|---|---:|---:|---:|
| pitch_angle_est | -0.008 | 2.104 | 3.798 |
| gyro_y | 0.000 | 1.906 | 143.053 |
| accel_per_current | 0.058 | 1.817 | 26.888 |
| omega_wheel_lf | 0.069 | 1.592 | 18.527 |
| gyro_z | 0.009 | 1.582 | 1.613 |
| delta_rr | -0.044 | 1.574 | 1.966 |
| kappa_proxy | 0.004 | 1.570 | 2.113 |
| I_diff_signed | 0.009 | 1.567 | 1.608 |

### train_flat_left

| feature | median z | p95 abs z | max abs z |
|---|---:|---:|---:|
| delta_lf | 1.165 | 1.754 | 2.055 |
| kappa_proxy | 1.151 | 1.689 | 1.960 |
| pitch_angle_est | -0.008 | 1.661 | 2.957 |
| delta_rr | -1.141 | 1.625 | 1.841 |
| omega_wheel_lf | -0.145 | 1.622 | 2.302 |
| gyro_z | 0.935 | 1.585 | 1.603 |
| I_diff_signed | 0.930 | 1.567 | 1.573 |
| I_lf | 0.689 | 1.560 | 2.417 |

### train_slope_straight

| feature | median z | p95 abs z | max abs z |
|---|---:|---:|---:|
| pitch_angle_est | -0.005 | 2.569 | 4.572 |
| gyro_y | 0.000 | 2.287 | 5.640 |
| I_rr | 0.111 | 2.112 | 2.521 |
| I_lf | 0.066 | 2.049 | 2.371 |
| I_diff_abs | -0.001 | 2.002 | 3.572 |
| delta_rr | -0.044 | 1.810 | 2.179 |
| delta_lf | -0.035 | 1.798 | 2.325 |
| kappa_proxy | 0.004 | 1.782 | 2.203 |

### sim_pure_turn

| feature | median z | p95 abs z | max abs z |
|---|---:|---:|---:|
| delta_lf | 1.666 | 1.704 | 1.704 |
| kappa_proxy | 1.610 | 1.644 | 1.644 |
| delta_rr | -1.546 | 1.575 | 1.575 |
| accel_per_current | 0.050 | 1.574 | 8.929 |
| gyro_z | 1.166 | 1.418 | 2.477 |
| I_sum | -1.160 | 1.392 | 1.498 |
| omega_wheel_lf | -1.190 | 1.242 | 1.285 |
| ws_imbalance | 0.605 | 1.103 | 2.420 |

### sim_pure_slope

| feature | median z | p95 abs z | max abs z |
|---|---:|---:|---:|
| gyro_y | 0.000 | 7.022 | 16.408 |
| pitch_angle_est | -0.008 | 3.952 | 4.390 |
| accel_per_current | 0.057 | 3.050 | 11.877 |
| v_hat | -0.317 | 1.415 | 1.455 |
| omega_wheel_lf | -0.313 | 1.396 | 1.435 |
| omega_wheel_rr | -0.314 | 1.395 | 1.434 |
| I_sum | -0.149 | 1.356 | 1.540 |
| accel_x_lp | -0.039 | 1.296 | 1.357 |

### sim_composite

| feature | median z | p95 abs z | max abs z |
|---|---:|---:|---:|
| gyro_y | 0.000 | 5.310 | 14.831 |
| pitch_angle_est | 0.676 | 3.227 | 3.571 |
| accel_per_current | 0.054 | 2.219 | 3.786 |
| omega_wheel_rr | -0.325 | 1.420 | 1.456 |
| v_hat | -0.342 | 1.404 | 1.443 |
| I_sum | -0.896 | 1.388 | 1.505 |
| omega_wheel_lf | -0.362 | 1.350 | 1.390 |
| accel_x_lp | -0.043 | 1.087 | 1.151 |

