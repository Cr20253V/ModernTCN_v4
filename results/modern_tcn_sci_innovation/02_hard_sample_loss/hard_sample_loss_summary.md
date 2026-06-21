# E2 Hard-Sample Focal Loss Summary

- E2 status: PASS
- method label: `hard-sample focal only`
- theta_smooth_status: `disabled_contract_limited`
- eligible runs: 0
- promotable runs: 0
- can expand seeds 42/101: False
- can enter E3: True
- no ONNX export: True
- no MATLAB/Simulink closed-loop: True
- no baseline overwrite: True

## Baseline

- acc_main: 0.966963
- acc_turn_transition: 0.497765
- stall_recall: 0.718750
- theta_edge_p95_abs_err: 2.755057
- flat_peak_theta_error: 5.335740

## Ranking

| rank | run | eligible | promotable | d_turn_transition | d_stall | d_theta_mae | d_edge | d_flat_peak | reason |
|---:|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | fs_t05_s05_sm000_seed21 | False | False | -0.019374 | -0.062500 | -0.103023 | -0.609695 | -1.699067 | not eligible |
| 2 | fs_t02_s02_sm000_seed21 | False | False | -0.043219 | -0.052083 | -0.136571 | -0.681780 | -2.419980 | not eligible |
| 3 | fs_t02_s05_sm000_seed21 | False | False | -0.055142 | -0.041667 | -0.236372 | -1.496581 | -0.860416 | not eligible |
| 4 | fs_t05_s02_sm000_seed21 | False | False | 0.008942 | -0.020833 | -0.275117 | -0.998847 | -2.914490 | not eligible |

## E3 Recommendation

```json
{
  "source": "baseline_fixed_loss",
  "loss_mode": "fixed",
  "reason": "E2 has no promotable run; continue E3 with original baseline fixed loss"
}
```
