# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\modern_tcn_metric_rebuild\16_recipe_vs_deployment_comparison\08_modern_base_exports\seed42\modern_base_seed42.onnx`
- sample: `results\modern_tcn_metric_rebuild\16_recipe_vs_deployment_comparison\08_modern_base_exports\seed42\modern_base_seed42_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 8.58307e-06 | 2.3668e-06 | 1 |
| logits_turn | 2.5034e-06 | 6.81728e-07 | 1 |
| theta_hat | 4.47035e-08 | 2.30502e-08 | 1 |
