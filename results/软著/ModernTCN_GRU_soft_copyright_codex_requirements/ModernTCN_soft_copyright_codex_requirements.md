# 基于 ModernTCN 的 AGV 工况感知与坡度调度软件 V1.0 软著材料生成技术要求（给 Codex 使用）

> 使用对象：Codex  
> 运行位置：当前项目仓库根目录 `Cr20253V/ModernTCN_v2`  
> 目标：基于当前仓库中与 ModernTCN 相关的自有源码、配置、流程和文档，生成一套可用于中国计算机软件著作权登记的辅助材料。  
> 重要原则：本申请包的软件主体是“ModernTCN 工况感知与坡度调度软件”，不是完整的 AGV-LPV-MPC 闭环控制平台。AGV 模型、LPV-MPC、路径生成和 Simulink 闭环只作为运行环境、验证环境和接口环境出现，不能喧宾夺主。

---

## 0. 总体要求

请在仓库根目录下生成如下目录：

```text
soft_copyright_modern_tcn/
├─ 00_application_info/
│  ├─ application_fields_draft.md
│  ├─ software_name_options.md
│  ├─ ownership_confirm_checklist.md
│  └─ material_boundary_statement.md
├─ 01_source_code_material/
│  ├─ source_file_index.csv
│  ├─ source_selection_report.md
│  ├─ ModernTCN_AGV_Perception_V1_full_source.txt
│  ├─ ModernTCN_AGV_Perception_V1_source_front30_back30.txt
│  ├─ ModernTCN_AGV_Perception_V1_source_front30_back30.docx
│  └─ ModernTCN_AGV_Perception_V1_source_front30_back30.pdf
├─ 02_software_document/
│  ├─ ModernTCN_AGV_Perception_V1_软件设计说明书.md
│  ├─ ModernTCN_AGV_Perception_V1_软件设计说明书.docx
│  └─ ModernTCN_AGV_Perception_V1_软件设计说明书.pdf
├─ 03_auxiliary_materials/
│  ├─ technical_feature_summary.md
│  ├─ user_manual_short.md
│  ├─ module_mapping_table.csv
│  ├─ input_output_contract.md
│  ├─ third_party_and_exclusion_statement.md
│  └─ difference_from_gru_application.md
└─ 04_compliance_check/
   ├─ page_format_check_report.md
   ├─ consistency_check_report.md
   ├─ duplication_boundary_check_report.md
   └─ final_submission_checklist.md
```

全部内容使用中文。源码材料保留 MATLAB/Python 原文，不要把源代码翻译成中文。

---

## 1. 软件名称与申请定位

### 1.1 推荐软件名称

推荐最终使用：

```text
软件全称：基于 ModernTCN 的 AGV 工况感知与坡度调度软件
软件简称：ModernTCN-AGV 感知调度软件
版本号：V1.0
```

备选名称：

```text
1. AGV 多任务时序工况感知与坡度调度软件 V1.0
2. 基于 ModernTCN 的 AGV 多任务时序感知软件 V1.0
3. ModernTCN-AGV 工况识别与坡度估计软件 V1.0
```

建议采用第一组推荐名称。所有材料的页眉、封面、申请字段草稿、源程序页眉必须完全一致：

```text
基于 ModernTCN 的 AGV 工况感知与坡度调度软件 V1.0
```

### 1.2 申请主体边界

本申请包的主体是：

```text
ModernTCN 多任务时序感知模型、数据读取与窗口组织、训练与评估、ONNX 导出、ONNXRuntime一致性验证、MATLAB在线预测、Simulink接口封装、坡度调度量输出与闭环验证接口。
```

不是主体的内容：

```text
AGV 非线性车辆动力学完整平台
LPV-MPC 控制器完整平台
Simulink 闭环控制模型本体
GRU/TCN 对照算法
论文图表生成系统
```

上述非主体内容可以作为“运行支撑模块”“验证环境”“接口模块”少量出现，但不得成为说明书主线。

