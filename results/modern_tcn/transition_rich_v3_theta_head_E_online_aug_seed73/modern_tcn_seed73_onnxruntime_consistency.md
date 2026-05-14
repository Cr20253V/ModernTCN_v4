# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\modern_tcn\transition_rich_v3_theta_head_E_online_aug_seed73\modern_tcn_seed73.onnx`
- sample: `results\modern_tcn\transition_rich_v3_theta_head_E_online_aug_seed73\modern_tcn_seed73_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 9.53674e-06 | 2.77658e-06 | 1 |
| logits_turn | 9.53674e-07 | 2.61197e-07 | 1 |
| theta_hat | 2.98023e-08 | 1.47702e-08 | 1 |
