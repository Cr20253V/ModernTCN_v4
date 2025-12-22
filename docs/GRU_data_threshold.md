# GRU算法训练数据相关阈值说明

本文件汇总了GRU算法训练数据生成与标签标注过程中涉及的所有关键阈值，以及 GRU 在线推理所使用的输入变量与特征映射，便于后续调参与排错。

---

## 1. 坡度判定阈值
- **阈值名称**：坡度角阈值（theta_slope_thresh）
- **数值**：2°（弧度形式：deg2rad(2)）
- **位置**：
  - 脚本：`GRU_gen_train_data.m`
  - 位置：`generate_labels` 子函数内（约568行）
  - 代码：
    ```matlab
    theta_slope_thresh = deg2rad(2);     % 坡度阈值 2°
    ```

---

## 2. 堵转判定相关阈值
- **高电流阈值（I_high_thresh）**
  - 数值：12.0 [A]（默认值，可网格搜索）
  - 位置：
    - 脚本：`GRU_gen_train_data.m`
    - 位置：配置区（约92行），`generate_labels` 子函数（约568行）
    - 代码：
      ```matlab
      cfg.label_search.I_high_grid = [10, 12, 14];  % 配置区
      I_high_thresh = thresholds.I_high_thresh;     % generate_labels
      ```

- **堵转轮速阈值（omega_wheel_stall_thresh）**
  - 数值：0.1 [rad/s]
  - 位置：
    - 脚本：`GRU_gen_train_data.m`
    - 位置：`generate_labels` 子函数（约568行）
    - 代码：
      ```matlab
      omega_wheel_stall_thresh = 0.1;      % 堵转轮速阈值 [rad/s]
      ```

- **堵转加速度阈值（accel_stall_thresh）**
  - 数值：0.02 [m/s²]（默认值，可网格搜索）
  - 位置：
    - 脚本：`GRU_gen_train_data.m`
    - 位置：配置区（约93行），`generate_labels` 子函数（约568行）
    - 代码：
      ```matlab
      cfg.label_search.accel_stall_grid = [0.015, 0.02, 0.025];  % 配置区
      accel_stall_thresh = thresholds.accel_stall_thresh;        % generate_labels
      ```

- **堵转最小持续时间（stall_dwell）**
  - 数值：1.0 [s]（默认值，可网格搜索）
  - 位置：
    - 脚本：`GRU_gen_train_data.m`
    - 位置：配置区（约94行），`generate_labels` 子函数（约568行）
    - 代码：
      ```matlab
      cfg.label_search.stall_dwell_grid = [0.8, 1.0, 1.2];  % 配置区
      stall_duration_thresh = thresholds.stall_dwell;        % generate_labels
      ```

---

## 3. 打滑判定相关阈值

### 3.1 打滑注入配置（数据生成侧）
- **牵引系数范围（slip_gamma_range）**
  - 数值：0.3 ~ 0.7（注入时用，非直接判据）
  - 位置：
    - 脚本：`GRU_gen_train_data.m`
    - 位置：配置区（约98行）
    - 代码：
      ```matlab
      cfg.slip_cfg.gamma_range = [0.3, 0.7];  % 牵引系数范围
      ```

- **转弯场景轻度打滑牵引系数（slip_in_turn.gamma_range）**
  - 数值：0.65 ~ 0.85
  - 位置：
    - 脚本：`GRU_gen_train_data.m`
    - 位置：配置区（约101行）
    - 代码：
      ```matlab
      cfg.slip_in_turn.gamma_range = [0.65, 0.85];  % 轻度打滑
      ```

### 3.2 打滑标注配置（V4.8 新增：强化可分性）
- **高电流比例阈值（I_slip_high_ratio）**
  - 数值：0.35（V5.1 更新前为 0.6）
  - 含义：`I_sum > I_slip_high_ratio × I_high_thresh` 时认为驱动电流达到“打滑候选”水平。
  - 位置：
    - 脚本：`GRU_gen_train_data.m`
    - 位置：配置区（约114行）
    - 代码：
      ```matlab
      cfg.slip_label.I_slip_high_ratio = 0.35;
      ```

- **打滑加速度上限（accel_slip_small）**
  - 数值：0.05 [m/s²]（高驱动但加速度低于此值视为动力失配）
  - 位置：
    - 脚本：`GRU_gen_train_data.m`
    - 位置：配置区（约115行）
    - 代码：
      ```matlab
      cfg.slip_label.accel_slip_small = 0.05;
      ```

