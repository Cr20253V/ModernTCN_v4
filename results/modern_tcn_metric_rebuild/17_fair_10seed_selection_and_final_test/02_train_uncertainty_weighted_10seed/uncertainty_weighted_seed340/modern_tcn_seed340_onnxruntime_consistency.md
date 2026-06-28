# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\02_train_uncertainty_weighted_10seed\uncertainty_weighted_seed340\modern_tcn_seed340.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\02_train_uncertainty_weighted_10seed\uncertainty_weighted_seed340\modern_tcn_seed340_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 4.76837e-06 | 1.82974e-06 | 1 |
| logits_turn | 5.72205e-06 | 1.26489e-06 | 1 |
| theta_hat | 7.45058e-08 | 2.36905e-08 | 1 |
