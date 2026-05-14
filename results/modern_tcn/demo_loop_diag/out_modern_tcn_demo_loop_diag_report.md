# ModernTCN Demo Loop Output Diagnostic

- out file: `E:\Matlab\Simulink\S-Function_16\out.mat`
- path file: `E:\Matlab\Simulink\S-Function_16\data\paths\path_modern_tcn_demo_loop_v1.mat`
- main truth: flat if `|theta_ground| < 2 deg`, slope otherwise; no disturbance injection means no true stall.
- turn truth: `|omega_ref| > 0.05 rad/s` with `0.40 s` dwell, matching training label generation.

## Summary

- overall main accuracy: `89.25%`
- overall turn accuracy: `80.42%`
- theta MAE all/slope/flat: `1.023 / 1.434 / 0.800 deg`
- flat false-slope rate: `7.74%`
- slope recall: `83.69%`
- right/left recall: `8.72% / 68.50%`

## Simulink vs Replay

- replay file: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\closed_loop_replay\out_modern_tcn_replay_modern_tcn_v4_turn_focus_A_theta_head_B_seed21.mat`
- max abs theta diff: `0 rad`
- label main diff count: `0`
- label turn diff count: `0`
- max abs conf diff: `5.01e-06`

## Zone Metrics

| zone | main acc | turn acc | theta all | theta slope | flat false slope | slope recall | right recall | left recall | pred main 1/2/3 | pred turn -1/0/1 | conf p10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 89.2 | 80.4 | 1.023 | 1.434 | 7.7 | 83.7 | 8.7 | 68.5 | 65.5/0.0/34.5 | 2.1/87.2/10.7 | 0.995 |
| startup | 100.0 | 100.0 | 0.000 | NaN | 0.0 | NaN | NaN | NaN | 100.0/0.0/0.0 | 0.0/100.0/0.0 | 1.000 |
| flat_right_turn | 100.0 | 60.4 | 0.606 | NaN | 0.0 | NaN | 14.4 | NaN | 100.0/0.0/0.0 | 6.6/93.4/0.0 | 1.000 |
| low_speed_flat_turn | 100.0 | 23.1 | 1.995 | NaN | 0.0 | NaN | 0.0 | NaN | 100.0/0.0/0.0 | 0.0/100.0/0.0 | 1.000 |
| pure_slope | 94.7 | 96.9 | 0.873 | 0.780 | 15.4 | 98.2 | NaN | NaN | 22.9/0.0/77.1 | 3.1/96.9/0.0 | 0.996 |
| slope_left_turn_composite | 68.6 | 74.6 | 1.866 | 2.226 | 4.7 | 60.5 | NaN | 70.2 | 52.4/0.0/47.6 | 0.0/40.0/60.0 | 0.922 |
| bumpy_theta_closure | 61.8 | 100.0 | 1.889 | 2.089 | 50.9 | 100.0 | NaN | NaN | 36.8/0.0/63.2 | 0.0/100.0/0.0 | 0.912 |
| closure | 100.0 | 100.0 | 0.000 | NaN | 0.0 | NaN | NaN | NaN | 100.0/0.0/0.0 | 0.0/100.0/0.0 | 1.000 |

## Confusion Matrices

Main order `[1 flat, 2 stall, 3 slope]`:

```text
   10759        0      902
       0        0        0
    1034        0     5306
```

Turn order `[-1 right, 0 straight, 1 left]`:

```text
     239     2501        0
     141    12317        0
       0      883     1920
```
