# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\15_bi_bu_uncertainty_stabilization\06_sentinel_closed_loop\exports\a2_freeze_early_seed42\modern_tcn_seed42.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\15_bi_bu_uncertainty_stabilization\06_sentinel_closed_loop\exports\a2_freeze_early_seed42\a2_freeze_early_seed42_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 6.19888e-06 | 1.73599e-06 | 1 |
| logits_turn | 2.5034e-06 | 1.06621e-06 | 1 |
| theta_hat | 5.96046e-08 | 2.08966e-08 | 1 |
