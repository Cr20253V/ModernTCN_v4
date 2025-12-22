# LPVMPC_AGV_simulink.slx 控制器参数加载逻辑说明

## 概述

本文档详细说明 **LPVMPC_AGV_simulink.slx** 运行时，MPC 控制器参数的**完整加载链路**，包括：
- 初始化阶段（PreLoadFcn）
- 控制器创建（mpc_setup_single_interp）
- 在线参数更新（mpc_update_from_rho）

---

## 一、参数加载流程总览

```
┌────────────────────────────────────────────────────────────────┐
│                    Simulink 模型启动                            │
│                    PreLoadFcn 执行                             │
└────────────────┬───────────────────────────────────────────────┘
                 │
    ┌────────────┴────────────┐
    │  步骤0：基础参数加载     │
    │  parameters.m           │
    │  → params 结构体         │
    └────────────┬────────────┘
                 │
    ┌────────────┴────────────┐
    │  步骤1：LPV 数据库加载   │
    │  lin_agv_db.mat         │
    │  → db_rt 结构体          │
    │  (A/B/C/D/E 网格表)     │
    └────────────┬────────────┘
                 │
    ┌────────────┴────────────┐
    │  步骤2：创建总线类型     │
    │  MPCPlantBus            │
    └────────────┬────────────┘
                 │
    ┌────────────┴────────────┐
    │  步骤3：加载优化参数     │
    │  maps_best.mat          │
    │  → maps_best 结构体      │
    │  (Q/R/dR范围、约束缩放) │
    └────────────┬────────────┘
                 │
    ┌────────────┴────────────────────────────────┐
    │  步骤4：创建/加载 MPC 控制器                 │
    │  ┌──────────────────────────────────────┐  │
    │  │ 优先：加载 ctrl.mat                   │  │
    │  │ 回退：调用 mpc_setup_single_interp    │  │
    │  │       使用 maps_best 中的权重         │  │
    │  └──────────────────────────────────────┘  │
    │  → ctrl 结构体                              │
    │    - ctrl.mpcobj (MATLAB MPC对象)          │
    │    - ctrl.maps   (权重/约束映射表)          │
    └────────────┬────────────────────────────────┘
                 │
    ┌────────────┴────────────┐
    │  步骤5：变量写入工作区   │
    │  base + Model Workspace │
    └────────────┬────────────┘
                 │
                 ▼
       ┌─────────────────┐
       │  模型仿真运行    │
       └─────────────────┘
                 │
       ┌─────────┴───────────────────────────┐
       │ 在线参数更新（每个仿真步）           │
       │ ┌─────────────────────────────────┐ │
       │ │ Adaptive MPC 自定义更新函数      │ │
       │ │ → mpc_update_from_rho(ρ,db,maps)│ │
       │ │   输入：ρ=[v;ω;θ]（滤波后）      │ │
       │ │   输出：A/B/C/D/E + Q/R/dR       │ │
       │ └─────────────────────────────────┘ │
       └─────────────────────────────────────┘
```

---

## 二、PreLoadFcn 详细步骤

### 步骤 0：加载基础参数 `parameters.m`

**目的**：加载车辆物理参数、控制参数、采样周期等。

**执行代码**：
```matlab
params = parameters();
```

**关键输出变量**：
- `params.Ts`：采样周期（0.05 s）
- `params.mass`：车辆质量（100 kg）
- `params.L`：轴距（2.0 m）
- `params.gravity`：重力加速度（9.81 m/s²）
- 其他：轮胎、电机、执行器、阻力参数等

**写入位置**：
- Base Workspace：`params`
- Model Workspace：`params`, `ff_rt`（前馈计算用），`v_ff_nom`

---

### 步骤 1：加载 LPV 数据库

**目的**：加载离散时间线性化模型网格表（A/B/C/D/E 矩阵）。

**执行代码**：
```matlab
% 尝试加载（优先级递减）
dbFiles = {'lin_agv_db.mat','plant_grid_test.mat','plant_grid.mat'};
```

**数据结构检测**：
- **情况1（标准格式）**：`S.db.A/B/C/D/E`（结构体嵌套）
- **情况2（顶层格式）**：`S.A/B/C/D/E`（直接顶层）

**关键输出变量**：
- `db_rt.A`：状态矩阵网格 `[Nv×Nw×Nt×4×4]`
- `db_rt.B`：输入矩阵网格 `[Nv×Nw×Nt×4×2]`（MV部分）
- `db_rt.C`：输出矩阵网格 `[Nv×Nw×Nt×4×4]`
- `db_rt.D`：直通矩阵网格 `[Nv×Nw×Nt×4×2]`
- `db_rt.E`：扰动矩阵网格 `[Nv×Nw×Nt×4×1]`（MD部分，坡度角θ）
- `db_rt.grid`：网格定义 `{V, W, T}`（速度、角速度、坡度角）
- `db_rt.Ts`：采样周期（与 params.Ts 一致）
- 维度信息：`nx=4, nu=2, ny=4, nd=1, Nv, Nw, Nt`

**网格范围示例**（3×3×3 默认网格）：
- `V_grid = [0.8, 1.0, 1.2]` m/s
- `W_grid = [-0.2, 0.0, 0.2]` rad/s（有符号，负为右转，正为左转）
- `T_grid = [-0.2, 0.0, 0.2]` rad（坡度角，≈±11.5°）

**写入位置**：
- Base Workspace：`db_rt`
- Model Workspace：`db_rt`

---

### 步骤 2：创建 MPCPlantBus

**目的**：为 Adaptive MPC 块创建总线类型定义（用于模型端口）。

