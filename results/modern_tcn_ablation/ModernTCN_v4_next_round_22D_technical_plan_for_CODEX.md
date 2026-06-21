# ModernTCN_v4 下一轮 22D 技术实验执行计划（交给 Codex 执行版）

**文件目的**：本文件用于指导 Codex 在 `Cr20253V/ModernTCN_v4` 仓库中继续开展下一轮 ModernTCN 改进实验。  
**核心前提**：所有新实验继续固定使用 **22 维输入**，不得回退到 19 维历史链路。  
**核心结论背景**：上一轮 `results/modern_tcn_ablation/` 下的三个官方特性补回实验均未通过离线 gate，因此均未进入 ONNX、MATLAB 或闭环测试。下一轮不应简单扩大失败配置的 seed 数，而应提出新的数据窗口、结构和诊断假设。
**执行定位**：本文是下一轮实验的总体技术合同，不是逐命令执行脚本。具体训练脚本、节点命令、超参数微调和失败恢复策略，应在后续每个阶段的节点级执行计划中再单独生成和评审。

---

## 0. 当前可信事实与执行边界

### 0.1 当前可信 baseline

当前可信 baseline 固定为：

```text
plant_revision: agv_physics_v2_plantfix
feature_contract: passive17_plus_all5
input_dim: 22
seq_len: 128
retained champion: turn_l020_tt25_tcm14_stw055_slrw060_seed101
```

当前 baseline 快照中记录的 22 维特征顺序为：

```text
1. gyro_z
2. I_lf
3. I_rr
4. omega_wheel_lf
5. omega_wheel_rr
6. delta_lf
7. delta_rr
8. v_hat
9. dv_hat_dt
10. ws_imbalance
11. I_sum
12. I_diff_signed
13. I_diff_abs
14. kappa_proxy
15. accel_per_current
16. dv_hat_dt_lp
17. accel_x_wheel
18. I_drive_signed
19. current_per_accel
20. drive_load_proxy
21. a_hp
22. yaw_consistency_error
```

当前 baseline 离线核心指标为：

```text
acc_main: 0.9669627984453082
acc_turn: 0.5788450860632982
acc_turn_transition: 0.4977645305514158
theta_mae_deg: 0.6793947815895081
flat_recall: 0.9695767195767195
stall_recall: 0.71875
slope_recall: 0.974909090909091
```

### 0.2 上一轮三个实验结论

上一轮 `results/modern_tcn_ablation/` 的结论是：

```text
exp1_grouped_ffn:
    NO_PROMOTION
    离线 gate 未通过
    未进入 ONNX / MATLAB / closed-loop
    局部现象：transition 或 theta 指标有改善，但 acc_main、acc_turn 或 stall_recall 下降。

exp2_dual_kernel:
    NO_PROMOTION / STOP_NO_MULTISEED
    默认 sweep 和 targeted tuning 均未通过组合 gate
    未进入 ONNX / MATLAB / closed-loop
    局部现象：small-kernel 分支可能提升局部响应，但引入 flat/stall 与 theta boundary 风险。

exp3_patch_full:
    NO_PROMOTION
    formal full128、rescue、densepatch continuation 均未通过完整离线 gate
    未进入 ONNX / MATLAB / closed-loop
    局部现象：densepatch/full 对 theta、transition、edge 有研究信号，但 acc_main、stall_recall 或 slope_recall 不能同时过线。
```

### 0.3 下一轮总原则

Codex 必须遵守以下原则：

