# 功能/类/脚本导航（func.md）
> 生成/修改任何业务代码前，**必须先阅读并检索本文件**，确认是否已有实现可复用。

## 约定
- 统一单位：m, m/s, rad；Ts 见 parameters.m
- 关键信号：ref=[X Y ψ v ω]，md=θ（theta_ground）
- ρ（调度变量）统一为有符号：ρ=[v, ω, θ]
- 颠簸默认幅值：0.2 rad

---

## 核心模块

### core/models - AGV动力学S-Function模型

#### 1. **agv_model_sfunc.m** - Simulink Level-2 S-Function包装器
- **路径**：agv_model_sfunc.m
- **职责**：Simulink Level-2 S-Function外壳，封装AGV离散植物模型
- **接口**：
  - **参数**：`p = parameters()` 结构体（必须包含Ts；可选nx、x0）
  - **输入端口(1)**：`u_all = [F_cmd; omega_cmd; theta_ground]` (3×1)
    - `F_cmd`：驱动力指令 [N]
    - `omega_cmd`：角速度指令 [rad/s]
    - `theta_ground`：地面坡度角 [rad]
  - **输出端口(1)**：`y` (31×1) - 详见output_eq.m
  - **离散状态**：`x` (8×1)，通过DWork管理
- **调用关系**：
  - `DoOutputs` → `output_eq(x, u, theta_ground, params)`
  - `DoUpdate` → `state_eq(x, u, theta_ground, params)`
- **关键方法**：
  - `DoPostPropSetup`：设置DWork数量和属性
  - `DoInitialize`：初始化离散状态（从params.x0或默认零向量）
  - `DoOutputs`：调用output_eq计算输出
  - `DoUpdate`：调用state_eq更新状态
- **采样时间**：params.Ts（默认0.05s）

---

#### 2. **state_eq.m** - AGV状态转移方程
- **路径**：state_eq.m
- **职责**：对角式双舵轮AGV状态转移方程（RK4数值积分）
- **接口**：`x_next = state_eq(x, u, theta_ground, params)`
- **状态向量** `x` (8×1)：
  1. `X` - 全局X坐标 [m]
  2. `Y` - 全局Y坐标 [m]
  3. `psi` - 航向角 [rad]
  4. `v` - 纵向速度 [m/s]
  5. `omega` - 偏航角速度 [rad/s]
  6. `delta_lf` - 左前轮转向角 [rad]
  7. `delta_rr` - 右后轮转向角 [rad]
  8. `beta` - 质心侧滑角 [rad]
- **输入向量** `u` (2×1)：
  1. `F_cmd` - 驱动力指令 [N]
  2. `omega_cmd` - 角速度指令 [rad/s]
- **关键功能模块**：
  1. **自动转向角计算**（基于omega_cmd反馈调整）
     - 几何公式：`delta = atan2(L, R_cmd) * sign(omega_cmd)`
     - 反馈缩放：防止omega超调
     - 执行器动力学：一阶滤波 + 速率限幅 + 角度限幅
  2. **载荷转移计算**
     - 纵向载荷转移：基于净驱动力估算加速度
     - 横向载荷转移：基于转弯半径估算横向加速度
     - 四轮法向载荷：N_lf, N_rf, N_lr, N_rr
  3. **轮胎侧向力**
     - 侧偏角：`alpha_f = delta_lf - (beta + Lf*omega/v)`
     - 侧偏角：`alpha_r = delta_rr - (beta - Lr*omega/v)` （对角式双舵轮）
     - 侧向力：`Fy = -C_a * alpha`，限幅到 `μ*N`
  4. **驱动力分配**（关键修复）
     - 载荷比例分配：`w_lf = N_lf/(N_lf+N_rr)`，`w_rr = N_rr/(N_lf+N_rr)`
     - 偏航控制：`Delta_Fx` 基于omega误差（P控制）
     - 摩擦椭圆限幅：`sqrt((Fx/μN)^2 + (Fy/μN)^2) ≤ 1`
  5. **RK4数值积分**（高精度）
     - 调用：`continuous_dynamics_core_v2`
     - 转向角插值：(k, mid, mid, k+1)
     - 动态F_drag：每个RK4子步重新计算空气阻力
  6. **稳定性保护**
     - 强横摆阻尼：`Mz_damping = -1000*omega`
     - 强侧滑阻尼：`beta_dot` 含 `-5.0*beta` 项
     - 角加速度限幅：`omega_dot_limit = 5.0 rad/s²`
     - 侧滑角变化率限幅：`beta_dot_limit = 10°/s`
- **子函数**：
  - `continuous_dynamics_core_v2`：连续动力学核心（V2，动态F_drag）
  - `continuous_dynamics_core`：原版（保留兼容性）
  - `compute_load_transfer`：载荷转移与滚阻计算
  - 工具函数：`sat`, `sat_sym`, `sat_smooth`, `softplus`, `normalizeAngle`

#### 2.1 **state_eq_ref.m** - 参考几何版本的状态转移
- **路径**：state_eq_ref.m
- **职责**：同 `state_eq.m`，但舵角目标由参考几何 ICR 生成；当 |ω_ref|<阈值时回退到测量几何
- **接口**：`x_next = state_eq_ref(x, u, theta_ground, params)`（ref 从基础工作区读取）
- **备注**：动力学、执行器一阶与限幅、载荷/胎力/分配、阻尼与积分器均与原版一致

---

#### 3. **output_eq.m** - AGV输出方程
- **路径**：output_eq.m
- **职责**：对角式双舵轮AGV输出方程（测量/观测/诊断）
- **接口**：`y = output_eq(x, u, theta_ground, params)`
- **输出向量** `y` (31×1)：
  - **[1-8] 基本状态变量**：X, Y, psi, v, omega, delta_lf, delta_rr, beta
  - **[9-11] IMU测量**：
    - `accel_x_meas` - 纵向加速度 [m/s²]
    - `gyro_y_meas` - 俯仰角速度 [rad/s]（含噪声）
    - `gyro_z_meas` - 偏航角速度 [rad/s]（含噪声）
  - **[12-13] 电流估计**：
    - `I_meas_lf` - 左前轮电机电流 [A]
    - `I_meas_rr` - 右后轮电机电流 [A]
  - **[14-15] 扰动力估计**：
    - `F_dist_calc_lf` - 左前轮扰动力 [N]
    - `F_dist_calc_rr` - 右后轮扰动力 [N]
  - **[16] 地面角度**：`theta_ground` [rad]
  - **[17-18] 轮速**：
    - `omega_wheel_lf` - 左前轮角速度 [rad/s]
    - `omega_wheel_rr` - 右后轮角速度 [rad/s]
  - **[19-27] AI算法专用输出**：
    - 载荷信息：`load_ratio_front`, `load_ratio_rear`, `load_transfer_lateral`
    - 轮胎利用率：`tire_utilization_lf`, `tire_utilization_rr`
    - 运动状态：`lateral_accel`, `slip_angle_front`, `slip_angle_rear`, `drive_force_asymmetry`
  - **[28-31] 扩展诊断信息**：
    - `slip_flag` - 打滑标志（0/1）
    - `stall_flag` - 堵转标志（0/1）
    - `N_lf` - 左前轮法向载荷 [N]
    - `N_rr` - 右后轮法向载荷 [N]
- **关键功能**：
  1. 与state_eq同步的力计算（转向、载荷、轮胎力、驱动力分配）
  2. 噪声注入（可通过params.enable_noise开关）
  3. 扰动观测（基于力平衡残差）
  4. AI特征工程输出（载荷/利用率/滑移状态）
