# ModernTCN\_v2 软著申请材料生成技术要求文档（给 Codex 使用）

> 目标：基于当前 GitHub 仓库 `Cr20253V/ModernTCN\_v2` 生成中国计算机软件著作权登记所需的辅助材料，重点生成“程序鉴别材料”“软件设计说明书/使用说明书”“申请表字段草稿”和“材料一致性检查清单”。  
> 注意：Codex 只负责从仓库生成材料，不负责判断著作权归属。申请人、著作权人、开发完成日期、首次发表日期、合作/委托/职务开发等法律信息必须由申请人最终确认。

\---

## 1\. 申请材料生成目标

请在仓库根目录下新建目录：

```text
soft\_copyright\_application/
├─ 00\_application\_info/
│  ├─ application\_fields\_draft.md
│  ├─ software\_name\_options.md
│  └─ ownership\_confirm\_checklist.md
├─ 01\_source\_code\_material/
│  ├─ source\_file\_index.csv
│  ├─ source\_selection\_report.md
│  ├─ ModernTCN\_AGV\_LPVMPC\_V1\_full\_source.txt
│  ├─ ModernTCN\_AGV\_LPVMPC\_V1\_source\_front30\_back30.txt
│  ├─ ModernTCN\_AGV\_LPVMPC\_V1\_source\_front30\_back30.docx
│  └─ ModernTCN\_AGV\_LPVMPC\_V1\_source\_front30\_back30.pdf
├─ 02\_software\_document/
│  ├─ ModernTCN\_AGV\_LPVMPC\_V1\_软件设计说明书.md
│  ├─ ModernTCN\_AGV\_LPVMPC\_V1\_软件设计说明书.docx
│  └─ ModernTCN\_AGV\_LPVMPC\_V1\_软件设计说明书.pdf
├─ 03\_auxiliary\_materials/
│  ├─ technical\_feature\_summary.md
│  ├─ user\_manual\_short.md
│  ├─ module\_mapping\_table.csv
│  └─ third\_party\_and\_exclusion\_statement.md
└─ 04\_compliance\_check/
   ├─ page\_format\_check\_report.md
   ├─ consistency\_check\_report.md
   └─ final\_submission\_checklist.md
```

全部生成物使用中文命名或中英文混合命名均可，但文件内容必须为中文，源代码材料保留代码原文。

\---

## 2\. 软件名称与版本建议

建议主名称使用以下之一，最终由申请人确认：

1. **面向对角双转向驱动AGV的ModernTCN-LPV-MPC工况感知与闭环控制仿真软件 V1.0**
2. **AGV工况感知与LPV-MPC闭环控制仿真软件 V1.0**
3. **基于ModernTCN的AGV工况感知与调度控制仿真软件 V1.0**

推荐使用第 2 个名称作为软著申请名称，原因是更像软件系统名称，避免将名称写得过长或过于论文标题化。

本文档后续统一使用：

```text
软件全称：AGV工况感知与LPV-MPC闭环控制仿真软件
软件简称：AGV-MTCN-MPC仿真软件
版本号：V1.0
```

生成所有页眉、封面、申请字段草稿时，必须保证软件名称与版本号完全一致。若申请人后续改名，必须全局替换。

\---

## 3\. 仓库主线理解

当前仓库是一个用于对角双转向驱动 AGV 闭环控制研究的软件工程。主线功能包括：

1. 建立 AGV 非线性车辆模型、参考路径模型、状态输出方程和参数配置；
2. 构建 LPV 线性化网格模型和 MPC 控制器；
3. 生成训练、测试和闭环展示所需的路径与时序数据集；
4. 使用 ModernTCN 对 AGV 当前工况进行在线感知，输出主工况分类、转向方向分类和坡度/调度量回归结果；
5. 将 ModernTCN 模型导出为 ONNX，并由 MATLAB/Simulink 加载到闭环控制仿真平台；
6. 提供 GRU、TCN、LPV-MPC theta 基线与 true-theta oracle 上界作为对照；
7. 自动完成离线训练评估、闭环仿真对比、多路径鲁棒性验证、扰动鲁棒性验证和实时性测试；
8. 输出训练指标、闭环指标、路径图、对比表和论文图表。

