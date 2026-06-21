# ModernTCN_small 后续 SCI 创新实验技术要求文档（Codex 执行版）

**项目仓库**：`https://github.com/Cr20253V/ModernTCN_v4`  
**文档用途**：指导 Codex 在当前项目中继续开展基于 `ModernTCN_small` 的 SCI 论文创新实验。  
**核心原则**：本轮工作不再以“补回官方 ModernTCN 完整结构”为主，而是围绕当前项目最优的 `ModernTCN_small`，面向 AGV 路径跟踪闭环控制进行针对性改进。  
**硬性前提**：不得影响当前最优结论，不得覆盖之前实验结果，不得修改当前 baseline 的默认行为。

---

## 1. 当前最优项目状态

当前项目已经完成多轮对比和 ablation。经过前期实验后，当前最优算法仍为：

```text
ModernTCN_small
input_dim = 22
seq_len = 128
feature_contract = passive17_plus_all5
plant_revision = agv_physics_v2_plantfix
```

当前 ModernTCN_small 是一个工程化轻量版本，不是官方完整 ModernTCN。其核心结构为：

```text
22维输入时间窗口 [B, 128, 22]
        ↓
轻量通道映射 / stem
        ↓
大核 depthwise temporal convolution
        ↓
pointwise channel mixing
        ↓
residual connection
        ↓
窗口级 readout + input statistics
        ↓
三任务输出：
    main_head: flat / stall / slope
    turn_head: right / straight / left
    theta_head: theta_hat
```

当前主线任务不是普通时间序列预测，而是：

```text
使用 ModernTCN_small 在线预测 AGV 行驶状态与调度量
        ↓
为 LPV-MPC 提供工况、转向、坡度/调度信息
        ↓
改善路径跟踪精度、控制平滑性和闭环稳定性
```

---

## 2. 当前薄弱环节

### 2.1 转向方向识别仍有提升空间

`turn_head` 输出：

```text
right / straight / left
```

典型问题：

```text
1. 转向进入/退出阶段识别困难；
2. straight 与 left/right 边界容易混淆；
3. 转向过渡窗口对闭环控制影响大；
4. 离线 turn 指标不高可能影响 MPC 调度和控制平滑性。
```

### 2.2 stall recall 仍是风险点

`main_head` 输出：

```text
flat / stall / slope
```

典型问题：

```text
1. stall 样本可能占比较低；
2. stall 边界窗口可能难以区分 flat/slope；
3. stall 误判会影响调度安全性；
4. stall 类可能需要困难样本加权或物理特征增强。
```

### 2.3 theta_hat 精度和平滑性仍可优化

`theta_head` 输出：

```text
theta_hat
```

典型问题：

```text
1. theta_hat 离线 MAE 不是唯一目标；
2. theta_hat 边界尖峰可能导致控制抖动；
3. flat 工况下 theta 应尽量接近 0；
4. slope 工况下 theta 应准确跟随坡度；
5. stall 工况下 theta 的物理意义可能不同于 slope；
6. theta 输出需要更适合闭环调度，而不是只追求离线误差。
```

### 2.4 多任务之间存在潜在冲突

当前模型同时优化：

```text
main classification
turn classification
theta regression
```

前期 ablation 中已反复出现以下现象：

```text
theta / transition 指标局部改善
但 acc_main / stall_recall / slope_recall 下降
```

这说明瓶颈可能不是模型容量不足，而是多任务训练目标之间存在冲突。

### 2.5 离线指标提升不一定带来闭环提升

后续实验必须坚持：

```text
离线测试通过 gate
        ↓
ONNX / MATLAB 一致性验证
        ↓
主路径闭环
        ↓
多路径闭环
        ↓
扰动鲁棒性闭环
```

不得只根据离线指标替换当前最优模型。

---

## 3. 前期失败实验的处理原则

前期已完成以下方向：

```text
1. grouped pointwise ConvFFN
2. dual-kernel large/small branch
3. patch/full ModernTCN
4. seq256 / densepatch 等后续尝试
```

这些方向未能超过当前 ModernTCN_small baseline。后续应按如下方式处理：

```text
1. 这些实验作为负结果证据保留；
2. 不删除、不覆盖、不重写这些结果；
3. 不再简单扩大这些失败配置的 seed；
4. 不再以“补回官方 ModernTCN 结构”为主线；
5. 如果借鉴其中思想，必须转化为更贴合 AGV 物理和闭环控制的结构。
```

---

## 4. 本轮总目标

