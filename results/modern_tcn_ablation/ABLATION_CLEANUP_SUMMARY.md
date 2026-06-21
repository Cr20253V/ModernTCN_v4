# ModernTCN 22D Ablation Cleanup Summary

更新时间：2026-06-21

## 范围

本次清理只覆盖 `results/modern_tcn_ablation/` 下的三个 ModernTCN 消融实验结果目录，不回退 `src/ModernTCN/` 中为实验新增或修改的模型、训练、导出、指标和延迟测试框架代码。

当前可信 baseline 仍固定为：

- plant revision: `agv_physics_v2_plantfix`
- feature contract: `passive17_plus_all5`
- input_dim: `22`
- seq_len: `128`
- retained champion: `turn_l020_tt25_tcm14_stw055_slrw060_seed101`

## 总结论

三个实验方向均未产生可替代当前项目结果的候选模型：

- `exp1_grouped_ffn`: `NO_PROMOTION`，离线 gate 未通过，未进入 ONNX、MATLAB 或闭环。
- `exp2_dual_kernel`: `NO_PROMOTION` / tuning `STOP_NO_MULTISEED`，默认 sweep 和 seed21 调参均未通过组合 gate，未进入 ONNX、MATLAB 或闭环。
- `exp3_patch_full`: `NO_PROMOTION`，formal full128、rescue、densepatch continuation 均未通过完整离线 gate，未进入 ONNX、MATLAB 或闭环。

因此，这批官方 ModernTCN 配置只能作为负结果和后续结构诊断参考，不应作为当前论文/项目对比结果的替换链路。

## 已保留

保留内容用于复盘实验流程、复用脚手架、追溯 gate 口径：

- 总体技术合同：`ModernTCN_v4_22dim_ablation_plan_for_CODEX.md`
- baseline 快照：`_baseline_snapshot/`
- 指标 schema：`_schemas/`
- 三个复用工具脚本：`exp1_tools.py`、`exp2_tools.py`、`exp3_tools.py`
- 各实验最终报告、summary 表、decision JSON、节点报告和跳过/未执行说明

主要保留证据：

- `exp1_grouped_ffn/grouped_ffn_final_report.md`
- `exp1_grouped_ffn_tune/grouped_ffn_tuning_report.md`
- `exp2_dual_kernel/dual_kernel_final_report.md`
- `exp2_dual_kernel_tune/dual_kernel_tuning_final_report.md`
- `exp3_patch_full/patch_full_final_report.md`
- `exp3_patch_full_rescue/rescue_report.md`
- `exp3_patch_full_densepatch_continuation/continuation_report.md`

## 已删除

删除内容为可再生成、且不再支撑晋级结论的过程产物：

- Python 缓存：`__pycache__/`
- 单次训练 run 目录：`gffn_*`、`tune_*`、`dual_*`、`full128_*`、`densepatch_*`
- smoke / logs / 临时工程预检目录：`_smoke/`、`_logs/`、`_engineering_preflight/`
- exp1 一次性批处理训练脚本：`run_node7_train_remaining.ps1`、`run_node8_k51.ps1`、`run_round*_seed21.ps1`
- 上述目录内的 checkpoint、训练日志、history、逐 run config 和中间文本文件

未删除任何 baseline 主链、ONNX 部署链、Simulink 闭环结果或 `results/paper/agv_model_parameter_correction_workflow/` 下的当前结果链。

## 三个实验流程

### exp1_grouped_ffn

流程：技术合同与工程预检 -> smoke -> 多配置/多 seed 离线训练 -> summary/gate -> seed21 小范围 tuning -> 停止。

结论：原始 sweep 和 tuning 都没有候选通过完整离线 gate。`grouped_ffn` 能在局部 transition 或 theta 指标上产生改善，但会牺牲 `acc_main`、`acc_turn` 或 `stall_recall`，综合 gate 不成立。

保留入口：

- `exp1_grouped_ffn/grouped_ffn_final_report.md`
- `exp1_grouped_ffn/EXP1_GROUPED_FFN_HANDOFF.md`
- `exp1_grouped_ffn/grouped_ffn_offline_summary.csv`
- `exp1_grouped_ffn_tune/grouped_ffn_tuning_report.md`

### exp2_dual_kernel

流程：D0 baseline/preflight -> D1-D4 API 和 schema 合同 -> smoke/single-seed -> 默认 k31 sweep -> offline gate -> seed21 targeted tuning -> 停止。

结论：`dual_kernel` 不是训练崩溃问题，而是局部响应分支会引入 flat/stall 和 theta boundary 风险。调参能找到 theta 较好的候选，但 transition、flat、stall、edge 或 peak 指标无法同时满足 gate。

保留入口：

- `exp2_dual_kernel/dual_kernel_final_report.md`
- `exp2_dual_kernel/dual_kernel_offline_summary.csv`
- `exp2_dual_kernel_tune/dual_kernel_tuning_final_report.md`
- `exp2_dual_kernel_tune/tuning_all_summary.csv`

### exp3_patch_full

流程：独立于旧 `ModernTCN_full` 结果重新做 full128 合同与预检 -> smoke/single-seed gate -> rescue -> densepatch continuation -> 停止。

结论：formal full128 在 single-seed 阶段即因 theta 明显失败而停止。后续 densepatch rescue 显示 transition/theta/edge 有研究信号，但 `acc_main`、`stall_recall` 或 `slope_recall` 仍无法同时过线，不应扩展 multi-seed 或进入部署验证。

保留入口：

- `exp3_patch_full/patch_full_final_report.md`
- `exp3_patch_full/excluded_legacy_full_artifacts.json`
- `exp3_patch_full_rescue/rescue_report.md`
- `exp3_patch_full_densepatch_continuation/continuation_report.md`

## 后续复用原则

1. 复用 `*_tools.py`、schema、baseline snapshot 和技术合同来设计新实验，不复用已失败候选的 checkpoint。
2. 若继续研究这三类结构，必须提出新的结构、损失或数据假设；不要直接扩大已失败配置的 seed 数。
3. 新候选至少先通过 seed21 离线 gate，再进入 multi-seed、ONNX export、MATLAB consistency 和闭环验证。
4. 旧 `ModernTCN_full` 流程和结果仍只作为排除对象，不作为 `exp3_patch_full` 的证据来源。