软著材料不要把论文写作内容作为主体，而应将项目描述成一个“用于 AGV 工况感知、LPV-MPC 调度与闭环仿真验证的软件系统”。

\---

## 4\. 源码材料生成范围

### 4.1 必须纳入的核心源码

请优先纳入以下文件/目录。若某个文件不存在，记录在 `source\_selection\_report.md` 中，不要中断整个流程。

#### 根目录入口

```text
init\_project.m
project\_root.m
results\_dir.m
```

用途：初始化 MATLAB 路径、定位项目根目录、规范输出目录。

#### 车辆模型与控制基础层

```text
src/core/agv\_model\_sfunc.m
src/core/agv\_model\_sfunc\_train\_data.m
src/core/state\_eq.m
src/core/output\_eq.m
src/core/state\_eq\_ref.m
src/core/output\_eq\_ref.m
src/core/state\_eq\_ref\_train\_data.m
src/core/output\_eq\_ref\_train\_data.m
src/core/parameters.m
src/core/UpdatePlantModel.m
src/core/UpdatePlantModel\_gru.m
src/core/preloadfcn\_modern\_tcn.m
src/core/preloadfcn\_gru.m
src/core/preloadfcn\_tcn.m
```

用途：AGV 动力学、仿真模型、训练数据仿真模型、参考轨迹、参数定义、闭环模型更新和预加载。

#### LPV 与 MPC

```text
src/lpv/lin\_agv\_at\_point.m
src/lpv/lin\_agv\_grid.m
src/mpc/mpc\_setup\_single\_interp.m
src/mpc/mpc\_update\_from\_rho.m
src/mpc/Cost\_Function.m
```

用途：LPV 模型线性化、控制器构造、在线调度更新和代价函数计算。

#### 路径生成

```text
src/paths/gen\_agv\_ref\_path.m
src/paths/gen\_agv\_theta10\_uniform\_paths.m
src/paths/gen\_factory\_logistics\_showcase\_path.m
src/paths/gen\_closed\_loop\_eval\_paths.m
src/paths/gen\_modern\_tcn\_demo\_path.m
src/paths/gen\_modern\_tcn\_theta\_sweep\_plot\_path.m
src/paths/gen\_modern\_tcn\_theta\_sweep\_short\_paths.m
```

用途：训练路径、展示路径、多路径闭环评估路径和坡度 sweep 评估路径生成。

#### ModernTCN 主方法

```text
src/ModernTCN/modern\_tcn\_model.py
src/ModernTCN/modern\_tcn\_data.py
src/ModernTCN/modern\_tcn\_metrics.py
src/ModernTCN/train\_modern\_tcn.py
src/ModernTCN/run\_modern\_tcn\_theta10\_v2\_multiseed.py
src/ModernTCN/export\_modern\_tcn\_onnx.py
src/ModernTCN/check\_onnxruntime\_consistency.py
src/ModernTCN/ModernTCN\_check\_matlab\_onnx.m
src/ModernTCN/ModernTCN\_default\_config.m
src/ModernTCN/ModernTCN\_load\_predictor.m
src/ModernTCN/ModernTCN\_predict\_window.m
src/ModernTCN/ModernTCN\_online\_step.m
src/ModernTCN/ModernTCN\_state\_classifier.m
src/ModernTCN/ModernTCN\_State\_Classifier\_sim.m
src/ModernTCN/ModernTCN\_analyze\_closed\_loop\_out.m
src/ModernTCN/ModernTCN\_replay\_closed\_loop\_yraw.m
src/ModernTCN/plot\_modern\_tcn\_theta\_scatter.m
src/ModernTCN/eval\_modern\_tcn\_theta\_sweep\_plot.m
```

用途：ModernTCN 模型定义、数据读取、训练、指标计算、ONNX 导出、一致性检查、MATLAB 在线推理、Simulink 包装和结果分析。

#### 对照算法与闭环比较

根据申请名称，GRU/TCN 可以作为“对照与验证模块”纳入源代码材料，但不要在说明书中把它们描述成主创新算法。

