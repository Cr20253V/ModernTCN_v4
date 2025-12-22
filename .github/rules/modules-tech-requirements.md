# 模块技术要求（LPV-MPC + GRU）

> 面向当前仓库现状（根目录为主），在不改变目录结构的前提下，细化各模块的接口、数据、算法与验证标准，便于后续调试与修改。

## 2. 参考路径生成（gen_agv_ref_path.m）

### 2.1 公共接口与参数
```matlab
function ref = gen_agv_ref_path(path_type, params)
% path_type ∈ {'straight','turn','straight_turn','slope','bumpy'}
% params: 结构体（优先使用 parameters() 输出），关键字段：
%   .Ts (秒)        采样周期（必需）
%   .T_end (秒)     轨迹时长（默认 20）
%   .R (米)         转弯半径（默认 10）
%   .v0 (m/s)       初速度（默认 1）
%   .theta0 (rad)   坡度常值（默认 0）
```
输出 `ref` 字段与单位：
- `t [N×1] (s)`；`X_ref, Y_ref [N×1] (m)`；`psi_ref [rad]`；`v_ref [m/s]`；`omega_ref [rad/s]`；`theta_ref [rad]`
- 误差参考：`e_y_ref, e_psi_ref, e_v_ref [N×1]`（通常为 0，供 MPC 用）
- 调度：`rho [N×3] = [v_ref, omega_ref, theta_ref]`（经一阶低通 τ≈0.3–0.5 s）

### 2.2 生成与保存
1) `t = (0:Ts:T_end)'`；2) 按类型生成轨迹（直线/转弯/直+弯/坡度/颠簸）；3) 计算 `psi_ref, v_ref, omega_ref`；4) 误差参考置 0；5) 构造并滤波 `rho`；6) 输出 `ref`；
7) 保存至根目录 `path_<type>.mat`，包含 `{ref, meta}`（meta: 生成时间、参数、版本、作者）。

直线：`X=v0*t, Y=0`；转弯：`X=R*sin(ωt), Y=R*(1-cos(ωt))`；直+弯：前 10 m 直线后接圆弧；坡度直线：直线+常值 `theta0`；颠簸直线：直线+`0.2*sin(t)` 扰动。

### 2.5 调度变量滤波说明
调度原始向量：`rho_raw = [v_ref, omega_ref, theta_ref]`。一阶低通：\(\tau \dot{\rho}_f + \rho_f = \rho_{raw}\)。离散实现：
```matlab
alpha = Ts/(tau+Ts);    % tau≈0.3–0.5 s
rho_f(k,:) = rho_f(k-1,:) + alpha*(rho_raw(k,:) - rho_f(k-1,:));
```
归一化：`rho_n = (rho_f - rho_min)./(rho_max - rho_min)`并裁剪到 `[0,1]`。`rho_min, rho_max` 由网格 `V_grid,W_grid,T_grid` 最值确定。

### 2.3 Simulink 对接（From Workspace）
- 路径全局参考（用于必要的可视化/外部模块）：`[X Y psi v omega]` 共 5 路。
- MPC 误差参考端口实际为 4×1，对应 `[e_y,e_psi,e_v,e_omega]`，常用零向量或误差目标。
- `ref_ts`: `time=t`, `signals.values` 按端口尺寸组织；若给误差参考则仅提供 4 列。
- 可直接将 `ref` 导出或生成 `ref_ts` 输入 `LPVMPC_AGV_simulink.slx`；端口尺寸以模型为准。

### 2.4 验收与自检
- 脚本：`test_gen_paths.m` 跑通；
- 产物：更新/覆盖根目录 `path_*.mat`；
- 维度：`numel(t)` 一致，无 NaN/Inf；`rho` 经过滤波。

---

## 3. 典型点线性化（lin_agv_grid.m / lin_agv_at_point.m）

