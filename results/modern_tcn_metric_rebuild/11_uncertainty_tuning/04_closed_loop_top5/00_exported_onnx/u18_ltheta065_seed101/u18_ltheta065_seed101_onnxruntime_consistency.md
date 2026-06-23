# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\00_exported_onnx\u18_ltheta065_seed101\u18_ltheta065_seed101.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\00_exported_onnx\u18_ltheta065_seed101\u18_ltheta065_seed101_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 9.53674e-06 | 2.40157e-06 | 1 |
| logits_turn | 5.72205e-06 | 1.08468e-06 | 1 |
| theta_hat | 6.70552e-08 | 2.47383e-08 | 1 |