- **轮速-地速偏差阈值（v_err_thresh）**
  - 数值：0.15 [m/s]（V5.1 更新前为 0.3 m/s）
  - 位置：
    - 脚本：`GRU_gen_train_data.m`
    - 位置：配置区（约116行）
    - 代码：
      ```matlab
      cfg.slip_label.v_err_thresh = 0.15;
      ```

- **轮胎利用率阈值（tire_util_thresh）**
  - 数值：0.55（V5.1 更新前为 0.75）
  - 位置：
    - 脚本：`GRU_gen_train_data.m`
    - 位置：配置区（约117行）
    - 代码：
      ```matlab
      cfg.slip_label.tire_util_thresh = 0.55;
      ```

- **打滑最小持续时间（slip_min_dwell）**
  - 数值：0.3 [s]（V5.1 更新前为 0.5 s）
  - 位置：
    - 脚本：`GRU_gen_train_data.m`
    - 位置：配置区（约118行）
    - 代码：
      ```matlab
      cfg.slip_label.slip_min_dwell = 0.3;
      ```

- **堵转排除边界（exclude_stall_margin）**
  - 数值：0.2 [s]（堵转窗口前后各排除此时间，避免 slip/stall 混淆）
  - 位置：
    - 脚本：`GRU_gen_train_data.m`
    - 位置：配置区（约119行）
    - 代码：
      ```matlab
      cfg.slip_label.exclude_stall_margin = 0.2;
      ```

---


## 4. 转弯判定阈值
- **转弯角速度阈值（omega_turn_thresh）**
  - 数值：0.05 [rad/s]
  - 位置：
    - 脚本：`GRU_gen_train_data.m`
    - 位置：`generate_labels` 子函数（约568行）
    - 代码：
      ```matlab
      omega_turn_thresh = 0.05;  % 转弯角速度阈值 [rad/s]
      ```

- **转弯最小驻留时间（turn_dwell）**
  - 数值：0.40 [s]
  - 位置：
    - 脚本：`GRU_gen_train_data.m`
    - 位置：`generate_labels` 子函数（约568行）
    - 代码：
      ```matlab
      turn_dwell_steps = max(1, round(0.40 / Ts));  % 转弯驻留时间 0.40s
      ```

---

## 5. 其他相关阈值
- **flat/slope/打滑等状态最小驻留时间（dwell_time）**
  - 数值：0.5 [s]
  - 位置：
    - 脚本：`GRU_gen_train_data.m`
    - 位置：`generate_labels` 子函数（约568行）
    - 代码：
      ```matlab
      dwell_time = 0.5;                    % 最小驻留时间 [s]
      dwell_steps = max(1, round(dwell_time / Ts));
      ```

---

> 注：所有阈值均以2025年11月项目代码为准，部分参数支持网格搜索自动优化，具体以实际配置和代码为准。

---

## 6. GRU 输入变量与特征映射

### 6.1 AGV 输出向量 y_raw (31×1) 定义

来源：`output_eq.m` / `func.md`

- **[1] X**：车辆质心位置 X 方向 [m]
- **[2] Y**：车辆质心位置 Y 方向 [m]
- **[3] psi**：车辆航向角 [rad]
- **[4] v**：车辆质心纵向速度 [m/s]
- **[5] omega**：车辆偏航角速度（车身围绕 z 轴）[rad/s]
- **[6] delta_lf**：左前轮转向角 [rad]
- **[7] delta_rr**：右后轮转向角 [rad]
- **[8] beta**：车辆质心侧偏角（车身速度与车身纵轴夹角）[rad]
- **[9] accel_x_meas**：IMU 纵向加速度测量值 [m/s²]
- **[10] gyro_y_meas**：IMU 俯仰角速度测量值 [rad/s]
- **[11] gyro_z_meas**：IMU 偏航角速度测量值 [rad/s]
- **[12] I_meas_lf**：左前轮电机电流估计值 [A]
- **[13] I_meas_rr**：右后轮电机电流估计值 [A]
- **[14] F_dist_calc_lf**：左前轮扰动力估计值 [N]
- **[15] F_dist_calc_rr**：右后轮扰动力估计值 [N]
- **[16] theta_ground**：地面坡度角（道路纵向坡度）[rad]
- **[17] omega_wheel_lf**：左前轮角速度 [rad/s]
- **[18] omega_wheel_rr**：右后轮角速度 [rad/s]
- **[19] load_ratio_front**：前轴法向载荷占比（(N_lf+N_rf)/总重）[-]
- **[20] load_ratio_rear**：后轴法向载荷占比（(N_lr+N_rr)/总重）[-]
- **[21] load_transfer_lateral**：左右轮侧向载荷转移程度 [-]
- **[22] tire_utilization_lf**：左前轮摩擦利用率（纵向+侧向椭圆归一化）[-]
- **[23] tire_utilization_rr**：右后轮摩擦利用率 [-]
- **[24] lateral_accel**：车辆横向加速度估计 [m/s²]
- **[25] slip_angle_front**：前轴等效侧偏角 [rad]
- **[26] slip_angle_rear**：后轴等效侧偏角 [rad]
- **[27] drive_force_asymmetry**：左右驱动力不对称度 [-]
- **[28] slip_flag**：打滑状态标志（0=无打滑，1=打滑）[-]
- **[29] stall_flag**：堵转状态标志（0=正常，1=堵转）[-]
- **[30] N_lf**：左前轮法向载荷 [N]
- **[31] N_rr**：右后轮法向载荷 [N]

