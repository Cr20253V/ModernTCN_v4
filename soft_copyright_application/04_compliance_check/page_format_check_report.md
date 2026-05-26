# 页面格式检查报告

生成日期：2026-05-25

## 1. 检查结论

已通过 Microsoft Word COM 导出 PDF。

## 2. 源程序材料

| 项目 | 检查结果 |
|---|---|
| 源码排版文件 | `soft_copyright_application/01_source_code_material/ModernTCN_AGV_LPVMPC_V1_source_front35_back35.docx` |
| 源码 PDF | `soft_copyright_application/01_source_code_material/ModernTCN_AGV_LPVMPC_V1_source_front35_back35.pdf` |
| 完整源码估算页数 | 522 |
| 提交版页数 | 70 |
| 每页目标行数 | 50 |
| 字体与字号 | Consolas，小字号紧凑排版 |
| 行距 | 固定紧凑行距 |
| 页眉/页脚 | 页眉左侧为 `AGV 工况感知与 LPV-MPC 闭环控制仿真软件`，右上角为“第 x 页 共 y 页”，页眉页脚均有横线 |
| 左侧标号 | 源码材料按页生成 1-50 行号 |

源程序 DOCX 由生成脚本按每页 50 行插入分页符，满足每页不少于 50 行的排版目标。完整源码超过提交页数，因此提交版由完整源码前 35 页和后 35 页组成，页数多于传统 60 页以提升可读性和材料余量。

## 3. 设计说明书

| 项目 | 检查结果 |
|---|---|
| 说明书 DOCX | `soft_copyright_application/02_software_document/ModernTCN_AGV_LPVMPC_V1_软件设计说明书.docx` |
| 说明书 PDF | `soft_copyright_application/02_software_document/ModernTCN_AGV_LPVMPC_V1_软件设计说明书.pdf` |
| Word 统计页数 | 20 |
| 页眉/页脚 | 页眉左侧为 `AGV 工况感知与 LPV-MPC 闭环控制仿真软件`，右上角为“第 x 页 共 y 页”，页眉页脚均有横线 |
| 正文字体 | 宋体/Arial 兼容设置，小四到五号区间 |
| 行距 | 正文约 1.25 倍行距 |


## 4. PDF抽样渲染检查

已使用 `pdftoppm` 抽样渲染源码 PDF 首页、抽取衔接页、末页和说明书 PDF 第 1、末页，并进行了非空像素检查。详见 `soft_copyright_application/04_compliance_check/pdf_render_qa_report.md`。


## 5. 待人工抽检事项

- [ ] 打开源码 PDF，确认前 35 页和后 35 页连续、页码正常、无空白页。
- [ ] 打开说明书 PDF，确认标题、表格、代码块和页眉页码显示正常。
- [ ] 若提交系统对页码位置、页边距或行数有地方性要求，应按受理机构要求微调。
- [ ] 本脚本使用 Microsoft Word 导出 PDF，并使用 `pdftoppm` 做抽样渲染非空检查；最终提交前仍建议人工打开 PDF 逐页检查。
