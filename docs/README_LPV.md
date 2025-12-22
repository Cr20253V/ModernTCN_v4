# README_LPV.md（增强版）
> 用于指导 LPV 建模、线性化与插值。统一约定如下：
- ρ（调度变量）统一为有符号：`rho=[v, omega, theta]`
- 颠簸默认幅值：`0.2 rad`

## 1. 参数脚本 `parameters.m`
### 1.1 功能
集中定义车辆/执行器/摩擦/坡度等参数，并**预计算匀速平衡力 F_cmd**（含滚阻/空气阻力/坡度分量），为线性化与仿真提供一致入口。

### 1.2 接口
- 形式：**函数** `function params = parameters()`
- 输出：结构体 `params`，包含：
  - `Ts`(double, s), `mass`(kg), `Iz`(kg·m²), 轮距/轴距、最大舵角、最大角速率、最大电流等；
  - `friction` 子结构（滚阻系数 C_r、空气阻力系数 C_d·A、ρ_air）；
  - `slope` 默认设置；
  - `F_cmd_eq`(N)：**匀速平衡力**；
  - `limits` 子结构（电流/加速度/舵角/角速率上界）；
  - `meta`：版本、日期。

### 1.3 实现要点
1. 以 `v_eq=1 m/s` 为默认匀速点；`F_cmd_eq = m*g*sin(theta) + m*C_r*g*cos(theta) + 0.5*ρ*C_dA*v_eq^2`；
2. 返回 `params`；记录 `meta.generated_by='parameters.m'`。

---

## 2. 目标路径生成 `gen_path_*.m`
为 5 种状态生成 dataset（Signal Editor 可识别）：**直行、转弯、直+弯、坡度直行、颠簸直行**。持续 20 s，v 从 1 m/s 启动；转弯半径 10 m；颠簸叠加 0.2·sin(t)。

### 2.1 公共接口
- 形式：**函数** `function ds = gen_path_xxx(params)`
- 输入：`params`（见 §1）
- 输出：`ds`（Simulink `dataset`）：
  - `ref` = `[X, Y, ψ, v, ω]`（行向量信号）
  - `md` = `theta_ground`（坡度角，rad）
- 产物：保存 `paths/path_xxx.mat`，字段 `{ds, meta}`。

### 2.2 具体脚本
- `gen_path_straight.m`、`gen_path_turn.m`、`gen_path_straight_turn.m`、`gen_path_slope.m`、`gen_path_bumpy.m`

---

## 3. 线性化脚本
> 非线性 AGV -> 线性/LPV 模型。矩阵维度：A(8×8), B(8×3), C(8×8), D(8×3)。

### 3.1 通用依赖
- `parameters.m`、非线性模型 `state_eq.m`、输出方程 `output_eq.m`；
- 数值线性化：有限差分/符号法（任选其一，但需在 `meta.method` 留痕）。

### 3.2 典型点线性化 `linearize_typical.m`
- **功能**：三种工况（直行/转弯/坡度直行）**单点**线性化。
- **接口**：
  ```matlab
  function out = linearize_typical(params, op)
  % op: struct，含字段：mode∈{'straight','turn','slope'}, x0(8×1), u0(3×1), theta0(rad)
  % out: struct，含 A,B,C,D, x0,u0, valid_range, meta
  ```
- **流程**：
  1) 载入 `params` 与 `op`；2) 在 `(x0,u0,theta0)` 处数值线性化；
  3) 构造 `out.ABcd` 并附 `valid_range`（速度/舵角/坡度的有效区间说明）；
  4) `save('lin/lin_typical_<mode>.mat','out')`。

### 3.3 多点线性化（颠簸）`linearize_bumpy.m`
- **功能**：在网格 `v∈[0.8,1.0,1.2]`、`theta∈[-0.2,-0.1,0,0.1,0.2]`、`a∈[-1,-0.5,0,0.5,1]` 上线性化。
- **接口**：
  ```matlab
  function out = linearize_bumpy(params, grid)
  % grid: struct，含 v_grid(1×3), theta_grid(1×5), a_grid(1×5)
  % out: struct，含 sys_list{Nv×Nθ×Na}.(A,B,C,D,x0,u0), points=[v,theta,a], meta
  ```
- **流程**：
  1) 生成网格点；2) 对每点线性化并填充 `sys_list`；
  3) 附 `points`（每行 [v,theta,a]）；
  4) `save('lin/lin_bumpy_grid.mat','out')`。

---

## 4. LPV 数据结构与插值
- **目标**：把 §3 产物统一组织为 LPV 调度模型数据：
  ```matlab
  LPV.AB = @(rho) ... % 插值器或顶点选择
  LPV.rho = [v, abs(omega), theta_hat, mu_hat]; % 可按场景裁剪
  LPV.meta = struct('type','grid'|'polytopic','smoothing','on','rho_rate_limit',[...]);
  ```
