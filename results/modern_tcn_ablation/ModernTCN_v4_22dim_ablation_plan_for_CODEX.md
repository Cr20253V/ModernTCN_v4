# ModernTCN_v4：22 维输入条件下的官方特性补回消融实验计划

> 目标读者：Codex / Code X 执行代理
> 项目仓库：`https://github.com/Cr20253V/ModernTCN_v4`
> 核心前提：**本轮所有实验固定在当前 22 维输入条件下进行**。不要回退到 19 维历史配置，不要使用 30 维输入，不要修改当前已验证的 baseline 结果。
> 核心目标：在不破坏当前 ModernTCN-small 主线结果、数据集、训练脚本和部署链路的前提下，逐步补回官方 ModernTCN 的关键特点，并验证这些补回是否能提升离线准确度与 AGV 闭环路径跟踪效果。

---

## 0. 总体原则

### 0.0 本文件定位

本文档是三类 ModernTCN 官方特性补回实验的**总体技术合同**，用于约束后续多个新窗口制定详细节点计划。本文档不要求一次性生成所有训练脚本、闭环脚本和汇总脚本。

后续执行时，每个实验方向都必须单独生成更细的节点计划，至少包括：

```text
具体代码改动清单
训练脚本参数和默认值修正
输出目录与 no_overwrite 检查
baseline 快照与指标读取脚本
离线汇总脚本
ONNX 导出与一致性检查脚本
MATLAB/Simulink 闭环 preflight
闭环运行与结果汇总脚本
最终 promote / no-promote 决策报告
```

也就是说，本文档只定义实验边界、结构假设、验收标准和不可破坏的共用规则；具体执行步骤以每个实验后续生成的节点级计划为准。

### 0.1 固定输入维度

本轮实验全部固定为：

```text
input_dim = 22
seq_len = 128 作为第一阶段默认窗口长度
```

除非执行本文档后部明确标注为“长窗口扩展建议”的实验，否则不得修改主线数据维度与默认窗口长度。

本轮不做以下内容：

```text
不做 19 维输入实验
不做 30 维输入实验
不覆盖当前 22 维 baseline 结果
不覆盖当前默认 ModernTCN-small 训练结果
不覆盖当前默认 ONNX 文件
不覆盖当前 MATLAB/Simulink 默认部署配置
```

### 0.2 保护当前 baseline

当前项目中已有的 ModernTCN-small 结果是本轮消融实验的基线。所有新实验必须新建模型名、新建配置名、新建输出目录、新建 MATLAB generated layers namespace。

禁止覆盖以下内容：

```text
src/ModernTCN/modern_tcn_model.py 中原 ModernTCNSmall 的默认行为
src/ModernTCN/ModernTCN_default_config.m
当前 baseline checkpoint
当前 baseline ONNX
当前 baseline MATLAB generated layers
当前 baseline closed-loop 结果目录
当前 compare 目录中的已有对比结果
```

允许新增文件、类、配置、脚本参数和新目录，但不得改变当前 baseline 的复现实验路径。

如果现有脚本或 MATLAB 默认配置仍指向旧的 22 维历史 baseline，允许在后续具体执行节点中把相关默认值修正为**当前已验证的 22 维 plantfix 最优配置**。这类修正必须满足：

```text
只修正默认指向，不删除旧结果
不覆盖当前最优 checkpoint / ONNX / closed-loop 结果
在 baseline snapshot 中记录修正前后的路径
在节点报告中说明为什么旧默认值不再代表当前 baseline
```

当前默认 baseline 身份应以当次执行前重新读取的 handoff、manifest、dataset contract 和 closed-loop 汇总为准，不得仅凭旧脚本默认路径判断。

### 0.3 每个实验只验证一个核心改动

本计划包含三个主实验方向：

```text
实验 1：补回 grouped pointwise ConvFFN
实验 2：补回 large-kernel + small-kernel 双分支
实验 3：补回 patch embedding / ModernTCNFull 结构
```