> 说明：GRU 在线推理的输入 `y_raw_t` 即为上述 31 维向量的当前时刻取值。

### 6.2 GRU 实际使用的 23 维特征（V1.5 更新）

来源：`GRU_prepare_dataset.m V1.5` / `GRU_state_classifier.m V1.4` 中的 `extractFeatures` 实现与 `feat_indices` 映射。

GRU 仅使用 y_raw 中的部分通道，并在在线与离线两侧做了一致的特征工程。特征定义如下（按特征向量顺序）：

1. **accel_x**（来自 y9：accel_x_meas）
  - 含义：纵向加速度测量 [m/s²]，反映驱动力、阻力与坡度的合成效果。
2. **gyro_z**（来自 y11：gyro_z_meas）
  - 含义：偏航角速度测量 [rad/s]，反映转弯强度和方向。
3. **I_lf**（来自 y12：I_meas_lf）
  - 含义：左前轮电机电流 [A]，反映驱动力需求与负载变化。
4. **I_rr**（来自 y13：I_meas_rr）
  - 含义：右后轮电机电流 [A]，与 I_lf 共同刻画驱动分配和工况。
5. **omega_wheel_lf**（来自 y17）
  - 含义：左前轮角速度 [rad/s]，反映轮速与地速匹配情况。
6. **omega_wheel_rr**（来自 y18）
  - 含义：右后轮角速度 [rad/s]。
7. **delta_lf**（来自 y6）
  - 含义：左前轮舵角 [rad]，反映车辆曲率与转弯趋势。
8. **delta_rr**（来自 y7）
  - 含义：右后轮舵角 [rad]，与 delta_lf 共同决定几何曲率和转弯工况。
9. **gyro_y**（来自 y10：gyro_y_meas）
  - 含义：俯仰角速度 [rad/s]，与坡度变化、起步/制动姿态相关。
10. **v_hat**（由 y17、y18 推导）
   - 计算：`v_hat = r * (omega_wheel_lf + omega_wheel_rr)/2`
   - 含义：基于轮速估计的车速 [m/s]，用于工况识别中的速度量纲统一。
11. **dv_hat_dt**（由 v_hat 差分+一阶低通滤波得到）
   - 含义：速度变化率 [m/s²]，刻画加减速过程（V1.1 采用滤波差分以降噪）。
12. **ws_imbalance**（由 y17、y18 推导）
   - 计算：`ws_imbalance = abs(omega_wheel_lf - omega_wheel_rr)`
   - 含义：左右轮轮速不平衡程度，反映转弯半径差、打滑或载荷不均。
13. **I_sum**（由 I_lf、I_rr 推导）
   - 计算：`I_sum = abs(I_lf) + abs(I_rr)`
   - 含义：总驱动电流 [A]，对应总驱动力与负载水平，是堵转/大坡度/重载的重要判据。
14. **I_diff_signed**（由 I_lf、I_rr 推导）
   - 计算：`I_diff_signed = I_lf - I_rr`
   - 含义：左右驱动电流带符号差值，保留“哪一侧更吃力”的方向信息（转弯+打滑判定）。
15. **I_diff_abs**（由 I_lf、I_rr 推导）
   - 计算：`I_diff_abs = abs(I_lf) - abs(I_rr)`
   - 含义：左右驱动电流幅值差，补充不对称程度特征。
16. **accel_x_lp**（由 accel_x 一阶低通滤波得到）
   - 含义：平滑后的纵向加速度 [m/s²]，用于提高堵转/坡度工况下的稳健性。
