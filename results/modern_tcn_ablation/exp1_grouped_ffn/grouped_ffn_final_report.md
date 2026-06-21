# grouped_ffn Final Report

## Decision

- decision: `NO_PROMOTION`
- stop_node: `node8_offline_gate`
- reason: no grouped_ffn run passed the quantified offline promotion gate; ONNX, MATLAB, and closed-loop nodes were not executed.
- attribution_boundary: same 22D plantfix dataset and near-baseline training recipe; conclusion is limited to this grouped FFN structure/recipe combination.

## Baseline

- acc_main: `0.9669627984453082`
- acc_turn: `0.5788450860632982`
- acc_turn_transition: `0.4977645305514158`
- theta_mae_deg: `0.6793947815895081`
- flat_recall: `0.9695767195767195`
- stall_recall: `0.71875`
- slope_recall: `0.974909090909091`

## Best Offline Candidate

- run_tag: `gffn_d4_k51_seed21`
- checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_ablation\exp1_grouped_ffn\gffn_d4_k51_seed21\modern_tcn_gffn_seed21.pt`
- offline_gate: `0`
- offline_gate_failures: `acc_main 0.963631 >= 0.963963 failed; acc_turn 0.568573 >= 0.573845 failed; stall_recall 0.635417 >= 0.66875 failed`
- acc_main: `0.9636313159355914`
- acc_turn: `0.5685730149916713`
- acc_turn_transition: `0.5067064083457526`
- theta_mae_deg: `0.6263420581817627`
- flat_recall: `0.9682539682539683`
- stall_recall: `0.6354166666666666`
- slope_recall: `0.9738181818181818`
- param_count: `85903`

## Top Offline Runs

| run_tag | acc_main | acc_turn | acc_turn_transition | theta_mae_deg | failures |
|---|---:|---:|---:|---:|---|
| `gffn_d4_k51_seed21` | 0.963631 | 0.568573 | 0.506706 | 0.626342 | acc_main 0.963631 >= 0.963963 failed; acc_turn 0.568573 >= 0.573845 failed; stall_recall 0.635417 >= 0.66875 failed |
| `gffn_d3_k31_seed21` | 0.961410 | 0.546641 | 0.484352 | 0.738616 | acc_main 0.96141 >= 0.963963 failed; acc_turn 0.546641 >= 0.573845 failed; acc_turn_transition 0.484352 >= 0.497765 failed; theta_mae_deg 0.738616 <= 0.689395 failed; slope_recall 0.967273 >= 0.969909 failed; stall_recall 0.635417 >= 0.66875 failed |
| `gffn_d4_k51_seed42` | 0.964464 | 0.551638 | 0.475410 | 0.599368 | acc_turn 0.551638 >= 0.573845 failed; acc_turn_transition 0.47541 >= 0.497765 failed; stall_recall 0.645833 >= 0.66875 failed |
| `gffn_d4_k31_seed42` | 0.964742 | 0.559134 | 0.475410 | 0.603667 | acc_turn 0.559134 >= 0.573845 failed; acc_turn_transition 0.47541 >= 0.497765 failed; stall_recall 0.635417 >= 0.66875 failed |
| `gffn_d4_k31_seed21` | 0.967796 | 0.565242 | 0.475410 | 0.803981 | acc_turn 0.565242 >= 0.573845 failed; acc_turn_transition 0.47541 >= 0.497765 failed; theta_mae_deg 0.803981 <= 0.689395 failed; stall_recall 0.614583 >= 0.66875 failed |

## Evidence Files

- offline summary csv: `results\modern_tcn_ablation\exp1_grouped_ffn\grouped_ffn_offline_summary.csv`
- offline summary md: `results\modern_tcn_ablation\exp1_grouped_ffn\grouped_ffn_offline_summary.md`
- best selection: `results\modern_tcn_ablation\exp1_grouped_ffn\best_run_selection.md`
- baseline snapshot: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_ablation\_baseline_snapshot\baseline_offline_metrics.csv`

## Not Executed

- ONNX export: not executed because node8 gate failed.
- ONNXRuntime latency: not executed because node8 gate failed.
- MATLAB ONNX consistency: not executed because node8 gate failed.
- closed-loop preflight and Simulink runs: not executed because node8 gate failed.
