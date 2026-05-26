# 基于 GRU 的 AGV 工况识别与坡度估计软件 V1.0 软著材料生成技术要求（给 Codex 使用）

> 使用对象：Codex  
> 运行位置：当前项目仓库根目录 `Cr20253V/ModernTCN_v2`  
> 目标：基于当前仓库中与 GRU 相关的自有源码、配置、流程和文档，生成一套可用于中国计算机软件著作权登记的辅助材料。  
> 重要原则：本申请包的软件主体是“GRU 工况识别与坡度估计软件”，不是完整 AGV-LPV-MPC 闭环控制平台，也不是 ModernTCN 主方法软件。公共 AGV 模型、LPV-MPC、路径生成和 Simulink 闭环只作为运行支撑和验证接口出现。

---

## 0. 总体要求

请在仓库根目录下生成如下目录：

```text
soft_copyright_gru/
├─ 00_application_info/
│  ├─ application_fields_draft.md
│  ├─ software_name_options.md
│  ├─ ownership_confirm_checklist.md
│  └─ material_boundary_statement.md
├─ 01_source_code_material/
│  ├─ source_file_index.csv
│  ├─ source_selection_report.md
│  ├─ GRU_AGV_Perception_V1_full_source.txt
│  ├─ GRU_AGV_Perception_V1_source_front30_back30.txt
│  ├─ GRU_AGV_Perception_V1_source_front30_back30.docx
│  └─ GRU_AGV_Perception_V1_source_front30_back30.pdf
├─ 02_software_document/
│  ├─ GRU_AGV_Perception_V1_软件设计说明书.md
│  ├─ GRU_AGV_Perception_V1_软件设计说明书.docx
│  └─ GRU_AGV_Perception_V1_软件设计说明书.pdf
├─ 03_auxiliary_materials/
│  ├─ technical_feature_summary.md
│  ├─ user_manual_short.md
│  ├─ module_mapping_table.csv
│  ├─ input_output_contract.md
│  ├─ third_party_and_exclusion_statement.md
│  └─ difference_from_modern_tcn_application.md
└─ 04_compliance_check/
   ├─ page_format_check_report.md
   ├─ consistency_check_report.md
   ├─ duplication_boundary_check_report.md
   └─ final_submission_checklist.md
```

所有非源码材料使用中文。源码材料保留 MATLAB 原文，不翻译代码。

---

## 1. 软件名称与申请定位

### 1.1 推荐软件名称

推荐最终使用：

```text
软件全称：基于 GRU 的 AGV 工况识别与坡度估计软件
软件简称：GRU-AGV 工况估计软件
版本号：V1.0
```

备选名称：

```text
1. AGV-GRU 多任务工况识别与坡度估计软件 V1.0
2. 基于 GRU 的 AGV 时序工况感知软件 V1.0
3. GRU-AGV 工况识别与在线推理软件 V1.0
```

建议采用推荐名称。所有材料页眉、封面、申请字段草稿和源码页眉必须完全一致：

```text
基于 GRU 的 AGV 工况识别与坡度估计软件 V1.0
```

### 1.2 申请主体边界

本申请包主体是：

```text
GRU 多任务时序模型训练、多seed训练入口、数据契约检查、默认部署配置、MATLAB推理函数、在线状态分类器、Simulink包装函数、模型加载到base workspace、GRU性能/延时/滤波参数测试与闭环验证接口。
```

不是主体的内容：

```text
ModernTCN Python网络结构和ONNX导出链路
TCN对照算法
完整AGV车辆仿真平台
完整LPV-MPC控制平台
论文图表系统
```

公共模型和验证平台可作为“支撑环境”出现，但不得成为 GRU 软著主体。

---

## 2. 软著材料生成依据与格式要求

Codex 按以下要求生成：

1. 申请材料通常包括申请表、软件鉴别材料、相关证明文件；
2. 鉴别材料包括程序和文档；
3. 程序和文档一般各取前、后连续 30 页；不足 60 页提交全部；
4. 源程序页面每页不少于 50 行；
5. 文档页面每页不少于 30 行；
6. A4 纸、纵向、单面、黑白可读；
7. 每页应有页码；
8. 软件全称、简称、版本号在所有材料中一致。