**执行代码**：
```matlab
nu_md = nu + nd;  % 3 (2 MV + 1 MD)
samplePlant = struct( ...
    'A',  zeros(nx, nx), ...     % 4x4
    'B',  zeros(nx, nu_md), ...  % 4x3（含MD列）
    'C',  zeros(ny, nx), ...     % 4x4
    'D',  zeros(ny, nu_md), ...  % 4x3
    'U',  zeros(nu_md, 1), ...   % 3x1（2 MV + 1 MD）
    'X',  zeros(nx, 1), ...
    'Y',  zeros(ny, 1), ...
    'DX', zeros(nx, 1), ...
    'Ts', Ts );
info = Simulink.Bus.createObject(samplePlant);
```

**关键输出**：
- `MPCPlantBus`：Simulink 总线类型
- `plant_ic`：初始样本结构体（用于块初始化）

**注意事项**：
- `B` 矩阵列数 = `nu_md = 3`（2个MV + 1个MD）
- 在线更新时，第3列将填充 `E(ρ)`（坡度扰动影响）

---

### 步骤 3：加载优化参数 `maps_best.mat`

**目的**：加载贝叶斯优化得到的**最优权重和约束参数**。

**执行代码**：
```matlab
if exist('maps_best.mat','file')
    Tm = load('maps_best.mat');
    maps_best = Tm.maps_best;
end
```

**maps_best 结构体内容**：

#### 3.1 权重范围
- `Q_range`：`[2×4]` 矩阵（行1=最小值，行2=最大值）
  - 列顺序：`[q_y, q_psi, q_v, q_omega]`
  - 示例：`Q_range = [15.0, 20.0, 3.5, 1.2; 22.0, 28.0, 5.5, 2.5]`
- `R_range`：`[2×2]` 矩阵
  - 列顺序：`[r_F, r_omega]`
  - 示例：`R_range = [0.0008, 0.0006; 0.0025, 0.0018]`
- `dR_range`：`[2×2]` 矩阵
  - 列顺序：`[r_dF, r_domega]`
  - 示例：`dR_range = [0.008, 0.006; 0.018, 0.015]`

#### 3.2 形状参数（权重插值形状控制）
- `alpha_Q`：`[1×4]`，Q各分量的下阈值（归一化域[0,1]）
- `beta_Q`：`[1×4]`，Q各分量的上阈值（满足 `alpha ≤ beta`）
- `alpha_R`、`beta_R`：`[1×2]`（同上，针对R）
- `alpha_dR`、`beta_dR`：`[1×2]`（同上，针对dR）

**作用**：在 `[alpha, beta]` 区间内线性过渡权重，区间外夹紧。

#### 3.3 约束缩放参数
- `scale_umin_lo`：`[1×2]`，|ω|=0 时的 `umin` 缩放系数
- `scale_umin_hi`：`[1×2]`，|ω|=max 时的 `umin` 缩放系数
- `scale_umax_lo/hi`：同上（针对 `umax`）

**作用**：根据角速度大小动态调整输入约束（例如转弯时放宽力约束）。

#### 3.4 其他参数
- `rho_min`、`rho_max`：调度变量范围 `[3×1]`（与网格端点一致）
- `timestamp`：生成时间戳
- `version`：版本号
- `note`：备注说明

**写入位置**：
- 仅保存在内存（`maps_best` 变量），不直接写入 Base Workspace

---

### 步骤 4：创建/加载 MPC 控制器

#### 4.1 优先尝试加载 `ctrl.mat`

**执行代码**：
```matlab
if exist('ctrl.mat','file')
    Tc = load('ctrl.mat');
    if isfield(Tc,'ctrl')
        ctrl = Tc.ctrl;
        ctrl_source = 'ctrl.mat';
    end
end
```

**适用场景**：
- 已经离线创建并保存了控制器
- 避免每次运行都重新创建（节省时间）

#### 4.2 回退：创建新控制器

**执行代码**：
```matlab
if isempty(ctrl) && exist('mpc_setup_single_interp','file')==2
    % 确定权重参数
    if maps_loaded && isfield(maps_best,'Q_range')
        Q_base = mean(maps_best.Q_range, 1);  % 取范围中点
        R_base = mean(maps_best.R_range, 1);
        dR_base = mean(maps_best.dR_range, 1);
    else
        % 使用默认权重
        Q_base = [3, 8, 1, 1];
        R_base = [1e-3, 1e-3];
        dR_base = [1e-2, 1e-2];
    end
    
    mpc_opts = struct('Np',30,'Nc',10, ...
        'Q', Q_base, 'R', R_base, 'dR', dR_base);
    
    ctrl = mpc_setup_single_interp(db_rt, mpc_opts);
end
```

**关键决策逻辑**：
1. **若有 maps_best**：使用优化的权重范围中点作为基准
2. **若无 maps_best**：使用硬编码默认值（保守策略）

#### 4.3 复制 maps_best 参数到 ctrl.maps

**执行代码**：
```matlab
if maps_loaded
    fields = {'Q_range','R_range','dR_range', ...
        'alpha_Q','beta_Q','alpha_R','beta_R','alpha_dR','beta_dR', ...
        'scale_umin_lo','scale_umin_hi','scale_umax_lo','scale_umax_hi'};
    
    for i = 1:length(fields)
        if isfield(maps_best, fields{i})
            ctrl.maps.(fields{i}) = maps_best.(fields{i});
        end
    end
end
```

**作用**：
- 将贝叶斯优化得到的参数覆盖控制器的默认映射表
- `ctrl.maps` 将在后续在线更新时使用

**写入位置**：
- Base Workspace：`ctrl`

---

### 步骤 5：GRU 模型加载（新增）

