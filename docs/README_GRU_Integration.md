# GRU模型集成到LPVMPC_AGV_simulink.slx指南

## 概述

本文档详细介绍如何将GRU工况识别模型集成到LPVMPC_AGV_simulink.slx中，实现在线坡度角估计（`theta_hat`）并注入MPC的MD（Measured Disturbance）通道。

## 前提条件

确保以下文件存在于项目根目录：
- ✅ `GRU_model.mat` - 训练好的GRU模型
- ✅ `GRU_scaler.mat` - 归一化参数
- ✅ `GRU_state_classifier.m` - 在线推理封装
- ✅ `GRU_infer.m` - GRU推理接口
- ✅ `LPVMPC_AGV_simulink.slx` - 现有Simulink模型
- ✅ `parameters.m` - 系统参数

---

## 集成步骤

### 步骤1：打开Simulink模型

```matlab
% 在MATLAB命令窗口执行
open_system('LPVMPC_AGV_simulink.slx')
```

---

### 步骤2：添加GRU工况识别子系统

#### 2.1 创建MATLAB Function块

1. 在Simulink库浏览器中找到 **User-Defined Functions → MATLAB Function**
2. 拖拽到模型的合适位置（建议放在Plant模块附近）
3. 双击该块，重命名为 `GRU_State_Classifier`

#### 2.2 配置MATLAB Function代码

双击 `GRU_State_Classifier` 块，在编辑器中输入以下代码：

```matlab
function [theta_hat, label_main, label_turn, conf_main] = GRU_State_Classifier(y_raw, reset)
%#codegen

% ========== 1. 声明所有 extrinsic 函数（必须在顶层，任何调用之前）==========
coder.extrinsic('evalin');
coder.extrinsic('assignin');
coder.extrinsic('GRU_state_classifier');

% ========== 2. 持久变量 ==========
persistent state is_initialized

% ========== 3. 显式指定输出类型和大小（避免Simulink推断错误）==========
theta_hat = 0.0;      % [1×1] double
label_main = 1.0;     % [1×1] double
label_turn = 0.0;     % [1×1] double
conf_main = 1.0;      % [1×1] double

% ========== 4. 初始化（首次调用或reset=1）==========
if isempty(is_initialized)
    is_initialized = false;
end

if ~is_initialized || reset == 1
    % 从Base Workspace读取预加载的数据（在PreLoadFcn中加载）
    model = evalin('base', 'gru_model');
    params = evalin('base', 'params');
    
    % 初始化分类器状态
    state = GRU_state_classifier('init', params, model);
    
    is_initialized = true;
    
    % 初始化阶段返回默认值
    return;
end

% ========== 5. 安全检查：确保state已定义（避免Coder错误）==========
if isempty(state)
    % 如果state未定义（异常情况），返回默认值
    return;
end

% ========== 6. 在线更新（每个采样周期调用）==========
[state, out] = GRU_state_classifier('update', state, y_raw);

% ========== 7. 提取输出（使用evalin间接访问，无需外部文件）==========
% 方法：将out临时保存到base workspace，然后用evalin提取字段
assignin('base', 'gru_out_temp', out);
theta_hat = evalin('base', 'double(gru_out_temp.theta_hat)');
label_main = evalin('base', 'double(gru_out_temp.label_main)');
label_turn = evalin('base', 'double(gru_out_temp.label_turn)');
conf_main = evalin('base', 'double(gru_out_temp.conf_main(1))');

end
```

**方案2的优点**：
- ✅ 不需要 `extract_gru_output.m` 外部文件
- ✅ 所有代码在一个函数内
- ✅ 同样解决了 mxArray 访问问题

**方案2的缺点**：
- ⚠️ 每步调用 4 次 `evalin`（稍慢，但可接受）
- ⚠️ 临时变量 `gru_out_temp` 占用 base workspace（很小）

**重要提示**：上述代码包含 `coder.extrinsic` 声明，这意味着：
- ✅ **仿真模式**：完全支持，调用MATLAB解释器执行
- ⚠️ **代码生成模式**：需要特殊处理（见下文"代码生成优化"）

#### 2.3 配置输入输出端口

在MATLAB Function编辑器的 **Edit Data** 按钮（或Ctrl+Shift+M）配置端口：

