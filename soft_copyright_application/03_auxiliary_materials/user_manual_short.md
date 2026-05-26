# 用户手册短版

## 1. 软件简介

本软件面向对角双转向驱动AGV的工况感知、LPV-MPC调度控制和闭环仿真验证，提供路径生成、车辆模型仿真、训练数据构建、ModernTCN多任务训练、ONNX导出、MATLAB在线推理、Simulink闭环仿真和对照实验评估功能。

## 2. 环境准备

建议使用 Windows 10/11 或兼容桌面系统，安装 MATLAB/Simulink、必要 MATLAB 工具箱、Python、PyTorch 和 ONNXRuntime。若进行深度模型训练，可配置 NVIDIA GPU；若仅运行已导出模型和闭环仿真，可使用普通 PC 工作站。

## 3. 初始化项目

在 MATLAB 中切换到项目根目录后运行：

```matlab
init_project;
root = project_root();
out_dir = results_dir();
```

## 4. 生成/检查数据集

当前主线数据集为：

```text
data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
```

对应数据契约为：

```text
data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2_contract.json
```

用户应优先检查数据契约中的 `Ts=0.01`、`seq_len=128`、`input_dim=19`、标签映射、split 策略和 scaler 策略。

## 5. 训练ModernTCN

Python 单 seed 训练入口为：

```bash
python src/ModernTCN/train_modern_tcn.py --dataset-file data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
```

多 seed 训练入口为：

```bash
python src/ModernTCN/run_modern_tcn_theta10_v2_multiseed.py
```

具体参数以脚本中的 `argparse` 定义为准。

## 6. 导出ONNX

默认部署模型位于：

```text
results/modern_tcn/modern_tcn_theta10_uniform_h0_v2_seed21/modern_tcn_seed21.onnx
```

可使用以下入口导出：

```bash
python src/ModernTCN/export_modern_tcn_onnx.py --checkpoint results/modern_tcn/modern_tcn_theta10_uniform_h0_v2_seed21/modern_tcn_seed21.pt
```

导出后可运行 ONNXRuntime 与 MATLAB 一致性检查脚本。

## 7. 加载Simulink闭环模型

在 MATLAB 中加载默认配置与闭环模型：

```matlab
init_project;
cfg = ModernTCN_default_config(project_root());
load_system('simulink/LPVMPC_AGV_simulink_Modern_TCN.slx');
```

GRU、TCN 和 IMU 对照模型分别位于 `simulink/LPVMPC_AGV_simulink_GRU.slx`、`simulink/LPVMPC_AGV_simulink_TCN.slx` 和 `simulink/LPVMPC_AGV_simulink_IMU.slx`。

## 8. 运行闭环仿真

闭环仿真由 Simulink 模型、预加载函数、ModernTCN 在线分类器和 LPV-MPC 更新函数共同完成。用户可通过对照实验脚本统一调用，也可手动加载模型并运行仿真。

## 9. 运行对照实验

常用对照入口包括：

```matlab
run_closed_loop_model_once
compare_tcn_gru_modern_closed_loop_out
run_lpvmpc_theta_baseline_experiment
run_multi_path_closed_loop_benchmark
run_closed_loop_robustness_experiment
run_realtime_benchmark
```

这些脚本用于生成三算法闭环比较、多路径评估、扰动鲁棒性评估和实时性统计。

## 10. 查看输出文件

主要结果输出到 `results/` 目录。ModernTCN 训练结果位于 `results/modern_tcn/modern_tcn_theta10_uniform_h0_v2_seed21/`；闭环对比结果位于 `results/compare/`；论文图表位于 `results/paper/`。

## 11. 常见问题

- 若 MATLAB 找不到函数，先运行 `init_project`。
- 若 ONNX 文件不存在，检查 `ModernTCN_default_config.m` 中的 `run_tag` 和 `onnx_file`。
- 若数据维度不匹配，检查数据契约中的 `seq_len=128` 和 `input_dim=19`。
- 若闭环模型加载失败，检查 `data/models/ctrl.mat`、`lin_agv_db.mat`、`plant_grid_test.mat` 和 Simulink 模型是否存在。
- 若实时性测试结果不能直接满足硬实时要求，应区分 ONNXRuntime+MPC 核心链路与 MATLAB/Simulink 桌面封装开销。
