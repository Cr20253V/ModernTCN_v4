# Sharp Turning Transition Path

- path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_sharp_turn_transition_theta10_v1.mat`
- preview: `E:\Matlab\Simulink\S-Function_16\figures\paths\path_closed_loop_sharp_turn_transition_theta10_v1_preview.png`
- role: `sharp_turn_transition`
- duration: `52.0 s`
- distance: `44.12 m`
- training path: `false`

## Ranges

| signal | min | max | limit used |
|---|---:|---:|---:|
| v [m/s] | 0.8200 | 0.8800 | [0.74, 1.12] |
| omega [rad/s] | -0.1080 | 0.1080 | +/-0.16 |
| theta [deg] | -5.2000 | 5.5000 | +/-7.50 |

## Coverage

| bucket | seconds |
|---|---:|
| turn | 21.15 |
| left turn | 13.06 |
| right turn | 8.09 |
| slope | 39.49 |
| slope + turn | 19.63 |
| low speed candidate | 0.00 |
| stall candidate window | 0.00 |
| min turn radius [m] | 7.59 |

## Route Zones

| zone | start | end |
|---|---:|---:|
| startup | 0.0 | 4.0 |
| uphill_left_transition | 4.0 | 22.0 |
| downhill_right_transition | 22.0 | 42.0 |
| flat_left_exit | 42.0 | 52.0 |

## Design Goal

Alternating left/right turn transitions overlapped with slope entry/exit; intended to stress coupled turn-transition recognition and theta scheduling.

## MATLAB Command

```matlab
init_project;
out = gen_closed_loop_eval_paths(struct('force', true));
```
