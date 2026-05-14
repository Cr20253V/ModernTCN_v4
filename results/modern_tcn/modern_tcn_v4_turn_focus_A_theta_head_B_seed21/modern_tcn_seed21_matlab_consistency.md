# ModernTCN MATLAB ONNX 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v4_turn_focus_A_theta_head_B_seed21\modern_tcn_seed21.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v4_turn_focus_A_theta_head_B_seed21\modern_tcn_seed21_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error |
|---|---:|---:|
| logits_main | 6.67572e-06 | 1.88562e-06 |
| logits_turn | 9.53674e-06 | 2.3072e-06 |
| theta_hat | 2.98023e-08 | 1.10012e-08 |
