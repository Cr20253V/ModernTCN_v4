# ModernTCN MATLAB ONNX 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed73\modern_tcn_seed73.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed73\modern_tcn_seed73_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error |
|---|---:|---:|
| logits_main | 6.67572e-06 | 2.08865e-06 |
| logits_turn | 3.8147e-06 | 1.31736e-06 |
| theta_hat | 5.96046e-08 | 1.90921e-08 |
