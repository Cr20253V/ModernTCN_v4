# AGV 模型参数修正与重跑计划

日期：2026-05-31

## 范围

本计划将轮胎侧偏刚度、横摆阻尼和侧滑角阻尼的修正视为一次 plant 模型版本更新。plant 改动后，LPV 数据库、MPC 参数、训练数据、学习模型、闭环实验、论文图片和论文表格都需要按顺序刷新。

当前涉及的关键文件：

- `src/core/parameters.m`
- `src/core/state_eq_ref.m`
- `src/core/state_eq_ref_train_data.m`
- `src/core/state_eq.m`
- `src/core/output_eq_ref.m`
- `src/lpv/lin_agv_at_point.m`
- `src/lpv/lin_agv_grid.m`
- `src/mpc/mpc_setup_single_interp.m`
- `src/mpc/mpc_update_from_rho.m`
- `data/models/lin_agv_db.mat`
- `data/models/maps_best.mat`
- `scripts/generate_tables.py`

本计划包目录：

- `results/paper/agv_model_parameter_correction_workflow/`

说明：

- 代码运行所需的 canonical artifact 仍保留在原工程位置，例如 `data/models/lin_agv_db.mat`、`data/models/maps_best.mat`、`results/compare/...`。
- 本计划相关的快照、报告、索引、参数记录、结果副本清单和交接文档统一放入本计划包目录。

## MPC 是否需要重新调整

需要。MPC 参数至少要重新验证，很多情况下还需要重新整定。

但不要在 nonlinear plant 和 LPV 数据库更新之前就最终整定 MPC。`front_cornering_stiffness`、`rear_cornering_stiffness`、`C_damping` 或 `beta_dot` 阻尼项变化后，非线性 plant 的横向和横摆响应会改变，LPV-MPC 使用的局部线性模型也会改变。因此：

- 必须先重新生成 LPV 数据库，再做最终 MPC 验证。
- 现有 `maps_best.mat` 应视为旧 plant 下的调参证据，不能直接当作新 plant 的最终参数。
- `Q`、`R`、`dR`、`Np`、`Nc`、软约束和调度滤波都要重新验证。
- 是否需要完整贝叶斯优化或网格调参，应在小规模稳定性和敏感性筛查之后决定。

## Node 0 - 冻结当前旧基线

目标：在修改参数前保留旧模型基线。

操作：

- 记录 `src/core/parameters.m` 中当前参数值。
- 记录 `state_eq_ref.m`、`state_eq_ref_train_data.m` 和 `state_eq.m` 中当前阻尼项。
- 保存或记录当前论文使用的结果目录：
  - `results/compare/tcn_gru_modern_closed_loop/`
  - `results/compare/lpvmpc_theta_baseline/`
  - `results/compare/multipath_closed_loop/`
  - `results/compare/robustness_closed_loop/`
  - `src/pic&table/`
  - `results/paper/pic/`
  - `results/paper/Latex/`

验收标准：

- 已生成一份旧基线说明，包含旧参数值和旧结果路径。
- 尚未改变任何代码行为。

建议产物：

- `results/paper/agv_model_parameter_correction_workflow/01_baseline/agv_model_old_baseline_snapshot.md`

## Node 1 - 定义候选 plant 参数

目标：先做小规模参数扫描，再确定最终 plant。

建议扫描范围：

- 侧偏刚度：
  - `C_alpha = 300`
  - `C_alpha = 1500`
  - `C_alpha = 3000`
  - `C_alpha = 6000`
- 横摆阻尼：
  - `C_damping = 100`
  - `C_damping = 250`
  - `C_damping = 500`
- 侧滑角阻尼：
  - 物理模型：正常速度下移除 `-5.0*beta`
  - 温和数值阻尼：使用 `-1.0*beta`
  - 旧稳定器：仅将 `-5.0*beta` 保留为旧基线

建议第一轮候选：

- `C_alpha = 1500` 或 `3000`
- `C_damping = 250`
- 正常速度下 `beta_dot` 不再包含 `-5.0*beta`
- 仅在低速启动区域保留温和 beta 回零项，用于数值稳定

验收标准：

- 候选集合足够小，可以快速测试。
- 旧模型仍作为参考基线保留，但不作为优先最终模型。

## Node 2 - 统一 plant 模型代码

