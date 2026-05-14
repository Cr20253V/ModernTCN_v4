# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\modern_tcn\modern_tcn_theta10_uniform_h0_v2_seed21\modern_tcn_seed21.onnx`
- sample: `results\modern_tcn\modern_tcn_theta10_uniform_h0_v2_seed21\modern_tcn_seed21_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 7.62939e-06 | 2.1557e-06 | 1 |
| logits_turn | 1.04904e-05 | 2.62369e-06 | 1 |
| theta_hat | 8.9407e-08 | 2.53785e-08 | 1 |