```text
src/gru/GRU\_train.m
src/gru/run\_GRU\_train\_theta10\_v2\_multi\_seed.m
src/gru/GRU\_default\_config.m
src/gru/GRU\_infer.m
src/gru/GRU\_state\_classifier.m
src/gru/GRU\_State\_Classifier\_gru\_sim.m
src/gru/GRU\_load\_default\_to\_base.m

src/TCN/TCN\_train.m
src/TCN/run\_TCN\_train\_theta10\_v2\_multi\_seed.m
src/TCN/TCN\_recommended\_cfg.m
src/TCN/TCN\_default\_config.m
src/TCN/TCN\_load\_predictor.m
src/TCN/TCN\_predict\_window.m
src/TCN/TCN\_state\_classifier.m
src/TCN/TCN\_State\_Classifier\_sim.m
src/TCN/configure\_tcn\_simulink\_model.m

src/Compare/run\_closed\_loop\_model\_once.m
src/Compare/compare\_modern\_tcn\_gru\_closed\_loop\_out.m
src/Compare/compare\_tcn\_gru\_modern\_closed\_loop\_out.m
src/Compare/run\_lpvmpc\_theta\_baseline\_experiment.m
src/Compare/run\_multi\_path\_closed\_loop\_benchmark.m
src/Compare/run\_closed\_loop\_robustness\_experiment.m
src/Compare/benchmark\_modern\_tcn\_onnx\_runtime.py
src/Compare/run\_realtime\_benchmark.m
```

用途：基线训练、闭环对比、多路径闭环、扰动鲁棒性、实时性测试。

#### 测试代码

```text
src/tests/test\_simulink\_closed\_loop.m
src/tests/test\_GRU\_workflow.m
src/tests/test\_gru\_performance.m
src/tests/test\_gru\_latency.m
src/tests/test\_gru\_filter\_constants.m
src/tests/test\_agv\_open\_loop.m
src/tests/test\_industrial\_open\_loop\_items.m
```

用途：验证初始化、开环仿真、闭环加载、分类器推理、GRU 工作流和延迟测试。

### 4.2 不应纳入源码鉴别材料的内容

请排除：

```text
.git/
.github/
.kilo/
.cursor/
.venv/
\_\_pycache\_\_/
slprj/
tools/tmp\_\*
tools/tmp\_slx\_\*
\*.slxc
\*.asv
\*.autosave
```

请排除或仅作为说明书附件引用，不放入程序源码材料：

```text
data/\*\*/\*.mat
data/\*\*/\*.csv
data/\*\*/\*.json
results/\*\*/\*.mat
results/\*\*/\*.csv
results/\*\*/\*.png
results/\*\*/\*.pt
results/\*\*/\*.onnx
results/\*\*/\*.md
figures/\*\*/\*.png
docs/\*\*/\*.md
\*.pdf
\*.docx
\*.slx
```

说明：

1. `.mat`、`.pt`、`.onnx`、`.slx` 属于数据、权重、模型或二进制工程文件，不适合作为源程序鉴别材料；
2. `results/` 是运行结果，不是源程序；
3. `docs/` 和论文报告不是程序源代码；
4. `generated\_layers/` 可能是 MATLAB ONNX 导入生成代码，若纳入必须在报告中标注为“自动生成兼容层”，建议默认排除；
5. 第三方依赖库、虚拟环境、缓存文件不得纳入申请源码。

\---

## 5\. 源码材料排版要求

### 5.1 生成完整源码汇编文件

生成 `ModernTCN\_AGV\_LPVMPC\_V1\_full\_source.txt`，按以下顺序串联所有被选源文件：

1. 根目录入口；
2. `src/core/`；
3. `src/lpv/`；
4. `src/mpc/`；
5. `src/paths/`；
6. `src/ModernTCN/`；
7. `src/Compare/`；
8. `src/gru/`；
9. `src/TCN/`；
10. `src/tests/`。

每个文件开始处插入文件边界：

```text
// ===== FILE: relative/path/to/file.ext =====
```

MATLAB 文件也可以使用 `% ===== FILE: ... =====`；Python 文件也可以使用 `# ===== FILE: ... =====`。为统一排版，汇编 TXT 中允许统一使用纯文本边界，不改变原始代码文件。

### 5.2 页码与页眉

生成 DOCX/PDF 时，每一页右上角必须标页码。页眉统一为：

```text
AGV工况感知与LPV-MPC闭环控制仿真软件 V1.0
```

若申请人改软件名称，页眉必须同步替换。

### 5.3 每页行数

程序源码页面需保证每页不少于 50 行。建议参数：