```text
1. 不覆盖当前 baseline 模型、数据、ONNX、MATLAB generated layers、Simulink 闭环结果。
2. 不复用上一轮失败候选 checkpoint 作为新结果证据。
3. 不再简单扩大 exp1/exp2/exp3 已失败配置的 seed 数。
4. 所有新实验继续固定 input_dim=22。
5. 新数据集如果修改 seq_len，必须另存为新文件，禁止覆盖 seq_len=128 数据集。
6. seq256 相关实验必须继续沿用当前 v5 plantfix / passive17_plus_all5 数据链语义，不得使用会让人误解为旧 v2 链路的命名。
7. 当前代码若仍存在 seq_len=128 的硬检查，必须先作为 Phase 2 前置能力适配解决；适配只允许放宽到明确白名单，如 128/256，不得放松 input_dim、feature_contract、horizon_steps 等核心契约。
8. 所有新模型必须使用新的 run_tag 和输出目录；只有真正新增结构族时才新增 model_family。
9. 新候选必须先通过离线 gate，再进入 ONNX / MATLAB / closed-loop。
10. 如果离线提升但闭环退化，只能作为研究结果，不能替代当前 baseline。
11. 多 seed 扩展不是默认起点。除非节点计划另有充分理由，本轮训练实验应先做 seed21 screening，只有接近或通过 gate 的配置才扩展 seeds 42/101。
```

---

## 1. 下一轮实验总目标

本轮不再直接问：

```text
官方 ModernTCN 特性在 22D seq128 下能否直接超过 baseline？
```

因为上一轮已经证明答案是否定的。

本轮改问：

```text
1. 在 22D 输入不变的条件下，seq_len 从 128 增加到 256 后，patch/full 是否能真正发挥长期上下文优势？
2. seq256 条件下，small baseline 自身是否也会提升？
3. densepatch/full 是否能超过同窗口 seq256 small baseline，而不只是超过旧 seq128 baseline？
4. 上一轮反复失败的 acc_main / stall_recall / slope_recall 是否来自结构问题、标签边界问题、样本分布问题，还是 loss 多任务冲突？
5. grouped FFN 和 dual-kernel 是否需要改成 hybrid / gated 增量分支，而不是替换当前 small 主干？
```

---

## 2. 新输出目录规范

新增下一轮根目录：

```text
results/modern_tcn_next_round_22d/
```

建议目录结构：

```text
results/modern_tcn_next_round_22d/
    00_evidence_lock/
    01_error_diagnosis/
    02_seq256_dataset/
    03_seq256_small_baseline/
    04_seq256_patch_full/
    05_optional_hybrid_gffn/
    06_optional_gated_dualkernel/
    07_sandbox_closed_loop/
    08_final_report/
```

所有新 run 目录原则上应包含下列证据。若现有训练脚本已有等价命名，不要求为了形式统一而改动成熟脚本；节点级计划只需记录实际文件名和路径映射。

```text
config.json
git_hash.txt
dataset_contract.json 或 dataset_contract_snapshot.json
train.log
history.csv
test_metrics.csv
confusion_matrices/
best_checkpoint.pt
decision.json
run_summary.md
```

必须实现 `--no_overwrite` 保护：

```text
如果输出目录已存在，训练脚本必须直接报错并停止，不得覆盖。
```

---

## 3. Phase 0：证据锁定与仓库状态检查

### 节点 0.1：锁定上一轮证据

Codex 需要生成：

```text
results/modern_tcn_next_round_22d/00_evidence_lock/evidence_lock.md
```

内容包括：

```text
1. 当前 git commit hash
2. 当前 baseline snapshot 路径
3. 当前 baseline checkpoint 路径
4. 当前 baseline ONNX 路径
5. 当前 baseline offline metrics
6. 上一轮 exp1/exp2/exp3 final report 路径
7. 上一轮三个实验为什么不继续原样扩 seed
8. 本轮所有实验固定 input_dim=22 的声明
```

### 节点 0.2：检查 baseline 文件存在性

Codex 需要检查以下文件是否存在：

```text
results/modern_tcn_ablation/_baseline_snapshot/baseline_identity.md
results/modern_tcn_ablation/_baseline_snapshot/baseline_offline_metrics.csv
results/modern_tcn_ablation/ABLATION_CLEANUP_SUMMARY.md
results/modern_tcn_ablation/exp1_grouped_ffn/grouped_ffn_final_report.md
results/modern_tcn_ablation/exp2_dual_kernel/dual_kernel_final_report.md
results/modern_tcn_ablation/exp3_patch_full_densepatch_continuation/continuation_report.md
```

输出：

```text
results/modern_tcn_next_round_22d/00_evidence_lock/file_existence_check.csv
```

字段：

```text
path, exists, size_bytes, modified_time
```

