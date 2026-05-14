# ModernTCN MATLAB ONNX 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta10_uniform_h0_v2_seed21\modern_tcn_seed21.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta10_uniform_h0_v2_seed21\modern_tcn_seed21_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error |
|---|---:|---:|
| logits_main | 8.58307e-06 | 2.27988e-06 |
| logits_turn | 9.53674e-06 | 2.43867e-06 |
| theta_hat | 6.70552e-08 | 2.14786e-08 |