**输入端口**：
| 名称 | 类型 | 维度 | 说明 |
|------|------|------|------|
| `y_raw` | double | [31×1] | Plant输出（来自output_eq） |
| `reset` | double | [1×1] | 重置信号（0=正常, 1=重置） |

**输出端口**：
| 名称 | 类型 | 维度 | 说明 |
|------|------|------|------|
| `theta_hat` | double | [1×1] | 坡度角估计 [rad] |
| `label_main` | double | [1×1] | 主分类 {1,2,3,4} |
| `label_turn` | double | [1×1] | 转弯状态 {-1,0,+1} |
| `conf_main` | double | [1×1] | 主分类置信度 [0,1] |

---

### 步骤3：连接信号线

#### 3.1 连接GRU输入（Plant输出 → GRU）

找到现有的 **Plant模块**（AGV_Model S-Function），它输出 `y_raw [31×1]`：

```
Plant (AGV_Model) 输出端口
   ↓
   ├─→ GRU_State_Classifier 的 y_raw 输入
   └─→ （现有连接，保持不变）
```

操作步骤：
1. 使用 **Mux** 或 **Bus Selector** 提取Plant的完整31维输出
2. 连接到 `GRU_State_Classifier` 的 `y_raw` 端口

#### 3.2 添加Reset信号（可选）

如果需要在仿真开始时重置GRU状态：
```
Constant (值=0)
   ↓
GRU_State_Classifier 的 reset 输入
```

或者使用 **Compare To Zero** 块检测仿真时间：
```
Clock → Compare (t==0) → GRU reset
```

#### 3.3 连接GRU输出到MPC的MD通道

找到 **Adaptive MPC Controller** 块或 **MPC控制器**模块：

```
GRU_State_Classifier 的 theta_hat 输出
   ↓
Adaptive MPC Controller 的 md (Measured Disturbance) 输入
```

**关键配置**：
- MPC块的 **Measured Disturbances** 端口应启用
- 输入维度：`[1×1]`（仅theta）
- 单位：rad（与LPV数据库的T_grid一致）

#### 3.4 连接诊断输出（可选）

将 `label_main`, `label_turn`, `conf_main` 连接到 **Scope** 或 **To Workspace** 块以监控工况识别：

```
label_main → Scope (显示 flat/slip/stall/slope)
label_turn → Scope (显示 right/straight/left)
conf_main  → Scope (显示置信度)
```

---

### 步骤4：配置RhoFilter（调度变量滤波）

GRU的 `theta_hat` 需要与MPC的调度变量 `rho=[v; omega; theta]` 一起滤波。

#### 4.1 修改现有RhoFilter MATLAB Function

如果模型中已有 `RhoFilter` 块，修改其代码：

```matlab
function rho_f = RhoFilter(v, omega, theta_hat, Ts, tau)
% 一阶低通滤波：rho_f = [v_f; omega_f; theta_hat_f]
% tau: 滤波时间常数 [s]（默认0.4s）

persistent rho_prev

if isempty(rho_prev)
    rho_prev = [v; omega; theta_hat];  % 初始化
end

alpha = Ts / (tau + Ts);
rho_f = alpha * [v; omega; theta_hat] + (1 - alpha) * rho_prev;
rho_prev = rho_f;

end
```

#### 4.2 连接信号

```
v (速度)     ────┐
omega (角速度) ──┤
theta_hat ───────┼─→ RhoFilter ─→ rho_f [3×1] ─→ MPC Scheduling 端口
Ts (常数) ───────┤
tau (常数) ──────┘
```

**参数值**：
- `Ts = 0.01` （来自parameters.m）
- `tau = 0.4` （推荐值，可在 0.3–0.5 s 范围调整）

---

### 步骤5：配置Adaptive MPC块

#### 5.1 找到Adaptive MPC Controller块

在模型中找到 **Adaptive MPC Controller** 块，双击打开配置面板。

#### 5.2 配置端口

| 端口名称 | 说明 | 连接 |
|---------|------|------|
| **mo** (Measured Outputs) | 测量输出 [4×1] | `[e_y; e_psi; e_v; e_omega]` |
| **ref** (Reference) | 参考轨迹 [4×1] | `[0; 0; 0; 0]`（误差趋零）|
| **md** (Measured Disturbance) | 测量扰动 [1×1] | `theta_hat`（来自GRU）|
| **mv** (Manipulated Variables) | 控制输出 [2×1] | `[F_cmd; omega_cmd]` |