**执行代码**：
```matlab
S_gru = load('GRU_model.mat');
if isfield(S_gru, 'model')
    assignin('base', 'gru_model', S_gru.model);
end
```

**关键输出**：
- `gru_model`：GRU工况识别模型（用于估计坡度角 `θ_hat`）

---

## 三、控制器创建详解：`mpc_setup_single_interp.m`

### 3.1 函数签名

```matlab
function ctrl = mpc_setup_single_interp(db, opts)
```

**输入**：
- `db`：LPV数据库（来自 PreLoadFcn 的 `db_rt`）
- `opts`：设计选项
  - `Np`, `Nc`：预测/控制时域（步数）
  - `Q`, `R`, `dR`：权重向量
  - `umin`, `umax`, `dumin`, `dumax`：约束
  - `ymin`, `ymax`：输出约束
  - `soft_weight_pos`, `soft_weight_yaw`：软约束惩罚

**输出**：
- `ctrl`：控制器结构体
  - `ctrl.mpcobj`：MATLAB MPC对象
  - `ctrl.db`：数据库引用
  - `ctrl.opts`：设计选项
  - `ctrl.maps`：权重/约束映射表
  - `ctrl.meta`：元数据

---

### 3.2 默认参数（若 opts 未指定）

#### 时域
```matlab
Np = round(1.5 / Ts);  % 预测时域 ≈ 1.5s（30步@Ts=0.05s）
Nc = round(0.5 / Ts);  % 控制时域 ≈ 0.5s（10步）
```

#### 权重
```matlab
Q  = [3, 8, 1, 1];      % [q_y, q_psi, q_v, q_omega]
R  = [1e-3, 1e-3];      % [r_F, r_omega]
dR = [1e-2, 1e-2];      % [r_dF, r_domega]
```

**说明**：
- `q_psi = 8`：航向误差权重最高（转向精度优先）
- `q_y = 3`：横向位置误差次之
- `q_v`, `q_omega = 1`：速度/角速度误差权重较低
- `R` 很小：允许较大控制输入（避免保守）
- `dR` 中等：平滑性约束适中

#### 约束
```matlab
umin = [-300; -0.6];       % [F_min(N), omega_min(rad/s)]
umax = [300; 0.6];
dumin = [-400; -0.4];      % [ΔF_min(N/步), Δω_min((rad/s)/步)]
dumax = [400; 0.4];
ymin = [-1.0; -0.5; -0.5; -0.3];  % [e_y, e_psi, e_v, e_omega]
ymax = [1.0; 0.5; 0.5; 0.3];
```

**说明**：
- 输入约束：力 ±300N，角速度 ±0.6 rad/s（≈34°/s）
- 速率约束：防止控制量突变
- 输出约束：软约束（允许违反，但惩罚）
  - `e_y` ±1.0 m（横向误差）
  - `e_psi` ±0.5 rad（≈29°，航向误差）
  - `e_v`, `e_omega`：实际未约束（设为 `[-Inf, Inf]`）

#### 软约束惩罚
```matlab
soft_weight_pos = 1e4;  % e_y 软约束权重
soft_weight_yaw = 1e4;  % e_psi 软约束权重
```

**作用**：
- 软约束允许临时违反输出约束
- 违反时在代价函数中增加惩罚项：`penalty = weight * |violation|`
- 权重 1e4 意味着违反代价很高，但不会导致问题不可行

---

### 3.3 基准模型选择

**选择策略**：使用网格中心点作为基准模型。

**执行代码**：
```matlab
i_center = ceil(Nv / 2);
j_center = ceil(Nw / 2);
k_center = ceil(Nt / 2);

A0 = squeeze(db.A(i_center, j_center, k_center, :, :));
B0 = squeeze(db.B(i_center, j_center, k_center, :, :));
C0 = squeeze(db.C(i_center, j_center, k_center, :, :));
D0 = squeeze(db.D(i_center, j_center, k_center, :, :));
E0 = squeeze(db.E(i_center, j_center, k_center, :, :));
```

**示例**（3×3×3网格）：
- 选择索引 `[2, 2, 2]`，对应 `ρ = [1.0 m/s, 0.0 rad/s, 0.0 rad]`
- 即：中速直行、平地

**原因**：
- 中心点通常代表最常见的工况
- 保证基准模型稳定（极端工况点可能不稳定）

---

### 3.4 创建 MPC 对象

#### 扩展输入矩阵（添加MD通道占位）

```matlab
if has_md
    B_aug = [B0, zeros(nx, 1)];  % [4×3]，第3列为MD占位
    D_aug = [D0, zeros(ny, 1)];  % [4×3]
else
    B_aug = B0;
    D_aug = D0;
end

plant = ss(A0, B_aug, C0, D_aug, Ts);
```

**关键点**：
- MPC 对象创建时需要声明 **输入通道数**
- 第3列初始为零（名义模型中MD无影响）
- **在线更新时**，第3列将被 `E(ρ)` 替换

#### 设置输入分组

```matlab
plant = setmpcsignals(plant, 'MV', [1 2], 'MD', 3);
```

**作用**：
- 通道1-2：操纵变量（Manipulated Variables，MV）
  - `F_cmd`（驱动力）
  - `omega_cmd`（角速度指令）
- 通道3：测量扰动（Measured Disturbance，MD）
  - `theta`（坡度角，由GRU估计）

#### 创建 MPC 对象

```matlab
mpcobj = mpc(plant, Ts, opts.Np, opts.Nc);
```

**配置权重**：
```matlab
mpcobj.Weights.OutputVariables = opts.Q;
mpcobj.Weights.ManipulatedVariables = opts.R;
mpcobj.Weights.ManipulatedVariablesRate = opts.dR;
```