17. **kappa_proxy**（由 delta_lf、delta_rr、W 推导）
   - 计算：`kappa_proxy ≈ (tan(delta_lf) - tan(delta_rr)) / W`
   - 含义：曲率近似量，用于区分直线/大曲率转弯工况。
18. **v_true**（来自 y4：v）【V1.5 新增】
   - 含义：车辆真实纵向速度 [m/s]，用于与 v_hat 对比检测轮速-地速失配。
19. **v_err**（由 v_hat、v_true 推导）【V1.5 新增】
   - 计算：`v_err = v_hat - v_true`
   - 含义：轮速-地速偏差 [m/s]，打滑核心特征（正值表示轮速快于地速）。
20. **v_err_norm**（由 v_err、v_true 推导）【V1.5 新增】
   - 计算：`v_err_norm = v_err / max(|v_true|, v_eps)`
   - 含义：归一化轮速-地速偏差 [-]，消除速度量纲影响。
21. **tire_util_max**（由 y22、y23 推导）【V1.5 新增】
   - 计算：`tire_util_max = max(tire_utilization_lf, tire_utilization_rr)`
   - 含义：轮胎最大摩擦利用率 [-]，接近 1 表示摩擦力饱和，是打滑先兆。
22. **tire_util_diff**（由 y22、y23 推导）【V1.5 新增】
   - 计算：`tire_util_diff = tire_utilization_lf - tire_utilization_rr`
   - 含义：左右轮摩擦利用率差异 [-]，反映不对称负载/打滑模式。
23. **theta_ground**（来自 y16：theta_ground）【V1.5 新增】
   - 含义：地面真实坡度角 [rad]，帮助模型直接看到坡度，增强 slope 识别能力。

> **V1.5 更新要点**：  
> - 特征维度从 17 维扩展到 23 维（+6 维）；  
> - 新增特征聚焦于增强 slip 与 flat/slope 的可分性：轮速-地速失配（v_err 系列）+ 摩擦饱和（tire_util 系列）+ 直接坡度（theta_ground）；  
> - 所有新特征在离线（GRU_prepare_dataset.m V1.5）与在线（GRU_state_classifier.m V1.4）完全对齐。

> 未被 GRU 使用的 y_raw 通道包括：X, Y, psi, omega（y5，被 gyro_z 替代）, beta, F_dist_*, load_ratio_*, load_transfer_lateral, lateral_accel, slip_angle_*, drive_force_asymmetry, slip_flag, stall_flag, N_lf, N_rr（y1–3, 5, 8, 14–15, 19–21, 24–27, 28–29, 30–31）。这些量仅用于控制/MPC 或其他算法，不参与 GRU 特征。

---

## 7. 各行驶状态与关键特征（定性说明）

> 说明：下面是依据 `GRU_gen_train_data.m` 的标签逻辑和物理启发，对不同主分类所依赖的观测量的**定性总结**，用于理解模型行为与后续调参与可解释分析。具体数值判据由神经网络学习得到，并不直接暴露在代码中。

### 7.1 flat（平地正常行驶）

- 典型观测模式：
  - `accel_x` / `accel_x_lp`：接近 0 或与期望加减速一致，无长时间大正/负偏置；
  - `I_sum`：中等或较低，总电流未持续接近上限；
  - `theta_hat`（回归输出）接近 0，且满足 `|theta_hat| < theta_slope_thresh`（训练标注使用 `theta_slope_thresh = 2°`）；
  - `ws_imbalance`、`kappa_proxy`：根据是否直行/轻微转弯变化，但不产生明显打滑特征；
  - `slip_flag = 0`，`stall_flag = 0`（在训练标注中作为 flat 的辅助约束）。
- 主要依赖特征：`accel_x_lp`, `I_sum`, `dv_hat_dt`, `ws_imbalance`, `kappa_proxy` 等，用于确认“既不是强坡度、也不是打滑/堵转”。

### 7.2 slope（坡度行驶）

- 训练标注核心判据（见第 1 节）：
  - 真实坡度满足 `|theta_ground| >= theta_slope_thresh = deg2rad(2)`；
  - 标签中 `label_main = 4`，且 `mask_theta = 1` 仅对 slope 样本为 1。
- 典型观测模式：
  - `accel_x` / `accel_x_lp`：在相同 F_cmd 下表现出持续正/负偏置；
  - `I_sum`：为维持同一速度而显著高于平地；
  - `gyro_y`：在坡道进入/退出时，俯仰角速度会有响应；
  - `theta_hat`：回归头输出的连续坡度估计值，在线侧再经过 `tau_theta=0.15s` 低通和 `theta_deadzone` 死区处理后使用。
