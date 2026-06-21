# exp3 patch_full densepatch continuation report

## 结论

- C1/C2/C3 均未通过完整离线 gate，按计划停止，不扩展 seed42/101。
- 本轮没有导出 ONNX，没有运行 MATLAB/Simulink，没有写 closed-loop 或 compare 目录。
- 最有价值的是 C3 `densepatch_wide24_seed21`：theta、transition、edge、stall 都过线，但 `acc_main` 和 `slope_recall` 仍不过线。
- 因此 densepatch/full 仍只能作为研究线索，不能作为候选模型晋级。

## Baseline gate

- baseline source: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101_summary.csv`
- `acc_main` baseline=0.966963 gate >= 0.963963
- `acc_turn` baseline=0.578845 gate >= 0.573845
- `acc_turn_transition` baseline=0.497765 gate >= 0.497765
- `theta_mae_deg` baseline=0.679395 gate <= 0.689395
- `flat_recall` baseline=0.969577 gate >= 0.959577
- `stall_recall` baseline=0.718750 gate >= 0.668750
- `slope_recall` baseline=0.974909 gate >= 0.969909
- `theta_edge_p95_abs_err` baseline=2.755057 gate <= 2.755057

## Seed21 continuation runs

| run | gate | acc_main | acc_turn | transition | theta_mae | edge_p95 | flat | stall | slope | failed metrics |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `densepatch_select_stall_seed21` | FAIL | 0.951416 | 0.602998 | 0.517139 | 0.570603 | 2.497931 | 0.965608 | 0.614583 | 0.959273 | acc_main, stall_recall, slope_recall |
| `densepatch_mainweight_seed21` | FAIL | 0.949473 | 0.590228 | 0.521610 | 0.623545 | 2.902961 | 0.969577 | 0.614583 | 0.955636 | acc_main, stall_recall, slope_recall, theta_edge_p95_abs_err |
| `densepatch_wide24_seed21` | FAIL | 0.951138 | 0.584675 | 0.517139 | 0.542230 | 2.413190 | 0.966931 | 0.677083 | 0.956364 | acc_main, slope_recall |

## 逐项判断

- C1 `select_stall_weight`: selection 权重确实写入，但结果等价于 R3；不能补回 stall/main/slope。
- C2 `main_class_multipliers + slope weights`: 主类权重调整没有救回 stall，且 `acc_main` 和 `slope_recall` 更差。
- C3 `dims=24,48`: 增容有效改善 `theta_mae_deg=0.542230`、`acc_turn_transition=0.517139`、`theta_edge_p95_abs_err=2.413190`、`stall_recall=0.677083`，但 `acc_main=0.951138` 与 `slope_recall=0.956364` 离 gate 仍远。

## 后续建议

1. 不建议继续在 exp3 patch_full 上做 seed 扩展或部署验证。
2. 若必须继续研究，只应另开计划，先从主类头/标签边界/样本分布诊断开始，而不是直接继续调 patch/full。
3. 当前结论应记录为 patch/full 在 22D plantfix seq128 下未能离线晋级。

## 输出文件

- `results\modern_tcn_ablation\exp3_patch_full_densepatch_continuation\continuation_summary.csv`
- `results\modern_tcn_ablation\exp3_patch_full_densepatch_continuation\continuation_gate_matrix.csv`
- `results\modern_tcn_ablation\exp3_patch_full_densepatch_continuation\continuation_decision.json`
- `results\modern_tcn_ablation\exp3_patch_full_densepatch_continuation\continuation_report.md`
