# 对角式双舵轮 AGV 建模与底层控制分析

本文档旨在提供对角式双舵轮 AGV 的完整数学描述。内容分为两部分：
1.  **物理建模**：基于牛顿-欧拉方程的刚体动力学与运动学描述。
2.  **底层控制分析**：解析当前仿真模型中内嵌的运动控制策略与稳定性增强算法。

---

## 第一章：AGV 运动学与动力学物理建模

### 1.1 概述
本章描述 AGV 作为刚体系统的客观物理规律。模型输入为各执行器的物理量（驱动力、转向角），输出为车辆状态的变化率。

> **与本项目代码实现一致的接口说明（建议用于论文表述）**：
> - 在本项目中，Plant（S-Function）对外输入为 `u_all=[F_cmd; omega_cmd; theta_ground]`：
>   - `F_cmd`：总驱动力/牵引力指令 [N]
>   - `omega_cmd`：期望横摆角速度指令 [rad/s]
>   - `theta_ground`：地面坡度角/纵向坡度扰动（Measured Disturbance）[rad]
> - 转向角 `delta_lf, delta_rr` **不是外部输入**，而是模型内部根据 ICR 几何约束和舵机一阶动力学生成，并作为状态量的一部分随时间演化。

**符号定义**：
参见附录符号表。

### 1.2 运动学模型 (Kinematics)
在车体坐标系 $o-xy$ 下，车辆质心的速度矢量为 $\vec{v} = [v \cos\beta, v \sin\beta]^T$。
在大地坐标系 $O-XY$ 下，位置更新方程为：

X_dot = v * cos(psi + beta)
Y_dot = v * sin(psi + beta)
psi_dot = omega

其中 psi 为航向角，beta 为质心侧偏角。

### 1.3 刚体动力学模型 (Rigid Body Dynamics)
基于牛顿-欧拉方程，考虑 3-DOF 平面运动（纵向、横向、横摆）。

#### 1.3.1 纵向动力学 (Longitudinal)
沿车体 $x$ 轴的力平衡方程：

m_eff * v_dot = sum(F_x) - F_drag - F_slope

*   **总驱动力**：sum(F_x) = F_x_lf + F_x_rr （仅左前、右后轮驱动）
*   **总阻力**：F_drag = F_roll + F_aero
    *   F_roll = C_r * m * g * cos(theta_slope)
    *   F_aero = 0.5 * rho * C_d * A * v^2 * sign(v)
*   **有效质量**：m_eff = m + 2 * (I_w + I_m * n^2) / r^2
    *（说明：代码实现中同样采用“等效质量”写法，其中系数 2 对应两驱动轮；严格物理上该等效主要影响纵向通道。）

#### 1.3.2 侧向动力学与侧偏角 (Lateral & Sideslip)
沿车体 $y$ 轴的力平衡（包含离心力项）：

m * v * (beta_dot + omega) = sum(F_y)

整理得到侧偏角变化率 $\dot{\beta}$：

beta_dot = (F_y_lf + F_y_rr) / (m * v) - omega

*   注：此方程在 $v \to 0$ 时存在奇异性，物理上对应静止时侧偏角无意义。

> **与代码一致的“增强型侧偏角动力学”**：
> - 代码在 `state_eq.m` 的连续动力学核心中采用
>   - 低速：`beta_dot = -5*beta`
>   - 正常速度：`beta_dot = (Fy_f+Fy_r)/(m_eff*max(|v|, low_speed_thresh/10)) - omega - 5*beta`
> - 并对 `beta_dot` 做限幅（约 ±10 deg/s），对 `beta` 做幅值保护（约 ±15 deg）。
> - 因此论文中若要“描述真实仿真Plant”，建议明确这是**虚拟阻尼 + 数值保护**，用于抑制低速奇异与侧偏发散。

#### 1.3.3 横摆动力学 (Yaw)
绕质心 $z$ 轴的力矩平衡方程：

I_z * omega_dot = sum(M_z)

总力矩由两部分组成：
1.  **轮胎侧向力产生的力矩**：
    M_z_tire = Lf * F_y_lf - Lr * F_y_rr
    *(注：此处假设转向角较小，侧向力主要贡献于横摆，精确推导需包含 F_x, F_y 经转向角 delta 投影后的分量)*

2.  **差动驱动产生的力矩**：
    M_z_drive = (W / 2) * (F_x_lf - F_x_rr)

> **与代码一致的“虚拟横摆阻尼”**：
> - `state_eq.m` 中还额外叠加阻尼力矩 `Mz_damping = -C_damping * omega`（典型值 `C_damping=1000`），用于提高阻尼比、抑制振荡。

### 1.4 轮胎模型 (Tire Model)
采用线性化轮胎模型结合摩擦圆限制。

1.  **轮胎侧偏角 alpha**：
    alpha_lf = beta + (Lf * omega) / v - delta_lf
    alpha_rr = beta - (Lr * omega) / v - delta_rr