**配置约束**：
```matlab
% 输入幅值约束（仅MV）
for i = 1:nu  % nu=2
    mpcobj.MV(i).Min = opts.umin(i);
    mpcobj.MV(i).Max = opts.umax(i);
    mpcobj.MV(i).RateMin = opts.dumin(i);
    mpcobj.MV(i).RateMax = opts.dumax(i);
end

% 输出软约束（e_y, e_psi）
mpcobj.OV(1).Min = opts.ymin(1);
mpcobj.OV(1).Max = opts.ymax(1);
mpcobj.OV(1).MinECR = opts.soft_weight_pos;
mpcobj.OV(1).MaxECR = opts.soft_weight_pos;

mpcobj.OV(2).Min = opts.ymin(2);
mpcobj.OV(2).Max = opts.ymax(2);
mpcobj.OV(2).MinECR = opts.soft_weight_yaw;
mpcobj.OV(2).MaxECR = opts.soft_weight_yaw;

% e_v, e_omega 不约束
mpcobj.OV(3).Min = -Inf;
mpcobj.OV(3).Max = Inf;
mpcobj.OV(4).Min = -Inf;
mpcobj.OV(4).Max = Inf;
```

---

### 3.5 构建权重/约束映射表 `ctrl.maps`

**目的**：为在线参数插值提供配置。

#### 调度变量范围
```matlab
maps.rho_min = [db.grid.V(1); db.grid.W(1); db.grid.T(1)];
maps.rho_max = [db.grid.V(end); db.grid.W(end); db.grid.T(end)];
```

#### 权重插值范围
```matlab
maps.Q_range = [opts.Q * 0.5; opts.Q * 1.5];  % [2×4]
maps.R_range = [opts.R * 0.5; opts.R * 1.5];  % [2×2]
maps.dR_range = [opts.dR * 0.5; opts.dR * 1.5];  % [2×2]
```

**说明**：
- 初始范围为基准权重的 ±50%
- **若 PreLoadFcn 载入了 maps_best**，将覆盖此范围

#### 形状参数（默认：线性插值）
```matlab
maps.alpha_Q = zeros(1,4);    % [0,0,0,0]
maps.beta_Q  = ones(1,4);     % [1,1,1,1]
maps.alpha_R = zeros(1,2);
maps.beta_R  = ones(1,2);
maps.alpha_dR = zeros(1,2);
maps.beta_dR  = ones(1,2);
```

**说明**：
- `alpha=0, beta=1` 表示在 `[0,1]` 区间内线性插值
- 可通过贝叶斯优化调整 `alpha/beta` 实现非线性形状

#### 约束缩放参数
```matlab
maps.scale_umin_lo = ones(1,2);
maps.scale_umin_hi = ones(1,2);
maps.scale_umax_lo = ones(1,2);
maps.scale_umax_hi = ones(1,2);
```

**说明**：
- 初始为1（不缩放）
- 可根据 `|ω|` 动态调整（例如转弯时放宽力约束）

#### 场景自适应权重调度参数（方案B，新增）
```matlab
maps.omega_threshold = 0.15;    % 角速度阈值 [rad/s]
maps.q_y_gain_max = 1.8;        % 转弯时 q_y 最大增益
maps.transition_width = 0.05;   % 过渡带宽度 [rad/s]
```

**作用**（在 `mpc_update_from_rho.m` 中实现）：
- 当 `|ω| > 0.15` rad/s 时，自动提高 `q_y`（横向跟踪权重）
- 最大增益 1.8 倍（转弯时更关注横向精度）
- 过渡带宽度 0.05 rad/s（平滑切换，避免抖动）

#### 输出约束上限
```matlab
maps.ey_max = abs(opts.ymax(1));      % 1.0 m
maps.epsi_max = abs(opts.ymax(2));    % 0.5 rad
maps.ev_max = abs(opts.ymax(3));      % 0.5 m/s
maps.eomega_max = abs(opts.ymax(4));  % 0.3 rad/s
```

#### 权重插值开关
```matlab
maps.enable_weight_interp = true;  % 启用在线权重插值
```

**注意**：
- 权重插值需要 Simulink 中**显式使用**（如外部权重端口）
- 或在脚本仿真中通过 `mpcobj.Weights.*` 手动应用

---

### 3.6 元数据

```matlab
ctrl.meta.version = 'V1.2';
ctrl.meta.generated_time = datestr(now, 'yyyy-mm-dd HH:MM:SS');
ctrl.meta.base_workpoint = [v_center, omega_center, theta_center];
ctrl.meta.Ts = Ts;
ctrl.meta.Np = opts.Np;
ctrl.meta.Nc = opts.Nc;
ctrl.meta.control_horizon_sec = opts.Nc * Ts;
ctrl.meta.prediction_horizon_sec = opts.Np * Ts;
ctrl.meta.has_md = true;
ctrl.meta.mv_signals = 'F_cmd[N], omega_cmd[rad/s]';
ctrl.meta.md_signals = 'theta[rad]';
```

---

## 四、在线参数更新：`mpc_update_from_rho.m`

### 4.1 函数签名

```matlab
function upd = mpc_update_from_rho(rho, db, maps)
```

**输入**：
- `rho`：当前调度变量 `[v; omega; theta]` (3×1)
  - `omega` 保留符号（正=左转，负=右转）
- `db`：LPV数据库（`db_rt`）
- `maps`：权重/约束映射表（`ctrl.maps`）

**输出**：
- `upd`：更新结构体
  - **模型矩阵**：`A`, `B`, `C`, `D`, `E`, `Bv`, `Dv`
  - **权重**：`Q`, `R`, `dR`
  - **约束**：`umin`, `umax`
  - **调试信息**：`rho_n`, `indices`, `weights`