不要一开始把三个方向混合到一个模型中。每个方向先独立证明是否有效。只有在单独实验有效后，才允许设计组合实验。

### 0.4 离线提升不等于闭环提升

本项目最终服务于 AGV 路径跟踪与 LPV-MPC 闭环控制。因此模型有效性必须分两级判断：

```text
第一级：离线训练/测试指标是否优于 baseline
第二级：闭环路径跟踪指标是否优于 baseline
```

如果某模型离线指标提升，但闭环路径跟踪退化，则该模型只能作为消融结果，不得替代当前默认 ModernTCN-small。

### 0.5 当前最优训练参数的使用方式

当前最优 ModernTCN-small 的训练参数可以作为后续实验的起始参考，但不能被视为所有新结构的固定最优解。每个新结构允许围绕当前最优训练 recipe 做小范围调整。

要求如下：

```text
第一轮优先复用当前最优模型的关键训练 recipe，保证可比性
如果新结构明显欠拟合、过拟合或 turn/theta 指标失衡，可以做小范围参数调整
所有参数调整必须写入 run 目录 config 和实验 summary
结构收益结论必须区分“结构改动收益”和“训练 recipe 改动收益”
不要把大量 loss/selector 超参搜索和结构消融混在同一个结论里
```

### 0.6 三个实验的共用工程要求

三个实验方向都应复用同一套工程支撑能力，避免每个实验临时写一套互不兼容的脚本。

后续具体节点计划中，应优先补齐以下共用能力：

```text
统一训练 CLI：支持 model_family、output_root、run_tag、no_overwrite
统一配置保存：每个 run 保存完整 config、dataset contract copy、feature_names、git hash
统一 baseline reader：只读取现有 baseline，不触发 baseline 重训
统一 metrics schema：离线和闭环指标列名在三个实验中保持一致
统一 summary writer：输出 per-seed、mean/std、best_run、晋级理由
统一 ONNX export wrapper：记录 input_shape、model_family、sample_file、opset
统一 ONNXRuntime / MATLAB 一致性检查
统一 MATLAB generated layers namespace 规则
统一 closed-loop preflight：确认实际加载的 ONNX、dataset、scaler、deployment 参数
统一 promote / no-promote 报告模板
```

如果某项共用能力尚不存在，不要求在本文档阶段实现；必须在对应实验的节点计划中作为前置工程节点补齐。

### 0.7 实验三的重新执行原则

当前项目中可能已经存在 ModernTCNFull 或 patch/full 相关实现和历史实验结果。后续实验三仍按本文档重新执行，不直接继承旧结论。

允许复用：

```text
已经存在且通过基本检查的模型类
数据读取、训练循环、metrics、ONNX 导出等通用代码
历史实验暴露出的工程问题和验证脚本
```

不得复用为最终结论：

```text
旧 full/patch 实验的离线最优判断
旧 full/patch 实验的闭环结论
旧 full/patch 实验的参数设置
旧实验中未经本轮 baseline snapshot 对齐的指标
```

实验三必须在当前 22 维 plantfix baseline、当前数据契约、当前闭环评价 shell 下重新生成证据。

### 0.8 后续详细计划的节点边界

后续每个实验方向应按节点执行。一个节点只完成一个明确目标，并在节点结束时给出通过/未通过证据。

建议每个实验方向至少拆成：

```text
节点 A：baseline 与代码可执行性 preflight
节点 B：模型族和 CLI 支持
节点 C：单 seed smoke / dry-run / no_overwrite 验证
节点 D：正式多 seed 离线训练
节点 E：离线汇总和晋级判定
节点 F：ONNX 导出和一致性检查
节点 G：主路径闭环
节点 H：multipath / robustness，条件执行
节点 I：最终实验报告
```

不得在一个节点中同时完成模型结构实现、多 seed 训练、ONNX 导出和闭环推广。