---

## 2. 软著材料生成依据与格式要求

Codex 生成材料时按以下通用要求处理：

1. 软著申请材料通常包括申请表、软件鉴别材料和相关证明文件；
2. 鉴别材料包括程序和文档；
3. 程序和文档一般各取前、后连续 30 页；不足 60 页的提交全部；
4. 源程序页面每页不少于 50 行；
5. 文档页面每页不少于 30 行；
6. A4 纸、纵向、单面、黑白可读；
7. 每页应有页码；
8. 软件名称、简称、版本号在所有材料中必须一致。

本任务只生成技术辅助材料，不生成申请人身份证明、单位证明、公章页、合作协议、委托合同等法律证明文件。无法确定的信息用 `[申请人填写]` 标注，不得编造。

---

## 3. 项目事实与技术事实

说明书和申请表草稿必须使用以下事实。若仓库实际内容与下述事实冲突，以仓库当前源码和配置文件为准，并在 `consistency_check_report.md` 中说明差异。

### 3.1 软件应用对象

```text
车辆对象：diagonal_dual_steer_drive_agv
主动驱动/转向轮：LF、RR
被动支撑轮：RF、LR
控制/仿真采样周期：Ts = 0.01 s
```

### 3.2 数据契约

```text
输入窗口长度：seq_len = 128
输入特征维度：input_dim = 19
标签时间策略：current_window_end
预测步长：horizon_steps = 0
数据划分策略：run_level_no_window_leakage
scaler 策略：fit_train_only_apply_val_test_online
```

### 3.3 19维输入特征

必须按下列顺序写入说明书和输入输出契约：

```text
accel_x
gyro_z
I_lf
I_rr
omega_wheel_lf
omega_wheel_rr
delta_lf
delta_rr
gyro_y
v_hat
dv_hat_dt
ws_imbalance
I_sum
I_diff_signed
I_diff_abs
accel_x_lp
kappa_proxy
accel_per_current
pitch_angle_est
```

### 3.4 输出任务

```text
主工况分类：flat=1, stall=2, slope=3
转向方向分类：right=-1, straight=0, left=1
坡度/调度量回归：theta_hat
```

ModernTCN 输出命名：

```text
logits_main：3维主工况分类 logits
logits_turn：3维转向方向分类 logits
theta_hat：1维坡度/调度量回归输出
```

### 3.5 ModernTCN 默认配置

当前默认主线配置：

```text
seed = 21
run_tag = modern_tcn_theta10_uniform_h0_v2_seed21
seq_len = 128
input_dim = 19
channels = 64
blocks = 5
kernel_size = 31
temporal_padding = same
dropout = 0.15
expansion = 2
部署模型 = results/modern_tcn/modern_tcn_theta10_uniform_h0_v2_seed21/modern_tcn_seed21.onnx
```

注意：如果代码中存在 causal ModernTCN 消融结果，可以在说明书中作为“扩展/消融验证能力”一笔带过，但 V1.0 主申请材料以 `temporal_padding=same` 的 seed 21 为主，不要把 causal 模型写成默认部署模型。

---

## 4. 源码材料筛选规则

### 4.1 必须优先纳入的 ModernTCN 核心源码

以下文件应作为源码材料主体。若不存在，记录为 `missing`，不要中断生成流程。

```text
src/ModernTCN/modern_tcn_model.py
src/ModernTCN/modern_tcn_data.py
src/ModernTCN/modern_tcn_metrics.py
src/ModernTCN/train_modern_tcn.py
src/ModernTCN/run_modern_tcn_theta10_v2_multiseed.py
src/ModernTCN/export_modern_tcn_onnx.py
src/ModernTCN/check_onnxruntime_consistency.py
src/ModernTCN/ModernTCN_check_matlab_onnx.m
src/ModernTCN/ModernTCN_default_config.m
src/ModernTCN/ModernTCN_load_predictor.m
src/ModernTCN/ModernTCN_predict_window.m
src/ModernTCN/ModernTCN_online_step.m
src/ModernTCN/ModernTCN_state_classifier.m
src/ModernTCN/ModernTCN_State_Classifier_sim.m
src/ModernTCN/ModernTCN_analyze_closed_loop_out.m
src/ModernTCN/ModernTCN_replay_closed_loop_yraw.m
```

