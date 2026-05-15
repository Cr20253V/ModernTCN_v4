# Long Uphill/Downhill Path

- path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_long_updown_theta10_v1.mat`
- preview: `E:\Matlab\Simulink\S-Function_16\figures\paths\path_closed_loop_long_updown_theta10_v1_preview.png`
- role: `long_updown`
- duration: `44.0 s`
- distance: `38.49 m`
- training path: `false`

## Ranges

| signal | min | max | limit used |
|---|---:|---:|---:|
| v [m/s] | 0.8400 | 0.9200 | [0.74, 1.12] |
| omega [rad/s] | -0.1000 | 0.0900 | +/-0.16 |
| theta [deg] | -5.8000 | 6.6000 | +/-7.50 |

## Coverage

| bucket | seconds |
|---|---:|
| turn | 12.73 |
| left turn | 8.22 |
| right turn | 4.51 |
| slope | 34.79 |
| slope + turn | 12.73 |
| low speed candidate | 0.00 |
| stall candidate window | 0.00 |
| min turn radius [m] | 9.20 |

## Route Zones

| zone | start | end |
|---|---:|---:|
| startup | 0.0 | 3.0 |
| uphill_long_entry | 3.0 | 16.0 |
| downhill_transition | 16.0 | 29.0 |
| uphill_return | 29.0 | 39.0 |
| flat_recovery | 39.0 | 44.0 |

## Design Goal

Long slope transitions with a few gentle transfer turns; intended to stress theta scheduling without leaving the LPV grid.

## MATLAB Command

```matlab
init_project;
out = gen_closed_loop_eval_paths(struct('force', true));
```
