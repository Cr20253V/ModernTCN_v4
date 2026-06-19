# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn_stage2_targeted\modern_tcn_v5_plantfix_stage2_l020_tt30_lr_seed101\modern_tcn_seed101.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn_stage2_targeted\modern_tcn_v5_plantfix_stage2_l020_tt30_lr_seed101\modern_tcn_seed101_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 8.10623e-06 | 1.50253e-06 | 1 |
| logits_turn | 2.77162e-06 | 7.22085e-07 | 1 |
| theta_hat | 1.49012e-07 | 2.7183e-08 | 1 |