- **子函数**：
  - `compute_load_transfer`：与state_eq共享
  - 工具函数：`sat`, `sat_sym`, `sat_smooth`

#### 3.1 **output_eq_ref.m** - 参考几何版本的输出方程
- **路径**：output_eq_ref.m
- **职责**：基于参考几何 ICR（x_c=0）计算目标舵角；当 |ω_ref|<阈值时回退到测量几何；观测/诊断逻辑与 `output_eq.m` 一致
- **接口**：`y = output_eq_ref(x, u, theta_ground, params)`（ref 从基础工作区读取）
- **备注**：按仿真时间对齐 `ref.t` 索引，优先 `R_ref=v_ref/ω_ref`，回退 `R_meas=v/ω`

---

### core/env - 工程环境与路径管理

#### 1. **project_root.m** - 项目根目录解析
- **路径**：project_root.m（仓库根目录）
- **职责**：返回当前 LPV-MPC 工程的根目录绝对路径，并在进程内做缓存；供脚本、Simulink 回调统一构造相对路径（如 `data/`、`results/`、`simulink/`）。
- **接口**：`root = project_root()`
- **特性**：
  - 自动根据 `mfilename('fullpath')` 解析所在目录；
  - 首次调用后在 persistent 变量中缓存，避免重复解析；
  - 要求文件固定放在仓库根目录（不要随脚本一起移动）。

#### 2. **init_project.m** - 工程环境初始化
- **路径**：init_project.m（仓库根目录）
- **职责**：初始化 LPV-MPC 工程运行环境，将 `src/` 及其子目录、`simulink/` 目录加入 MATLAB 路径，并打印当前工程根目录；通常在脚本或 Simulink PreLoadFcn 中首先调用。
- **接口**：`init_project()`（无输入输出）
- **特性**：
  - 依赖 `project_root()` 获取根目录；
  - 使用 `addpath(genpath(...))` 递归加入 `src/` 下所有模块；
  - 单次调用即可满足大部分脚本/模型的路径需求。

#### 3. **results_dir.m** - 统一结果输出目录
- **路径**：results_dir.m（仓库根目录）
- **职责**：构造并创建 `results/<subdir>` 结果输出目录，供脚本与 Simulink 统一落盘路径（如 `results/closed_loop`、`results/bo/history` 等）。
- **接口**：`out_dir = results_dir(subdir)`
  - `subdir`：字符串（可为空），例如 `'closed_loop'`、`'gru/train_logs'`。
- **特性**：
  - 内部调用 `project_root()` + `fullfile(root,'results',subdir)`；
  - 若目录不存在则自动 `mkdir` 创建；
  - 返回绝对路径，可直接用于 `save`/`writematrix` 等。

---

#### 4. **parameters.m** - 集中参数定义
- **路径**：parameters.m
- **职责**：集中维护模型与控制参数
- **接口**：`params = parameters()`
- **关键参数分类**：
  - 时基：`Ts = 0.01s`
  - 车辆几何：`mass=100kg`, `L=2m`, `W=0.8m`, `h_cg=0.5m`, `Iz=16.67 kg·m²`
  - 车轮：`wheel_radius=0.15m`, `wheel_inertia=0.0135 kg·m²`
  - 电机传动：`motor_torque_constant=1.21 Nm/A`, `gear_ratio=10`, `current_limit=9A`
  - 执行器：`max_steering_angle=90°`, `max_steering_rate=300°/s`, `steering_time_constant=0.08s`
  - 环境阻力：`rolling_resistance=0.015`, `friction_coefficient=0.8`, `drag_coefficient_area=0.5m²`
  - **轮胎侧偏**：`front_cornering_stiffness=300 N/rad`, `rear_cornering_stiffness=300 N/rad`
  - 噪声：`enable_noise=false`, 噪声标准差（电流/轮速/扰动）
  - 线性化友好性：`use_smooth_saturation=false`, `smooth_gain=30`
- **版本**：V4.0

---

## 模块：paths - 参考轨迹生成

### 1. **gen_agv_ref_path.m** - 统一路径生成接口
- **路径**：gen_agv_ref_path.m
- **职责**：为5种工况生成参考轨迹数据（直行、转弯、直+弯、坡度直行、颠簸直行）
- **关键接口**：`ref = gen_agv_ref_path(path_type, params, opts)`
  - **输入**：
    - `path_type`：字符串 ∈ {'straight', 'turn', 'straight_turn', 'slope', 'bumpy'}
    - `params`：参数结构体（来自 parameters.m）
    - `opts`：可选参数（T_end, R, v0, theta_slope, bumpy_amp, rho_filter_tau）
  - **输出**：结构体 `ref`，包含
    - `t, X_ref, Y_ref, psi_ref, v_ref, omega_ref, theta_ref`：参考轨迹
    - `e_y_ref, e_psi_ref, e_v_ref`：误差参考（=0，便于MPC）
    - `rho`：调度变量 [v, omega, theta]（已滤波，有符号）
    - `time, signals`：From Workspace 兼容格式
    - `meta`：元数据（生成时间、参数、版本）
- **特性**：
  - 持续 20s（可配置）；初速度 1 m/s；转弯半径 10 m
  - 颠簸：地面坡度扰动 0.2 rad·sin(t)（保持几何路径为直线）
  - 坡度默认 5°
  - 直线→转弯：S曲线平滑过渡（2.0s），避免曲率阶跃
  - rho 调度变量经一阶滤波（τ=0.4s），避免快速跳变
  - 输出格式兼容 Simulink From Workspace 模块
- **产物**：可保存为 `path_<type>.mat`（包含 ref 及 meta 信息）
- **版本**：V1.1

### 2. **test_gen_paths.m** - 路径生成测试脚本
- **路径**：test_gen_paths.m
- **职责**：批量生成所有5种路径并可视化
- **关键接口**：运行脚本（无参数）
- **产物**：
  - `path_straight.mat`
  - `path_turn.mat`
  - `path_straight_turn.mat`
  - `path_slope.mat`
  - `path_bumpy.mat`
  - 可视化图像：`path_<type>_preview.png`
- **版本**：V1.0

## 模块：bo - 贝叶斯优化

### 1. **Cost_Function.m** - 多工况评估函数（根目录）
- **路径**：`Cost_Function.m`
- **职责**：复现 Adaptive MPC 闭环，结合 turn / straight_turn / slope / straight / bumpy 场景计算加权代价；支持从 `cfg.ctrl` 传入已创建控制器，避免重复创建；内部使用 `evalc` 静默调用 `mpcmoveAdaptive` 抑制控制台输出。
- **接口**：`[J, report] = Cost_Function(params, db, cfg, scenes)`（支持默认参数、内部生成 LPV 数据库、配置权重/罚值/滤波/ctrl/maps）。
- **输出**：`J`（失败或异常返回 1e6）、`report`（含场景 RMSE、Δu、约束违反、平均/最大求解时间、失败次数；可选保存到根目录）。

