# V6 Longrun Diag2Steer Baseline Before Balanced Build

- Recorded: 2026-05-11
- New balanced tag reserved: `v6_longrun_diag2steer_balanced`
- Existing `v6_longrun_diag2steer` data/model outputs are intentionally not reused as balanced outputs.

## Existing V6 Dataset

| artifact | path | last write | bytes |
|---|---|---:|---:|
| dataset | `data/tcn/ModernTCN_dataset_v6_longrun_diag2steer.mat` | 2026-05-10 00:48:11 +08:00 | 185782996 |
| train data | `data/tcn/ModernTCN_train_data_v6_longrun_diag2steer.mat` | 2026-05-10 00:32:31 +08:00 | 158555137 |
| scaler | `data/tcn/ModernTCN_scaler_v6_longrun_diag2steer.mat` | 2026-05-10 00:48:11 +08:00 | 1188 |
| split | `data/tcn/ModernTCN_shared_run_split_v6_longrun_diag2steer.mat` | 2026-05-10 00:48:07 +08:00 | 6606 |
| theta coverage | `results/modern_tcn/ModernTCN_dataset_v6_longrun_diag2steer_theta_coverage.md` | 2026-05-10 00:48:13 +08:00 | 2119 |

## Existing ModernTCN Candidate

Latest exported/calibrated candidate:

- checkpoint: `results/modern_tcn/modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select_scale1p02/modern_tcn_seed42.pt`
- ONNX: `results/modern_tcn/modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select_scale1p02/modern_tcn_seed42.onnx`
- MATLAB full-test: `results/modern_tcn/matlab_full_testset_modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select_scale1p02/ModernTCN_v1_matlab_full_testset_summary.csv`
- theta scatter: `results/paper/modern_tcn_theta_scatter/modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select_scale1p02/modern_tcn_theta_scatter_report.md`
- rich-window scatter: `results/paper/modern_tcn_theta_sweep_plot/modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_stage2_t080_p95select_scale1p02/rich_window_v4/modern_tcn_theta_sweep_report.md`

Best P95-repair sweep row before calibration:

| run_tag | score | theta MAE | theta P95 | near-flat P95 | true-zero P95 | main | turn | turn transition | slope recall |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `modern_tcn_v6_theta_p95_s42_gate_p0p25_f0p10_tail_neg80_uf` | 5.0687 | 0.2965 | 1.3244 | 0.4263 | 0.4268 | 0.9773 | 0.9397 | 0.6882 | 0.9416 |

## Notes

- The current git worktree already contains many unrelated tracked and untracked changes. This record only freezes the relevant v6 artifacts for this balanced run.
- Balanced outputs must use `v6_longrun_diag2steer_balanced` names and must not overwrite the files listed above.
