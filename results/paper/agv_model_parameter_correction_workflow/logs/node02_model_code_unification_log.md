# Node 2 模型代码统一记录

状态：已完成。

## 修改时间

- 2026-05-31

## 修改文件

- `src/core/parameters.m`
- `src/core/state_eq_ref.m`
- `src/core/state_eq.m`
- `src/core/state_eq_ref_train_data.m`

## 统一后的参数

- `front_cornering_stiffness = 3000 N/rad`
- `rear_cornering_stiffness = 3000 N/rad`
- `yaw_damping = 250 Nm/(rad/s)`
- `sideslip_damping = 0 1/s`
- `sideslip_low_speed_damping = 1 1/s`

## 代码口径

- 主仿真 `state_eq_ref.m` 从 `parameters.m` 读取横摆和侧滑阻尼。
- 兼容实现 `state_eq.m` 从 `parameters.m` 读取横摆和侧滑阻尼。
- 训练数据版本 `state_eq_ref_train_data.m` 从 `parameters.m` 读取横摆和侧滑阻尼。
- 正常速度 `beta_dot` 不再硬编码 `-5.0*beta`。
- 低速 `beta_dot` 改为 `-sideslip_low_speed_damping * beta`。

## 检查

- `state_eq_ref` 短步进调用通过。
- `state_eq_ref_train_data` 短步进调用通过。
- `rg "1000.0|-5.0\\s*\\*\\s*beta"` 未在目标核心文件中发现旧硬编码残留。

## 注意

- `state_eq_ref.m` 和 `state_eq_ref_train_data.m` 原本存在转向几何和偏航控制细节差异，本节点只统一 plant 物理参数，不额外重构几何/控制逻辑。