本轮目标不是证明官方 ModernTCN 比当前 small 版更强，而是构建一个更适合 AGV 闭环路径跟踪的 `ModernTCN_small` 增强版本。

推荐论文方法方向：

```text
Physics-Guided Confidence-Scheduled ModernTCN-small
```

或者：

```text
PGCS-ModernTCN-small
```

建议目标：

```text
1. 保留当前 ModernTCN_small 主干；
2. 不破坏当前最优离线和闭环 baseline；
3. 引入 AGV 物理变量分组；
4. 缓解 main / turn / theta 多任务冲突；
5. 提升 turn_transition 和 stall_recall；
6. 改善 theta_hat 的闭环调度平滑性；
7. 用闭环路径跟踪指标证明改进有效。
```

---

## 5. 总体实验路线

后续研发路线按以下顺序进行：

```text
Phase 0: 冻结当前 baseline 和历史实验结果
Phase 1: 不改模型结构，先做多任务损失优化
Phase 2: 加入困难样本与 theta 平滑损失
Phase 3: 加入 AGV 物理分组残差门控结构
Phase 4: 加入工况条件化 theta experts
Phase 5: 加入置信度感知调度层
Phase 6: 通过闭环测试筛选 SCI 主方法
Phase 7: 汇总消融、负结果和论文主结论
```

所有阶段必须顺序执行，不得跳过 baseline 复核直接训练新结构。

---

## 6. 输出目录规范

新增本轮实验根目录：

```text
results/modern_tcn_sci_innovation/
```

建议目录结构：

```text
results/modern_tcn_sci_innovation/
    00_baseline_lock/
    01_loss_optimization/
    02_hard_sample_loss/
    03_physics_group_gate/
    04_mode_conditioned_theta/
    05_confidence_scheduling/
    06_closed_loop_validation/
    07_ablation_summary/
    08_final_report/
```

所有新实验必须使用新目录，不得覆盖：

```text
results/modern_tcn_ablation/
results/modern_tcn_next_round_22d/
results/compare/tcn_gru_modern_closed_loop/
已有 baseline checkpoint
已有 ONNX
已有 MATLAB generated layers
已有 Simulink 默认配置
```

所有新模型必须使用新的 `model_family`，禁止修改当前 `model_family="small"` 的默认行为。

---

## 7. Phase 0：冻结 baseline

### 7.1 目标

确保所有后续实验均与当前最优 ModernTCN_small 公平比较，并保证不会覆盖已有结果。

### 7.2 执行任务

生成：

```text
results/modern_tcn_sci_innovation/00_baseline_lock/baseline_lock.md
results/modern_tcn_sci_innovation/00_baseline_lock/baseline_offline_metrics.csv
results/modern_tcn_sci_innovation/00_baseline_lock/baseline_closed_loop_metrics.csv
results/modern_tcn_sci_innovation/00_baseline_lock/baseline_file_check.csv
```

必须记录：

```text
1. git commit hash
2. baseline checkpoint path
3. baseline dataset path
4. baseline dataset contract
5. input_dim = 22
6. seq_len = 128
7. feature_names
8. training/validation/test window count
9. baseline offline metrics
10. baseline closed-loop metrics
11. baseline ONNX path
12. baseline MATLAB config path
13. previous ablation result directories
```

### 7.3 停止条件

```text
1. 如果当前默认数据链不是 22D，必须停止。
2. 如果 baseline 文件不存在，必须停止。
3. 如果脚本试图覆盖历史结果，必须停止。
```

---

## 8. Phase 1：多任务损失优化

本阶段不改 ModernTCN_small 结构，只改训练损失。  
目的是判断当前瓶颈是否主要来自多任务 loss 冲突。

### Experiment 1A：Uncertainty Weighting

#### 目标

自动学习 main、turn、theta 三个任务 loss 权重。

普通形式：

```text
L = w_main * L_main + w_turn * L_turn + w_theta * L_theta
```

改成：

```text
L = exp(-s_main)  * L_main  + s_main
  + exp(-s_turn)  * L_turn  + s_turn
  + exp(-s_theta) * L_theta + s_theta
```

其中：

```text
s_main, s_turn, s_theta 为可学习参数
```

#### 新 train_mode

```text
model_family = small
loss_mode = uncertainty_weighting
run_group = exp1a_uncertainty
```

#### 配置建议

```text
input_dim = 22
seq_len = 128
model_family = small
channels = 64
blocks = 5
kernel_size = 31
dropout = 0.15
temporal_padding = same
seeds = 21, 42, 101
```

#### 输出目录

