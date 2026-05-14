# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_kinTurnD_seed73\modern_tcn_seed73.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_kinTurnD_seed73\modern_tcn_seed73_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 9.53674e-06 | 2.77658e-06 | 1 |
| logits_turn | 9.53674e-07 | 2.61197e-07 | 1 |
| theta_hat | 5.21541e-08 | 1.56579e-08 | 1 |
