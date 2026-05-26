# 材料边界声明

## 1. 申请主体

本申请包的软件主体是"ModernTCN 工况感知与坡度调度软件"，核心内容包括：

1. ModernTCN 多任务时序感知模型定义（Python）
2. 统一数据集读取与窗口组织（Python）
3. 多任务损失函数与训练指标（Python）
4. 单 seed 与多 seed 训练入口（Python）
5. ONNX 模型导出（Python）
6. ONNXRuntime 一致性验证（Python）
7. MATLAB ONNX 一致性检查（MATLAB）
8. 默认部署配置加载（MATLAB）
9. predictor 加载与在线窗口维护（MATLAB）
10. 单窗口预测（MATLAB）
11. 状态分类器（MATLAB）
12. theta 输出调理与限幅（MATLAB）
13. Simulink 接口封装（MATLAB）
14. 闭环输出分析与回放（MATLAB）
15. 闭环验证接口（preloadfcn_modern_tcn）

## 2. 非主体内容

以下内容在本申请包中仅作为运行支撑模块、验证环境或接口环境出现，不作为软件主体：

1. AGV 非线性车辆动力学完整平台（state_eq.m、output_eq.m 等）
2. LPV 线性化与 MPC 控制器完整平台（lin_agv_at_point.m、mpc_setup_single_interp.m 等）
3. Simulink 闭环控制模型本体（.slx 文件）
4. GRU/TCN 对照算法（src/gru/、src/TCN/）
5. 论文图表生成系统（src/pic&table/）
6. 通用测试验证脚本（src/tests/）

## 3. 与 GRU 申请包的边界

- ModernTCN 申请包以 Python 实现的 ModernTCN 网络、ONNX 导出和跨环境部署链路为主体；
- GRU 申请包以 MATLAB 实现的 GRU 训练、推理、状态分类器和 Simulink 封装为主体；
- 两者可共用数据契约和验证平台，但源码鉴别材料、说明书章节主线、申请表功能描述必须分别突出各自算法和实现流程；
- ModernTCN 包不把 GRU 训练/推理源码作为主体；
- GRU 包不把 ModernTCN Python 模型定义和 ONNX 导出源码作为主体。

## 4. 排除范围

以下内容不纳入源程序鉴别材料：

- `.git/`、`.github/`、`.kilo/`、`.cursor/`、`.venv/`、`__pycache__/`、`slprj/` 等缓存和环境目录
- `data/**/*.mat`、`data/**/*.csv`、`data/**/*.json` 等数据文件
- `results/**/*.mat`、`results/**/*.csv`、`results/**/*.png`、`results/**/*.pt`、`results/**/*.onnx`、`results/**/*.md` 等结果和模型文件
- `figures/**/*.png`、`docs/**/*.md` 等图表和文档
- `*.pdf`、`*.docx`、`*.slx`、`*.slxc`、`*.asv`、`*.autosave` 等二进制和工程文件
- `src/ModernTCN/generated_layers/` 等 MATLAB ONNX 导入自动生成兼容层