### 节点 0.3：确认 22D 数据链仍然可用

检查当前 22D seq128 数据 contract，确认：

```text
input_dim == 22
seq_len == 128
feature_contract == passive17_plus_all5
plant_revision == agv_physics_v2_plantfix
```

输出：

```text
results/modern_tcn_next_round_22d/00_evidence_lock/current_22d_seq128_contract_check.md
```

如发现当前训练脚本默认指向 19D 或历史数据链，必须停止并报告，不得继续训练。

---

## 4. Phase 1：错误诊断，不训练新模型

上一轮三个方向共同暴露出一个模式：

```text
transition / theta / edge 可能改善
但 acc_main / stall_recall / slope_recall 容易下降
```

因此下一轮必须先做诊断，避免盲目继续调模型。

### 节点 1.1：生成 baseline 主类与转向类混淆矩阵

使用当前 baseline checkpoint 和 22D seq128 test set，重新跑一次 offline inference，生成：

```text
results/modern_tcn_next_round_22d/01_error_diagnosis/baseline_seq128_predictions.csv
results/modern_tcn_next_round_22d/01_error_diagnosis/baseline_main_confusion_matrix.csv
results/modern_tcn_next_round_22d/01_error_diagnosis/baseline_turn_confusion_matrix.csv
results/modern_tcn_next_round_22d/01_error_diagnosis/baseline_classification_report.md
```

必须包含：

```text
main: flat / stall / slope
turn: right / straight / left
每类 precision / recall / f1 / support
```

### 节点 1.2：分析 stall 与 slope 的样本分布

生成：

```text
results/modern_tcn_next_round_22d/01_error_diagnosis/stall_slope_sample_distribution.md
results/modern_tcn_next_round_22d/01_error_diagnosis/stall_slope_sample_distribution.csv
```

至少统计：

```text
1. train / val / test 中 flat / stall / slope 样本数
2. stall 样本在不同 run / segment 中的分布
3. slope 样本在不同 run / segment 中的分布
4. stall 持续窗口长度分布
5. slope 持续窗口长度分布
6. transition window 数量
7. turn transition 与 main class 的交叉表
```

### 节点 1.3：分析 theta 误差和 main 错误的关系

生成：

```text
results/modern_tcn_next_round_22d/01_error_diagnosis/theta_error_vs_main_error.csv
results/modern_tcn_next_round_22d/01_error_diagnosis/theta_error_vs_main_error.md
```

至少统计：

```text
1. main 判断正确时的 theta_mae_deg
2. main 判断错误时的 theta_mae_deg
3. flat 被误判为 slope/stall 时的 theta 分布
4. slope 被误判为 flat/stall 时的 theta 分布
5. theta 绝对误差 top 5% 样本对应的 main/turn 类别分布
6. theta_edge_p95_abs_err 与 main 错误是否重叠
```

### 节点 1.4：生成诊断结论

输出：

```text
results/modern_tcn_next_round_22d/01_error_diagnosis/diagnosis_summary.md
```

结论必须回答：

```text
1. stall_recall 是不是主要由样本稀少导致？
2. slope_recall 下降是否集中在坡度边界？
3. theta 改善和 main 分类下降是否存在明显 trade-off？
4. transition 改善是否以 straight/flat 稳定性下降为代价？
5. 下一步 seq256 是否有理论必要？
```

---

## 5. Phase 2：构建 22D seq256 数据链

本轮最重要的新假设：

```text
官方 patch/full 特性在 seq128 下无法充分发挥；
应先把窗口长度从 128 提升到 256，再比较 seq256 small 与 seq256 patch/full。
```

### Phase 2 前置能力边界

在生成或训练 seq256 之前，必须确认当前 Python 数据加载、训练配置和模型 shape 检查允许 `input_dim=22, seq_len=256` 的新数据链。若代码中仍存在“ModernTCN 第一阶段只能 seq_len=128”的硬检查，应先做最小能力适配：

```text
1. 只把允许窗口长度扩展为明确白名单，例如 128 和 256。
2. 不放松 input_dim=22、feature_contract=passive17_plus_all5、horizon_steps=0、label_time_policy=current_window_end。
3. 不改变 seq128 baseline 的默认行为。
4. 适配完成后先 dry-run 验证数据加载和模型 forward，再进入训练节点。
```

