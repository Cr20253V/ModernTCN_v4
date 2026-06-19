# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.onnx`
- sample: `results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 5.72205e-06 | 1.40071e-06 | 1 |
| logits_turn | 4.29153e-06 | 1.00746e-06 | 1 |
| theta_hat | 2.6077e-07 | 3.9814e-08 | 1 |
