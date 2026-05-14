# AGV Theta10 Uniform Dataset Coverage

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v1_balance_probe.mat`
- horizon_steps: `0`
- theta_mask_strategy: `nonstall_full_range`
- Source train data: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v1.mat`

## Split Summary

| split | windows | runs | theta mask | flat | stall | slope | nonzero turn ratio | straight ratio | L/R balance | slope+turn overlap | zero abs ratio | bin imbalance | bin CV |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 12259 | 68 | 11732 | 2436 | 527 | 9296 | 0.4230 | 0.5770 | 0.9014 | 0.3440 | 0.0152 | 1.450 | 0.096 |
| val | 4268 | 14 | 4226 | 888 | 42 | 3338 | 0.4358 | 0.5642 | 0.9538 | 0.3469 | 0.0047 | 1.446 | 0.133 |
| test | 3698 | 16 | 3606 | 741 | 92 | 2865 | 0.4248 | 0.5752 | 0.9276 | 0.3636 | 0.0086 | 1.445 | 0.131 |

## Theta One-Degree Bins

| split | `[-10,-9)` | `[-9,-8)` | `[-8,-7)` | `[-7,-6)` | `[-6,-5)` | `[-5,-4)` | `[-4,-3)` | `[-3,-2)` | `[-2,-1)` | `[-1,0)` | `[0,1)` | `[1,2)` | `[2,3)` | `[3,4)` | `[4,5)` | `[5,6)` | `[6,7)` | `[7,8)` | `[8,9)` | `[9,10)` | out of range |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 507 | 609 | 609 | 609 | 420 | 609 | 609 | 609 | 609 | 609 | 609 | 609 | 609 | 609 | 609 | 609 | 452 | 609 | 609 | 609 | 0 |
| val | 238 | 179 | 183 | 240 | 240 | 211 | 172 | 176 | 199 | 209 | 240 | 240 | 240 | 210 | 166 | 173 | 240 | 203 | 240 | 227 | 0 |
| test | 198 | 198 | 198 | 169 | 198 | 148 | 137 | 198 | 198 | 198 | 147 | 198 | 164 | 198 | 198 | 173 | 198 | 198 | 149 | 143 | 0 |

## Turn Labels

| split | right | straight | left |
|---|---:|---:|---:|
| train | 2727 | 7074 | 2458 |
| val | 952 | 2408 | 908 |
| test | 756 | 2127 | 815 |

## Omega Proxy Bins

Proxy: unscaled window-end `gyro_z`.

| split | `[0,0.02)` | `[0.02,0.05)` | `[0.05,0.08)` | `[0.08,0.12)` | `[0.12,0.16)` | `[0.16,0.22)` | `>=0.22` |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 3276 | 1064 | 1151 | 1877 | 4832 | 59 | 0 |
| val | 779 | 158 | 355 | 1193 | 1743 | 40 | 0 |
| test | 857 | 205 | 286 | 653 | 1693 | 4 | 0 |

## Radius Proxy Bins

Proxy: `R = abs(v_hat) / abs(gyro_z)` for `abs(gyro_z) >= 0.05`.

| split | `<6` | `[6,8)` | `[8,10)` | `[10,12)` | `[12,16)` | `[16,20)` | `>=20` |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 1368 | 2078 | 1072 | 544 | 687 | 459 | 1711 |
| val | 330 | 463 | 231 | 104 | 170 | 86 | 1947 |
| test | 338 | 824 | 214 | 144 | 229 | 161 | 726 |

## Steering Proxy Bins

Proxy: max absolute unscaled `delta_lf`/`delta_rr` at the window end, in degrees.

| split | `[0,2)` | `[2,5)` | `[5,10)` | `[10,15)` | `[15,20)` | `[20,30)` | `>=30` |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 5215 | 2056 | 3481 | 1460 | 47 | 0 | 0 |
| val | 2682 | 479 | 749 | 358 | 0 | 0 | 0 |
| test | 1499 | 713 | 1085 | 401 | 0 | 0 | 0 |

## Coverage Gate

- passed: `1`
- failures: none