### 节点 2.1：生成 22D seq256 数据集

新数据集必须保持 22D 输入不变，只改变窗口长度。

建议文件名：

```text
data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_seq256.mat
data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_seq256_contract.json
```

硬性要求：

```text
input_dim = 22
seq_len = 256
feature_contract = passive17_plus_all5
plant_revision = agv_physics_v2_plantfix
horizon_steps = 0
label_time_policy = current_window_end
scaler_policy = fit_train_only_apply_val_test_online
split_policy = 与 seq128 baseline 保持一致
```

命名要求：

```text
文件名必须体现 v5_plantfix_passive17_plus_all5_seq256，避免误解为旧 v2 数据链。
```

### 节点 2.2：验证 seq256 数据集

生成：

```text
results/modern_tcn_next_round_22d/02_seq256_dataset/seq256_dataset_validation.md
results/modern_tcn_next_round_22d/02_seq256_dataset/seq256_window_counts.csv
results/modern_tcn_next_round_22d/02_seq256_dataset/seq256_feature_contract_snapshot.json
```

必须检查：

```text
1. input_dim 是否为 22
2. seq_len 是否为 256
3. feature_names 是否与 baseline 22D 完全一致
4. train / val / test split 是否没有泄漏
5. scaler 是否只 fit train
6. label 是否取 window end
7. horizon_steps 是否仍为 0
8. train/val/test window count 是否合理
```

如果任何一项失败，停止，不得训练。

---

## 6. Phase 3：训练 seq256 small baseline

在评估 full/densepatch 之前，必须先建立同窗口 baseline。

不能拿 seq256 full 直接和 seq128 small baseline 比较，否则无法判断收益来自：

```text
1. 更长窗口
2. full/densepatch 结构
3. 训练随机性
```

### 节点 3.1：训练 small_seq256_k31

配置：

```text
model_family = small
input_dim = 22
seq_len = 256
channels = 64
blocks = 5
kernel_size = 31
dropout = 0.15
temporal_padding = same
dataset = 22d seq256
seeds = 21, 42, 101
```

执行粒度：

```text
先训练 seed21 作为 screening；只有 seed21 在完整 gate 上接近或通过，才扩展 seed42 和 seed101。
```

输出目录：

```text
results/modern_tcn_next_round_22d/03_seq256_small_baseline/small_seq256_k31_seed21/
results/modern_tcn_next_round_22d/03_seq256_small_baseline/small_seq256_k31_seed42/
results/modern_tcn_next_round_22d/03_seq256_small_baseline/small_seq256_k31_seed101/
```

### 节点 3.2：训练 small_seq256_k51

配置：

```text
model_family = small
input_dim = 22
seq_len = 256
channels = 64
blocks = 5
kernel_size = 51
dropout = 0.15 或 0.20
temporal_padding = same
dataset = 22d seq256
seeds = 21, 42, 101
```

执行粒度：

```text
先训练 seed21 作为 screening；只有 seed21 在完整 gate 上接近或通过，才扩展 seed42 和 seed101。
```

输出目录：

```text
results/modern_tcn_next_round_22d/03_seq256_small_baseline/small_seq256_k51_seed21/
...
```

### 节点 3.3：汇总 seq256 small baseline

生成：

```text
results/modern_tcn_next_round_22d/03_seq256_small_baseline/seq256_small_offline_summary.csv
results/modern_tcn_next_round_22d/03_seq256_small_baseline/seq256_small_offline_summary.md
results/modern_tcn_next_round_22d/03_seq256_small_baseline/seq256_small_best_selection.md
```

必须比较：

```text
seq128 champion baseline
small_seq256_k31 mean/std
small_seq256_k51 mean/std
```

重点指标：

```text
acc_main
acc_turn
acc_turn_transition
theta_mae_deg
flat_recall
stall_recall
slope_recall
theta_edge_p95_abs_err
flat_peak_theta_error
false_turn_straight
```

### 节点 3.4：seq256 small 晋级判断

