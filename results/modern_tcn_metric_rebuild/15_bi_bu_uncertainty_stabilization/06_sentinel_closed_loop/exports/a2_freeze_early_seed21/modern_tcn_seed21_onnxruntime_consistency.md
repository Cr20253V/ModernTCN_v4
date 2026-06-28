# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\15_bi_bu_uncertainty_stabilization\06_sentinel_closed_loop\exports\a2_freeze_early_seed21\modern_tcn_seed21.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\15_bi_bu_uncertainty_stabilization\06_sentinel_closed_loop\exports\a2_freeze_early_seed21\a2_freeze_early_seed21_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 6.19888e-06 | 2.04953e-06 | 1 |
| logits_turn | 2.38419e-06 | 6.8103e-07 | 1 |
| theta_hat | 6.33299e-08 | 2.06055e-08 | 1 |
