# E4 flatreg001 rerun training and closed-loop summary

- timestamp: 2026-06-22 18:54
- candidate: `mode_theta_detach_flatreg001_seed21_rerun_20260622`
- source intent: retrain the unrecoverable `mode_theta_detach_flatreg001_seed21` parameters, then run one closed-loop sandbox without overwriting the original run directory.
- status: `CLOSED_LOOP_SANDBOX_PASS`
- formal validation: `false`
- original `mode_theta_detach_flatreg001_seed21` overwritten: `false`

## Training

- checkpoint: `results/modern_tcn_sci_innovation/04_mode_conditioned_theta/mode_theta_detach_flatreg001_seed21_rerun_20260622/modern_tcn_mode_theta_seed21.pt`
- config: `small_mode_theta`, `loss_mode=fixed`, `seed=21`, `theta_gate_detach=true`, `flat_theta_reg_lambda=0.01`
- best_epoch: 72
- test acc_main: 0.969739
- test acc_turn_transition: 0.482861
- test theta_mae_deg: 0.616433
- test flat_recall: 0.966931
- test slope_recall: 0.981091

## ONNX

- onnx: `results/modern_tcn_sci_innovation/04_mode_conditioned_theta/mode_theta_detach_flatreg001_seed21_rerun_20260622/onnx_sandbox/mode_theta_detach_flatreg001_seed21_rerun_20260622.onnx`
- ONNXRuntime consistency: `pass=1`
- max_abs_error: logits_main 8.583e-06, logits_turn 4.768e-06, theta_hat 2.068e-07
- mean_abs_error: logits_main 2.043e-06, logits_turn 1.075e-06, theta_hat 3.388e-08

## Closed-loop Sandbox

- path: `data/paths/path_closed_loop_sharp_turn_transition_theta10_v1.mat`
- output root: `results/modern_tcn_sci_innovation/04_mode_conditioned_theta/e4_cl_001r_20260622`
- baseline ONNX: locked seed101 plantfix baseline
- candidate ONNX: rerun flatreg001 ONNX above
- report: `results/modern_tcn_sci_innovation/04_mode_conditioned_theta/e4_cl_001r_20260622/e4_001r_report.md`
- summary csv: `results/modern_tcn_sci_innovation/04_mode_conditioned_theta/e4_cl_001r_20260622/e4_001r_summary.csv`
- rank csv: `results/modern_tcn_sci_innovation/04_mode_conditioned_theta/e4_cl_001r_20260622/e4_001r_rank.csv`

## Overall Closed-loop Metrics

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | j_du | viol_rate | theta_mae_deg | main_acc_pct | turn_acc_pct | overall_rank |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline_lock_seed101 | 0.040584 | 0.126903 | 0.041595 | 0.035577 | 0.021913 | 0.513653 | 5.323703 | 0 | 0.600178 | 94.1371 | 48.8449 | 2 |
| mode_theta_detach_flatreg001_seed21_rerun_20260622 | 0.028053 | 0.057274 | 0.022436 | 0.033478 | 0.012392 | 0.312007 | 2.441195 | 0 | 0.563557 | 96.0396 | 70.0835 | 1 |

## Delta vs Locked Baseline

- ey_rmse: -0.012531
- ey_peak: -0.069629
- epsi_rmse: -0.019159
- ev_rmse: -0.002099
- eomega_rmse: -0.009521
- xy_rmse: -0.201646
- j_du: -2.882507
- theta_mae_deg: -0.036621
- main_acc_pct: +1.902543
- turn_acc_pct: +21.238594

## Notes

- The first closed-loop attempt wrote MAT files under a much longer nested path. Both simulations finished, but `compare_tcn_gru_modern_closed_loop_out` could not load the long-path candidate MAT. Those diagnostic files were left in the rerun directory and are not used for the decision.
- The accepted closed-loop evidence is the second run under the shorter E4 path `e4_cl_001r_20260622`.
- This is a sandbox check only. It does not change the earlier E4 offline-gate conclusion and does not count as formal MATLAB/Simulink validation expansion.
