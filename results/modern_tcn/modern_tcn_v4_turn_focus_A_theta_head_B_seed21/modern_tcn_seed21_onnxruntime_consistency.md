# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\modern_tcn\modern_tcn_v4_turn_focus_A_theta_head_B_seed21\modern_tcn_seed21.onnx`
- sample: `results\modern_tcn\modern_tcn_v4_turn_focus_A_theta_head_B_seed21\modern_tcn_seed21_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 5.72205e-06 | 1.58759e-06 | 1 |
| logits_turn | 7.62939e-06 | 1.87134e-06 | 1 |
| theta_hat | 4.47035e-08 | 1.78698e-08 | 1 |