---

## 1. 基线快照任务

在做任何模型改动前，先建立不可变基线快照。

### 节点 1.1：确认当前 22 维 baseline 身份

请检查以下位置，确认当前主线确实是 22 维输入：

```text
Python 训练脚本默认配置
ModernTCNConfig 默认 input_dim
当前 dataset contract
当前 baseline 训练日志
当前 checkpoint config
当前 ONNX input shape
当前 MATLAB 默认配置
当前 handoff / manifest 中记录的最优 22 维 plantfix baseline
```

确认后生成：

```text
results/modern_tcn_ablation/_baseline_snapshot/baseline_identity.md
```

该文件必须包含：

```text
git commit hash
repository path
dataset path
dataset contract path
input_dim = 22
seq_len = 128
feature_names，必须列出 22 个输入特征名
train/val/test window count
baseline checkpoint path
baseline ONNX path
baseline MATLAB config path
baseline generated layers namespace
baseline closed-loop result directory
baseline training recipe，包括 loss weights、selector weights、deployment smoothing/dwell 参数
如果脚本默认值被修正，记录修正前路径和修正后路径
```

验收标准：

```text
baseline_identity.md 存在
其中明确写入 input_dim = 22
其中没有把 19 维历史配置作为本轮实验输入
其中没有把 30 维配置作为本轮实验输入
```

### 节点 1.2：复制 baseline 指标

不要重新训练 baseline。请读取现有结果，生成以下文件：

```text
results/modern_tcn_ablation/_baseline_snapshot/baseline_offline_metrics.csv
results/modern_tcn_ablation/_baseline_snapshot/baseline_closed_loop_metrics.csv
results/modern_tcn_ablation/_baseline_snapshot/baseline_summary.md
```

离线指标至少包括：

```text
acc_main
acc_turn
acc_turn_transition
theta_mae_deg
theta_p95_abs_err_deg
flat_recall
stall_recall
slope_recall
right_recall
straight_recall
left_recall
```

闭环指标至少包括：

```text
ey_rmse
epsi_rmse
xy_rmse
theta_mae_deg
theta_sched_mae_deg
main_acc_pct
turn_acc_pct
omega_cmd_rms
delta_u_rms
constraint_touch_count
overall_rank
```

验收标准：

```text
baseline_offline_metrics.csv 存在
baseline_closed_loop_metrics.csv 存在
baseline_summary.md 存在
所有 baseline 文件只读引用已有结果，不触发 baseline 重训
```

---

## 2. 统一实验目录规范

新增统一消融实验根目录：

```text
results/modern_tcn_ablation/
```

三个实验方向分别使用：

```text
results/modern_tcn_ablation/exp1_grouped_ffn/
results/modern_tcn_ablation/exp2_dual_kernel/
results/modern_tcn_ablation/exp3_patch_full/
```

闭环测试结果统一放在：

```text
results/compare/modern_tcn_ablation_closed_loop/
```

每个 run 的输出目录格式建议为：

```text
results/modern_tcn_ablation/<exp_name>/<run_tag>/
```

例如：

```text
results/modern_tcn_ablation/exp1_grouped_ffn/gffn_d4_k31_seed21/
results/modern_tcn_ablation/exp2_dual_kernel/dual_k31_s5_seed21/
results/modern_tcn_ablation/exp3_patch_full/full128_mid_seed21/
```

每个 run 目录至少保存：

```text
config.json
config.yaml 或 config.md
train_log.txt
metrics_val.csv
metrics_test.csv
checkpoint.pt
best_model.pt
git_hash.txt
dataset_contract_copy.json
feature_names.txt
```

如果导出 ONNX，还必须保存：

```text
model.onnx
pytorch_onnx_consistency.md
matlab_onnx_consistency.md
```

所有训练脚本必须支持：

```text
--no_overwrite
```

如果输出目录已存在，必须直接报错退出，不得覆盖已有结果。

---

