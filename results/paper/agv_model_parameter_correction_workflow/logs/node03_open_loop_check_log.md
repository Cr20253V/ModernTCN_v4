# Node 3 开环物理合理性自检记录

状态：已完成。

## 执行命令

```matlab
cd('E:/Matlab/Simulink/S-Function_16');
addpath(genpath('src'));
run('src/tests/test_agv_open_loop.m');
```

## 当前参数

- `front_cornering_stiffness = 3000 N/rad`
- `rear_cornering_stiffness = 3000 N/rad`
- `yaw_damping = 250 Nm/(rad/s)`
- `sideslip_damping = 0 1/s`
- `sideslip_low_speed_damping = 1 1/s`

## 主要结果

- 静态平衡：PASS，峰值速度漂移 `0.00e+00 m/s`。
- 恒力加速：PASS，理论加速度 `0.785 m/s^2`，实际 `0.784 m/s^2`，误差 `0.1%`。
- 低速左转 `omega_cmd=+0.10 rad/s`：PASS，实际 `omega=0.0888 rad/s`，跟踪率 `88.8%`。
- 低速右转 `omega_cmd=-0.10 rad/s`：PASS，实际 `omega=-0.0885 rad/s`，跟踪率 `88.5%`。
- S 弯左转 `omega_cmd=+0.37 rad/s`：FAIL by old open-loop threshold，实际 `omega=0.3137 rad/s`，跟踪率 `84.8%`，`beta=1.429 deg`。
- S 弯右转 `omega_cmd=-0.37 rad/s`：FAIL by old open-loop threshold，实际 `omega=-0.3144 rad/s`，跟踪率 `85.0%`，`beta=2.737 deg`。
- 第一弯右转 `omega_cmd=-0.39 rad/s`：FAIL by old open-loop threshold，实际 `omega=-0.3290 rad/s`，跟踪率 `84.4%`，`beta=2.952 deg`。
- 5 deg 坡度阻力：PASS，理论减速度 `-0.925 m/s^2`，实际 `-0.925 m/s^2`。
- 稳态速度：PASS，目标 `1.20 m/s`，稳态 `1.20 m/s`。
- 输出变量检查：PASS。
- 10 deg 极限爬坡：PASS，最终速度 `4.987 m/s`。

## 侧偏刚度小对比

附加测试比较 `C_alpha=3000` 与 `6000`：

- `C_alpha=3000`：`omega_cmd=0.37` 时稳态跟踪约 `85%`，`beta_peak` 约 `1.46-2.76 deg`，数值稳定。
- `C_alpha=6000`：当前开环几何/偏航分配下实际 `omega` 接近 `0`，不适合作为第一候选。

## 结论

- Node 3 的数值稳定性和基础物理自检通过。
- S 弯开环角速度跟踪约 `85%`，说明后续 Node 5/6 需要重新验证和整定 MPC/偏航相关权重。
- 不建议在当前几何/驱动力分配不变的前提下把第一候选直接提高到 `C_alpha=6000`。
- 本轮继续使用 `C_alpha=3000` 进入 Node 4。
