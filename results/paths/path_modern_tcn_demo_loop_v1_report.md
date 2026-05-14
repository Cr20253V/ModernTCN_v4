# ModernTCN Demo Closed-Loop Path

- path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_modern_tcn_demo_loop_v1.mat`
- preview: `E:\Matlab\Simulink\S-Function_16\figures\paths\path_modern_tcn_demo_loop_v1_preview.png`
- duration: `180.0 s`
- curve: `rotated Gerono lemniscate`
- curve length: `160.86 m`
- minimum radius: `6.43 m`
- closure distance: `0.0000 m`
- closure heading error: `0.0000 deg`

## Ranges

| signal | min | max |
|---|---:|---:|
| v [m/s] | 0.7778 | 1.0112 |
| omega [rad/s] | -0.1543 | 0.1558 |
| theta [deg] | -5.5000 | 5.5000 |

## Coverage

| state bucket | seconds |
|---|---:|
| flat | 104.80 |
| slope | 75.21 |
| pure slope | 47.89 |
| slope + turn composite | 27.32 |
| flat turn | 41.37 |
| left turn | 34.23 |
| right turn | 34.46 |
| straight / low-yaw | 111.32 |
| low speed candidate | 23.48 |

## Zones

| zone | start | end |
|---|---:|---:|
| startup | 0.0 | 12.0 |
| flat_right_turn | 12.0 | 48.0 |
| low_speed_flat_turn | 48.0 | 62.0 |
| pure_slope | 64.0 | 110.0 |
| slope_left_turn_composite | 116.0 | 148.0 |
| bumpy_theta_closure | 152.0 | 170.0 |
| closure | 170.0 | 180.0 |

## Design Notes

- The path stays inside the V4 training envelope: speed around 0.8-1.1 m/s, radius above 6.4 m, theta within +/-5.5 deg.
- It favors ModernTCN by emphasizing state classification, transition timing, left/right turn signs, slope-turn overlap, and hard-negative flat turns.
- It avoids making the demo mostly long smooth slope plateaus, where GRU theta regression would be the dominant advantage.
- Dataset stall/load/slip states require disturbance injection; this path records optional windows but does not inject disturbances by itself.
- No Simulink model file is modified by this generator.

## MATLAB Command

```matlab
init_project;
result = gen_modern_tcn_demo_path();
load(result.path_file, 'ref');
```