```text
results/modern_tcn_sci_innovation/01_loss_optimization/uncertainty_seed21/
results/modern_tcn_sci_innovation/01_loss_optimization/uncertainty_seed42/
results/modern_tcn_sci_innovation/01_loss_optimization/uncertainty_seed101/
```

#### 必须记录

```text
1. final s_main / s_turn / s_theta
2. 每个 epoch 的任务 loss
3. 每个 epoch 的有效任务权重
4. offline metrics
5. confusion matrix
```

### Experiment 1B：GradNorm

#### 目标

动态平衡 main、turn、theta 三个任务的梯度强度，缓解某个任务主导训练的问题。

#### 新 train_mode

```text
model_family = small
loss_mode = gradnorm
run_group = exp1b_gradnorm
```

#### 配置建议

```text
input_dim = 22
seq_len = 128
model_family = small
channels = 64
blocks = 5
kernel_size = 31
dropout = 0.15
gradnorm_alpha = 1.5
seeds = 21, 42, 101
```

#### 输出目录

```text
results/modern_tcn_sci_innovation/01_loss_optimization/gradnorm_seed21/
results/modern_tcn_sci_innovation/01_loss_optimization/gradnorm_seed42/
results/modern_tcn_sci_innovation/01_loss_optimization/gradnorm_seed101/
```

#### 必须记录

```text
1. 每个任务的梯度范数
2. 每个任务的动态权重
3. main / turn / theta loss 曲线
4. offline metrics
5. 是否出现训练不稳定
```

### Phase 1 判断标准

比较：

```text
baseline small
uncertainty weighting
GradNorm
```

核心指标：

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
```

处理方法：

```text
如果 uncertainty weighting 最好：
    后续所有实验使用 uncertainty weighting 作为默认 loss_mode。

如果 GradNorm 最好：
    后续所有实验使用 GradNorm 作为默认 loss_mode。

如果两者都不如 baseline：
    后续实验继续使用原 baseline loss，不再强行使用动态权重。

如果某方法只提升 theta 但明显损害 acc_main/stall/slope：
    不进入下一阶段主线，只作为负结果记录。
```

输出：

```text
results/modern_tcn_sci_innovation/01_loss_optimization/loss_optimization_summary.md
results/modern_tcn_sci_innovation/01_loss_optimization/loss_optimization_decision.json
```

---

## 9. Phase 2：困难样本与平滑损失

本阶段仍不改主干结构。  
目标是提升 turn_transition、stall_recall 和 theta 输出平滑性。

### Experiment 2：Focal + Smooth Loss

#### 目标

在 Phase 1 最优 loss 设置基础上，增加：

```text
1. transition focal loss
2. stall focal / class-balanced loss
3. theta smoothness loss
```

#### 推荐损失形式

```text
L_total =
    L_main
  + L_turn
  + L_theta
  + lambda_stall * L_stall_focal
  + lambda_transition * L_transition_focal
  + lambda_smooth * L_theta_smooth
```

其中：

```text
L_transition_focal:
    只对 turn transition window 或其附近窗口加权。

L_stall_focal:
    对 main=stall 样本加权，提升 stall recall。

L_theta_smooth:
    对同一 run 中相邻窗口的 theta_hat 做平滑约束。
```

#### 新 train_mode

```text
model_family = small
loss_mode = <Phase 1 best> + hard_sample_smooth
run_group = exp2_focal_smooth
```

#### 配置建议

第一轮小网格：

```text
lambda_transition = [0.2, 0.5]
lambda_stall = [0.2, 0.5]
lambda_smooth = [0.01, 0.03]
focal_gamma = 2.0
```

不要一次跑完整笛卡尔积。建议先跑 4 个配置：

```text
fs_t02_s02_sm001
fs_t05_s02_sm001
fs_t02_s05_sm001
fs_t05_s05_sm003
```

每个配置先跑：

```text
seed = 21
```

只有 seed21 接近或超过 baseline，再扩展：

```text
seeds = 42, 101
```

#### 输出目录

```text
results/modern_tcn_sci_innovation/02_hard_sample_loss/<run_tag>/
```

#### Phase 2 判断标准

优先关注：

```text
acc_turn_transition
stall_recall
theta_mae_deg
theta_edge_p95_abs_err
flat_peak_theta_error
```

处理方法：

```text
如果 transition 提升但 acc_main 或 slope_recall 明显下降：
    不晋级，记录为多任务冲突。

如果 stall_recall 提升但 flat_recall 明显下降：
    不晋级，降低 lambda_stall 后重试一次。

