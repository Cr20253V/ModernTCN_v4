# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\modern_tcn\transition_rich_v3_seed42\modern_tcn_seed42.onnx`
- sample: `results\modern_tcn\transition_rich_v3_seed42\modern_tcn_seed42_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 2.86102e-06 | 1.00459e-06 | 1 |
| logits_turn | 7.62939e-06 | 1.47801e-06 | 1 |
| theta_hat | 4.09782e-08 | 1.97324e-08 | 1 |
