# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\modern_tcn\modern_tcn_theta_calib_uflast_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_seed21.onnx`
- sample: `results\modern_tcn\modern_tcn_theta_calib_uflast_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_seed21_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 5.72205e-06 | 1.75772e-06 | 1 |
| logits_turn | 7.62939e-06 | 2.0694e-06 | 1 |
| theta_hat | 3.72529e-08 | 1.35769e-08 | 1 |