可作为辅助验证源码纳入，但不要超过主体篇幅：

```text
src/ModernTCN/test_causal_modern_tcn.py
src/ModernTCN/plot_modern_tcn_theta_scatter.m
src/ModernTCN/eval_modern_tcn_theta_sweep_plot.m
src/Compare/benchmark_modern_tcn_onnx_runtime.py
src/Compare/compare_modern_tcn_gru_closed_loop_out.m
src/Compare/compare_tcn_gru_modern_closed_loop_out.m
src/Compare/run_closed_loop_model_once.m
src/Compare/run_realtime_benchmark.m
```

### 4.2 可少量纳入的公共支撑源码

这些文件只作为 ModernTCN 软件的运行支撑，不应占据前后 60 页的大部分：

```text
init_project.m
project_root.m
results_dir.m
src/core/preloadfcn_modern_tcn.m
src/core/parameters.m
src/paths/gen_agv_ref_path.m
src/paths/gen_agv_theta10_uniform_paths.m
src/paths/gen_factory_logistics_showcase_path.m
src/paths/gen_modern_tcn_demo_path.m
src/paths/gen_modern_tcn_theta_sweep_plot_path.m
src/paths/gen_modern_tcn_theta_sweep_short_paths.m
```

如需说明闭环验证接口，可以纳入少量：

```text
src/lpv/lin_agv_at_point.m
src/lpv/lin_agv_grid.m
src/mpc/mpc_setup_single_interp.m
src/mpc/mpc_update_from_rho.m
```

但不能让 LPV-MPC 代码成为源码材料主体。

### 4.3 默认排除

必须排除：

```text
.git/
.github/
.kilo/
.cursor/
.venv/
__pycache__/
slprj/
tools/tmp_*
tools/tmp_slx_*
*.slxc
*.asv
*.autosave
```

必须排除或仅在说明书中作为运行产物引用，不纳入源程序材料：

```text
data/**/*.mat
data/**/*.csv
data/**/*.json
results/**/*.mat
results/**/*.csv
results/**/*.png
results/**/*.pt
results/**/*.onnx
results/**/*.md
figures/**/*.png
docs/**/*.md
*.pdf
*.docx
*.slx
src/ModernTCN/generated_layers/
```

说明：

1. `.pt`、`.onnx` 是模型权重/部署产物，不是源程序；
2. `.mat` 是数据、模型或仿真输出，不是源程序；
3. `.slx` 是 Simulink 二进制模型，不纳入源程序文本；
4. `generated_layers` 可能是 MATLAB ONNX 导入自动生成层，默认排除；如果必须引用，只在说明书中标注为“自动生成兼容层，不作为自有源程序主体”。

### 4.4 避免与 GRU 申请包高度重复

ModernTCN 源码材料中禁止大量纳入：

```text
src/gru/*.m
src/TCN/*.m
src/tests/test_gru*.m
```

这些内容属于 GRU/TCN 对照链路或另一个申请包。ModernTCN 包中最多在 `source_selection_report.md` 说明“作为对照算法存在，未纳入本申请主体”。

---

## 5. 源码汇编与排版要求

### 5.1 汇编顺序

