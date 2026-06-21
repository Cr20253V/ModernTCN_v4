# ModernTCN SCI Innovation E5 Handoff

阶段：`E5 / 05_confidence_scheduling`

## 结论

- E5 status: `PASS`
- E5 role: deployment-side offline safety screen, not baseline replacement
- sandbox closed-loop executed: False
- sandbox better than raw baseline: False
- can enter Phase 6 sandbox expansion: False
- can enter Phase 6 formal: False

## Offline 排序

| rank | run | safe | theta_sched_mae | low_conf | rate_hit | reason |
|---:|---|---|---:|---:|---:|---|
| 1 | `cs_main_c06_d02` | False | 1.294800 | 0.009439 | 0.114381 | theta_sched_mae_deg 1.294800 > raw+0.010 0.689395; flat_peak_theta_error 9.631826 > raw+0.300 5.635740; theta_edge_p95_abs_err 9.725619 > raw+0.300 2.493127 |
| 2 | `cs_mainturn_c06_d01` | False | 1.307092 | 0.159356 | 0.101055 | theta_sched_mae_deg 1.307092 > raw+0.010 0.689395; flat_peak_theta_error 9.731826 > raw+0.300 5.635740; theta_edge_p95_abs_err 9.825619 > raw+0.300 2.493127 |
| 3 | `cs_main_c07_d01` | False | 1.305653 | 0.015269 | 0.115491 | theta_sched_mae_deg 1.305653 > raw+0.010 0.689395; flat_peak_theta_error 9.731826 > raw+0.300 5.635740; theta_edge_p95_abs_err 9.825619 > raw+0.300 2.493127 |
| 4 | `cs_main_c06_d01` | False | 1.305653 | 0.009439 | 0.116324 | theta_sched_mae_deg 1.305653 > raw+0.010 0.689395; flat_peak_theta_error 9.731826 > raw+0.300 5.635740; theta_edge_p95_abs_err 9.825619 > raw+0.300 2.493127 |
| 5 | `rate_limit_only_d01` | False | 1.305625 | 0.000000 | 0.116602 | theta_sched_mae_deg 1.305625 > raw+0.010 0.689395; flat_peak_theta_error 9.731826 > raw+0.300 5.635740; theta_edge_p95_abs_err 9.825619 > raw+0.300 2.493127 |

## 必读证据

- `e5_preflight.md`
- `baseline_prediction_cache.md`
- `confidence_scheduling_offline_master_table.csv`
- `confidence_scheduling_offline_summary.md`
- `confidence_scheduling_decision.json`

## Safety

- no training: True
- no ONNX export: True
- no baseline overwrite: True
- no formal compare write: True
- MATLAB E5 filter default disabled: True
