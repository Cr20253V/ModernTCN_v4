# ModernTCN SCI Innovation E2 Handoff

更新时间：2026-06-21  
仓库：`E:\Matlab\Simulink\S-Function_16`  
阶段：`E2 / 02_hard_sample_loss`  

## 结论

E2 流程执行完成，状态为 `PASS`，但实验结论是负结果：

- 方法标签：`hard-sample focal only`
- `theta_smooth_status=disabled_contract_limited`
- 正式 seed21 runs：4
- `eligible_runs=0`
- `promotable_runs=0`
- 不建议扩展 seeds `42/101`
- 可以进入 E3，但 E3 应继续使用原 baseline fixed loss，不使用 E2 focal 设置

`theta smoothness` 没有被测试，也不应记录为负结果。当前 dataset 只有 `run_id_*`，没有可靠 window/order 字段；`run_id` 也不是按同一 run 连续排序，因此不能安全构造同 run 相邻窗口 smooth loss。

## 必读证据

- `results/modern_tcn_sci_innovation/02_hard_sample_loss/e2_preflight.md`
- `results/modern_tcn_sci_innovation/02_hard_sample_loss/e2_smoke_report.md`
- `results/modern_tcn_sci_innovation/02_hard_sample_loss/hard_sample_loss_summary.md`
- `results/modern_tcn_sci_innovation/02_hard_sample_loss/hard_sample_loss_decision.json`
- `results/modern_tcn_sci_innovation/02_hard_sample_loss/hard_sample_loss_master_table.csv`

## Baseline Reference

Baseline 来自：

`results/paper/agv_model_parameter_correction_workflow/08_models/modern_tcn/modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101/modern_tcn_seed101_summary.csv`

关键参考值：

| metric | baseline |
|---|---:|
| acc_main | 0.966963 |
| acc_turn | 0.578845 |
| acc_turn_transition | 0.497765 |
| theta_mae_deg | 0.679395 |
| flat_recall | 0.969577 |
| stall_recall | 0.718750 |
| slope_recall | 0.974909 |
| theta_edge_p95_abs_err | 2.755057 |
| flat_peak_theta_error | 5.335740 |

注意：`theta_edge_p95_abs_err` 和 `flat_peak_theta_error` 是从 champion summary 补全的，不来自简化版 E0 baseline CSV。

## E2 Run Ranking

| rank | run_tag | eligible | promotable | d_turn_transition | d_stall | d_theta_mae | d_edge | d_flat_peak |
|---:|---|---|---|---:|---:|---:|---:|---:|
| 1 | `fs_t05_s05_sm000_seed21` | False | False | -0.019374 | -0.062500 | -0.103023 | -0.609695 | -1.699067 |
| 2 | `fs_t02_s02_sm000_seed21` | False | False | -0.043219 | -0.052083 | -0.136571 | -0.681780 | -2.419980 |
| 3 | `fs_t02_s05_sm000_seed21` | False | False | -0.055142 | -0.041667 | -0.236372 | -1.496581 | -0.860416 |
| 4 | `fs_t05_s02_sm000_seed21` | False | False | +0.008942 | -0.020833 | -0.275117 | -0.998847 | -2.914490 |

`fs_t05_s02_sm000_seed21` 是唯一提升 `acc_turn_transition` 的 run，但同时 `acc_main`、`acc_turn`、`theta_mae_deg`、`flat_recall`、`theta_edge_p95_abs_err` 和 `flat_peak_theta_error` 均未过保护线，因此不能晋级。

## 实现改动

新增或更新的源码：

- `src/ModernTCN/modern_tcn_model.py`
  - 在 `ModernTCNConfig` 中加入 E2 参数：`lambda_transition_focal`、`lambda_stall_focal`、`lambda_theta_smooth`、`focal_gamma`、`theta_smooth_mode`。
