# Uncertainty Seed101 Rerun Sandbox Closed-Loop Summary

- status: `PASS_SANDBOX`
- scope: sandbox-only rerun closed-loop, not formal validation.
- candidate: `uncertainty_seed101_rerun_20260622`
- rerun checkpoint: `results/modern_tcn_sci_innovation/01_loss_optimization/uncertainty_seed101_rerun_20260622/modern_tcn_seed101.pt`
- candidate ONNX: `results/modern_tcn_metric_rebuild/05_sandbox_closed_loop_if_needed/00_exported_onnx/uncertainty_seed101_rerun_20260622/uncertainty_seed101_rerun_20260622.onnx`
- path: `data/paths/path_closed_loop_sharp_turn_transition_theta10_v1.mat`
- baseline: `baseline_lock`
- formal validation: `false`
- formal compare write: `false`

## Closed-Loop Result

| controller | ey_rmse | epsi_rmse | xy_rmse | j_du | viol_rate | theta_mae_deg | main_acc_pct | turn_acc_pct | overall_rank |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `uncertainty_seed101_rerun_20260622` | 0.0291805 | 0.0342259 | 0.438300 | 2.16207 | 0 | 0.48299 | 91.982 | 62.706 | 1 |
| `baseline_lock` | 0.0405838 | 0.0415952 | 0.513653 | 5.32370 | 0 | 0.60018 | 94.137 | 48.845 | 2 |

## Evidence Files

- summary: `uncertainty_seed101_rerun_summary.csv`
- rank: `uncertainty_seed101_rerun_rank.csv`
- report: `uncertainty_seed101_rerun_report.md`
- status: `uncertainty_seed101_rerun_status.json`
- candidate output MAT: `uncertainty_seed101_rerun_20260622_out.mat`
- baseline output MAT: `baseline_lock_out.mat`
- MATLAB stdout: `../uncertainty_seed101_rerun_matlab_stdout.log`
- ONNXRuntime consistency: `../00_exported_onnx/uncertainty_seed101_rerun_20260622/uncertainty_seed101_rerun_20260622_onnxruntime_consistency.json`

## Boundary

This result evaluates a rerun candidate. It is not a restored historical `uncertainty_seed101` checkpoint and must not be used to rewrite the historical E1 record.
