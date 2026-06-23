# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\00_exported_onnx\u06_lr0013_seed101\u06_lr0013_seed101.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\00_exported_onnx\u06_lr0013_seed101\u06_lr0013_seed101_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 5.72205e-06 | 2.00421e-06 | 1 |
| logits_turn | 2.5034e-06 | 8.55575e-07 | 1 |
| theta_hat | 7.45058e-08 | 2.80561e-08 | 1 |
