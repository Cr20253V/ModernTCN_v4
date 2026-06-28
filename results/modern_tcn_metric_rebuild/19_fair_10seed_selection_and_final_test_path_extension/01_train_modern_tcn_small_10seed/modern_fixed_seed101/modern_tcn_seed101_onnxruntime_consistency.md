# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\01_train_modern_tcn_small_10seed\modern_fixed_seed101\modern_tcn_seed101.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\18_fair_10seed_selection_and_final_test_recut_recipe\01_train_modern_tcn_small_10seed\modern_fixed_seed101\modern_tcn_seed101_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 9.53674e-06 | 2.00545e-06 | 1 |
| logits_turn | 4.94719e-06 | 1.37696e-06 | 1 |
| theta_hat | 5.96046e-08 | 2.31666e-08 | 1 |
