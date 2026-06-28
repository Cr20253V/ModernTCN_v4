# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\01_train_modern_tcn_small_10seed\modern_fixed_seed1\modern_tcn_seed1.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\17_fair_10seed_selection_and_final_test\01_train_modern_tcn_small_10seed\modern_fixed_seed1\modern_tcn_seed1_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 6.67572e-06 | 1.96944e-06 | 1 |
| logits_turn | 4.29153e-06 | 1.32589e-06 | 1 |
| theta_hat | 5.21541e-08 | 2.14204e-08 | 1 |