本任务只生成技术辅助材料，不生成身份证明、权属证明、委托合同、合作协议、公章页等法律文件。无法确定字段写 `[申请人填写]`。

---

## 3. 项目事实与技术事实

### 3.1 软件应用对象

```text
车辆对象：diagonal_dual_steer_drive_agv
主动驱动/转向轮：LF、RR
被动支撑轮：RF、LR
采样周期：Ts = 0.01 s
```

### 3.2 数据契约

当前 GRU 主线使用与 ModernTCN 相同的统一数据集，而不是旧 `data/gru` 数据链。必须在说明书中说明：旧 `data/gru` 可作为历史链路或归档链路，当前 V1.0 主材料以统一 `theta10_uniform_h0_v2` 数据契约为准。

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
坡度估计/调度量回归：theta_hat
```

GRU 说明书中可以使用以下输出描述：

```text
主工况预测结果
转向方向预测结果
坡度估计值或调度量 theta_hat
分类置信度或中间统计量
在线状态分类器输出
```

如果源码中实际变量名不同，以源码为准，并在 `input_output_contract.md` 中列出“源码变量名—说明书名称”的对应关系。

### 3.5 GRU 默认配置

当前 GRU 主线配置：

```text
seed = 101
case_name = inputstats_hidden96_l2
hidden_size = 96
num_layers = 2
head_pooling = last_mean_inputstats
turn_head = mlp/inputstats
部署模型 = data/models/GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed101.mat
元数据 = data/models/GRU_meta_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed101.mat
```

不要把旧 `GRU_model_gru_fair_v1_*`、`transition_rich_v2_*`、`transition_rich_v3_*` 等历史模型写成 V1.0 默认部署模型。可以在说明书中以“历史实验结果或归档对象”提及。

---

## 4. 源码材料筛选规则

### 4.1 必须优先纳入的 GRU 核心源码

以下文件是 GRU 申请包主体。若不存在，记录为 `missing`，不要中断。

```text
src/gru/GRU_train.m
src/gru/run_GRU_train_theta10_v2_multi_seed.m
src/gru/GRU_check_v4_dataset_contract.m
src/gru/GRU_default_config.m
src/gru/GRU_infer.m
src/gru/GRU_state_classifier.m
src/gru/GRU_State_Classifier_gru_sim.m
src/gru/GRU_load_default_to_base.m
src/gru/GRU_ModernTCN_v4_compare.m
```

如仓库中存在以下文件，也可以作为历史数据链或辅助功能纳入，但必须标注角色：

```text
src/gru/GRU_prepare_dataset.m
src/gru/GRU_gen_train_data.m
src/gru/run_GRU_prepare_dataset_mamba_compare.m
src/gru/GRU_train_legacy_v17.m
```

说明：

1. 当前 V1.0 主线使用统一 `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`；
2. 旧 `data/gru` 数据链可以作为历史功能或兼容功能，不要写成主线；
3. 如纳入 legacy 文件，`source_selection_report.md` 必须解释其作用，不要让 legacy 占据源码材料主体。

### 4.2 GRU 支撑源码

可少量纳入：

```text
init_project.m
project_root.m
results_dir.m
src/core/preloadfcn_gru.m
src/core/parameters.m
src/paths/gen_agv_ref_path.m
src/paths/gen_agv_theta10_uniform_paths.m
src/paths/gen_factory_logistics_showcase_path.m
src/Compare/run_closed_loop_model_once.m
src/Compare/compare_modern_tcn_gru_closed_loop_out.m
src/Compare/compare_tcn_gru_modern_closed_loop_out.m
```

可纳入 GRU 测试源码：

```text
src/tests/test_GRU_workflow.m
src/tests/test_gru_performance.m
src/tests/test_gru_latency.m
src/tests/test_gru_filter_constants.m
```

这些测试文件可以放在完整源码汇编中后部，但前 30 页应优先体现 GRU 训练、配置、推理和在线分类器，不要一开始就是公共车辆模型。

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

必须排除或仅作为说明书中的运行产物引用：

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
```

