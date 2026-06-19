# 旧模型基线快照

状态：Node 0 已完成。

记录时间：2026-05-31 16:27:55 +08:00

## 当前参数

- `src/core/parameters.m:54`：`front_cornering_stiffness = 300 N/rad`
- `src/core/parameters.m:55`：`rear_cornering_stiffness = 300 N/rad`
- `src/core/state_eq_ref.m:379`：主 RK4 核心 `C_damping = 250.0`
- `src/core/state_eq_ref.m:470`：兼容核心 `C_damping = 1000.0`
- `src/core/state_eq_ref_train_data.m:176`：训练数据核心 `Mz_damping = -1000.0 * omega`
- `src/core/state_eq.m:357`：主 RK4 核心 `C_damping = 1000.0`
- `src/core/state_eq.m:448`：兼容核心 `C_damping = 1000.0`
- 正常速度 `beta_dot` 阻尼项：`-5.0*beta`
- 低速 `beta_dot` 阻尼项：`-5.0*beta`

## 当前入口

- `src/core/agv_model_sfunc.m:109`：输出方程调用 `output_eq_ref`
- `src/core/agv_model_sfunc.m:131`：状态更新调用 `state_eq_ref`

## 当前结果目录

- 主闭环：`results/compare/tcn_gru_modern_closed_loop/`
- LPV-MPC baseline：`results/compare/lpvmpc_theta_baseline/`
- multipath：`results/compare/multipath_closed_loop/`
- robustness：`results/compare/robustness_closed_loop/`
- 论文图片：`results/paper/pic/`
- LaTeX 表格：`results/paper/Latex/`
- 源数据：`src/pic&table/`

## Git 工作区注意

执行 Node 0 前，工作区已有与本任务无关的修改/删除/未跟踪文件，包括：

- `results/paper/pic/temp_result.md` 已修改。
- `results/软著/...` 下存在已删除项。
- `results/paper/Conference/` 为未跟踪目录。
- 若干中文分析文档为未跟踪文件。

这些均未在 Node 0 中回滚或修改。

## 备注

- 本文件用于冻结旧模型状态，不代表已完成参数修正。
- 后续 Node 2 会统一主仿真、兼容实现和训练数据版本中的刚度/阻尼口径。