生成 `ModernTCN_AGV_Perception_V1_full_source.txt` 时，按以下顺序拼接：

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
23. src/paths/ModernTCN相关路径生成脚本
24. 少量公共接口脚本
```

不要把 `state_eq.m`、`output_eq.m`、大型车辆模型代码放在前 30 页主体位置。否则软件材料会偏向车辆仿真平台，而不是 ModernTCN 感知软件。

### 5.2 文件边界

每个源码文件前插入：

```text
===== FILE: relative/path/to/file.ext =====
```

不要修改源文件逻辑。只在汇编文本中插入边界标记。

### 5.3 页眉、页码和行数

DOCX/PDF 页眉：

```text
基于 ModernTCN 的 AGV 工况感知与坡度调度软件 V1.0
```

页码格式建议：

```text
第 X 页 共 Y 页
```

排版建议：

```text
纸张：A4
方向：纵向
字体：Consolas 或 Courier New
字号：8.5 pt 或 9 pt
页边距：上 1.5 cm，下 1.5 cm，左 1.8 cm，右 1.5 cm
行距：固定值 10 pt
每页目标行数：55 行
```

若完整源码超过 60 页，生成：

```text
ModernTCN_AGV_Perception_V1_source_front30_back30.*
```

内容必须是完整源码汇编排版后的前 30 页和后 30 页，合计 60 页。不要生成 front35/back35。

若完整源码不足 60 页，提交全部源码，并将文件名改为：

```text
ModernTCN_AGV_Perception_V1_source_all.*
```

### 5.4 源码索引

生成 `source_file_index.csv`，字段：

```text
order,relative_path,language,lines,include_status,module,role,reason
```

`include_status` 取值：

```text
included
excluded_public_support
excluded_gru_tcn_other_application
excluded_binary_or_data
excluded_result
excluded_cache
excluded_generated
excluded_third_party
missing
```

---

## 6. 软件设计说明书要求

生成：

```text
ModernTCN_AGV_Perception_V1_软件设计说明书.md
ModernTCN_AGV_Perception_V1_软件设计说明书.docx
ModernTCN_AGV_Perception_V1_软件设计说明书.pdf
```

建议扩充到 35-60 页，最低不要少于 30 页。若不足 60 页则提交全文。每页尽量不少于 30 行，避免最后几页大面积空白。

### 6.1 说明书目录

请按以下目录生成，并写具体内容，不要只写空标题：

```text
封面
修订记录
目录

第1章 软件概述
  1.1 软件名称、简称与版本
  1.2 开发背景
  1.3 软件目标
  1.4 应用对象与使用场景
  1.5 软件边界
  1.6 与GRU申请包的边界区别

第2章 运行环境
  2.1 硬件环境
  2.2 软件环境
  2.3 开发语言
  2.4 Python依赖
  2.5 MATLAB/Simulink依赖
  2.6 输入输出文件环境

第3章 总体架构
  3.1 离线训练架构
  3.2 在线部署架构
  3.3 数据流
  3.4 控制/调用流
  3.5 与AGV-LPV-MPC验证平台的接口关系
  3.6 架构图或ASCII流程图

第4章 数据契约与输入特征
  4.1 数据来源
  4.2 统一数据集
  4.3 窗口化策略
  4.4 run级划分与防泄漏策略
  4.5 scaler拟合策略
  4.6 19维输入特征
  4.7 三任务标签定义
  4.8 输入输出数据格式

第5章 ModernTCN模型模块
  5.1 模块定位
  5.2 模型输入输出
  5.3 ModernTCN-small结构
  5.4 大核深度时序卷积
  5.5 残差连接与通道混合
  5.6 多任务输出头
  5.7 窗口统计特征融合
  5.8 same padding默认部署说明
  5.9 causal padding消融说明

第6章 训练与评估模块
  6.1 单seed训练入口
  6.2 多seed训练入口
  6.3 数据加载
  6.4 损失函数与指标
  6.5 checkpoint保存
  6.6 summary和history输出
  6.7 训练报告生成
  6.8 异常检查

第7章 ONNX导出与一致性验证
  7.1 ONNX导出目标
  7.2 输入输出名称
  7.3 PyTorch参考输出
  7.4 ONNXRuntime一致性检查
  7.5 MATLAB ONNX一致性检查
  7.6 部署文件冻结规则
  7.7 自动生成层的处理边界

