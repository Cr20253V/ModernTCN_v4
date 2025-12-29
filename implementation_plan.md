# GRU算法移除上帝视角参数 - 实施计划

移除GRU模型中的"上帝视角"参数，使其仅依赖IMU和AGV常规可观测数据。

## 变更概要

### 移除的参数（6个）
| 参数 | 描述 | 原因 |
|------|------|------|
| `v_true` | 真实地速 | 仿真器内部状态，实际不可观测 |
| `v_err` | 轮速-地速偏差 | 依赖v_true |
| `v_err_norm` | 归一化偏差 | 依赖v_true |
| `tire_util_max` | 最大轮胎利用率 | 需底层摩擦力模型，不可观测 |
| `tire_util_diff` | 轮胎利用率差异 | 同上 |
| `theta_ground` | 真实坡度角 | 仿真器设置值，实际不可观测 |

### 新增的替代特征（2个）
| 特征 | 计算方式 | 用途 |
|------|----------|------|
| `accel_per_current` | `accel_x_lp / I_sum` | 替代v_err检测打滑（电流-加速度失配） |
| `pitch_angle_est` | `∫gyro_y dt`（带衰减） | 间接推断坡度 |

### 特征维度变化
- 移除6维，新增2维 → **23维 → 19维**

---

## Proposed Changes

### GRU模块

#### [MODIFY] [GRU_prepare_dataset.m]
1. 移除第201-220行：`v_true`, `v_err`, `v_err_norm`, `tire_util_*`, `theta_ground`的提取和计算
2. 新增`accel_per_current`计算：`accel_x_lp ./ max(I_sum, 0.1)`
3. 新增`pitch_angle_est`计算：对`gyro_y`进行累积积分（带1阶衰减防漂移）
4. 更新第223-227行的特征组合矩阵
5. 更新第238-262行的`feat_names`列表

---

#### [MODIFY] [GRU_state_classifier.m]
1. 移除第195-198行的feat_indices：`v_true`, `tire_util_lf`, `tire_util_rr`, `theta_ground`
2. 在initClassifier中新增状态变量：`pitch_angle_est_prev`
3. 移除第377-396行的特征计算
4. 新增`accel_per_current`和`pitch_angle_est`计算
5. 更新第399-402行的特征组合

---

#### [MODIFY] [GRU_gen_train_data.m]
1. 移除配置中的`v_err_thresh`和`tire_util_thresh`（第102-104行）
2. 移除`generate_labels`中的v_err和tire_util相关判据（第666-675行，第688-689行，第711-717行）
3. 新增`accel_per_current`作为slip判定替代特征

---

## Verification Plan

### 自动化验证
```matlab
% 1. 运行数据预处理，验证特征维度
run('GRU_prepare_dataset.m');
assert(size(dataset.X_train, 3) == 19, '特征维度应为19');

% 2. 运行测试脚本
run('test_GRU_workflow.m');
```

### 手动验证
- 运行`GRU_gen_train_data.m`生成新数据，检查slip标注分布
- 确认无NaN/Inf特征值
