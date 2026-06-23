# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\12_uncertainty_replacement_qualification\03_closed_loop_representatives\00_exported_onnx\ua_seed21\ua_seed21.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\12_uncertainty_replacement_qualification\03_closed_loop_representatives\00_exported_onnx\ua_seed21\ua_seed21_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 1.23978e-05 | 1.88376e-06 | 1 |
| logits_turn | 1.90735e-06 | 4.42223e-07 | 1 |
| theta_hat | 1.15484e-07 | 4.38304e-08 | 1 |
