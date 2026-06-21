# E5 Confidence-Aware Scheduling Summary

- E5 status: `PASS`
- role: offline safety screen for deployment-side theta scheduling
- baseline replacement: False
- sandbox closed-loop executed: False
- can enter Phase 6 sandbox expansion: False
- can enter Phase 6 formal: False
- no training: True
- no ONNX export: True
- no baseline overwrite: True
- no formal compare write: True

## Offline Gate

- can enter sandbox: False
- best confidence run: ``

Reasons:

- no confidence scheduling config passed offline safety screen

## Replay Order

- run IDs contiguous: False
- contiguous segments: 3174
- advisory step metrics: True

## Offline Ranking

| rank | run | safe | theta raw | theta sched | step raw p95 | step sched p95 | low conf | rate hit | flat peak | edge p95 | score |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `cs_main_c06_d02` | False | 0.679395 | 1.294800 | 14.589640 | 0.200000 | 0.009439 | 0.114381 | 9.631826 | 9.725619 | 11.753298 |
| 2 | `cs_mainturn_c06_d01` | False | 0.679395 | 1.307092 | 14.589640 | 0.100000 | 0.159356 | 0.101055 | 9.731826 | 9.825619 | 11.750915 |
| 3 | `cs_main_c07_d01` | False | 0.679395 | 1.305653 | 14.589640 | 0.100000 | 0.015269 | 0.115491 | 9.731826 | 9.825619 | 11.737369 |
| 4 | `cs_main_c06_d01` | False | 0.679395 | 1.305653 | 14.589640 | 0.100000 | 0.009439 | 0.116324 | 9.731826 | 9.825619 | 11.736786 |
| 5 | `rate_limit_only_d01` | False | 0.679395 | 1.305625 | 14.589640 | 0.100000 | 0.000000 | 0.116602 | 9.731826 | 9.825619 | 11.735859 |

## Interpretation

Offline smoothness is advisory because the test split is not a proven time-contiguous replay. E5 does not prove superiority over the frozen baseline; it only screens deployment-side filter candidates.