目标：确保所有模型入口使用同一套物理假设。

操作：

- 更新 `src/core/parameters.m` 中的候选或最终参数。
- 更新 `src/core/state_eq_ref.m`。
- 更新 `src/core/state_eq_ref_train_data.m`。
- 更新 `src/core/state_eq.m`，避免兼容实现继续保留旧行为。
- 检查 `src/core/output_eq_ref.m` 中的派生特征是否依赖旧 plant 假设。
- 如有条件，增加版本标记或注释，例如 `plant_param_revision = agv_physics_v2`。

重要规则：

- 不要让 `state_eq_ref.m` 使用 `C_damping=250`，而训练数据代码仍使用 `1000`。

验收标准：

- 执行 `rg "C_damping|1000.0|-5.0\\*beta|front_cornering_stiffness|rear_cornering_stiffness" src/core` 后，没有非预期旧 plant 残留。
- 主仿真和训练数据仿真使用同一套目标刚度和阻尼。

## Node 3 - 开环物理合理性自检

目标：在接触 MPC 前，先确认修正后的 plant 稳定且物理上合理。

操作：

- 运行开环直行测试。
- 运行低速和常速转弯测试。
- 运行纯坡度测试。
- 运行转弯加坡度复合测试。

检查指标：

- `omega` 响应上升时间和超调。
- `beta` 峰值和收敛情况。
- 侧向力饱和比例。
- 转向角和转向角速度行为。
- 坡度下的速度响应。
- 是否出现 NaN/Inf。
- 是否出现不合理振荡。

验收标准：

- 直线行驶稳定。
- 常规参考曲率下转向不迟钝。
- `beta` 不发散。
- 驱动力和横摆角速度指令不长期贴边。

决策：

- 若不稳定，返回 Node 1。
- 若合理，继续重新生成 LPV 数据库。

## Node 4 - 重新生成 LPV 数据库

目标：重建 LPV-MPC 使用的局部线性模型。

操作：

- 使用 `src/lpv/lin_agv_grid.m` 重新生成 `data/models/lin_agv_db.mat`。
- 确认 `lin_agv_at_point.m` 调用的是修正后的 `state_eq_ref.m`。
- 检查 LPV 网格覆盖范围：
  - 速度 `v`
  - 横摆角速度 `omega`
  - 坡度 `theta`

验收标准：

- LPV 数据库生成过程无数值失败。
- 线性化矩阵全部为有限值。
- 网格范围覆盖评估路径。
- 数据库时间戳或版本晚于 plant 参数修改。

建议产物：

- 更新后的 `data/models/lin_agv_db.mat`
- `results/paper/agv_model_parameter_correction_workflow/04_lpv_database/lpv_database_regeneration_report.md`
- 如需保留数据库副本，可复制到 `results/paper/agv_model_parameter_correction_workflow/04_lpv_database/`

## Node 5 - MPC 重调前的可行性检查

目标：判断旧 MPC 设置在新 plant 和新 LPV 数据库下是否还能工作。

操作：

- 先使用 `mpc_setup_single_interp.m` 的现有默认值。
- 如果旧 `maps_best.mat` 造成行为混乱，先临时禁用或忽略。
- 使用 oracle 坡度调度运行短闭环路径。
- 对比：
  - 求解状态。
  - 约束违背。
  - `e_y`、`e_psi`、`e_v`、`e_omega`。
  - `F_cmd`、`omega_cmd`。
  - 输入增量。

验收标准：

- MPC 求解稳定。
- oracle-slope LPV-MPC 至少能跟踪一条短验证路径。
- 不出现持续饱和或求解不可行。

决策：

- 若可行性失败，优先调约束和预测时域。
- 若可行但跟踪差或动作激进，再调权重。

## Node 6 - MPC 重新整定

目标：为修正后的 plant 重新整定控制器。

整定顺序：

1. 先固定约束，只调 `Q/R/dR`。
2. 只有响应时序明显不合适时，再调整 `Np` 和 `Nc`。
3. 只有出现不可行或过多约束违背时，再调整软约束。
4. plant 和控制器稳定后，再调整调度滤波。

需要检查的参数：

