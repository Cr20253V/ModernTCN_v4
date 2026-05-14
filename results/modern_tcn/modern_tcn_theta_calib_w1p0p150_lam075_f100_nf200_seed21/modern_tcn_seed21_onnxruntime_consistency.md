# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\modern_tcn\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_seed21.onnx`
- sample: `results\modern_tcn\modern_tcn_theta_calib_w1p0p150_lam075_f100_nf200_seed21\modern_tcn_seed21_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 5.72205e-06 | 1.58759e-06 | 1 |
| logits_turn | 7.62939e-06 | 1.87134e-06 | 1 |
| theta_hat | 5.21541e-08 | 2.04891e-08 | 1 |
