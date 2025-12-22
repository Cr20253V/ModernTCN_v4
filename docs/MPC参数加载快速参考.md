# MPC 参数加载快速参考卡片

> 快速查阅版本，详细说明见 `MPC参数加载逻辑说明.md`

---

## 一、初始化阶段（PreLoadFcn，仅运行一次）

| 步骤 | 文件/变量 | 作用 | 输出到 |
|-----|----------|------|-------|
| **0** | `parameters.m` | 加载物理参数、Ts | `params` (Base WS) |
| **1** | `lin_agv_db.mat` | 加载LPV数据库（A/B/C/D/E网格） | `db_rt` (Base WS) |
| **2** | 内部生成 | 创建总线类型 | `MPCPlantBus`, `plant_ic` |
| **3** | `maps_best.mat` | 加载优化权重/约束参数 | `maps_best` (内存) |
| **4** | `mpc_setup_single_interp()` | 创建MPC控制器对象 | `ctrl` (Base WS) |
| **5** | `GRU_model.mat` | 加载GRU工况识别模型 | `gru_model` (Base WS) |

### 关键变量结构

#### `db_rt`（LPV数据库）
```matlab
db_rt.A     % [Nv×Nw×Nt×4×4] 状态矩阵
db_rt.B     % [Nv×Nw×Nt×4×2] 输入矩阵（MV）
db_rt.E     % [Nv×Nw×Nt×4×1] 扰动矩阵（MD）
db_rt.grid  % {V, W, T} 网格定义
db_rt.Ts    % 采样周期
```

#### `ctrl`（MPC控制器）
```matlab
ctrl.mpcobj  % MATLAB MPC对象
ctrl.maps    % 权重/约束映射表
  .Q_range     % [2×4] 输出权重范围
  .R_range     % [2×2] 输入权重范围
  .dR_range    % [2×2] 速率权重范围
  .alpha_Q/R/dR % 形状参数下界
  .beta_Q/R/dR  % 形状参数上界
  .scale_umin/umax_lo/hi % 约束缩放
  .omega_threshold  % 转弯判定阈值 (0.15 rad/s)
  .q_y_gain_max     % 转弯时q_y增益 (1.8)
```

#### `maps_best`（贝叶斯优化结果）
```matlab
% 由 Bayesian_Optimization.m 生成
% 在 PreLoadFcn 步骤4 中复制到 ctrl.maps
maps_best.Q_range   % 覆盖默认权重范围
maps_best.alpha_Q   % 覆盖形状参数
maps_best.scale_*   % 覆盖约束缩放
```

---

## 二、在线更新阶段（每个仿真步）

```
Step 1: Plant 输出
  ↓ y_raw [31×1]
Step 2: GRU 推理
  ↓ theta_hat [rad]
Step 3: 构造 ρ（RhoFilter）
  ↓ rho_f = [v; ω; θ_hat]（滤波，τ=0.4s）
Step 4: 模型/权重插值
  mpc_update_from_rho(rho_f, db_rt, ctrl.maps)
  ↓ upd.{A,B,C,D,E,Q,R,dR,umin,umax}
Step 5: MPC 求解
  mpcmoveAdaptive(mpcobj, xmpc, plant_model, Nominal, y_meas, r_ref, md)
  ↓ u_mpc = [F_cmd; omega_cmd]
Step 6: Plant 更新
  state_eq_ref(x, u, theta_ground, params)
  ↓ x_next
```

---

## 三、关键函数接口速查

### `mpc_setup_single_interp(db, opts)`
**输入**：
- `db`：LPV数据库（来自 `db_rt`）
- `opts`：设计选项（Np, Nc, Q, R, dR, 约束等）

**输出**：
- `ctrl`：控制器结构体
  - `ctrl.mpcobj`：MPC对象
  - `ctrl.maps`：权重/约束映射表

**默认参数**：
```matlab
Np = round(1.5/Ts);      % 预测时域 ≈1.5s (30步)
Nc = round(0.5/Ts);      % 控制时域 ≈0.5s (10步)
Q  = [3, 8, 1, 1];       % [e_y, e_psi, e_v, e_omega]
R  = [1e-3, 1e-3];       % [F_cmd, omega_cmd]
dR = [1e-2, 1e-2];       % 速率权重
umin = [-300; -0.6];     % 输入下界
umax = [300; 0.6];
```

---

### `mpc_update_from_rho(rho, db, maps)`
**输入**：
- `rho`：调度变量 `[v; omega; theta]` (3×1)
- `db`：LPV数据库
- `maps`：权重/约束映射表

**输出**：
- `upd`：更新结构体
  - `A/B/C/D`：插值后的模型矩阵
  - `E/Bv`：扰动影响矩阵（坡度角）
  - `Q/R/dR`：插值后的权重
  - `umin/umax`：插值后的约束