---

### 4.2 归一化与边界饱和

```matlab
v = max(min(rho(1), V_grid(end)), V_grid(1));
omega = max(min(rho(2), W_grid(end)), W_grid(1));
theta = max(min(rho(3), T_grid(end)), T_grid(1));

if Nv > 1
    v_n = (v - V_grid(1)) / (V_grid(end) - V_grid(1));
else
    v_n = 0;
end
% 同理计算 w_n, t_n
rho_n = [v_n; w_n; t_n];  % ∈ [0,1]^3
```

**作用**：
- 饱和到网格范围（避免外推）
- 归一化到 `[0,1]`（便于插值计算）

---

### 4.3 定位网格单元（三线性插值）

**目标**：找到包围当前 `ρ` 的8个顶点。

**执行代码**（支持非均匀网格）：
```matlab
i_low = find(V_grid <= v, 1, 'last');
i_low = max(1, min(Nv-1, i_low));
i_high = min(i_low + 1, Nv);
% 同理定位 j_low, j_high, k_low, k_high
```

**计算局部坐标** `ξ, η, ζ ∈ [0,1]`：
```matlab
if V_grid(i_high) > V_grid(i_low)
    xi = (v - V_grid(i_low)) / (V_grid(i_high) - V_grid(i_low));
else
    xi = 0;
end
% 同理计算 eta, zeta
```

**三线性插值权重**（8个顶点）：
```matlab
w(1) = (1-xi) * (1-eta) * (1-zeta);  % (i_low,  j_low,  k_low)
w(2) = xi * (1-eta) * (1-zeta);      % (i_high, j_low,  k_low)
w(3) = (1-xi) * eta * (1-zeta);      % (i_low,  j_high, k_low)
w(4) = xi * eta * (1-zeta);          % (i_high, j_high, k_low)
w(5) = (1-xi) * (1-eta) * zeta;      % (i_low,  j_low,  k_high)
w(6) = xi * (1-eta) * zeta;          % (i_high, j_low,  k_high)
w(7) = (1-xi) * eta * zeta;          % (i_low,  j_high, k_high)
w(8) = xi * eta * zeta;              % (i_high, j_high, k_high)

w = w / sum(w);  % 归一化（数值稳定性）
```

---

### 4.4 插值模型矩阵

```matlab
A_interp = zeros(4, 4);
B_interp = zeros(4, 2);
C_interp = zeros(4, 4);
D_interp = zeros(4, 2);
E_interp = zeros(4, 1);

for p = 1:8
    i = indices(p, 1);
    j = indices(p, 2);
    k = indices(p, 3);
    
    A_interp = A_interp + w(p) * squeeze(db.A(i, j, k, :, :));
    B_interp = B_interp + w(p) * squeeze(db.B(i, j, k, :, :));
    C_interp = C_interp + w(p) * squeeze(db.C(i, j, k, :, :));
    D_interp = D_interp + w(p) * squeeze(db.D(i, j, k, :, :));
    E_interp = E_interp + w(p) * squeeze(db.E(i, j, k, :, :));
end
```

---

### 4.5 插值权重（按维度映射）

#### 调度因子计算

**策略**：根据 `ρ_n` 的各分量，为每个权重元素计算独立的调度因子。

**默认线性组合**（可通过 `maps.factor_*` 自定义）：
```matlab
fy   = 0.3*rho_n(1) + 0.2*rho_n(2) + 0.5*rho_n(3);  % 影响 q_y
fpsi = 0.1*rho_n(1) + 0.7*rho_n(2) + 0.2*rho_n(3);  % 影响 q_psi
fv   = 0.8*rho_n(1) + 0.1*rho_n(2) + 0.1*rho_n(3);  % 影响 q_v
fomega = 0.2*rho_n(1) + 0.6*rho_n(2) + 0.2*rho_n(3);  % 影响 q_omega

fR_F   = 0.6*rho_n(1) + 0.3*rho_n(2) + 0.1*rho_n(3);  % 影响 r_F
fR_w   = 0.2*rho_n(1) + 0.7*rho_n(2) + 0.1*rho_n(3);  % 影响 r_omega

fdR_F  = 0.5*rho_n(1) + 0.3*rho_n(2) + 0.2*rho_n(3);  % 影响 r_dF
fdR_w  = 0.2*rho_n(1) + 0.6*rho_n(2) + 0.2*rho_n(3);  % 影响 r_domega
```

**解释**：
- `q_y`：坡度影响最大（系数0.5），速度次之（0.3）
- `q_psi`：角速度影响最大（系数0.7），转弯时航向更重要
- `q_v`：速度影响最大（系数0.8）
- `r_omega`：角速度影响最大（系数0.7）

#### 形状映射（可选）

若设置了 `maps.alpha_*` 和 `maps.beta_*`：
```matlab
shape_map = @(x, a, b) max(0, min(1, (x - a) ./ max(b - a, eps)));

fy     = shape_map(fy,     maps.alpha_Q(1),  maps.beta_Q(1));
fpsi   = shape_map(fpsi,   maps.alpha_Q(2),  maps.beta_Q(2));
% 同理处理 fv, fomega, fR_F, fR_w, fdR_F, fdR_w
```

**作用**：在 `[alpha, beta]` 区间内线性过渡，区间外夹紧为0或1。

#### 权重插值

```matlab
if enable_weight_interp && isfield(maps, 'Q_range')
    Q_min = maps.Q_range(1, :);
    Q_max = maps.Q_range(2, :);
    Q_interp = Q_min + [fy; fpsi; fv; fomega]' .* (Q_max - Q_min);
end

% 同理插值 R_interp, dR_interp
```

