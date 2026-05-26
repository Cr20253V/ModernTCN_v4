# 申请表字段草稿

> 说明：以下内容为软著申请表辅助草稿，无法从仓库确定的权属、日期和主体信息均保留为 `[申请人填写]`，不得由生成脚本自行编造。

软件全称：基于 ModernTCN 的 AGV 工况感知与坡度调度软件

软件简称：ModernTCN-AGV 感知调度软件

版本号：V1.0

开发完成日期：[申请人填写]

首次发表日期：[未发表/申请人填写]

软件分类：[建议：人工智能应用软件/工业控制软件/仿真分析软件，最终以系统选项为准]

开发方式：[独立开发/合作开发/委托开发/职务开发，申请人确认]

权利取得方式：[原始取得/继受取得，申请人确认]

编程语言：Python、MATLAB

源程序量：约 5267 行（按本次核心源码汇编 TXT 统计，含文件边界标记、注释和空行；正式填报前可按官方系统口径复核）

硬件环境：普通 PC 工作站或具备 MATLAB/Simulink 和 Python 深度学习环境的计算机；建议 CPU 多核、内存 16GB 及以上；如使用 GPU 训练，可选 NVIDIA GPU。

软件环境：Windows 10/11 或兼容桌面操作系统；Python 3.8+；PyTorch；ONNXRuntime；MATLAB/Simulink；必要时包含 MATLAB Deep Learning Toolbox、Statistics and Machine Learning Toolbox 等。

主要功能：ModernTCN 多任务时序感知模型定义与训练、统一数据契约与数据加载、多 seed 训练与指标汇总、ONNX 模型导出、ONNXRuntime 一致性验证、MATLAB 端 ONNX 一致性检查、MATLAB 在线窗口维护与预测、状态分类器、Simulink 接口封装、坡度调度量输出与闭环验证接口。

技术特点：面向 AGV 的大核深度时序卷积多任务感知，结合 128 步 19 维输入窗口、三任务输出（主工况分类、转向方向分类、坡度回归）、统一数据契约、run 级防泄漏划分、跨 Python/MATLAB ONNX 部署和面向 LPV-MPC 调度验证的 theta 输出调理。

## 300-500字软件功能说明

本软件面向对角双转向驱动AGV的工况感知与坡度调度需求，提供基于ModernTCN的多任务时序感知、模型训练、模型导出、在线推理和闭环验证接口。软件以128步、19维传感观测窗口作为输入，完成主工况识别、转向方向分类和坡度/调度量回归，输出logits_main、logits_turn和theta_hat等结果。软件支持使用统一数据契约进行数据加载、训练集拟合scaler、run级数据划分和多seed训练，能够生成训练指标、历史曲线和模型报告。软件可将PyTorch训练得到的ModernTCN模型导出为ONNX格式，并提供ONNXRuntime一致性检查、MATLAB端ONNX一致性检查、MATLAB在线预测、状态分类器和Simulink包装接口。AGV车辆模型、LPV-MPC和Simulink闭环模型在本软件中作为验证平台和接口环境，用于检查ModernTCN感知输出在闭环控制场景中的可调用性和稳定性。本软件不包含第三方深度学习框架源码、训练数据权属证明、模型权重源程序或申请人身份证明材料。
