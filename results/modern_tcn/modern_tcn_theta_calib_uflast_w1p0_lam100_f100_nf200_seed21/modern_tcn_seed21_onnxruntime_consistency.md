# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\modern_tcn\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_seed21.onnx`
- sample: `results\modern_tcn\modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21\modern_tcn_seed21_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 5.72205e-06 | 1.94088e-06 | 1 |
| logits_turn | 7.62939e-06 | 2.38667e-06 | 1 |
| theta_hat | 6.70552e-08 | 1.82918e-08 | 1 |
