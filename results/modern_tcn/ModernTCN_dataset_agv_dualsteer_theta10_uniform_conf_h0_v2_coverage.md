# AGV Theta10 Uniform Dataset Coverage

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`
- horizon_steps: `0`
- theta_mask_strategy: `nonstall_full_range`
- Source train data: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`

## Split Summary

| split | windows | runs | theta mask | flat | stall | slope | nonzero turn ratio | straight ratio | L/R balance | slope+turn overlap | zero abs ratio | bin imbalance | bin CV |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 18302 | 71 | 17963 | 3739 | 339 | 14224 | 0.4628 | 0.5372 | 0.9004 | 0.3685 | 0.0144 | 1.450 | 0.128 |
| val | 2607 | 15 | 2560 | 509 | 47 | 2051 | 0.3797 | 0.6203 | 0.8966 | 0.3125 | 0.0129 | 1.448 | 0.118 |
| test | 3733 | 16 | 3616 | 757 | 117 | 2859 | 0.4139 | 0.5861 | 0.9004 | 0.3197 | 0.0003 | 1.444 | 0.138 |

## Theta One-Degree Bins

| split | `[-10,-9)` | `[-9,-8)` | `[-8,-7)` | `[-7,-6)` | `[-6,-5)` | `[-5,-4)` | `[-4,-3)` | `[-3,-2)` | `[-2,-1)` | `[-1,0)` | `[0,1)` | `[1,2)` | `[2,3)` | `[3,4)` | `[4,5)` | `[5,6)` | `[6,7)` | `[7,8)` | `[8,9)` | `[9,10)` | out of range |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 748 | 811 | 914 | 787 | 847 | 925 | 882 | 1078 | 890 | 802 | 1080 | 967 | 915 | 791 | 745 | 809 | 1012 | 1078 | 816 | 1066 | 0 |
| val | 139 | 139 | 112 | 139 | 139 | 139 | 102 | 96 | 108 | 139 | 139 | 123 | 139 | 139 | 139 | 137 | 112 | 129 | 139 | 112 | 0 |
| test | 205 | 201 | 197 | 198 | 164 | 154 | 200 | 142 | 198 | 204 | 152 | 203 | 157 | 197 | 198 | 205 | 145 | 155 | 197 | 144 | 0 |

## Turn Labels

| split | right | straight | left |
|---|---:|---:|---:|
| train | 4013 | 9832 | 4457 |
| val | 468 | 1617 | 522 |
| test | 813 | 2188 | 732 |

## Omega Proxy Bins

Proxy: unscaled window-end `gyro_z`.

| split | `[0,0.02)` | `[0.02,0.05)` | `[0.05,0.08)` | `[0.08,0.12)` | `[0.12,0.16)` | `[0.16,0.22)` | `>=0.22` |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 3958 | 1523 | 1870 | 3976 | 6903 | 72 | 0 |
| val | 626 | 146 | 202 | 512 | 1117 | 4 | 0 |
| test | 906 | 214 | 355 | 667 | 1573 | 18 | 0 |

## Radius Proxy Bins

Proxy: `R = abs(v_hat) / abs(gyro_z)` for `abs(gyro_z) >= 0.05`.

| split | `<6` | `[6,8)` | `[8,10)` | `[10,12)` | `[12,16)` | `[16,20)` | `>=20` |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 1350 | 2973 | 1466 | 965 | 1387 | 787 | 3893 |
| val | 231 | 573 | 122 | 115 | 152 | 54 | 588 |
| test | 320 | 695 | 188 | 144 | 222 | 171 | 873 |

## Steering Proxy Bins

Proxy: max absolute unscaled `delta_lf`/`delta_rr` at the window end, in degrees.

| split | `[0,2)` | `[2,5)` | `[5,10)` | `[10,15)` | `[15,20)` | `[20,30)` | `>=30` |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 7849 | 3820 | 5030 | 1581 | 22 | 0 | 0 |
| val | 1242 | 332 | 771 | 262 | 0 | 0 | 0 |
| test | 1683 | 719 | 938 | 392 | 1 | 0 | 0 |

## Coverage Gate

- passed: `1`
- failures: none