### 2. **Bayesian_Optimization.m** - 贝叶斯优化驱动（根目录）
- **路径**：`Bayesian_Optimization.m`
- **职责**：调度 `bayesopt` 优化 Q/R/dR、alpha/beta 形状、约束缩放、tau；每次评估仅创建一次控制器并通过 `cfg.ctrl` 传入 `Cost_Function`；生成 `maps_best.mat`（根目录）。
- **接口**：`[best, boResults] = Bayesian_Optimization(params, db, options)`（默认场景权重 {turn:0.35, slope:0.30, straight_turn:0.20, bumpy:0.10, straight:0.05}；评估次数可通过 `options.MaxObjectiveEvaluations` 指定）。
- **变量范围（当前实现）**：
  - Q：`q_y∈[10,25], q_psi∈[12,30], q_v∈[2.0,6], q_omega∈[0.5,3]`
  - R：`log10(r_F)∈[-3.5,-2], log10(r_omega)∈[-3.8,-2.2]`
  - dR：`log10(rdF)∈[-2.2,-1], log10(rdw)∈[-2.5,-1]`
  - 形状参数：`alpha/beta ∈ [0,1]`（内部强制 `alpha≤beta`）
  - 约束缩放：`scale_umin/umax_lo/hi ∈ [0.9,1.1]`
  - ρ滤波：`tau∈[0.2,0.6]`
- **结果输出**：
  - `maps_best.mat`（根目录）：保存 Q/R/dR 基准与范围、alpha/beta、scale_*、rho_min/max、timestamp、version。
  - 可选 `bo_history_<timestamp>.mat`（根目录），由 `options.save_history=true` 触发。

### 3. **start_bayesian.m** - 启动与汇报脚本（根目录）
- **路径**：`start_bayesian.m`
- **职责**：装载 `params` 与 `lin_agv_db.mat`、配置评估次数与是否保存历史、调用 `Bayesian_Optimization` 并打印总耗时/最优点/各场景性能与历史统计。
- **要点**：总耗时采用 `tic/toc` 实测；控制台仅显示一次权重设置（避免重复创建控制器）。

### 4. **maps_best.mat** - 优化结果映射
- **路径**：`maps_best.mat`（根目录）
- **职责**：保存 `maps_best`（Q0/R0/dR0、范围缩放、约束缩放、tau、rho_min/max），供脚本或 Simulink 的自定义更新函数加载。

---
## 关键修复记录（2025-10-02）

### 已修复的9个关键问题

#### 1. 驱动力分配错误（50%驱动力损失）
- **问题**：`W_total = m*g*cos(theta); w_lf = N_lf/W_total`（用单轮载荷除以全车重量）
- **修复**：`W_drive = N_lf + N_rr; w_lf = N_lf/W_drive`（在驱动轮之间分配）
- **影响**：修复前驱动力只有50%，修复后恢复100%

#### 2. RK4积分精度问题
- **问题**：`F_drag`在RK4子步中固定，但`F_aero`依赖于变化的`v`
- **修复**：创建`continuous_dynamics_core_v2`，在每个RK4子步动态计算`F_aero`
- **影响**：直线速度跟踪从衰减改善到完美跟踪

#### 3. 侧偏刚度过大（40倍 → 10倍 → 最终调整）
- **问题1**：`C_af = 12000 N/rad`导致转弯时侧向力饱和，摩擦圈无纵向余量
- **修复1**：降低到`C_af = 800 N/rad`
- **问题2**：直线行驶时仍产生过大轮胎力矩
- **修复2**：进一步降低到`C_af = 300 N/rad`
- **影响**：侧向力从100%饱和降低到合理范围，直线稳定性大幅改善

#### 4. 后轮侧偏角公式错误（对角式双舵轮）
- **问题**：`alpha_r = -delta_rr - (beta - Lr*omega/v)`（自行车模型）
- **修复**：`alpha_r = delta_rr - (beta - Lr*omega/v)`（对角式双舵轮）
- **影响**：修正了后轮侧向力符号

#### 5. 偏航控制缺失
- **问题**：对角式双舵轮主要靠驱动力差产生偏航力矩，而不是转向角差
- **修复**：增加偏航控制：`Delta_Fx = 2*Mz_needed/W`，基于omega误差
- **影响**：omega能够响应omega_cmd

#### 6. 载荷转移加速度估计
- **问题**：`a_long = F_cmd/m`（未考虑阻力）
- **修复**：`F_net_est = F_cmd - F_rolling - F_aero - F_slope; a_long = F_net_est/m`
- **影响**：载荷转移计算更准确

#### 7. 横摆阻尼不足（关键修复）⭐
- **问题**：缺少横摆阻尼，omega在数值误差下发散
- **修复**：添加强阻尼`Mz_damping = -1000*omega`
- **影响**：omega从失控（285 rad/s）降低到完美收敛（0.000 rad/s）

#### 8. 侧滑角阻尼不足（关键修复）⭐
- **问题**：beta阻尼系数0.8太小，导致beta发散到±15°极限
- **修复**：增大阻尼到5.0，并限制beta_dot
- **影响**：Y方向漂移从4.26m降低到0.000m

#### 9. 数值稳定性保护
- **修复**：增加omega_dot和beta_dot的限幅保护
- **影响**：防止数值爆炸

---

## 当前状态总结（2025-10-02 最终更新）

### ✅ **AGV动力学模型已完成** 🎯

**关键参数设置**：
- 横摆阻尼：C_damping = 1000 Nm/(rad/s)
- 侧滑角阻尼：5.0
- 侧偏刚度：C_af = C_ar = 300 N/rad
- 摩擦系数：μ = 0.8

**模型特点**：
- ✅ 对角式双舵轮AGV动力学模型
- ✅ 完整的轮胎力建模（侧偏刚度+摩擦椭圆）
- ✅ 载荷转移、滚阻、坡度、空气阻力
- ✅ RK4高精度数值积分
- ✅ 内置稳定性保护（横摆阻尼、侧滑阻尼）
- 🎯 准备就绪：可用于MPC控制器设计

**重要说明**：
- 当前模型内置了控制/阻尼机制（自动转向、偏航控制、横摆阻尼等）
- 这些机制用于稳定性保护和基础控制
- 转弯等复杂工况需要LPV-MPC控制器（项目核心目标）

---

## 模块：线性化（已实现）

### 1. **lin_agv_at_point.m** - 单点线性化内核
- **路径**：lin_agv_at_point.m
- **职责**：在指定工作点对AGV路径坐标系误差动力学进行线性化
- **关键接口**：`sys = lin_agv_at_point(x0, u0, theta0, params)`
  - **输入**：
    - `x0`：工作点状态向量 [X Y psi v omega delta_lf delta_rr beta] (8×1)
    - `u0`：工作点输入向量 [F_cmd omega_cmd] (2×1)
    - `theta0`：工作点坡度角 (标量)
    - `params`：参数结构体
  - **输出**：
    - `sys`：结构体，包含 A_d(4×4), B_d(4×2), C(4×4), D(4×2), E_d(4×1)（离散）
    - 状态：[e_y, e_psi, e_v, e_omega]（路径坐标系误差）
    - 输入：[F_cmd, omega_cmd]
    - 扰动：[theta]
- **方法**：数值有限差分（一步差分，离散模型）
- **特性**：
  - 几何投影：e_y反映射考虑psi_ref
  - 曲率耦合：可选开关（默认关闭）
  - 元数据：含离散化说明、几何投影信息
- **产物**：sys 结构体（含元数据和有效范围）
- **版本**：V1.2

### 2. **lin_agv_grid.m** - 网格线性化主流程
- **路径**：lin_agv_grid.m
- **职责**：在调度变量网格 ρ=[v, ω, θ] 上批量线性化，生成LPV模型表
- **关键接口**：`db = lin_agv_grid(params, grid, opts)`
  - **输入**：
    - `params`：参数结构体（来自 parameters.m）
    - `grid`：网格定义 {V_grid（速度）, W_grid（角速度，有符号）, T_grid（坡度）}
    - `opts`：选项（coord, disc, keep_E, export_mat）
  - **输出**：
    - `db`：数据库结构体，包含
      - A, B, C, D, E：矩阵数组 (Nv×Nw×Nt×...)（离散时间模型）
      - grid：网格定义
      - Ts, nx, nu, ny, nd：维度信息
      - meta：元数据（耗时、不稳定点数、离散化说明等）