### 3.1 接口与默认参数
```matlab
function db = lin_agv_grid(params, grid, opts)
% params: parameters() 结构体（物理/轮胎/采样等）；
% grid  : struct，字段 V_grid(Nv×1), W_grid(Nw×1), T_grid(Nt×1)  % ρ=[v,ω,θ]
% opts  : .coord='path', .disc='zoh'|'foh', .keep_E=true,
%         .export_mat='plant_grid.mat'  % 根目录，沿用现有产物命名
```
默认约定：
- 工作点 `ρ*=[v*, ω*, θ*]`，曲率 `κ*=ω*/max(v*,1e-3)`，误差为 0；
- 状态 `x=[e_y,e_psi,e_v,e_omega]^T (nx=4)`；输入 `u=[F_cmd,omega_cmd]^T (nu=2)`；输出 `y=[e_y,e_psi,e_v,e_omega]^T (ny=4)`；扰动 `d=[theta]^T (nd=1)` 进入 `E(ρ)`（纵向）。

### 3.2 数学与近似
- 纵向：`F_long = F_cmd - F_roll - F_aero(v) - m g sin(theta)`；
- 横向：小角侧偏线性 `F_y ≈ C_alpha·alpha`；
- 非线性开关：在工作点附近等效线性化，避免 A/B 出现离散切换。

### 3.3 离散化与导出
- `(Ac,Bc,Cc,Dc,Ec) → sysd=c2d(ss(Ac,Bc,Cc,Dc),Ts,opts.disc)`；
- 表结构：`db.grid.(V/W/T), db.Ts, db.A/B/C/D/E(i,j,k,:,:)`；
- 导出：`save(opts.export_mat,'-struct','db')`（根目录 `plant_grid.mat`）。

### 3.4 验证与回归
- 极点位于单位圆内或可被 MPC 稳定；
- `C` 与输出选择一致；
- `v→0, ω→0, |θ|→max` 数值稳定；
- 1–2 步预测与高保真 Plant 对比误差 ≤ 5%；
- 快速检查：若存在 `lin_agv_db.mat`/`plant_grid_test.mat`，用以对比维度与采样时间一致性。

日志建议：`lin_log(i,j,k).rho=[v;ω;θ]; lin_log(i,j,k).eig=eig(A);` 用于后续稳定性筛选。

### 3.5 失败与回退
- 若某工作点线性化结果含 NaN/Inf：记录并跳过该点；插值时自动由相邻点平滑补偿。
- 若极点模值最大 `>1.05`：可做谱缩放：`A = A * (0.99/max_abs_eig)`（保守修正）。
- 若 E(ρ) 维度不一致：抛出错误而非静默继续。

---

## 4. 自适应 MPC（mpc_setup_single_interp.m / mpc_update_from_rho.m）

### 4.1 控制器创建接口
```matlab
function ctrl = mpc_setup_single_interp(db, opts)
% 输入：db（线性化库），opts（Np,Nc,Q,R,dR,约束、软约束…）
% 流程：选 ρ 中心点基准模型 → mpc(ss(...)) → 设置 Weights/Constraints
% 输出：ctrl 结构，含 mpcobj 与（可选）权重/约束映射 maps
```

### 4.2 在线插值与模型更新接口
```matlab
function upd = mpc_update_from_rho(rho, db, maps)
% rho=[v;omega;theta]（有符号，前置一阶滤波 τ≈0.3–0.5 s）
% 步骤：ρ 归一化 → 角点与权重 → A..E 三线性插值 → （可选）Q/R/约束映射
% 返回：upd.A,B,C,D,E 及（可选）权重/约束更新项
```

### 4.3 Simulink 接线（Adaptive MPC）
- 测量输出 mo：`[e_y,e_psi,e_v,e_omega]`（4×1）。
- 参考 ref：实际为 4×1 零向量（误差趋零）或误差目标 `[e_y_ref,e_psi_ref,e_v_ref,e_omega_ref]`。
- 测量扰动 md：`theta_hat`（如启用 E(ρ)）。
- Scheduling：`rho_f=[v_f;ω_f;θ_f]`（一阶滤波后）。
- 自定义更新函数应用 `upd.A..E`；权重/约束可由外部端口或回调覆盖。

### 4.4 设计默认值与安全裁剪
- 预测/控制域：`Np≈2.0–3.0 s`，`Nc≈0.5–1.0 s`；
- 权重：`Q=diag([3,8,1,1])`，`R=diag([1e-3,1e-3])`，`dR=diag([1e-2,1e-2])`；
- 约束示例：`F∈[-Fmax,Fmax]`，`ω∈[-0.6,0.6]`，`|ΔF|≤400 N/步`，`|Δω|≤0.4 rad/s/步`；
- 小量保护：`v_sat=max(v,1e-3)`；所有权重/约束做边界裁剪防数值发散。

