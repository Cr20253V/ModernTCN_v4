# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\modern_tcn\transition_rich_v3_seed73\modern_tcn_seed73_legacy.onnx`
- sample: `results\modern_tcn\transition_rich_v3_seed73\modern_tcn_seed73_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 5.72205e-06 | 1.77448e-06 | 1 |
| logits_turn | 4.76837e-06 | 1.2638e-06 | 1 |
| theta_hat | 5.21541e-08 | 2.53203e-08 | 1 |