如果 theta_mae 降低但 theta_edge_p95 或 flat_peak 变差：
    不晋级，因为闭环可能抖动。

如果三者综合优于 baseline：
    作为 loss-best baseline 进入 Phase 3。
```

输出：

```text
results/modern_tcn_sci_innovation/02_hard_sample_loss/hard_sample_loss_summary.md
results/modern_tcn_sci_innovation/02_hard_sample_loss/hard_sample_loss_decision.json
```

---

## 10. Phase 3：AGV 物理分组残差门控

这是本轮最重要的结构创新方向。  
注意：本阶段不再使用官方通用 grouped pointwise ConvFFN，而是基于 AGV 物理含义分组。

### Experiment 3：Physics-Group Residual Gate

#### 目标

在保留当前 ModernTCN_small 主干的前提下，增加 AGV 物理分组辅助分支，使模型更好利用车辆物理结构。

#### 建议模型名称

```text
model_family = small_physics_group_gate
method_name = PG-ModernTCN-small
```

#### 物理分组建议

请按 22D feature_names 精确建立索引映射，不要硬编码错误顺序。建议分组如下：

```text
Group 1: yaw / steering group
    gyro_z
    delta_lf
    delta_rr
    kappa_proxy
    yaw_consistency_error

Group 2: drive / current / load group
    I_lf
    I_rr
    I_sum
    I_diff_signed
    I_diff_abs
    drive_load_proxy
    current_per_accel
    accel_per_current

Group 3: velocity / acceleration group
    v_hat
    dv_hat_dt
    dv_hat_dt_lp
    accel_x_wheel
    a_hp

Group 4: wheel imbalance group
    omega_wheel_lf
    omega_wheel_rr
    ws_imbalance
```

如果发现有未分配特征，放入：

```text
Group 5: residual group
```

但必须在报告中列出。

#### 结构要求

保留原 ModernTCN_small 主干：

```text
h_base = ModernTCN_small_trunk(x)
```

新增物理组分支：

```text
h_yaw   = GroupTemporalBranch(x_yaw)
h_drive = GroupTemporalBranch(x_drive)
h_vel   = GroupTemporalBranch(x_vel)
h_wheel = GroupTemporalBranch(x_wheel)
```

门控融合：

```text
g = softmax(Gate([h_yaw, h_drive, h_vel, h_wheel]))

h_phys = g_yaw   * h_yaw
       + g_drive * h_drive
       + g_vel   * h_vel
       + g_wheel * h_wheel

h_final = h_base + alpha * h_phys
```

硬性要求：

```text
1. alpha 初始化为 0.0 或 0.1；
2. alpha 必须可学习；
3. 原 small 主干初始行为应尽量接近 baseline；
4. 不得修改 model_family="small" 的行为；
5. 必须记录每个样本或每类工况下的 group gate 平均权重；
6. 必须记录 alpha 的训练变化。
```

#### 分支结构建议

每个 `GroupTemporalBranch` 可使用轻量结构：

```text
Conv1d(group_dim, branch_channels, kernel_size=1)
Depthwise Conv1d(branch_channels, branch_channels, kernel_size=15 or 31, groups=branch_channels)
BatchNorm
ReLU
Global mean / last / max pooling
Linear to hidden_dim
```

第一轮建议：

```text
branch_channels = 16
branch_kernel = 31
alpha_init = 0.0
gate_hidden = 32
```

#### 训练配置

基于 Phase 2 的 best loss，如果 Phase 2 没有收益，则基于 baseline loss。

```text
input_dim = 22
seq_len = 128
model_family = small_physics_group_gate
channels = 64
blocks = 5
kernel_size = 31
branch_channels = 16
branch_kernel = 31
alpha_init = 0.0 or 0.1
seeds = 21, 42, 101
```

建议先跑：

```text
pg_alpha0_seed21
pg_alpha01_seed21
```

如果 seed21 接近或超过 baseline，再扩展 3 seeds。

#### 输出目录

```text
results/modern_tcn_sci_innovation/03_physics_group_gate/<run_tag>/
```

#### 必须输出

```text
1. offline metrics
2. main confusion matrix
3. turn confusion matrix
4. per-class group gate mean
5. per-class group gate std
6. per-task group gate mean
7. alpha final value
8. feature group index audit
9. gate interpretability report
```

#### Phase 3 判断标准

通过条件：

```text
acc_main >= reference_acc_main - 0.003
acc_turn >= reference_acc_turn - 0.005
acc_turn_transition >= reference_acc_turn_transition
theta_mae_deg <= reference_theta_mae_deg + 0.01
stall_recall 不明显下降
slope_recall 不明显下降
```

加分条件：

```text
1. group gate 在不同工况下有可解释差异；
2. yaw group 在 turn transition 中权重更高；
3. drive/current group 在 stall 中权重更高；
4. velocity group 在 flat/slope 中有合理变化；
5. alpha 学到非零，说明物理分支有贡献。
```

处理方法：

```text
如果 alpha 最终接近 0：
    物理分支未被使用，记录为无效结构。

