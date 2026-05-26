# 重复边界检查报告

生成日期：2026-05-25

## 1. 检查目的

本报告检查 ModernTCN 申请包与 GRU 申请包之间的源码鉴别材料重复情况，确保两个申请包各自突出不同的算法和实现流程。

## 2. ModernTCN 申请包源码范围

ModernTCN 申请包纳入的核心源码（22 个文件）：

| 序号 | 文件 | 语言 | 归属 |
|---:|---|---|---|
| 1 | init_project.m | MATLAB | 公共支撑 |
| 2 | project_root.m | MATLAB | 公共支撑 |
| 3 | results_dir.m | MATLAB | 公共支撑 |
| 4 | modern_tcn_model.py | Python | ModernTCN 核心 |
| 5 | modern_tcn_data.py | Python | ModernTCN 核心 |
| 6 | modern_tcn_metrics.py | Python | ModernTCN 核心 |
| 7 | train_modern_tcn.py | Python | ModernTCN 核心 |
| 8 | run_modern_tcn_theta10_v2_multiseed.py | Python | ModernTCN 核心 |
| 9 | export_modern_tcn_onnx.py | Python | ModernTCN 核心 |
| 10 | check_onnxruntime_consistency.py | Python | ModernTCN 核心 |
| 11 | ModernTCN_default_config.m | MATLAB | ModernTCN 部署 |
| 12 | ModernTCN_load_predictor.m | MATLAB | ModernTCN 部署 |
| 13 | ModernTCN_predict_window.m | MATLAB | ModernTCN 部署 |
| 14 | ModernTCN_online_step.m | MATLAB | ModernTCN 部署 |
| 15 | ModernTCN_state_classifier.m | MATLAB | ModernTCN 部署 |
| 16 | ModernTCN_State_Classifier_sim.m | MATLAB | ModernTCN 部署 |
| 17 | ModernTCN_check_matlab_onnx.m | MATLAB | ModernTCN 一致性 |
| 18 | preloadfcn_modern_tcn.m | MATLAB | 闭环接口 |
| 19 | ModernTCN_analyze_closed_loop_out.m | MATLAB | 结果分析 |
| 20 | ModernTCN_replay_closed_loop_yraw.m | MATLAB | 结果分析 |
| 21 | benchmark_modern_tcn_onnx_runtime.py | Python | 辅助验证 |
| 22 | run_realtime_benchmark.m | MATLAB | 辅助验证 |

## 3. GRU 申请包预期源码范围

GRU 申请包应以以下文件为主体（不在 ModernTCN 包中）：

| 文件 | 语言 | 归属 |
|---|---|---|
| src/gru/GRU_train.m | MATLAB | GRU 核心 |
| src/gru/run_GRU_train_theta10_v2_multi_seed.m | MATLAB | GRU 核心 |
| src/gru/GRU_default_config.m | MATLAB | GRU 部署 |
| src/gru/GRU_infer.m | MATLAB | GRU 核心 |
| src/gru/GRU_state_classifier.m | MATLAB | GRU 部署 |
| src/gru/GRU_State_Classifier_gru_sim.m | MATLAB | GRU 部署 |
| src/gru/GRU_load_default_to_base.m | MATLAB | GRU 部署 |

## 4. 重复检查结果

| 检查项 | 结果 |
|---|---|
| ModernTCN 包是否包含 GRU 源码 | 否 |
| ModernTCN 包是否包含 TCN 源码 | 否 |
| 两个包的 Python 核心代码是否重叠 | 否（ModernTCN 包以 Python 为主，GRU 包以 MATLAB 为主） |
| 两个包的 MATLAB 部署代码是否重叠 | 否（ModernTCN 使用 ModernTCN_*.m，GRU 使用 GRU_*.m） |
| 公共支撑代码是否重叠 | 是（init_project.m、project_root.m、results_dir.m 可共用，但仅作为少量支撑） |
| 验证平台代码是否重叠 | 部分（AGV 模型、LPV-MPC 可在两个包中引用，但不作为主体） |

## 5. 结论

ModernTCN 申请包与 GRU 申请包的源码鉴别材料不存在实质性重复。公共支撑代码（3 个文件，62 行）占 ModernTCN 包总行数的 1.2%，不影响主体区分。两个申请包分别以 Python ModernTCN 网络 + ONNX 部署和 MATLAB GRU 网络 + Simulink 封装为主体，算法和实现流程明确区分。
