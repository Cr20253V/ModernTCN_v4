# Physics-Guided Multi-task TCN for AGV State Estimation and LPV-MPC Path Tracking

更新时间：2026-04-24

## 0. 当前执行决策（2026-04-28）

截至 `pg_confirm_v3`，当前形式的 physics-guided loss 已完成初版实现和多 seed 消融，但尚未稳定优于非 PG staged TCN。具体表现为：

- `lambda_phy=0.005` 对 `slope_recall` 有局部改善倾向，但对 `theta_mae_deg` 和训练稳定性存在负面影响。
- 多 seed 平均下，PG-TCN 没有超过当前 TCN 临时最优 `staged_bestbase_inputstats_turn_lam050`。
- 当前 PG 最优单次结果不足以支撑“physics-guided TCN 是主线最优模型”的论文主张。

因此当前阶段采用以下工程和论文叙事：

1. 主线模型暂定为 `multi-task staged TCN`，即当前临时最优 `staged_bestbase_inputstats_turn_lam050`。
2. `GRU` 保留为公平对照模型。
3. `physics-guided TCN` 保留为消融实验分支，不作为当前主线模型。
4. 后续若要重新把 PG 升级为主线创新点，需要重新设计 PG 约束，而不是继续扩大 `lambda_phy/lambda_smooth` 权重搜索。

当前更稳妥的论文主张应从“完整 Physics-Guided TCN 显著优于 GRU”调整为：

> A multi-task TCN state estimator with explicit temporal receptive field and MATLAB-native deployment improves the fairness and real-time feasibility of LPV-MPC state scheduling; physics-guided regularization is evaluated as an ablation and remains a candidate for future refinement.

本文档后续保留原始 PG 设计方案，作为第二阶段继续优化的技术储备；但当前实验执行应优先完成 `TCN / GRU / PG-TCN ablation` 的固定对照和闭环验证。

## 1. 研究定位

本方向建议将 Mamba2 分支替换为 TCN 分支，形成：

- LPV-MPC + Multi-task staged TCN
- LPV-MPC + Physics-Guided TCN ablation
- LPV-MPC + GRU
- LPV-MPC + IMU

TCN 不直接替代 LPV-MPC 的预测模型，而是替代当前 GRU/Mamba2 所处的“工况/状态估计器”位置。其输入为 AGV 行驶过程中的传感器与派生特征窗口，输出为：

- 主工况：`label_main in {flat, stall, slope}`
- 转弯状态：`label_turn in {right, straight, left}`
- 坡度估计：`theta_hat`

这些输出继续进入现有 LPV-MPC 调度链路，用于更新 `rho = [v, omega, theta]` 及相关权重/约束映射。论文主问题应写成：

> A temporal convolutional multi-task state estimator improves LPV-MPC path tracking robustness and real-time feasibility for AGVs under slope, turn, and disturbance conditions.

不要把论文主张写成“TCN 理论上优于 GRU”。更稳妥的表述是：在当前 AGV 闭环控制架构中，TCN 的有限感受野、并行推理、稳定梯度路径和 MATLAB 原生部署路径，使其更适合高频窗口估计和 LPV-MPC 在线调度。物理一致性正则目前只作为消融分支报告，不作为主线性能结论。

## 2. TCN 相较于 GRU 的优势

### 2.1 固定感受野更适合当前窗口估计任务

当前 GRU 通过循环状态逐步读取长度为 `seq_len=128` 的窗口，最后取末端隐状态做预测。TCN 通过膨胀因果卷积定义明确的历史感受野：

```text
R = 1 + (k - 1) * sum(d_i)
```

其中 `k` 是卷积核长度，`d_i` 是第 `i` 个卷积块的 dilation。若使用 `k=3`、dilation 为 `[1, 2, 4, 8, 16, 32]`，感受野为 `127` 个采样点，约等于 `1.27 s`，与当前 `seq_len=128` 几乎对齐。