### 4.5 验证清单
- 固定 ρ 在角点处闭环可稳定；
- `straight→turn`（S 曲线≈2 s）与 `bumpy`（θ 正弦）场景切换平滑；
- 记录 `rho, solve_time, slack, status`；P95 求解时间满足目标。
失败兜底：插值后若 A/B/C/D 任意出现 NaN/Inf → 使用上一周期预测模型并递增失败计数；连续 ≥3 次进入安全模式（输出保持或限幅）。

### 4.6 代价函数与 API 映射
$$
J = \sum_{i=1}^{N_p} (y_{k+i|k}-r_{k+i})^\top Q (y_{k+i|k}-r_{k+i})
 + \sum_{i=0}^{N_c-1} \Delta u_{k+i|k}^\top R_\Delta \Delta u_{k+i|k}
 + \sum_{i=0}^{N_c-1} u_{k+i|k}^\top R u_{k+i|k}
 + \lambda_s \sum_{i=1}^{N_p} \|\epsilon_{k+i}\|_1
 + (y_{k+N_p|k})^\top P y_{k+N_p|k}
$$
```matlab
mpcobj.Weights.OutputVariables = [q_y, q_psi, q_v, q_omega];
mpcobj.Weights.ManipulatedVariables = [r_F, r_omega];
mpcobj.Weights.ManipulatedVariablesRate = [r_dF, r_domega];
% MV/OV 上下界与软约束（示例，按项目现值替换）
```

### 4.7 三线性插值权重
归一化坐标 `(ξ,η,ζ)∈[0,1]^3` 八角点：
```
w000=(1-ξ)*(1-η)*(1-ζ)
w100=ξ*(1-η)*(1-ζ)
w010=(1-ξ)*η*(1-ζ)
w110=ξ*η*(1-ζ)
w001=(1-ξ)*(1-η)*ζ
w101=ξ*(1-η)*ζ
w011=(1-ξ)*η*ζ
w111=ξ*η*ζ
```
插值：`A = Σ w_ijk*A_ijk`（B,C,D,E 同理）。权重做：`w=abs(w); w=w/sum(w)` 防微负漂移。

### 4.8 RhoFilter 与驻留
滤波：`alpha=Ts/(tau+Ts)`；驻留判定：若 `|rho_raw-rho_f|/max(|rho_raw|,1e-6)<1e-3` 连续 ≥5 步 → 可降低更新频率。
最小驻留时间 `T_stay≈0.2–0.3 s` 避免曲率快速闪动。

---

## 6. 在线控制与仿真（LPVMPC_AGV_simulink.slx）
- 参考信号：`ref=[X Y psi v omega]`（或误差参考，依模型配置）；
- 扰动：`md=theta_ground`（坡度）；
- 日志：每步记录 `rho, slack, solve_time, status`；
- 自检脚本：`test_lpvmpc_workflow.m`。
### 6.1 安全模式
- MPC 求解失败或 `solve_time_ms>10` → 使用 `u_prev` 并标记 `status='fallback'`；连续失败 ≥3 次 → 进入降级：`u=[0;0]`。
### 6.2 日志字段建议
`t, rho_f, u_cmd, u_prev, solve_time_ms, status, slack, e_y, e_psi, e_v, e_omega`。

---

## 7. 贝叶斯优化（Bayesian_Optimization.m / Cost_Function.m）

### 7.1 评估函数细化
- 输入：`params`（`parameters()` 结果）、`db`（可为空则内部构建 3×3×3 默认网格）、`cfg`（权重/范围/滤波/罚值/ctrl/maps）、`scenes`（默认权重：turn 0.35, slope 0.30, straight_turn 0.20, bumpy 0.10, straight 0.05）。
- 流程：每 `Ts` 计算误差 → 构造并滤波 `rho`（τ=0.4）→ `mpc_update_from_rho` → 更新 `MPCobj` → `mpcmoveAdaptive` → `state_eq_ref` 推进 → 记录指标；
- 失败即返回 `1e6`；屏蔽控制台输出（`evalc`）。

