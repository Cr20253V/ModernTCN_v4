# E5 Offline Run: cs_mainturn_c06_d01

## Config

```json
{
  "tag": "cs_mainturn_c06_d01",
  "confidence_mode": "main_turn_conf",
  "conf_threshold": 0.6,
  "delta_theta_max_deg_per_step": 0.1,
  "offline_only": false
}
```

## Metrics

- offline_safe: False
- reason: theta_sched_mae_deg 1.307092 > raw+0.010 0.689395; flat_peak_theta_error 9.731826 > raw+0.300 5.635740; theta_edge_p95_abs_err 9.825619 > raw+0.300 2.493127
- theta_raw_mae_deg: 0.679395
- theta_sched_mae_deg: 1.307092
- theta_raw_step_p95_deg: 14.589640
- theta_sched_step_p95_deg: 0.100000
- low_conf_window_ratio: 0.159356
- rate_limit_hit_ratio: 0.101055
- flat_peak_theta_error: 9.731826
- theta_edge_p95_abs_err: 9.825619
- advisory_step_metrics: True

Offline step/smoothness metrics are advisory if the test split order is not a true time sequence.
