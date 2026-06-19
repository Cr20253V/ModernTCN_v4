# MPC 重新整定报告

状态：Node 5-6 已完成到短窗口可行性整定。尚未宣称完成论文全路线最终 BO/Simulink 全量整定。

## 基础设置

- LPV 数据库版本：`agv_physics_v2_stabilized`
- 是否使用旧 `maps_best.mat`：否，旧 `data/models/maps_best.mat` 仅作为历史参考，本轮未覆盖 canonical 文件。
- 初始 `Np/Nc`：`150 / 50`
- 初始 `Q/R/dR`：`Q=[15.293, 28.737, 5.076, 2.9918]`，`R=[1e-3, 1e-3]`，`dR=[1e-2, 1e-2]`
- 初始约束：`F_cmd=[-600,600] N`，`omega_cmd=[-1.2,1.2] rad/s`，`dF=[-400,400] N/step`，`domega=[-0.9,0.9] rad/s/step`
- 输出软约束：`e_y=[-1.0,1.0] m`，`e_psi=[-0.5,0.5] rad`，软约束权重 `3e3`

## 可行性检查

- 第一次使用未稳定化 LPV 数据库时失败：
  - `J=1e6`
  - `fail_count=4`
  - 错误：`QP Hessian matrix too large, not positive definite`
  - 诊断：中心点离散极点 `16.1661`，全库最大极点约 `78.2895`
- 稳定化 LPV 数据库后，startup 2 s 短窗口通过：
  - `J=1.25988`
  - `fail_count=0`
  - `e_y RMSE=0`
  - `e_psi RMSE=0`
  - `e_v RMSE=0.00085`
  - `e_omega RMSE=0`
  - `constraint Linf=0`
  - `omega saturation=0`
- 使用 Node 6 最优短窗口配置后，4 个 2 s 窗口均通过：
  - `startup`: `J=0.500897`, `fail=0`, `e_y=0`, `e_psi=0`, `e_v=0.000812`, `constraint=0`
  - `turn`: `J=1.97544`, `fail=0`, `e_y=0.018468`, `e_psi=0.050816`, `e_v=0.012725`, `constraint=0`
  - `slope`: `J=1.70455`, `fail=0`, `e_y=0.034410`, `e_psi=0.071277`, `e_v=0.020629`, `constraint=0`
  - `composite`: `J=1.61506`, `fail=0`, `e_y=0.000169`, `e_psi=0.000684`, `e_v=0.128260`, `constraint=0`

## 最终设置

- `Np`：`30`
- `Nc`：`10`
- `Q`：`[15.293, 28.737, 5.076, 2.9918]`
- `R`：`[1e-3, 1e-3]`
- `dR`：`[1e-2, 1e-2]`
- 输入约束：`F_cmd=[-600,600] N`，`omega_cmd=[-1.2,1.2] rad/s`
- 输入变化率约束：`dF=[-400,400] N/step`，`domega=[-0.9,0.9] rad/s/step`
- 输出软约束：`e_y=[-1.0,1.0] m`，`e_psi=[-0.5,0.5] rad`，软约束权重 `3e3`
- 调度滤波：离线复现器中使用 `tau=0.35 s`

## 输出

- canonical `maps_best.mat` 路径：`data/models/maps_best.mat`，本轮未覆盖。
- 本目录副本路径：
  - `results/paper/agv_model_parameter_correction_workflow/06_mpc_retuning/maps_best_agv_physics_v2_node06.mat`
  - `results/paper/agv_model_parameter_correction_workflow/06_mpc_retuning/node05_smoke_startup_2s.mat`
  - `results/paper/agv_model_parameter_correction_workflow/06_mpc_retuning/node06_startup_2s_grid_tuning.mat`
  - `results/paper/agv_model_parameter_correction_workflow/06_mpc_retuning/node06_best_window_verification.mat`
- 调参结论：短窗口可行性已恢复，`Np=30/Nc=10` 明显降低求解负担；但 full-route Simulink 和完整 BO 仍应在 Node 9 之前单独执行。

## 重要注意

- 当前 Simulink 入口 `src/core/UpdatePlantModel.m` 仍硬编码一套 BO 权重区间；本轮 Node 6 的短窗口整定使用的是离线 `Cost_Function`/`mpc_setup_single_interp` 路径。
- 因此，本报告给出的配置是下一轮 MPC 全路线验证的候选起点，不应直接视为论文最终控制器参数。
