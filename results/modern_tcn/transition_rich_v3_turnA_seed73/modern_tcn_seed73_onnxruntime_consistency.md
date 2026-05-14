# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_turnA_seed73\modern_tcn_seed73.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_turnA_seed73\modern_tcn_seed73_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 5.72205e-06 | 1.72357e-06 | 1 |
| logits_turn | 3.8147e-06 | 9.77889e-07 | 1 |
| theta_hat | 5.21541e-08 | 1.58907e-08 | 1 |
