# exp3 patch_full rescue report

## 结论

- 本轮 rescue 不晋级：不导出 ONNX、不进入 MATLAB/Simulink、不跑闭环。
- `densepatch` 是有效挽救方向：R3/R4 均把 `theta_mae_deg` 拉回 baseline 附近或更优，并把 `acc_turn_transition` 恢复到 baseline 附近或更高。
- 仍未达到正式 gate：主要短板是 `acc_main` 和 `stall_recall`，R3 还缺 `slope_recall`，R4 还缺 `theta_edge_p95_abs_err`。
- 若继续，不应直接 9-run 全矩阵或 promote；建议另开一个窄范围 densepatch rescue 计划。

## Baseline 与 gate

- baseline source: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101_summary.csv`
- `acc_main` baseline=0.966963 gate >= 0.963963
- `acc_turn` baseline=0.578845 gate >= 0.573845
- `acc_turn_transition` baseline=0.497765 gate >= 0.497765
- `theta_mae_deg` baseline=0.679395 gate <= 0.689395
- `flat_recall` baseline=0.969577 gate >= 0.959577
- `stall_recall` baseline=0.718750 gate >= 0.668750
- `slope_recall` baseline=0.974909 gate >= 0.969909
- `theta_edge_p95_abs_err` baseline=2.755057 gate <= 2.755057

## Rescue runs

| run | formal gate | acc_main | acc_turn | acc_turn_transition | theta_mae_deg | theta_edge_p95 | flat | stall | slope |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `full128_light_theta_select_seed21` | FAIL | 0.950861 | 0.578845 | 0.467958 | 0.748058 | 2.909252 | 0.945767 | 0.635417 | 0.963273 |
| `full128_light_theta_loss_seed21` | FAIL | 0.955858 | 0.581621 | 0.472429 | 0.791792 | 3.934220 | 0.972222 | 0.677083 | 0.961091 |
| `full128_densepatch_theta_select_seed21` | FAIL | 0.951416 | 0.602998 | 0.517139 | 0.570603 | 2.497931 | 0.965608 | 0.614583 | 0.959273 |
| `full128_densepatch_theta_loss_seed21` | FAIL | 0.958634 | 0.579400 | 0.499255 | 0.618801 | 3.384803 | 0.966931 | 0.614583 | 0.968364 |

## 逐项判断

- R1 `light + selector`: theta 从 D6 的 2.198 降到 0.748，但 transition、flat、stall、slope 仍不过线。
- R2 `light + theta loss`: flat/stall 有改善，但 theta 与 transition 仍不过线。
- R3 `densepatch + selector`: 最有价值的信号，transition=0.517139 超过 baseline，theta=0.570603 优于 baseline，edge 也优于 baseline；但 acc_main、stall、slope 不过线。
- R4 `densepatch + theta loss`: 更均衡，acc_main/slope 比 R3 回升，transition=0.499255 略高于 baseline，theta=0.618801 仍优于 baseline；但 stall 仍低，edge 退化。

## 后续建议

1. 不基于本轮 rescue 单 seed promote。
2. 若继续，应只围绕 `patch_size=8, patch_stride=2, dims=16,32` 开一个新的窄范围计划。
3. 优先验证 `densepatch + selector-only` 的多 seed 稳定性，再尝试更轻的 theta loss，例如降低 `lambda_theta` 或 `theta_neg_weight`，目标是保住 R3 的 transition/edge，同时补回 acc_main/stall/slope。
4. 在新的离线 gate 通过前，继续禁止 ONNX、MATLAB/Simulink 和闭环验证。

## 生成文件

- `results\modern_tcn_ablation\exp3_patch_full_rescue\rescue_summary.csv`
- `results\modern_tcn_ablation\exp3_patch_full_rescue\rescue_gate_matrix.csv`
- `results\modern_tcn_ablation\exp3_patch_full_rescue\rescue_decision.json`
- `results\modern_tcn_ablation\exp3_patch_full_rescue\rescue_report.md`