这带来两个优势：

1. 论文上可以明确说明模型只利用最近约 1.28 s 的可观测历史，避免“隐式记忆长度不清楚”的问题。
2. 工程上可以把窗口长度、感受野、采样周期三者绑定，便于解释实时估计延迟。

### 2.2 并行计算路径更适合 MATLAB/Simulink 部署

GRU 的时间维计算天然串行，窗口长度越长，推理路径越长。TCN 的 1-D 卷积可在时间维并行计算，即使在 MATLAB Deep Learning Toolbox 中也更容易利用向量化和 GPU 加速。

在当前项目中，这一点很关键：

- GRU 分支已经能 MATLAB 原生运行，TCN 可以沿用 `dlnetwork` 工作流。
- Mamba2 分支依赖 Python/TCP/CPU fallback，部署复杂度较高。
- TCN 可以直接构建 MATLAB 原生模型，减少跨语言接口对实时性统计的污染。

### 2.3 梯度路径更稳定，适合多任务头

GRU 需要通过时间递归传播梯度，长窗口下仍可能受梯度衰减、门控饱和影响。TCN 的残差膨胀卷积块使梯度通过残差路径直接回传，训练更稳定，尤其适合同时学习分类头和回归头：

```text
shared TCN encoder
  -> main-state classification head
  -> turn-state classification head
  -> slope regression head
```

对当前任务而言，分类与回归共享的是同一组短时动力学线索：加速度、轮速、电流、横摆角速度、转向角、俯仰角速度及其派生量。TCN 的局部卷积滤波天然适合提取这些短时变化模式。

### 2.4 更容易加入物理一致性约束

TCN 本身是数据驱动模型，但其输出可被物理残差约束。相比 GRU，TCN 的窗口输出更稳定、感受野更明确，因此适合在训练损失中加入弱物理先验：

- 平地 `theta_hat` 应接近 0。
- 坡道中 `theta_hat` 与纵向加速度、电流/驱动力、速度变化率之间应满足方向一致性。
- 转弯状态与 `gyro_z`、`kappa_proxy` 的符号应一致。
- 工况切换不应出现高频抖动，可加入时间平滑或驻留一致性损失。

这使论文从“换一个网络”升级为“物理引导的闭环状态估计器”。

## 3. 如何调整现有流程以凸显 TCN 优势

### 3.1 数据集生成：必须增加动态过渡样本

当前数据流程已经能支持 `flat/stall/slope`、`turn`、`theta_hat` 多任务训练，但若要凸显 TCN，需要让训练和测试集中包含更多短时动态过渡段，而不是只有稳态段。

建议在数据生成或路径选择中强化以下片段：

1. 平地到坡道、坡道到平地的过渡段。
2. 直行到转弯、转弯到直行的过渡段。
3. 轻扰动到强扰动的变化段。
4. 堵转注入开始和恢复阶段。
5. 坡道与转弯叠加，即“坡道转弯”或“转弯后接坡道”。

原因：TCN 的优势不是记住很长历史，而是识别局部时间模式。若数据只有长稳态区，GRU 和 TCN 都容易得到类似结果，优势难以显现。

### 3.2 路径设计：建议新增挑战路径

路径设计必须区分“训练阶段”和“成果展示阶段”。训练阶段的目标是高密度覆盖局部动态模式，成果展示阶段的目标是给论文提供整段工业路径的可视化跟踪结果。不要再把单条 150 s 长路径作为主要训练模板。

训练阶段建议以大量 `15-40 s` 短片段为主，每段包含 1-4 个明确事件，例如：

- 平地直行 -> 坡道 -> 平地恢复。
- 直行 -> 左转/右转 -> 直行恢复。
- 平地 -> S 弯 -> 扰动 -> 恢复。
- 坡道 -> 转弯 -> 坡道退出。
- 堵转注入 -> 堵转恢复。

