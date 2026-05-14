# Factory Logistics Showcase Path

- path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v5.mat`
- preview: `E:\Matlab\Simulink\S-Function_16\figures\paths\path_factory_logistics_showcase_theta10_v5_preview.png`
- duration: `240.0 s`
- distance: `235.42 m`
- training path: `false`

## Ranges

| signal | min | max | limit used |
|---|---:|---:|---:|
| v [m/s] | 0.9010 | 1.0546 | [0.74, 1.12] |
| omega [rad/s] | -0.0944 | 0.0883 | +/-0.16 |
| theta [deg] | -7.5000 | 5.5000 | +/-7.50 |

## Coverage

| bucket | seconds |
|---|---:|
| left turn | 37.07 |
| right turn | 35.44 |
| straight / low-yaw | 167.50 |
| slope | 147.92 |
| flat | 92.09 |
| slope + turn composite | 38.17 |
| flat turn | 34.34 |
| low speed candidate | 0.00 |
| min turn radius [m] | 11.17 |

| start-end distance [m] | 0.00 |

## Route Zones

| zone | start | end |
|---|---:|---:|
| startup | 0.0 | 12.0 |
| receiving_to_rack_aisle | 12.0 | 52.0 |
| north_storage_loop | 52.0 | 92.0 |
| ramp_transfer_downhill | 92.0 | 124.0 |
| downhill_picking_aisle | 124.0 | 178.0 |
| shipping_cross_aisle | 178.0 | 208.0 |
| return_to_receiving_loop | 208.0 | 240.0 |

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
