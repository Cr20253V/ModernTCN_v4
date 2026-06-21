# E3 Physics-Group Residual Gate Summary

- E3 status: PASS
- eligible runs: 0
- promotable runs: 0
- can expand seeds 42/101: False
- can enter E4: True
- no ONNX export: True
- no MATLAB/Simulink closed-loop: True
- no baseline overwrite: True

## Ranking

| rank | run | eligible | promotable | alpha_final | gate_score | d_turn_transition | d_stall | d_theta_mae | reason |
|---:|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | `pg_alpha01_seed21` | False | False | 0.364322 | 2 | 0.014903 | -0.083333 | 0.044386 | not eligible |
| 2 | `pg_alpha0_seed21` | False | False | 0.208433 | 1 | 0.010432 | -0.083333 | 0.021672 | not eligible |

## E4 Strategy

```json
{
  "source": "baseline_fixed_loss",
  "model_family": "small",
  "reason": "E3 has no promotable run"
}
```