原因：TCN 的优势是有限感受野内的局部动态识别。若训练数据主要来自一条 120-150 s 长路径，稳态样本会占据主要比例，过渡样本稀疏，GRU 和 TCN 的差异很难在闭环指标中体现。

建议将路径分为三类：

1. 基础短片段，`12-20 s`：单一工况学习，如直线、单左转、单右转、单坡道、单扰动。
2. 组合短片段，`20-40 s`：多事件组合，如直行-转弯-坡道-恢复。
3. 长验证/展示路径，`90-150 s`：用于论文成果图，不作为主要训练来源。

短路径参数建议采用“工业合理为主、边界挑战为辅”的比例：

```text
70% 工业合理范围
20% 边界但仍物理合理
10% 极端挑战样本
```

推荐参数范围：

- 速度：主范围 `0.6-1.5 m/s`，少量挑战到 `1.8 m/s`。
- 转弯半径：主范围 `6-20 m`，挑战样本 `4-6 m`。
- 坡度：主范围 `2-6 deg`，挑战样本到 `8 deg` 左右。
- 坡度过渡时间：主范围 `1.0-3.0 s`，挑战样本 `0.5-1.0 s`。
- 扰动强度：训练中以轻中等扰动为主，强扰动更多用于鲁棒性测试。

路径参数可以更丰富，但不能脱离物理可信度。过于夸张的路径会使模型学习仿真器特征，而不是工业 AGV 的真实动态模式。

现有路径可以保留，但建议新增或组合以下路径用于 TCN 论文实验：

- `path_slope_turn.mat`：坡道 + 转弯组合。
- `path_slope_s_curve.mat`：坡道 + S 弯组合。
- `path_disturbance_transition.mat`：平地、坡道、扰动、恢复按时间段切换。
- `path_industrial_challenge.mat`：工业路径中加入连续曲率变化、坡度变化和速度变化。

这些路径不应只用于训练，也要作为未见测试路径的一部分。论文中可以把结果分为：

- in-distribution scenarios：训练中见过类型的路径。
- transition-rich scenarios：过渡丰富路径。
- out-of-distribution scenarios：未见组合路径。

TCN 的优势重点应在后两类场景中体现。

成果展示阶段建议使用一条 `90-150 s` 的整段长路径。该路径应是测试路径，而不是训练主路径。建议包含：

```text
平地直行
左转/右转
S 弯
坡道上行
坡道中转弯
扰动段
恢复段
长直道稳定段
```

论文主图可展示整段 XY 轨迹跟踪，并配合局部放大图展示坡道、转弯和扰动过渡段。

### 3.2.1 采样周期与窗口长度建议

当前工程全部路径均为 `Ts=0.01 s`，现有 LPV 数据库、MPC、GRU 和对比脚本也围绕该采样周期建立。为了降低第一版落地风险，建议分阶段处理：

第一阶段，工程落地与公平对比：

```text
Ts = 0.01 s
seq_len = 128
窗口物理长度 = 1.28 s
训练路径长度 = 15-40 s
成果展示路径长度 = 90-150 s
```

该阶段最大限度复用现有 `parameters.m`、LPV 数据库、GRU 对照和 Simulink 模型，优先验证 TCN 链路是否成立。

第二阶段，论文工业化版本：

```text
Ts = 0.02 s
seq_len = 64
窗口物理长度 = 1.28 s
训练路径长度 = 20-40 s
成果展示路径长度 = 90-150 s
```

`Ts=0.02 s` 更接近工业 AGV 路径跟踪控制频率，同时保持与第一阶段相同的物理窗口长度。若采用该阶段，需要同步重建或复核 LPV 数据库、MPC 参数、GRU/TCN 数据集和公平对比基线。

不建议将 `Ts=0.05 s` 作为主实验采样周期。20 Hz 对常规路径跟踪可能足够，但对本文关注的短时状态识别、坡度过渡和堵转/扰动检测偏粗，容易削弱 TCN 的局部动态建模优势。