## 3. MATLAB generated layers namespace 规范

新实验导入 ONNX 到 MATLAB 时，必须使用独立 namespace。

禁止覆盖默认：

```text
src/ModernTCN/generated_layers/+modern_tcn_onnx_layers/
```

建议新建：

```text
src/ModernTCN/generated_layers/+modern_tcn_gffn_onnx_layers/
src/ModernTCN/generated_layers/+modern_tcn_dualkernel_onnx_layers/
src/ModernTCN/generated_layers/+modern_tcn_full_onnx_layers/
```

验收标准：

```text
默认 generated layers 不变
每个实验方向有自己的 generated layers namespace
MATLAB online predictor 可以通过参数选择使用哪个 namespace
Simulink 默认模型不被自动替换
```

---

## 4. 实验 1：补回 grouped pointwise ConvFFN

### 4.1 实验假设

官方 ModernTCN 的重要特点之一是把时间建模和变量/特征融合解耦。当前项目的 ModernTCN-small 已经保留了大核 depthwise temporal convolution，但 pointwise mixing 是普通通道混合，没有显式区分：

```text
变量内部的特征融合
同一特征维度下的跨变量融合
```

实验 1 的假设是：

```text
在保持 22 维输入、seq_len=128、无 patch 的前提下，补回 grouped pointwise ConvFFN 可以提升多变量 AGV 状态识别能力，尤其可能改善 acc_turn_transition、转向分类、theta_hat 稳定性和跨变量耦合建模。
```

### 4.2 新增模型族

新增：

```text
model_family = "small_gffn"
```

不要修改原 `ModernTCNSmall` 默认行为。新增以下类：

```text
ModernTCNGroupedConfig
ModernTCNGroupedBlock
ModernTCNGroupedSmall
```

### 4.3 模型结构要求

输入仍为：

```text
x: [B, T, F]
F = 22
T = 128
```

第一步：variable embedding。

```text
[B, T, F]
→ transpose
[B, F, T]
→ reshape
[B*F, 1, T]
→ Conv1d(1, dmodel, kernel_size=1)
→ BatchNorm1d(dmodel)
→ ReLU
→ reshape
[B, F*dmodel, T]
```

第二步：depthwise temporal convolution。

```text
Conv1d(
    in_channels=F*dmodel,
    out_channels=F*dmodel,
    kernel_size=kernel_size,
    padding=kernel_size//2,
    groups=F*dmodel
)
```

第三步：ConvFFN1，变量内部特征融合。

```text
groups = F = 22
```

含义：每个变量内部的 dmodel 个特征互相融合，但不同变量之间暂时不混合。

第四步：ConvFFN2，同一特征维度下跨变量融合。

先 reshape/permute：

```text
[B, F*dmodel, T]
→ [B, F, dmodel, T]
→ [B, dmodel, F, T]
→ [B, dmodel*F, T]
```

然后：

```text
groups = dmodel
```

含义：同一 feature 维度下，22 个变量之间进行融合。

第五步：残差连接与读出。

每个 block 保留：

```text
residual connection
BatchNorm 或 LayerNorm，优先沿用当前 small 版兼容 ONNX/MATLAB 的规范
ReLU 或 GELU，优先使用当前工程中已经验证兼容的激活
Dropout
可选 layer_scale，默认可以先关闭或使用较小初值
```

readout 保持当前 small 版思想：

```text
h_last
h_mean
h_max
input_stats，包括 last/mean/std/max/min
```

输出头保持三任务：

```text
main_head: flat / stall / slope
turn_head: right / straight / left
theta_head: theta_hat
```

### 4.4 推荐配置

第一轮只使用 22 维、seq_len=128 的当前数据集。

请先跑以下配置：

```text
gffn_d3_k31:
  dmodel = 3
  kernel_size = 31
  blocks = 5
  dropout = 0.15

 gffn_d4_k31:
  dmodel = 4
  kernel_size = 31
  blocks = 5
  dropout = 0.15

 gffn_d6_k31:
  dmodel = 6
  kernel_size = 31
  blocks = 5
  dropout = 0.20
```

