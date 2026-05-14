# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed11\modern_tcn_seed11.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed11\modern_tcn_seed11_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 5.72205e-06 | 1.546e-06 | 1 |
| logits_turn | 3.8147e-06 | 1.05053e-06 | 1 |
| theta_hat | 1.09896e-07 | 3.99887e-08 | 1 |
