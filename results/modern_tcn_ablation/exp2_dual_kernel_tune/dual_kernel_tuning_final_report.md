# exp2 dual_kernel 调参最终报告

## 结论

本轮对 `small_dualkernel` 做了两轮 seed21 离线筛选调参，共 10 个候选。所有候选均固定当前 22 维 `plantfix` baseline 数据链：

- dataset: `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- input_dim: `22`
- seq_len: `128`
- output root: `results/modern_tcn_ablation/exp2_dual_kernel_tune/`

最终决策：`NO_PROMOTION_TUNING / STOP_NO_MULTISEED`。

原因是没有 seed21 候选通过 exp2 离线 gate，因此没有启动 seeds `42,101`，也没有导出 ONNX、没有启动 MATLAB/Simulink、没有写入 compare closed-loop 目录。

## 当前 dual-kernel 的优势

1. `small_kernel=7, dual_branch_scale=0.35` 能保留一部分局部响应收益。最佳候选 `tune_r1_scale035_s7_seed21` 的 `theta_mae_deg=0.665343`，优于 baseline gate 上限 `0.689395`。
2. 同一候选的 `acc_main=0.965852`、`acc_turn=0.579400`、`slope_recall=0.980000`、`false_turn_straight=0.413864` 均在 gate 内，说明 dual branch 不是全局退化。
3. 默认 sweep 中已经观察到局部 transition 提升的个别 seed，说明 dual-kernel 结构确实可能强化转向边界响应。

## 当前 dual-kernel 的短板

最佳调参候选仍失败 5 项：

- `acc_turn_transition=0.494784`，低于 gate `0.497765`。
- `flat_recall=0.955026`，低于 gate `0.959577`。
- `stall_recall=0.645833`，低于 gate `0.668750`。
- `theta_edge_p95_abs_err=3.556906`，高于 gate `2.805057`。
- `flat_peak_theta_error=7.179438`，高于 gate `5.585740`。

主要问题不是训练崩溃，也不是 dataset/路径错误，而是 dual branch 的局部响应会把 flat/stall 判别和 theta 边界/峰值误差推坏。闭环风险对应为：transition 离线收益不足以抵消边界 theta spike 与控制抖动风险。

## 调参范围

Round1 从默认 `k31/s7` 接近区域出发，尝试：

- 降低 dual branch scale: `0.35`, `0.25`
- 加 stall/main selection
- 加 edge/flat peak selection
- 加 mild false-turn guard
- 回看 `small_kernel=5` 平衡配置

Round2 只围绕最佳区域做局部搜索：

- `scale=0.30`
- `small_branch_init=zero`
- 温和 main/stall selection
- 温和 edge/flat peak selection

所有训练均启用 `--no-overwrite`，输出目录独立，不覆盖 baseline、exp1、ONNX、MATLAB generated layers 或 closed-loop 结果。

## 关键结果

完整结果见：

- `results/modern_tcn_ablation/exp2_dual_kernel_tune/tuning_all_summary.csv`
- `results/modern_tcn_ablation/exp2_dual_kernel_tune/tuning_all_summary.md`

排名前 3 的结果完全相同，均对应 `scale=0.35/small_kernel=7` 的同一最佳 epoch：

| rank | run_tag | main | turnT | theta | flat | stall | edge_p95 | false_turn | flat_peak |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `tune_r1_scale035_s7_seed21` | 0.965852 | 0.494784 | 0.665343 | 0.955026 | 0.645833 | 3.556906 | 0.413864 | 7.179438 |
| 2 | `tune_r1_theta_s7_seed21` | 0.965852 | 0.494784 | 0.665343 | 0.955026 | 0.645833 | 3.556906 | 0.413864 | 7.179438 |
| 3 | `tune_r2_edgeflat035_s7_seed21` | 0.965852 | 0.494784 | 0.665343 | 0.955026 | 0.645833 | 3.556906 | 0.413864 | 7.179438 |

这说明 edge/flat-peak selection 只是选回同一个 checkpoint，不能解决边界退化。

## 归因边界

1. `scale=0.30` 恢复了 flat recall，但 theta 明显恶化到 `1.087994`，说明单纯降低 branch scale 会损失有效表达。
2. `small_branch_init=zero` 提高了 main/flat，但 theta、transition、false-turn 都未达 gate，说明 early small-branch perturbation 不是唯一原因。
3. main/stall selection 没有把 stall 推过 gate，并且压低 transition/theta，说明当前 loss/selection 里缺少直接且稳定的 stall 约束。
4. edge/flat-peak selection 不改变 loss，只改变 checkpoint selection；它无法修复 boundary spike，说明问题更可能在训练目标或结构输出分布，而不是单纯 epoch 选择。

## 后续建议

不建议继续在当前 dual-kernel recipe 上扩大 seed 或导出闭环。若继续研究 dual-kernel，应先做结构或损失层面的新节点，而不是继续小范围调参：

1. 给 small branch 加 learnable gate 或 per-block scale，并初始化为接近 0，再让训练学习打开程度。
2. 增加直接面向 `theta_edge_p95_abs_err` / `flat_peak_theta_error` 的训练损失，而不是只在 selection score 里惩罚。
3. 为 stall 类建立明确的 main-head loss 权重或采样策略，并单独验证 flat/stall 与 transition 的 trade-off。
4. 在新结构通过 seed21 离线 gate 前，不进入 multi-seed、ONNX、MATLAB 或 closed-loop。