可选追加：

```text
gffn_d4_k51:
  dmodel = 4
  kernel_size = 51
  blocks = 4
  dropout = 0.20
```

每个配置先跑 3 个 seed：

```text
21, 42, 101
```

### 4.5 训练命令参数要求

训练脚本需要支持类似参数：

```bash
--model_family small_gffn \
--input_dim 22 \
--seq_len 128 \
--dmodel 4 \
--kernel_size 31 \
--blocks 5 \
--dropout 0.15 \
--seed 21 \
--run_tag gffn_d4_k31_seed21 \
--output_root results/modern_tcn_ablation/exp1_grouped_ffn \
--no_overwrite
```

### 4.6 离线汇总

生成：

```text
results/modern_tcn_ablation/exp1_grouped_ffn/grouped_ffn_offline_summary.csv
results/modern_tcn_ablation/exp1_grouped_ffn/grouped_ffn_offline_summary.md
```

汇总内容必须包含：

```text
baseline ModernTCN-small
每个 gffn 配置的每个 seed
每个配置的 mean/std
最佳 seed
是否满足进入闭环条件
```

### 4.7 进入闭环条件

候选模型进入 ONNX/闭环前至少满足：

```text
acc_main >= baseline_acc_main - 0.003
acc_turn >= baseline_acc_turn - 0.005
acc_turn_transition >= baseline_acc_turn_transition
theta_mae_deg <= baseline_theta_mae_deg + 0.01
flat/stall/slope recall 无明显退化
```

如果多个模型满足条件，优先选择：

```text
acc_turn_transition 更高
theta_mae_deg 更低
模型参数更少
推理更快
```

### 4.8 ONNX 与闭环

最优 run 导出 ONNX，并生成：

```text
pytorch_onnx_consistency.md
matlab_onnx_consistency.md
```

闭环输出目录：

```text
results/compare/modern_tcn_ablation_closed_loop/exp1_grouped_ffn/<best_run>/
```

先跑主路径：

```text
path_factory_logistics_showcase_theta10_v3
```

若主路径不退化，再跑 multipath 和 robustness。

---

## 5. 实验 2：补回 large-kernel + small-kernel 双分支

### 5.1 实验假设

官方 ModernTCN 的大核模块包含重参数化思想，训练时可以同时利用大核和小核分支。当前项目 small 版只使用单个大核 depthwise convolution。

实验 2 的假设是：

```text
在保持当前 small 主体结构不变的前提下，加入 small-kernel temporal branch 可以改善短时突变和边界识别，例如转向进入/退出、坡度切换、堵转瞬间、电流峰值和轮速差突变。
```

### 5.2 新增模型族

新增：

```text
model_family = "small_dualkernel"
```

新增类：

```text
ModernTCNDualKernelConfig
ModernTCNDualKernelBlock
ModernTCNDualKernelSmall
```

不要修改原 `ModernTCNBlock` 和 `ModernTCNSmall` 默认行为。

### 5.3 模型结构要求

保持当前 small 版主体结构，只替换 temporal depthwise convolution。

原结构：

```text
temporal = depthwise Conv1d(kernel_size=31)
```

新结构：

```text
large_branch = depthwise Conv1d(kernel_size=large_kernel)
small_branch = depthwise Conv1d(kernel_size=small_kernel)
temporal_output = large_branch(x) + small_branch(x)
```

然后接：

```text
BatchNorm
ReLU
pointwise Conv1d
ReLU
Dropout
pointwise Conv1d
BatchNorm
Dropout
residual connection
```

第一阶段不要实现结构重参数化合并，保持 ONNX 与 MATLAB 导入简单。

### 5.4 推荐配置

先跑：

