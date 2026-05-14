# Factory Logistics Showcase Path

- path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v6.mat`
- preview: `E:\Matlab\Simulink\S-Function_16\figures\paths\path_factory_logistics_showcase_theta10_v6_preview.png`
- duration: `196.0 s`
- distance: `168.56 m`
- training path: `false`

## Ranges

| signal | min | max | limit used |
|---|---:|---:|---:|
| v [m/s] | 0.8600 | 0.8600 | [0.74, 1.12] |
| omega [rad/s] | 0.0000 | 0.1323 | +/-0.16 |
| theta [deg] | -7.5000 | 5.5000 | +/-7.50 |

## Coverage

| bucket | seconds |
|---|---:|
| left turn | 24.08 |
| right turn | 0.00 |
| straight / low-yaw | 171.93 |
| slope | 143.25 |
| flat | 52.76 |
| slope + turn composite | 7.57 |
| flat turn | 16.51 |
| low speed candidate | 0.00 |
| min turn radius [m] | 6.50 |

| start-end distance [m] | 12.99 |

## Route Zones

| zone | start | end |
|---|---:|---:|
| startup | 0.0 | 12.0 |
| outbound_rack_aisle | 12.0 | 68.0 |
| approach_to_u_turn | 68.0 | 85.0 |
| adjacent_aisle_u_turn | 85.0 | 110.8 |
| return_downhill_aisle | 110.8 | 172.0 |
| shipping_return_aisle | 172.0 | 196.0 |

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
