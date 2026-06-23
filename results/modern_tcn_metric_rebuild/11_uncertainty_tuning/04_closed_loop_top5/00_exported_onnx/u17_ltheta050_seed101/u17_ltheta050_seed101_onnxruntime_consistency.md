# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\00_exported_onnx\u17_ltheta050_seed101\u17_ltheta050_seed101.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\00_exported_onnx\u17_ltheta050_seed101\u17_ltheta050_seed101_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 8.58307e-06 | 1.98806e-06 | 1 |
| logits_turn | 7.62939e-06 | 1.16959e-06 | 1 |
| theta_hat | 5.96046e-08 | 2.0882e-08 | 1 |