第8章 MATLAB在线推理模块
  8.1 默认配置加载
  8.2 predictor加载
  8.3 在线窗口维护
  8.4 单窗口预测
  8.5 状态分类器
  8.6 theta输出调理
  8.7 限幅、deadzone与变化率约束
  8.8 Simulink包装函数

第9章 闭环验证接口
  9.1 验证平台说明
  9.2 preloadfcn_modern_tcn
  9.3 Simulink模型接口
  9.4 与LPV-MPC调度量的接口
  9.5 输出日志与结果分析
  9.6 闭环验证不是本软件主体的说明

第10章 结果分析与报告模块
  10.1 闭环输出分析
  10.2 yraw回放
  10.3 theta散点图
  10.4 theta sweep评估
  10.5 实时性测试
  10.6 与GRU/TCN比较的边界

第11章 用户使用说明
  11.1 初始化项目
  11.2 检查数据集
  11.3 训练ModernTCN
  11.4 多seed训练
  11.5 导出ONNX
  11.6 检查ONNXRuntime一致性
  11.7 检查MATLAB一致性
  11.8 加载MATLAB predictor
  11.9 运行Simulink闭环验证
  11.10 查看结果

第12章 技术特点
  12.1 多任务时序工况感知
  12.2 大核时序卷积结构
  12.3 统一数据契约
  12.4 跨Python/MATLAB部署
  12.5 面向闭环调度的theta输出调理
  12.6 可复现实验与验证

第13章 数据安全、第三方依赖与权属边界
  13.1 本地数据处理
  13.2 第三方依赖声明
  13.3 模型权重与训练数据不作为源程序
  13.4 自动生成代码处理
  13.5 权属确认事项

第14章 版本说明
  14.1 V1.0功能范围
  14.2 不包含的功能
  14.3 后续扩展方向

附录A 主要源码文件清单
附录B 输入输出文件清单
附录C 默认配置表
附录D 运行命令示例
附录E 术语表
```

### 6.2 说明书写作口径

必须使用“软件说明书”口吻，不要使用论文口吻。

使用：

```text
本软件实现……
本模块用于……
该功能支持……
该接口用于……
```

避免：

```text
本文提出……
本文证明……
实验表明本文方法……
论文第X节……
审稿人……
```

### 6.3 必须包含的架构图文本

可用 ASCII 图：

```text
路径/仿真数据
     │
     ▼
统一数据集与数据契约 ──> 128×19窗口 ──> ModernTCN训练
     │                                      │
     │                                      ▼
     │                              checkpoint / ONNX
     │                                      │
     ▼                                      ▼
MATLAB在线窗口维护 <── ONNX/MATLAB加载器 <── 一致性检查
     │
     ▼
logits_main / logits_turn / theta_hat
     │
     ▼
