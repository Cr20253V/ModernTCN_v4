# GRU 工况识别算法使用指南

> **版本**: V1.0  
> **最后更新**: 2025-01-XX  
> **作者**: LPV-MPC Project

本文档详细说明 GRU 工况识别算法从数据生成到在线推理的完整流程，以及各阶段关键参数的调整策略。

---

## 📋 目录

1. [算法概述](#算法概述)
2. [完整工作流程](#完整工作流程)
3. [阶段一：数据生成](#阶段一数据生成)
4. [阶段二：数据预处理](#阶段二数据预处理)
5. [阶段三：模型训练](#阶段三模型训练)
6. [阶段四：模型推理](#阶段四模型推理)
7. [阶段五：测试验证](#阶段五测试验证)
8. [关键参数影响分析](#关键参数影响分析)
9. [常见问题与解决方案](#常见问题与解决方案)
10. [快速参考](#快速参考)

---

## 算法概述

GRU 工况识别算法用于识别 AGV 的行驶工况，包括：

- **主分类**（4类）：flat（平地）、slip（打滑）、stall（堵转）、slope（坡度）
- **转弯状态**（3类）：left（左转）、straight（直行）、right（右转）
- **坡度回归**：估计坡度角 θ̂ [rad]

算法采用**多任务学习**架构，通过一个 GRU 网络同时完成三个任务，提高计算效率。

---

## 完整工作流程

### 流程图

```
┌─────────────────────────────────────────────────────────────┐
│  阶段一：数据生成 (GRU_gen_train_data.m)                    │
│  └─> GRU_train_data_full.mat                                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  阶段二：数据预处理 (GRU_prepare_dataset.m)                 │
│  └─> GRU_dataset_processed.mat + GRU_scaler.mat            │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  阶段三：模型训练 (GRU_train.m)                              │
│  └─> GRU_model.mat + GRU_meta.mat + GRU_logs/             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  阶段四：在线推理                                            │
│  ├─ GRU_infer.m (单步推理)                                  │
│  └─ GRU_state_classifier.m (在线封装)                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  阶段五：测试验证 (test_GRU_workflow.m)                      │
│  └─> 测试报告和可视化                                        │
└─────────────────────────────────────────────────────────────┘
```

### 典型工作流

#### 首次训练
1. 运行 `GRU_gen_train_data.m` → 生成原始数据
2. 运行 `GRU_prepare_dataset.m` → 预处理数据
3. 运行 `GRU_train.m` → 训练模型
4. 运行 `test_GRU_workflow.m` → 验证模型

#### 在线部署
1. 在 Simulink 中加载 `GRU_model.mat` 和 `parameters.m`
2. `GRU_State_Classifier` 模块调用 `GRU_state_classifier.m`
3. 模块内部调用 `GRU_infer.m` 进行推理

---

## 阶段一：数据生成

### 执行脚本
**`GRU_gen_train_data.m`**

### 功能说明
- 通过调用 Simulink 模型 `GRU_DataGen.slx` 生成高保真训练数据
- 支持路径参数随机化（域随机化）
- 支持打滑/堵转注入（通过 InjectionWrapper）
- 自动标注（label_main, label_turn, theta）

### 依赖文件
- `parameters.m`（系统参数）
- `gen_agv_ref_path.m`（参考路径生成）
- `GRU_DataGen.slx`（Simulink 仿真模型）

### 生成文件
**`GRU_train_data_full.mat`**
```
data
├── runs(k): 每回合数据
│   ├── .t [N×1]: 时间向量 [s]
│   ├── .u [N×2]: 控制输入 [F_cmd, omega_cmd]
│   ├── .y_raw [N×31]: 原始输出（含传感器数据）
│   ├── .label_main [N×1]: 主分类 {1,2,3,4}
│   ├── .label_turn [N×1]: 转弯状态 {-1,0,+1}
│   ├── .theta [N×1]: 坡度角真值 [rad]
│   └── .meta: 元数据（参数、种子、注入窗口）
└── .meta: 全局元数据
```

### 关键参数

#### 数据规模参数
| 参数 | 默认值 | 说明 | 影响 |
|------|--------|------|------|
| `cfg.num_runs` | 150 | 每场景回合数 | 增大→数据量↑，训练更充分，但生成时间↑ |
| `cfg.T_end` | 20 s | 每回合仿真时长 | 增大→单回合样本↑，覆盖更长时序 |
| `cfg.Ts` | 0.05 s | 采样周期 | 需与系统参数一致 |

#### 场景配置
| 参数 | 默认值 | 说明 | 影响 |
|------|--------|------|------|
| `cfg.scenes` | `{'straight', 'turn_left', 'turn_right', 'straight_turn', 'slope', 'bumpy'}` | 场景列表 | 覆盖不全→模型无法识别未训练场景 |

#### 域随机化参数
| 参数 | 默认值 | 说明 | 影响 |
|------|--------|------|------|
| `cfg.path_rand.v0_range` | [0.8, 1.2] m/s | 初速度范围 | 范围大→泛化更好，但可能引入异常样本 |
| `cfg.path_rand.R_range` | [8, 12] m | 转弯半径范围 | 影响转弯场景多样性 |
| `cfg.path_rand.theta_slope_range` | [-10, 10] deg | 坡度角范围 | 范围大→覆盖更广坡度 |

#### 打滑注入参数
| 参数 | 默认值 | 说明 | 影响 |
|------|--------|------|------|
| `cfg.slip_cfg.prob` | 0.70 | 打滑概率 | 增大→slip样本↑，但可能过度 |
| `cfg.slip_cfg.gamma_range` | [0.3, 0.7] | 牵引系数范围 | 范围大→打滑强度变化大 |
| `cfg.slip_cfg.duration_range` | [2, 4] s | 持续时间范围 | 影响打滑事件的时序特征 |

#### 堵转注入参数
| 参数 | 默认值 | 说明 | 影响 |
|------|--------|------|------|
| `cfg.stall_cfg.prob` | 0.40 | 堵转概率 | 增大→stall样本↑ |
| `cfg.stall_cfg.load_range` | [200, 300] N | 外部负载范围 | 影响堵转强度 |

### 使用示例
```matlab
% 修改配置区域
cfg.num_runs = 150;          % 每场景150次
cfg.scenes = {'straight', 'turn_left', 'turn_right', 'straight_turn', 'slope', 'bumpy'};
cfg.slip_cfg.prob = 0.70;   % 打滑概率
cfg.stall_cfg.prob = 0.40;  % 堵转概率

% 运行脚本
GRU_gen_train_data;
```

---

### 执行脚本
- **`test_GRU_workflow.m`**：快速 sanity check，复用旧流程。
- **`test_gru_performance.m`**：离线+在线指标一体化脚本，记录混淆矩阵、θ̂ MAE、坡度识别延迟、run 级别准确率等，结果保存到 `GRU_logs/eval_reports/`。
- **`test_closed_loop_performance.m`**：批量 Simulink 仿真，统计速度跟踪、姿态误差、F_cmd 饱和比例及 slope 延迟，结果保存到 `GRU_logs/closed_loop_eval/`。

### 功能说明
1. **test_GRU_workflow**：检查依赖 → 运行单步/在线推理 → 输出示意图，适合 smoke test。
2. **test_gru_performance**：
   - 加载数据集切分（Train/Val/Test）并运行 GRU_infer，输出准确率、精确率/召回率、混淆矩阵、坡度 MAE。
   - 按 run 数据（`GRU_train_data_full.mat`）进行真实在线推理，评估驻留后的分类率、坡度延迟，并自动绘图。
   - 统一保存 `split_<name>_metrics.mat`、`online_eval_<scene>.png` 及 `GRU_eval_summary_<timestamp>.mat`。
3. **test_closed_loop_performance**：
   - 自动加载 `path_*.mat` 参考轨迹并推送至基础工作区，调用 `LPVMPC_AGV_simulink` 批量仿真。
   - 默认监控信号 `diag.*`（速度、姿态、theta_hat、label_main、F_cmd 等），计算 RMS/峰值误差、steady-state 误差、坡度识别延迟与命令饱和比例。
   - 支持通过 `cfg.scenarios` 传入自定义路径或结构体（含 `path_file`, `name`, `stop_time`），输出 `timeseries_<scene>.mat` 与 `closed_loop_summary_<tag>.mat`。

### 依赖文件
- `GRU_model.mat`
- `GRU_dataset_processed.mat`
- `GRU_train_data_full.mat`
- `GRU_infer.m`
- `GRU_state_classifier.m`
- `LPVMPC_AGV_simulink.slx` 及其 `diag.*` 日志信号
- `parameters.m`

### 生成文件
- `GRU_logs/test_online_inference.png`
- `GRU_logs/eval_reports/split_<name>_metrics.mat`
- `GRU_logs/eval_reports/online_eval_<scene>.png`
- `GRU_logs/eval_reports/GRU_eval_summary_<timestamp>.mat`
- `GRU_logs/closed_loop_eval/timeseries_<scene>.mat`
- `GRU_logs/closed_loop_eval/closed_loop_summary_<tag>.mat`

### 使用示例
```matlab
% 基础工作流（快速检查）
├── .mask_theta_train/val/test [N×1]: slope样本掩码

% GRU 性能评估（指定 run 索引、关闭绘图）
├── .scaler: 归一化统计量（mean, std）
├── .feat_names: 特征名称列表

% 闭环评估（仅平路+坡度，仿真 25 s）
└── .meta: 元数据
```
```

**`GRU_scaler.mat`**
```
scaler
├── .mean [1×feat_dim]: 均值
├── .std [1×feat_dim]: 标准差
├── .tau_diff: 速度差分滤波参数
└── .tau_accel_lp: 加速度低通滤波参数
```

### 关键参数

#### 序列参数
| 参数 | 默认值 | 说明 | 影响 |
|------|--------|------|------|
| `cfg.seq_len` | 48 | 序列长度（≈2.4s） | 增大→捕获更长依赖，但计算量↑ |
| `cfg.stride` | 12 | 滑窗步长（≈0.6s间隔） | 增大→样本数↓，重叠少 |

#### 数据分割
| 参数 | 默认值 | 说明 | 影响 |
|------|--------|------|------|
| `cfg.train_ratio` | 0.7 | 训练集比例 | 增大→训练数据↑，但验证/测试数据↓ |
| `cfg.val_ratio` | 0.15 | 验证集比例 | 用于早停和超参调优 |
| `cfg.test_ratio` | 0.15 | 测试集比例 | 用于最终评估 |

#### 特征滤波参数
| 参数 | 默认值 | 说明 | 影响 |
|------|--------|------|------|
| `cfg.tau_accel_lp` | 0.4 s | 加速度低通滤波时间常数 | 增大→平滑更强，但可能丢失快速变化 |
| `cfg.tau_diff` | 0.3 s | 速度差分滤波时间常数 | 影响dv_hat_dt的平滑度 |

### 使用示例
```matlab
% 修改配置区域
cfg.seq_len = 48;           % 序列长度
cfg.stride = 12;             % 滑窗步长
cfg.train_ratio = 0.7;       % 训练集比例
cfg.tau_accel_lp = 0.4;      % 加速度滤波时间常数

% 运行脚本
GRU_prepare_dataset;
```

---

## 阶段三：模型训练

### 执行脚本
**`GRU_train.m`**

### 功能说明
1. 加载预处理数据集（`GRU_dataset_processed.mat`）
2. 构建三头 GRU 网络
   - GRU 特征提取层（2层，hidden=96, dropout=0.2）
   - 主分类头（Dense(4) + softmax）
   - 转弯分类头（Dense(3) + softmax）
   - 坡度回归头（Dense(1)）
3. 自定义训练循环
   - 混合损失：L = CE_main(加权) + λ_turn·CE_turn + λ_theta·MSE_theta·mask_theta
   - 类别权重平衡（按类频次反比）
   - 梯度裁剪（阈值=5.0）
   - 学习率调度（cosine/step）
   - 早停（patience=20）
4. 保存模型和元数据

### 依赖文件
- `GRU_dataset_processed.mat`（阶段二产物）
- Deep Learning Toolbox（MATLAB R2024b+）

### 生成文件
**`GRU_model.mat`**
```
model
├── .net_feature: GRU特征提取网络（dlnetwork）
├── .fc_main_weights/bias: 主分类头权重/偏置
├── .fc_turn_weights/bias: 转弯分类头权重/偏置
├── .fc_theta_weights/bias: 坡度回归头权重/偏置
├── .scaler: 归一化参数（从dataset复制）
├── .class_labels_main: 主分类标签名称
├── .class_labels_turn: 转弯标签名称
└── .seq_len: 序列长度
```

**`GRU_meta.mat`**
```
meta
├── .hyperparams: 超参数配置
├── .train_history: 训练历史（loss, acc等）
├── .best_epoch: 最佳轮次
└── .metrics: 评估指标
```

**`GRU_logs/`**（目录）
- `training_curves.png`: 训练曲线图
- 其他日志文件

### 关键参数

#### 模型架构参数
| 参数 | 默认值 | 说明 | 影响 |
|------|--------|------|------|
| `cfg.hidden_size` | 96 | GRU隐藏层大小 | 增大→容量↑，但可能过拟合，计算量↑ |
| `cfg.num_layers` | 2 | GRU层数 | 增大→表达能力↑，但训练难、易过拟合 |
| `cfg.dropout` | 0.2 | Dropout概率 | 增大→正则化↑，但可能欠拟合 |

#### 训练超参数
| 参数 | 默认值 | 说明 | 影响 |
|------|--------|------|------|
| `cfg.batch_size` | 64 | 批量大小 | 增大→训练稳定，但内存占用↑，可能泛化差 |
| `cfg.max_epochs` | 150 | 最大训练轮数 | 增大→训练充分，但可能过拟合 |
| `cfg.initial_lr` | 1e-3 | 初始学习率 | 过大→训练不稳定；过小→收敛慢 |
| `cfg.lr_schedule` | 'cosine' | 学习率调度策略 | 'cosine'→平滑衰减；'step'→阶梯衰减 |

#### 损失函数权重
| 参数 | 默认值 | 说明 | 影响 |
|------|--------|------|------|
| `cfg.lambda_turn` | 0.3 | 转弯分类损失权重 | 增大→更关注转弯分类，可能影响主分类 |
| `cfg.lambda_theta` | 0.5 | 坡度回归损失权重 | 增大→更关注坡度回归，可能影响分类 |

#### 正则化参数
| 参数 | 默认值 | 说明 | 影响 |
|------|--------|------|------|
| `cfg.grad_clip` | 5.0 | 梯度裁剪阈值 | 增大→允许更大梯度，可能不稳定 |
| `cfg.patience` | 20 | 早停耐心值 | 增大→允许更多无改善轮次，可能过拟合 |

#### 类别平衡参数
| 参数 | 默认值 | 说明 | 影响 |
|------|--------|------|------|
| `cfg.use_class_weights` | true | 是否使用类别权重 | 开启→平衡类别，提升少数类性能 |
| `cfg.class_weight_method` | 'custom' | 类别权重计算方法 | 不同方法对类别平衡效果不同 |

### 使用示例
```matlab
% 修改配置区域
cfg.hidden_size = 96;        % GRU隐藏层大小
cfg.num_layers = 2;          % GRU层数
cfg.batch_size = 64;         % 批量大小
cfg.max_epochs = 150;        % 最大训练轮数
cfg.initial_lr = 1e-3;       % 初始学习率
cfg.lambda_turn = 0.3;      % 转弯分类损失权重
cfg.lambda_theta = 0.5;     % 坡度回归损失权重

% 运行脚本
GRU_train;
```

---

## 阶段四：模型推理

### 4.1 单步推理接口

#### 执行脚本
**`GRU_infer.m`**

#### 功能说明
- 输入：归一化序列 [seq_len, feat_dim]
- GRU 前向传播
- 三头输出：label_main, label_turn, theta_hat
- 置信度输出

#### 依赖文件
- `GRU_model.mat`（阶段三产物）

#### 使用示例
```matlab
load('GRU_model.mat', 'model');
x_seq = randn(48, 17);  % [seq_len, feat_dim]，已归一化
[label_main, label_turn, theta_hat, conf] = GRU_infer(x_seq, model);
```

---

### 4.2 在线推理封装（Simulink集成）

#### 执行脚本
**`GRU_state_classifier.m`**

#### 功能说明
提供序列缓冲、最小驻留时间、低通滤波等功能，适用于 Simulink 在线推理。

**初始化模式**：`'init'`
- 初始化状态（序列缓冲、滤波参数等）

**更新模式**：`'update'`
1. 特征提取（从 y_raw [31×1] 提取 17 维特征）
2. 序列缓冲（FIFO，维护 seq_len 长度）
3. 归一化（使用 model.scaler）
4. 调用 GRU_infer 推理
5. 最小驻留时间处理（主分类 0.20s，转弯 0.40s）
6. theta_hat 低通滤波（tau=0.15s）
7. 条件处理（V1.3 新增）
   - 非 slope 场景：强制 theta_hat=0
   - slope 场景：死区处理（阈值 0.02 rad）

#### 依赖文件
- `GRU_infer.m`（单步推理接口）
- `GRU_model.mat`（阶段三产物）
- `parameters.m`

#### 关键参数

| 参数 | 默认值 | 说明 | 影响 |
|------|--------|------|------|
| `state.seq_len` | 48 | 序列长度 | 需与训练时一致，否则性能下降 |
| `state.dwell_main` | 0.20 s | 主分类驻留时间 | 增大→更稳定，但响应慢 |
| `state.dwell_turn` | 0.40 s | 转弯状态驻留时间 | 增大→更稳定，但响应慢 |
| `state.tau_theta` | 0.15 s | theta_hat 低通滤波时间常数 | 增大→更平滑，但响应慢 |
| `state.theta_deadzone` | 0.02 rad | theta_hat 死区阈值 | 增大→消除更多小波动，但可能丢失小坡度 |
| `state.tau_diff` | 0.3 s | 速度差分滤波 | 需与预处理一致 |
| `state.tau_accel_lp` | 0.4 s | 加速度低通滤波 | 需与预处理一致 |

#### 使用示例
```matlab
% 初始化
params = parameters();
load('GRU_model.mat', 'model');
state = GRU_state_classifier('init', params, model);

% 在线循环
for t = 1:N
    y_raw_t = output_eq(x, u, theta, params);  % [31×1]
    [state, out] = GRU_state_classifier('update', state, y_raw_t);
    fprintf('t=%.2f: %s, %s, θ=%.2f°\n', ...
        t*params.Ts, out.label_main_name, out.label_turn_name, rad2deg(out.theta_hat));
end
```

---

## 阶段五：测试验证

### 执行脚本
**`test_GRU_workflow.m`**

### 功能说明
1. 检查依赖文件
2. 加载模型和数据集
3. 测试单步推理（GRU_infer）
4. 测试在线推理（GRU_state_classifier）
5. 可视化结果

### 依赖文件
- `GRU_model.mat`
- `GRU_dataset_processed.mat`
- `GRU_infer.m`
- `GRU_state_classifier.m`
- `parameters.m`

### 生成文件
- `GRU_logs/test_online_inference.png`（可视化结果）

### 使用示例
```matlab
% 直接运行
test_GRU_workflow;
```

---

## 关键参数影响分析

### 参数调整优先级

#### 数据生成阶段
- **优先调整**：`num_runs`（数据量）、`slip_cfg.prob`、`stall_cfg.prob`（类别平衡）
- **次要调整**：域随机化范围（泛化能力）

#### 数据预处理阶段
- **优先调整**：`seq_len`（时序建模能力）、`stride`（样本数量）
- **次要调整**：滤波参数（特征质量）

#### 模型训练阶段
- **优先调整**：`hidden_size`、`batch_size`、`initial_lr`（训练效果）
- **次要调整**：损失权重、早停参数（多任务平衡）

#### 在线推理阶段
- **优先调整**：驻留时间、滤波参数（稳定性与响应速度）
- **次要调整**：死区阈值（消除波动）

### 参数联动关系

1. **序列长度一致性**：训练时的 `seq_len` 必须与在线推理时的 `state.seq_len` 一致
2. **滤波参数一致性**：预处理时的 `tau_accel_lp`、`tau_diff` 必须与在线推理时一致
3. **归一化一致性**：在线推理必须使用训练时的 `scaler` 进行归一化

---

## 常见问题与解决方案

### 问题1：模型在 slip/stall 场景识别率低

**原因**：少数类样本不足

**解决方案**：
- 增大 `cfg.slip_cfg.prob`（如 0.5→0.7）
- 增大 `cfg.stall_cfg.prob`（如 0.2→0.4）
- 增大 `cfg.num_runs`（如 100→150）
- 使用类别权重平衡（`cfg.use_class_weights = true`）

---

### 问题2：模型过拟合

**原因**：模型容量过大或训练轮数过多

**解决方案**：
- 增大 `cfg.dropout`（如 0.2→0.3）
- 减小 `cfg.hidden_size`（如 96→64）
- 减小 `cfg.num_layers`（如 2→1）
- 增大 `cfg.patience` 配合早停

---

### 问题3：在线推理抖动

**原因**：驻留时间过短或滤波不足

**解决方案**：
- 增大 `state.dwell_main`（如 0.20→0.30s）
- 增大 `state.dwell_turn`（如 0.40→0.45s）
- 增大 `state.tau_theta`（如 0.15→0.20s）
- 增大 `state.theta_deadzone`（如 0.01→0.02 rad）

---

### 问题4：响应速度慢

**原因**：驻留时间或滤波时间常数过大

**解决方案**：
- 减小驻留时间（需平衡稳定性）
- 减小 `state.tau_theta`（需平衡平滑度）
- **注意**：响应速度与稳定性是权衡关系，需根据实际需求调整

---

### 问题5：坡度估计不准

**原因**：损失权重不平衡或训练数据覆盖不足

**解决方案**：
- 增大 `cfg.lambda_theta`（如 0.3→0.5）
- 检查训练数据中 slope 场景的覆盖范围
- 检查特征滤波参数是否一致（预处理与在线推理）

---

### 问题6：平地场景 theta_hat 波动

**原因**：GRU 在非 slope 场景下仍输出非零值

**解决方案**：
- 已在 V1.3 版本中修复：非 slope 场景强制 theta_hat=0
- 如仍有波动，可增大 `state.theta_deadzone`

---

## 快速参考

### 文件清单

| 文件 | 阶段 | 作用 |
|------|------|------|
| `GRU_gen_train_data.m` | 数据生成 | 生成原始训练数据 |
| `GRU_prepare_dataset.m` | 数据预处理 | 预处理和切片 |
| `GRU_train.m` | 模型训练 | 训练 GRU 模型 |
| `GRU_infer.m` | 推理 | 单步推理接口 |
| `GRU_state_classifier.m` | 推理 | 在线推理封装 |
| `test_GRU_workflow.m` | 测试 | 快速端到端检查 |
| `test_gru_performance.m` | 测试 | 离线/在线指标评估、run 级别对比 |
| `test_closed_loop_performance.m` | 测试 | Simulink 闭环批量评估 |

### 产物文件清单

| 文件 | 阶段 | 内容 |
|------|------|------|
| `GRU_train_data_full.mat` | 数据生成 | 原始训练数据 |
| `GRU_dataset_processed.mat` | 数据预处理 | 预处理后的数据集 |
| `GRU_scaler.mat` | 数据预处理 | 归一化参数 |
| `GRU_model.mat` | 模型训练 | 训练好的模型 |
| `GRU_meta.mat` | 模型训练 | 训练元数据 |
| `GRU_logs/` | 模型训练 | 训练日志和可视化 |
| `GRU_logs/eval_reports/` | 测试 | GRU 指标报告、在线截图 |
| `GRU_logs/closed_loop_eval/` | 测试 | 闭环仿真结果、summary |

### 典型参数配置

#### 快速测试配置
```matlab
% 数据生成
cfg.num_runs = 1;
cfg.scenes = {'straight'};

% 数据预处理
cfg.seq_len = 48;
cfg.stride = 12;

% 模型训练
cfg.max_epochs = 10;
cfg.batch_size = 32;
```

#### 完整训练配置
```matlab
% 数据生成
cfg.num_runs = 150;
cfg.scenes = {'straight', 'turn_left', 'turn_right', 'straight_turn', 'slope', 'bumpy'};
cfg.slip_cfg.prob = 0.70;
cfg.stall_cfg.prob = 0.40;

% 数据预处理
cfg.seq_len = 48;
cfg.stride = 12;
cfg.train_ratio = 0.7;

% 模型训练
cfg.hidden_size = 96;
cfg.num_layers = 2;
cfg.batch_size = 64;
cfg.max_epochs = 150;
cfg.initial_lr = 1e-3;
```

#### 在线推理配置
```matlab
% 在 GRU_state_classifier.m 中
state.dwell_main = 0.20;     % 主分类驻留时间
state.dwell_turn = 0.40;     % 转弯状态驻留时间
state.tau_theta = 0.15;      % theta_hat 滤波时间常数
state.theta_deadzone = 0.02; % 死区阈值
```

---

## 版本历史

- **V1.4**（2025-11-26）：统一在线/离线驻留时间（0.20s/0.40s）与 `tau_theta=0.15s`，降低识别延时
- **V1.3**（2025-01-XX）：非 slope 场景强制 theta_hat=0，增加死区处理
- **V1.2**（2025-11-04）：恢复驻留时间至 0.4s
- **V1.1**（2025-11-01）：特征计算与离线对齐，增加 I_diff_signed 特征

---

## 相关文档

- `README_GRU_Integration.md`：GRU 与 MPC 集成说明
- `func.md`：功能导航文档
- `change.md`：变更记录

---

## 联系方式

如有问题或建议，请参考项目文档或联系开发团队。