如果 alpha 很大但主指标下降：
    说明物理分支破坏主干，不晋级。

如果 gate 无可解释性但指标提升：
    可以作为性能改进，但论文解释性较弱。

如果 gate 有解释性且指标提升：
    作为 SCI 主方法候选进入 Phase 4。
```

---

## 11. Phase 4：工况条件化 theta experts

本阶段解决 theta 回归在不同工况下物理意义不同的问题。

### Experiment 4：Mode-Conditioned Theta Experts

#### 目标

用三个工况条件化 theta experts 替代单一 theta head。

#### 新 model_family

```text
model_family = small_mode_theta
```

如果 Phase 3 成功，则基于：

```text
model_family = small_physics_group_gate_mode_theta
```

#### 结构要求

当前共享特征：

```text
h = trunk_or_pg_feature(x)
```

输出：

```text
main_logits = main_head(h)
p_main = softmax(main_logits)

theta_flat  = theta_flat_head(h)
theta_stall = theta_stall_head(h)
theta_slope = theta_slope_head(h)

theta_hat =
    p_flat  * theta_flat
  + p_stall * theta_stall
  + p_slope * theta_slope
```

建议第一轮使用：

```text
theta_gate_detach = True
```

即：

```text
theta_hat =
    detach(p_flat)  * theta_flat
  + detach(p_stall) * theta_stall
  + detach(p_slope) * theta_slope
```

目的是防止 theta loss 反向破坏 main_head。

#### 可选正则

```text
flat_theta_regularization:
    对 main label = flat 的样本，惩罚 |theta_flat|

expert_diversity_regularization:
    防止三个 expert 完全相同

mode_consistency_regularization:
    当 label=slope 时，提高 theta_slope 的学习权重
```

第一轮建议只使用：

```text
theta_gate_detach = True
flat_theta_reg_lambda = 0.01
```

不要同时加入太多正则。

#### 训练配置

```text
input_dim = 22
seq_len = 128
base_model = Phase 2 best 或 Phase 3 best
theta_gate_detach = True
flat_theta_reg_lambda = [0.0, 0.01, 0.03]
seeds = 21, 42, 101
```

建议先跑：

```text
mode_theta_detach_flatreg001_seed21
mode_theta_detach_flatreg003_seed21
```

#### 输出目录

```text
results/modern_tcn_sci_innovation/04_mode_conditioned_theta/<run_tag>/
```

#### 必须输出

```text
1. theta overall MAE
2. theta MAE by main class
3. flat theta peak error
4. slope theta MAE
5. stall theta MAE
6. expert contribution statistics
7. main confusion matrix
8. 是否因 theta expert 破坏 main 分类
```

#### Phase 4 判断标准

通过条件：

```text
theta_mae_deg <= reference_theta_mae_deg
flat_peak_theta_error <= reference_flat_peak_theta_error
theta_edge_p95_abs_err <= reference_theta_edge_p95_abs_err
acc_main 不明显下降
stall_recall 不明显下降
slope_recall 不明显下降
```

处理方法：

```text
如果 theta 改善但 main 分类明显下降：
    保留 theta_gate_detach=True，降低 theta loss 权重或 flat reg。

如果 flat theta peak 改善但 slope theta 变差：
    调低 flat_theta_reg_lambda。

如果三个 expert 输出几乎相同：
    说明条件化没有起作用，可停止该方向。

如果 theta by-class 全面改善：
    作为 prediction-best 候选进入 Phase 5。