```text
纸张：A4
方向：纵向
打印：单面
字体：Consolas 或 Courier New
字号：8.5 pt 或 9 pt
页边距：上 1.5 cm，下 1.5 cm，左 1.8 cm，右 1.5 cm
行距：固定值 10 pt 左右
每页目标行数：55 行
```

不要插入大量空白页。不要让单页只有几十行注释。不要在源码材料中插入说明书正文。

### 5.4 前30页与后30页抽取

若完整源码汇编排版后大于 60 页，请生成：

```text
ModernTCN\_AGV\_LPVMPC\_V1\_source\_front30\_back30.\*
```

内容为完整源码汇编排版后的：

```text
第 1-30 页 + 最后 30 页
```

中间不连续部分用一页“抽取说明页”是不建议的，因为官方要求是前、后各连续 30 页。请直接把前 30 页和后 30 页合并成 60 页，并保持原页码或重新编页均可；建议重新编页为 1-60，同时在 `source\_selection\_report.md` 中记录其来源为完整源码的前后各 30 页。

若完整源码不足 60 页，则提交全部源码，文件名改为：

```text
ModernTCN\_AGV\_LPVMPC\_V1\_source\_all.\*
```

### 5.5 代码文件索引

生成 `source\_file\_index.csv`，字段如下：

```text
order,relative\_path,language,lines,include\_status,module,reason
```

`include\_status` 取值：

```text
included
excluded\_binary\_or\_data
excluded\_result
excluded\_cache
excluded\_third\_party
missing
```

\---

## 6\. 软件设计说明书生成要求

请生成 `ModernTCN\_AGV\_LPVMPC\_V1\_软件设计说明书.md/docx/pdf`。说明书必须是中文，建议 60 页左右，至少满足“作为文档鉴别材料提交时格式清晰、每页不少于 30 行”的要求。若最终文档不足 60 页，也可以提交全文，但应尽量内容完整。

### 6.1 排版要求

```text
纸张：A4
方向：纵向
打印：单面
正文：宋体，小四或五号
英文/代码/路径：Consolas 或等宽字体
行距：固定值 20 磅或 1.25 倍
页眉：AGV工况感知与LPV-MPC闭环控制仿真软件 V1.0
页脚或右上角：页码
图表：黑白可读
```

### 6.2 说明书目录结构

请按以下目录生成，不要只写空标题。每章都要结合仓库实际文件、实际模块和实际功能写具体内容。

```text
封面
修订记录
目录

第1章 软件概述
  1.1 软件名称、简称与版本
  1.2 开发背景
  1.3 软件目标
  1.4 适用对象与应用场景
  1.5 软件边界

第2章 运行环境
  2.1 硬件环境
  2.2 软件环境
  2.3 开发语言与依赖
  2.4 输入输出文件环境
  2.5 目录结构说明

第3章 总体架构
  3.1 系统总体架构
  3.2 功能模块划分
  3.3 数据流与控制流
  3.4 离线训练与在线闭环关系
  3.5 Simulink 与 MATLAB/Python 协同方式

第4章 数据与路径生成模块
  4.1 参考路径生成
  4.2 训练数据生成
  4.3 数据窗口化
  4.4 数据契约
  4.5 19维输入特征
  4.6 主工况、转向方向与坡度标签

第5章 AGV模型与LPV-MPC控制模块
  5.1 AGV车辆模型
  5.2 状态方程和输出方程
  5.3 参考模型
  5.4 LPV线性化
  5.5 MPC控制器构造
  5.6 在线调度更新
  5.7 控制代价与约束处理

第6章 ModernTCN工况感知模块
  6.1 模块定位
  6.2 输入输出定义
  6.3 ModernTCN-small网络结构
  6.4 大核深度卷积残差块
  6.5 多任务输出头
  6.6 窗口统计特征融合
  6.7 坡度输出调理与调度约束
  6.8 ONNX导出与部署

第7章 训练、评估与模型导出
  7.1 训练入口
  7.2 多seed训练流程
  7.3 损失函数和指标
  7.4 checkpoint保存
  7.5 ONNX一致性检查
  7.6 MATLAB端一致性检查

第8章 Simulink闭环仿真模块
  8.1 闭环模型组成
  8.2 预加载函数
  8.3 在线预测流程
  8.4 LPV-MPC更新流程
  8.5 闭环输出保存
  8.6 仿真异常处理

第9章 对照算法与基线模块
  9.1 GRU基线
  9.2 TCN基线
  9.3 LPV-MPC theta0基线
  9.4 IMU theta基线
  9.5 true-theta oracle上界
  9.6 对照模块的作用边界

第10章 实验、报告与验证模块
  10.1 三算法闭环对比
  10.2 多路径闭环实验
  10.3 扰动鲁棒性实验
  10.4 实时性测试
  10.5 测试脚本
  10.6 输出报告

第11章 用户使用说明
  11.1 初始化项目
  11.2 加载默认ModernTCN配置
  11.3 运行离线训练
  11.4 导出ONNX模型
  11.5 运行闭环仿真
  11.6 运行对比实验
  11.7 查看结果
  11.8 常见问题

第12章 技术特点
  12.1 面向AGV闭环控制的多任务时序感知
  12.2 LPV-MPC与深度时序模型协同
  12.3 统一数据契约与公平对照
  12.4 ONNX/MATLAB/Simulink跨环境部署
  12.5 多路径、扰动和实时性验证

第13章 数据安全与维护
  13.1 本地数据处理
  13.2 文件管理
  13.3 结果可追溯
  13.4 版本维护

第14章 版本说明
  14.1 V1.0功能范围
  14.2 后续扩展方向

附录A 主要源码文件清单
附录B 主要输入输出文件清单
附录C 关键参数表
附录D 术语表
```