### 3.3 训练数据切分：必须按 run-level 划分

继续使用按回合划分，不能把同一回合的相邻窗口同时放入训练和测试。否则 TCN 的局部模式识别能力会被数据泄漏放大，论文结论不可信。

建议固定：

- `seq_len = 128`
- `stride = 64` 作为主实验
- 另做 `seq_len = 64 / 128 / 256` 的消融实验

消融实验的目的不是找最好看的结果，而是证明感受野长度与控制性能之间存在合理关系。

### 3.4 对比流程：不要只比较离线准确率

离线分类准确率只能作为辅助指标。主结论必须来自闭环路径跟踪：

- `ey_rmse`
- `epsi_rmse`
- `ev_rmse`
- `eomega_rmse`
- `j_du`
- `viol_rate`
- `realtime_p50_ms / p95_ms / timeout_rate`

TCN 相对 GRU 的优势应至少在以下一种组合中成立：

1. 跟踪误差下降，控制平滑性不劣化。
2. 跟踪误差相近，但推理时间更低，超时率更低。
3. 常规路径相近，但强扰动/过渡路径显著更稳。

### 3.5 公平性约束

TCN 与 GRU 对比时必须保持：

- 同一训练母集。
- 同一 run-level split。
- 同一输入特征集合。
- 同一输出标签定义。
- 同一 `seq_len` 和 `stride`，除非做显式消融。
- 同一 LPV-MPC 参数、约束、路径、扰动和随机种子。
- 同一在线后处理策略，或明确报告差异。

如果 TCN 使用物理约束损失，建议同时训练一个 `vanilla TCN` 作为消融基线：

- GRU
- vanilla TCN
- physics-guided TCN
- IMU

若保留 Mamba2，也可作为额外对照，但不建议让 Mamba2 成为主叙事。

## 4. 可立足创新点

### 创新点 1：面向 LPV-MPC 调度的多任务 TCN 状态估计器

核心主张：

> 提出一种面向 AGV LPV-MPC 在线调度的多任务 TCN 状态估计器，同时估计行驶主工况、转弯状态和坡度角；物理一致性损失作为可选正则项进行消融验证。

理论支持：

1. LPV-MPC 的调度变量 `rho = [v, omega, theta]` 对模型插值和权重更新敏感。若 `theta_hat` 或工况标签抖动，会导致 `mpc_update_from_rho` 产生频繁模型/权重切换，进而增加 `j_du` 或约束违反风险。
2. TCN 的有限感受野与残差膨胀卷积可稳定提取局部动力学特征，适合估计当前时刻调度变量。
3. 物理一致性损失理论上能把纯数据拟合限制在可解释的物理区域内，但当前初版实验未证明其稳定优于非 PG staged TCN，因此只作为消融结果报告。

建议损失函数形式：

```text
L = L_main
  + lambda_turn  * L_turn
  + lambda_theta * L_theta
  + lambda_flat  * L_theta_flat
  + lambda_phy   * L_phy
  + lambda_smooth * L_smooth
```

其中：

- `L_theta_flat`：平地样本上约束 `theta_hat -> 0`。
- `L_phy`：坡度、电流/驱动力、纵向加速度、速度变化率之间的方向一致性。
- `L_smooth`：限制 `theta_hat` 和标签概率的高频抖动。

需要特别注意：

- 物理约束不能使用在线不可观测或泄漏标签的信息。
- 物理约束应作为软约束，不应压过监督损失。
- 必须做 `vanilla TCN` vs `physics-guided TCN` 消融，否则创新点无法被实验验证。
- 当前 `pg_confirm_v3` 的执行结论是：PG-TCN 不作为主线模型，保留为 ablation branch。

### 创新点 2：感受野可控的短时动态估计与闭环控制性能关联

核心主张：

