# LPV-MPC 使用说明

## 概述

本文档介绍如何使用线性化脚本和MPC控制器设计脚本，实现AGV的自适应LPV-MPC控制，并开展贝叶斯优化。

## 关键统一
- ρ（调度变量）统一为有符号：`rho = [v; omega; theta]`
- 颠簸默认幅值：`0.2 rad`
- 贝叶斯优化脚本与产物放在根目录：`Cost_Function.m`, `Bayesian_Optimization.m`, `maps_best.mat`

## 目录结构（节选）
```
E:\Matlab\Simulink\S-Function_14\
├── lin_agv_at_point.m
├── lin_agv_grid.m
├── mpc_setup_single_interp.m
├── mpc_update_from_rho.m
├── parameters.m
├── state_eq.m
├── output_eq.m
├── Cost_Function.m
├── Bayesian_Optimization.m
└── func.md
```

## 快速开始

1) 网格线性化（示例 3×3×3，θ覆盖 ±0.2 rad）：
```matlab
params = parameters();
grid.V_grid = [0.8; 1.0; 1.2];
grid.W_grid = [-0.2; 0.0; 0.2];   % 有符号 ω
grid.T_grid = [-0.2; 0.0; 0.2];   % 颠簸幅值匹配 0.2 rad
lin_opts = struct('coord','path','disc','zoh','keep_E',true,'export_mat','plant_grid.mat');
db = lin_agv_grid(params, grid, lin_opts);
```

2) 创建单控制器并在线插值：
```matlab
ctrl = mpc_setup_single_interp(db, struct());
rho = [1.0; 0.1; 0.05];
upd = mpc_update_from_rho(rho, db, ctrl.maps);
```

3) Simulink 集成
- Adaptive MPC 自定义更新函数返回：A,B,C,D,（E/Bv）
- Measured outputs: `[e_y;e_psi;e_v;e_omega]`；Reference: `[0;0;0;0]`；MD: `theta`
- Scheduling: `rho_f = first_order_filter([v;omega;theta], tau=0.4s)`

4) 贝叶斯优化
```matlab
[best, boResults] = Bayesian_Optimization(params, db, struct());
```

## API 落地澄清
- 脚本版（mpcmoveAdaptive一类接口）：
  1. 每个采样步将 `mpcobj.Model.Plant.A/B/C/D = upd.A/B/C/D`；
  2. 将 `upd.Bv` 作为 MD 通道影响矩阵（可通过自定义结构或 setoutdist/Estimator 变体实现）；
  3. 若在线权重：`mpcobj.Weights.OutputVariables = upd.Q;` 等（或使用外部权重端口）。
- Simulink 版：
  - Adaptive MPC 自定义更新函数直接返回 A,B,C,D,Bv（E），块内应用；权重/约束通过外部端口或回调覆盖。

## 稳定性与性能
- 网格点 `|eig(A)| < 1.0` 或可由 MPC 稳定
- 预测域：2.0–3.0 s；控制域：0.5–1.0 s

## 故障排查
- 线性化失败：检查网格范围（避免 v=0；θ 不超 ±0.2 rad 示例）
- MPC 不稳定：检查基准模型极点/权重/软约束
- 求解时间过长：缩短 Np/Nc 或更换求解器