### 6.3 说明书必须写入的项目事实

必须写入以下事实，不得泛泛而谈：

1. 软件面向 **diagonal dual steer drive AGV**，主动驱动/转向轮为 `LF` 和 `RR`，被动支撑轮为 `RF` 和 `LR`；
2. 采样周期 `Ts = 0.01 s`，输入窗口长度 `seq\_len = 128`，输入维度 `input\_dim = 19`；
3. 19 个输入特征为：

```text
accel\_x
gyro\_z
I\_lf
I\_rr
omega\_wheel\_lf
omega\_wheel\_rr
delta\_lf
delta\_rr
gyro\_y
v\_hat
dv\_hat\_dt
ws\_imbalance
I\_sum
I\_diff\_signed
I\_diff\_abs
accel\_x\_lp
kappa\_proxy
accel\_per\_current
pitch\_angle\_est
```

4. 主工况分类标签为 `flat=1`、`stall=2`、`slope=3`；
5. 转向方向分类标签为 `right=-1`、`straight=0`、`left=1`；
6. 数据划分策略为 `run\_level\_no\_window\_leakage`；
7. scaler 策略为 `fit\_train\_only\_apply\_val\_test\_online`；
8. 当前默认 ModernTCN 部署模型使用 seed 21，配置包括：

```text
run\_tag = modern\_tcn\_theta10\_uniform\_h0\_v2\_seed21
seq\_len = 128
input\_dim = 19
channels = 64
blocks = 5
kernel\_size = 31
temporal\_padding = same
dropout = 0.15
expansion = 2
ONNX = results/modern\_tcn/modern\_tcn\_theta10\_uniform\_h0\_v2\_seed21/modern\_tcn\_seed21.onnx
```

9. ModernTCN 模型输出为：

```text
logits\_main: 3维主工况分类logits
logits\_turn: 3维转向方向分类logits
theta\_hat: 1维坡度/调度量回归输出
```

10. Simulink 闭环主模型包括：

```text
simulink/LPVMPC\_AGV\_simulink\_Modern\_TCN.slx
simulink/LPVMPC\_AGV\_simulink\_GRU.slx
simulink/LPVMPC\_AGV\_simulink\_TCN.slx
simulink/LPVMPC\_AGV\_simulink\_IMU.slx
```

11. 核心控制模块包括 `src/core`、`src/lpv`、`src/mpc`，核心感知模块为 `src/ModernTCN`，核心对比验证模块为 `src/Compare`；
12. 说明书中可以写闭环结果和实时性结果，但不要夸大为已完成嵌入式硬实时部署。应表述为：ONNXRuntime+MPC 核心链路满足 10 ms 控制周期的计算余量；MATLAB/Simulink extrinsic 封装主要用于桌面仿真验证。

### 6.4 说明书语言风格

