# 候选 plant 参数记录

状态：Node 1 已完成。

## 本轮采用的第一候选

- `front_cornering_stiffness = 3000 N/rad`
- `rear_cornering_stiffness = 3000 N/rad`
- `C_damping = 250 Nm/(rad/s)`
- 正常速度 `beta_dot`：移除人工 `-5.0*beta` 阻尼项
- 低速 `beta_dot`：使用温和数值回零项 `-1.0*beta`
- 保留 `beta_dot` 变化率限幅 `deg2rad(10)`

## 选择理由

- `300 N/rad` 对当前 200 kg AGV 明显偏软，第一候选提升到 `3000 N/rad`，仍比乘用车典型量级保守。
- `C_damping = 250` 已落在此前建议的 `100-300` 范围内，且主 `state_eq_ref.m` 已经使用该值，因此本轮先统一所有 plant 入口为 `250`。
- 正常速度下移除 `-5.0*beta`，避免让学习模型和 LPV 线性化继续学习强人工侧滑稳定器。
- 低速保留 `-1.0*beta`，主要用于启动/低速数值稳定，不作为正常行驶动力学来源。

## 后续判断

- 若 Node 3 开环检查出现明显振荡或 `beta` 发散，优先尝试低速/正常速度均使用 `-1.0*beta` 的 mild damping 版本。
- 若转向仍迟钝，可继续比较 `C_alpha = 6000 N/rad`。
- 若控制过度激进或横摆振荡，可在 Node 6 MPC 重新整定阶段调整 `Q/R/dR`，不要先把 plant 阻尼重新调回 `1000`。
