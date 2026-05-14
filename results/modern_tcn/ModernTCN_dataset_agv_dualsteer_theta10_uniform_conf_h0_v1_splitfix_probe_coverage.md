# AGV Theta10 Uniform Dataset Coverage

- Dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v1_splitfix_probe.mat`
- horizon_steps: `0`
- theta_mask_strategy: `nonstall_full_range`
- Source train data: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v1.mat`

## Split Summary

| split | windows | runs | theta mask | flat | stall | slope | nonzero turn ratio | straight ratio | L/R balance | slope+turn overlap | zero abs ratio | bin imbalance | bin CV |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 14816 | 68 | 14289 | 3049 | 527 | 11240 | 0.4291 | 0.5709 | 0.8928 | 0.3441 | 0.0188 | 2.214 | 0.187 |
| val | 4957 | 14 | 4915 | 1001 | 42 | 3914 | 0.4325 | 0.5675 | 0.8923 | 0.3469 | 0.0057 | 2.819 | 0.330 |
| test | 4568 | 16 | 4476 | 905 | 92 | 3571 | 0.4205 | 0.5795 | 0.8295 | 0.3619 | 0.0078 | 2.255 | 0.275 |

## Theta One-Degree Bins

| split | `[-10,-9)` | `[-9,-8)` | `[-8,-7)` | `[-7,-6)` | `[-6,-5)` | `[-5,-4)` | `[-4,-3)` | `[-3,-2)` | `[-2,-1)` | `[-1,0)` | `[0,1)` | `[1,2)` | `[2,3)` | `[3,4)` | `[4,5)` | `[5,6)` | `[6,7)` | `[7,8)` | `[8,9)` | `[9,10)` | out of range |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | 507 | 750 | 629 | 753 | 420 | 875 | 816 | 750 | 748 | 742 | 930 | 629 | 676 | 763 | 693 | 853 | 452 | 757 | 716 | 830 | 0 |
| val | 238 | 179 | 183 | 312 | 468 | 211 | 172 | 176 | 199 | 209 | 309 | 284 | 347 | 210 | 166 | 173 | 370 | 203 | 279 | 227 | 0 |
| test | 284 | 274 | 300 | 169 | 261 | 148 | 137 | 280 | 233 | 251 | 147 | 274 | 164 | 260 | 244 | 173 | 309 | 276 | 149 | 143 | 0 |

## Turn Labels

| split | right | straight | left |
|---|---:|---:|---:|
| train | 3359 | 8458 | 2999 |
| val | 1133 | 2813 | 1011 |
| test | 871 | 2647 | 1050 |

## Omega Proxy Bins

Proxy: unscaled window-end `gyro_z`.

| split | `[0,0.02)` | `[0.02,0.05)` | `[0.05,0.08)` | `[0.08,0.12)` | `[0.12,0.16)` | `[0.16,0.22)` | `>=0.22` |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 3900 | 1265 | 1404 | 2252 | 5924 | 71 | 0 |
| val | 948 | 197 | 402 | 1333 | 2032 | 45 | 0 |
| test | 1069 | 273 | 346 | 790 | 2086 | 4 | 0 |

## Radius Proxy Bins

Proxy: `R = abs(v_hat) / abs(gyro_z)` for `abs(gyro_z) >= 0.05`.

| split | `<6` | `[6,8)` | `[8,10)` | `[10,12)` | `[12,16)` | `[16,20)` | `>=20` |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 1643 | 2537 | 1334 | 648 | 851 | 558 | 2080 |
| val | 405 | 576 | 267 | 127 | 209 | 94 | 2134 |
| test | 415 | 1056 | 257 | 173 | 285 | 181 | 859 |

## Steering Proxy Bins

Proxy: max absolute unscaled `delta_lf`/`delta_rr` at the window end, in degrees.

| split | `[0,2)` | `[2,5)` | `[5,10)` | `[10,15)` | `[15,20)` | `[20,30)` | `>=30` |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 6246 | 2501 | 4255 | 1767 | 47 | 0 | 0 |
| val | 3040 | 567 | 917 | 433 | 0 | 0 | 0 |
| test | 1850 | 861 | 1360 | 497 | 0 | 0 | 0 |

## Coverage Gate

- passed: `0`
- failures:
  - train theta bin imbalance 2.214 exceeds 1.500.
  - val theta bin imbalance 2.819 exceeds 1.500.
  - test theta bin imbalance 2.255 exceeds 1.500.
  - test left/right balance 0.8295 is below 0.8500.