- `Q = [q_y, q_psi, q_v, q_omega]`
- `R = [r_F, r_omega]`
- `dR = [r_dF, r_domega]`
- `Np`
- `Nc`
- `umin`、`umax`
- `dumin`、`dumax`
- `ymin`、`ymax`
- `soft_weight_pos`
- `soft_weight_yaw`
- `rho_filter_tau`
- `maps_best.mat` 中的自适应映射范围

建议流程：

- 从 `src/mpc/mpc_setup_single_interp.m` 的现有默认值开始。
- 在 oracle-slope 闭环条件下做小规模网格调参或贝叶斯优化。
- 优化目标包括：
  - lateral RMSE 低。
  - heading RMSE 低。
  - 平滑性代价合理。
  - 约束违背为零或接近零。
  - 控制饱和不过多。

验收标准：

- oracle-slope LPV-MPC 稳定且性能较好。
- zero-slope 和 IMU-slope baseline 仍然有意义，而不是被人为调坏。
- 最终 MPC 设置有明确记录且可复现。

建议产物：

- 更新或新建 `data/models/maps_best.mat`
- `results/paper/agv_model_parameter_correction_workflow/06_mpc_retuning/mpc_retuning_report.md`
- 如需保留 `maps_best.mat` 副本，可复制到 `results/paper/agv_model_parameter_correction_workflow/06_mpc_retuning/`

## Node 7 - 重新生成训练数据

目标：让学习数据集反映修正后的 plant 和重新验证后的控制接口。

操作：

- 重建 ModernTCN/GRU/TCN 训练数据集。
- 重新生成 dataset contract JSON。
- 重新生成 train-only scaler 统计量。
- 校验 feature names 和输入维度。
- 确认是否继续采用 non-IMU feature policy。

验收标准：

- 新 `.mat` 数据集存在。
- contract JSON 与实际数据形状和特征一致。
- train/validation/test 划分策略保留。
- 数据集元数据记录 plant 参数版本和 MPC 版本。

重要：

- 不要用旧阻尼或旧侧偏刚度生成的数据训练新模型。

## Node 8 - 重新训练学习模型

目标：基于修正后的数据集重新训练估计器。

操作：

- 重新训练 ModernTCN。
- 重新训练 GRU。
- 如果论文仍保留 TCN baseline，重新训练 TCN。
- 如果论文仍保留 offline/closed-loop mismatch 消融，重新训练 causal ModernTCN。
- 为选定 ModernTCN checkpoint 导出 ONNX。
- 运行 PyTorch/ONNXRuntime/MATLAB 一致性检查。

验收标准：

- 模型报告和 checkpoint 存在。
- 测试集指标可接受。
- ONNX 和 MATLAB 推理一致性检查通过。

建议产物：

- 更新后的 `results/modern_tcn/...`
- 更新后的 `results/gru/...`
- 更新后的 `results/tcn/...`
- 更新后的 `data/models/...`
- `results/paper/agv_model_parameter_correction_workflow/08_models/model_retraining_report.md`

## Node 9 - 重新运行主闭环实验

目标：在修正后的模型上重跑论文主对比。

控制器/基线：

- `LPV-MPC_theta0`
- `LPV-MPC_IMU_theta`
- `LPV-MPC_oracle_theta`
- `GRU`
- `TCN`
- `ModernTCN`
- 若保留 causal ModernTCN，也一并重跑

指标：

- lateral RMSE。
- heading RMSE。
- XY RMSE。
- 速度和横摆角速度误差。
- scheduled-slope MAE。
- 平滑性代价。
- 最大限幅命中率。
- 约束违背率。
- 求解时间。

验收标准：

- 所有方法使用同一个修正后的 plant 和同一套 MPC 设置。
- scheduled slope 使用 MATLAB `rho_f(:,3)` / Python `rho[:, 2]`。
- 结果保存在新的 run tag 下，不与旧结果混用。

## Node 10 - 重新运行多路径和鲁棒性实验

目标：确认修正后的模型不只在主展示路径上有效。

操作：

- 重跑 multipath closed-loop benchmark。
- 重跑 robustness closed-loop benchmark。
- 检查原路径难度在新 plant 下是否仍然合适。

验收标准：

- aggregate CSV 已重新生成。
- 每条路径的报告已重新生成。
- 没有将旧 plant 和新 plant 的结果混在同一张表中。

## Node 11 - 重新生成源数据和图片

