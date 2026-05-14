# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed73\modern_tcn_seed73.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_seed73\modern_tcn_seed73_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 7.62939e-06 | 1.96695e-06 | 1 |
| logits_turn | 3.8147e-06 | 8.2391e-07 | 1 |
| theta_hat | 4.93601e-08 | 1.81608e-08 | 1 |
