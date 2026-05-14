# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed21\modern_tcn_seed21.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed21\modern_tcn_seed21_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 4.76837e-06 | 1.37277e-06 | 1 |
| logits_turn | 3.8147e-06 | 1.16182e-06 | 1 |
| theta_hat | 9.87202e-08 | 3.48373e-08 | 1 |