> 建立 TCN 感受野长度与 AGV 闭环路径跟踪性能之间的实验关联，证明有限历史窗口对高频 LPV-MPC 调度具有更好的实时性和稳定性折中。

理论支持：

1. AGV 当前工况估计主要依赖最近一段传感器历史，而不是无限长历史。过短窗口无法捕捉坡度/堵转过渡；过长窗口可能引入陈旧状态，增加响应滞后。
2. TCN 的感受野由卷积核和 dilation 显式控制，可将模型记忆长度映射到物理时间，例如 `64/128/256` 点分别约为 `0.64/1.28/2.56 s`。
3. GRU 的有效记忆长度由门控状态隐式决定，难以直接解释；TCN 可把“模型看到多长历史”写成可复现实验变量。

建议消融：

- TCN-R64：约 0.64 s 感受野。
- TCN-R128：约 1.28 s 感受野。
- TCN-R256：约 2.56 s 感受野。

重点观察：

- 坡道/堵转识别延迟。
- `theta_hat` 过渡误差。
- `j_du` 是否因估计滞后或抖动升高。
- `ey_rmse` 与 `epsi_rmse` 是否随感受野存在 U 型趋势。

需要特别注意：

- 感受野消融不能改变训练集划分。
- 不同感受野模型的参数量应尽量接近，避免把“网络更大”误认为“感受野更好”。
- 论文中不要只报告离线 F1，要报告闭环性能随感受野变化的结果。

### 创新点 3：转移丰富场景下的闭环鲁棒性评估协议

核心主张：

> 构建包含坡度-转弯-扰动过渡的 AGV 闭环评估协议，用配对统计检验证明学习估计器对 LPV-MPC 的实际增益。

理论支持：

1. 控制器性能不只取决于稳态识别准确率，而取决于关键过渡时刻的估计误差和延迟。
2. MPC 调度变量在过渡段错误，会直接影响预测模型插值和输入权重，导致轨迹误差、控制抖动或约束接近饱和。
3. 配对统计设计能隔离路径、扰动、随机种子的影响，比单次曲线对比更适合论文结论。

需要特别注意：

- 保留现有 Friedman + Wilcoxon(Holm) 分析。
- 每条路径、扰动、seed 都要配对。
- 至少报告均值、标准差、中位数、四分位数、校正后 p 值和效应量。

## 5. 建议新增或修改的工程模块

### 5.1 新增 TCN 目录结构

建议在 `src/TCN` 下逐步形成：

```text
src/TCN/
  Physics_Guided_Multi_task_TCN_Implementation_Guide.md
  TCN_prepare_dataset.m
  TCN_train.m
  TCN_infer.m
  TCN_state_classifier.m
  run_TCN_prepare_dataset_compare.m
  run_TCN_train_compare.m
  summarize_tcn_results.m
```

`TCN_prepare_dataset.m` 可以先复用 GRU 数据预处理逻辑，保持输入特征、标签、切分一致。第一版不要重写所有数据生成逻辑，优先保证与 GRU 公平对比。

### 5.2 TCN 模型建议结构

建议第一版采用轻量残差 TCN：

```text
sequenceInputLayer(feat_dim)
TCN block 1: conv1d causal, dilation=1
TCN block 2: conv1d causal, dilation=2
TCN block 3: conv1d causal, dilation=4
TCN block 4: conv1d causal, dilation=8
TCN block 5: conv1d causal, dilation=16
TCN block 6: conv1d causal, dilation=32
global/last-step feature extraction
multi-task heads
```

每个 TCN block 建议包含：

- dilated causal 1-D convolution
- layer normalization 或 batch normalization
- ReLU/GELU
- dropout
- residual connection

MATLAB 中若因版本限制没有直接的 causal padding，可采用左侧 padding + 裁剪，或在自定义前向中保证不使用未来时间点。

### 5.3 在线封装

`TCN_state_classifier.m` 应尽量复刻 `GRU_state_classifier.m` 的接口：