应使用软著说明书风格，不要写成论文。示例风格：

```text
本软件提供面向对角双转向驱动AGV的工况感知、LPV-MPC调度控制与闭环仿真验证功能。软件通过路径生成、车辆模型仿真、时序数据窗口化、ModernTCN多任务预测、ONNX模型导出、MATLAB在线推理和Simulink闭环仿真等模块，实现从离线训练到在线控制验证的完整流程。
```

避免以下表达：

```text
本文提出……
本文证明……
实验表明本文方法……
审稿人……
论文第X节……
```

改成：

```text
本软件实现……
本模块用于……
该功能支持……
验证结果用于评估……
```

\---

## 7\. 申请表字段草稿生成要求

生成 `application\_fields\_draft.md`，包含以下字段草稿。无法确定的信息使用 `\[申请人填写]`，不要编造。

```text
软件全称：AGV工况感知与LPV-MPC闭环控制仿真软件
软件简称：AGV-MTCN-MPC仿真软件
版本号：V1.0
开发完成日期：\[申请人填写]
首次发表日期：\[未发表/申请人填写]
软件分类：\[建议：工业控制软件/仿真分析软件/人工智能应用软件，最终以系统选项为准]
开发方式：\[独立开发/合作开发/委托开发/职务开发，申请人确认]
权利取得方式：\[原始取得/继受取得，申请人确认]
编程语言：MATLAB、Python
源程序量：\[Codex统计纳入源码的有效代码行数后填写]
硬件环境：普通PC工作站或具备MATLAB/Simulink和Python深度学习环境的计算机；建议CPU多核、内存16GB及以上；如使用GPU训练，可选NVIDIA GPU。
软件环境：Windows 10/11 或兼容桌面操作系统；MATLAB/Simulink；Python；PyTorch；ONNXRuntime；必要时包含MATLAB Deep Learning Toolbox、Model Predictive Control Toolbox等。
主要功能：AGV车辆模型仿真、参考路径生成、LPV线性化、MPC控制器构建、ModernTCN工况感知、坡度调度量预测、ONNX导出、MATLAB在线推理、Simulink闭环仿真、对照算法评估、多路径与扰动鲁棒性验证、实时性测试。
技术特点：面向AGV闭环控制的多任务时序感知，结合大核深度时序卷积、LPV-MPC在线调度、统一数据契约、ONNX跨环境部署和闭环评价流程，实现工况识别、转向识别、坡度回归与控制仿真的一体化。
```

另生成一段 300-500 字的软件功能说明，用于申请表复制：

```text
本软件面向对角双转向驱动AGV的工况感知与闭环控制仿真需求，提供从路径生成、车辆建模、训练数据构建、时序神经网络训练到LPV-MPC闭环仿真的完整工具链。软件以MATLAB/Simulink为车辆模型与控制仿真平台，以Python/PyTorch实现ModernTCN多任务时序感知模型，通过128步、19维观测窗口识别AGV主工况、转向方向并回归坡度调度量。软件支持将训练模型导出为ONNX，并在MATLAB端完成在线预测和Simulink闭环调用。系统还提供GRU、TCN、无AI坡度基线和真实坡度上界等对照流程，支持离线指标评估、闭环轨迹跟踪评价、多路径鲁棒性实验、扰动鲁棒性实验和实时性测试，便于对AGV在坡道、转向和异常工况下的控制性能进行可复现验证。
```

\---

## 8\. 技术特点摘要生成要求

生成 `technical\_feature\_summary.md`，包含以下内容：

### 8.1 主要功能点

1. 项目初始化与路径管理；
2. AGV车辆模型仿真；
3. LPV线性化与MPC控制器构建；
4. 参考路径和训练路径生成；
5. 统一时序数据集构建；
6. ModernTCN多任务工况感知；
7. ONNX模型导出与一致性验证；
8. MATLAB在线推理与Simulink闭环调用；
9. GRU/TCN/LPV-MPC基线对照；
10. 多路径、扰动鲁棒性和实时性评价。

### 8.2 技术创新/特点表述

请写成软件实现特点，不要写成专利式或论文式创新点：

