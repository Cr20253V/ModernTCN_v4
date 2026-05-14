# ModernTCN MATLAB ONNX 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed42\modern_tcn_seed42.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed42\modern_tcn_seed42_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error |
|---|---:|---:|
| logits_main | 4.29153e-06 | 1.18398e-06 |
| logits_turn | 1.14441e-05 | 1.57277e-06 |
| theta_hat | 6.33299e-08 | 1.6531e-08 |
