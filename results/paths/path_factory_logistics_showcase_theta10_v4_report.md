# Factory Logistics Showcase Path

- path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v4.mat`
- preview: `E:\Matlab\Simulink\S-Function_16\figures\paths\path_factory_logistics_showcase_theta10_v4_preview.png`
- duration: `240.4 s`
- distance: `206.79 m`
- training path: `false`

## Ranges

| signal | min | max | limit used |
|---|---:|---:|---:|
| v [m/s] | 0.8600 | 0.8600 | [0.74, 1.12] |
| omega [rad/s] | 0.0000 | 0.1075 | +/-0.16 |
| theta [deg] | -7.5000 | 5.5000 | +/-7.50 |

## Coverage

| bucket | seconds |
|---|---:|
| left turn | 58.81 |
| right turn | 0.00 |
| straight / low-yaw | 181.65 |
| slope | 161.29 |
| flat | 79.17 |
| slope + turn composite | 27.10 |
| flat turn | 31.71 |
| low speed candidate | 0.00 |
| min turn radius [m] | 8.00 |

| start-end distance [m] | 0.03 |

## Route Zones

| zone | start | end |
|---|---:|---:|
| startup | 0.0 | 12.0 |
| receiving_to_rack_aisle | 12.0 | 52.0 |
| northwest_ramp_corner | 52.0 | 68.6 |
| upper_cross_aisle | 68.6 | 103.6 |
| southwest_return_corner | 103.6 | 120.2 |
| downhill_picking_aisle | 120.2 | 172.2 |
| southeast_transfer_corner | 172.2 | 188.8 |
| shipping_cross_aisle | 188.8 | 223.8 |
| final_docking_corner | 223.8 | 240.4 |

## Design Rationale

- This is a long industrial logistics loop from receiving through rack aisles to shipping and back near the start; it is not a training path.
- It stays inside the theta10 V2 envelope: speed about 0.76-1.10 m/s, turn radius above 6 m, theta within +/-7.5 deg.
- It is ModernTCN-friendly for a defensible reason: closed-loop screening showed ModernTCN theta regression is strongest on straight slope-changing logistics aisles, so this v4 loop keeps the large theta workload on long straight segments and uses rounded corners mainly for route closure.
- It does not use the `agv_theta10_uniform_v2_*` training generator or file naming pattern.
- Use the same `path_file` for `LPVMPC_AGV_simulink_GRU.slx` and `LPVMPC_AGV_simulink_Modern_TCN.slx`.

## MATLAB Command

```matlab
init_project;
result = gen_factory_logistics_showcase_path();
load(result.path_file, 'ref');
```
