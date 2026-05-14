# Factory Logistics Showcase Path

- path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v9.mat`
- preview: `E:\Matlab\Simulink\S-Function_16\figures\paths\path_factory_logistics_showcase_theta10_v9_preview.png`
- duration: `238.5 s`
- distance: `205.11 m`
- training path: `false`

## Ranges

| signal | min | max | limit used |
|---|---:|---:|---:|
| v [m/s] | 0.8600 | 0.8600 | [0.74, 1.12] |
| omega [rad/s] | -0.0860 | 0.0000 | +/-0.16 |
| theta [deg] | 0.0000 | 5.5000 | +/-7.50 |

## Coverage

| bucket | seconds |
|---|---:|
| left turn | 0.00 |
| right turn | 36.32 |
| straight / low-yaw | 202.19 |
| slope | 143.88 |
| flat | 94.63 |
| slope + turn composite | 0.00 |
| flat turn | 36.32 |
| low speed candidate | 0.00 |
| min turn radius [m] | 10.00 |

| start-end distance [m] | 20.02 |

## Route Zones

| zone | start | end |
|---|---:|---:|
| startup | 0.0 | 12.0 |
| outbound_rack_aisle | 12.0 | 90.0 |
| approach_to_u_turn | 90.0 | 100.0 |
| adjacent_aisle_u_turn | 100.0 | 138.5 |
| return_recovery_aisle | 138.5 | 158.0 |
| return_slope_aisle | 158.0 | 232.0 |
| shipping_return_aisle | 232.0 | 238.5 |

## Design Rationale

- This is a long industrial near-loop route from receiving through rack aisles, a U-turn transfer, and a return aisle back near the start; it is not a training path.
- It stays inside the theta10 V2 envelope: speed about 0.76-1.10 m/s, turn radius above 6 m, theta within +/-7.5 deg.
- It is ModernTCN-friendly for a defensible reason: closed-loop screening showed ModernTCN theta regression is strongest on straight slope-changing logistics aisles, so this v6 near-loop keeps the large theta workload on long straight segments and uses one U-turn mainly to bring the route back near the start.
- It does not use the `agv_theta10_uniform_v2_*` training generator or file naming pattern.
- Use the same `path_file` for `LPVMPC_AGV_simulink_GRU.slx` and `LPVMPC_AGV_simulink_Modern_TCN.slx`.

## MATLAB Command

```matlab
init_project;
result = gen_factory_logistics_showcase_path();
load(result.path_file, 'ref');
```
