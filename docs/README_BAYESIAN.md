# 贝叶斯优化使用说明

> **版本**：V2.11 | **最后更新**：2025-12-29

## 概述

贝叶斯优化用于自动调整 **Adaptive MPC 控制器** 的权重和场景自适应参数，以最小化多场景闭环跟踪代价。

## 文件结构

```
src/bo/
├── Bayesian_Optimization.m   # 主脚本：两阶段贝叶斯优化
├── start_bayesian.m          # 快速启动脚本
src/mpc/
├── Cost_Function.m           # 代价函数：多场景闭环评估
├── mpc_setup_single_interp.m # MPC 控制器创建
├── mpc_update_from_rho.m     # 在线权重/模型更新
```

## 快速开始

```matlab
% 方法1：使用默认配置
run('src/bo/start_bayesian.m')

% 方法2：自定义配置
params = parameters();
db = load('data/models/lin_agv_db.mat'); db = db.db;
options.MaxObjectiveEvaluations = 50;  % 评估次数
options.scenes = struct('multi_turn_left', 0.4, 'straight_turn', 0.3, ...
                        'slope', 0.1, 'bumpy', 0.1, 'straight', 0.1);
[best, boResults] = Bayesian_Optimization(params, db, options);
```

## 优化变量

| 类别 | 变量名 | 范围 | 说明 |
|------|--------|------|------|
| **Q权重** | `q_y` | [15, 35] | 横向误差权重 |
| | `q_psi` | [12, 30] | 航向误差权重 |
| | `q_v` | [3, 8] | 速度误差权重 |
| | `q_omega` | [0.5, 3] | 角速度误差权重 |
| **R权重** | `log10_r_F` | [-4, -2.5] | 驱动力权重（对数） |
| | `log10_r_omega` | [-3.8, -2.2] | 角速度指令权重（对数） |
| **形状参数** | `alpha_Q/R/dR` | [0, 1] | 权重插值下界 |
| | `beta_Q/R/dR` | [0, 1] | 权重插值上界 |
| **场景自适应** | `omega_threshold` | [0.05, 0.20] | 转弯判定阈值 [rad/s] |
| | `q_y_gain_max` | [1.2, 2.5] | 转弯时 q_y 增益 |
| | `theta_threshold` | [0.03, 0.05] | 坡度判定阈值 [rad] |
| | `q_v_gain_max` | [1.2, 2.0] | 坡度时 q_v 增益 |
| **其他** | `tau` | [0.2, 0.6] | ρ 滤波时间常数 |

## 场景权重配置

默认场景及权重（权重和应为 1.0）：

| 场景 | 路径类型 | 默认权重 | 说明 |
|------|----------|----------|------|
| `multi_turn_left` | 变半径左转 | 0.20 | R=6.67m→10m→20m |
| `multi_turn_right` | 变半径右转 | 0.20 | R=6.67m→10m→20m |
| `straight_left_turn` | 直线后左转 | 0.15 | 3s 直行后转弯 |
| `straight_right_turn` | 直线后右转 | 0.15 | 3s 直行后转弯 |
| `slope` | 坡度直线 | 0.10 | 5° 固定坡度 |
| `bumpy` | 颠簸直线 | 0.10 | 坡度振荡扰动 |
| `straight` | 平地直线 | 0.10 | 基准场景 |

> **注意**：`turn` 和 `straight_turn` 已删除（与其他场景重复）。

## 代价函数组成

```
J = Σ (场景权重 × 场景代价)

场景代价 = J_trk + J_smooth + J_cons + J_rt

J_trk     = 1.1×RMSE(e_y)/e_y_max + 1.0×RMSE(e_psi)/e_psi_max + ...
J_smooth  = 0.08×RMS(ΔF)/ΔF_max + 0.07×RMS(Δω)/Δω_max
J_cons    = 10×L1(约束违反) + 50×L∞(约束违反)
J_rt      = max(0, (avg_ms - 5)/5) + (max_ms > 10)×0.5
```

## 两阶段优化流程

```
┌─────────────────────────────────────────────┐
│ 第一阶段：全局搜索                           │
│ - 默认 100 次评估                            │
│ - 采集函数：Expected Improvement Plus        │
│ - 产出：全局最优参数候选                     │
└───────────────────┬─────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 第二阶段：局部精细搜索                       │
│ - 以第一阶段最优为中心收缩边界（shrink=35%） │
│ - 默认 30 次评估                             │
│ - 产出：最终最优参数                         │
└───────────────────┬─────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 保存产物                                     │
│ - data/models/maps_best.mat                  │
└─────────────────────────────────────────────┘
```

## 关键配置参数

```matlab
options = struct();

% 评估次数
options.MaxObjectiveEvaluations = 100;  % 第一阶段（建议 50-150）

% 第二阶段配置
options.local_refine.enable = true;     % 是否启用
options.local_refine.shrink = 0.35;     % 边界收缩比例
options.local_refine.num_evals = 30;    % 评估次数
options.local_refine.num_seeds = 8;     % 初始点数量
options.local_refine.jitter = 0.08;     % 初始点抖动幅度

% 历史保存
options.save_history = true;  % 保存优化历史到 results/bo/history/
```

## 产物说明

| 文件 | 位置 | 说明 |
|------|------|------|
| `maps_best.mat` | `data/models/` | 最优权重/约束映射表 |
| `bo_history_*.mat` | `results/bo/history/` | 优化历史（可选） |
| `bo_report_*.mat` | `results/bo_reports/` | 单次评估报告 |

## 常见问题

### 1. 如何提高转弯跟踪精度？
- 增大 `multi_turn_left` 场景权重
- 增大 `q_y_gain_max` 搜索上界
- 降低 `omega_threshold` 下界

### 2. 优化时间过长？
- 减少 `MaxObjectiveEvaluations`
- 禁用第二阶段：`options.local_refine.enable = false`
- 减少场景数量

### 3. 如何复用优化结果？
```matlab
% 加载最优映射
load('data/models/maps_best.mat', 'maps_best');

% 应用到 MPC 控制器
ctrl.maps = maps_best;
```

## 依赖关系

```
Bayesian_Optimization.m
    ├── Cost_Function.m
    │       ├── gen_agv_ref_path.m      (路径生成)
    │       ├── mpc_setup_single_interp.m (控制器创建)
    │       ├── mpc_update_from_rho.m   (在线更新)
    │       └── state_eq_ref.m          (AGV 模型)
    └── lin_agv_grid.m (若 db 为空时自动调用)
```
