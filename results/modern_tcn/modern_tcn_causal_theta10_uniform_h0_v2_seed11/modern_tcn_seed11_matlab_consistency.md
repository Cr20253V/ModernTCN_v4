# ModernTCN MATLAB ONNX 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed11\modern_tcn_seed11.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed11\modern_tcn_seed11_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error |
|---|---:|---:|
| logits_main | 7.62939e-06 | 2.17557e-06 |
| logits_turn | 7.62939e-06 | 2.00327e-06 |
| theta_hat | 6.89179e-08 | 2.06637e-08 |
