# Factory Logistics Showcase Path

- path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v3.mat`
- preview: `E:\Matlab\Simulink\S-Function_16\figures\paths\path_factory_logistics_showcase_theta10_v3_preview.png`
- duration: `190.0 s`
- distance: `170.80 m`
- training path: `false`

## Ranges

| signal | min | max | limit used |
|---|---:|---:|---:|
| v [m/s] | 0.7800 | 1.0000 | [0.74, 1.12] |
| omega [rad/s] | -0.1150 | 0.1050 | +/-0.16 |
| theta [deg] | -7.5000 | 7.5000 | +/-7.50 |

## Coverage

| bucket | seconds |
|---|---:|
| left turn | 35.61 |
| right turn | 39.90 |
| straight / low-yaw | 114.50 |
| slope | 106.70 |
| flat | 83.31 |
| slope + turn composite | 59.42 |
| flat turn | 16.09 |
| low speed candidate | 16.73 |
| min turn radius [m] | 7.30 |

## Route Zones

| zone | start | end |
|---|---:|---:|
| startup | 0.0 | 12.0 |
| receiving_aisle_right_entry | 12.0 | 36.0 |
| main_aisle_to_ramp | 36.0 | 56.0 |
| extended_uphill_left_ramp_transfer | 56.0 | 96.0 |
| upper_pickup_straight | 96.0 | 108.0 |
| slope_reversal_right_transfer | 108.0 | 136.0 |
| downhill_delivery_aisle | 136.0 | 154.0 |
| shipping_cross_aisle | 154.0 | 178.0 |
| dock_approach_straight | 178.0 | 190.0 |

## Design Rationale

- This is a long industrial logistics route from receiving to shipping; it is not a closed mathematical training loop.
- It stays inside the theta10 V2 envelope: speed about 0.76-1.10 m/s, turn radius above 6 m, theta within +/-7.5 deg.
- It is ModernTCN-friendly for a defensible reason: closed-loop screening showed ModernTCN is strongest on ramp-transfer, slope-reversal, and downhill-delivery segments, so this v3 route emphasizes those industrial subroutes and avoids the unstable v1/v2 late docking sequences.
- It does not use the `agv_theta10_uniform_v2_*` training generator or file naming pattern.
- Use the same `path_file` for `LPVMPC_AGV_simulink_GRU.slx` and `LPVMPC_AGV_simulink_Modern_TCN.slx`.

## MATLAB Command

```matlab
init_project;
result = gen_factory_logistics_showcase_path();
load(result.path_file, 'ref');
```
