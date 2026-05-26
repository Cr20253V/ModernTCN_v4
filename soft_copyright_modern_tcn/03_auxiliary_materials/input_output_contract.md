# 输入输出契约

## 1. 输入数据契约

### 1.1 输入窗口格式

| 参数 | 值 | 说明 |
|---|---|---|
| seq_len | 128 | 输入窗口长度（时间步） |
| input_dim | 19 | 输入特征维度 |
| Ts | 0.01 s | 控制/仿真采样周期 |
| 窗口覆盖时长 | 1.28 s | seq_len × Ts |
| 输入形状（训练） | [batch, 128, 19] | PyTorch 训练格式 |
| 输入形状（ONNX） | [1, 128, 19] | ONNX 导出固定形状 |
| 数据类型 | float32 | 单精度浮点 |

### 1.2 19 维输入特征

按以下顺序排列，顺序不可变更：

| 序号 | 特征名 | 含义 | 来源 |
|---:|---|---|---|
| 1 | accel_x | 纵向加速度 | IMU/仿真输出 |
| 2 | gyro_z | 偏航角速度 | IMU/仿真输出 |
| 3 | I_lf | 左前轮电流 | 驱动器反馈 |
| 4 | I_rr | 右后轮电流 | 驱动器反馈 |
| 5 | omega_wheel_lf | 左前轮角速度 | 编码器 |
| 6 | omega_wheel_rr | 右后轮角速度 | 编码器 |
| 7 | delta_lf | 左前轮转向角 | 转向编码器 |
| 8 | delta_rr | 右后轮转向角 | 转向编码器 |
| 9 | gyro_y | 俯仰角速度 | IMU |
| 10 | v_hat | 估计速度 | 状态估计器 |
| 11 | dv_hat_dt | 速度变化率 | 数值微分 |
| 12 | ws_imbalance | 轮速不平衡量 | 计算量 |
| 13 | I_sum | 电流和 | 计算量 |
| 14 | I_diff_signed | 有符号电流差 | 计算量 |
| 15 | I_diff_abs | 电流差绝对值 | 计算量 |
| 16 | accel_x_lp | 低通滤波纵向加速度 | 滤波器 |
| 17 | kappa_proxy | 曲率代理量 | 计算量 |
| 18 | accel_per_current | 单位电流加速度 | 计算量 |
| 19 | pitch_angle_est | 估计俯仰角 | 状态估计器 |

### 1.3 归一化策略

- 策略：`fit_train_only_apply_val_test_online`
- 仅在训练集上计算均值 `scaler_mean` 和标准差 `scaler_std`
- 归一化公式：`x_norm = (x - scaler_mean) / (scaler_std + eps)`
- `eps = 1e-8`
- scaler 参数保存在数据集 `.mat` 文件和 checkpoint 中

## 2. 输出数据契约

### 2.1 三任务输出

| 输出名 | 形状 | 类型 | 说明 |
|---|---|---|---|
| logits_main | [1, 3] | float32 | 主工况分类 logits |
| logits_turn | [1, 3] | 转向方向分类 logits |
| theta_hat | [1, 1] | float32 | 坡度/调度量回归 |

### 2.2 主工况分类标签映射

| 标签值 | 含义 | logits 索引 |
|---:|---|---:|
| 1 | flat（平地） | 0 |
| 2 | stall（堵转） | 1 |
| 3 | slope（坡道） | 2 |

解码方式：`label = argmax(logits_main) + 1`

### 2.3 转向方向分类标签映射

| 标签值 | 含义 | logits 索引 |
|---:|---|---:|
| -1 | right（右转） | 0 |
| 0 | straight（直行） | 1 |
| 1 | left（左转） | 2 |

解码方式：`label = argmax(logits_turn) - 1`

### 2.4 theta 输出调理

| 参数 | 默认值 | 说明 |
|---|---|---|
| theta_output_gain | 1.0 | 输出增益 |
| theta_abs_limit | deg2rad(12) | 绝对值限幅 |
| theta_rate_limit | deg2rad(5) | 变化率约束 |
| theta_mpc_deadzone | deg2rad(2) | MPC 死区 |

## 3. 数据划分契约

| 参数 | 值 | 说明 |
|---|---|---|
| split_policy | run_level_no_window_leakage | run 级划分，无窗口泄漏 |
| scaler_policy | fit_train_only_apply_val_test_online | 仅训练集拟合 scaler |
| label_strategy | current_window_end | 窗口末端标签 |
| horizon_steps | 0 | 当前步预测 |

## 4. 车辆对象契约

| 参数 | 值 | 说明 |
|---|---|---|
| vehicle_type | diagonal_dual_steer_drive_agv | 对角双转向驱动 AGV |
| 主动轮 | LF, RR | 左前、右后 |
| 被动轮 | RF, LR | 右前、左后 |
| Ts | 0.01 s | 控制采样周期 |