```matlab
state = TCN_state_classifier('init', params, model);
[state, out] = TCN_state_classifier('update', state, y_raw_t);
```

输出字段保持一致：

```matlab
out.label_main
out.label_turn
out.theta_hat
out.conf_main
out.conf_turn
out.label_main_name
out.label_turn_name
out.debug
```

这样可以最大限度复用 Simulink 模型和 `src/Compare` 统计脚本。

## 6. 实施计划

### 阶段 1：冻结研究边界

1. 冻结 TCN 的任务定义：只替换状态估计器，不改 LPV-MPC 主体。
2. 冻结输入特征：第一版沿用 GRU 的 19 维特征。
3. 冻结输出标签：`label_main`、`label_turn`、`theta_hat`。
4. 冻结公平性规则：同数据、同路径、同扰动、同随机种子。

产出：

- 本指导文档。
- TCN 与 GRU 的接口契约。

### 阶段 2：数据与路径准备

1. 第一版保持 `Ts=0.01 s`，复用现有 LPV-MPC/GRU 对照链路。
2. 以 `15-40 s` 短片段为主生成训练数据，增加坡度、转弯、扰动、堵转过渡样本。
3. 新增长展示路径 `90-150 s`，仅用于成果展示和最终闭环测试，不作为训练主路径。
4. 复用现有训练母集生成 TCN 数据集，随后逐步替换为 TCN 专用短片段母集。
5. 新增过渡丰富路径，用于训练增强和闭环测试。
6. 保存 run-level split，保证 GRU/TCN 使用同一划分。
7. 检查类别分布，重点关注 `stall`、坡道过渡、左右转样本。

产出：

- `data/tcn/TCN_dataset_processed.mat`
- `data/tcn/TCN_scaler.mat`
- 过渡路径 `data/paths/path_*challenge*.mat`

### 阶段 3：模型训练与消融

1. 训练 vanilla TCN。
2. 训练 physics-guided TCN。
3. 做感受野消融：R64/R128/R256。
4. 输出离线指标：分类 F1、坡度 MAE、过渡段延迟。

产出：

- `data/models/TCN_model.mat`
- `data/models/TCN_meta.mat`
- `results/tcn/train_logs_*`

### 阶段 4：Simulink 集成

1. 新增 `TCN_state_classifier.m`。
2. 复制 GRU Simulink 分支，形成 `LPVMPC_AGV_simulink_TCN.slx`。
3. 保持日志字段与 GRU/Mamba2/IMU 一致。
4. 跑单路径冒烟测试，确认无维度、单位、延迟问题。

产出：

- `simulink/LPVMPC_AGV_simulink_TCN.slx`
- TCN 单路径闭环测试报告。

### 阶段 5：公平闭环对比

1. 扩展 `run_compare_mamba2_gru_imu_batch.m` 或新增 `run_compare_tcn_gru_imu_batch.m`。
2. 对比对象建议为 `TCN_PG / TCN_vanilla / GRU / IMU`。
3. 跑小规模矩阵验证，再跑全量矩阵。
4. 使用 Friedman + Wilcoxon(Holm) 输出统计结论。

产出：

- `results/compare/tcn_gru_imu/.../raw/case_rows.mat`
- `analysis_report.md`
- 论文图表。

### 阶段 6：论文整理

1. 写清楚 TCN 不是替代 MPC，而是服务 LPV-MPC 调度。
2. 用消融证明物理约束和感受野设计有效。
3. 用闭环指标证明控制收益，而不是只用离线准确率。
4. 报告失败场景和外推边界。

## 7. 推荐实验矩阵

最低可发表矩阵建议：

```text
controllers: IMU, GRU, vanilla TCN, physics-guided TCN
paths: short_transition_set, slope_turn, slope_s_curve, disturbance_transition, industrial_challenge
disturbance_levels: 0, 1, 2
seeds: 1:10
```

总仿真数约：

