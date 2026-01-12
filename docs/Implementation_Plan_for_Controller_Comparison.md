# 控制器对比测试实现计划（LPVMPC+GRU vs LPVMPC+IMU vs 非线性MPC）

日期：2026-01-02

## 0.1 实验取向声明（对比公平性与目标）
本对比实验的主要目标是凸显 **LPVMPC+GRU** 在坡度/工况估计与闭环控制表现上的优势。因此：

- **IMU 分支将采用“弱基线”实现**：使用最小工程量、可运行且可解释的单 IMU 方案，而非追求最优的姿态融合/多传感器融合。
- **原因需要在报告中明确标注**：IMU 估计理论上可以做得更完善（例如加入更完整的姿态融合/漂移抑制），但本实验选择弱基线是为了突出 GRU 的优势与工程价值。
- **边界条件**：弱基线不应被做成“明显不合理/无法运行”的稻草人；应保证同一组路径下能稳定闭环，并输出完整日志契约。

该声明将用于解释：IMU 分支可能存在累计漂移等局限性，这属于预期现象，不作为实现缺陷。

## 0. 背景与目标
当前工程已实现 **LPV-MPC + GRU** 用于 AGV 路径跟踪与坡度角估计/调度（Simulink 模型：`simulink/LPVMPC_AGV_simulink.slx`）。后续需要引入：

- **LPVMPC + 单IMU**（用 IMU 估计坡度/工况，替代 GRU 输出的 `theta_hat`）
- **非线性MPC（NMPC）** 控制器

并要求：

- 在 **相同目标路径** 下，对比三种控制方式的 **性能指标**
- 对比过程 **可复现**、**可批量运行**、**可扩展**（未来再加控制器不重写评估框架）


## 1. 现有工程可复用基础
工程已具备“批量闭环仿真 + 指标解析”的入口：

- 闭环评估入口脚本：`src/tests/test_closed_loop_performance.m`
  - 能按场景/路径批量仿真并从 `logsout` 中抽取指标
  - 当前用于“对比不同 GRU 或控制配置”
- GRU 在线推理封装：`src/gru/GRU_state_classifier.m`
  - 能从 plant 输出 `y_raw (31×1)` 估计 `theta_hat`、`label_main`、`label_turn`
- MPC 创建：`src/mpc/mpc_setup_single_interp.m`
  - 创建 Adaptive MPC 控制器（含可选 MD 通道 theta）

因此，本计划的关键不是“从零写评估”，而是：

1) **采用“三模型分叉”**：为三种控制策略各自维护一个仿真模型（减少耦合、便于独立调参/调试）
2) **统一日志信号契约**：三个模型必须输出同名 `logsout` 信号，保证指标解析脚本可复用
3) **统一批量运行入口**：用一个 MATLAB 脚本驱动 model × scenario × repeat 的批量仿真，并产出统一 summary


## 2. 对比测试的总体架构（推荐：模型三分叉）
建议把对比测试拆成三层：

### 2.1 模型层（Simulink：三分叉）
目标：为三种控制策略分别维护 3 个仿真模型（入口、日志契约一致）：

- `LPVMPC_AGV_simulink_GRU.slx`：LPVMPC + GRU（基线）
- `LPVMPC_AGV_simulink_IMU.slx`：LPVMPC + 单IMU（仅替换坡度估计链路）
- `LPVMPC_AGV_simulink_NMPC.slx`：非线性MPC（独立控制器子系统）

> 命名建议：以上为建议命名；你也可以保留原模型名，用 `_GRU/_IMU/_NMPC` 后缀建立副本。

关键要求（决定对比能否自动化）：
- 三个模型必须输出 **同名** 的信号到 `logsout`（详见第3节“日志信号契约”）
- 三个模型必须支持同一套仿真注入参数：路径变量 `ref`/`agv_ref_path`、StopTime、噪声开关、随机种子等

