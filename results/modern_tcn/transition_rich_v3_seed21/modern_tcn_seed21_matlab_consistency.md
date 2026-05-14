# ModernTCN MATLAB ONNX 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed21\modern_tcn_seed21.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed21\modern_tcn_seed21_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error |
|---|---:|---:|
| logits_main | 6.67572e-06 | 1.57518e-06 |
| logits_turn | 5.72205e-06 | 1.2732e-06 |
| theta_hat | 6.70552e-08 | 2.6077e-08 |