```text
4 controllers * 6-8 paths * 3 disturbances * 10 seeds = 720-960 cases
```

若加入 Mamba2 作为额外对照，则为 1050 cases。考虑 Mamba2 TCP 服务稳定性，建议先不把 Mamba2 放进主表，可作为附录或扩展对照。

论文成果展示路径单独运行，不建议纳入训练集：

```text
controllers: IMU, GRU, vanilla TCN, physics-guided TCN
path: path_industrial_showcase 或 path_industrial_challenge
T_end: 90-150 s
disturbance_levels: 1 或 2
seeds: 选 1-3 个代表性 seed
```

该阶段主要输出轨迹图、误差时间序列和局部放大图，不承担统计显著性结论。

## 8. 结果判定门槛

声明 physics-guided TCN 优于 GRU，建议同时满足：

1. `ey_rmse` 或 `epsi_rmse` 至少一项显著优于 GRU，Holm 校正后 `p < 0.05`。
2. `j_du` 不显著劣化，最好显著降低。
3. `viol_rate` 不显著劣化。
4. 推理耗时 P95 低于 GRU，或至少不高于 GRU。
5. 在过渡丰富路径中优势更明显。
6. `physics-guided TCN` 优于 `vanilla TCN`，证明创新点有效。

如果只在离线 F1 上优于 GRU，但闭环指标没有改善，不建议写成“优化路径跟踪”，只能写成“改善状态识别”。

## 9. 风险与注意事项

1. 不要修改 MPC 参数来迁就 TCN，否则对比不公平。若要调参，应对所有控制器统一调参或明确作为第二阶段实验。
2. 不要让 TCN 使用 GRU 没有的输入特征，除非开设单独实验说明信息增益。
3. 不要只选对 TCN 有利的路径。主表必须覆盖常规路径和挑战路径。
4. 不要把 Mamba2 的部署失败当作 TCN 的性能优势。TCN 的优势应来自闭环指标和实时性数据。
5. 物理损失权重需要做敏感性分析，否则可能被质疑为调参堆结果。
6. 若过渡路径由训练分布直接复制，必须在论文中说明测试路径的独立性。

## 10. 建议论文结构

1. Introduction
   - AGV 路径跟踪需要可靠的在线工况/坡度估计。
   - GRU 可用但存在串行推理、有效记忆不可解释、过渡抖动等问题。
   - 提出 physics-guided multi-task TCN。

2. System Model and LPV-MPC Framework
   - AGV 动力学、LPV 调度变量、MPC 更新机制。

3. Physics-Guided Multi-task TCN
   - 输入特征、网络结构、感受野设计、多任务头、物理损失。

4. Experimental Protocol
   - 数据生成、路径、扰动、配对统计、公平性约束。

5. Results
   - 离线估计结果。
   - 闭环路径跟踪结果。
   - 消融：vanilla vs physics-guided，感受野长度。

6. Discussion
   - 何时 TCN 优于 GRU。
   - 限制：固定采样、仿真到实车差距、极端 OOD 工况。

7. Conclusion

## 11. 一页执行清单

1. 第一版固定 `Ts=0.01 s`，不要同时改采样周期和模型结构。
2. 复用 GRU 数据预处理逻辑，生成 TCN 数据集。
3. 新增 `15-40 s` 短片段训练路径，提高过渡样本密度。
4. 单独设计 `90-150 s` 成果展示长路径，不作为训练主路径。
5. 实现 vanilla TCN 和 physics-guided TCN。
6. 保持 GRU/TCN 输入输出契约一致。
7. 新增 TCN 在线封装和 Simulink 分支。
8. 跑 `TCN_vanilla / TCN_PG / GRU / IMU` 闭环对比。
9. 做统计检验和消融分析。
10. 第二阶段再评估是否切换到 `Ts=0.02 s` 的工业化主实验。
11. 只有在闭环主指标通过门槛后，才把论文主张写成“改善 AGV path tracking”。