### 4.4 避免与 ModernTCN 申请包高度重复

GRU 包中禁止大量纳入：

```text
src/ModernTCN/*.py
src/ModernTCN/export_modern_tcn_onnx.py
src/ModernTCN/check_onnxruntime_consistency.py
src/ModernTCN/ModernTCN_*.m
src/TCN/*.m
```

可以在说明书中说明 ModernTCN 是对照对象或同项目中的另一套感知链路，但不能让 ModernTCN 源码成为 GRU 包主体。

---

## 5. 源码汇编与排版要求

### 5.1 汇编顺序

生成 `GRU_AGV_Perception_V1_full_source.txt` 时，按以下顺序拼接：

```text
1. init_project.m
2. project_root.m
3. results_dir.m
4. src/gru/GRU_default_config.m
5. src/gru/GRU_check_v4_dataset_contract.m
6. src/gru/GRU_train.m
7. src/gru/run_GRU_train_theta10_v2_multi_seed.m
8. src/gru/GRU_infer.m
9. src/gru/GRU_state_classifier.m
10. src/gru/GRU_State_Classifier_gru_sim.m
11. src/gru/GRU_load_default_to_base.m
12. src/core/preloadfcn_gru.m
13. src/gru/GRU_ModernTCN_v4_compare.m
14. src/tests/test_GRU_workflow.m
15. src/tests/test_gru_performance.m
16. src/tests/test_gru_latency.m
17. src/tests/test_gru_filter_constants.m
18. src/Compare/compare_modern_tcn_gru_closed_loop_out.m
19. src/Compare/compare_tcn_gru_modern_closed_loop_out.m
20. 少量路径生成和公共支撑脚本
```

不要把 `state_eq.m`、`output_eq.m`、`agv_model_sfunc.m` 放在前 30 页主体位置。GRU 软著材料前部必须体现 GRU 模型配置、训练、推理和在线分类器。

### 5.2 文件边界

每个文件前插入：

```text
===== FILE: relative/path/to/file.ext =====
```

不要修改源文件逻辑。只在汇编文本中插入边界标记。

### 5.3 页眉、页码和行数

DOCX/PDF 页眉：

```text
基于 GRU 的 AGV 工况识别与坡度估计软件 V1.0
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
GRU_AGV_Perception_V1_source_front30_back30.*
```

内容必须是完整源码汇编排版后的前 30 页和后 30 页，合计 60 页。不要生成 front35/back35。

若完整源码不足 60 页，则提交全部源码，文件名改为：

```text
GRU_AGV_Perception_V1_source_all.*
```

### 5.4 源码索引

生成 `source_file_index.csv`：

```text
order,relative_path,language,lines,include_status,module,role,reason
```

`include_status` 取值：

```text
included
included_legacy_support
excluded_modern_tcn_other_application
excluded_tcn_other_application
excluded_binary_or_data
excluded_result
excluded_cache
excluded_third_party
missing
```

---

## 6. 软件设计说明书要求

生成：

```text
GRU_AGV_Perception_V1_软件设计说明书.md
GRU_AGV_Perception_V1_软件设计说明书.docx
GRU_AGV_Perception_V1_软件设计说明书.pdf
```

建议扩充到 35-60 页，最低不要少于 30 页。若不足 60 页，提交全文。每页尽量不少于 30 行。

### 6.1 说明书目录

按以下目录生成：

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
  1.6 与ModernTCN申请包的边界区别

第2章 运行环境
  2.1 硬件环境
  2.2 软件环境
  2.3 开发语言
  2.4 MATLAB依赖
  2.5 Python/数据文件依赖说明
  2.6 输入输出文件环境

第3章 总体架构
  3.1 GRU离线训练架构
  3.2 GRU在线推理架构
  3.3 数据流
  3.4 调用流
  3.5 与AGV-LPV-MPC验证平台的接口关系
  3.6 架构图或ASCII流程图