**核心算法**：
1. 归一化 `ρ` 到 `[0,1]^3`
2. 定位8个顶点（三线性插值）
3. 计算插值权重 `w = [w1,...,w8]`
4. 插值模型：`A = Σ w_i * A_i`
5. 插值权重：按维度映射（`fy, fpsi, fv, fomega`）
6. 场景自适应：转弯时提高 `q_y`

---

## 四、权重调度策略

### 方案A：按维度映射（默认）
每个权重元素独立调度：
```matlab
% 调度因子（默认线性组合）
fy   = 0.3*v_n + 0.2*ω_n + 0.5*θ_n  % 影响 q_y
fpsi = 0.1*v_n + 0.7*ω_n + 0.2*θ_n  % 影响 q_psi
fv   = 0.8*v_n + 0.1*ω_n + 0.1*θ_n  % 影响 q_v
fomega = 0.2*v_n + 0.6*ω_n + 0.2*θ_n  % 影响 q_omega

% 权重插值
q_y = Q_min(1) + fy * (Q_max(1) - Q_min(1))
```

### 方案B：场景自适应（叠加）
转弯时自动提高 `q_y`：
```matlab
if |ω| < ω_thresh - Δω:
    q_y_gain = 1.0          % 直线区域
elseif |ω| > ω_thresh + Δω:
    q_y_gain = gain_max     % 转弯区域 (1.8×)
else:
    q_y_gain = smooth_interp  % 平滑过渡

q_y_final = q_y * q_y_gain
```

**参数**（在 `ctrl.maps` 中）：
- `omega_threshold = 0.15` rad/s
- `q_y_gain_max = 1.8`
- `transition_width = 0.05` rad/s

---

## 五、约束调度策略

### 基于角速度的线性插值
```matlab
ω_n = (ω - ω_min) / (ω_max - ω_min)  % 归一化

umin = (1-ω_n) * umin_lo + ω_n * umin_hi
umax = (1-ω_n) * umax_lo + ω_n * umax_hi
```

### 缩放因子（叠加）
```matlab
scale_umin = (1-ω_n) * scale_lo + ω_n * scale_hi
umin_final = umin * scale_umin
```

**示例**：
- 直线（`ω_n=0`）：使用 `umin_lo`, `scale_lo`
- 转弯（`ω_n=1`）：使用 `umin_hi`, `scale_hi`（可放宽约束）

---

## 六、贝叶斯优化流程

```
Bayesian_Optimization(params, db, options)
  ├─ 第一阶段：全局搜索（100次评估，默认）
  │   ├─ 优化变量：q_y, q_psi, ..., tau (19个)
  │   ├─ 目标函数：Cost_Function
  │   │   ├─ 场景：turn, slope, straight_turn, bumpy, straight
  │   │   └─ 代价：J = Σ w_s * J_scene
  │   └─ 输出：全局最优点
  │
  ├─ 第二阶段：局部精细搜索（30次评估，默认）
  │   ├─ 优化范围：全局最优点 ±20%
  │   └─ 输出：局部最优点
  │
  └─ 保存结果：maps_best.mat（根目录）
      ├─ Q_range, R_range, dR_range
      ├─ alpha_Q/R/dR, beta_Q/R/dR
      ├─ scale_umin/umax_lo/hi
      └─ timestamp, version
```

**启动脚本**：`start_bayesian.m`

---

## 七、故障排查速查

| 症状 | 可能原因 | 检查项 | 解决方案 |
|-----|---------|-------|---------|
| **MPC求解失败** | 约束过严 | `Info.QPCode` | 放宽输出约束 `ymin/ymax` |
| | 模型不稳定 | `max(abs(eig(A)))` | 检查线性化网格范围 |
| | 权重过大 | `upd.Q` | 检查 `Q_range` 上界 |
| **权重未生效** | 外部端口未连接 | Simulink块配置 | 启用"External Weights" |
| | 插值被禁用 | `ctrl.maps.enable_weight_interp` | 设为 `true` |
| **坡度补偿无效** | GRU估计不准 | `abs(θ_hat - θ_ground)` | 检查GRU模型性能 |
| | MD通道错误 | `upd.E(3,:)` | 确认第3行非零 |
| | MD未连接 | Simulink接线 | 检查 `md` 端口 |
| **转弯e_y过大** | `q_y` 过低 | `upd.Q(1)` | 提高 `Q_range(1)` |
| | 场景自适应未启用 | `q_y_gain` | 检查 `omega_threshold` |
| | 增益过小 | `q_y_gain_max` | 调整为 1.8~2.5 |

---

## 八、调试技巧