#### 5.3 启用自定义模型更新函数

在 **Adaptive MPC** 块参数对话框：
1. 勾选 **Use custom state estimation function**（如果需要）
2. 勾选 **Use custom update function**
3. 设置 **Scheduling signals** 为 `rho_f`（来自RhoFilter）

#### 5.4 配置自定义更新函数

在块参数中指定更新函数：
```
Function name: mpc_update_from_rho
```

确保Simulink能找到该函数：
```matlab
% 在MATLAB命令窗口检查
which mpc_update_from_rho
% 应返回：E:\Matlab\Simulink\S-Function_14\mpc_update_from_rho.m
```

---

### 步骤6：配置仿真参数

#### 6.1 加载必要数据到Base Workspace ⭐

**重要**：GRU_State_Classifier块需要从Base Workspace读取预加载的数据。

在模型的 **PreLoadFcn** 回调中添加：

```matlab
% 模型初始化脚本（File → Model Properties → Callbacks → PreLoadFcn）

fprintf('正在初始化模型...\n');

% ========== 必须项：GRU依赖 ==========
% 加载系统参数（GRU_State_Classifier会用evalin读取）
params = parameters();
fprintf('  ✓ 加载params\n');

% 加载GRU模型（GRU_State_Classifier会用evalin读取）
if ~exist('gru_model', 'var')
    load('GRU_model.mat', 'model');
    gru_model = model;
    clear model;  % 避免变量名冲突
    fprintf('  ✓ 加载gru_model\n');
end

% ========== 可选项：MPC和参考轨迹 ==========
% 加载LPV数据库
if exist('lin_agv_db.mat', 'file')
    load('lin_agv_db.mat', 'db');
    fprintf('  ✓ 加载db (LPV数据库)\n');
end

% 创建MPC控制器
if exist('db', 'var') && ~exist('ctrl', 'var')
    ctrl = mpc_setup_single_interp(db, struct());
    fprintf('  ✓ 创建ctrl (MPC控制器)\n');
end

% 加载参考轨迹（示例：转弯场景）
if ~exist('ref', 'var')
    ref = gen_agv_ref_path('turn', params);
    fprintf('  ✓ 生成ref (参考轨迹)\n');
end

fprintf('✓ 模型初始化完成\n\n');
```

**配置PreLoadFcn的步骤**：
1. 在Simulink中，点击菜单栏 **File → Model Properties → Callbacks**
2. 在左侧列表选择 **PreLoadFcn**
3. 在右侧编辑器中粘贴上述代码
4. 点击 **OK** 保存

#### 6.2 设置求解器

在模型配置参数（Ctrl+E）中：
- **Solver**: `ode4` (Runge-Kutta) 或 `ode5` (Dormand-Prince)
- **Fixed-step size**: `0.01` (与params.Ts一致)
- **Stop time**: `20` (与参考轨迹时长一致)

---

### 步骤7：测试集成

#### 7.1 编译检查

```matlab
% 在MATLAB命令窗口
open_system('LPVMPC_AGV_simulink.slx')
set_param('LPVMPC_AGV_simulink', 'SimulationCommand', 'update')
```

检查是否有编译错误（红色波浪线）。

#### 7.2 短时仿真测试

```matlab
% 运行2秒仿真测试
set_param('LPVMPC_AGV_simulink', 'StopTime', '2')
sim('LPVMPC_AGV_simulink')

% 检查输出
disp('GRU theta_hat 前10步:')
disp(theta_hat(1:10))  % 假设已连接到To Workspace块
```

#### 7.3 完整场景测试

```matlab
% 加载测试脚本
test_lpvmpc_with_gru_workflow
```

---

## 信号流总览

