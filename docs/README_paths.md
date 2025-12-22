# AGV 参考路径生成模块使用说明

## 概述
本模块提供统一接口 `gen_agv_ref_path.m`，用于生成 5 种工况的 AGV 参考轨迹数据，支持 LPV-MPC 控制器设计与仿真。

## 支持的路径类型

| 路径类型 | 说明 | 典型应用 |
|---------|------|---------|
| `'straight'` | 平地直线行驶 | 基础速度跟踪、平顺性测试 |
| `'turn'` | 恒定半径转弯 | 转向性能、横向动力学测试 |
| `'straight_turn'` | 先直线后转弯（S曲线平滑过渡） | 综合工况、切换性能测试 |
| `'slope'` | 坡度直线行驶 | 爬坡能力、载荷转移测试 |
| `'bumpy'` | 颠簸直线行驶（地面坡度扰动） | 扰动抑制、鲁棒性测试 |
| `'s_curve'` | 0–2s直行后进行左右各一次、半径固定的S弯 | 复合转向、避障路线测试 |

## 快速开始

### 1. 基本用法
```matlab
% 载入参数
params = parameters();

% 生成直线路径
ref_straight = gen_agv_ref_path('straight', params);

% 生成转弯路径
ref_turn = gen_agv_ref_path('turn', params);
```

### 2. 自定义参数
```matlab
params = parameters();

% 自定义选项
opts.T_end = 30;           % 仿真时长 30s（默认20s）
opts.R = 15;               % 转弯半径 15m（默认10m）
opts.v0 = 1.5;             % 初速度 1.5 m/s（默认1.0m/s）
opts.theta_slope = deg2rad(15);  % 坡度15°（默认5°）
opts.bumpy_amp = 0.2;       % 颠簸幅值 0.2 rad（默认0.2 rad）

% 生成路径
ref = gen_agv_ref_path('slope', params, opts);
```

### 3. 批量生成与保存
```matlab
% 运行测试脚本，生成所有路径并可视化
test_gen_paths;

% 将生成：
% - path_straight.mat
% - path_turn.mat
% - path_straight_turn.mat
% - path_slope.mat
% - path_bumpy.mat
% - path_<type>_preview.png（可视化图像）
```

## 输出结构说明

生成的 `ref` 结构体包含以下字段：

### 核心轨迹数据
| 字段 | 维度 | 单位 | 说明 |
|-----|------|-----|------|
| `t` | [N×1] | s | 时间向量 |
| `X_ref` | [N×1] | m | 全局X坐标参考 |
| `Y_ref` | [N×1] | m | 全局Y坐标参考 |
| `psi_ref` | [N×1] | rad | 航向角参考 |
| `v_ref` | [N×1] | m/s | 纵向速度参考 |
| `omega_ref` | [N×1] | rad/s | 角速度参考 |
| `theta_ref` | [N×1] | rad | 坡度角参考 |

### MPC 跟踪误差参考（均为0）
| 字段 | 维度 | 单位 | 说明 |
|-----|------|-----|------|
| `e_y_ref` | [N×1] | m | 横向误差参考 |
| `e_psi_ref` | [N×1] | rad | 航向误差参考 |
| `e_v_ref` | [N×1] | m/s | 速度误差参考 |

### 调度变量（已滤波）
| 字段 | 维度 | 单位 | 说明 |
|-----|------|-----|------|
| `rho` | [N×3] | - | 列为 [v, ω, θ]（均为有符号），已经过一阶滤波（τ=0.4s） |

### Simulink 接口
| 字段 | 说明 |
|-----|------|
| `time` | 与 `t` 相同，用于 From Workspace 模块 |
| `signals.values` | [N×9] 矩阵：[X, Y, psi, v, omega, theta, e_y, e_psi, e_v] |
| `signals.dimensions` | 9（信号维度） |

### 元数据
| 字段 | 说明 |
|-----|------|
| `meta.path_type` | 路径类型字符串 |
| `meta.generation_time` | 生成时间戳 |
| `meta.version` | 版本号 |
| `meta.author` | 作者信息 |
| `meta.params` | 生成参数（T_end, R, v0 等） |