```text
dual_k31_s3:
  channels = 64
  blocks = 5
  large_kernel = 31
  small_kernel = 3
  dropout = 0.15

 dual_k31_s5:
  channels = 64
  blocks = 5
  large_kernel = 31
  small_kernel = 5
  dropout = 0.15

 dual_k31_s7:
  channels = 64
  blocks = 5
  large_kernel = 31
  small_kernel = 7
  dropout = 0.15
```

可选追加：

```text
dual_k51_s5:
  channels = 64
  blocks = 4
  large_kernel = 51
  small_kernel = 5
  dropout = 0.20
```

每个配置跑：

```text
seeds = 21, 42, 101
```

### 5.5 训练命令参数要求

训练脚本需要支持类似参数：

```bash
--model_family small_dualkernel \
--input_dim 22 \
--seq_len 128 \
--channels 64 \
--blocks 5 \
--large_kernel 31 \
--small_kernel 5 \
--dropout 0.15 \
--seed 21 \
--run_tag dual_k31_s5_seed21 \
--output_root results/modern_tcn_ablation/exp2_dual_kernel \
--no_overwrite
```

### 5.6 离线重点指标

实验 2 不只看整体准确率，要重点看边界和突变指标：

```text
acc_turn_transition
left_recall
right_recall
theta_edge_p95_abs_err
flat_peak_theta_error
false_turn_straight
stall_recall
```

如果当前评估脚本没有这些细分项，请新增离线分析脚本，但不要修改 baseline 原始结果。新增脚本应输出到 ablation 目录。

### 5.7 闭环重点指标

闭环重点看：

```text
转向过渡段 ey_rmse
转向过渡段 xy_rmse
omega_cmd_rms
delta_u_rms
theta_hat 是否有尖峰
constraint_touch_count
是否出现闭环振荡
```

如果 small-kernel 分支提高了离线 transition accuracy，但导致闭环控制输入更抖，则该模型不得作为默认模型。

### 5.8 输出目录

离线输出：

```text
results/modern_tcn_ablation/exp2_dual_kernel/
```

闭环输出：

```text
results/compare/modern_tcn_ablation_closed_loop/exp2_dual_kernel/<best_run>/
```

---

## 6. 实验 3：补回 patch embedding / ModernTCNFull

### 6.1 实验假设

官方 ModernTCN 的核心特点包括 patch embedding、变量-特征二维结构、大核 depthwise temporal convolution、变量内 FFN、跨变量 FFN、多 stage 表示等。当前项目代码中已经存在 `ModernTCNFull` 候选结构。

实验 3 的假设是：

```text
在 22 维输入条件下，引入 patch embedding 和更接近官方 ModernTCN 的 full 结构，可能提高长时间依赖建模和跨变量融合能力，从而改善离线准确度和闭环路径跟踪效果。
```

但该实验风险最高，因为 patch 会降低时间分辨率，可能损害转向过渡和闭环响应。

### 6.2 第一阶段：seq_len=128，不改数据集

第一阶段必须固定：

```text
input_dim = 22
seq_len = 128
```

不要新建长窗口数据集。先验证 patch/full 在当前窗口下是否有价值。

请检查训练脚本是否完整支持：

```text
--model_family full
--patch_size
--patch_stride
--dims
--stage_blocks
--large_kernels
--small_kernels
--ffn_ratio
--layer_scale_init
```

如果不支持，请补齐 CLI 参数和 config 保存。

### 6.3 推荐配置

先跑轻量版本，不要直接跑过大的 full 默认配置。

```text
full128_light:
  input_dim = 22
  seq_len = 128
  patch_size = 16
  patch_stride = 4
  dims = (8, 16)
  stage_blocks = (1, 1)
  large_kernels = (15, 9)
  small_kernels = (5, 3)

full128_mid:
  input_dim = 22
  seq_len = 128
  patch_size = 16
  patch_stride = 4
  dims = (16, 32)
  stage_blocks = (1, 1)
  large_kernels = (15, 9)
  small_kernels = (5, 3)

full128_densepatch:
  input_dim = 22
  seq_len = 128
  patch_size = 8
  patch_stride = 2
  dims = (16, 32)
  stage_blocks = (1, 1)
  large_kernels = (15, 9)
  small_kernels = (5, 3)
```