**示例**：
- `Q_range = [15, 20, 3.5, 1.2; 22, 28, 5.5, 2.5]`
- 若 `fy = 0.6`，则 `q_y = 15 + 0.6*(22-15) = 19.2`

---

### 4.6 场景自适应权重调度（方案B）

**目的**：转弯时自动提高 `q_y`（横向跟踪权重）。

**执行代码**：
```matlab
omega_thresh = maps.omega_threshold;  % 0.15 rad/s
gain_max = maps.q_y_gain_max;        % 1.8
trans_width = maps.transition_width;  % 0.05 rad/s

omega_abs = abs(omega);

if omega_abs <= (omega_thresh - trans_width)
    q_y_gain = 1.0;  % 直线区域
elseif omega_abs >= (omega_thresh + trans_width)
    q_y_gain = gain_max;  % 转弯区域
else
    % 过渡区域：三次 Hermite 平滑插值
    s = (omega_abs - (omega_thresh - trans_width)) / (2 * trans_width);
    q_y_gain = 1.0 + (gain_max - 1.0) * (3*s^2 - 2*s^3);
end

Q_interp(1) = Q_interp(1) * q_y_gain;  % 应用增益到 q_y
```

**效果**：
- 直线（`|ω|<0.10`）：`q_y` 保持基准值
- 急转弯（`|ω|>0.20`）：`q_y` 放大 1.8 倍
- 中间：平滑过渡

---

### 4.7 约束插值

#### 基于角速度的线性插值
```matlab
omega_n = rho_n(2);  % 归一化角速度
umin_interp = (1-omega_n) * maps.umin_range(1,:)' + omega_n * maps.umin_range(2,:)';
umax_interp = (1-omega_n) * maps.umax_range(1,:)' + omega_n * maps.umax_range(2,:)';
```

#### 叠加缩放因子
```matlab
scale_umin = (1-omega_n) * maps.scale_umin_lo + omega_n * maps.scale_umin_hi;
scale_umax = (1-omega_n) * maps.scale_umax_lo + omega_n * maps.scale_umax_hi;

umin_interp = umin_interp .* scale_umin;
umax_interp = umax_interp .* scale_umax;
```

**示例**：
- 若 `scale_umax_hi = [1.2, 1.0]`
- 转弯时（`omega_n=1`）：`F_max` 放大 1.2 倍，允许更大驱动力

---

### 4.8 组装输出结构体

```matlab
upd.A = A_interp;   % [4×4]
upd.B = B_interp;   % [4×2] MV部分
upd.C = C_interp;   % [4×4]
upd.D = D_interp;   % [4×2]
upd.E = E_interp;   % [4×1] MD部分（θ扰动）
upd.Bv = E_interp;  % [4×1] Adaptive MPC专用名称
upd.Dv = zeros(ny, nd);  % [4×1] MD直通矩阵（通常为零）

upd.Q = Q_interp;
upd.R = R_interp;
upd.dR = dR_interp;
upd.umin = umin_interp;
upd.umax = umax_interp;

upd.rho = [v; omega; theta];  % 饱和后的实际 ρ
upd.rho_n = rho_n;
upd.indices = indices;  % 8×3 顶点索引
upd.weights = w;        % 8×1 插值权重
```

---

## 五、仿真运行时的参数更新流程

### 5.1 Simulink 块接线

```
┌─────────────────────────────────────────────────────────────┐
│                    LPVMPC_AGV_simulink.slx                  │
└─────────────────────────────────────────────────────────────┘

  [Reference]                         [theta_ground]
      │                                      │
      │                                      ▼
      ▼                              ┌──────────────┐
┌─────────────┐                      │     Plant     │
│Path Error   │◀────────────────────┤  (S-Function) │
│Calculator   │                      └──────┬────────┘
└──────┬──────┘                             │
       │                                    │ y_raw [31×1]
       │ [e_y, e_psi,                       │
       │  e_v, e_omega]                     ▼
       │                              ┌──────────────┐
       │                              │     GRU      │
       │                              │State Classify│
       │                              └──────┬───────┘
       │                                     │ theta_hat
       │                                     │
       │         ┌───────────────────────────┘
       │         │
       ▼         ▼
┌─────────────────────────────────┐
│       Adaptive MPC              │
│  ┌────────────────────────────┐ │
│  │ 自定义更新函数              │ │
│  │ mpc_update_from_rho        │ │
│  │   输入: rho_f=[v;ω;θ_hat]  │ │
│  │   输出: A,B,C,D,Bv         │ │
│  └────────────────────────────┘ │
│                                 │
│  输入端口:                       │
│  - mo (Measured Outputs): y    │
│  - ref (Reference): [0;0;0;0]  │
│  - md (Meas. Disturbance): θ   │
│                                 │
│  输出: u = [F_cmd; omega_cmd]   │
└─────────────┬───────────────────┘
              │
              ▼
          [Plant]
```

---

### 5.2 每个仿真步的执行流程

#### Step 1：Plant 输出
```matlab
y_raw = output_eq_ref(x, u, theta_ground, params);  % [31×1]
```

#### Step 2：GRU 推理
```matlab
[state_gru, out_gru] = GRU_state_classifier('update', state_gru, y_raw);
theta_hat = out_gru.theta_hat;  % 估计的坡度角
```

#### Step 3：构造 ρ（RhoFilter 块）
```matlab
v = y_raw(4);
omega = y_raw(5);
rho_raw = [v; omega; theta_hat];

% 一阶低通滤波（τ=0.4s）
alpha = Ts / (tau + Ts);
rho_f = alpha * rho_raw + (1 - alpha) * rho_f_prev;
```

