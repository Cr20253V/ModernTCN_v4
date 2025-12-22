# 项目运行规则（运行时/开发通用规范）

> 面向本仓库的日常开发、联调与交付的统一约束：语言、代码风格、注释、接口与目录、提交与文档。

## 1. 语言与沟通
- 回答与注释：中文为主，必要时补英文术语。
- 单位统一：m, m/s, rad；采样周期 `Ts` 由 `parameters.m` 提供。
- 代理/协作：若执行中存在不确定性或缺少信息，需立即向作者提问并标注“假设/可选”。

## 2. 语言栈与文件类型
- 首选：MATLAB（.m）与 Simulink（.slx）。
- 禁止直接修改/提交的构建产物与缓存：`slprj/`, `*_grt_rtw/`, `*.slxc`, `*.autosave`, `GRU_logs/`。
- 首选新增/修改：`.m`, `.md` 与顶层 `.mat` 产物。

## 3. 代码风格（MATLAB）
- 函数化优先：每个核心功能独立函数文件，`function ... end`。
- 命名语义化：避免单字母；如 `x_ref`, `u_mpc`, `rho_grid`。
- 向量化与预分配：避免不必要循环与动态扩容。
- I/O 约定：读写 `.mat` 使用清晰变量名，必要时说明维度与单位。
- 输出最小可运行示例，并给出 `matlab -batch` 命令范例。

示例：
```matlab
function y = saturate(u, umin, umax)
%SATURATE Clamp u into [umin, umax]
    y = min(max(u, umin), umax);
end
```

## 4. 注释规范（脚本/函数头模板）
```matlab
% =============================
% 文件名：xxx.m
% 版本号：V1.0
% 最后修改时间：YYYY-MM-DD
% 作者：xxx
% 功能描述：
% 输入参数：
%   - xxx：类型，单位，说明
% 输出参数：
%   - xxx：类型，单位，说明
% 依赖：
% 备注：
% =============================
```

## 5. 接口与数据约定
- 路径全局参考（用于可视化/外部模块）：`ref_global=[X Y psi v omega]`（5 列）。
- MPC 误差状态：`x_err=[e_y,e_psi,e_v,e_omega]^T`；MPC 参考端口实际为 4×1（零向量或设定误差目标）。
- 调度变量：`rho=[v, omega, theta]`；经一阶滤波（τ≈0.3–0.5 s）。
- From Workspace：结构 `time` + `signals.values`，若驱动 MPC 误差参考，仅提供 4 列。

## 6. 当前项目结构与约束（与现状对齐）
- 根目录为主（flat），核心脚本与产物集中在仓库根：
    - 模型/方程：`parameters.m`, `state_eq.m`, `state_eq_ref.m`, `output_eq.m`, `output_eq_ref.m` 及 `*_ref_train_data.m`
    - 线性化：`lin_agv_at_point.m`, `lin_agv_grid.m`；产物：`plant_grid.mat`, `plant_grid_test.mat`, `lin_agv_db.mat`
    - MPC：`mpc_setup_single_interp.m`, `mpc_update_from_rho.m`
    - 参考轨迹：`gen_agv_ref_path.m`；产物：`path_straight.mat`, `path_turn.mat`, `path_straight_turn.mat`, `path_slope.mat`, `path_bumpy.mat`
    - GRU：`GRU_*.m` 系列脚本与 `GRU_*.mat` 产物
    - 优化：`Bayesian_Optimization.m`, `Cost_Function.m`, `start_bayesian.m`；产物：`maps_best.mat`
    - Simulink：`LPVMPC_AGV_simulink.slx`, `GRU_DataGen.slx`, `test.slx`
    - 文档：`docs/`（本文件所在）
- 自动/中间产物目录：`slprj/`, `*_grt_rtw/`, `*.slxc`, `*.autosave`, `GRU_logs/` — 禁止手改、禁止提交自定义内容。
- 新增辅助脚本与配置：仍放置于根目录（与现状一致）。如需新建子目录，需评审后统一迁移。
- 新产物命名与位置需延续现有惯例：
    - 线性化库：`plant_grid.mat`（可添加版本尾缀）；
    - 参考路径：`path_<type>.mat`；
    - 优化结果：`maps_best.mat`；
    - 其余 `.mat` 产物放根目录并含 `meta` 字段（生成时间、参数、版本、作者）。

## 7. 文档与“代码导航”协作（func.md）
- 生成/修改业务代码前，必须先阅读根目录 `func.md`。
- 新增或修改任意 Service/Manager/脚本/接口，必须同步更新 `func.md` 条目：层级/路径/职责/签名/输入输出/备注。
- CI 建议：若新增 `.m` 但未更新 `func.md`，阻断合入。

## 8. 提交与留痕（Git 规范要点）
- 提交标题：`<type>(<module>): <简要描述>`，如 `feat(mpc): 支持 ρ 三线性插值`。
- 类型：`feat|fix|refactor|doc|test|chore|style|perf`；破坏性修改用 `!` 或 `BREAKING CHANGE:` 段。
- 提交正文应包含：Context/Changes/Impact/Verification/Artifacts/Migration/Refs 等结构化段（详见 `docs/change.md` 模板）。

## 9. 交付清单
- 代码（含注释与版本头）。
- `.mat` 产物（含 `meta` 字段）。
- `func.md` 导航更新。
- 报告（图表脚本生成，保证可复现）。

## 10. 数值与稳健性通用约定
- 小量保护：`v_sat=max(v,1e-3)` 参与曲率与除法。
- 过滤与驻留：调度量与分类器输出使用一阶滤波与最小驻留时间以抑制抖动。
- 失败兜底：一旦出现 NaN/Inf 或求解失败，立即终止该回合并返回大代价用于调参流程。

## 11. 扩展补充（可选增强规范）
- MATLAB 版本与兼容：建议在 `parameters.m` 顶部注明测试版本（示例：R2023b）；出现版本相关差异需在 `change.md` 标记。 
- `.mat` 产物元信息：统一使用 `meta` 字段：`meta.version`, `meta.generated_at`, `meta.source_script`, `meta.params_hash`（可用 `DataHash` 若安装），`meta.author`。缺失不阻断，但优化/调试优先。 
- 错误处理：所有核心入口脚本（`mpc_setup_single_interp.m`, `lin_agv_grid.m`, `GRU_train.m`, `Cost_Function.m`）在输入校验失败时使用 `error(...)` 而非静默返回；调参场景可用 `warning` + 继续。 
- 日志格式建议（文本或 MAT）：结构数组字段：`t, rho, u, status, solve_time_ms, slack, e_y, e_psi, e_v, e_omega`，便于统一分析。 
- 性能基线：单步 MPC 求解 P95 < 2 ms（当前目标）若超过需记录 `change.md` 并触发优化任务。 
- 命名前缀：调度相关变量统一前缀 `rho_`（如 `rho_raw`, `rho_f`, `rho_n`）；权重映射使用 `maps.Q_range`, `maps.R_range` 等。 
- 断言与数值卫士：推荐在更新模型前添加：`assert(all(isfinite(upd.A(:))), 'A contains NaN/Inf')` 等，调试阶段可暂用。 
- 可追溯性：重要脚本末尾可写入 `fprintf('[TRACE] %s generated %s\n', mfilename, out_file);` 供日志聚合。