```
┌─────────────────────────────────────────────────────────────────┐
│  LPVMPC_AGV_simulink.slx 信号流（集成GRU后）                      │
└─────────────────────────────────────────────────────────────────┘

参考轨迹 (From Workspace)
   │
   │  [X_ref, Y_ref, psi_ref, v_ref, omega_ref, theta_ref]
   ↓
┌──────────────┐
│ Path Error   │  计算路径坐标系误差
│ Calculator   │  → [e_y, e_psi, e_v, e_omega]
└──────┬───────┘
       │
       ├─────────────────────────┐
       │                         │
       ↓                         ↓
┌──────────────┐          ┌──────────────┐
│ Adaptive MPC │ ←────────┤ RhoFilter    │
│ Controller   │   rho_f  │ [v,ω,θ_hat]  │
└──────┬───────┘          └──────┬───────┘
       │                         ↑
       │  [F_cmd, omega_cmd]     │ theta_hat
       ↓                         │
┌──────────────┐          ┌──────────────┐
│ Plant        │ ─────────→│ GRU_State    │
│ (S-Function) │  y_raw    │ Classifier   │
└──────┬───────┘  [31×1]  └──────┬───────┘
       │                         │
       ↓                         ↓
    [X,Y,ψ,v,ω,...]      [label_main, label_turn, conf]
       │                         │
       └─────────────┬───────────┘
                     ↓
              Scopes & Logging
```

---

## 故障排查

### 问题0：编译错误 "无法从类型为 mxArray 的变量中提取字段" ⭐⭐

这是MATLAB Coder的核心限制，有两种情况：

#### 情况A：无法访问 `load()` 返回的结构体字段

**错误信息**：
```
无法从类型为 mxArray 的变量中提取字段 model，因为此变量不是结构体。
函数 'GRU_State_Classifier'，行 XX: "model_data"
```

**原因**：`coder.extrinsic('load')` 返回 `mxArray` 类型，无法访问 `.model` 字段

**解决方案**：PreLoadFcn预加载 + evalin读取
```matlab
% PreLoadFcn中：
load('GRU_model.mat', 'model');
gru_model = model;

% MATLAB Function中：
coder.extrinsic('evalin');
model = evalin('base', 'gru_model');  % ✅ 可以访问
```

---

#### 情况B：无法访问 extrinsic 函数返回的结构体字段 ⭐

**错误信息**：
```
无法从类型为 mxArray 的变量中提取字段 theta_hat，因为此变量不是结构体。
函数 'GRU_State_Classifier'，行 XX: "out"
```

**原因**：
- `GRU_state_classifier` 被声明为 `coder.extrinsic`
- 它的返回值 `out` 也是 `mxArray` 类型
- 无法访问 `out.theta_hat` 等字段

**解决方案**（✅ 已在上文代码中修正）：
创建辅助函数 `extract_gru_output.m` 来提取字段：

```matlab
% 1) 创建 extract_gru_output.m（根目录）
function [theta_hat, label_main, label_turn, conf_main] = extract_gru_output(out)
    theta_hat = double(out.theta_hat);
    label_main = double(out.label_main);
    label_turn = double(out.label_turn);
    conf_main = double(out.conf_main(1));
end

% 2) 在MATLAB Function中声明并调用
coder.extrinsic('extract_gru_output');  % 顶层声明

[state, out] = GRU_state_classifier('update', state, y_raw);
[theta_hat, label_main, label_turn, conf_main] = extract_gru_output(out);  % ✅ 可以访问
```

**关键要点**：
- ❌ 不能直接访问 extrinsic 函数返回的结构体字段
- ✅ 创建另一个 extrinsic 辅助函数来提取字段
- ✅ 辅助函数也必须在顶层声明

---

### 问题0.5：编译错误 "持久变量在某些执行路径中未定义" ⭐

**错误信息**：
```
持久变量 state 在某些执行路径中未定义。要进行代码生成，所有变量在使用前都必须完全定义。
函数 'GRU_State_Classifier'，行 35: "state"
```

**原因**：
- MATLAB Coder进行静态分析时，无法保证 `state` 在第35行使用时一定已定义
- 虽然逻辑上首次调用会初始化 `state`，但Coder要求所有代码路径都明确定义变量

**解决方案**（✅ 已在上文代码中修正）：
在使用 `state` 之前添加安全检查：

```matlab
% 初始化后return
if ~is_initialized || reset == 1
    state = GRU_state_classifier('init', params, model);
    is_initialized = true;
    return;
end

% ⭐ 安全检查：确保state已定义
if isempty(state)
    return;  % 异常情况：返回默认值
end

% 现在可以安全使用state
[state, out] = GRU_state_classifier('update', state, y_raw);
```

---

### 问题0.6：编译错误 "对 coder.extrinsic 的调用可能只出现在顶层"

**错误信息**：
```
对 coder.extrinsic 的调用可能只出现在顶层。
函数 'GRU_state_classifier' 在使用后标记了 coder.extrinsic。
```