```

---

## 12. Phase 5：置信度感知调度层

本阶段重点不是提高离线指标，而是提高闭环路径跟踪效果。

### Experiment 5：Confidence-Aware Scheduling Filter

#### 目标

让神经网络输出更适合 LPV-MPC 调度，降低 theta 抖动和闭环控制输入波动。

#### 基本思想

不要直接使用：

```text
theta_sched = theta_hat
```

而是使用：

```text
theta_sched = c * theta_hat + (1 - c) * theta_safe
```

其中：

```text
c = confidence score
theta_safe = safe fallback scheduling value
```

再加入变化率限制：

```text
theta_sched(t) = clip(
    theta_sched(t),
    theta_sched(t-1) - delta_theta_max,
    theta_sched(t-1) + delta_theta_max
)
```

#### confidence 计算方式

第一轮不新增复杂 uncertainty head，直接用已有 logits：

```text
main_conf = max(softmax(main_logits))
turn_conf = max(softmax(turn_logits))
```

推荐：

```text
c = main_conf
```

或者：

```text
c = main_conf * turn_conf
```

#### theta_safe 候选

按优先级测试：

```text
1. theta_safe = previous theta_sched
2. theta_safe = low-pass theta_hat
3. theta_safe = 0 for high-confidence flat
4. theta_safe = baseline theta_hat
```

第一轮建议：

```text
theta_safe = previous theta_sched
```

#### 配置建议

```text
conf_threshold = [0.5, 0.6, 0.7]
delta_theta_max_deg_per_step = [0.05, 0.1, 0.2]
confidence_mode = [main_conf, main_turn_conf]
```

不要跑完整笛卡尔积。先跑：

```text
cs_main_c06_d01
cs_main_c07_d01
cs_mainturn_c06_d01
cs_main_c06_d02
```

#### 适用模型

优先使用：

```text
Phase 4 best model
```

如果 Phase 4 无收益，则使用：

```text
Phase 3 best model
```

如果 Phase 3 也无收益，则使用：

```text
baseline ModernTCN_small
```

这意味着即使模型结构没有提升，也可以测试调度层是否带来闭环收益。

#### 输出目录

```text
results/modern_tcn_sci_innovation/05_confidence_scheduling/<run_tag>/
```

#### 必须输出

```text
1. theta_raw vs theta_sched 曲线
2. theta_sched_mae_deg
3. theta_sched_smoothness
4. main_conf / turn_conf 分布
5. 低置信度窗口统计
6. 调度变化率统计
7. sandbox closed-loop metrics
```

---

## 13. Phase 6：闭环验证

只有通过前面离线 gate 的候选，或者明确作为 sandbox 的 confidence scheduling，才允许进入闭环。

### 13.1 闭环验证顺序

```text
Step 1: 单路径主场景闭环
Step 2: 多路径闭环
Step 3: 扰动鲁棒性闭环
Step 4: 与 ModernTCN_small / TCN / GRU / oracle 对比
```

### 13.2 输出目录

正式候选：

```text
results/modern_tcn_sci_innovation/06_closed_loop_validation/formal/<run_tag>/
```

sandbox 候选：

```text
results/modern_tcn_sci_innovation/06_closed_loop_validation/sandbox/<run_tag>/
```

不得写入或覆盖旧目录：

```text
results/compare/tcn_gru_modern_closed_loop/
```

### 13.3 闭环指标

必须统计：

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
gap_to_oracle
```

### 13.4 闭环晋级规则

正式候选必须满足：

```text
1. 闭环不失稳；
2. xy_rmse <= baseline；
3. ey_rmse <= baseline；
4. constraint_touch_count 不增加；
5. omega_cmd_rms 或 delta_u_rms 不高于 baseline 5%；
6. theta_sched_mae_deg 不高于 baseline；
7. main/turn 在线准确率不显著下降。
```

处理方法：

```text
如果离线优于 baseline，但闭环差：
    不替代 baseline，记录为“离线提升未转化为闭环收益”。

如果离线略低，但 confidence scheduling 闭环更平滑：
    可作为控制接口创新，不作为感知模型替换。

如果闭环单路径提升但多路径退化：
    不作为最终主方法，只作为局部场景有效。

如果多路径和扰动均提升：
    进入论文主结果。
```

---

## 14. 最小可执行实验组合

本轮最小可执行组合为 5 个方向。Codex 应按顺序执行。

### E0：Baseline 复核

```text
模型：ModernTCN_small
输入：22D
窗口：seq_len=128
目的：锁定当前最优结果
是否训练：否，优先读取已有结果
```

输出：

```text
baseline_lock.md
baseline_offline_metrics.csv
baseline_closed_loop_metrics.csv
```

### E1：Loss-only Optimization

```text
模型：ModernTCN_small
改动：uncertainty weighting 或 GradNorm
目的：验证多任务冲突是否是主要瓶颈
```

执行：

```text
1. 跑 uncertainty weighting，seeds = 21,42,101
2. 跑 GradNorm，seeds = 21,42,101
3. 选择更好者作为后续 loss 策略
```

