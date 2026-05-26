# 用户手册短版

## 1. 软件简介

本软件面向对角双转向驱动 AGV 的工况感知与坡度调度需求，提供基于 ModernTCN 的多任务时序感知、模型训练、ONNX 导出、在线推理和闭环验证接口。

## 2. 环境准备

建议使用 Windows 10/11 或兼容桌面系统，安装 Python 3.8+、PyTorch、ONNXRuntime、MATLAB/Simulink。若进行深度模型训练，可配置 NVIDIA GPU；若仅运行已导出模型和在线推理，可使用普通 PC 工作站。

## 3. 初始化项目

在 MATLAB 中切换到项目根目录后运行：

```matlab
init_project;
root = project_root();
out_dir = results_dir();
```

## 4. 检查数据集

当前主线数据集为：

```text
data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
```

对应数据契约为：

```text
data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2_contract.json
```

用户应优先检查数据契约中的 `Ts=0.01`、`seq_len=128`、`input_dim=19`、标签映射、split 策略和 scaler 策略。

## 5. 训练 ModernTCN

Python 单 seed 训练入口为：

```bash
python src/ModernTCN/train_modern_tcn.py --dataset-file data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
```

多 seed 训练入口为：

```bash
python src/ModernTCN/run_modern_tcn_theta10_v2_multiseed.py
```

## 6. 导出 ONNX

默认部署模型位于：

```text
results/modern_tcn/modern_tcn_theta10_uniform_h0_v2_seed21/modern_tcn_seed21.onnx
```

可使用以下入口导出：

```bash
python src/ModernTCN/export_modern_tcn_onnx.py --checkpoint results/modern_tcn/modern_tcn_theta10_uniform_h0_v2_seed21/modern_tcn_seed21.pt
```

## 7. 检查一致性

ONNXRuntime 一致性检查：

```bash
python src/ModernTCN/check_onnxruntime_consistency.py
```

MATLAB ONNX 一致性检查：

```matlab
ModernTCN_check_matlab_onnx();
```

## 8. 加载 MATLAB predictor

```matlab
cfg = ModernTCN_default_config(project_root());
[predictor, info] = ModernTCN_load_predictor(cfg);
```

## 9. 运行 Simulink 闭环验证

```matlab
init_project;
cfg = ModernTCN_default_config(project_root());
load_system('simulink/LPVMPC_AGV_simulink_Modern_TCN.slx');
sim('simulink/LPVMPC_AGV_simulink_Modern_TCN.slx');
```

## 10. 查看结果

主要结果输出到 `results/` 目录。ModernTCN 训练结果位于 `results/modern_tcn/modern_tcn_theta10_uniform_h0_v2_seed21/`。

## 11. 常见问题

- 若 MATLAB 找不到函数，先运行 `init_project`。
- 若 ONNX 文件不存在，检查 `ModernTCN_default_config.m` 中的 `run_tag` 和 `onnx_file`。
- 若数据维度不匹配，检查数据契约中的 `seq_len=128` 和 `input_dim=19`。
