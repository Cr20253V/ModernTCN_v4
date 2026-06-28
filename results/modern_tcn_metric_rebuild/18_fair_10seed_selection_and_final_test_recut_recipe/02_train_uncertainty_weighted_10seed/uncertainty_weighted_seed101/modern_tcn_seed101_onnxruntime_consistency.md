# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\02_train_uncertainty_weighted_10seed\uncertainty_weighted_seed101\modern_tcn_seed101.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\02_train_uncertainty_weighted_10seed\uncertainty_weighted_seed101\modern_tcn_seed101_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 6.67572e-06 | 1.88251e-06 | 1 |
| logits_turn | 4.08292e-06 | 1.05208e-06 | 1 |
| theta_hat | 8.9407e-08 | 2.58442e-08 | 1 |
