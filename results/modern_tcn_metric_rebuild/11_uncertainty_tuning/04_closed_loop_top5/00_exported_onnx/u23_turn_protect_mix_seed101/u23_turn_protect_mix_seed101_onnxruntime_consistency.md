# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\00_exported_onnx\u23_turn_protect_mix_seed101\u23_turn_protect_mix_seed101.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\00_exported_onnx\u23_turn_protect_mix_seed101\u23_turn_protect_mix_seed101_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 6.67572e-06 | 1.95205e-06 | 1 |
| logits_turn | 3.8147e-06 | 1.24394e-06 | 1 |
| theta_hat | 5.96046e-08 | 2.33413e-08 | 1 |