- **产物**：`plant_grid.mat`（默认）
- **特性**：
  - 进度显示与ETA估算
  - 稳定性校验（极点检查）
  - 自动创建目录
  - **重要**：表内矩阵为离散模型，无需c2d转换
  - 转向假设：双舵轮等角（single-track-equivalent）
- **版本**：V1.2

---

## 模块：MPC控制器设计（已实现）

### 1. **mpc_setup_single_interp.m** - 单一自适应MPC创建
- **路径**：mpc_setup_single_interp.m
- **职责**：创建单一MPC控制器对象，支持在线模型和权重插值
- **关键接口**：`ctrl = mpc_setup_single_interp(db, opts)`
  - **输入**：
    - `db`：LPV模型数据库（来自 lin_agv_grid.m）
    - `opts`：设计选项，包含
      - Np, Nc：预测/控制时域（步数）
      - Q, R, dR：权重向量
      - umin, umax：输入约束
      - dumin, dumax：输入速率约束
      - ymin, ymax：输出约束（软约束）
      - soft_weight_pos, soft_weight_yaw：软约束惩罚系数（分离设置）
  - **输出**：
    - `ctrl`：控制器结构体，包含
      - mpcobj：MATLAB MPC对象（2个MV + 1个MD）
      - db：数据库引用
      - opts：设计选项
      - maps：权重/约束映射表（含ey_max, epsi_max, normalize_fn）
      - meta：元数据（含has_md标志）
- **默认参数**：
  - Np ≈ 2.5s, Nc ≈ 0.6s（根据Ts自适应）
  - Q = [3, 8, 1, 1]（[e_y, e_psi, e_v, e_omega]）
  - R = [1e-3, 1e-3], dR = [1e-2, 1e-2]
  - 软约束权重：pos=1e4, yaw=1e4
- **特性**：
  - 基于网格中心点作为基准模型
  - 支持 Adaptive MPC 在线更新
  - 误差参考：[0; 0; 0; 0]（趋零控制）
  - **MD通道**：theta（坡度角前馈补偿）
  - 输入分组：MV=[F_cmd, omega_cmd], MD=[theta]
  - 自动设置信号名称
- **版本**：V1.2

### 2. **mpc_update_from_rho.m** - 在线模型更新
- **路径**：mpc_update_from_rho.m
- **职责**：根据当前调度变量 ρ 进行三线性插值，输出更新的模型和权重
- **关键接口**：`upd = mpc_update_from_rho(rho, db, maps)`
  - **输入**：
    - `rho`：当前调度变量 [v; omega; theta] (3×1)（omega有符号）
    - `db`：LPV模型数据库
    - `maps`：权重/约束映射表
  - **输出**：
    - `upd`：更新结构体，包含
      - A (4×4), B (4×2), C (4×4), D (4×2)：插值后的模型矩阵
      - E (4×1), Bv (4×1), Dv (4×1)：MD通道矩阵（Bv=E，Dv=0）
      - Q, R, dR：插值后的权重（按维度映射）
      - umin, umax：插值后的约束（可选）
      - rho_n：归一化调度变量 [0,1]^3
      - indices：插值顶点索引 (8×3)
      - weights：插值权重 (8×1)
- **方法**：三线性插值（8个顶点）
- **特性**：
  - 边界饱和处理
  - 权重归一化（数值稳定）
  - **支持非均匀网格**（二分查找定位）
  - **统一normalize_fn接口**
  - **权重按维度映射**（Q/R/dR各分量智能调整）
  - **MD通道支持**：Bv=E(ρ)，用于坡度角前馈
  - 调试信息输出
- **版本**：V1.2

---

## 模块：贝叶斯优化（根目录）

### 1. **Cost_Function.m** - MPC闭环评估函数
- **路径**：Cost_Function.m（根目录）
- **职责**：在MATLAB环境中复现Adaptive MPC闭环，输出加权代价J和详细报告
- **关键接口**：`[J, report] = Cost_Function(params, db, cfg, scenes)`
  - **输入**：
    - `params`：parameters() 结果
    - `db`：LPV数据库（允许为空，内部生成3×3×3默认网格）
    - `cfg`：配置结构体，含 tau, ey_max, epsi_max, ev_max, eomega_max, dF_max, dw_max, ctrl_maps, debug
    - `scenes`：场景权重结构体（turn, slope, straight_turn, bumpy, straight）
  - **输出**：
    - `J`：总加权代价（失败/异常返回1e6）
    - `report`：详细报告（各场景RMSE、Δu、约束违反、求解时间、失败标记）
- **仿真流程**：
  1. 调用 mpc_setup_single_interp 构建控制器，使用 mpcstate 初始化
  2. 对每个场景调用 gen_agv_ref_path (T_end=20, bumpy_amp=0.2)
  3. 每个采样周期：计算路径坐标系误差、rho滤波、mpc_update_from_rho、构造plant_model+Nominal、mpcmoveAdaptive求解、state_eq_ref推进
  4. 失败立即终止（NaN/Inf或Info.QPCode非'feasible'/'optimal'）
- **API实现**（关键）：
  - 调用方式：`[u_mpc, Info] = mpcmoveAdaptive(mpcobj, xmpc, plant_model, Nominal, y_meas, r_ref, md)`
  - `plant_model`：每步更新的离散状态空间模型，`B=[upd.B, upd.E]`（4×3），`D=[upd.D, zeros(4,1)]`（4×3）
  - `Nominal.U`：3×1（2个MV + 1个MD），其他字段均为零向量
  - 成功判定：`Info.QPCode == 'feasible'` 或 `'optimal'`
- **代价计算**：
  - `J_trk = 1.1*RMSE(e_y)/ey_max + 1.0*RMSE(e_psi)/epsi_max + 0.2*RMSE(e_omega)/eomega_max + 0.1*RMSE(e_v)/ev_max`
  - `J_smooth = 0.08*RMS(ΔF)/dF_max + 0.07*RMS(Δω)/dw_max`
  - `J_cons = 10*L1 + 50*Linf`（约束越界惩罚）
  - `J_rt = max(0,(avg_ms-5)/5) + (max_ms>10)*0.5`（实时性惩罚）
  - `J_scene = J_trk + J_smooth + J_cons + J_rt`
- **API落地**：每步构造plant_model和Nominal结构体，调用 mpcmoveAdaptive(mpcobj, xmpc, plant_model, Nominal, ...)
- **前馈力**：`F_eq = c_r*m*g*cos(θ) + 0.5*ρ*CdA*v^2`（不含m·g·sinθ，避免与MD通道重复）
- **版本**：V2.1（修复 mpcmoveAdaptive 调用方式与成功判定 Info.QPCode）

### 2. **Bayesian_Optimization.m** - 贝叶斯优化驱动
- **路径**：Bayesian_Optimization.m（根目录）
- **职责**：使用bayesopt调度Cost_Function，获得最优参数并生成maps_best.mat
- **关键接口**：`[best, boResults] = Bayesian_Optimization(params, db, options)`
  - **输入**：
    - `params`：parameters() 结果
    - `db`：LPV库（可为空，自动生成3×3×3默认网格）
    - `options`：可选结构体（scenes, MaxObjectiveEvaluations, save_history）
  - **输出**：
    - `best`：最优设计（变量、代价J、report、ctrl_maps）
    - `boResults`：bayesopt原始结果
