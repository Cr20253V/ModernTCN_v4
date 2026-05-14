# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed101\modern_tcn_seed101.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed101\modern_tcn_seed101_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 5.24521e-06 | 1.53544e-06 | 1 |
| logits_turn | 5.72205e-06 | 1.27902e-06 | 1 |
| theta_hat | 5.96046e-08 | 1.32713e-08 | 1 |