可选（非必须）：
- 未来如果维护成本过高，可再回收为单模型 Variant/Switch；但首期以三分叉为主，降低耦合风险。


### 2.2 运行层（MATLAB 脚本：统一驱动三模型）
目标：提供统一入口，一键跑完：

- 模型集合（建议用 map 管理）：
  - `lpvmpc_gru  -> simulink/LPVMPC_AGV_simulink_GRU`
  - `lpvmpc_imu  -> simulink/LPVMPC_AGV_simulink_IMU`
  - `nmpc        -> simulink/LPVMPC_AGV_simulink_NMPC`
- 路径集合：来自 `data/paths/path_*.mat` 或自定义
- 每条路径重复次数 N（用于统计均值/方差）

并保存：
- 每次仿真的 `timeseries_*.mat`（可选）
- 一份可对比的 `summary.mat`（带 controller 维度）

实现建议（与现状脚本关系）：
- 不直接在 `src/tests/test_closed_loop_performance.m` 上“硬改到底”，而是以它为基础新建一个脚本（例如 `src/tests/run_controller_comparison_batch.m`），只保留可复用的信号抽取与结果结构。
- `test_closed_loop_performance.m` 作为参考/回归脚本保留，避免影响既有流程。


### 2.3 评估/报告层（后处理脚本）
目标：读取一个或多个 `summary.mat`，生成：

- 指标对比表（每条路径 × 每种控制器）
- 汇总统计（均值/方差/最差值）
- 关键曲线对比图（同路径叠加）


## 3. 统一“日志信号契约”（必须先冻结）
要做到自动对比，最关键的是：三种控制方式输出同一套 `logsout` 信号名。

现有 `test_closed_loop_performance.m` 内部已通过 `signal_names` 映射做了解析；后续要把它提升为**项目级契约**。

本项目选择：**在 `logsout` 中统一记录 `diag.*` 命名空间信号**（即信号名带 `diag.` 前缀）。

这样做的原因：
- 你当前已按 `diag.X/diag.e_y/...` 的方式添加日志，沿用可减少后续反复改名
- 诊断信号集中在同一命名空间，便于脚本批量抽取与版本演进

建议统一至少包含：

### 3.1 跟踪相关
- `diag.X, diag.Y, diag.psi, diag.v, diag.omega`（实际状态）
- `diag.X_ref, diag.Y_ref, diag.psi_ref, diag.v_ref, diag.omega_ref`（参考）
- `diag.e_y, diag.e_psi, diag.e_v, diag.e_omega`（误差向量，统一来自 Global2PathError）

信号来源建议（与当前 LPVMPC+GRU 模型对齐）：
- `diag.X, diag.Y, diag.psi, diag.v, diag.omega`：来自 plant 输出总线 `C`，其顺序固定为 `C=[X, Y, psi, v, omega]`
- `diag.e_y, diag.e_psi, diag.e_v, diag.e_omega`：统一来自 `Global2PathError` 输出（当前实现为 4 维）

### 3.2 控制相关
- `diag.F_cmd, diag.omega_cmd`（控制器输出）
- `du` 或 `dF_cmd/domega_cmd`（若有）
- `sat_flag` 或饱和比例（若能记录）

### 3.3 估计/调度相关
- `diag.theta_ground`（真值；用于分析，不一定给控制器用）
- `diag.theta_hat`（控制器最终使用的坡度估计；无论来自 GRU 还是 IMU，都叫 `theta_hat`）
- `diag.rho_f`（调度滤波输出；当前模型为 `rho_f=[v_f; omega_f; theta_f]`）
- `diag.rho_n`（可选，仅监控/调试用的归一化量；不参与 UpdatePlantModel）
- `diag.y_wt, diag.u_wt, diag.du_wt, diag.umin, diag.umax`（可选：在线权重/约束调度输出；用于解释性能差异）
- `diag.F_limit`（力限幅，供饱和占比计算；若上下限不对称，建议同时记录正负限或取绝对最大值）