### E2：Hard-sample + Smooth Loss

```text
模型：ModernTCN_small
改动：transition focal + stall focal + theta smoothness
目的：提升 transition、stall 和 theta 平滑性
```

执行：

```text
1. 以 E1 最优 loss 策略为基础；
2. seed21 小网格搜索；
3. 接近 gate 后扩展到 seeds 42,101；
4. 选出 loss-best baseline。
```

### E3：Physics-Group Residual Gate

```text
模型：ModernTCN_small + AGV 物理分组残差门控
目的：验证物理分组是否优于通用 grouped FFN
```

执行：

```text
1. 保留原 small 主干；
2. 增加 yaw/steer、drive/current/load、velocity/acc、wheel imbalance 物理组分支；
3. 使用 softmax gate 融合；
4. 用 alpha residual 接入主干；
5. 记录 gate 可解释性；
6. 与 baseline 和 loss-best baseline 比较。
```

### E4：Mode-Conditioned Theta Experts

```text
模型：E2 或 E3 最佳模型 + 工况条件化 theta experts
目的：解决不同工况下 theta 物理意义不同的问题
```

执行：

```text
1. main_head 输出 flat/stall/slope 概率；
2. 三个 theta expert 分别预测 theta_flat/theta_stall/theta_slope；
3. 用 main soft probability 融合；
4. 第一轮使用 detach(main_prob)；
5. 重点比较 theta by class 和 flat peak。
```

### E5：Confidence-Aware Scheduling Filter

```text
模型：E4 / E3 / baseline 最佳模型
改动：置信度感知 theta 调度与变化率限制
目的：改善闭环路径跟踪和平滑性
```

执行：

```text
1. 基于 main_conf / turn_conf 构建 confidence；
2. theta_sched = c * theta_hat + (1-c) * theta_safe；
3. theta_safe 第一轮使用 previous theta_sched；
4. 加入 delta_theta_max rate limit；
5. 先 sandbox 闭环；
6. 若改善明显，再进入正式闭环验证。
```

---

## 15. 实验结果分支处理规则

### 15.1 E1/E2 有效

```text
1. 将最优 loss 策略作为后续所有模型默认训练策略；
2. 在报告中说明当前瓶颈主要来自多任务冲突和困难样本不足；
3. 继续执行 E3；
4. E3 必须与 loss-best baseline 比较，而不是只与原 baseline 比较。
```

### 15.2 E1/E2 无效

```text
1. 后续继续使用原 baseline loss；
2. 将 E1/E2 记录为负结果；
3. 继续执行 E3；
4. 不再在 loss 上做大规模网格搜索。
```

### 15.3 E3 有效

```text
1. 将其作为结构主创新候选；
2. 继续 E4；
3. 闭环时优先测试 E3/E4 模型；
4. 报告 gate 在不同工况下的物理解释。
```

### 15.4 E3 无效

```text
1. 不继续扩展更复杂物理分支；
2. 记录 gate 权重和 alpha；
3. 如果 alpha≈0，说明模型拒绝物理分支；
4. 继续测试 E4 时基于 E2 或 baseline。
```

### 15.5 E4 有效

```text
1. 进入 E5；
2. 重点闭环测试 theta_sched 和控制平滑性；
3. 论文中强调不同工况下调度量估计的差异。
```

### 15.6 E4 无效

```text
1. 不再继续增加 theta experts 复杂度；
2. 直接使用 E3 或 E2 最佳模型进入 E5；
3. 如果 theta 改善但 main 下降，检查 detach 是否生效。
```

### 15.7 E5 有效

```text
1. 即使模型离线提升有限，也可作为控制接口创新；
2. 进入 formal closed-loop；
3. 多路径和扰动鲁棒性必须验证；
4. 与 oracle true-theta 的 gap 必须报告。
```

### 15.8 E5 无效

```text
1. 保留模型预测端最优结果；
2. 不将 confidence scheduling 写入主方法；
3. 记录为负结果；
4. 最终论文主线回到 E2/E3/E4 中最有效模块。
```

---

## 16. 统一离线 gate

候选模型进入 ONNX / MATLAB / 闭环前，必须满足以下离线 gate。

```text
acc_main >= baseline_acc_main - 0.003
acc_turn >= baseline_acc_turn - 0.005
acc_turn_transition >= baseline_acc_turn_transition
theta_mae_deg <= baseline_theta_mae_deg + 0.01
flat_recall >= baseline_flat_recall - 0.010
stall_recall >= baseline_stall_recall - 0.050
slope_recall >= baseline_slope_recall - 0.005
theta_edge_p95_abs_err 不恶化
flat_peak_theta_error 不恶化
```