```text
（1）软件将AGV动态模型、LPV-MPC控制器和ModernTCN时序感知模型组织为统一闭环仿真流程，实现工况识别、转向识别和坡度调度量回归的协同使用。
（2）软件采用固定长度时序窗口和19维可观测特征构建输入数据，并通过run级数据划分和训练集拟合scaler策略降低数据泄漏风险。
（3）软件的ModernTCN模块采用大核深度时序卷积、通道混合和残差结构，输出主工况、转向方向和坡度回归三类结果。
（4）软件支持将PyTorch模型导出为ONNX格式，并在MATLAB/Simulink闭环模型中加载使用，形成跨语言部署链路。
（5）软件提供三算法闭环对比、多路径闭环实验、扰动鲁棒性实验和实时性测试，支持对控制性能进行可复现评估。
```

\---

## 9\. 第三方、数据与排除说明

生成 `third\_party\_and\_exclusion\_statement.md`。至少包含：

1. 本次源码鉴别材料仅从申请人仓库中的 MATLAB/Python 源文件中选择；
2. 未纳入虚拟环境、第三方库源码、缓存文件、训练数据、模型权重、ONNX文件、MAT文件、图片、论文图表和自动生成临时文件；
3. PyTorch、ONNXRuntime、MATLAB/Simulink 等作为运行环境或依赖工具出现，不作为本软件申请的自有源代码；
4. 若仓库中存在基于公开算法思想实现的模块，材料中应描述为“软件实现了面向AGV场景的工程化时序感知与闭环控制流程”，不要声称第三方基础框架或基础算法归申请人所有；
5. 申请人应最终确认是否包含外部开源代码、合作开发代码、导师/学校/单位职务成果等权属问题。

\---

## 10\. 一致性检查

生成 `consistency\_check\_report.md`，检查以下项目：

```text
\[ ] 所有材料中的软件名称一致
\[ ] 所有材料中的版本号一致
\[ ] 源码页眉与申请表软件名称一致
\[ ] 设计说明书页眉与申请表软件名称一致
\[ ] 源程序每页不少于50行
\[ ] 文档每页不少于30行（含图页除外）
\[ ] 源程序右上角或页脚有页码
\[ ] 文档右上角或页脚有页码
\[ ] 源码材料未包含第三方库、虚拟环境、缓存和二进制文件
\[ ] 说明书未写成论文口吻
\[ ] 说明书中的功能与实际仓库文件对应
\[ ] 申请表字段中的开发完成日期、首次发表日期、权利取得方式已由申请人确认
\[ ] 如果软件已公开发表，首次发表日期与公开记录一致
\[ ] 如果软件未发表，申请表填写“未发表”或按官方系统选项填写
\[ ] 如果存在合作/委托/职务开发，已准备对应证明文件
```

\---

## 11\. Codex执行步骤

### 步骤1：扫描仓库

1. 遍历仓库文件；
2. 根据第4章规则筛选源代码；
3. 统计每个文件行数、语言、所属模块；
4. 生成 `source\_file\_index.csv` 和 `source\_selection\_report.md`。

### 步骤2：生成源码汇编

1. 按指定模块顺序拼接源码；
2. 插入文件边界；
3. 生成完整 TXT；
4. 排版生成 DOCX/PDF；
5. 若超过 60 页，抽取前30页和后30页；
6. 检查每页行数、页眉、页码。

### 步骤3：生成设计说明书

1. 读取 `PROJECT\_AI\_CONTEXT.md`、`PROJECT\_FLOW\_MANIFEST.md`、数据契约 JSON、默认配置文件和核心源码；
2. 按第6章目录生成中文说明书；
3. 说明书必须包含架构图或文字版架构图。若不画图，请用 ASCII 图或表格描述；
4. 输出 MD、DOCX、PDF 三种格式；
5. 检查名称、版本和页码一致性。

### 步骤4：生成申请表辅助内容

1. 生成 `application\_fields\_draft.md`；
2. 源程序量由实际纳入源码行数统计；
3. 对无法确定字段标注 `\[申请人填写]`；
4. 不要编造申请人姓名、身份证号、单位、完成日期、发表日期。

### 步骤5：生成最终检查清单

1. 汇总材料；
2. 报告缺失文件；
3. 报告疑似第三方/自动生成/二进制文件；
4. 给出最终提交前人工确认事项。

\---

## 12\. 设计说明书中的模块映射表模板

请在说明书附录中生成如下表：