每个配置跑：

```text
seeds = 21, 42, 101
```

### 6.4 训练命令参数要求

训练脚本需要支持类似参数：

```bash
--model_family full \
--input_dim 22 \
--seq_len 128 \
--patch_size 16 \
--patch_stride 4 \
--dims 16,32 \
--stage_blocks 1,1 \
--large_kernels 15,9 \
--small_kernels 5,3 \
--seed 21 \
--run_tag full128_mid_seed21 \
--output_root results/modern_tcn_ablation/exp3_patch_full \
--no_overwrite
```

### 6.5 离线重点指标

full/patch 版本必须重点检查：

```text
acc_turn_transition 是否下降
theta_hat 是否更平滑
stall_recall 是否下降
slope_recall 是否改善
acc_turn 是否改善
```

如果 full/patch 版本整体准确率提高，但 `acc_turn_transition` 明显下降，则不适合闭环控制。

### 6.6 闭环条件

只有 full128 的某个候选模型满足离线晋级条件，才允许导出 ONNX 和进入闭环。

闭环输出目录：

```text
results/compare/modern_tcn_ablation_closed_loop/exp3_patch_full/<best_run>/
```

先跑主路径：

```text
path_factory_logistics_showcase_theta10_v3
```

如果主路径闭环劣于 baseline，则停止 patch/full 方向，不再做长窗口。

### 6.7 长窗口扩展建议，条件执行

只有在 `seq_len=128` 的 full/patch 版本同时满足以下条件时，才允许启动长窗口实验：

```text
离线指标不低于 baseline
acc_turn_transition 不退化
主路径闭环不退化
theta_hat 平滑性或路径跟踪指标有改善
```

若满足条件，可以新建 seq_len=256 数据集。新数据集必须单独命名，不能覆盖原数据。

建议文件名：

```text
data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2_seq256.mat
data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2_seq256_contract.json
```

保持不变：

```text
input_dim = 22
feature_names 完全相同
raw data source 完全相同
run-level split policy 完全相同
scaler policy = fit_train_only_apply_val_test_online
label_time_policy = current_window_end
horizon_steps = 0
```

只改变：

```text
seq_len = 256
window extraction
online buffer length
```

seq_len=256 推荐配置：

```text
full256_mid:
  input_dim = 22
  seq_len = 256
  patch_size = 16
  patch_stride = 4
  dims = (16, 32)
  stage_blocks = (1, 1)

full256_slow:
  input_dim = 22
  seq_len = 256
  patch_size = 32
  patch_stride = 8
  dims = (16, 32)
  stage_blocks = (1, 1)
```

只有 seq_len=256 明确有收益，才考虑 seq_len=512。seq_len=512 对应更长历史窗口，可能改善慢变化坡道/载荷，但也可能降低闭环响应速度，因此不得作为第一轮默认实验。

---

## 7. 统一离线晋级标准

候选模型进入 ONNX/闭环前，至少满足：

```text
acc_main >= baseline_acc_main - 0.003
acc_turn >= baseline_acc_turn - 0.005
acc_turn_transition >= baseline_acc_turn_transition
theta_mae_deg <= baseline_theta_mae_deg + 0.01
slope_recall >= baseline_slope_recall - 0.005
stall_recall 无明显下降
```

如果某模型 `acc_turn_transition` 提升明显，但 theta 略差，可以保留为闭环候选，但必须在 summary 中说明原因。

每个实验方向最多选择 1 到 2 个模型进入闭环，避免闭环仿真数量失控。

---

## 8. 统一闭环晋级标准

候选模型成为“有益改动”，必须满足：