如果 seq256 small 明显劣于 seq128 baseline，说明更长窗口本身可能不适配当前任务。此时仍可继续做少量 full256 seed21 诊断，但不应直接扩展 full256 多 seed。

如果 seq256 small 优于或接近 seq128 baseline，则将最佳 seq256 small 作为本轮新 baseline。

记录：

```text
results/modern_tcn_next_round_22d/03_seq256_small_baseline/seq256_reference_baseline_decision.json
```

字段：

```text
selected_reference: small_seq256_k31 或 small_seq256_k51 或 keep_seq128_baseline
reason
selected_run_tag
selected_metrics
```

---

## 7. Phase 4：训练 seq256 densepatch/full

这是本轮最重要的模型实验。

本阶段默认先做三个 full256 配置的 seed21 screening。只有某个配置在完整 gate 上接近或通过，才扩展 seed42 和 seed101；若 seed21 已明显失败，不应直接全量多 seed。

### 节点 4.1：full256_dense_A

配置：

```text
model_family = full
input_dim = 22
seq_len = 256
patch_size = 16
patch_stride = 4
expected_tokens ≈ 61
dims = (16, 32)
stage_blocks = (1, 1)
large_kernels = (15, 9)
small_kernels = (5, 3)
dropout = 0.15 或 0.20
dataset = 22d seq256
seeds = 21, 42, 101
```

输出：

```text
results/modern_tcn_next_round_22d/04_seq256_patch_full/full256_dense_A_seed21/
...
```

### 节点 4.2：full256_dense_B

配置：

```text
model_family = full
input_dim = 22
seq_len = 256
patch_size = 8
patch_stride = 2
expected_tokens ≈ 125
dims = (16, 32)
stage_blocks = (1, 1)
large_kernels = (15, 9)
small_kernels = (5, 3)
dropout = 0.15 或 0.20
dataset = 22d seq256
seeds = 21, 42, 101
```

目的：

```text
减少 patch 降采样造成的时间分辨率损失。
```

### 节点 4.3：full256_wide

配置：

```text
model_family = full
input_dim = 22
seq_len = 256
patch_size = 16
patch_stride = 4
expected_tokens ≈ 61
dims = (24, 48)
stage_blocks = (1, 1)
large_kernels = (15, 9)
small_kernels = (5, 3)
dropout = 0.20
dataset = 22d seq256
seeds = 21, 42, 101
```

目的：

```text
对应上一轮 densepatch_wide24 在 theta/transition/edge/stall 上的局部信号，
观察 seq256 是否能补回 acc_main 和 slope_recall。
```

### 节点 4.4：full256 离线汇总

生成：

```text
results/modern_tcn_next_round_22d/04_seq256_patch_full/full256_offline_summary.csv
results/modern_tcn_next_round_22d/04_seq256_patch_full/full256_offline_summary.md
results/modern_tcn_next_round_22d/04_seq256_patch_full/full256_best_selection.md
```

必须同时比较：

```text
seq128 champion baseline
seq256 small reference baseline
full256_dense_A
full256_dense_B
full256_wide
```

### 节点 4.5：full256 gate

候选 full256 进入 ONNX/闭环前，必须满足相对于 **seq256 small reference baseline** 的 gate。

如果 seq256 small 不成立，则使用 seq128 champion baseline 作为 fallback gate，但报告必须注明。

建议 gate：

```text
acc_main >= reference_acc_main - 0.003
acc_turn >= reference_acc_turn - 0.005
acc_turn_transition >= reference_acc_turn_transition
theta_mae_deg <= reference_theta_mae_deg + 0.01
flat_recall >= reference_flat_recall - 0.010
stall_recall >= reference_stall_recall - 0.050
slope_recall >= reference_slope_recall - 0.005
theta_edge_p95_abs_err <= reference_theta_edge_p95_abs_err
```

如果 full256 在 theta/transition 明显优于 reference，但 acc_main 或 slope_recall 未过线，不能直接晋级。可以进入 Phase 7 sandbox，但不得进入正式 closed-loop compare。

---

## 8. Phase 5：可选 hybrid grouped FFN