目标：更新所有依赖闭环或数据集结果的论文图片。

大概率受影响的图片：

- Fig. 5：如果路径元数据或路径呈现变化。
- Fig. 6：主闭环结果。
- Fig. 7：scheduled slope。
- Fig. 8：控制平滑性。
- Fig. 9：鲁棒性。
- Fig. 10：offline/closed-loop mismatch，如果保留。

大概率不受影响或只需文字检查的图片：

- Fig. 1：整体框架。
- Fig. 2：AGV 模型示意图，除非图中标注了具体参数。
- Fig. 3：scheduling mismatch 概念图。
- Fig. 4：时序估计器结构图，除非特征集变化。

验收标准：

- `src/pic&table/` 中的源 CSV 来自新结果文件。
- `results/paper/pic/` 下的 PNG/PDF/SVG 已重新生成。
- `results/paper/agv_model_parameter_correction_workflow/11_figures_tables/` 中记录图片和表格刷新清单。
- 图片 caption 不再引用旧数值。

## Node 12 - 重新生成表格

目标：用可追溯的新数据源刷新论文表格。

操作：

- 运行 `scripts/generate_tables.py`。
- 检查：
  - Table 1：车辆参数。
  - Table 2：MPC 设置。
  - Table 3：数据集 contract。
  - Table 4：模型元数据。
  - Table 6：主闭环结果。
  - Table 7：多路径汇总。
  - Table 8：鲁棒性汇总。
  - Table 9：消融或 mismatch 表，如果保留。
  - Table 10：实时性，如果模型文件变化。

验收标准：

- `results/paper/Latex/tables_generated.tex` 已重新生成。
- `results/paper/Latex/tables_data_sources.md` 指向新结果文件。
- `results/paper/Latex/missing_table_data_report.md` 显示无缺失数据。
- 重新校验 Table 6 的 scheduled-slope 映射：Python `rho[:, 2]` 等于 MATLAB `rho_f(:,3)`。

## Node 13 - 更新论文正文

目标：让正文论述与修正后的模型和结果一致。

操作：

- 更新模型参数描述。
- 如正文提到旧人工阻尼，需要更新相关讨论。
- 更新所有数值结果。
- 更新 limitations 和 sim-to-real gap 讨论。
- 避免继续用旧 plant 的结果支撑新 plant 的结论。

验收标准：

- 摘要、结果、结论、图片 caption 和表格中没有旧数值残留。
- 正文清楚说明修正后的 AGV 模型假设。

## Node 14 - 编译和一致性审计

目标：完成论文侧最终验证。

操作：

- 编译 `paper_v1_tables_check.tex` 或当前使用的论文验证目标。
- 如有需要，编译主论文。
- 搜索旧参数或旧结果：
  - `300`
  - `1000`
  - `-5.0 beta`
  - 旧 RMSE 数值
  - 旧 run tag
- 交叉检查数据源路径和 caption。

验收标准：

- LaTeX 可编译。
- 没有把旧模型结果当作当前结果引用。
- 表格和图片内部一致。

## Node 15 - 最终归档和交接

目标：让新模型和新结果在后续对话中可复现、可追踪。

操作：

- 创建最终运行总结，包含：
  - plant 参数版本。
  - MPC 版本。
  - 数据集版本。
  - 模型 checkpoint 版本。
  - 闭环结果目录。
  - 图片/表格重新生成日期。
- 将旧基线和新修正结果分开放置。

验收标准：

- 后续任意对话都能快速判断哪些 artifact 属于修正后的模型。

建议产物：

- `results/paper/agv_model_parameter_correction_workflow/15_final_handoff/agv_model_parameter_correction_final_report.md`

## 最小执行路径

如果时间有限，先执行下面这条最小路径：

1. Node 0 - 冻结旧基线。
2. Node 1 - 选择小规模候选参数集合。
3. Node 2 - 统一代码。
4. Node 3 - 开环自检。
5. Node 4 - 重新生成 LPV 数据库。
6. Node 5 - MPC 可行性检查。
7. Node 6 - 如有需要，重新整定 MPC。
8. Node 9 - 重跑主闭环中的 oracle 和关键 baseline smoke test。

只有当这条最小路径表现良好后，再开始完整重建数据集、重训模型和刷新论文 artifact。