- `src/ModernTCN/modern_tcn_metrics.py`
  - 增加 transition focal、stall focal 的 raw/weighted loss 分量。
  - 增加 `loss_main_bundle_base`、`loss_turn_bundle_base`、`loss_theta_bundle_base`，用于 loss scale 审计。
  - 增加 `flat_as_stall_ratio`、`stall_as_flat_ratio`、`cm_main`、`cm_turn` 输出。
  - 当 `lambda_theta_smooth > 0` 或 smooth mode 非 off 时直接报错，避免伪造 smooth loss。
- `src/ModernTCN/train_modern_tcn.py`
  - 增加 E2 CLI 参数。
  - history/config/report 保存新增 loss 分量、confusion matrix、误判比例和 `theta_smooth_status`。
- `src/ModernTCN/run_sci_e2_hard_sample_loss.py`
  - E2 专用编排脚本，负责 preflight、零损失等价测试、`--no-overwrite` 探针、smoke、正式 seed21 网格和 decision 汇总。

复现命令：

```powershell
python src\ModernTCN\run_sci_e2_hard_sample_loss.py
```

当前 E2 run 目录已经存在，直接重跑会被 `--no-overwrite` 阻止。若需要重跑，必须先另开新的输出目录或新 run tag，不要覆盖当前结果。

## 验证记录

- `python -m py_compile src\ModernTCN\modern_tcn_model.py src\ModernTCN\modern_tcn_metrics.py src\ModernTCN\train_modern_tcn.py src\ModernTCN\run_sci_e2_hard_sample_loss.py` 通过。
- zero-loss equivalence 已验证：新增参数全为 0/off 时 fixed baseline loss 行为不变。
- `--no-overwrite` 探针已验证。
- smoke 三项全部通过，未触发 loss scale 降档：
  - transition/base_turn 最大约 `0.464577`
  - stall/base_main 最大约 `0.138168`
- 每个正式 run 都保存了 checkpoint、summary CSV、history CSV、`config.json`、`git_hash.txt`、`dataset_contract_copy.json`、`feature_names.txt`、train report。
- E2 输出目录内 `.onnx` 数量为 0。
- E2 输出目录内 `generated_layers` / `closed_loop` / `compare` 目录数量为 0。
- 未运行 MATLAB/Simulink 闭环。
- 未覆盖 baseline checkpoint、baseline ONNX、旧 ablation 或旧 compare 目录。

## 下一阶段建议

进入 E3：`03_physics_group_gate`。

E3 默认策略：

```json
{
  "source": "baseline_fixed_loss",
  "loss_mode": "fixed",
  "reason": "E2 has no promotable run; continue E3 with original baseline fixed loss"
}
```

执行 E3 前应读取：

1. `results/modern_tcn_sci_innovation/ModernTCN_small_SCI_innovation_requirements_for_CODEX.md`
2. `results/modern_tcn_sci_innovation/00_baseline_lock/e0_decision.json`
3. `results/modern_tcn_sci_innovation/01_loss_optimization/loss_optimization_decision.json`
4. `results/modern_tcn_sci_innovation/02_hard_sample_loss/hard_sample_loss_decision.json`
5. 本文件

E3 硬性约束建议：

- 不继续 E2 focal 调参。
- 不扩展 E2 seeds `42/101`。
- 不把 E2 best failed run 当作后续 baseline。
- E3 只写入 `results/modern_tcn_sci_innovation/03_physics_group_gate/` 或必要源码位置。
- 保留 `model_family=small` 的默认行为；新增结构必须使用新的 model family。
- E3 离线 gate 前不得导出 ONNX，不得进入 MATLAB/Simulink 闭环。

## 给下一轮 Codex 的简短指令

请继续 ModernTCN SCI innovation 工作流的 E3 / Phase 3：Physics-Group Residual Gate。先读取本文件和 E2 decision。E2 已完成且无 promotable run，因此 E3 使用原 baseline fixed loss，不继承任何 E2 focal 设置；不要重跑 E2，不要扩展 E2 seeds，不要导出 ONNX，不要运行 MATLAB/Simulink。只在 `results/modern_tcn_sci_innovation/03_physics_group_gate/` 下产出 E3 结果，必要源码改动需保持 `model_family=small` 默认行为不变。
