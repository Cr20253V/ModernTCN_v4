# E4 Smoke Report

- status: PASS
- no ONNX export: True
- no MATLAB/Simulink closed-loop: True

| check | status | detail |
|---|---|---|
| `small_dry_run` | `dry_run_ok` | `dry_run forward ok` |
| `small_mode_theta_dry_run` | `dry_run_ok` | `dry_run forward ok` |
| `baseline_checkpoint_regression` | `PASS` | `[(4, 3), (4, 3), (4, 1)]` |
| `detach_gradient_probe` | `PASS` | `detached_grad=0.000e+00, attached_grad=3.145e+01` |
| `no_overwrite_probe` | `PASS` | `existing non-empty dir rejected` |
| `expert_stats_probe` | `PASS` | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_sci_innovation\04_mode_conditioned_theta\_smoke\expert_stats_probe\expert_differentiation_statistics.json` |
