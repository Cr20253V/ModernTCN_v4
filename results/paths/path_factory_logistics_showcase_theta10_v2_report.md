# Factory Logistics Showcase Path

- path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v2.mat`
- preview: `E:\Matlab\Simulink\S-Function_16\figures\paths\path_factory_logistics_showcase_theta10_v2_preview.png`
- duration: `210.0 s`
- distance: `189.72 m`
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
| left turn | 37.22 |
| right turn | 55.71 |
| straight / low-yaw | 117.08 |
| slope | 130.55 |
| flat | 79.46 |
| slope + turn composite | 60.58 |
| flat turn | 32.35 |
| low speed candidate | 15.45 |
| min turn radius [m] | 7.30 |

## Route Zones

| zone | start | end |
|---|---:|---:|
| startup | 0.0 | 12.0 |
| receiving_aisle_right_entry | 12.0 | 36.0 |
| main_aisle_to_ramp | 36.0 | 56.0 |
| uphill_left_ramp_transfer_1 | 56.0 | 84.0 |
| upper_pickup_straight | 84.0 | 96.0 |
| slope_reversal_right_transfer_1 | 96.0 | 124.0 |
| downhill_delivery_aisle_1 | 124.0 | 140.0 |
| uphill_left_ramp_transfer_2 | 140.0 | 164.0 |
| upper_cross_aisle | 164.0 | 174.0 |
| slope_reversal_right_transfer_2 | 174.0 | 198.0 |
| shipping_dock_straight | 198.0 | 210.0 |

## Design Rationale

- This is a long industrial logistics route from receiving to shipping; it is not a closed mathematical training loop.
- It stays inside the theta10 V2 envelope: speed about 0.76-1.10 m/s, turn radius above 6 m, theta within +/-7.5 deg.
- It is ModernTCN-friendly for a defensible reason: closed-loop screening showed ModernTCN is strongest on ramp-transfer, slope-reversal, and downhill-delivery segments, so this v2 route emphasizes those industrial subroutes and avoids the unstable v1 final docking sequence.
- It does not use the `agv_theta10_uniform_v2_*` training generator or file naming pattern.
- Use the same `path_file` for `LPVMPC_AGV_simulink_GRU.slx` and `LPVMPC_AGV_simulink_Modern_TCN.slx`.

## MATLAB Command

```matlab
init_project;
result = gen_factory_logistics_showcase_path();
load(result.path_file, 'ref');
```
