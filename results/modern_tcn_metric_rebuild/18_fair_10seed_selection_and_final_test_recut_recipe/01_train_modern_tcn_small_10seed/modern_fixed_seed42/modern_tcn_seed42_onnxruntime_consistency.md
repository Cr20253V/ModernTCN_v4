# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\01_train_modern_tcn_small_10seed\modern_fixed_seed42\modern_tcn_seed42.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\01_train_modern_tcn_small_10seed\modern_fixed_seed42\modern_tcn_seed42_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 6.67572e-06 | 1.74716e-06 | 1 |
| logits_turn | 7.62939e-06 | 1.01142e-06 | 1 |
| theta_hat | 8.9407e-08 | 2.11876e-08 | 1 |
