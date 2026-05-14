# ModernTCN MATLAB ONNX 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed11\modern_tcn_seed11.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed11\modern_tcn_seed11_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error |
|---|---:|---:|
| logits_main | 4.76837e-06 | 1.50036e-06 |
| logits_turn | 3.8147e-06 | 1.19116e-06 |
| theta_hat | 7.45058e-08 | 2.8871e-08 |
