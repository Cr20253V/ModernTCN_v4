# Real-Time Benchmark

- timestamp: `2026-05-15 17:20:30`
- Ts: `10 ms`
- output root: `E:\Matlab\Simulink\S-Function_16\results\compare\realtime_benchmark`

## Summary

| metric | mean ms | p50 ms | p95 ms | max ms | p95 margin ms | pass p95 |
|---|---:|---:|---:|---:|---:|---:|
| onnxruntime_single_window | 0.380407 | 0.3659 | 0.450725 | 1.8839 | 9.54927 | 1 |
| matlab_replay_update_predict_steady | 17.1346 | 15.2057 | 28.3888 | 42.4473 | -18.3888 | 0 |
| matlab_replay_update_predict_all | 17.8181 | 15.2315 | 28.508 | 2116.5 | -18.508 | 0 |
| matlab_replay_update_all | 17.2946 | 15.1256 | 28.3553 | 2116.5 | -18.3553 | 0 |
| mpc_solve_time | 0.0267582 | 0.0243068 | 0.0415962 | 2.17656 | 9.9584 | 1 |
| cycle_onnxruntime_plus_mpc | 0.407166 | 0.390207 | 0.492321 | 4.06046 | 9.50768 | 1 |
| cycle_matlab_replay_plus_mpc | 17.1613 | 15.23 | 28.4304 | 44.6239 | -18.4304 | 0 |
| simulink_wall_per_step | 29.3024 | 29.3024 | 30.094 | 30.094 | -20.094 | 0 |

## Notes

- `onnxruntime_single_window` is pure batch=1 ONNXRuntime inference.
- `matlab_replay_update_predict_steady` replays closed-loop `diag.y_raw` through the MATLAB online wrapper after the sliding window is ready and after the configured first-predict warmup count.
- `mpc_solve_time` comes from `diag_solve_time_ms` in closed-loop logs after the configured warmup period.
- `simulink_wall_per_step` is desktop Simulink wall time and is not used as embedded controller compute time.