第4章 数据契约与输入特征
  4.1 当前统一数据集
  4.2 旧GRU数据链与当前数据链区别
  4.3 窗口化策略
  4.4 run级划分与防泄漏策略
  4.5 scaler策略
  4.6 19维输入特征
  4.7 三任务标签定义
  4.8 输入输出数据格式

第5章 GRU模型训练模块
  5.1 模块定位
  5.2 默认配置
  5.3 GRU网络结构
  5.4 hidden_size与num_layers
  5.5 head_pooling策略
  5.6 turn_head策略
  5.7 多任务输出
  5.8 训练过程
  5.9 多seed训练

第6章 数据契约检查与预处理模块
  6.1 数据契约检查
  6.2 统一数据集读取
  6.3 特征标准化
  6.4 inputstats使用
  6.5 旧数据处理链说明
  6.6 异常与缺失字段处理

第7章 GRU推理模块
  7.1 GRU_infer
  7.2 输入窗口检查
  7.3 scaler应用
  7.4 主工况预测
  7.5 转向方向预测
  7.6 theta_hat坡度估计
  7.7 置信度和中间状态输出

第8章 在线状态分类器模块
  8.1 GRU_state_classifier定位
  8.2 在线窗口维护
  8.3 驻留时间机制
  8.4 theta低通滤波
  8.5 tau_accel_lp与tau_diff
  8.6 抖动抑制
  8.7 输出调理
  8.8 Simulink包装函数

第9章 部署与闭环验证接口
  9.1 默认模型加载
  9.2 GRU_load_default_to_base
  9.3 preloadfcn_gru
  9.4 Simulink模型接口
  9.5 与LPV-MPC调度量的接口
  9.6 闭环输出保存
  9.7 验证平台不是本软件主体的说明

第10章 测试与评估模块
  10.1 GRU工作流测试
  10.2 性能测试
  10.3 延时测试
  10.4 滤波参数测试
  10.5 闭环对比测试
  10.6 与ModernTCN/TCN比较的边界

第11章 用户使用说明
  11.1 初始化项目
  11.2 检查统一数据集
  11.3 加载默认配置
  11.4 训练GRU
  11.5 多seed训练
  11.6 加载默认模型
  11.7 执行单窗口推理
  11.8 运行在线状态分类器
  11.9 运行Simulink闭环验证
  11.10 查看测试结果

第12章 技术特点
  12.1 面向AGV传感窗口的GRU时序建模
  12.2 多任务工况识别与坡度估计
  12.3 inputstats融合策略
  12.4 在线状态分类与抖动抑制
  12.5 驻留时间和滤波参数评估
  12.6 与统一闭环验证平台对接

第13章 数据安全、第三方依赖与权属边界
  13.1 本地数据处理
  13.2 第三方依赖声明
  13.3 模型文件与数据文件不作为源程序
  13.4 历史数据链处理
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

使用软件说明书口吻：

```text
本软件实现……
本模块用于……
该接口支持……
该功能用于……
```

避免论文口吻：

```text
本文提出……
本文证明……
实验表明本文方法……
论文第X节……
```

### 6.3 必须包含的架构图文本

```text
统一AGV时序数据集
      │
      ▼
128×19输入窗口 ──> scaler / inputstats ──> GRU训练
      │                                      │
      │                                      ▼
      │                                GRU_model.mat
      │                                      │
      ▼                                      ▼
在线窗口维护 ───────────────> GRU_infer / GRU_state_classifier
      │                                      │
      ▼                                      ▼
主工况预测 / 转向预测 / theta_hat坡度估计
      │
      ▼
Simulink闭环验证接口 / LPV-MPC调度验证
```

### 6.4 申请表功能说明草稿

在 `application_fields_draft.md` 中写入 300-500 字，可直接复制：