只有在 Phase 1 诊断确认 main/stall/slope 下滑不是单纯数据问题，且 Phase 4 full256 未通过时，才执行本阶段。

上一轮 exp1 的问题是：直接把 pointwise mixing 替换成 grouped FFN 后，transition/theta 有改善，但 acc_main、acc_turn 或 stall_recall 下降。因此本轮不再做替换式 grouped FFN，而是做增量式 hybrid。

本阶段不是复用上一轮 `small_gffn` 继续调参，而是一个新的结构假设。当前代码如果尚未支持 `small_hybrid_gffn`，必须先在节点级计划中单独设计模型 family、CLI 参数、checkpoint metadata、summary 字段和回归测试；未完成这些能力建设前不得直接训练。

### 节点 5.1：新增 hybrid_gffn 模型

新增：

```text
model_family = small_hybrid_gffn
```

结构思想：

```text
baseline_branch = 当前 ModernTCN-small 原始 block 输出
grouped_branch = grouped FFN 辅助分支
alpha = learnable scalar 或 per-block scalar，初始化为 0.0 或 0.1

output = baseline_branch + alpha * grouped_branch
```

硬性要求：

```text
1. 不改变 model_family=small 的默认行为。
2. alpha 初始化必须很小，避免 grouped 分支一开始破坏 baseline 表征。
3. checkpoint 中保存 alpha 参数。
4. 训练日志中记录每个 block 的 alpha 最终值。
```

### 节点 5.2：训练 hybrid_gffn

建议先在 seq128 上验证，再考虑 seq256。

配置：

```text
small_hybrid_gffn_seq128_d4_k51_alpha0
small_hybrid_gffn_seq128_d4_k51_alpha01
small_hybrid_gffn_seq256_d4_k63_alpha0
```

每个配置先跑：

```text
seed = 21
```

只有 seed21 接近 gate，才扩展：

```text
seeds = 42, 101
```

### 节点 5.3：hybrid_gffn 判断

重点看：

```text
1. 是否保留 baseline acc_main / stall_recall
2. 是否保留 grouped FFN 的 transition/theta 收益
3. alpha 是否真的学到非零
4. alpha 过大时是否导致分类退化
```

如果 alpha 最终接近 0，说明 grouped 分支无用。  
如果 alpha 变大但分类退化，说明 grouped 分支仍然冲突。

---

## 9. Phase 6：可选 gated dual-kernel

上一轮 exp2 的问题是：small-kernel 分支容易引入 theta boundary 和 flat/stall 风险。因此本轮不再做简单相加式 dual-kernel，而是做 gated / head-specific dual-kernel。

本阶段不是复用上一轮 `small_dualkernel` 继续调参，而是一个新的结构假设。当前代码如果尚未支持 `small_gated_dualkernel`，必须先在节点级计划中单独设计模型 family、CLI 参数、checkpoint metadata、summary 字段和回归测试；未完成这些能力建设前不得直接训练。

### 节点 6.1：新增 gated_dualkernel 模型

新增：

```text
model_family = small_gated_dualkernel
```

结构思想：

```text
large_branch = depthwise large kernel 主分支
small_branch = depthwise small kernel 辅助分支
gate = learnable scalar 或 per-block scalar，初始化为 0.0 或 0.05

temporal_feature = large_branch + sigmoid(gate) * small_branch
```

进一步建议：

```text
theta_head 只读取 large-dominant features
turn_head 可以读取 large + gated small features
main_head 默认读取 large-dominant features
```

如果当前代码结构实现 head-specific feature routing 过于复杂，可先实现 scalar-gated dual-kernel，不做 head-specific routing。

### 节点 6.2：训练 gated_dualkernel

建议配置：

```text
gated_dual_seq128_k31_s7_gate0
gated_dual_seq128_k31_s5_gate0
gated_dual_seq256_k51_s7_gate0
```

每个先跑：

```text
seed = 21
```

只有 seed21 的 theta boundary、flat_peak、stall_recall 同时接近 gate，才扩展 seed。

### 节点 6.3：gated_dualkernel 判断

重点看：

