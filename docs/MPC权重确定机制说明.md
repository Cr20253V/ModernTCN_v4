# MPC权重系数确定机制详解

## 三层权重机制

### 第一层：基准权重（启动时）
**来源**：PreLoadFcn 中创建 ctrl 时设置
**时机**：打开Simulink模型时（一次性）
**作用**：作为 mpcobj 的初始权重

```matlab
% 从 maps_best.mat 提取的均值
Q_base = mean(maps_best.Q_range, 1);  % 例如 [15.32, 29.92, 3.54, 2.89]
R_base = mean(maps_best.R_range, 1);  % 例如 [0.002029, 0.002254]
dR_base = mean(maps_best.dR_range, 1); % 例如 [0.010076, 0.022951]

% 设置到 mpcobj
ctrl.mpcobj.Weights.OutputVariables = Q_base;
ctrl.mpcobj.Weights.ManipulatedVariables = R_base;
ctrl.mpcobj.Weights.ManipulatedVariablesRate = dR_base;
```

---

### 第二层：在线插值（每个时间步）✨
**来源**：`mpc_update_from_rho` 函数
**时机**：仿真运行时，每个采样周期（Ts）
**作用**：根据当前工况动态调整权重

#### 工作流程：

```
每个时间步（每 Ts = 0.05s）：
    ↓
1. UpdatePlantModel 函数被调用
    ↓
2. 获取当前调度变量 rho = [v; omega; theta]
   例如：rho = [1.05; 0.12; 0.03]  (转弯+小坡)
    ↓
3. 调用 mpc_update_from_rho(rho, db_rt, ctrl.maps)
    ↓
4. 归一化 rho → rho_n ∈ [0,1]³
   例如：rho_n = [0.625; 0.8; 0.575]
    ↓
5. 从 ctrl.maps 读取权重范围：
   ctrl.maps.Q_range = [
       7.66,  14.96, 1.77, 1.44;  ← Q_min (基准×0.5)
       22.98, 44.89, 5.31, 4.33   ← Q_max (基准×1.5)
   ]
    ↓
6. 根据 rho_n 和形状参数插值：
   
   # 步骤6.1：计算调度因子（考虑形状参数）
   对于 q_y：
       f_y = 0.3*rho_n(1) + 0.2*rho_n(2) + 0.5*rho_n(3)
       例如：f_y = 0.3*0.625 + 0.2*0.8 + 0.5*0.575 = 0.635
       
       应用形状映射（alpha_Q, beta_Q）：
       f_y_shaped = shape_map(f_y, alpha_Q, beta_Q)
   
   # 步骤6.2：线性插值
   Q_interp(1) = Q_min(1) + f_y_shaped * (Q_max(1) - Q_min(1))
               = 7.66 + 0.635 * (22.98 - 7.66)
               = 17.39  ← 本步的 q_y
   
   同理计算 q_psi, q_v, q_omega, r_F, r_omega, rdF, rdw
    ↓
7. 返回插值后的权重：
   upd.Q  = [17.39, 34.21, 4.12, 3.05]
   upd.R  = [0.001523, 0.001692]
   upd.dR = [0.007557, 0.017208]
    ↓
8. 更新 mpcobj 的权重（在 Cost_Function 中）：
   mpcobj.Weights.OutputVariables = upd.Q;
   mpcobj.Weights.ManipulatedVariables = upd.R;
   mpcobj.Weights.ManipulatedVariablesRate = upd.dR;
    ↓
9. MPC 用新权重求解本步优化问题
```

---

### 第三层：场景自适应增益（可选）✨
**来源**：`mpc_update_from_rho` 内部逻辑（L293-342）
**时机**：在插值基础上叠加
**作用**：转弯时自动提高横向跟踪权重

```matlab
% 在 mpc_update_from_rho.m 中：
omega_abs = abs(omega);  % 当前角速度绝对值

if omega_abs > (omega_thresh + trans_width)
    % 转弯区域：放大 q_y
    q_y_gain = q_y_gain_max;  % 例如 1.8 倍
    Q_interp(1) = Q_interp(1) * q_y_gain;
    
    % 例如：17.39 * 1.8 = 31.30
end
```

