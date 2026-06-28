# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\02_train_uncertainty_weighted_10seed\uncertainty_weighted_seed7\modern_tcn_seed7.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\02_train_uncertainty_weighted_10seed\uncertainty_weighted_seed7\modern_tcn_seed7_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 9.53674e-06 | 2.03463e-06 | 1 |
| logits_turn | 6.67572e-06 | 1.45038e-06 | 1 |
| theta_hat | 1.04308e-07 | 2.6077e-08 | 1 |