```text
theta_edge_p95_abs_err
flat_peak_theta_error
stall_recall
acc_turn_transition
omega-risk proxy，如 false_turn_straight
```

如果小核 gate 最终接近 0，说明 small branch 不适合当前任务。  
如果 gate 非零但 boundary 指标变差，停止该方向。

---

## 10. Phase 7：sandbox closed-loop，不作为正式晋级

正式规则是：未通过离线 gate 的模型不得进入正式闭环 compare。  
但为了验证“theta/transition 局部改善是否可能带来闭环局部收益”，允许做 sandbox closed-loop。

sandbox closed-loop 仍必须遵守路径隔离：使用显式 `modern_tcn_sim_cfg.onnx_file / dataset_file` 注入候选模型和数据，不依赖 MATLAB 全局默认路径；运行前必须预检输出路径长度和目标目录，避免写入正式 compare 目录。

### 节点 7.1：sandbox 候选

只允许选择最多 2 个模型：

```text
1. full256 最佳候选，如果 theta/transition/edge 明显优于 reference，但 acc_main 或 slope_recall 略差。
2. hybrid_gffn 最佳候选，如果 transition/theta 有收益且分类退化有限。
```

不建议 exp2 原始 dual-kernel 进入 sandbox，因为上一轮 boundary 风险太明显。

### 节点 7.2：sandbox 目录

输出目录必须是：

```text
results/modern_tcn_next_round_22d/07_sandbox_closed_loop/
```

不得写入：

```text
results/compare/tcn_gru_modern_closed_loop/
results/compare/modern_tcn_ablation_closed_loop/
```

### 节点 7.3：sandbox 报告

输出：

```text
results/modern_tcn_next_round_22d/07_sandbox_closed_loop/sandbox_closed_loop_report.md
```

报告必须写明：

```text
这是诊断性闭环，不是 promotion。
不替代当前 baseline。
不用于正式论文主对比，除非后续补齐 gate 和 multi-path 验证。
```

---

## 11. Phase 8：是否考虑 seq512

当前不建议直接执行 seq512。  
只有满足以下条件时，才允许开 seq512：

```text
1. seq256 small 不明显劣于 seq128 baseline；
2. 至少一个 full256 / densepatch 在离线 gate 上接近或通过；
3. Phase 1 诊断显示 slope 或 theta 错误确实需要更长历史；
4. 训练和推理资源允许；
5. 预期 online buffer 增加不会破坏闭环实时性。
```

如果执行 seq512，建议先做最小配置：

```text
input_dim = 22
seq_len = 512
patch_size = 32
patch_stride = 8
expected_tokens ≈ 61
dims = (16, 32)
stage_blocks = (1, 1)
large_kernels = (15, 9)
small_kernels = (5, 3)
```

必须同时训练：

```text
small_seq512_k51
full512_patch32_stride8
```

不能只训练 full512。

---

## 12. 统一晋级规则

### 12.1 离线晋级

候选模型必须相对于当前 reference baseline 满足：

```text
acc_main >= reference_acc_main - 0.003
acc_turn >= reference_acc_turn - 0.005
acc_turn_transition >= reference_acc_turn_transition
theta_mae_deg <= reference_theta_mae_deg + 0.01
flat_recall >= reference_flat_recall - 0.010
stall_recall >= reference_stall_recall - 0.050
slope_recall >= reference_slope_recall - 0.005
theta_edge_p95_abs_err <= reference_theta_edge_p95_abs_err
```

如果候选模型只是 theta 明显好，但 acc_main 或 slope_recall 明显差，则不得晋级。

### 12.2 ONNX/MATLAB 晋级

离线通过后，必须执行：

```text
1. PyTorch vs ONNXRuntime consistency
2. PyTorch vs MATLAB ONNX consistency
3. generated layers namespace audit
4. latency test
```

新 namespace 规则：

```text
seq256 small:
    +modern_tcn_seq256_onnx_layers

full256:
    +modern_tcn_full256_onnx_layers

hybrid_gffn:
    +modern_tcn_hybrid_gffn_onnx_layers

gated_dualkernel:
    +modern_tcn_gated_dualkernel_onnx_layers
```

禁止覆盖当前默认：