### 3.4 计算性能
- `diag.solve_time_ms`（控制器求解耗时；尽量接近优化器时间）
- `diag.total_step_time_ms`（可选：每步总耗时/墙钟时间；包含模型与 GRU 的额外开销，用于解释整体实时性）

> 说明：
> - 对于 NMPC：需要输出 `diag.solve_time_ms`；若可行也输出 `diag.total_step_time_ms`。
> - 对于 LPVMPC：若暂时无法从 Adaptive MPC Controller 块直接拿到求解耗时，可先在脚本侧测量并写入结果结构；但 `diag.total_step_time_ms` 仍可作为“端到端耗时”先行记录。


## 4. 指标体系（建议首版必选 + 可选扩展）
为避免指标爆炸，建议分两层。

### 4.1 首版必选（建议对比最小集合）
**跟踪精度**
- 横向误差 `e_y`：RMS、峰值（Peak）、稳态均值（最后 10% 时间窗）
- 航向误差 `e_psi`：RMS、峰值
- 速度误差 `v_ref - v`：RMS、峰值

**控制代价/平顺性**
- `|F_cmd|` 峰值
- `|omega_cmd|` 峰值
- 控制变化率 RMS（例如 `diff(F_cmd)/Ts`、`diff(omega_cmd)/Ts`）

**约束/鲁棒性**
- 饱和占比：`|F_cmd| > 0.95*F_limit` 的时间比例
- 仿真失败/求解失败次数（feasible/optimal 以外视为失败）

**计算复杂度**
- 求解耗时均值、95分位、最大值

### 4.2 可选扩展（第二阶段再加）
- 能耗/力功：`∫ |F_cmd * v| dt` 或近似功耗
- jerk/舒适性：`d²u/dt²` 的统计
- 工况识别准确率（对 GRU/IMU 的 label 也可对比，但这属于“识别系统”评估）


## 5. 三种控制方式的实现落点

### 5.1 LPVMPC + GRU（已存在）
- GRU 输出：`theta_hat`（来自 `GRU_State_Classifier` 块）
- MPC 使用：`md = theta_hat`，`rho=[v,omega,theta_hat]`（或其滤波版本）

这个作为基线，不建议大改。

#### 5.1.1 基线模型“关键模块接口”（基于你提供的接线图/代码，建议写入对比契约）
为保证 IMU/NMPC 分叉模型能做到“最小改动 + 完全可比”，建议把下列接口约定显式写入本计划，并在三个模型中尽量保持一致。

**(1) RhoFilter（调度变量滤波）**
- 函数签名：`[rho_f, rho_n] = RhoFilter(v_in, omega_in, theta_in, Ts, tau)`
- 输出：`rho_f=[v_f; w_f; t_f]`，其中 `v_f=max(v_in,0)`（速度负值被截断），`rho_n` 仅用于监控
- 当前接线确认：`theta_in` 使用 `theta_hat`（来自 GRU 在线估计输出），因此 `rho_f` 的第三维是 `theta_hat` 的一阶滤波值
- 对比建议：
  - 三个模型统一记录 `rho_f`（以及可选 `rho_n`），方便解释权重/约束调度差异
  - 若未来存在倒车/负速度场景，需要评估 `max(v_in,0)` 是否会引入不可比性（当前对比路径若都为前进，可先不改）

**(2) UpdatePlantModel（LPV 在线插值 + 权重/约束调度输出）**
- 函数签名：`[plant, y_wt, u_wt, du_wt, ecr_wt, umin, umax] = UpdatePlantModel(rho, db_rt, MPC_idx, ff_rt, v_ff_nom)`
- 关键行为：
  - `plant.B=[Bmv,Bmd]`，把坡度作为 1 个 MD 通道（`nd=1`）
  - 同时输出 `y_wt/u_wt/du_wt` 与 `umin/umax` 供 Adaptive MPC 使用