### 1. 打印当前 ρ 与插值结果
```matlab
fprintf('ρ = [%.3f, %.3f, %.3f]\n', rho(1), rho(2), rho(3));
upd = mpc_update_from_rho(rho, db_rt, ctrl.maps);
fprintf('Q = [%.2f, %.2f, %.2f, %.2f]\n', upd.Q);
fprintf('插值顶点: [%d,%d,%d] 至 [%d,%d,%d]\n', ...
    upd.debug.i_range(1), upd.debug.j_range(1), upd.debug.k_range(1), ...
    upd.debug.i_range(2), upd.debug.j_range(2), upd.debug.k_range(2));
```

### 2. 验证模型矩阵插值
```matlab
% 检查特征值（稳定性）
eig_A = eig(upd.A);
fprintf('max|λ(A)| = %.3f (应 < 1.0)\n', max(abs(eig_A)));

% 检查扰动影响（坡度角）
fprintf('E(纵向) = %.6f (应非零)\n', upd.E(3,1));
```

### 3. 观察场景自适应效果
```matlab
omega_abs = abs(rho(2));
fprintf('|ω| = %.3f rad/s\n', omega_abs);
fprintf('q_y_gain = %.2f (阈值: %.3f)\n', ...
    q_y_gain, ctrl.maps.omega_threshold);
```

### 4. 检查权重范围加载
```matlab
fprintf('Q_range:\n');
disp(ctrl.maps.Q_range);
fprintf('基准Q: [%.2f, %.2f, %.2f, %.2f]\n', ...
    mean(ctrl.maps.Q_range, 1));
```

---

## 九、文件清单

| 文件名 | 位置 | 作用 |
|-------|------|------|
| `parameters.m` | 根目录 | 集中参数定义 |
| `lin_agv_db.mat` | 根目录 | LPV数据库（离线生成） |
| `maps_best.mat` | 根目录 | 优化权重/约束（贝叶斯优化产物） |
| `ctrl.mat` | 根目录 | 预创建的控制器（可选，节省时间） |
| `GRU_model.mat` | 根目录 | GRU工况识别模型 |
| `mpc_setup_single_interp.m` | 根目录 | MPC控制器创建 |
| `mpc_update_from_rho.m` | 根目录 | 在线参数更新 |
| `Cost_Function.m` | 根目录 | MPC闭环评估 |
| `Bayesian_Optimization.m` | 根目录 | 贝叶斯优化驱动 |
| `start_bayesian.m` | 根目录 | 优化启动脚本 |
| `LPVMPC_AGV_simulink.slx` | 根目录 | Simulink仿真模型 |

---

## 十、常用命令速查

### 生成LPV数据库
```matlab
params = parameters();
grid.V_grid = [0.8; 1.0; 1.2];
grid.W_grid = [-0.2; 0.0; 0.2];
grid.T_grid = [-0.2; 0.0; 0.2];
lin_opts = struct('coord','path','disc','zoh','keep_E',true,'export_mat','lin_agv_db.mat');
db = lin_agv_grid(params, grid, lin_opts);
```

### 创建MPC控制器
```matlab
params = parameters();
db = load('lin_agv_db.mat', 'db').db;
ctrl = mpc_setup_single_interp(db, struct());
save('ctrl.mat', 'ctrl');
```

### 运行贝叶斯优化
```matlab
params = parameters();
db = load('lin_agv_db.mat', 'db').db;
options.MaxObjectiveEvaluations = 100;
[best, boResults] = Bayesian_Optimization(params, db, options);
% 自动生成 maps_best.mat
```

### 运行Simulink仿真
```matlab
% 确保 PreLoadFcn 已配置
open_system('LPVMPC_AGV_simulink.slx');
sim('LPVMPC_AGV_simulink');
```

### 检查优化结果
```matlab
load('maps_best.mat');
fprintf('优化权重基准:\n');
fprintf('  Q_base = [%.2f, %.2f, %.2f, %.2f]\n', mean(maps_best.Q_range,1));
fprintf('  R_base = [%.6f, %.6f]\n', mean(maps_best.R_range,1));
fprintf('  dR_base = [%.6f, %.6f]\n', mean(maps_best.dR_range,1));
```

---

## 十一、核心设计理念

1. **分层设计**：参数 → 数据库 → 控制器 → 在线更新
2. **智能调度**：根据工况 `ρ` 自适应调整模型和参数
3. **按维度映射**：每个权重元素独立调度（非统一缩放）
4. **场景自适应**：转弯时自动提高横向跟踪精度
5. **前馈补偿**：坡度角进入MD通道，提前预测扰动
6. **贝叶斯优化**：自动寻找最优权重范围
7. **数值稳健**：边界饱和、滤波、归一化保证稳定性

---

**版本**：V1.0（2025-11-06）  
**配套文档**：`MPC参数加载逻辑说明.md`（详细版）  
**维护记录**：见 `change.md`