#### Step 4：MPC 自定义更新函数
```matlab
upd = mpc_update_from_rho(rho_f, db_rt, ctrl.maps);

% 构造 plant_model（更新后的模型）
plant_model.A = upd.A;
plant_model.B = [upd.B, upd.E];  % [4×3]（含MD列）
plant_model.C = upd.C;
plant_model.D = [upd.D, zeros(4,1)];  % [4×3]
plant_model.Ts = db_rt.Ts;

% 可选：更新权重（需外部端口或回调）
% mpcobj.Weights.OutputVariables = upd.Q;
% mpcobj.Weights.ManipulatedVariables = upd.R;
% mpcobj.Weights.ManipulatedVariablesRate = upd.dR;
```

#### Step 5：MPC 求解
```matlab
y_meas = [e_y; e_psi; e_v; e_omega];  % 测量输出
r_ref = [0; 0; 0; 0];                 % 误差参考（趋零控制）
md = theta_hat;                       % 测量扰动

[u_mpc, Info, xmpc_next] = mpcmoveAdaptive(mpcobj, xmpc, plant_model, Nominal, y_meas, r_ref, md);
```

**Nominal 结构体**：
```matlab
Nominal.U = zeros(3,1);  % [2 MV + 1 MD]
Nominal.X = zeros(4,1);
Nominal.Y = zeros(4,1);
Nominal.DX = zeros(4,1);
```

#### Step 6：Plant 更新
```matlab
u_plant = [u_mpc(1); u_mpc(2); theta_ground];  % [F_cmd; omega_cmd; theta_ground]
x_next = state_eq_ref(x, u_plant, theta_ground, params);
```

---

## 六、参数传递总结表

| 参数类型 | 来源 | 传递路径 | 最终应用位置 | 更新频率 |
|---------|------|---------|-------------|---------|
| **基础参数** | `parameters.m` | PreLoadFcn → Base WS → Plant | Plant S-Function | 初始化一次 |
| **LPV数据库** | `lin_agv_db.mat` | PreLoadFcn → `db_rt` → MPC更新函数 | `mpc_update_from_rho` | 初始化一次 |
| **优化权重范围** | `maps_best.mat` | PreLoadFcn → `ctrl.maps` → 更新函数 | `mpc_update_from_rho` | 初始化一次 |
| **MPC对象** | `mpc_setup_single_interp` | PreLoadFcn → `ctrl.mpcobj` → Adaptive MPC块 | Adaptive MPC Controller | 初始化一次 |
| **权重映射表** | `ctrl.maps` | 控制器创建 → 更新函数 | `mpc_update_from_rho` | 初始化一次 |
| **模型矩阵** | `db_rt.A/B/C/D/E` | 在线插值 → `plant_model` | Adaptive MPC求解器 | 每个仿真步 |
| **权重Q/R/dR** | `ctrl.maps.*_range` | 在线插值 → `upd.Q/R/dR` | （可选）MPC权重端口 | 每个仿真步 |
| **约束umin/umax** | `ctrl.maps.scale_*` | 在线插值 → `upd.umin/umax` | （可选）MPC约束端口 | 每个仿真步 |
| **坡度角估计** | GRU推理 | `y_raw` → GRU → `theta_hat` | MPC的MD端口 + `ρ` | 每个仿真步 |
| **调度变量** | `[v,ω,θ_hat]` | Plant输出 + GRU → RhoFilter → 更新函数 | `mpc_update_from_rho` | 每个仿真步 |

---

## 七、关键设计决策与理由

### 7.1 为什么使用"范围插值"而非"固定权重"？

**问题**：不同工况（直行/转弯/上坡）对控制性能要求不同。

**解决方案**：
- 直行：低 `q_y`（横向误差容忍度高），高 `q_v`（速度精度优先）
- 转弯：高 `q_y`、`q_psi`（横向+航向精度优先）
- 上坡：高 `q_v`（维持速度），放宽 `umax`（允许大驱动力）

**实现**：
- 通过 `Q_range`、`R_range` 定义权重上下界
- 根据 `ρ_n` 插值（`fy`、`fpsi`等调度因子）
- 贝叶斯优化自动寻找最优范围

---

### 7.2 为什么坡度角 `θ` 进入 MD 通道而非 MV？

**MD（Measured Disturbance）vs MV（Manipulated Variable）**：
- **MV**：可控输入（如 `F_cmd`、`omega_cmd`）
- **MD**：可测量但不可控的扰动（如坡度角、风速）

**MPC 处理 MD 的优势**：
- **前馈补偿**：提前预测未来 `Np` 步的 `θ` 影响，预先调整控制量
- **零滞后**：无需等到误差出现才反应
- **鲁棒性**：即使 `θ` 估计有偏差，反馈控制可补偿

**实现**：
- `upd.Bv = E(ρ)`：扰动影响矩阵（`θ` 如何影响状态）
- MPC 在优化时考虑：`x_{k+1} = A x_k + B u_k + Bv θ_k`

---

### 7.3 为什么权重需要"按维度映射"而非统一缩放？

**问题**：
- `q_y`（横向误差）与 `q_v`（速度误差）对不同工况的敏感性不同
- 统一缩放（如 `Q *= 1.5`）无法体现差异化需求

**解决方案**：
- 每个权重元素独立调度（`fy`, `fpsi`, `fv`, `fomega`）
- 形状参数（`alpha/beta`）控制非线性过渡
- 因子权重（`factor_y`, `factor_psi`等）可自定义 `ρ` 各分量的影响比例