- 主要依赖特征：`accel_x`, `accel_x_lp`, `I_sum`, `dv_hat_dt`, `gyro_y`, `v_hat`。

### 7.3 slip（打滑）【V4.8 更新：强化标注逻辑】

- 训练标注核心判据（见第 3.2 节）：
  - **多条件联合**（宁少勿滥策略）：
    1. 在注入窗口内（初步候选）；
    2. 轮速-地速失配：`v_hat - v_true > v_err_thresh`（0.3 m/s）；
    3. 高驱动但低加速度：`I_sum > I_slip_high` 且 `|accel_x_lp| < accel_slip_small`（0.05 m/s²）；
    4. 轮胎利用率接近饱和：`tire_util_max > tire_util_thresh`（0.75）；
    5. 非堵转条件：轮速不能太低；
    6. 排除堵转边界 ±0.2s；
    7. 最小持续时间 0.5s。
- 典型观测模式（V1.5 新特征增强）：
  - **核心特征**：
    - `v_err` / `v_err_norm`：明显为正（轮速 > 地速），是打滑最直接证据；
    - `tire_util_max`：接近或超过 0.75，摩擦力饱和；
    - `I_sum`：中高电流（0.6–0.8 × I_high_thresh），但不到堵转水平。
  - **辅助特征**：
    - `accel_x_lp`：低于正常加速（< 0.05 m/s²），动力-加速度失配；
    - `ws_imbalance`：在直线大牵引或转弯时显著增大；
    - `I_diff_signed` / `I_diff_abs` / `tire_util_diff`：左右不对称，反映局部打滑。
  - **与其他类区别**：
    - vs flat：`v_err` 明显非 0，`tire_util_max` 更高；
    - vs slope：`theta_ground` 不大（< 2°），但 `v_err` 明显偏大；
    - vs stall：轮速不接近 0，`I_sum` 未达堵转阈值。
- 主要依赖特征（V1.5）：`v_err`, `v_err_norm`, `tire_util_max`, `tire_util_diff`, `I_sum`, `accel_x_lp`, `ws_imbalance`, `I_diff_signed`, `I_diff_abs`。

### 7.4 stall（堵转）

- 训练标注核心阈值（见第 2 节）：
  - `I_high_thresh`、`omega_wheel_stall_thresh`、`accel_stall_thresh` 和 `stall_dwell` 组合：
   - 车速/轮速接近 0；
   - 电流持续接近上限；
   - 纵向加速度长期接近 0。
- 典型观测模式：
  - `v_hat` / `omega_wheel_*`：接近 0；
  - `I_sum`：长时间高值；
  - `accel_x_lp`：接近 0；
  - `dv_hat_dt`：接近 0；
  - `stall_flag`：在 output_eq 中也会被置 1，但 GRU 训练主要使用连续特征，而非单一二值量。
- 主要依赖特征：`v_hat`, `omega_wheel_lf`, `omega_wheel_rr`, `I_sum`, `accel_x_lp`, `dv_hat_dt`。

---

> 小结：GRU 在线推理只使用 y_raw 中与**纵向动力学、电机电流、轮速、转向几何和 IMU**高度相关的 9 条原始通道，并在此基础上构造 17 维特征向量。位置类量（X、Y、psi）、大部分 AI 诊断量（载荷比例、轮胎利用率标志等）不会直接影响 GRU 的判断，更适合作为后处理和可视化指标。

## 8. GRU 在线坡度死区与抑噪逻辑

> 说明：本节记录 GRU 在线推理阶段对坡度估计 `theta_hat` 采用的平地抑噪逻辑，与训练标注阈值（2°）区分开来，仅作用于 **在线输出端**，不改变训练数据和模型结构。

- **硬死区阈值（theta_deadzone_hard）**
  - 数值：1.0°（弧度形式：`deg2rad(1.0)`）
  - 位置：
    - 脚本：`GRU_state_classifier.m`
    - 位置：`initClassifier` 中基础参数初始化区域
    - 代码：
      ```matlab
      state.theta_deadzone_hard = deg2rad(1.0);   % <1° 强制置零
      ```
  - 含义：当在线估计的低通坡度 `theta_hat_current` 落在 `[-1°, +1°]` 范围内，且当前主工况标签 `label_main_current == flat` 时，对外输出的坡度估计 `theta_hat_out` 被直接置为 0。内部状态和标签不被修改，仅抑制送往 RhoFilter / MPC 的小噪声。