- **变量集**（第一阶段）：
  - Q权重：`q_y∈[1,10], q_psi∈[5,20], q_v∈[0.1,3], q_omega∈[0.1,3]`
  - R权重：`log10(r_F)∈[-4,-2], log10(r_omega)∈[-4,-2]`
  - dR权重：`log10(rdF)∈[-3,-1], log10(rdw)∈[-3,-1]`
  - 形状参数：`alpha_Q/R/dR∈[0.3,2.0], beta_Q/R/dR∈[0.6,3.0]`（约束α≤β）
  - 约束缩放：`scale_umin/umax_lo/hi∈[0.8,1.5]`
  - 滤波时间常数：`tau∈[0.2,0.6]`
- **算法配置**：
  - 采集函数：expected-improvement-plus
  - 总评估：100次（可通过options.MaxObjectiveEvaluations调整）
  - 单线程执行
  - 失败/不可行代价：1e6
- **结果输出**：
  - `maps_best.mat`（根目录）：含 Q_range, R_range, dR_range, alpha/beta, scale_*, rho_min/max, timestamp, version
  - 可选：`bo_history_<timestamp>.mat`（通过options.save_history=true启用）
- **db为空处理**：自动生成默认网格（V=[0.8,1.0,1.2], W=[-0.2,0,0.2], T=[-0.2,0,0.2]）
- **特性**：
  - enable_factor在Simulink代码生成路径不生效（仅MATLAB仿真路径有效）
  - 自动传递rho_min/rho_max到ctrl.maps
  - 打印最优代价、失败次数
- **版本**：V2.0

---

## 模块：AI工况识别（根目录，GRU）

### 1. **GRU_gen_train_data.m** - 训练数据生成（脚本版 + Simulink集成 + 物理一致启发式）
- **路径**：GRU_gen_train_data.m（根目录）
- **职责**：通过Simulink模型 GRU_DataGen.slx 生成GRU训练数据，最大化还原仿真环境
- **使用方式**：**直接运行脚本**
  - 命令行：`run('GRU_gen_train_data.m')` 或 `GRU_gen_train_data`
  - 修改脚本开头的"配置区域"来调整参数（场景、回合数、注入概率等）
- **配置参数**（脚本顶部 `cfg` 结构体）：
  - `cfg.scenes`：场景列表 {'straight','turn_left','turn_right','straight_turn','slope','bumpy'} (V4.1新增左右转)
  - `cfg.num_runs`：每场景生成回合数（默认100，可改为10快速测试）
  - `cfg.T_end`：仿真时长 [s]（默认20）
  - `cfg.noise_on`：是否开启传感器噪声（默认true）
  - `cfg.output_file`：保存文件名（默认 'GRU_train_data_full.mat'）
  - `cfg.path_rand.*`：路径参数随机化范围（v0, R, theta_slope, bumpy_amp等）
  - `cfg.slip_cfg.*`：打滑注入配置（prob=0.5, t_start_range=[3,12], gamma_range=[0.3,0.7]）
  - `cfg.slip_in_turn.*`：**V4.2新增** 转弯场景轻度打滑（prob=0.15, gamma_range=[0.65,0.85]）
  - `cfg.stall_cfg.*`：堵转注入配置（prob=0.2, t_start_range=[11,17], load_range=[200,300]）
  - `cfg.slip_heuristic.*`：**V4.2新增** 打滑启发式配置（k_torque自动拟合，fit_scene='straight'）
  - `cfg.label_search.*`：**V4.2新增** 阈值网格搜索（enabled=false默认关闭，网格3×3×3）
- **输出数据**（工作区变量 `data`，自动保存至 `cfg.output_file`）：
  - `data.runs(k)`：每回合数据
    - `t`：时间向量 [Nx1] [s]
    - `u`：控制输入 [Nx2]=[F_cmd, omega_cmd] [N, rad/s]（MPC原始输出）
    - `y_raw`：原始输出 [Nx31]（来自 Simulink）
    - `label_main`：主分类标签 [Nx1]∈{1,2,3,4} (flat/slip/stall/slope)
    - `label_turn`：转弯状态标签 [Nx1]∈{-1,0,+1} (right/straight/left)
    - `theta`：坡度角真值 [Nx1] [rad]
    - `meta`：元数据（inject_info, path_params, noise_on, run_idx, seed）
- **特性**：
  - **路径参数随机化**：v0, R, theta_slope, bumpy_amp, turn_transition（每回合独立采样）
  - **打滑注入**（InjectionWrapper）：
    - 非转弯场景：`slip_gamma ∈ [0.3,0.7]`，概率50%
    - **V4.2新增** 转弯场景轻度打滑：`slip_gamma ∈ [0.65,0.85]`，概率15%（覆盖"转弯+打滑"）
  - **堵转注入**（InjectionWrapper）：施加外部负载 `stall_load ∈ [200,300] N`，所有场景均可
  - **标注策略**：优先级递减（**stall→slip→slope→flat**），转弯独立维度
  - **V4.2新增** 物理一致打滑启发式：`accel_expected ≈ k_torque·I_sum/mass`（k_torque自动拟合）
  - **V4.2新增** 阈值网格搜索：可选优化stall/slip判别阈值（3×3×3网格，默认关闭）
  - **最小驻留时间**：主类别0.20s，转弯状态0.40s
  - **不改Plant/parameters.m**：注入通过 InjectionWrapper 实现
- **依赖**：GRU_DataGen.slx（需配置 InjectionWrapper）
- **产物**：`GRU_train_data_full.mat`（默认，根目录）
- **版本**：V4.2 (2025-11-01，物理一致打滑启发式 + 转弯轻度打滑 + 阈值搜索)

### 2. **test_GRU_gen_train_data.m** - 数据生成测试脚本
- **路径**：test_GRU_gen_train_data.m（根目录）
- **职责**：快速测试GRU_gen_train_data，验证数据生成、标签分布、可视化
- **关键接口**：运行脚本（无参数）
- **产物**：`GRU_train_data_test.mat`（根目录）
- **版本**：V1.0

### 3. **GRU_prepare_dataset.m** - 数据预处理（已实现）
- **路径**：GRU_prepare_dataset.m（根目录）
- **职责**：GRU训练数据预处理（特征提取、序列化、归一化、分割）
- **使用方式**：**直接运行脚本**
  - 命令行：`run('GRU_prepare_dataset.m')` 或 `GRU_prepare_dataset`
  - 修改脚本开头的"配置区域"来调整参数
- **配置参数**（脚本顶部 `cfg` 结构体）：
  - `cfg.input_file`：输入数据文件（默认 'GRU_train_data_full.mat'）
  - `cfg.output_file`：输出数据文件（默认 'GRU_dataset_processed.mat'）
  - `cfg.seq_len`：序列长度（默认48 ≈ 2.4s）
  - `cfg.stride`：滑窗步长（默认12）
  - `cfg.train_ratio/val_ratio/test_ratio`：数据分割比例（默认0.7/0.15/0.15）
  - `cfg.tau_accel_lp`：加速度低通滤波时间常数（默认0.4s）
  - `cfg.tau_diff`：速度差分滤波时间常数（默认0.3s）
