# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\14_uncertainty_stability_optimization\04_closed_loop_multiseed\00_exported_onnx\s01_lr13_select_edges_flat_seed42\s01_lr13_select_edges_flat_seed42.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\14_uncertainty_stability_optimization\04_closed_loop_multiseed\00_exported_onnx\s01_lr13_select_edges_flat_seed42\s01_lr13_select_edges_flat_seed42_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 1.43051e-05 | 2.20537e-06 | 1 |
| logits_turn | 4.05312e-06 | 1.36284e-06 | 1 |
| theta_hat | 6.70552e-08 | 2.89874e-08 | 1 |