AGV-LPV-MPC闭环验证接口
```

### 6.4 申请表功能说明草稿

在 `application_fields_draft.md` 中写入 300-500 字，可直接复制：

```text
本软件面向对角双转向驱动AGV的工况感知与坡度调度需求，提供基于ModernTCN的多任务时序感知、模型训练、模型导出、在线推理和闭环验证接口。软件以128步、19维传感观测窗口作为输入，完成主工况识别、转向方向分类和坡度/调度量回归，输出logits_main、logits_turn和theta_hat等结果。软件支持使用统一数据契约进行数据加载、训练集拟合scaler、run级数据划分和多seed训练，能够生成训练指标、历史曲线和模型报告。软件可将PyTorch训练得到的ModernTCN模型导出为ONNX格式，并提供ONNXRuntime一致性检查、MATLAB端ONNX一致性检查、MATLAB在线预测、状态分类器和Simulink包装接口。AGV车辆模型、LPV-MPC和Simulink闭环模型在本软件中作为验证平台和接口环境，用于检查ModernTCN感知输出在闭环控制场景中的可调用性和稳定性。本软件不包含第三方深度学习框架源码、训练数据权属证明、模型权重源程序或申请人身份证明材料。
```

---

## 7. 辅助材料要求

### 7.1 `technical_feature_summary.md`

写入以下要点：

1. 固定长度多变量时序窗口；
2. 19维AGV观测特征；
3. 主工况、转向方向和坡度回归三任务输出；
4. 大核深度时序卷积；
5. 多seed训练与指标汇总；
6. ONNX导出；
7. PyTorch/ONNXRuntime/MATLAB一致性验证；
8. MATLAB在线窗口维护；
9. Simulink接口封装；
10. 面向LPV-MPC调度验证的theta输出调理。

### 7.2 `difference_from_gru_application.md`

必须明确：

```text
ModernTCN申请包以Python实现的ModernTCN网络、ONNX导出和跨环境部署链路为主体；
GRU申请包以MATLAB实现的GRU训练、推理、状态分类器和Simulink封装为主体；
两者可共用数据契约和验证平台，但源码鉴别材料、说明书章节主线、申请表功能描述必须分别突出各自算法和实现流程；
ModernTCN包不把GRU训练/推理源码作为主体；
GRU包不把ModernTCN Python模型定义和ONNX导出源码作为主体。
```

### 7.3 `third_party_and_exclusion_statement.md`

至少包含：

1. PyTorch、ONNXRuntime、MATLAB/Simulink 是依赖环境，不是自有源代码；
2. `.pt`、`.onnx`、`.mat`、`.slx`、`.png`、`.csv`、`.md` 结果报告不纳入源程序；
3. `generated_layers` 默认作为自动生成兼容层排除；
4. 申请人需确认是否存在职务开发、合作开发、委托开发或第三方开源代码；
5. GitHub 公开仓库若构成首次发表，首次发表日期需由申请人确认。

---

## 8. 一致性检查要求

生成 `consistency_check_report.md`，至少检查：

```text
[ ] 软件全称在所有材料中一致
[ ] 版本号均为 V1.0
[ ] 页眉包含软件全称和 V1.0
[ ] 源码材料为 front30/back30 或 all，不是 front35/back35
[ ] 源码每页不少于 50 行
[ ] 文档每页不少于 30 行
[ ] ModernTCN 核心源码占源码材料主体
[ ] GRU/TCN源码没有占据ModernTCN申请包主体
[ ] .pt/.onnx/.mat/.slx 未纳入源程序鉴别材料
[ ] generated_layers 未作为自有核心源码纳入
[ ] 说明书没有论文口吻
[ ] 说明书明确AGV/LPV-MPC/Simulink为验证环境或接口环境
[ ] 申请表字段中的著作权人、开发完成日期、首次发表日期已标注为申请人确认
```

---

## 9. Codex执行步骤

1. 扫描仓库；
2. 按本要求筛选 ModernTCN 相关源码；
3. 生成 `source_file_index.csv`；
4. 拼接完整源码；
5. 排版生成源码 DOCX/PDF；
6. 抽取前30页和后30页；
7. 生成软件设计说明书；
8. 生成申请表字段草稿；
9. 生成辅助材料；
10. 生成一致性检查报告；
11. 输出最终材料路径。

终端最终输出：

```text
ModernTCN软著申请辅助材料已生成：
1. 申请表字段草稿：soft_copyright_modern_tcn/00_application_info/application_fields_draft.md
2. 源码鉴别材料：soft_copyright_modern_tcn/01_source_code_material/ModernTCN_AGV_Perception_V1_source_front30_back30.pdf
3. 软件设计说明书：soft_copyright_modern_tcn/02_software_document/ModernTCN_AGV_Perception_V1_软件设计说明书.pdf
4. 技术特点摘要：soft_copyright_modern_tcn/03_auxiliary_materials/technical_feature_summary.md
5. 一致性检查报告：soft_copyright_modern_tcn/04_compliance_check/consistency_check_report.md

请申请人最终确认软件名称、版本号、著作权人、开发完成日期、首次发表日期、开发方式、权利取得方式及证明文件。
```
