# 源码选择报告

生成日期：2026-05-25

## 1. 选择原则

本次程序鉴别材料采用白名单方式，从当前仓库中选择与“AGV工况感知与LPV-MPC闭环控制仿真软件 V1.0”直接相关的 MATLAB/Python 源文件。选择范围覆盖项目初始化、AGV 车辆模型、LPV 线性化、MPC 控制器、参考路径生成、ModernTCN 多任务工况感知、ONNX 导出与 MATLAB/Simulink 在线推理、GRU/TCN 对照实验、闭环比较和测试验证脚本。

未纳入虚拟环境、第三方库源码、缓存目录、训练数据、模型权重、ONNX 文件、MAT 文件、图片、论文图表、PDF/DOCX 文档和 Simulink 二进制模型。Simulink `.slx` 模型作为软件运行环境和闭环平台在说明书中引用，不作为源程序文本纳入。

## 2. 纳入统计

| 项目 | 数值 |
|---|---:|
| 纳入源文件数量 | 78 |
| 纳入源码行数 | 25939 |
| 完整源码汇编估算页数 | 522 |
| 抽取源码页数 | 70 |
| 每页目标行数 | 50 |

## 3. 抽取说明

完整源码约 522 页，抽取完整源码排版后的第 1-35 页和最后 35 页。

生成的完整源码汇编文件为：

- `soft_copyright_application/01_source_code_material/ModernTCN_AGV_LPVMPC_V1_full_source.txt`

生成的提交用源码鉴别材料为：

- `soft_copyright_application/01_source_code_material/ModernTCN_AGV_LPVMPC_V1_source_front35_back35.txt`
- `soft_copyright_application/01_source_code_material/ModernTCN_AGV_LPVMPC_V1_source_front35_back35.docx`
- `soft_copyright_application/01_source_code_material/ModernTCN_AGV_LPVMPC_V1_source_front35_back35.pdf`

## 4. 缺失文件

无。

## 5. 排除说明

- `.git/`、`.github/`、`.kilo/`、`.cursor/`、`.venv/`、`__pycache__/`、`slprj/` 和 Simulink 缓存文件属于环境、缓存或平台配置，不纳入源程序。
- `data/`、`results/`、`figures/` 下的数据、模型、图表、报告和中间结果不作为源程序鉴别材料。
- `.mat`、`.pt`、`.onnx`、`.slx`、`.slxc`、`.pdf`、`.docx` 等文件属于数据、模型、二进制工程文件或文档，不作为源程序文本。
- `src/ModernTCN/generated_layers/` 为 MATLAB 导入 ONNX 后产生的兼容层代码，默认标注为自动生成兼容层，不纳入本次核心源码。
- `src/pic&table/` 下脚本主要用于论文图表生成，与软著申请的软件主体功能不同，未纳入程序鉴别材料。