### 7.2 优化脚本细化
- 变量范围与形参映射按现有实现（见仓库脚本）；
- 评估 ≥ 60 次建议；单线程；
- 产物：根目录 `maps_best.mat`（含范围/形参、rho_min/max、timestamp、version），可选 `bo_report_*.mat`, `bo_history_*.mat`。
#### 7.2.1 失败处理
- 单场景失败（NaN/Inf / mpc 失败）→ 该场景代价设高罚（如 2e6）；若 ≥50% 场景失败 → 提前终止评估返回 1e6。
- 控制器构建异常：直接返回 5e6 并记录 `report.fail_reason`。
#### 7.2.2 报告字段建议
`report.scenes(s).RMSE, RMS_du, violations, solve_time_mean, solve_time_max, status_flags`；汇总：`report.J_total, J_components, failure_count`。

### 7.3 运行命令（Windows）
```cmd
matlab -batch "run('start_bayesian.m')"
```
### 7.4 版本化
- 保存旧版本：`maps_best_<timestamp>.mat`；
- 记录 `meta.seed, meta.max_evals, meta.selection`；
- 若 `J` 改善 <2% 可选择不覆盖主文件减少 churn。

---

## 8. AI 工况识别（GRU_* 系列）

### 8.1 数据生成与预处理
- 生成：`GRU_gen_train_data.m`（可调用 `GRU_DataGen.slx`），场景使用 `gen_agv_ref_path`；
- 预处理：`GRU_prepare_dataset.m` 输出 `GRU_dataset_processed.mat`（含 `X, y_main, y_turn, y_theta, mask_theta, scaler, feat_names`）。
#### 8.1.1 数据质量
- NaN 比例 >1%：序列剔除或插值；极端值 |z|>6 裁剪到 ±6；
- 类不平衡：采用类权重或过采样少数类（stall/slip）。

### 8.2 训练与推理
- 训练：`GRU_train.m` → 产物 `GRU_model.mat`, `GRU_scaler.mat`, `GRU_meta.mat`；
- 推理：`GRU_infer.m`（序列输入→三头输出）；在线封装：`GRU_state_classifier.m`（驻留/低通/稳健）。
#### 8.2.1 训练循环示例
```matlab
for epoch = 1:opts.epochs
	[loss_main, loss_turn, loss_theta] = forward_pass(batch,...);
	loss = loss_main + opts.lambda_turn*loss_turn + opts.lambda_theta*loss_theta;
	backprop(loss);
	if mod(epoch,5)==0, evaluate_val(); end
	if early_stop_trigger, break; end
end
```
#### 8.2.2 产物保存
- `GRU_model.mat`: `net`, 最优 epoch, 指标摘要；
- `GRU_meta.mat`: `feat_names, class_weights, seq_len, stride, Ts, commit_SHA`（可选）；
- `GRU_scaler.mat`: `mean, std`。

### 8.3 评估与目标
- 指标：主分类 Acc/macro-F1，转弯 Acc，坡度 MAE/RMSE（deg）；
- 时延：MATLAB 推理均值/P95 < 1 ms/步；
- 压测：低 μ、强噪声、长坡、急转+颠簸、连续打滑；
- 自检：`test_GRU_workflow.m`；日志输出至 `GRU_logs/`。
#### 8.3.1 指标阈值建议
- `macro_F1_main >= 0.85`；`Acc_turn >= 0.85`；`MAE_theta_deg <= 1.5`；
- 推理时延：mean <0.6 ms, P95 <1.0 ms；
- 低于阈值需在 `change.md` 说明原因与改进计划。

---

## 9. 变更同步与文档
- 修改/新增上述任一脚本或接口，须同步更新根目录 `func.md`（条目含：路径/职责/签名/输入输出/单位/备注）；
- 在 `change.md` 留痕（Context/Changes/Impact/Verification/Artifacts/Migration/Refs）。
### 9.1 func.md 条目建议字段
- `deps`（依赖脚本或 .mat）、`interfaces`（函数签名）、`units`（关键单位）、`updated_at`、`status`(`stable|experimental|deprecated`)。
### 9.2 CI 检查要点
- 新增 `.m` 未更新 `func.md` → 阻断；
- 接口/维度变化无 `BREAKING CHANGE` 声明 → 阻断；
- GRU 或 MPC 关键指标低于阈值且无解释 → 阻断；
- 提交正文缺少 `Context` 或 `Changes` 段 → 警告或阻断（按策略）。