- 风险/优化点（会影响“对比公平性”）：
  - 你当前代码里 `maps_local` 是函数内部硬编码（`enable_weight_interp=true`，以及固定 range/scale）。而 PreLoadFcn 又加载了 `maps_best` 并写入 `ctrl.maps`。
  - 建议在计划中明确：对比版本要么“统一用 maps_best→ctrl.maps→mpc_update_from_rho 的调度”，要么“统一用 UpdatePlantModel 内置 maps_local”。避免 GRU/IMU/NMPC 三套逻辑不一致导致不可比。
  - 建议把 `y_wt/u_wt/du_wt/umin/umax` 纳入 `logsout`（至少保存统计量或关键时刻），用于复盘“性能差异来自估计还是来自调度范围”。

**(3) Global2PathError（误差向量）**
- 你提供的实现实际输出为 4 维：`y_e=[e_y; e_psi; e_v; e_omega]`（代码注释里提到 `e_s`，但当前未输出）
- 对比建议：
  - 统一把 `e_y/e_psi/e_v/e_omega` 作为日志契约的误差来源（不要在不同模型里重复实现不同误差定义）
  - 若后续确实需要 `e_s`（进度误差），应在三模型同步增加并纳入契约

**(4) GRU_State_Classifier（在线坡度/工况识别）**
- 当前 MATLAB Function 通过 `coder.extrinsic + evalin/assignin` 与基础工作区交互（每步写 `gru_out_temp` 再读字段）。
- 风险/优化点（对批量仿真影响很大）：
  - **并行仿真不安全**：`assignin('base',...)` 会导致不同 worker/不同 run 之间相互覆盖，基本无法用 `parsim` 做并行。
  - **仿真性能开销**：频繁 `evalin/assignin` 会显著拖慢仿真，影响“计算耗时”指标的公平对比。
  - 计划建议：
    - 首版对比若只做串行 batch，可先保留现状，但要在报告里说明“GRU 分支包含额外 MATLAB 工作区开销”。
    - 若要做公平的计算耗时对比，建议把 GRU block 改为“无 base workspace 副作用”的输出路径（例如直接从 `out` 结构体提取数值，或将推理封装到不依赖 base ws 的函数接口），这样才能启用 `parsim` 并减少额外开销。

**(5) PreLoadFcn（初始化/数据加载）**
- 当前 PreLoadFcn 负责：`init_project()`、加载 `params/db_rt/ctrl/maps_best/gru_model`、创建 `MPCPlantBus`。
- 对比建议：
  - 三分叉模型要保持“相同的初始化语义”（尤其 `db_rt/ctrl/maps_best`），否则出现“模型A用的是旧数据库/旧权重”的不可复现问题。
  - 批量仿真脚本建议采用：`load_system` 一次 + 尽可能使用 Fast Restart（前提是模型结构不变且变量注入方式稳定）。


### 5.2 LPVMPC + 单IMU（推荐作为第一步新增）
目标：仅替换 `theta_hat` 来源，使对比尽可能“控制变量法”。

**做法建议（弱基线，最小可行）**：
- 采用“陀螺积分 + 轻微泄漏/低通”的最简 IMU 估计（刻意不引入更完整的姿态融合），以凸显 GRU 的优势。
- 具体形式可沿用工程中已有思路（示意）：
  - `theta_hat = (1-α)*theta_hat_prev + α*(theta_hat_prev + gyro_y*Ts)`
  - 或 `theta_hat = λ*theta_hat_prev + gyro_y*Ts`（带泄漏项 λ<1）
  - 其中 `gyro_y` 来自 `y_raw(10)`（工程已有定义）
- 在 Simulink IMU 分叉模型内新增轻量 `IMU_Theta_Estimator`（MATLAB Function）输出：
  - `theta_hat`（单位 rad；命名保持与 GRU 分支一致，便于复用 UpdatePlantModel/RhoFilter/日志契约）

