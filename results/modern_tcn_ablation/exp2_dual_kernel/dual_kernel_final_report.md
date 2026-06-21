# dual_kernel Final Report

## Decision

- decision: `NO_PROMOTION`
- stop_node: `D8_offline_gate`
- runs: `9`
- best_run: `dual_k31_s7_seed42`
- reason: no default k31 dual-kernel candidate passed the combined offline and boundary gates.

## Baseline

- baseline: `ModernTCN_turn_l020_tt25_seed101`
- input_dim: `22`
- seq_len: `128`
- plant_revision: `agv_physics_v2_plantfix`
- feature_contract: `passive17_plus_all5`
- baseline_boundary_source: `baseline_boundary_metrics_exp2.csv`

## Best Candidate

- run_tag: `dual_k31_s7_seed42`
- checkpoint: `results/modern_tcn_ablation/exp2_dual_kernel/dual_k31_s7_seed42/modern_tcn_dualkernel_seed42.pt`
- acc_main: `0.9597445863409217`
- acc_turn: `0.5746807329261522`
- acc_turn_transition: `0.5052160953800298`
- theta_mae_deg: `0.9414589405059814`
- stall_recall: `0.625`
- theta_edge_p95_abs_err: `3.2611522674560547`
- false_turn_straight: `0.42524573202276256`
- flat_peak_theta_error: `7.065547943115234`
- offline_gate_failures: `acc_main`, `theta_mae_deg`, `flat_recall`, `stall_recall`, `theta_edge_p95_abs_err`, `flat_peak_theta_error`

## Group Means

| config | n | acc_main | acc_turn | acc_turn_transition | theta_mae_deg | gate_passes |
|---|---:|---:|---:|---:|---:|---:|
| `dual_k31_s3` | 3 | 0.965205 | 0.550250 | 0.473423 | 0.997132 | 0 |
| `dual_k31_s5` | 3 | 0.959837 | 0.516935 | 0.446597 | 0.845044 | 0 |
| `dual_k31_s7` | 3 | 0.964649 | 0.560429 | 0.482365 | 0.760435 | 0 |

## Not Executed

- D9 `dual_k51_s5`: skipped because default k31 branch was not near-passing across the combined gate.
- D10 ONNX export: not executed.
- D11 MATLAB consistency / namespace audit: not executed.
- D12-D14 closed-loop stages: not executed.

## Evidence

- D0 baseline preflight: `D0_preflight_baseline.md`
- D1 model API: `D1_model_api_report.md`
- D2 CLI contract: `D2_cli_contract.md`
- D3 deployment API: `D3_deployment_api_report.md`
- D4 summary schema: `../_schemas/dual_kernel_metrics_schema.md`
- D5 smoke: `_smoke/dual_k31_s5_seed21_smoke/D5_smoke_report.md`
- D6 single-seed gate: `D6_single_seed_gate.md`
- D8 offline summary: `dual_kernel_offline_summary.csv`, `dual_kernel_offline_summary.md`, `best_run_selection.md`
- D9 skip: `D9_skip.md`
