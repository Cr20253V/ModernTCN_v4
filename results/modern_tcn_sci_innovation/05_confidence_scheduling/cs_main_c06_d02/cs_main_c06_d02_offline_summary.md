# E5 Offline Run: cs_main_c06_d02

## Config

```json
{
  "tag": "cs_main_c06_d02",
  "confidence_mode": "main_conf",
  "conf_threshold": 0.6,
  "delta_theta_max_deg_per_step": 0.2,
  "offline_only": false
}
```

## Metrics

- offline_safe: False
- reason: theta_sched_mae_deg 1.294800 > raw+0.010 0.689395; flat_peak_theta_error 9.631826 > raw+0.300 5.635740; theta_edge_p95_abs_err 9.725619 > raw+0.300 2.493127
- theta_raw_mae_deg: 0.679395
- theta_sched_mae_deg: 1.294800
- theta_raw_step_p95_deg: 14.589640
- theta_sched_step_p95_deg: 0.200000
- low_conf_window_ratio: 0.009439
- rate_limit_hit_ratio: 0.114381
- flat_peak_theta_error: 9.631826
- theta_edge_p95_abs_err: 9.725619
- advisory_step_metrics: True

Offline step/smoothness metrics are advisory if the test split order is not a true time sequence.