- **软死区阈值（theta_deadzone_soft）**
  - 数值：1.5°（弧度形式：`deg2rad(1.5)`）
  - 位置：
    - 脚本：`GRU_state_classifier.m`
    - 位置：`initClassifier` 与 `updateClassifier` 中死区处理段
    - 代码：
      ```matlab
      state.theta_deadzone_soft = deg2rad(1.5);   % 1°~1.5° 线性压缩
      ```
  - 含义：当 `|theta_hat_current|` 落在 `[1°, 1.5°)` 区间、且 `label_main_current == flat` 时，对外坡度输出按线性系数进行压缩：
    - 先计算 `theta_abs = abs(theta_hat_out)`；
    - 计算归一化比例 `scale = (theta_abs - theta_deadzone_hard) / (theta_deadzone_soft - theta_deadzone_hard)`；
    - 输出 `theta_hat_out = sign(theta_hat_out) * (scale * theta_abs)`，使 1° 处输出仍为 0，1.5° 处逐渐过渡到原始值。

- **应用条件与不变性**
  - 死区逻辑仅在 `label_main_current == 1 (flat)` 时生效；一旦 GRU 判定为坡度工况（`label_main_current == 4`），则不再压制 `theta_hat`，以保留真实坡度信息。
  - 死区处理只作用于对外输出 `out.theta_hat`，内部的 `state.theta_hat_current` 及分类驻留逻辑保持原始 GRU 输出，用于后续时间上的平滑与状态判断，不会被硬清零。
  - 阈值 1°/1.5° 低于训练标注阈值 2°，不会破坏 slope 样本与 flat 样本在训练数据中的划分，只是在线侧对平地附近的小扰动做工程化抑制。

> 调参建议：如平地场景下 MPC 仍对 `theta_hat` 残余波动敏感，可进一步略微提高 `theta_deadzone_hard`（如 1.2°）或减小 `theta_deadzone_soft - theta_deadzone_hard` 间隔；若希望更早感知轻微坡度，则可反向减小两者，但建议始终保持 `theta_deadzone_soft ≤ theta_slope_thresh = 2°`。

## 9. 本次数据生成与训练关键配置（V5.1）

> 说明：本节记录 2025-11 使用的一版“稳定基线”配置，用于复现当前 99%+ 主分类准确率的实验结果。

- **数据规模与切片参数**：
  - 原始回合数：3000（`GRU_train_data_full.mat`）
  - 序列长度：96，滑窗步长：24（约 4.8 s，步长 1.2 s）
  - 按回合划分数据集：训练/验证/测试 = 70%/15%/15%

- **主分类标签分布（训练集，切片级）**：
  - flat: 23804（67.9%）
  - slip: 2449（7.0%，过采样前）→ 3674（过采样后）
  - stall: 1551（4.4%）
  - slope: 7271（20.7%）

- **少数类处理策略**：
  - 预处理阶段：对 slip 类做简单随机过采样，目标样本数 ≈ 1.5 × 原始 slip 数量；
  - 训练阶段：主分类使用 `class_labels = (1:4)'` 固定顺序，采用自定义“moderate balanced v1.6”类别权重：
    - flat: 0.4615，slip: 1.5385，stall: 1.3846，slope: 0.6154。

- **打滑判定策略（摘要）**：
  - 物理判据基于 `v_err`, `I_sum`, `accel_x_lp`, `tire_util_max` 等特征，使用 3.2 节所列阈值；
  - 新增回退逻辑：若在某回合中注入了 slip 但物理筛选后没有任何时刻通过判据，则在该注入时间窗内将所有满足“非堵转且远离堵转边界”的样本标记为 slip，以避免完全缺类。

- **训练配置**：
  - GRU 结构：输入维度 23，序列长度 96，双层 GRU（每层 96 单元）；
  - 多任务输出：主分类（4 类）、转弯分类（3 类）、坡度回归（1 维）；
  - 优化器：Adam，初始学习率 1e-3，cosine 调度，梯度裁剪 5.0；
  - 训练轮数：100 epoch，早停基于验证集总损失；
  - 最终测试性能：主分类准确率 99.07%，macro-F1 0.9825，转弯分类准确率 99.30%，坡度 MAE ≈ 0.97°。

> 若后续需要重新生成训练数据或比较不同版本，只需对照本节配置与 3.2 节阈值，即可判断是否与当前 V5.1 基线一致。