```text
闭环不失稳
xy_rmse <= baseline_xy_rmse
ey_rmse <= baseline_ey_rmse
constraint_touch_count 不增加
omega_cmd_rms <= baseline_omega_cmd_rms * 1.05
delta_u_rms <= baseline_delta_u_rms * 1.05
overall_rank 优于或等于 baseline
```

如果离线提升但闭环退化，结论必须写成：

```text
该结构提升离线感知性能，但没有转化为闭环收益，因此不推荐替代当前默认 ModernTCN-small。
```

---

## 9. 最终模型替换规则

只有当某个候选模型满足以下全部条件，才允许建议替换当前默认 ModernTCN-small：

```text
离线多 seed 均值优于 baseline
最佳 seed 闭环主路径优于 baseline
multipath 闭环不退化
robustness 闭环不退化
ONNXRuntime 一致性通过
MATLAB ONNX 一致性通过
Simulink 部署无需修改主控制器逻辑
推理时间满足实时性要求
输出没有明显尖峰或振荡
```

如果不满足全部条件，则该模型只能作为：

```text
消融实验结果
候选增强模型
论文讨论项
```

不能替换当前默认模型。

---

## 10. 推荐执行顺序

请按以下顺序执行，不要跳过基线快照：

```text
阶段 0：建立 baseline snapshot，固定 22 维输入
阶段 1：实验 1 grouped pointwise ConvFFN
阶段 2：实验 2 dual-kernel branch
阶段 3：实验 3A full128 patch，不改数据集
阶段 4：只有 full128 有收益时，才做 seq_len=256
阶段 5：只有 seq_len=256 有收益时，才考虑 seq_len=512
```

优先级排序：

```text
最高优先级：small_gffn
第二优先级：small_dualkernel
第三优先级：full128 patch
条件执行：seq_len=256
谨慎执行：seq_len=512
```

---

## 11. 每个实验最终产物

每个实验完成后，至少生成：

```text
results/modern_tcn_ablation/<exp>/offline_summary.csv
results/modern_tcn_ablation/<exp>/offline_summary.md
results/modern_tcn_ablation/<exp>/best_run_selection.md
```

如果进入 ONNX：

```text
results/modern_tcn_ablation/<exp>/<best_run>/model.pt
results/modern_tcn_ablation/<exp>/<best_run>/model.onnx
results/modern_tcn_ablation/<exp>/<best_run>/pytorch_onnx_consistency.md
results/modern_tcn_ablation/<exp>/<best_run>/matlab_onnx_consistency.md
```

如果进入闭环：

```text
results/compare/modern_tcn_ablation_closed_loop/<exp>/<best_run>/closed_loop_summary.csv
results/compare/modern_tcn_ablation_closed_loop/<exp>/<best_run>/closed_loop_report.md
```

最终总报告：

```text
results/modern_tcn_ablation/modern_tcn_official_feature_ablation_summary.md
```

总报告必须回答：

```text
grouped pointwise ConvFFN 是否有效？
dual-kernel branch 是否有效？
patch/full 是否有效？
是否有模型同时提升离线和闭环？
是否推荐替换当前默认 ModernTCN-small？
如果不替换，哪些结果可以写入论文消融？
```

---

## 12. 给 Codex 的执行提示

请优先完成以下最小闭环：

```text
1. 建立 baseline snapshot。
2. 新增 small_gffn 模型族。
3. 跑 gffn_d4_k31_seed21。
4. 确认训练、测试、保存、评估、目录保护全部正常。
5. 再跑 gffn_d3_k31/gffn_d4_k31/gffn_d6_k31 的 3 seeds。
6. 汇总 exp1 结果。
7. 只有 exp1 最优模型满足离线晋级条件后，再导出 ONNX 和跑闭环。
```

不要一开始同时实现所有实验方向。先把 exp1 的工程链路跑通，再复制该链路到 exp2 和 exp3。