## 在 Simulink 中使用

### 方法1：From Workspace
```matlab
% 生成路径
params = parameters();
ref = gen_agv_ref_path('turn', params);

% 保存到基础工作区
assignin('base', 'ref', ref);

% 在 Simulink 中：
% 1. 添加 From Workspace 模块
% 2. 设置参数：Data = ref.signals.values
% 3. 设置参数：Time = ref.time
```

### 方法2：信号编辑器
```matlab
% 生成并保存
params = parameters();
ref = gen_agv_ref_path('straight_turn', params);
save('path_straight_turn.mat', 'ref');

% 在 Simulink Signal Editor 中导入 path_straight_turn.mat
```

## 典型参数值（已更新）

| 参数 | 默认值 | 说明 |
|-----|--------|------|
| `T_end` | 20.0 s | 仿真总时长 |
| `v0` | 1.0 m/s | 初始速度 |
| `R` | 10.0 m | 转弯半径 |
| `theta_slope` | 5° | 坡度角 |
| `bumpy_amp` | 0.2 rad | 颠簸振幅（地面坡度扰动） |
| `rho_filter_tau` | 0.4 s | 调度变量滤波时间常数 |
| `turn_transition` | 0.4 s | 转弯过渡时间（S曲线） |

## 设计说明

### 调度变量滤波
为避免 LPV-MPC 中调度变量快速跳变导致的控制不稳定，`rho` 经过一阶低通滤波：

```
y[k] = α·x[k] + (1-α)·y[k-1]
其中 α = Ts / (Ts + τ)
```

默认时间常数 τ = 0.4s，满足规范要求（0.3–0.5s）。

### 路径坐标系误差
所有误差参考（`e_y_ref`, `e_psi_ref`, `e_v_ref`）设为 0，便于 MPC 直接进行跟踪控制。

### S 曲线平滑过渡（straight_turn 专用）
为避免曲率阶跃导致调度变量跳变，`straight_turn` 在直线到转弯切换时采用余弦S曲线：

```
ω(τ) = ω_max · 0.5 · (1 - cos(π·τ))
其中 τ = (t - t_switch) / t_trans ∈ [0, 1]
```

- 过渡时间默认 0.4s（可配置 0.3–0.5s）
- 保证 ω 及其导数连续，减少执行器冲击
- 改善 LPV-MPC 调度稳定性

### 颠簸工况建模策略
颠簸体现为**地面坡度扰动**（`theta_ref`），而非几何路径扰动（Y方向）：

- **优点**：几何路径保持直线，符合 Frenet 坐标系"误差=0"理念
- **实现**：`theta = bumpy_amp · sin(t)`，默认振幅 0.2 rad
- **用途**：供 MD 端口（测量扰动）和 AI 工况识别使用

## 可视化示例

运行 `test_gen_paths.m` 会为每种路径生成 6 个子图：
1. **XY 轨迹**：平面轨迹图
2. **参考速度**：v vs. 时间
3. **参考角速度**：ω vs. 时间
4. **参考航向角**：ψ vs. 时间
5. **坡度角参考**：θ vs. 时间
6. **调度变量 ρ**：[v, ω, θ] vs. 时间（滤波后）

## 依赖项

- `parameters.m`：提供 `Ts` 等基础参数

## 版本历史

- **V1.1** (2025-10-23)
  - 统一 ρ 为有符号 [v, ω, θ]
  - 颠簸默认幅值改为 0.2 rad
- **V1.0** (2025-10-02)
  - 初始版本，支持 5 种路径类型

## 后续开发

本模块是 LPV-MPC 项目的第一步，后续将开发：
1. 线性化模块（`lin/`）
2. MPC 设计模块（`mpc/`）
3. 贝叶斯优化（根目录 `Cost_Function.m`、`Bayesian_Optimization.m`）
4. AI 工况识别（`ai/`）

## 联系与反馈

如有问题或建议，请参考 `func.md` 中的模块导航文档。