|模块|主要文件|功能说明|输入|输出|
|-|-|-|-|-|
|项目初始化|init\_project.m, project\_root.m, results\_dir.m|设置路径与结果目录|项目根目录|MATLAB搜索路径、结果路径|
|车辆模型|src/core/\*.m|AGV动力学与输出计算|状态、控制量、参数|状态导数、输出量|
|LPV线性化|src/lpv/\*.m|建立调度点线性模型|AGV状态点、参数|LPV网格模型|
|MPC控制|src/mpc/\*.m|构造与更新MPC控制器|LPV模型、调度量、约束|控制输入|
|路径生成|src/paths/\*.m|生成训练和闭环路径|路径参数|ref结构、路径mat文件|
|ModernTCN训练|src/ModernTCN/\*.py|训练多任务时序模型|数据集mat文件|checkpoint、指标、ONNX|
|ModernTCN部署|src/ModernTCN/\*.m|MATLAB端加载和在线预测|ONNX模型、在线窗口|工况、转向、坡度输出|
|Simulink闭环|simulink/*.slx, preloadfcn*.m|闭环控制仿真|控制器、模型、路径|logsout、闭环结果|
|对照实验|src/gru, src/TCN, src/Compare|基线训练与闭环对比|统一数据集、路径|指标表、报告|
|测试验证|src/tests/\*.m|流程检查和性能测试|模型与配置|测试报告|

\---

## 13\. 用户手册短版要求

生成 `user\_manual\_short.md`，内容包括：

```text
1. 软件简介
2. 环境准备
3. 初始化项目
4. 生成/检查数据集
5. 训练ModernTCN
6. 导出ONNX
7. 加载Simulink闭环模型
8. 运行闭环仿真
9. 运行对照实验
10. 查看输出文件
11. 常见问题
```

命令示例可以使用占位形式：

```matlab
init\_project;
cfg = ModernTCN\_default\_config(project\_root());
load\_system('simulink/LPVMPC\_AGV\_simulink\_Modern\_TCN.slx');
```

```bash
python src/ModernTCN/train\_modern\_tcn.py --dataset-file data/tcn/ModernTCN\_dataset\_agv\_dualsteer\_theta10\_uniform\_conf\_h0\_v2.mat
python src/ModernTCN/export\_modern\_tcn\_onnx.py --run-tag modern\_tcn\_theta10\_uniform\_h0\_v2\_seed21
```

如果实际脚本参数不同，请以源码中的 argparse 或函数定义为准，不要硬编不存在的参数。

\---

## 14\. 最终输出要求

Codex 完成后，在终端输出：

```text
软著申请材料辅助文件已生成：
1. 申请表字段草稿：soft\_copyright\_application/00\_application\_info/application\_fields\_draft.md
2. 源码鉴别材料：soft\_copyright\_application/01\_source\_code\_material/ModernTCN\_AGV\_LPVMPC\_V1\_source\_front30\_back30.pdf
3. 软件设计说明书：soft\_copyright\_application/02\_software\_document/ModernTCN\_AGV\_LPVMPC\_V1\_软件设计说明书.pdf
4. 用户手册短版：soft\_copyright\_application/03\_auxiliary\_materials/user\_manual\_short.md
5. 一致性检查报告：soft\_copyright\_application/04\_compliance\_check/consistency\_check\_report.md

请申请人最终确认：软件名称、版本号、著作权人、开发完成日期、首次发表日期、开发方式、权利取得方式及证明文件。
```

不要自动提交任何申请。不要上传个人身份材料。不要把申请人的身份证、营业执照、公章等敏感材料写入仓库。

\---

## 15\. 人工最终确认清单

申请人提交前必须确认：

1. 软件名称是否最终确定；
2. 版本号是否统一为 V1.0；
3. 著作权人是谁；
4. 是否属于学校/单位职务成果；
5. 是否有合作开发人；
6. 是否需要单位盖章或个人签字；
7. 开发完成日期是否真实；
8. 首次发表日期是否真实，若未发表则按未发表处理；
9. GitHub公开仓库是否构成首次发表，若构成则日期应与公开记录一致；
10. 仓库是否包含他人开源代码；
11. 是否需要补充合作开发协议、任务书、委托合同或权属证明；
12. 生成的源程序与文档页眉软件名称是否与申请表完全一致。

