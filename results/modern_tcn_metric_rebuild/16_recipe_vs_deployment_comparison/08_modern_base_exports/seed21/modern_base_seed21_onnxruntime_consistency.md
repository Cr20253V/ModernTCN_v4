# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\modern_tcn_metric_rebuild\16_recipe_vs_deployment_comparison\08_modern_base_exports\seed21\modern_base_seed21.onnx`
- sample: `results\modern_tcn_metric_rebuild\16_recipe_vs_deployment_comparison\08_modern_base_exports\seed21\modern_base_seed21_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 4.29153e-06 | 1.25294e-06 | 1 |
| logits_turn | 3.8147e-06 | 6.28022e-07 | 1 |
| theta_hat | 8.9407e-08 | 3.06754e-08 | 1 |