**预期局限性（需在报告中标注原因）**：
- 仅陀螺积分会存在累计漂移；本实验接受该现象，因为目标是突出 GRU 的优势。
- 若漂移导致闭环不稳定，可引入“最小必要的工程性约束”（仍保持弱基线定位）：
  - `theta_hat` 限幅（例如 ±10° 或按模型实际坡度范围设定）
  - 起始/分段重置策略（例如每条路径 run 初始重置为 0）
  - 可选：非常弱的回零项（避免无界漂移），但不做复杂融合

重要约束：
- 对比时保持 MPC 参数（Q/R/dR/约束等）一致，避免把“估计差异”和“控制器调参差异”混在一起。


### 5.3 非线性MPC（实现路线取决于工具箱）
这里分两条路线，建议先确认你本机是否有 Nonlinear MPC Toolbox：

**路线A：有 Nonlinear MPC Toolbox（首选）**
- 在 Simulink 中使用 Nonlinear MPC Controller 块或 MATLAB 中 `nlmpc` 对象
- 状态模型用工程现有的 `state_eq.m`（或 `state_eq_ref.m`）
- 输出/参考与约束映射到 `F_cmd, omega_cmd`

**路线B：无工具箱（MVP 方案）**
- 先在 MATLAB 脚本层实现“离线/仿真式 NMPC”（每步 `fmincon` 求解）
- 生成同样格式的 `sim_out` 或至少生成指标所需时序
- 待可用后，再决定是否集成回 Simulink

无论哪条路线，必须满足：
- 统一日志：输出 `F_cmd, omega_cmd, solve_time_ms, e_y, e_psi, v` 等
- 统一约束：输入限幅、变化率限幅（尽量对齐 LPVMPC）


## 6. 批量对比脚本的改造方案
建议以 `src/tests/test_closed_loop_performance.m` 为基础，新建脚本实现“多模型驱动”的批量评估入口（避免影响现有脚本的历史用途）。

建议脚本名：`src/tests/run_controller_comparison_batch.m`（可调整）

### 6.1 cfg 结构体扩展
新增字段建议：
- `cfg.controller_variants`：例如 `{'lpvmpc_gru','lpvmpc_imu','nmpc'}`（逻辑标签，用于索引模型与结果）
- `cfg.model_map`：例如 `struct('lpvmpc_gru','LPVMPC_AGV_simulink_GRU', 'lpvmpc_imu','LPVMPC_AGV_simulink_IMU', 'nmpc','LPVMPC_AGV_simulink_NMPC')`
- `cfg.seed`：随机种子（保证噪声一致）
- `cfg.enable_noise`：是否启用测量噪声
- `cfg.save_timeseries`：每次仿真是否保存完整 `sim_out`

并建议新增（用于可复现与公平对比）：
- `cfg.rng_policy`：随机种子策略（固定/派生；见第9节）
- `cfg.metrics_window.steady_ratio`：稳态窗口比例（默认 0.10）
- `cfg.metrics.enable_core_tracking_metrics`：是否计算 `e_y/e_psi` 等核心指标（默认 true）

### 6.2 外层循环改为 model(controller) × scenario
现状：只循环 scenarios（且只面向单模型）。
改造后：
1) 循环 controller（标签）
2) 由 `cfg.model_map(controller)` 解析出对应的 **Simulink 模型名**，分别调用 `sim()`
3) 循环 scenario（含重复次数）
4) 每次仿真前注入 base workspace 变量（统一注入，三模型都要兼容），例如：
  - `ref` / `agv_ref_path`（参考路径结构体）
  - `params.enable_noise`（或单独的 `enable_noise`）
  - `rng(cfg.seed)`（或每次 run 固定 seed 派生）
  - GRU 模型：确保 `gru_model` 已加载；IMU/NMPC 模型可忽略该变量但不应报错