- **特征工程**（符合规范8.6，仅原始量+派生）：
  - **必选原始通道**（6个）：accel_x, gyro_z, I_lf, I_rr, omega_wheel_lf, omega_wheel_rr
  - **推荐原始通道**（3个）：delta_lf, delta_rr, gyro_y
  - **派生特征**（8个）：v_hat（轮速估计）, dv_hat_dt（滤波差分，V1.1）, ws_imbalance（轮速差异）, I_sum, I_diff_signed（V1.1新增）, I_diff_abs, accel_x_lp（低通滤波）, kappa_proxy（曲率近似）
  - 总计：17维特征（V1.1：16→17）
- **输出数据**（dataset结构体）：
  - 训练/验证/测试集（70%/15%/15%）
  - `X_{train/val/test}`：[N, seq_len, feat_dim]（归一化后）
  - `y_main_{train/val/test}`：[N,1] ∈ {1,2,3,4}（flat/slip/stall/slope）
  - `y_turn_{train/val/test}`：[N,1] ∈ {-1,0,+1}（right/straight/left）
  - `y_theta_{train/val/test}`：[N,1] [rad]（坡度角真值）
  - `mask_theta_{train/val/test}`：[N,1]（slope样本=1，其他=0）
  - `scaler`：归一化参数（mean, std，仅用训练集统计）
  - `feat_names`：特征名称列表（17个，V1.1）
  - `meta`：元数据（时间、版本、参数、tau_accel_lp、tau_diff）
- **特性**：
  - z-score归一化（仅用训练集统计，避免数据泄漏）
  - 随机分割（固定种子保证可复现）
  - 自动统计标签分布（主分类/转弯状态/坡度角）
  - 单独保存scaler（便于部署，V1.1含滤波参数）
  - **训练-推理一致性**（V1.1）：滤波参数写入meta/scaler，便于在线同步
- **依赖**：GRU_train_data_full.mat（由 GRU_gen_train_data.m 生成）
- **产物**：
  - `GRU_dataset_processed.mat`（完整数据集，根目录）
  - `GRU_scaler.mat`（归一化参数+滤波参数，根目录）
- **版本**：V1.1 (2025-10-30)
- **V1.1更新**：
  - dv_hat_dt 改为滤波差分（tau_diff=0.3s），抑制噪声
  - 增加 I_diff_signed 特征，保留方向信息
  - 特征维度：16→17
  - 滤波参数写入meta/scaler（便于在线推理同步）

### 4. **GRU_train.m** - GRU模型训练（已实现）
- **路径**：GRU_train.m（根目录）
- **职责**：GRU多任务学习训练脚本（主分类+转弯分类+坡度回归）
- **使用方式**：直接运行脚本（配置在脚本开头的cfg结构体）
- **关键接口**：`run('GRU_train.m')` 或 `GRU_train`
- **输入**：GRU_dataset_processed.mat（由 GRU_prepare_dataset.m 生成）
- **输出**：
  - `GRU_model.mat`：训练好的模型（dlnetwork + 三头权重）
  - `GRU_meta.mat`：训练元数据（超参数、训练历史、测试性能、**V1.1新增：详细评估指标**）
  - `GRU_logs/`：训练日志目录（损失曲线图、**V1.1新增：混淆矩阵可视化**）
- **架构**：
  - GRU×2（hidden=96, dropout=0.2）→ 最末时刻特征 → 三头：
    - 主分类头：Dense(4)+softmax（flat/slip/stall/slope）
    - 转弯分类头：Dense(3)+softmax（right/straight/left）
    - 坡度回归头：Dense(1)（θ̂ [rad]）
- **损失函数**：`L = CE_main(加权) + λ_turn·CE_turn + λ_theta·MSE_theta·mask_theta`
- **训练管理**：
  - Adam优化器（lr=1e-3，cosine/step调度）
  - 梯度裁剪（threshold=5.0）
  - 早停（patience=10，min_delta=1e-4）
  - 类别权重平衡（inverse/sqrt_inverse/balanced）
- **实现方式**：使用dlnetwork + dlfeval + dlgradient实现自定义训练循环
- **版本**：V1.1 (2025-11-01)
- **V1.1新增功能（详细评估与自动分析）**：
  - 测试集评估自动输出：
    - **混淆矩阵**（4×4，含可视化图）
    - **Per-class指标**（Precision/Recall/F1-Score/Support）
    - **macro-F1 / weighted-F1**
  - **自动分析函数**（`analyzeModelPerformance`）：
    - 根据8个维度自动诊断模型性能
    - 输出整体评估（完美/良好/需关注/需改进）
    - 针对性建议：过采样、调整类别权重、数据增强、检查标注、混淆对分析等
    - 警告检测：类别不平衡、低召回率、低精确率、严重混淆对
  - 评估指标保存至 `meta.test_detailed`（包含所有指标+分析结果）
  - **特别优化**：针对少数类样本量<500或召回率<0.6的情况，自动给出改进方案

### 5. **GRU_infer.m** - GRU推理接口（已实现）
- **路径**：GRU_infer.m（根目录）
- **职责**：GRU单步推理接口
- **关键接口**：`[label_main, label_turn, theta_hat, conf] = GRU_infer(x_seq, model)`
- **输入**：
  - `x_seq`：输入序列 [seq_len, feat_dim] 或 [feat_dim, seq_len, 1]（已归一化）
  - `model`：模型结构体（从 GRU_model.mat 加载）
- **输出**：
  - `label_main`：主分类标签 ∈ {1,2,3,4} (flat/slip/stall/slope)
  - `label_turn`：转弯状态标签 ∈ {-1,0,+1} (right/straight/left)
  - `theta_hat`：坡度角估计 [rad]
  - `conf`：置信度结构体（.conf_main [4×1], .conf_turn [3×1], .label_main_name, .label_turn_name）
- **特性**：
  - 自动处理输入维度（支持[seq_len,feat_dim]和[feat_dim,seq_len,1]）
  - 支持GPU加速（如果模型在GPU上）
  - 数值稳健性检查
- **版本**：V1.0

### 6. **GRU_state_classifier.m** - 在线推理封装（已实现）
- **路径**：GRU_state_classifier.m（根目录）
- **职责**：GRU工况识别在线推理封装（序列缓冲、最小驻留时间、低通滤波）
- **关键接口**：
  - 初始化：`state = GRU_state_classifier('init', params, model)`
  - 单步更新：`[state, out] = GRU_state_classifier('update', state, y_raw_t)`
- **输入**：
  - `params`：系统参数结构体（来自 parameters.m）
  - `model`：GRU模型结构体（来自 GRU_model.mat）
  - `y_raw_t`：当前时刻的原始输出 [31×1]（来自 output_eq/output_eq_ref）
- **输出**：
  - `state`：更新后的状态结构体
  - `out`：推理输出结构体
    - `.label_main` ∈ {1,2,3,4}
    - `.label_turn` ∈ {-1,0,+1}
    - `.theta_hat` [rad]
    - `.conf_main/conf_turn`：置信度
    - `.label_main_name/label_turn_name`：标签名称
    - `.debug`：调试信息
- **特性**：
  - **序列缓冲**：维护最近 seq_len 步的特征（FIFO）
  - **特征提取**：从 y_raw 提取原始传感量 + 派生特征（与 GRU_prepare_dataset.m 一致）
  - **最小驻留时间**：主分类0.20s，转弯状态0.40s（避免抖动）
  - **θ̂ 低通滤波**：τ=0.4s（一阶低通）
  - **数值稳健**：NaN/Inf兜底为当前状态，序列未满输出默认值（flat, straight, θ=0）
  - **归一化**：使用 model.scaler 自动归一化
