# ModernTCN ONNXRuntime 一致性检查

- onnx: `results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\00_exported_onnx\uncertainty_seed101_rerun_20260622\uncertainty_seed101_rerun_20260622.onnx`
- sample: `results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\00_exported_onnx\uncertainty_seed101_rerun_20260622\uncertainty_seed101_rerun_20260622_pytorch_reference.mat`
- pass: `1`

| output | max abs error | mean abs error | pass |
|---|---:|---:|---:|
| logits_main | 6.67572e-06 | 1.88251e-06 | 1 |
| logits_turn | 4.08292e-06 | 1.05208e-06 | 1 |
| theta_hat | 8.9407e-08 | 2.58442e-08 | 1 |
