# ModernTCN ONNXRuntime 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn_stage2_targeted\modern_tcn_v5_plantfix_stage2_l020_tt30_lr_seed303\modern_tcn_seed303.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn_stage2_targeted\modern_tcn_v5_plantfix_stage2_l020_tt30_lr_seed303\modern_tcn_seed303_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 5.72205e-06 | 2.00172e-06 | 1 |
| logits_turn | 3.8147e-06 | 1.05426e-06 | 1 |
| theta_hat | 8.19564e-08 | 3.82424e-08 | 1 |
