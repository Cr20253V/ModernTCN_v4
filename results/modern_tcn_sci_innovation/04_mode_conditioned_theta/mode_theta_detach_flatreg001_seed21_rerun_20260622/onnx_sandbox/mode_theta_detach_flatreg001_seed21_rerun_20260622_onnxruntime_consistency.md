# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\modern_tcn_sci_innovation\04_mode_conditioned_theta\mode_theta_detach_flatreg001_seed21_rerun_20260622\onnx_sandbox\mode_theta_detach_flatreg001_seed21_rerun_20260622.onnx`
- sample: `results\modern_tcn_sci_innovation\04_mode_conditioned_theta\mode_theta_detach_flatreg001_seed21_rerun_20260622\onnx_sandbox\mode_theta_detach_flatreg001_seed21_rerun_20260622_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 8.58307e-06 | 2.04255e-06 | 1 |
| logits_turn | 4.76837e-06 | 1.07537e-06 | 1 |
| theta_hat | 2.06754e-07 | 3.38769e-08 | 1 |
