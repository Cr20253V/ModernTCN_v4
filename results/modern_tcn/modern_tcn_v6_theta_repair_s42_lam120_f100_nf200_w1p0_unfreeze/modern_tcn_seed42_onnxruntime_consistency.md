# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_seed42.onnx`
- sample: `results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_seed42_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 1.33514e-05 | 2.27677e-06 | 1 |
| logits_turn | 1.33514e-05 | 1.36159e-06 | 1 |
| theta_hat | 5.36442e-07 | 5.45042e-08 | 1 |