- **要求**：提供 `build_lpv_model.m`，从 `lin/*.mat` 读取，构建插值/多面体描述并校验维度一致性；`save('lin/lpv_model.mat','LPV')`。
- `mpc_update_from_rho` 支持 α/β 形状参数与 factor_*，可三线性插值 A..E 并返回 `Bv=E(rho)`

---

## 5. MPC 设计脚本 `design_mpc_*.m`
### 5.1 公共接口与目标
- **接口**：
  ```matlab
  function mpc_cfg = design_mpc_<scene>(params, LPV, opts)
  % scene ∈ {straight, turn, slope, bumpy}
  % mpc_cfg: struct（QP 权重/约束/P/M/求解器/调度策略/软约束罚因子等）
  ```
- **控制目标**：
  - 轨迹：最小化 (X,Y) 跟踪误差；速度趋近 1 m/s；
  - 平顺：抑制 Δu、加速度与转角速率；
  - 约束：电流/加速度/转角/角速率（硬/软约束并行实现，软约束惩罚项 ≥ 1e3 起始）。

### 5.2 调度与可行性保障
- **调度变量** `rho=[v,|omega|,theta_hat,mu_hat] (subset)`；
- **调度可信域 TR-LPVMPC**：在 QP 中对 `||rho(k)-rho(k-1)||` 设软约束或在外环加一阶滤波与最小驻留时间；
- **Tube 收缩（可选）**：对位置/速度/转向约束做收缩，半径来源于建模误差上界；
- **DOB/ESO（可选）**：估计合成扰动并前馈。

### 5.3 场景化差异
- `design_mpc_straight.m`：P/M **较长**（例：P≥25, M≥5）；
- `design_mpc_turn.m`：P/M **较短**（例：P≈15, M≈3），加大转角速率惩罚；
- `design_mpc_slope.m`：对 `theta_hat` 敏感，允许较大 `md` 变化；
- `design_mpc_bumpy.m`：基于多点 LPV，开启 TR 与（可选）Tube。

### 5.4 产物
- 保存 `mpc/mpc_<scene>.mat`，包含：`mpc_cfg` 与 `meta`（Ts/P/M/Q/R/罚因子/约束/求解器/调度策略/版本/时间）。

---

## 6. 在线控制与仿真接线
- **接口函数**：`mpc_step.m(params, mpc_cfg, LPV, ref, md, x)` → `u`；内部完成调度、QP 求解、rate-limit；
- **Signal 接口**：`ref=[X Y psi v omega]`，`md=theta_ground`；
- **日志**：每步记录 `rho, slack, solve_time, status` 至环路日志。
- 脚本版：每步将 A/B/C/D 覆盖为 `upd.*`，MD 通道使用 `upd.Bv`；权重可在线覆盖
- Simulink 版：Adaptive MPC 自定义更新函数应用 `A..D,Bv`；权重/约束由外部端口覆盖

---

## 7. 贝叶斯优化 `bo_mpc_*.m`
- **接口**：`function best = bo_mpc_<scene>(params, LPV, init_cfg)`；
- **可调集合**：`Q,R,软约束罚因子,P,M,rho_rate_limit`；
- **指标**：综合加权（轨迹 RMSE、Δu 均方、约束违例率、平均求解时间）；
- **回写**：更新 `mpc/mpc_<scene>.mat` 中的 `mpc_cfg`。
- 根目录：`Cost_Function.m`、`Bayesian_Optimization.m`、`maps_best.mat`
- 变量集：`Q0,R0,dR0, alpha/beta 形状, scale_umin/umax, tau`
- 失败处理：单场景失败记 1e6，不中断其它场景；总失败标记

---

## 8. AI 工况识别（GRU / 1D-CNN）
### 8.1 数据生成与预处理
- `gen_train_data.m(params, scenario)`：基于仿真批量生成样本，字段包含时间戳/状态/输入/坡度标签。
- 预处理：标准化/滑窗切片（GRU/CNN 输入形状明确）。

### 8.2 GRU
- **训练接口**：`train_gru.m(data, opts)` → `model_gru.mat`；
- **输入张量**：`[batch, seq_len, feat_dim]`；
- **输出**：多任务（分类：直行/打滑/堵转/上下坡；回归：θ̂）。
- **部署接口**：`infer_gru.m(x_t_seq)` → `label, theta_hat, conf`；**推理时间**统计入日志。

### 8.3 1D-CNN
- **训练接口**：`train_cnn.m(data, opts)` → `model_cnn.mat`；
- 其它同 GRU。

### 8.4 与控制耦合
- `state_classifier.m(x)`：封装对 GRU/CNN 的调用，输出 `label, theta_hat, mu_hat(optional)`；
- 与 MPC 调度：将 `theta_hat, mu_hat` 注入 `rho`，并通过**一阶滤波+最小驻留时间**防抖。

