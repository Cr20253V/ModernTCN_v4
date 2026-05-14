# ModernTCN Dataset Theta Coverage

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v6_longrun_diag2steer_balanced.mat`
- theta_mask_strategy: `nonstall_full_range`
- Source train data: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_train_data_v6_longrun_diag2steer_balanced.mat`

## Split Coverage

| split | windows | theta mask | flat | stall | slope | neg | zero | pos | strict `abs(theta)<2` | runs `<2` | `-8..-2` | `+2..+8` | `-8..-6` | `+6..+8` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 13582 | 13212 | 7421 | 370 | 5791 | 3985 | 5186 | 4041 | 7421 | 88 | 2820 | 2971 | 1441 | 1462 |
| val | 2833 | 2765 | 1638 | 68 | 1127 | 669 | 1180 | 916 | 1638 | 19 | 470 | 657 | 217 | 261 |
| test | 3036 | 2963 | 1704 | 73 | 1259 | 823 | 1169 | 971 | 1704 | 20 | 576 | 683 | 280 | 277 |

## Turn Coverage

| split | right | straight | left | straight ratio | L/R balance | slope+turn overlap | overlap ratio |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 1734 | 9830 | 2018 | 0.7238 | 0.8593 | 2088 | 0.1580 |
| val | 379 | 1910 | 544 | 0.6742 | 0.6967 | 564 | 0.2040 |
| test | 477 | 2080 | 479 | 0.6851 | 0.9958 | 561 | 0.1893 |

## Omega Proxy Bins

Proxy uses the unscaled window-end `gyro_z` feature because `omega_ref` is not stored in the prepared dataset.

| split | `[0,0.02)` | `[0.02,0.05)` | `[0.05,0.08)` | `[0.08,0.12)` | `[0.12,0.16)` | `[0.16,0.22)` | `>=0.22` |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 6543 | 1465 | 1227 | 2127 | 2204 | 16 | 0 |
| val | 1427 | 259 | 395 | 345 | 407 | 0 | 0 |
| test | 1368 | 322 | 371 | 520 | 454 | 1 | 0 |

## Radius Proxy Bins

Proxy uses `R = abs(v_hat) / abs(gyro_z)` for windows with `abs(gyro_z) >= 0.05`.

| split | `<6m` | `[6,12)m` | `[12,20)m` | `[20,40)m` | `>=40m` |
|---|---:|---:|---:|---:|---:|
| train | 271 | 2966 | 1789 | 439 | 109 |
| val | 84 | 627 | 383 | 53 | 0 |
| test | 76 | 653 | 442 | 142 | 33 |

## Theta Supervision Bins

| split | `<-8` | `[-8,-6)` | `[-6,-4)` | `[-4,-2)` | `[-2,0)` | `[0,2)` | `[2,4)` | `[4,6)` | `[6,8)` | `>=8` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 0 | 1441 | 697 | 638 | 1209 | 6256 | 504 | 1005 | 1214 | 248 |
| val | 0 | 217 | 76 | 78 | 298 | 1439 | 223 | 173 | 224 | 37 |
| test | 0 | 280 | 57 | 185 | 301 | 1457 | 178 | 228 | 136 | 141 |

## Core Theta Gate Bins

| split | `[-8,-6)` | `[-6,-4)` | `[-4,-2)` | `[-2,-0.5)` | `[0.5,2)` | `[2,4)` | `[4,6)` | `[6,8)` | zero ratio |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 1441 | 697 | 638 | 837 | 894 | 504 | 1005 | 1214 | 0.3925 |
| val | 217 | 76 | 78 | 273 | 212 | 223 | 173 | 224 | 0.4268 |
| test | 280 | 57 | 185 | 148 | 253 | 178 | 228 | 136 | 0.3945 |

## Coverage Gate

- passed: `0`
- failures:
  - val left/right balance 0.6967 is below 0.7000.

## Train Feature Side Stats

| feature | neg mean | neg std | pos mean | pos std | r neg | r pos |
|---|---:|---:|---:|---:|---:|---:|
| accel_x | -0.0136 | 0.4743 | 0.0069 | 0.0996 | 0.0147 | 0.0198 |
| gyro_y | -0.0902 | 0.8360 | 0.0847 | 0.7862 | 0.0046 | -0.0032 |
| I_lf | -0.7445 | 0.8418 | 0.7513 | 0.7206 | 0.2612 | 0.3443 |
| I_rr | -0.7606 | 0.8249 | 0.6103 | 0.7292 | 0.2659 | 0.2573 |
| omega_wheel_lf | -0.0417 | 1.1403 | -0.0635 | 0.3258 | -0.0383 | 0.2874 |
| omega_wheel_rr | -0.0424 | 1.1668 | -0.0547 | 0.3178 | -0.0371 | 0.3100 |
| v_hat | -0.0421 | 1.1537 | -0.0592 | 0.3195 | -0.0377 | 0.3009 |
| dv_hat_dt | -0.0307 | 0.9324 | 0.0158 | 0.2075 | 0.0226 | 0.0155 |
| I_sum | 0.2825 | 0.8464 | 0.3907 | 0.5588 | -0.4179 | 0.6931 |
| accel_x_lp | -0.0358 | 1.0133 | 0.0176 | 0.2229 | 0.0247 | 0.0124 |
| pitch_angle_est | -0.3623 | 1.1076 | 0.3670 | 1.0057 | 0.0191 | -0.0254 |
