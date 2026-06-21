# E4 Mode-Conditioned Theta Experts Summary

- E4 status: PASS
- safe eligible runs: 0
- promotable runs: 0
- best run: `mode_theta_detach_flatreg001_seed21`
- can expand seeds 42/101: False
- can enter E5: True
- no ONNX export: True
- no MATLAB/Simulink closed-loop: True
- no baseline overwrite: True

## Ranking

| rank | run | safe | promotable | flat_reg | theta | flat_peak | edge | acc_main | expert_diff | reason |
|---:|---|---|---|---:|---:|---:|---:|---:|---|---|
| 1 | `mode_theta_detach_flatreg001_seed21` | False | False | 0.010 | 0.616433 | 6.068908 | 2.651289 | 0.969739 | True | not safe_eligible |
| 2 | `mode_theta_detach_flatreg003_seed21` | False | False | 0.030 | 0.666874 | 5.952684 | 2.869949 | 0.958356 | True | not safe_eligible |
| 3 | `mode_theta_detach_flatreg000_seed21` | False | False | 0.000 | 0.651509 | 6.434472 | 3.692942 | 0.970294 | True | not safe_eligible |

## E5 Strategy

```json
{
  "source": "baseline_small",
  "model_family": "small",
  "reason": "E4 has no promotable run; E5 sandbox may still proceed"
}
```
