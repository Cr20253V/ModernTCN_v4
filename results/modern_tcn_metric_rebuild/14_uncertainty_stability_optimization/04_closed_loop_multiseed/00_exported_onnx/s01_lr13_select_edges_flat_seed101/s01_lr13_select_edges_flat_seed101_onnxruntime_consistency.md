# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\14_uncertainty_stability_optimization\04_closed_loop_multiseed\00_exported_onnx\s01_lr13_select_edges_flat_seed101\s01_lr13_select_edges_flat_seed101.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\14_uncertainty_stability_optimization\04_closed_loop_multiseed\00_exported_onnx\s01_lr13_select_edges_flat_seed101\s01_lr13_select_edges_flat_seed101_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 4.76837e-06 | 1.82539e-06 | 1 |
| logits_turn | 5.72205e-06 | 1.11572e-06 | 1 |
| theta_hat | 8.9407e-08 | 3.18978e-08 | 1 |