**原因**：
- `coder.extrinsic` 声明必须在函数**最顶层**（不能在if语句内）
- 必须在**任何调用之前**声明

**解决方案**：将所有 `coder.extrinsic` 放在函数开头：
```matlab
function [theta_hat, ...] = GRU_State_Classifier(y_raw, reset)
%#codegen

% ✅ 正确：在函数顶层，所有调用之前声明
coder.extrinsic('evalin');
coder.extrinsic('GRU_state_classifier');
coder.extrinsic('extract_gru_output');
% ...
end
```

---

### 问题1：编译错误 "Undefined function 'GRU_state_classifier'"

**原因**：MATLAB Function块无法找到外部函数

**解决方案**：
1. 确保 `GRU_state_classifier.m` 在MATLAB路径中：
   ```matlab
   addpath(pwd)  % 添加当前目录
   ```
2. 检查文件是否存在：
   ```matlab
   which GRU_state_classifier
   % 应返回完整路径
   ```

### 问题2：仿真卡顿或很慢

**原因**：GRU推理计算量大

**解决方案**：
1. 降低采样频率（在GRU块前加 **Rate Transition**，例如降至10 Hz）
2. 检查GRU模型是否在GPU上（移到CPU）：
   ```matlab
   model.net_feature = gatherFromGPUToHost(model.net_feature);
   ```

### 问题3：theta_hat输出全为0

**原因**：GRU序列缓冲未满（前48步）

**解决方案**：
- 正常现象，序列满后（约2秒）开始输出有效值
- 可在 `GRU_state_classifier.m` 的 `initClassifier` 中预填充初始值

### 问题4：MPC求解失败

**原因**：theta_hat跳变过大

**解决方案**：
1. 增大RhoFilter的 `tau`（例如0.5s）
2. 在theta_hat输出后添加 **Rate Limiter** 块（限制 ±0.1 rad/s）

### 问题5：代码生成失败

**原因**：`coder.extrinsic` 不支持嵌入式目标

**解决方案**：见下节"代码生成优化"

---

## 代码生成优化（用于嵌入式目标）

如果需要生成C代码（例如用于硬件在环HIL），需要将GRU推理重写为可代码生成的版本。

### 方案1：使用MATLAB Coder支持的深度学习层

将 `dlnetwork` 转换为 `network` 对象（仅支持部分层）：
```matlab
% 在GRU_train.m训练后执行
net_codegen = coder.loadDeepLearningNetwork('GRU_model.mat', 'model');
```

### 方案2：使用Simulink Deep Learning Toolbox

将GRU改为 **Stateful Predict** 块（支持代码生成）：
1. 导出GRU为ONNX：
   ```matlab
   exportONNXNetwork(model.net_feature, 'gru_feature.onnx')
   ```
2. 在Simulink中使用 **ONNX Predict** 块

### 方案3：手动实现GRU（完全可代码生成）

参考 `GRU_state_classifier.m` 的特征提取逻辑，将GRU层展开为矩阵运算（工作量大）。

---

## 性能指标

集成后的预期性能：

| 指标 | 目标值 | 说明 |
|------|--------|------|
| **GRU推理延迟** | < 1 ms/步 | 在i7-10代CPU上 |
| **MPC求解时间** | < 5 ms/步 | P95百分位 |
| **theta_hat精度** | MAE < 2° | 对比theta_ground |
| **主分类准确率** | > 85% | 在线推理（含驻留时间） |
| **转弯分类准确率** | > 95% | 在线推理 |

---

## 下一步

1. **闭环验证**：运行完整20s仿真，对比有/无GRU的MPC性能
2. **压力测试**：测试极端工况（连续坡度、急转弯+颠簸）
3. **参数调优**：调整RhoFilter的tau、GRU驻留时间
4. **硬件部署**：如需要，执行代码生成优化

---

## 参考文档

- `func.md` - 功能导航（GRU模块详细接口）
- `README_LPVMPC_Usage.md` - LPV-MPC使用指南
- `.cursor/rules/lpvmpc.mdc` - 设计规范（第8节：AI工况识别）
- `test_GRU_workflow.m` - GRU离线测试示例

---

**版本**：V1.0  
**最后更新**：2025-11-05  
**作者**：LPV-MPC Project