补充建议（与当前 GRU block 实现相关）：
- 如果未来希望启用 `parsim` 并行：尽量避免在模型运行过程中对 base workspace 做 `assignin/evalin`（至少要把 GRU/IMU 的在线估计链路改为“无副作用”）。
- 若先采用串行 batch：建议明确 `cfg.run_mode='serial'`，并将“GRU分支的额外 MATLAB 开销”与“控制器求解耗时”区分记录（例如同时记录 `mpc_solve_time_ms` 与 `total_step_time_ms`）。

### 6.3 结果结构统一
建议 summary 的核心结构：
- `summary.controllers(i).name`
- `summary.controllers(i).reports{j}`（每条路径/重复一次的 report）
- `summary.controllers(i).stats`（对每条路径与总体的聚合统计）

这样后处理脚本只需要遍历 `summary.controllers`。


## 7. 报告脚本（compare_controller_performance.m）
建议新增：`src/tests/compare_controller_performance.m`，职责：

- 输入：一个或多个 `closed_loop_summary_*.mat`
- 输出：
  - 对比表（.mat + .csv）
  - 曲线图（.png）
  - 汇总说明（.md 或 .txt）

推荐保存目录：`results/compare/<timestamp>/`。


## 8. 里程碑与验收标准（强烈建议按此推进）

### M0：工具箱与路线确认（0.1天）
- 目的：提前锁定 NMPC 路线，避免后期计划大改
- 建议执行：
  - `ver('mpc')`
  - `exist('nlmpc','file')` 或 `which nlmpc`（检查 `nlmpc` 函数是否可用）
- 验收：明确是否具备 Nonlinear MPC Toolbox；若缺失则直接采用路线B并在计划中调整 M5 工期预期

### M1：冻结日志契约（1天）
- 验收：基线 `lpvmpc_gru` 能输出契约内全部 `logsout` 信号

并行推进（建议同 M1 完成）：
- 指标计算函数同步补齐核心跟踪指标：`e_y_rms/e_y_peak/e_psi_rms`，以及控制变化率 RMS（`diff(F_cmd)/Ts`、`diff(omega_cmd)/Ts`）
- 明确随机种子机制并落到 `cfg` 与 `summary`（见第9节）

### M2：创建三分叉模型骨架（0.5~1天）
- 验收：三个模型都能加载同一路径并跑通到结束；三者 `logsout` 至少包含契约中“首版必需”的信号集合

### M3：实现 LPVMPC+IMU（0.5~1天）
- 验收：IMU 分叉模型在同一路径下能跑通，并输出同名 `theta_hat`

### M4：扩展批量仿真脚本为三控制器（1天）
- 验收：一条命令可跑完 controllers×scenarios×repeat，并输出 summary

### M5：引入 NMPC（2~5天，取决于工具箱与求解稳定性）
- 验收：NMPC 在至少 straight + turn 两类路径上稳定运行，且耗时统计可输出

### M6：报告与快测（1天）
- 验收：自动生成对比表与图；提供 quick config（短StopTime、少路径）可快速回归


## 9. 已确定参数 vs 待确定参数（先写死框架，便于后续落地）

### 9.1 已确定（当前信息足够，可直接写入实现）
- **plant 输出顺序**：`C=[X, Y, psi, v, omega]`
- **调度变量滤波输入**：`RhoFilter.theta_in = theta_hat`
- **误差定义来源**：`Global2PathError` 输出 `y_e=[e_y; e_psi; e_v; e_omega]`
- **模型初始化入口**：PreLoadFcn 负责加载 `params/db_rt/ctrl/maps_best/gru_model` 与创建 `MPCPlantBus`

### 9.2 待确定（需要你后续给出数值/策略，但现在先把字段写进计划与 cfg）
- **IMU 弱基线参数**：
  - 泄漏/低通系数：`λ` 或 `α`（默认 TBD）
  - 限幅范围：`theta_hat` 的最小/最大值（默认 TBD，建议与数据集/工况范围一致）
  - 重置策略：每个 run 初始化是否强制 `theta_hat=0`（默认 TBD）
- **噪声参数**：
  - `cfg.enable_noise`、噪声强度（默认 TBD；但必须同 seed 绑定并记录）
