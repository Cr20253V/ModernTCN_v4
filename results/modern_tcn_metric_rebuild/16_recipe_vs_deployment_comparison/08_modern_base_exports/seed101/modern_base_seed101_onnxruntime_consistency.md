# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\modern_tcn_metric_rebuild\16_recipe_vs_deployment_comparison\08_modern_base_exports\seed101\modern_base_seed101.onnx`
- sample: `results\modern_tcn_metric_rebuild\16_recipe_vs_deployment_comparison\08_modern_base_exports\seed101\modern_base_seed101_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 4.76837e-06 | 1.73599e-06 | 1 |
| logits_turn | 2.6226e-06 | 7.3947e-07 | 1 |
| theta_hat | 5.96046e-08 | 2.27592e-08 | 1 |