**效果**：
- 直线行驶时：`q_y = 17.39`（基础插值）
- 急转弯时：`q_y = 31.30`（×1.8 增益）
- 过渡区域：平滑变化（避免抖动）

---

## 完整示例

### 场景：左转弯 + 小坡

**输入状态**：
```
v     = 1.05 m/s
omega = 0.12 rad/s  (左转)
theta = 0.03 rad    (小坡)
```

**权重计算过程**：

| 步骤 | 计算 | 结果 |
|------|------|------|
| 归一化 | rho_n = [(1.05-0.8)/(1.2-0.8), ...] | [0.625, 0.8, 0.575] |
| 调度因子 | f_y = 0.3×0.625 + 0.2×0.8 + 0.5×0.575 | 0.635 |
| 形状映射 | shape_map(0.635, alpha_Q, beta_Q) | 0.712 |
| 线性插值 | 7.66 + 0.712×(22.98-7.66) | 18.57 |
| 场景增益 | omega=0.12 > 0.15? 否 → 无增益 | 18.57 |
| **最终q_y** | - | **18.57** |

**同理计算其他权重**：
```
Q_final  = [18.57, 35.42, 4.05, 2.98]
R_final  = [0.001612, 0.001804]
dR_final = [0.008123, 0.018456]
```

**这些权重用于本步（t=k）的MPC求解！**

---

## 关键机制：权重为什么要在线变化？

### 原因1：工况适应
不同工况需要不同的控制策略：
- **直线高速**：重视速度跟踪（↑ q_v）
- **转弯**：重视横向/航向（↑ q_y, q_psi）
- **坡道**：重视速度稳定（↑ q_v）

### 原因2：模型非线性
AGV动力学在不同速度/曲率下表现不同，固定权重无法全局最优。

### 原因3：鲁棒性
通过 alpha/beta 形状参数和因子权重，实现平滑过渡，避免抖动。

---

## 调试技巧

### 查看当前权重
在Simulink仿真时，在 UpdatePlantModel 函数中添加：
```matlab
% 在调用 mpc_update_from_rho 后
fprintf('t=%.2f: rho=[%.2f,%.3f,%.2f°], Q=[%.2f,%.2f,%.2f,%.2f]\n', ...
    t, rho(1), rho(2), rad2deg(rho(3)), upd.Q(1), upd.Q(2), upd.Q(3), upd.Q(4));
```

### 记录权重历史
```matlab
% 在 workspace 中预分配
assignin('base', 'Q_history', zeros(N, 4));

% 每步记录
Q_hist = evalin('base', 'Q_history');
Q_hist(k, :) = upd.Q;
assignin('base', 'Q_history', Q_hist);

% 仿真后绘图
figure;
plot(Q_history);
legend('q_y', 'q\_psi', 'q_v', 'q\_omega');
title('MPC权重在线变化');
```

---

## 总结

### 权重确定的三个时刻

| 时刻 | 机制 | 来源 | 频率 |
|------|------|------|------|
| **模型加载时** | 基准权重 | maps_best.mat 的均值 | 一次 |
| **每个时间步** | 在线插值 | mpc_update_from_rho + ctrl.maps | 每0.05s |
| **转弯时** | 场景增益 | omega_threshold 触发 | 动态 |

### 权重的层级关系

```
maps_best.mat (贝叶斯优化结果)
    ↓
Q_base (均值，作为基准)
    ↓
Q_range = [Q_base×0.5; Q_base×1.5] (变化区间)
    ↓
rho = [v; omega; theta] (当前工况)
    ↓
Q_interp (在线插值，每步不同)
    ↓
Q_final (叠加场景增益，转弯时更大)
    ↓
MPC求解器使用 Q_final 计算最优控制
```

### 为什么这样设计？

**静态权重（老方法）**：
```
Q = [3, 8, 1, 1]  (固定)
→ 直线还行，转弯不好
```

**LPV自适应权重（您的系统）**：
```
Q(rho) = f(v, omega, theta)  (动态)
→ 各种工况都优秀！✨
```

这就是**LPV-MPC（线性参数变化模型预测控制）**的核心优势！

