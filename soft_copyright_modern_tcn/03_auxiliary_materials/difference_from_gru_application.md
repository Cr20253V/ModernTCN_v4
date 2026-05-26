# 与 GRU 申请包的边界区别

## 1. 算法主体不同

- **ModernTCN 申请包**：以 Python 实现的 ModernTCN 多任务时序网络为核心，包含模型定义（modern_tcn_model.py）、数据加载（modern_tcn_data.py）、训练指标（modern_tcn_metrics.py）、训练入口（train_modern_tcn.py、run_modern_tcn_theta10_v2_multiseed.py）、ONNX 导出（export_modern_tcn_onnx.py）和跨环境一致性验证（check_onnxruntime_consistency.py、ModernTCN_check_matlab_onnx.m）。
- **GRU 申请包**：以 MATLAB 实现的 GRU 网络为核心，包含 GRU 训练（GRU_train.m）、推理（GRU_infer.m）、状态分类器（GRU_state_classifier.m）和 Simulink 封装（GRU_State_Classifier_gru_sim.m）。

## 2. 源码鉴别材料不同

- **ModernTCN 包**的源码鉴别材料以 Python 模型定义、训练流程、ONNX 导出和 MATLAB 在线部署代码为主体。
- **GRU 包**的源码鉴别材料以 MATLAB GRU 训练、推理和分类器代码为主体。
- 两个申请包的源码鉴别材料不重叠。

## 3. 说明书主线不同

- **ModernTCN 说明书**以大核时序卷积模型、多任务输出头、ONNX 跨平台部署和一致性验证为主线。
- **GRU 说明书**以 MATLAB GRU 网络实现、训练流程和 Simulink 集成为主线。

## 4. 申请表功能描述不同

- **ModernTCN 申请表**突出 Python 实现的 ModernTCN 网络、ONNX 导出和跨 Python/MATLAB 部署链路。
- **GRU 申请表**突出 MATLAB 实现的 GRU 训练、推理和 Simulink 封装。

## 5. 共用部分

两个申请包可共用以下内容：

1. 统一数据契约（数据集格式、窗口长度、特征维度、标签映射）；
2. AGV 车辆模型和 LPV-MPC 验证平台（仅作为运行环境引用）；
3. 路径生成模块（仅作为运行支撑引用）。

共用内容不作为任何一个申请包的主体，仅在说明书中作为运行环境或验证平台少量提及。

## 6. 明确排除

- ModernTCN 包不把 `src/gru/*.m` 和 `src/TCN/*.m` 作为源码鉴别材料主体；
- GRU 包不把 `src/ModernTCN/*.py` 和 ONNX 导出代码作为源码鉴别材料主体。
