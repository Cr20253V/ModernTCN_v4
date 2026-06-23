# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\00_exported_onnx\u04_lwlr0030_seed101\u04_lwlr0030_seed101.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\00_exported_onnx\u04_lwlr0030_seed101\u04_lwlr0030_seed101_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 7.15256e-06 | 1.69997e-06 | 1 |
| logits_turn | 3.8147e-06 | 8.51384e-07 | 1 |
| theta_hat | 5.96046e-08 | 2.82889e-08 | 1 |