---

## 9. 文档化与“代码导航”协作（func.md）
> 目标：像“图书馆检索”一样，让 Cursor/代理在**生成业务代码前**先查是否已有实现，避免重复造轮子。

### 9.1 强制校验流程
1) **第一步必须主动查看 `func.md`**；  
2) 通过工具（如 `read_file`）读取 `func.md` 全文，确认是否存在相关功能/服务/脚本；  
3) 若已存在：应复用/封装/重构，**不得**并行实现重复功能；若需更改，先评审再修改。

### 9.2 维护规则（更新时机与内容）
- **任何新增或修改** Service/Manager/Mapper/脚本/模型接口，**同步更新 `func.md`**；
- 每条目内容包括：**层级/路径/名称/职责简述/关键方法签名/输入输出/备注**；
- 允许为 MATLAB 组件与 Simulink 模块建条目；
- 推荐条目排序：模块 → 层（gen/design/train/deploy/bo/lin）→ 文件。

### 9.3 `func.md` 的推荐结构（模板）
```markdown
# 功能/类/脚本导航（func.md）
> 生成/修改业务代码前，**必须先阅读**本文件。

## 约定
- 统一单位 m, m/s, rad；Ts 见 parameters.m
- 关键名词：ref=[X Y psi v omega], md=theta_ground

---

## 模块：core/models
### 脚本
- **parameters.m**
  - 路径：core/models/parameters.m
  - 职责：集中参数定义与 F_cmd 预计算
  - 关键接口：`params = parameters()`
  - 产物：结构体 params
- **state_eq.m / output_eq.m**
  - ...（同上格式）

## 模块：lin（线性化）
- **linearize_typical.m**
  - 路径：lin/linearize_typical.m
  - 职责：直行/转弯/坡度直行典型点线性化
  - 关键接口：`out = linearize_typical(params, op)`
  - 产物：`lin/lin_typical_<mode>.mat`（A,B,C,D,meta）

- **linearize_bumpy.m**
  - 路径：lin/linearize_bumpy.m
  - 职责：颠簸直行多点线性化（v/theta/a 网格）
  - 关键接口：`out = linearize_bumpy(params, grid)`
  - 产物：`lin/lin_bumpy_grid.mat`（sys_list, points, meta）

## 模块：mpc（控制器）
- **design_mpc_straight.m**
  - 路径：mpc/design_mpc_straight.m
  - 职责：平地直行 MPC 设计（P/M 较长，速度平顺优先）
  - 关键接口：`cfg = design_mpc_straight(params, LPV, opts)`
  - 产物：`mpc/mpc_straight.mat`（cfg, meta）
- **design_mpc_turn.m** / **design_mpc_slope.m** / **design_mpc_bumpy.m**
  - ...（同上格式）

## 模块：paths（参考轨迹）
- **gen_path_*.m**
  - 路径：paths/gen_path_*.m
  - 职责：生成 dataset（ref, md）
  - 关键接口：`ds = gen_path_xxx(params)`
  - 产物：`paths/path_xxx.mat`

## 模块：bo（调参）
- **bo_mpc_*.m**
  - 路径：bo/bo_mpc_*.m
  - 职责：贝叶斯优化各场景 MPC 参数
  - 关键接口：`best = bo_mpc_<scene>(params, LPV, init_cfg)`
  - 产物：更新 `mpc/mpc_<scene>.mat`

## 模块：ai（工况识别）
- **train_gru.m / infer_gru.m**
  - 路径：ai/gru/*.m
  - 职责：GRU 训练与推理（分类+坡度回归）
- **train_cnn.m / infer_cnn.m**
  - 路径：ai/cnn/*.m
  - 职责：1D-CNN 训练与推理
- **state_classifier.m**
  - 路径：ai/runtime/state_classifier.m
  - 职责：统一推理接口（含防抖/驻留时间）
```

### 9.4 产物与校验
- `func.md` 存放于仓库根目录；任何 PR 必须更新相关条目；
- 在 CI 中加入钩子：若新增 `.m` 但 `func.md` 未更新则拒绝合入。

---

## 10. 代码注释规范（脚本/函数头部模板）
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

---

## 11. 目录建议（可按需调整）
```
core/models/          % parameters, state_eq, output_eq
paths/                % gen_path_*.m 与 .mat
lin/                  % linearization 产物与脚本
lin/logs/             % 线性化留痕
mpc/                  % design_mpc_*.m 与 .mat
bo/                   % bo_mpc_*.m
ai/gru/ ai/cnn/       % 训练与推理
ai/runtime/           % 在线推理封装
sim/                  % 联调脚本
docs/                 % 报告与说明
```

---

## 12. 交付清单（每阶段）
- 代码（含注释与版本头）；
- 产物 `.mat` 与 `meta` 字段；
- `func.md` 导航更新；
- 报告（图表脚本生成，可复现）。
