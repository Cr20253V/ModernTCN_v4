# AGV Theta10 Uniform Dataset Coverage

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v1.mat`
- horizon_steps: `0`
- theta_mask_strategy: `nonstall_full_range`
- Source train data: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v1.mat`

## Split Summary

| split | windows | runs | theta mask | flat | stall | slope | nonzero turn ratio | straight ratio | L/R balance | slope+turn overlap | zero abs ratio | bin imbalance | bin CV |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 17497 | 68 | 17019 | 3694 | 478 | 13325 | 0.4405 | 0.5595 | 0.9318 | 0.3600 | 0.0175 | 2.241 | 0.191 |
| val | 3333 | 14 | 3255 | 649 | 78 | 2606 | 0.3762 | 0.6238 | 0.8857 | 0.2995 | 0.0006 | 6.755 | 0.641 |
| test | 3511 | 16 | 3406 | 612 | 105 | 2794 | 0.4161 | 0.5839 | 0.9402 | 0.3347 | 0.0097 | 9.700 | 0.680 |

## Theta One-Degree Bins

| split | `[-10,-9)` | `[-9,-8)` | `[-8,-7)` | `[-7,-6)` | `[-6,-5)` | `[-5,-4)` | `[-4,-3)` | `[-3,-2)` | `[-2,-1)` | `[-1,0)` | `[0,1)` | `[1,2)` | `[2,3)` | `[3,4)` | `[4,5)` | `[5,6)` | `[6,7)` | `[7,8)` | `[8,9)` | `[9,10)` | out of range |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 631 | 922 | 674 | 905 | 692 | 787 | 1000 | 933 | 1042 | 758 | 1050 | 844 | 921 | 1074 | 694 | 816 | 896 | 1080 | 818 | 482 | 0 |
| val | 358 | 72 | 79 | 255 | 69 | 251 | 54 | 207 | 67 | 245 | 248 | 89 | 196 | 66 | 67 | 203 | 53 | 73 | 246 | 357 | 0 |
| test | 40 | 209 | 359 | 74 | 388 | 196 | 71 | 66 | 71 | 199 | 88 | 254 | 70 | 93 | 342 | 180 | 182 | 83 | 80 | 361 | 0 |

## Turn Labels

| split | right | straight | left |
|---|---:|---:|---:|
| train | 3990 | 9789 | 3718 |
| val | 665 | 2079 | 589 |
| test | 708 | 2050 | 753 |

## Omega Proxy Bins

Proxy: unscaled window-end `gyro_z`.

| split | `[0,0.02)` | `[0.02,0.05)` | `[0.05,0.08)` | `[0.08,0.12)` | `[0.12,0.16)` | `[0.16,0.22)` | `>=0.22` |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 3915 | 1290 | 1595 | 3374 | 7234 | 89 | 0 |
| val | 1063 | 222 | 273 | 598 | 1170 | 7 | 0 |
| test | 939 | 223 | 284 | 403 | 1638 | 24 | 0 |

## Radius Proxy Bins

Proxy: `R = abs(v_hat) / abs(gyro_z)` for `abs(gyro_z) >= 0.05`.

| split | `<6` | `[6,8)` | `[8,10)` | `[10,12)` | `[12,16)` | `[16,20)` | `>=20` |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 1709 | 3072 | 1238 | 709 | 1009 | 589 | 3966 |
| val | 257 | 307 | 346 | 121 | 191 | 164 | 662 |
| test | 497 | 790 | 274 | 118 | 145 | 80 | 445 |

## Steering Proxy Bins

Proxy: max absolute unscaled `delta_lf`/`delta_rr` at the window end, in degrees.

| split | `[0,2)` | `[2,5)` | `[5,10)` | `[10,15)` | `[15,20)` | `[20,30)` | `>=30` |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 8001 | 2893 | 4667 | 1909 | 27 | 0 | 0 |
| val | 1689 | 631 | 747 | 266 | 0 | 0 | 0 |
| test | 1446 | 405 | 1118 | 522 | 20 | 0 | 0 |

## Coverage Gate

- passed: `0`
- failures:
  - train theta bin imbalance 2.241 exceeds 1.500.
  - val theta bin imbalance 6.755 exceeds 1.500.
  - test theta bin imbalance 9.700 exceeds 1.500.
