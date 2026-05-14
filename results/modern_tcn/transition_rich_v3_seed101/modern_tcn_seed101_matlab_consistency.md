# ModernTCN MATLAB ONNX 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed101\modern_tcn_seed101.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed101\modern_tcn_seed101_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error |
|---|---:|---:|
| logits_main | 6.19888e-06 | 1.41002e-06 |
| logits_turn | 5.72205e-06 | 1.17222e-06 |
| theta_hat | 7.45058e-08 | 2.18861e-08 |
