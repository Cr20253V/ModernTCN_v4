# 两份软著材料生成总说明（给 Codex 使用）

本仓库可拆分为两份软著申请辅助材料：

1. `soft_copyright_modern_tcn/`：基于 ModernTCN 的 AGV 工况感知与坡度调度软件 V1.0
2. `soft_copyright_gru/`：基于 GRU 的 AGV 工况识别与坡度估计软件 V1.0

## 总体边界

两份材料可以共用以下事实：

- 车辆对象为 diagonal dual steer drive AGV；
- 主动驱动/转向轮为 LF、RR，被动支撑轮为 RF、LR；
- 采样周期 Ts = 0.01 s；
- 输入窗口 seq_len = 128；
- 输入维度 input_dim = 19；
- 使用统一 19 维输入特征；
- 主工况分类为 flat/stall/slope；
- 转向方向分类为 right/straight/left；
- 回归输出为 theta_hat；
- 使用 run_level_no_window_leakage 和 fit_train_only_apply_val_test_online；
- AGV模型、LPV-MPC和Simulink闭环主要作为验证平台或接口环境。

## 不得混淆的边界

ModernTCN 申请包主体：

- `src/ModernTCN/*.py`
- `src/ModernTCN/*.m`
- ONNX导出
- ONNXRuntime一致性验证
- MATLAB ONNX加载与在线预测
- Simulink包装
- ModernTCN相关分析脚本

GRU 申请包主体：

- `src/gru/*.m`
- GRU训练
- 多seed训练
- 默认部署配置
- GRU推理
- 在线状态分类器
- Simulink包装
- GRU测试、延时、滤波参数评估

两份材料的源码鉴别材料不应大量重复。公共支撑文件可以少量纳入，但不要让公共车辆模型、LPV-MPC或Simulink平台成为任一申请包的主体。