**示例**：
- 转弯时：`fpsi = 0.1*v + 0.7*ω + 0.2*θ`
  - 主要由角速度 `ω` 主导（系数0.7）
  - 航向跟踪在转弯时更重要
- 上坡时：`fv = 0.8*v + 0.1*ω + 0.1*θ`
  - 主要由速度 `v` 主导（系数0.8）
  - 维持速度在爬坡时最关键

---

### 7.4 为什么需要"滤波 ρ"？

**问题**：
- 原始 `ρ=[v, ω, θ_hat]` 可能包含测量噪声
- 快速跳变会导致模型突变，引起控制震荡

**解决方案**：
- 一阶低通滤波（τ=0.4s）
- 平滑 `ρ` 的变化

**实现**：
```matlab
alpha = Ts / (tau + Ts);
rho_f = alpha * rho_raw + (1 - alpha) * rho_f_prev;
```

**效果**：
- 避免模型参数抖动
- 保持控制连续性

---

## 八、故障排查指南

### 问题 1：MPC 求解失败（Info.QPCode = 'infeasible'）

**可能原因**：
1. 约束过严（输出约束 `ymin/ymax` 不可行）
2. 模型矩阵插值错误（`A` 不稳定）
3. 权重设置不当（`Q` 过大导致问题刚性）

**排查步骤**：
1. 检查 `upd.A` 的特征值：`max(abs(eig(upd.A)))`（应 <1）
2. 临时放宽输出约束：`ymin=[-Inf;...], ymax=[Inf;...]`
3. 检查 `upd.Q/R/dR` 是否异常（NaN、负值、过大）
4. 查看 `Info.Iterations` 和 `Info.Cost`

---

### 问题 2：权重未生效（控制性能与预期不符）

**可能原因**：
- Simulink Adaptive MPC 块未连接外部权重端口
- `maps.enable_weight_interp = false`（权重插值被禁用）

**解决方案**：
1. 确认 `ctrl.maps.enable_weight_interp = true`
2. 在 Adaptive MPC 块中启用"External Weights"端口
3. 手动验证：脚本仿真中打印 `upd.Q`，观察是否随 `ρ` 变化

---

### 问题 3：坡度补偿无效（上坡掉速）

**可能原因**：
1. GRU估计 `θ_hat` 不准确
2. `upd.E` 矩阵错误（扰动影响矩阵）
3. MD 通道未正确连接

**排查步骤**：
1. 对比 `theta_hat` 与 `theta_ground`：`mean(abs(theta_hat - theta_ground))`（应 <2°）
2. 检查 `upd.E` 第3行（纵向动力学）是否非零
3. 确认 Adaptive MPC 块的 `md` 端口已连接 `theta_hat`
4. 验证前馈力计算：`F_eq = m*g*sin(theta) + c_r*m*g*cos(theta) + F_aero`

---

### 问题 4：转弯时横向误差过大

**可能原因**：
1. `q_y` 权重过低
2. 场景自适应未启用（方案B）
3. `omega_threshold` 设置过高（未触发增益）

**解决方案**：
1. 提高 `maps.Q_range` 第1列（`q_y`）
2. 确认 `maps.omega_threshold = 0.15`（合理阈值）
3. 检查 `maps.q_y_gain_max = 1.8`（增益足够大）
4. 打印 `q_y_gain`，观察转弯时是否提高
5. 调整 `maps.transition_width`（过渡带宽度）

---

## 九、扩展阅读

### 相关文档
- `func.md`：功能模块导航（脚本、接口、依赖）
- `README_LPVMPC_Usage.md`：LPV-MPC使用指南
- `README_GRU_Integration.md`：GRU工况识别集成说明
- `MPC权重确定机制说明.md`：权重设计详细说明
- `change.md`：版本更新记录

### 关键脚本
- `parameters.m`：集中参数定义
- `lin_agv_grid.m`：LPV数据库生成
- `mpc_setup_single_interp.m`：MPC控制器创建
- `mpc_update_from_rho.m`：在线参数更新
- `Cost_Function.m`：MPC闭环评估
- `Bayesian_Optimization.m`：权重优化

---

## 十、总结

### 参数加载链路精炼版

```
parameters.m → params
    ↓
lin_agv_db.mat → db_rt (A/B/C/D/E网格)
    ↓
maps_best.mat → maps_best (Q/R/dR范围、约束缩放)
    ↓
mpc_setup_single_interp → ctrl
    ├─ ctrl.mpcobj (MPC对象，基准模型+权重+约束)
    └─ ctrl.maps (权重/约束映射表，可被maps_best覆盖)
        ↓
每个仿真步：
    Plant → y_raw → GRU → theta_hat
                      ↓
    [v, ω, theta_hat] → RhoFilter → rho_f
                                      ↓
    mpc_update_from_rho(rho_f, db_rt, ctrl.maps)
        ├─ 三线性插值 A/B/C/D/E
        ├─ 按维度插值 Q/R/dR
        ├─ 场景自适应增益（转弯时提高q_y）
        └─ 约束插值 umin/umax
            ↓
    Adaptive MPC 求解（使用更新后的模型+权重+约束）
        ↓
    控制输出 [F_cmd, omega_cmd] → Plant
```

### 核心理念

1. **分层设计**：参数→数据库→控制器→在线更新
2. **智能调度**：根据工况（`ρ`）自适应调整模型和参数
3. **贝叶斯优化**：自动寻找最优权重范围
4. **场景自适应**：转弯时自动提高横向跟踪精度
5. **前馈补偿**：坡度角进入MD通道，提前预测扰动影响

---

**版本**：V1.0（2025-11-06）  
**作者**：Auto-generated  
**维护**：见 `change.md`

