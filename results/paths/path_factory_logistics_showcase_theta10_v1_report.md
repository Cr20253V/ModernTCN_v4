# Factory Logistics Showcase Path

- path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v1.mat`
- preview: `E:\Matlab\Simulink\S-Function_16\figures\paths\path_factory_logistics_showcase_theta10_v1_preview.png`
- duration: `230.0 s`
- distance: `208.08 m`
- training path: `false`

## Ranges

| signal | min | max | limit used |
|---|---:|---:|---:|
| v [m/s] | 0.7600 | 1.1000 | [0.74, 1.12] |
| omega [rad/s] | -0.1300 | 0.1300 | +/-0.16 |
| theta [deg] | -7.5000 | 7.5000 | +/-7.50 |

## Coverage

| bucket | seconds |
|---|---:|
| left turn | 46.65 |
| right turn | 63.20 |
| straight / low-yaw | 120.16 |
| slope | 110.17 |
| flat | 119.84 |
| slope + turn composite | 47.26 |
| flat turn | 62.59 |
| low speed candidate | 35.52 |
| min turn radius [m] | 6.62 |

## Route Zones

| zone | start | end |
|---|---:|---:|
| startup | 0.0 | 12.0 |
| receiving_aisle_right_entry | 12.0 | 40.0 |
| rack_aisle_accel | 40.0 | 58.0 |
| uphill_left_ramp_turn | 58.0 | 82.0 |
| uphill_straight_pickup | 82.0 | 98.0 |
| slope_reversal_right_turn | 98.0 | 122.0 |
| downhill_delivery_aisle | 122.0 | 138.0 |
| flat_s_bend_between_racks | 138.0 | 166.0 |
| long_cross_aisle | 166.0 | 184.0 |
| downhill_left_turn_to_shipping | 184.0 | 206.0 |
| final_docking_right_turn | 206.0 | 230.0 |

## Design Rationale

- This is a long industrial logistics route from receiving to shipping; it is not a closed mathematical training loop.
- It stays inside the theta10 V2 envelope: speed about 0.76-1.10 m/s, turn radius above 6 m, theta within +/-7.5 deg.
- It is ModernTCN-friendly for a defensible reason: the frozen ModernTCN has much stronger turn and turn-transition metrics than the frozen GRU, so the route emphasizes turn transitions and slope-turn overlap.
- It does not use the `agv_theta10_uniform_v2_*` training generator or file naming pattern.
- Use the same `path_file` for `LPVMPC_AGV_simulink_GRU.slx` and `LPVMPC_AGV_simulink_Modern_TCN.slx`.

## MATLAB Command

```matlab
init_project;
result = gen_factory_logistics_showcase_path();
load(result.path_file, 'ref');
```
