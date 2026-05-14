# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\modern_tcn\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select\modern_tcn_seed42.onnx`
- sample: `results\modern_tcn\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select\modern_tcn_seed42_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 1.14441e-05 | 2.07157e-06 | 1 |
| logits_turn | 7.62939e-06 | 8.94535e-07 | 1 |
| theta_hat | 1.04308e-07 | 2.15605e-08 | 1 |
