# AGV 模型参数修正计划包索引

本目录用于集中管理 AGV 模型参数修正流程的计划文档、阶段报告、快照、结果副本清单和最终交接材料。

## 目录结构

- `agv_model_parameter_correction_plan.md`：主计划文档。
- `01_baseline/`：旧模型基线快照和旧结果路径记录。
- `04_lpv_database/`：LPV 数据库重建报告和数据库副本记录。
- `06_mpc_retuning/`：MPC 可行性检查、调参报告和 `maps_best.mat` 副本记录。
- `07_dataset/`：数据集重建报告和 contract/scaler 记录。
- `08_models/`：模型重训、checkpoint、ONNX 和一致性检查记录。
- `09_closed_loop/`：主闭环、多路径和鲁棒性重跑报告。
- `11_figures_tables/`：论文图片、源数据和表格刷新记录。
- `15_final_handoff/`：最终总结和后续交接文档。
- `logs/`：执行日志、命令记录和临时检查记录。

## 路径原则

- 工程脚本依赖的 canonical artifact 仍放在原位置，例如 `data/models/lin_agv_db.mat`、`data/models/maps_best.mat`、`results/compare/...`。
- 本目录保存计划、报告、快照、清单和必要副本，避免打乱现有脚本路径。