- **随机种子机制（必须冻结）**：
  - `cfg.seed_base`（默认 TBD）
  - seed 派生规则：建议 `seed = seed_base + hash(controller,scenario,repeat)` 或可复现的整数映射（默认 TBD）
  - `summary` 必须记录每次 run 的 seed 与噪声开关
- **指标计算窗口**：
  - 稳态窗口比例 `steady_ratio`（建议默认 0.10，若你有偏好可改）
- **计算耗时口径**：
  - 记录 `mpc_solve_time_ms`（控制器求解耗时）与可选 `total_step_time_ms`（含模型/GRU 开销）是否都需要（默认 TBD）


## 9. 风险与对策
- **NMPC 求解耗时/不可行**：先做短预测域、保守约束、设置超时与失败惩罚；优先跑 straight 再扩展。
- **日志信号不齐导致脚本报错**：先冻结契约再开发控制器，缺失信号必须在模型内补齐并保持同名。
- **公平性问题（调参差异）**：第一阶段强制使用同一套输入限幅/变化率限幅；NMPC 若需要不同权重，必须在报告中注明。
- **随机噪声影响可复现**：统一设置 `rng(cfg.seed)`，并在 summary 中记录 seed 与噪声开关。


## 10. 建议的下一步（最小可跑版本）
优先做：
1) 复制现有模型形成三分叉：`*_GRU / *_IMU / *_NMPC`（先保持其余部分一致）
2) 在三个模型中对齐并验证“日志信号契约”（先覆盖首版必选信号）
3) 在新脚本 `run_controller_comparison_batch.m` 中实现 `cfg.model_map`，按 controller 选择不同模型批量运行
4) 先跑 `straight`、repeat=1，验证三模型都能产出可解析的 summary

跑通后再引入 NMPC。

---

## 附录：实施进度日志

### 2026-01-03

#### M0：工具箱与路线确认 ✅
- [x] 检查 MPC Toolbox 可用性 — **可用**
- [x] 检查 Nonlinear MPC 可用性（`nlmpc` 函数存在性/可调用性）— **可用**
- [x] 确定 NMPC 实现路线 — **路线A（工具箱）**

#### M1：冻结日志契约（进行中）

**差距分析完成**：
- 现有 `test_closed_loop_performance.m` 的 `default_signal_names()` 仅映射 **7 个**信号：
  - `v`, `v_ref`, `theta_hat`, `theta_ground`, `theta_ref`, `label_main`, `F_cmd`
- 对比计划契约需补齐约 **15 个**信号

**Simulink 信号日志已添加**：
- [x] 跟踪状态：`diag.X`, `diag.Y`, `diag.psi`, `diag.v`, `diag.omega`
- [x] 路径误差：`diag.e_y`, `diag.e_psi`, `diag.e_v`, `diag.e_omega`
- [x] 参考值：`diag.X_ref`, `diag.Y_ref`, `diag.psi_ref`, `diag.v_ref`, `diag.omega_ref`
- [x] 控制输出：`diag.F_cmd`, `diag.omega_cmd`
- [x] 估计/调度：`diag.theta_hat`, `diag.theta_ground`, `diag.label_main`
- [ ] 求解耗时：`diag.solve_time_ms` — **暂未实现**（优先在脚本层面测量/记录）
- [ ] 每步总耗时：`diag.total_step_time_ms` — **暂未实现**（脚本层面更易先行实现，用于端到端实时性对比）

**待完成**：
- [ ] 新建 `run_controller_comparison_batch.m`（含新的 `default_signal_names()` 和 `analyze_results`）
- [ ] 扩展指标计算支持 `e_y_rms`, `e_psi_rms`, 控制变化率 RMS

**技术决策记录**：
1. 按计划 2.2 节，新建独立脚本而非修改 `test_closed_loop_performance.m`
2. 求解耗时首版设为可选，等三种控制器跑通后再统一补充
