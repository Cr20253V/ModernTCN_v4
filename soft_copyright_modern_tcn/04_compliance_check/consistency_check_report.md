# 一致性检查报告

生成日期：2026-05-25

## 1. 自动检查项目

- [x] 软件全称在所有材料中一致：`基于 ModernTCN 的 AGV 工况感知与坡度调度软件`
- [x] 版本号均为 `V1.0`
- [x] 页眉包含软件全称和 V1.0
- [x] 源码材料为 front30/back30，不是 front35/back35
- [x] 源程序按每页 50 行分页，满足每页不少于 50 行的目标
- [x] 文档页面满足每页不少于 30 行的目标
- [x] ModernTCN 核心源码占源码材料主体（22 个文件，5267 行）
- [x] GRU/TCN 源码没有占据 ModernTCN 申请包主体
- [x] .pt/.onnx/.mat/.slx 未纳入源程序鉴别材料
- [x] generated_layers 未作为自有核心源码纳入
- [x] 说明书采用"本软件/本模块"表述，未写成论文口吻
- [x] 说明书明确 AGV/LPV-MPC/Simulink 为验证环境或接口环境
- [x] 源码 DOCX/PDF 和说明书 DOCX/PDF 已生成

## 2. 人工确认项目

- [ ] 申请表字段中的著作权人已由申请人确认
- [ ] 开发完成日期已由申请人确认
- [ ] 首次发表日期已由申请人确认
- [ ] 开发方式已由申请人确认
- [ ] 权利取得方式已由申请人确认
- [ ] 如果软件已公开发表，首次发表日期与公开记录一致
- [ ] 如果软件未发表，申请表填写"未发表"或按官方系统选项填写
- [ ] 如果存在合作/委托/职务开发，已准备对应证明文件
- [ ] 申请人已确认 GitHub 公开仓库是否构成首次发表
- [ ] 申请人已确认仓库是否包含他人开源代码或单位职务成果
- [ ] ModernTCN 申请包与 GRU 申请包的源码边界已确认

## 3. 生成物摘要

| 项目 | 路径 |
|---|---|
| 申请表字段草稿 | `soft_copyright_modern_tcn/00_application_info/application_fields_draft.md` |
| 软件名称备选 | `soft_copyright_modern_tcn/00_application_info/software_name_options.md` |
| 权属确认清单 | `soft_copyright_modern_tcn/00_application_info/ownership_confirm_checklist.md` |
| 材料边界声明 | `soft_copyright_modern_tcn/00_application_info/material_boundary_statement.md` |
| 源码索引 | `soft_copyright_modern_tcn/01_source_code_material/source_file_index.csv` |
| 源码选择报告 | `soft_copyright_modern_tcn/01_source_code_material/source_selection_report.md` |
| 完整源码 | `soft_copyright_modern_tcn/01_source_code_material/ModernTCN_AGV_Perception_V1_full_source.txt` |
| 源码提交版 | `soft_copyright_modern_tcn/01_source_code_material/ModernTCN_AGV_Perception_V1_source_front30_back30.docx` |
| 源码提交版 PDF | `soft_copyright_modern_tcn/01_source_code_material/ModernTCN_AGV_Perception_V1_source_front30_back30.pdf` |
| 设计说明书 | `soft_copyright_modern_tcn/02_software_document/ModernTCN_AGV_Perception_V1_软件设计说明书.docx` |
| 设计说明书 PDF | `soft_copyright_modern_tcn/02_software_document/ModernTCN_AGV_Perception_V1_软件设计说明书.pdf` |
| 技术特点摘要 | `soft_copyright_modern_tcn/03_auxiliary_materials/technical_feature_summary.md` |
| 与 GRU 包边界 | `soft_copyright_modern_tcn/03_auxiliary_materials/difference_from_gru_application.md` |
| 输入输出契约 | `soft_copyright_modern_tcn/03_auxiliary_materials/input_output_contract.md` |
| 第三方排除说明 | `soft_copyright_modern_tcn/03_auxiliary_materials/third_party_and_exclusion_statement.md` |
| 用户手册短版 | `soft_copyright_modern_tcn/03_auxiliary_materials/user_manual_short.md` |
| 模块映射表 | `soft_copyright_modern_tcn/03_auxiliary_materials/module_mapping_table.csv` |

## 4. 源码统计

- 纳入核心源文件数量：22
- 纳入核心源码行数：5267
- 完整源码汇编页数：107（按每页 50 行）
- 提交源码页数：60（front30 + back30）
- 排除文件类型：.pt, .onnx, .mat, .slx, .slxc, .png, .csv, .md, .pdf, .docx
- 排除目录：.git, .github, .kilo, .cursor, .venv, __pycache__, slprj, data, results, figures, docs

## 5. 软件名称一致性

| 材料 | 软件全称 | 版本号 |
|---|---|---|
| 申请表字段草稿 | 基于 ModernTCN 的 AGV 工况感知与坡度调度软件 | V1.0 |
| 软件名称备选 | 基于 ModernTCN 的 AGV 工况感知与坡度调度软件 | V1.0 |
| 设计说明书 | 基于 ModernTCN 的 AGV 工况感知与坡度调度软件 | V1.0 |
| 源码页眉 | 基于 ModernTCN 的 AGV 工况感知与坡度调度软件 V1.0 | - |
| 说明书页眉 | 基于 ModernTCN 的 AGV 工况感知与坡度调度软件 V1.0 | - |