- **运行策略**：
  - 初始阶段（序列未满 seq_len 步）：输出默认值
  - 候选标签稳定 ≥ dwell_steps：更新当前标签
  - 候选标签改变：重置计数器
- **版本**：V1.0

### 7. **test_GRU_workflow.m** - GRU工作流测试脚本（已实现）
- **路径**：test_GRU_workflow.m（根目录）
- **职责**：测试GRU工况识别完整工作流（训练验证、单步推理、在线推理、可视化）
- **关键接口**：`run('test_GRU_workflow.m')`
- **功能**：
  1. 检查依赖文件
  2. 加载模型和数据集
  3. 测试单步推理（GRU_infer，前10个样本）
  4. 测试在线推理（GRU_state_classifier，完整回合）
  5. 可视化结果（主分类、转弯状态、坡度角）
- **输出**：
  - 控制台：准确率、MAE、推理结果摘要
  - 图像：`GRU_logs/test_online_inference.png`
- **实际性能**（2025-10-31验证）：
  - 训练集：87.51%（主分类）, 98.82%（转弯）, 1.64°（坡度MAE）
  - 单步推理：80.00%（主分类）, 100.00%（转弯）, 1.13°（坡度MAE）
  - 在线推理：62.62%（主分类）, 100.00%（转弯）, 0.12ms/步
- **版本**：V1.0

### 8. **test_gru_performance.m** - GRU性能评估脚本
- **路径**：test_gru_performance.m（根目录）
- **职责**：统一执行离线（Train/Val/Test切分）与在线run级别评估，输出主分类/转弯/坡度MAE/延迟等核心指标。
- **使用方式**：`test_gru_performance()` 或 `cfg = struct('runs_per_mode',10,'enable_plots',false); test_gru_performance(cfg);`
- **主要特性**：
  - 按 `cfg.runs_per_mode` 对每个行驶模式抽样固定条数 run，确保指标覆盖 flat/straight/turn/slope/bumpy 等模式。
  - 自动保存 `split_<name>_metrics.mat`、`online_eval_<scene>.png`、`GRU_eval_summary_<timestamp>.mat` 到 `GRU_logs/eval_reports/`。
  - 在线阶段调用 `GRU_state_classifier` 进行驻留/滤波后的实时推理，并统计坡度识别延迟。
  - 配置项支持覆写模型/数据路径、run索引、seq_len、是否绘图等，便于批量对比训练版本。

---

## 模块：Simulink集成（已实现）

### 1. **LPVMPC_AGV_simulink.slx** - 完整闭环仿真模型
- **路径**：LPVMPC_AGV_simulink.slx（根目录）
- **职责**：Simulink环境下的LPV-MPC闭环控制仿真（含GRU工况识别）
- **关键模块**：
  - **Plant (AGV_Model S-Function)**：AGV动力学植物（调用agv_model_sfunc.m）
  - **Adaptive MPC Controller**：自适应MPC控制器（在线更新模型）
  - **GRU_State_Classifier (MATLAB Function)**：GRU工况识别（输出theta_hat）
  - **RhoFilter (MATLAB Function)**：调度变量滤波（ρ=[v;ω;θ_hat]）
  - **Path Error Calculator**：路径坐标系误差计算
  - **Reference Source (From Workspace)**：参考轨迹输入
- **信号流**：
  - 参考轨迹 → 误差计算 → MPC求解 → Plant → GRU推理 → theta_hat → RhoFilter → MPC更新
- **集成文档**：见 `README_GRU_Integration.md`
- **版本**：V1.0+

### 2. **README_GRU_Integration.md** - GRU集成指南（已实现）
- **路径**：README_GRU_Integration.md（根目录）
- **职责**：详细说明GRU模型如何集成到LPVMPC_AGV_simulink.slx
- **内容**：

### 3. **LPVMPC_AGV_simulink PreLoadFcn** - Simulink 模型初始化回调
- **位置**：Simulink 模型 `LPVMPC_AGV_simulink.slx` 的 **PreLoadFcn** 回调（脚本形式，不是独立 .m 文件）。
- **职责**：在仿真启动前完成控制相关全部环境初始化：
  - 调用 `init_project()` / `project_root()` / `results_dir()` 建立统一路径环境；
  - 加载基础参数 `params`、前馈结构 `ff_rt` 与名义速度 `v_ff_nom`；
  - 从 `data/models/` / 根目录加载 LPV 数据库（`lin_agv_db.mat` / `plant_grid*.mat`），构造 `db_rt`；
  - 基于 `db_rt` 创建 `MPCPlantBus` 与 `plant_ic`；
  - 加载 `maps_best.mat` 与 `ctrl.mat`（若不存在则调用 `mpc_setup_single_interp` 新建 `ctrl`）并写入 Base Workspace；
  - 从 `data/paths/path_*.mat` 批量加载 5 种参考路径，构造 `path_refs` 结构与按工况分组的 `timeseries` 集合 `path_inputs.<scenario>.<signal>`；
  - 基于 `path_inputs` 动态创建 Bus 对象 `PathRefBus`，供 From Workspace 以 `Bus: PathRefBus` 方式输出多路参考信号；
  - 从 `data/models/` / `data/gru/` 加载 GRU 工况识别模型和 scaler（`GRU_model.mat` / `GRU_scaler.mat`），导出为 `gru_model` / `gru_scaler`；
  - 构造并写出 `env_paths`（根目录/data/models/paths/gru/results）与 `results_paths`（results 下各子目录）的统一路径描述。
- **接口/变量输出**（写入 Base Workspace / Model Workspace）：
  - 控制相关：`params`, `ff_rt`, `v_ff_nom`, `db_rt`, `MPCPlantBus`, `plant_ic`, `ctrl`；
  - 参考路径：`path_refs`, `path_inputs`, `PathRefBus`；
  - AI 模型：`gru_model`, `gru_scaler`；
  - 路径环境：`env_paths`, `results_paths`。
- **版本**：V3.0（2025-12-10），详细流程参见 `docs/MPC参数加载逻辑说明.md` 中“PreLoadFcn 详细步骤”最新版补充。
  - 前提条件检查
  - 7步详细操作步骤（创建MATLAB Function、连接信号、配置MPC、测试）
  - 信号流总览图
  - 故障排查（5个常见问题）
  - 代码生成优化（3种方案）
  - 性能指标（延迟、精度、准确率）
- **关键步骤**：
  1. 添加GRU_State_Classifier MATLAB Function块
  2. 连接Plant输出(y_raw) → GRU输入
  3. 连接GRU输出(theta_hat) → MPC的MD端口
  4. 配置RhoFilter（ρ=[v;ω;θ_hat]）
  5. 配置Adaptive MPC自定义更新函数（mpc_update_from_rho）
  6. 配置PreLoadFcn加载模型和数据
  7. 运行测试验证集成
- **版本**：V1.0（2025-11-05）

### 3. **test_lpvmpc_with_gru_workflow.m** - GRU+MPC集成测试脚本（已实现）
- **路径**：test_lpvmpc_with_gru_workflow.m（根目录）
- **职责**：验证GRU与LPV-MPC的协同工作（离线仿真+性能分析）
- **关键接口**：`run('test_lpvmpc_with_gru_workflow.m')`
- **功能**：
  1. 检查依赖文件（Simulink模型、GRU模型、LPV数据库等）
  2. 加载系统参数、LPV数据库、GRU模型、创建MPC控制器
  3. 生成测试场景（turn/bumpy/slope）
  4. 检查Simulink模型关键模块（GRU_State_Classifier、RhoFilter）
  5. **离线测试**：完整20s闭环仿真（GRU → theta_hat → MPC → Plant）
  6. 结果分析（跟踪性能、GRU精度、实时性）
  7. 可视化（误差、坡度估计、工况分类、控制输入）
