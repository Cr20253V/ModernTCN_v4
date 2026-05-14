# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_clean_turnC_seed73\modern_tcn_seed73.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_clean_turnC_seed73\modern_tcn_seed73_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 6.67572e-06 | 1.85178e-06 | 1 |
| logits_turn | 5.72205e-06 | 1.19209e-06 | 1 |
| theta_hat | 1.13621e-07 | 2.04745e-08 | 1 |