2.  **侧向力 F_y**：
    F_y_lin = -C_alpha * alpha
    考虑到附着极限 mu * N，实际侧向力为：
    F_y = sign(F_y_lin) * min(|F_y_lin|, mu * N)

---

## 第二章：底层运动控制策略分析

当前的 AGV 仿真模型并非纯粹的开环被控对象，而是内嵌了为了其在仿真中保持稳定而设计的**底层控制与数值保护**。本章解析这些策略。

> **重要实现细节（避免论文与工程不一致）**：
> - 在 Simulink 的 Plant S-Function 中，当前版本实际调用的是 `state_eq_ref.m / output_eq_ref.m`（而不是 `state_eq.m / output_eq.m`）。
> - 两者的核心“底层控制结构”基本一致，但 `*_ref` 版本在转向几何（ICR 半径）上会优先参考 `ref.v_ref/ref.omega_ref`，以保证与参考轨迹曲率一致。

### 2.1 偏航运动控制 (Yaw Stability Control)
物理模型表明差动驱动力矩 M_z_drive 取决于 F_x_lf 和 F_x_rr 的差值。模型中内置了一个 **P 控制器** 来主动调节这个差值。

*   **控制目标**：使实际横摆角速度 omega 跟踪指令值 omega_cmd。
*   **控制律**：
    1.  计算误差：e_omega = omega_cmd - omega
    2.  比例控制计算期望角加速度：omega_dot_des = K_p * e_omega
    3.  计算所需额外力矩：M_z_req = I_z * omega_dot_des
    4.  转换为驱动力差指令：
        Delta_F_x = (2 * M_z_req) / W
*   **实现效果**：这使得 AGV 表现为一个**对横摆角速度指令闭环**的系统，而非开环系统。
    *补充：实现中还包含多重保护与限幅（低速关断、角速度超限刹车力矩、`omega_dot` 限幅、`Delta_Fx` 限幅等），这些对稳定性与可重复仿真非常关键，建议在论文中以“工程实现增强项”单独列出。

### 2.2 稳定性增强策略 (Stability Augmentation)
为了解决刚体模型在低速下的数值奇异性以及增强动态稳定性，模型引入了**虚拟阻尼**项。

#### 2.2.1 虚拟侧偏阻尼 (Virtual Sideslip Damping)
在 $\dot{\beta}$ 方程中人为添加了强阻尼项：

beta_dot_model = sum(F_y) / (m * v) - omega - 5.0 * beta  (Virtual Damping)

*   **物理意义**：这是一项并不存在的物理力，但在控制上等效于通过微调转向或驱动力来施加一个“使其回到运动方向”的恢复力矩。
*   **作用**：防止侧偏角 $\beta$ 在仿真中发散，特别是在低速段，强制 $\beta$ 收敛到 0，模拟了轮胎低速下的强自对准特性。

#### 2.2.2 虚拟横摆阻尼 (Virtual Yaw Damping)
在横摆动力学中添加了与 $\omega$ 成正比的阻尼力矩：

M_z_total = M_z_phys - C_yaw * omega  (Virtual Damping)

*   **作用**：增加系统的阻尼比，减少超调和震荡，模拟车身摩擦或未建模的阻尼效应。

### 2.3 牵引力控制 (Traction Control)
模型中内嵌了基于摩擦椭圆的**牵引力限制器**：

F_x_allow = mu * N * sqrt(1 - (F_y / (mu * N))^2)

*   **策略**：当检测到侧向力 $F_y$ 较大（如急转弯）时，主动限制纵向驱动力 $F_x$ 的上限。
*   **作用**：防止“顾此失彼”，确保轮胎合力不超出附着极限圆，优先保证侧向稳定性（防侧滑），其次提供纵向驱动力。

### 2.4 低速与静止处理 (Low Speed Handling)
当 $v < v_{thresh}$ (0.05 m/s) 时：
1.  **运动学**：使用显式的强阻尼 $\dot{\beta} = -C_{low} \beta$ 强制侧偏角归零。
2.  **动力学**：禁止差动偏航控制 ($\Delta F_x = 0$)，防止在原地产生过大的自旋力矩导致数值不稳定。
3.  **阻力**：滚动阻力计算考虑了符号函数平滑，避免零速震荡。

---

## 总结
该 AGV 模型是一个**面向控制的增强型动力学模型 (Control-Oriented Augmented Dynamic Model)**。
1.  **物理层**：通过牛顿-欧拉方程和非线性轮胎模型，准确描述了车辆的基本物理特性（惯性、摩擦、几何约束）。
2.  **控制层**：内嵌了**差动偏航控制**、**虚拟阻尼稳定**和**牵引力保护**，使得该模型不仅反映了“车是什么”，还反映了“底层驱动器怎么控制车”。

这种设计非常适合用于上层算法（如路径规划、轨迹跟踪 MPC）的开发与验证，因为它屏蔽了底层电机控制的复杂性，提供了一个稳定、响应可预测的被控对象接口。
