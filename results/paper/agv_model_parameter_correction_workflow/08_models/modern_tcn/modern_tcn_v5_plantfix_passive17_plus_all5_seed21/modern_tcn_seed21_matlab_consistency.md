# ModernTCN MATLAB ONNX 一致性检查

- onnx: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_passive17_plus_all5_seed21\modern_tcn_seed21.onnx`
- sample: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_passive17_plus_all5_seed21\modern_tcn_seed21_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error |
|---|---:|---:|
| logits_main | 4.76837e-06 | 1.65713e-06 |
| logits_turn | 3.57628e-06 | 1.03191e-06 |
| theta_hat | 6.70552e-08 | 2.70084e-08 |
