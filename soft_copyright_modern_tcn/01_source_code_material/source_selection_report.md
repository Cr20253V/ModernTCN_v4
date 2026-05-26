# 源码选择报告

生成日期：2026-05-25

## 1. 选择原则

本次程序鉴别材料以"基于 ModernTCN 的 AGV 工况感知与坡度调度软件 V1.0"为申请主体，优先纳入 ModernTCN 核心源码，包括：

1. ModernTCN 模型定义（Python）
2. 数据读取与窗口组织（Python）
3. 训练与评估（Python）
4. ONNX 导出与一致性验证（Python/MATLAB）
5. MATLAB 在线预测与状态分类器（MATLAB）
6. Simulink 接口封装（MATLAB）
7. 闭环验证接口与结果分析（MATLAB）

公共支撑模块（init_project.m、project_root.m、results_dir.m）少量纳入。路径生成、车辆参数等作为运行支撑在索引中记录但不占据源码主体。

## 2. 纳入统计

| 项目 | 数值 |
|---|---:|
| 纳入核心源文件数量 | 22 |
| 纳入核心源码行数 | 5267 |
| 完整源码汇编估算页数 | 106（按每页 50 行） |
| 提交源码页数 | 60（front30 + back30） |
| 每页目标行数 | 50 |

## 3. 源码汇编顺序

按以下顺序拼接：

```text
 1. init_project.m
 2. project_root.m
 3. results_dir.m
 4. src/ModernTCN/modern_tcn_model.py
 5. src/ModernTCN/modern_tcn_data.py
 6. src/ModernTCN/modern_tcn_metrics.py
 7. src/ModernTCN/train_modern_tcn.py
 8. src/ModernTCN/run_modern_tcn_theta10_v2_multiseed.py
 9. src/ModernTCN/export_modern_tcn_onnx.py
10. src/ModernTCN/check_onnxruntime_consistency.py
11. src/ModernTCN/ModernTCN_default_config.m
12. src/ModernTCN/ModernTCN_load_predictor.m
13. src/ModernTCN/ModernTCN_predict_window.m
14. src/ModernTCN/ModernTCN_online_step.m
15. src/ModernTCN/ModernTCN_state_classifier.m
16. src/ModernTCN/ModernTCN_State_Classifier_sim.m
17. src/ModernTCN/ModernTCN_check_matlab_onnx.m
18. src/core/preloadfcn_modern_tcn.m
19. src/ModernTCN/ModernTCN_analyze_closed_loop_out.m
20. src/ModernTCN/ModernTCN_replay_closed_loop_yraw.m
21. src/Compare/benchmark_modern_tcn_onnx_runtime.py
22. src/Compare/run_realtime_benchmark.m
```

前 30 页主要覆盖 Python 模型定义、数据加载、训练指标、训练入口和 ONNX 导出；后 30 页覆盖 MATLAB 在线推理、状态分类器、闭环分析和实时性测试。

## 4. 抽取说明

完整源码约 106 页，抽取完整源码排版后的前 30 页和后 30 页，合计 60 页。

生成的完整源码汇编文件为：

- `soft_copyright_modern_tcn/01_source_code_material/ModernTCN_AGV_Perception_V1_full_source.txt`

生成的提交用源码鉴别材料为：

- `soft_copyright_modern_tcn/01_source_code_material/ModernTCN_AGV_Perception_V1_source_front30_back30.txt`
- `soft_copyright_modern_tcn/01_source_code_material/ModernTCN_AGV_Perception_V1_source_front30_back30.docx`
- `soft_copyright_modern_tcn/01_source_code_material/ModernTCN_AGV_Perception_V1_source_front30_back30.pdf`

## 5. 排除说明

### 5.1 GRU/TCN 对照代码

`src/gru/` 和 `src/TCN/` 下的所有 MATLAB 文件属于 GRU/TCN 对照算法，对应另一个独立的软著申请包。ModernTCN 申请包中不纳入这些源码，仅在本报告中说明"作为对照算法存在，未纳入本申请主体"。

### 5.2 车辆模型与控制代码

`src/core/` 下的 `state_eq.m`、`output_eq.m`、`state_eq_ref.m`、`output_eq_ref.m`、`agv_model_sfunc.m` 等文件属于 AGV 非线性车辆动力学平台，不是 ModernTCN 感知软件的主体。`src/lpv/` 和 `src/mpc/` 下的 LPV 线性化和 MPC 控制器代码同样不作为本申请主体。

### 5.3 公共支撑模块

`init_project.m`、`project_root.m`、`results_dir.m` 和 `src/core/preloadfcn_modern_tcn.m` 作为项目初始化和闭环验证接口少量纳入。

### 5.4 缓存与环境目录

`.git/`、`.github/`、`.kilo/`、`.cursor/`、`.venv/`、`__pycache__/`、`slprj/` 等属于环境、缓存或平台配置，不纳入源程序。

### 5.5 数据与结果文件

`data/`、`results/`、`figures/`、`docs/` 下的数据、模型、图表、报告和中间结果不作为源程序鉴别材料。`.mat`、`.pt`、`.onnx`、`.slx`、`.pdf`、`.docx` 等文件属于数据、模型、二进制工程文件或文档，不作为源程序文本。

### 5.6 自动生成层

`src/ModernTCN/generated_layers/` 为 MATLAB 导入 ONNX 后产生的兼容层代码，默认标注为自动生成兼容层，不纳入本次核心源码。
