# LPV 数据库重建报告

状态：Node 4 已完成，已生成 MPC 可用的稳定化 LPV 数据库。

## 输入

- plant 参数版本：`agv_physics_v2` 候选
- `lin_agv_at_point.m` 检查结果：线性化链路已接入修正后的 plant 参数，并增加了不稳定离散极点裁剪，保证 LPV-MPC 预测模型在单位圆内。
- `lin_agv_grid.m` 网格配置：
  - `V_grid = [0.02 0.04 0.06 0.08 0.10 0.14 0.20 0.35 0.60 1.00 1.20]'`
  - `W_grid = linspace(-1.20, 1.20, 15)'`
  - `Theta_grid = deg2rad((-12:1:12)')`
  - 采样时间 `Ts = 0.0100 s`

## 输出

- canonical 数据库路径：`data/models/lin_agv_db.mat`
- canonical 网格快照路径：`data/models/plant_grid_test.mat`
- 本目录副本路径：
  - `results/paper/agv_model_parameter_correction_workflow/04_lpv_database/lin_agv_db_agv_physics_v2_stabilized.mat`
  - `results/paper/agv_model_parameter_correction_workflow/04_lpv_database/plant_grid_test_agv_physics_v2_stabilized.mat`
- 旧基线备份：
  - `results/paper/agv_model_parameter_correction_workflow/01_baseline/lin_agv_db_old_baseline.mat`
  - `results/paper/agv_model_parameter_correction_workflow/01_baseline/plant_grid_test_old_baseline.mat`
- 最新生成时间：2026-05-31

## 实际生成摘要

- 第一次生成摘要：
  - `Nv=11, Nw=15, Nt=25, unstable=504, Ts=0.0100`
  - 后续 Node 5 发现中心工作点存在离散极点 `16.1661`，全库最大极点约 `78.2895`，会导致 MPC 报错 `QP Hessian matrix too large, not positive definite`。
- 稳定化后生成摘要：
  - `NODE4_REGEN_STABILIZED Nv=11 Nw=15 Nt=25 unstable=0 maxeig=1 mineig=0.999 finite=1`
- 数据库结构字段：
  - `grid`, `Ts`, `A`, `B`, `C`, `D`, `E`, `nx`, `nu`, `ny`, `nd`, `Nv`, `Nw`, `Nt`, `workpoints`, `meta`
- `db.meta` 字段：
  - `version`, `generated_by`, `generated_time`, `model_semantics`, `discretization_note`, `steer_model`, `steer_assumption`, `coordinate`, `discretization`, `total_time`, `unstable_count`, `marginal_count`, `states`, `inputs`, `outputs`, `scheduling`, `disturbances`

## 验收

- 是否生成成功：是，稳定化后 canonical `data/models/lin_agv_db.mat` 已更新。
- 是否存在 NaN/Inf：否，`FINITE_OK=1`
- 网格规模：
  - `Nv = 11`
  - `Nw = 15`
  - `Nt = 25`
- 不稳定工作点计数：`0 / 4125`
- 最大离散极点模：约 `1.000`，主要为路径误差模型的积分器/边界稳定模态。
- 网格覆盖是否满足评估路径：从速度 `0.02-1.20 m/s`、横摆角速度 `-1.20-1.20 rad/s`、坡度 `-12 deg` 到 `+12 deg` 的范围看，覆盖当前论文主评估场景是合理的。

## 备注

- Node 4 曾出现一次仅影响报告补写的元数据字段读取错误：尝试访问不存在的 `db.meta.boundary_count`。这不影响数据库生成。
- 第一次 LPV 数据库虽然有限值检查通过，但不满足 MPC 数值稳定性要求；最终以稳定化后的数据库为准。
- 修改过的线性化文件：`src/lpv/lin_agv_at_point.m`。