特殊说明：

```text
E5 confidence scheduling 可以作为 sandbox 进入闭环，即使模型本体未完全通过 gate；
但不得写入正式 compare 目录，不得替代 baseline。
```

---

## 17. ONNX / MATLAB / Simulink 要求

任何正式候选进入闭环前，必须通过：

```text
1. PyTorch vs ONNXRuntime consistency
2. PyTorch vs MATLAB ONNX consistency
3. generated layers namespace audit
4. latency test
```

新 namespace 建议：

```text
+modern_tcn_lossopt_onnx_layers
+modern_tcn_pg_onnx_layers
+modern_tcn_mode_theta_onnx_layers
+modern_tcn_conf_sched_onnx_layers
```

禁止覆盖：

```text
+modern_tcn_onnx_layers
```

---

## 18. 最终报告要求

最终生成：

```text
results/modern_tcn_sci_innovation/08_final_report/sci_innovation_final_report.md
results/modern_tcn_sci_innovation/08_final_report/sci_innovation_decision.json
results/modern_tcn_sci_innovation/08_final_report/sci_innovation_master_table.csv
```

报告必须回答：

```text
1. 当前 ModernTCN_small 的主要薄弱环节是什么？
2. 多任务动态权重是否有效？
3. transition/stall focal 与 theta smoothness 是否有效？
4. AGV 物理分组门控是否有效？
5. gate 权重是否具有物理解释？
6. 工况条件化 theta experts 是否有效？
7. confidence-aware scheduling 是否改善闭环？
8. 哪些模块可以组成最终 SCI 主方法？
9. 哪些模块是负结果？
10. 是否建议替换当前 ModernTCN_small baseline？
11. 如果不替换，是否能形成控制接口创新？
12. 最终模型相对 TCN、GRU、ModernTCN_small、oracle 的表现如何？
```

---

## 19. 建议论文主线

如果实验成功，建议论文方法命名：

```text
Physics-Guided Confidence-Scheduled ModernTCN-small
```

可写作：

```text
PGCS-ModernTCN
```

建议贡献点：

```text
Contribution 1:
提出面向对角双转向 AGV 的物理分组残差门控 ModernTCN_small，
根据 yaw/steering、drive/current/load、velocity/acceleration、wheel imbalance 等物理组建模时序特征。

Contribution 2:
提出工况条件化 theta 调度估计头，
根据 flat/stall/slope 软概率融合不同 theta experts，提高不同工况下的调度量估计稳定性。

Contribution 3:
提出置信度感知的 LPV-MPC 神经调度接口，
在低置信度或边界工况下平滑融合神经网络输出和安全调度量，改善路径跟踪平滑性与闭环稳定性。
```

---

## 20. Codex 硬性停止条件

遇到以下情况必须停止并生成 failure report：

```text
1. 当前数据链不是 22D；
2. 当前 seq_len 不是 128，但脚本仍声称复现 baseline；
3. 新实验覆盖了 baseline 目录；
4. 新实验覆盖了 previous ablation 目录；
5. 新 model_family 修改了 small 默认行为；
6. generated MATLAB layers 覆盖默认 namespace；
7. 未通过离线 gate 却写入正式闭环 compare 目录；
8. confidence scheduling sandbox 被误写为正式结果；
9. feature group index 与 22D feature_names 不一致；
10. 训练结果没有保存 config / git hash / dataset contract。
```

failure report 路径：

```text
results/modern_tcn_sci_innovation/<phase>/failure_report.md
```

---

## 21. 最简执行摘要

Codex 应按以下顺序执行：

```text
1. 锁定当前 22D ModernTCN_small baseline；
2. 跑 uncertainty weighting 和 GradNorm；
3. 跑 transition/stall focal + theta smoothness；
4. 构建 AGV physics-group residual gate；
5. 构建 mode-conditioned theta experts；
6. 构建 confidence-aware scheduling filter；
7. 通过离线 gate 后再进入 ONNX/MATLAB/闭环；
8. 根据结果决定 SCI 主方法；
9. 所有失败结果保留为负结果，不覆盖当前最优结论。
```

本轮核心思想：

```text
不再追求让模型更像官方 ModernTCN，
而是让 ModernTCN_small 更像一个服务于 AGV LPV-MPC 闭环控制的物理感知调度网络。
```
