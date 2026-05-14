# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed11\modern_tcn_seed11.onnx`
- sample: `results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed11\modern_tcn_seed11_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 9.53674e-06 | 2.08616e-06 | 1 |
| logits_turn | 5.72205e-06 | 1.59194e-06 | 1 |
| theta_hat | 4.47035e-08 | 2.31666e-08 | 1 |