```text
本软件面向对角双转向驱动AGV的时序工况识别与坡度估计需求，提供基于GRU的多任务感知模型训练、配置管理、在线推理、状态分类和闭环验证接口。软件以128步、19维AGV传感观测窗口作为输入，结合训练集拟合的scaler和输入统计信息，完成主工况分类、转向方向分类和坡度/调度量估计。软件提供GRU训练函数、多seed训练入口、数据契约检查、默认部署配置、GRU推理函数、在线状态分类器、Simulink包装函数和默认模型加载函数，支持在MATLAB/Simulink环境中进行窗口维护、工况输出、theta_hat输出调理以及闭环验证调用。软件还提供工作流测试、性能测试、延时测试和滤波参数测试脚本，用于评估GRU在AGV工况识别、转向识别和坡度估计中的稳定性与实时性。AGV车辆模型、LPV-MPC和Simulink闭环模型在本软件中作为验证平台和接口环境，不作为本软件申请的主体内容。本软件不包含第三方平台源码、训练数据权属证明、模型文件源程序或申请人身份证明材料。
```

---

## 7. 辅助材料要求

### 7.1 `technical_feature_summary.md`

写入以下要点：

1. 基于 GRU 的 AGV 多变量时序建模；
2. 128步、19维输入窗口；
3. 主工况识别、转向方向分类和坡度估计三任务输出；
4. hidden_size=96、num_layers=2 的默认部署结构；
5. inputstats 与 head pooling 融合；
6. turn_head MLP/inputstats 策略；
7. MATLAB 推理函数；
8. 在线状态分类器；
9. 驻留时间、低通滤波和抖动抑制；
10. Simulink 闭环验证接口；
11. 性能、延时和滤波参数测试。

### 7.2 `difference_from_modern_tcn_application.md`

必须明确：

```text
GRU申请包以MATLAB实现的GRU训练、推理、状态分类器、Simulink封装和测试评估为主体；
ModernTCN申请包以Python实现的ModernTCN网络、ONNX导出、ONNXRuntime/MATLAB一致性检查和跨环境部署为主体；
两者可共用统一数据契约、AGV验证平台和闭环对比脚本，但源码鉴别材料和说明书主线必须分开；
GRU包不纳入ModernTCN的Python模型定义、ONNX导出和ONNXRuntime检查源码作为主体；
ModernTCN包不纳入GRU训练、推理和状态分类器源码作为主体。
```

### 7.3 `third_party_and_exclusion_statement.md`

至少包含：

1. MATLAB/Simulink 是运行环境，不是自有源代码；
2. GRU 基础网络结构属于通用深度学习方法，本软件保护的是在 AGV 工况识别与坡度估计场景中的软件实现、工程流程和接口；
3. `.mat` 模型、训练数据、仿真输出、图片和结果报告不纳入源程序；
4. 旧数据链和历史模型仅作为兼容或归档内容，不是 V1.0 默认主体；
5. 申请人需确认是否存在职务开发、合作开发、委托开发或第三方开源代码；
6. GitHub 公开仓库若构成首次发表，首次发表日期需由申请人确认。

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
[ ] GRU核心源码占源码材料主体
[ ] ModernTCN/TCN源码没有占据GRU申请包主体
[ ] .mat/.pt/.onnx/.slx 未纳入源程序鉴别材料
[ ] 说明书没有论文口吻
[ ] 说明书明确AGV/LPV-MPC/Simulink为验证环境或接口环境
[ ] 说明书说明当前GRU主线使用统一数据集，而非旧data/gru主线
[ ] 申请表字段中的著作权人、开发完成日期、首次发表日期已标注为申请人确认
```

---

## 9. Codex执行步骤

1. 扫描仓库；
2. 按本要求筛选 GRU 相关源码；
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
GRU软著申请辅助材料已生成：
1. 申请表字段草稿：soft_copyright_gru/00_application_info/application_fields_draft.md
2. 源码鉴别材料：soft_copyright_gru/01_source_code_material/GRU_AGV_Perception_V1_source_front30_back30.pdf
3. 软件设计说明书：soft_copyright_gru/02_software_document/GRU_AGV_Perception_V1_软件设计说明书.pdf
4. 技术特点摘要：soft_copyright_gru/03_auxiliary_materials/technical_feature_summary.md
5. 一致性检查报告：soft_copyright_gru/04_compliance_check/consistency_check_report.md

请申请人最终确认软件名称、版本号、著作权人、开发完成日期、首次发表日期、开发方式、权利取得方式及证明文件。
```