```text
+modern_tcn_onnx_layers
```

说明：

```text
上述 namespace 是部署阶段的目标规则。具体执行时必须先检查导出 sidecar metadata、MATLAB loader 的 model_family 识别逻辑和 generated layers 目录是否已经支持这些命名；未完成前不得进入 MATLAB consistency 或 closed-loop。
```

### 12.3 闭环晋级

正式闭环候选必须满足：

```text
1. 主路径闭环不失稳
2. xy_rmse <= reference
3. ey_rmse <= reference
4. constraint_touch_count 不增加
5. omega_cmd_rms 或 delta_u_rms 不高于 reference 5%
6. main/turn 在线准确率不显著低于 reference
7. theta_sched_mae_deg 不高于 reference
```

只有主路径通过，才允许 multipath 和 robustness。

---

## 13. 最终报告要求

所有阶段完成后，生成：

```text
results/modern_tcn_next_round_22d/08_final_report/next_round_22d_final_report.md
results/modern_tcn_next_round_22d/08_final_report/next_round_22d_decision.json
results/modern_tcn_next_round_22d/08_final_report/next_round_22d_master_summary.csv
```

最终报告必须回答：

```text
1. seq256 small 是否优于 seq128 small？
2. full256 / densepatch 是否优于同窗口 seq256 small？
3. full256 是否解决了 seq128 full 的 acc_main / slope_recall 问题？
4. main/stall/slope 失败是否来自样本分布、标签边界、结构冲突还是 loss 冲突？
5. hybrid_gffn 是否比替换式 grouped_ffn 更好？
6. gated_dualkernel 是否避免了原 dual-kernel 的 boundary 风险？
7. 是否有候选模型可以进入正式 ONNX / MATLAB / closed-loop？
8. 是否建议替换当前 baseline？
9. 如果不替换，哪些结果可写入论文负结果或消融分析？
```

---

## 14. 推荐执行顺序

Codex 应按以下顺序执行，不得跳步：

```text
Phase 0: 证据锁定与仓库状态检查
Phase 1: baseline 错误诊断
Phase 2: 生成 22D seq256 数据链
Phase 3: 训练 seq256 small baseline
Phase 4: 训练 seq256 densepatch/full
Phase 5: 只有必要时执行 hybrid grouped FFN
Phase 6: 只有必要时执行 gated dual-kernel
Phase 7: 只有诊断需要时执行 sandbox closed-loop
Phase 8: 总报告
```

最重要的第一轮执行子集是：

```text
1. Phase 0
2. Phase 1
3. Phase 2
4. Phase 3 small_seq256_k31/k51
5. Phase 4 full256_dense_A/full256_dense_B/full256_wide
```

如果这些没有产生接近 gate 的结果，不要继续 Phase 5/6/7。

---

## 15. Codex 执行时的硬性停止条件

遇到以下情况必须停止并生成 failure report：

```text
1. 当前数据链不是 22D。
2. seq256 数据集 feature_names 与 baseline 22D 不完全一致。
3. train/val/test split 出现泄漏。
4. scaler 不是 fit_train_only_apply_val_test_online。
5. label_time_policy 不是 current_window_end。
6. 任一新实验输出目录已存在但脚本试图覆盖。
7. 新模型改变了 model_family=small 的默认行为。
8. ONNX generated layers 覆盖了默认 namespace。
9. 未通过离线 gate 却写入正式 closed-loop compare 目录。
```

failure report 路径：

```text
results/modern_tcn_next_round_22d/<phase>/failure_report.md
```

---

## 16. 简短任务摘要

本轮任务不是继续证明上一轮三个失败实验，而是建立新的更合理假设：

```text
在 22D 输入固定条件下，官方 ModernTCN 的 patch/full 特性可能需要更长历史窗口才能发挥作用。
因此应先构建 seq256 数据链，训练同窗口 small baseline，再验证 full256 densepatch 是否能超过同窗口 baseline。
同时通过诊断明确 acc_main / stall_recall / slope_recall 反复下降的原因。
只有当新的候选同时通过离线 gate 和部署一致性检查，才允许进入正式闭环。
```
