# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\14_uncertainty_stability_optimization\04_closed_loop_multiseed\00_exported_onnx\s01_lr13_select_edges_flat_seed21\s01_lr13_select_edges_flat_seed21.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\14_uncertainty_stability_optimization\04_closed_loop_multiseed\00_exported_onnx\s01_lr13_select_edges_flat_seed21\s01_lr13_select_edges_flat_seed21_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 6.67572e-06 | 1.79311e-06 | 1 |
| logits_turn | 4.29153e-06 | 1.02601e-06 | 1 |
| theta_hat | 6.70552e-08 | 2.56114e-08 | 1 |