- **输出**：
  - 控制台：RMSE、MAE、求解时间统计
  - 图像：`test_lpvmpc_with_gru_result.png`（6子图）
  - 日志：`test_lpvmpc_with_gru_log.mat`
- **测试场景**：bumpy（颠簸直行，theta=0.2·sin(t)）
- **性能指标**（示例目标）：
  - RMSE(e_y) < 0.15 m
  - MAE(theta) < 2°
  - 平均求解时间 < 5 ms
- **版本**：V1.0（2025-11-05）

### 4. **test_closed_loop_performance.m** - LPVMPC闭环批量评估
- **路径**：test_closed_loop_performance.m（根目录）
- **职责**：批量运行 `LPVMPC_AGV_simulink`，针对多行驶模式统计速度/姿态误差、坡度延迟与执行器饱和，便于GRU与控制器联合验证。
- **使用方式**：`test_closed_loop_performance()` 或通过 `cfg.scenarios`/`cfg.mode_sample_count` 覆写场景列表与抽样数。
- **主要特性**：
  - 默认覆盖 flat/straight/turn/straight_turn/slope/bumpy 六种路径，可自定义结构体场景（含 path_file/name/stop_time）。
  - 对每个场景保存时序数据(`timeseries_<scene>.mat` 可选)与聚合指标(`closed_loop_summary_<tag>.mat`)至 `GRU_logs/closed_loop_eval/`。
  - F_cmd 饱和检测、坡度识别延迟、速度RMS、姿态MAE等指标统一输出，并在终端打印分场景摘要。
  - 自动处理 Simulink 模型加载、结果目录创建与信号名称映射，支持扩展指标计算。

---

## 下一步：扩展功能（建议）

1. **硬件部署**
   - 代码生成优化（GRU → ONNX/Coder/手动展开）
   - HIL测试（dSPACE/Speedgoat）

---

## 参考文档

- `.cursor/rules/lpvmpc.mdc` - LPV-MPC设计规范（已更新：ρ有符号、颠簸0.2 rad、API落地澄清、失败处理细化）
- `README_LPV.md` - LPV建模说明
- `README_LPVMPC_Usage.md` - LPV-MPC使用指南
- `README_paths.md` - 参考路径生成模块

---

## 模块：GRU 分类测试与评估（根目录，辅助分析）

### 1. **test_GRU_latency.m** - GRU 决策延迟参数扫描
- **路径**：`test_gru_latency.m`
- **职责**：在固定 GRU 模型和数据集的前提下，系统扫描主分类驻留时间 `dwell_main`、转弯驻留时间 `dwell_turn` 与坡度估计一阶滤波时间常数 `tau_theta` 对整体性能的影响，帮助选择一组在“延迟、准确率、抖动”之间折中的默认参数。
- **使用方式**：
  - 直接运行脚本：`run('test_gru_latency.m')`。
  - 在脚本顶部的配置区域修改候选参数网格与评分权重。
- **评估内容**：
  - 对每组 (dwell_main, dwell_turn, tau_theta) 组合，基于统一的离线 run 集合统计：
    - 主分类准确率 / 转弯准确率；
    - 坡度估计 MAE（deg）；
    - Slope/Slip/Turn 场景识别延迟（s）；
    - 抖动次数（label 翻转次数 / 分钟）。
  - 使用统一的加权打分函数，对所有组合排序并输出 top-N 结果表。
- **与在线推理的关系**：
  - 根据本脚本给出的最优组合，当前默认值已更新为：`dwell_main = 0.20 s`，`dwell_turn = 0.40 s`，`tau_theta = 0.15 s`，并同步到 `GRU_state_classifier.m` 与数据标注逻辑中（转弯驻留时间 0.40 s）。
- **产物**：
  - 控制台：参数组合排行榜及指标对比表。
  - 日志：`GRU_logs/latency_eval/latency_eval_<timestamp>.mat`（包含各组合详细指标与打分）。

### 2. **test_gru_filter_constants.m** - 输入滤波时间常数评估
- **路径**：`test_gru_filter_constants.m`
- **职责**：在不改动离线数据集和 GRU 训练结果的前提下，针对 GRU 输入侧一阶滤波时间常数 `tau_accel_lp`（加速度低通）与 `tau_diff`（速度差分滤波）做敏感性分析，比较不同组合对分类精度、坡度估计与延迟/抖动的影响。
- **使用方式**：
  - 直接运行脚本：`run('test_gru_filter_constants.m')`。
  - 在脚本顶部配置区域设置：
    - `cfg.model_file`、`cfg.raw_data_file`、`cfg.results_dir`；
    - `cfg.runs_per_mode`：每种行驶模式抽样的 run 数量（当前默认 10）；
    - `cfg.tau_accel_lp_override` / `cfg.tau_diff_override`：如不为空，则对加载的 `model.scaler` 中对应字段进行覆写，实现“在线试验不同滤波时间常数”；
    - `cfg.save_timeseries`：是否保存逐 run 时序细节，便于深入分析。
- **评估内容**：
  - 对选中的 run 集合逐 run 调用 `GRU_state_classifier`，在在线决策逻辑（驻留 + θ̂ 低通）保持不变的前提下统计：
    - 主分类/转弯准确率；
    - 坡度估计 MAE（deg）；
    - Slope/Slip/Turn 延迟（s）；
    - 抖动频率（次/分钟）。
  - 根据 `cfg.runs_per_mode`，针对每个行驶模式（flat/straight/turn/straight_turn/slope/bumpy 等）尽量等量抽样 run，使指标覆盖六种典型工况。
- **典型用法**：
  - 保持当前默认 `tau_accel_lp = 0.4 s`，`tau_diff = 0.3 s`，多次运行脚本确认基线稳定性；
  - 在不重新生成数据/不重新训练的条件下，临时将 `cfg.tau_accel_lp_override` / `cfg.tau_diff_override` 设为其他候选值（如 0.3 / 0.2），重复运行脚本，对比输出指标与波动范围；
  - 确认“仅调输入滤波时间常数”对整体延迟影响有限、主要起到噪声抑制与细节保持的权衡作用。
- **产物**：
  - 控制台：单次评估的汇总指标表。
  - 日志：`GRU_logs/filter_constant_eval/filter_eval_<timestamp>.mat`，包含本次评估的配置、逐 run 指标和聚合结果。

### 3. **test_gru_performance.m** - 统一性能评估（补充说明）
- **补充职责**：在原有说明基础上，本脚本可以作为上面两个专项评估的“基线评估”，用于在修改 GRU 训练数据/模型或在线参数（例如 dwell、tau_theta）后，统一检查：
  - Train/Val/Test 切分上的单步推理性能；
  - run 级别在线推理准确率、坡度 MAE 与延迟；
  - 各行驶模式下的典型表现与运行时间开销。
- **推荐使用顺序**：
  1. 使用 `GRU_gen_train_data.m` + `GRU_prepare_dataset.m` + `GRU_train.m` 完成一轮训练；
  2. 用 `test_gru_performance.m` 做一次完整评估，确认模型本身的离线/在线性能；
  3. 若需要进一步精调在线决策逻辑，再分别使用 `test_GRU_latency.m`（dwell/tau_theta）与 `test_gru_filter_constants.m`（tau_accel_lp/tau_diff）做局部敏感性分析。
