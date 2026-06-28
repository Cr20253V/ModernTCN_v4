# 18 Fair 10-Seed Selection and Final Test Recut Recipe

本目录记录一次重新裁剪训练 recipe 后的公平十种子选模与闭环验证实验。目标是在不覆盖 `17_fair_10seed_selection_and_final_test` 既有结果的前提下，用更接近 `16_recipe_vs_deployment_comparison` 中 uncertainty seed101 rerun 的训练参数，重新比较：

- `ModernTCN_small`
- `Uncertainty-weighted ModernTCN_small`

核心结论：

- 两个算法最终都选出 `seed101`。
- 离线硬筛阶段，`Uncertainty-weighted ModernTCN_small seed101` 的 `offline_v2_score` 最低。
- validation sentinel 阶段，`ModernTCN_small seed101` 的平均 `J_control` 略低。
- final test 四条闭环路径综合排名中，`Uncertainty-weighted ModernTCN_small seed101` 更优。

## 目录结构

| 目录 | 作用 | 状态 |
|---|---|---|
| `00_protocol_lock/` | 协议锁定、路径预检、手动训练脚本 | 已完成 |
| `01_train_modern_tcn_small_10seed/` | `ModernTCN_small` 十种子训练输出与汇总 | 已完成 |
| `02_train_uncertainty_weighted_10seed/` | uncertainty-weighted 十种子训练输出与汇总 | 已完成 |
| `03_offline_screen/` | 离线硬筛与例外候选判定 | 已完成 |
| `04_validation_sentinel_closed_loop/` | validation sentinel 闭环验证 | 已完成 |
| `05_seed_selection/` | 每个算法选择最终 seed | 已完成 |
| `06_final_test_closed_loop/` | 最终四路径闭环测试 | 已完成 |
| `09_final_report/` | 最终报告与决策表 | 已完成 |
| `tools/` | 本轮 wrapper runner | 已完成 |

说明：本目录没有独立的 `07` / `08` 节点目录；本轮已执行到 final test 与 final report，最终结论基于离线筛选、validation sentinel、seed selection 和 final test。

## 实验输入与隔离策略

本轮新建目录为：

`results/modern_tcn_metric_rebuild/18_fair_10seed_selection_and_final_test_recut_recipe`

它复用 17 的节点 runner 逻辑，但输出根目录改到 18，因此不会覆盖 17 的已有数据。训练 recipe 改为参考：

`results/modern_tcn_sci_innovation/01_loss_optimization/uncertainty_seed101_rerun_20260622/config.json`

手动训练脚本位于：

- `00_protocol_lock/manual_train_modern_fixed.ps1`
- `00_protocol_lock/manual_train_uncertainty.ps1`

两个脚本均使用 `--device cuda`，并输出到 18 目录内部。

## N0 协议锁定与预检

工作内容：

- 锁定 validation sentinel 路径和 final test 路径。
- 检查路径文件是否存在。
- 检查对应 baseline closed-loop 输出是否存在。
- 确认 validation 和 final test 路径拆分没有混用。
- 生成手动训练脚本。

结果：

- `can_start=true`
- 必需路径和 baseline 输出均存在。
- validation sentinel 使用 2 条路径。
- final test 使用 4 条路径。
- 本轮输出根目录与 17 隔离。

主要产物：

- `00_protocol_lock/preflight_decision.json`
- `00_protocol_lock/protocol_lock.json`
- `00_protocol_lock/runner_preflight_report.md`
- `00_protocol_lock/manual_train_modern_fixed.ps1`
- `00_protocol_lock/manual_train_uncertainty.ps1`

## N1 ModernTCN_small 十种子训练

工作内容：

- 手动执行 `ModernTCN_small` 十个 seed 的训练。
- 每个 seed 输出 checkpoint、ONNX、参考 sample、训练 summary 和 history。
- 训练完成后汇总为统一的 `training_summary.csv`。

训练 seed 集合：

`1, 7, 11, 21, 42, 73, 101, 202, 340, 520`

结果：

- 训练汇总表包含 10 行。
- 后续离线硬筛中，`seed42` 和 `seed101` 通过。

主要产物：

- `01_train_modern_tcn_small_10seed/training_summary.csv`
- `01_train_modern_tcn_small_10seed/modern_fixed_seed*/`

## N2 Uncertainty-weighted ModernTCN_small 十种子训练

工作内容：

- 手动执行 uncertainty-weighted 版本十个 seed 的训练。
- 每个 seed 输出 checkpoint、ONNX、参考 sample、训练 summary 和 history。
- 训练完成后汇总为统一的 `training_summary.csv`。

训练 seed 集合：

`1, 7, 11, 21, 42, 73, 101, 202, 340, 520`

结果：

- 训练汇总表包含 10 行。
- 后续离线硬筛中，只有 `seed101` 通过。

主要产物：

- `02_train_uncertainty_weighted_10seed/training_summary.csv`
- `02_train_uncertainty_weighted_10seed/uncertainty_weighted_seed*/`

## N3 训练结果汇总

工作内容：

- 从两个训练目录读取每个 seed 的训练结果。
- 汇总离线指标、checkpoint 路径、ONNX 路径和训练成功状态。
- 计算每个 seed 的 `offline_v2_score`。

汇总指标包括：

- `acc_main`
- `acc_turn`
- `acc_turn_transition`
- `theta_mae_deg`
- `theta_edge_p95_abs_err`
- `flat_peak_theta_error`
- `flat_recall`
- `stall_recall`
- `slope_recall`
- `offline_v2_score`

`offline_v2_score` 越低越好。对越高越好的指标使用 `baseline / candidate`，对越低越好的指标使用 `candidate / baseline`，再取平均。

结果：

| 算法 | 汇总行数 | 最低 `offline_v2_score` seed | 最低分 |
|---|---:|---:|---:|
| `modern_fixed` | 10 | 101 | 0.980059344576828 |
| `uncertainty_weighted` | 10 | 101 | 0.970838817749306 |

## N4 离线硬筛

工作内容：

- 对两个算法的 20 个训练结果执行统一的 offline hard screen。
- 硬筛阈值不因某个算法表现较差而放宽。
- 若某算法没有任何 seed 通过硬筛，才启用例外机制：按 `offline_v2_score` 选择最多前 3 个作为 `exception_sentinel_candidates`，并标记 `screen_exception_used=true`。本轮没有触发例外机制。

硬筛规则：

| 指标 | 规则 |
|---|---|
| `acc_main` | 不得比 baseline 低超过 `0.03` |
| `stall_recall` | 不得比 baseline 低超过 `0.05` |
| `slope_recall` | 不得比 baseline 低超过 `0.02` |
| `theta_edge_p95_abs_err` | 不得超过 baseline 的 `1.10x` |
| `flat_peak_theta_error` | 不得超过 baseline 的 `1.15x` |

硬筛结果：

| 算法 | 通过 seed | `offline_v2_score` | 是否例外 |
|---|---:|---:|---|
| `modern_fixed` | 42 | 1.01845860927486 | 否 |
| `modern_fixed` | 101 | 0.980059344576828 | 否 |
| `uncertainty_weighted` | 101 | 0.970838817749306 | 否 |

整体统计：

| 算法 | 训练数 | 硬筛通过数 | 硬筛失败数 | 例外候选数 |
|---|---:|---:|---:|---:|
| `modern_fixed` | 10 | 2 | 8 | 0 |
| `uncertainty_weighted` | 10 | 1 | 9 | 0 |

失败 seed 与原因：

| 算法 | seed | `offline_v2_score` | 失败原因 |
|---|---:|---:|---|
| `modern_fixed` | 1 | 1.0585033706208 | `flat_peak_theta_error` |
| `modern_fixed` | 7 | 1.04883129856036 | `theta_edge_p95_abs_err;flat_peak_theta_error` |
| `modern_fixed` | 11 | 1.02434916828023 | `stall_recall;flat_peak_theta_error` |
| `modern_fixed` | 21 | 1.02255495051725 | `theta_edge_p95_abs_err` |
| `modern_fixed` | 73 | 1.01264055773866 | `stall_recall;theta_edge_p95_abs_err` |
| `modern_fixed` | 202 | 1.0489545061548 | `stall_recall;theta_edge_p95_abs_err;flat_peak_theta_error` |
| `modern_fixed` | 340 | 1.0231571387773 | `stall_recall;flat_peak_theta_error` |
| `modern_fixed` | 520 | 1.01377941238629 | `stall_recall` |
| `uncertainty_weighted` | 1 | 1.15854769466635 | `stall_recall;theta_edge_p95_abs_err;flat_peak_theta_error` |
| `uncertainty_weighted` | 7 | 1.00438174710922 | `flat_peak_theta_error` |
| `uncertainty_weighted` | 11 | 1.0523647419079 | `stall_recall;theta_edge_p95_abs_err` |
| `uncertainty_weighted` | 21 | 1.09351261643159 | `flat_peak_theta_error` |
| `uncertainty_weighted` | 42 | 1.07901896581399 | `theta_edge_p95_abs_err` |
| `uncertainty_weighted` | 73 | 1.06266001793329 | `stall_recall;theta_edge_p95_abs_err` |
| `uncertainty_weighted` | 202 | 1.15287885771829 | `stall_recall;theta_edge_p95_abs_err;flat_peak_theta_error` |
| `uncertainty_weighted` | 340 | 0.994766045789448 | `stall_recall;flat_peak_theta_error` |
| `uncertainty_weighted` | 520 | 0.99942222837595 | `stall_recall` |

主要产物：

- `03_offline_screen/offline_screen_decision.csv`
- `03_offline_screen/offline_screen_decision.json`
- `03_offline_screen/exception_sentinel_candidates.csv`

## N5 validation sentinel 候选导出

工作内容：

- 将 N4 中 `enter_validation_sentinel=true` 的候选导出到 validation sentinel manifest。
- 检查候选 ONNX、sample file、checkpoint 等闭环验证所需文件是否存在。

进入 validation sentinel 的候选：

| 候选 | 算法 | seed | 是否例外 |
|---|---|---:|---|
| `modern_fixed_seed42` | `modern_fixed` | 42 | 否 |
| `modern_fixed_seed101` | `modern_fixed` | 101 | 否 |
| `uncertainty_weighted_seed101` | `uncertainty_weighted` | 101 | 否 |

主要产物：

- `04_validation_sentinel_closed_loop/validation_exports.csv`
- `04_validation_sentinel_closed_loop/sentinel_manifest.csv`

## N6 validation sentinel 闭环验证

工作内容：

- 在 2 条 validation sentinel 路径上运行 closed-loop。
- 对每个候选计算每条路径的 `J_control_path`。
- 检查是否出现 `path_catastrophic`。

validation sentinel 路径：

- `agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16`
- `agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06`

候选结果：

| 候选 | 路径数 | `J_control_mean` | 最差 `J_control_path` | catastrophic 数 |
|---|---:|---:|---:|---:|
| `modern_fixed_seed101` | 2 | 1.01353585089277 | 1.13653646062924 | 0 |
| `modern_fixed_seed42` | 2 | 1.01551478066377 | 1.17415927377489 | 0 |
| `uncertainty_weighted_seed101` | 2 | 1.05467388588771 | 1.24074316216084 | 0 |

逐路径结果：

| 路径 | 候选 | `J_control_path` | `path_fail` | `path_catastrophic` |
|---|---|---:|---|---|
| `036_short_bin06_m04p5_theta_edge_speed_R16` | `modern_fixed_seed42` | 1.17415927377489 | true | false |
| `036_short_bin06_m04p5_theta_edge_speed_R16` | `modern_fixed_seed101` | 1.13653646062924 | true | false |
| `036_short_bin06_m04p5_theta_edge_speed_R16` | `uncertainty_weighted_seed101` | 1.24074316216084 | true | false |
| `039_short_bin09_m01p5_right_R06` | `modern_fixed_seed42` | 0.856870287552642 | false | false |
| `039_short_bin09_m01p5_right_R06` | `modern_fixed_seed101` | 0.890535241156301 | false | false |
| `039_short_bin09_m01p5_right_R06` | `uncertainty_weighted_seed101` | 0.868604609614572 | false | false |

解释：

- validation sentinel 中，`modern_fixed_seed101` 的平均 `J_control` 在 `modern_fixed` 算法内部最低。
- `uncertainty_weighted` 只有 `seed101` 一个硬筛通过候选，因此它成为该算法的 sentinel 候选。
- 三个候选都没有 catastrophic path。

主要产物：

- `04_validation_sentinel_closed_loop/validation_sentinel_execution_summary.md`
- `04_validation_sentinel_closed_loop/sentinel_candidate_path_metrics.csv`
- `04_validation_sentinel_closed_loop/sentinel_path_metrics.csv`
- 各 sentinel 路径子目录下的 `validation_sentinel_summary.csv`、`validation_sentinel_rank.csv`、`validation_sentinel_report.md`

## N7 seed 选择

工作内容：

- 每个算法只在自己的候选内部选择最优 seed。
- 选择标准为最低 `validation_sentinel_J_control_mean`。
- 若出现并列，则继续参考 `offline_v2_score` 和 seed 排序。

选择结果：

| 算法 | 最终 seed | 候选 ID | `validation_sentinel_J_control_mean` | `offline_v2_score` | 选择状态 |
|---|---:|---|---:|---:|---|
| `modern_fixed` | 101 | `modern_fixed_seed101` | 1.01353585089277 | 0.980059344576828 | pass |
| `uncertainty_weighted` | 101 | `uncertainty_weighted_seed101` | 1.05467388588771 | 0.970838817749306 | pass |

主要产物：

- `05_seed_selection/selected_seed_decision.csv`
- `05_seed_selection/selected_seed_decision.json`

## N8 final test 闭环测试

工作内容：

- 将 N7 选出的两个最终候选送入 final test。
- 每条路径同时比较 baseline `ModernTCN`、`modern_fixed_seed101`、`uncertainty_weighted_seed101`。
- 每条路径输出 summary、rank 和 report。

final test 路径：

- `path_factory_logistics_showcase_theta10_v10`
- `path_closed_loop_sharp_turn_transition_theta10_v1`
- `path_closed_loop_long_updown_theta10_v1`
- `path_modern_tcn_showcase_candidate_soft_updown_straight_turn_v1`

执行结果：

- 4 条路径均生成 `final_test_summary.csv`。
- 4 条路径均生成 `final_test_rank.csv`。
- 4 条路径均生成 `final_test_report.md`。
- `final_test_execution_summary.md` 中 4 条路径状态均为 `ok`。

说明：外层 Python 调用曾因 30 分钟超时返回，但 MATLAB 侧已完成全部 4 条 final test 路径输出；因此以本目录下实际生成的 CSV/MD 结果为准。

final test 排名：

| 路径 | 第 1 | 第 2 | 第 3 |
|---|---|---|---|
| `path_closed_loop_long_updown_theta10_v1` | `ModernTCN` | `uncertainty_weighted_seed101` | `modern_fixed_seed101` |
| `path_closed_loop_sharp_turn_transition_theta10_v1` | `uncertainty_weighted_seed101` | `modern_fixed_seed101` | `ModernTCN` |
| `path_factory_logistics_showcase_theta10_v10` | `uncertainty_weighted_seed101` | `modern_fixed_seed101` | `ModernTCN` |
| `path_modern_tcn_showcase_candidate_soft_updown_straight_turn_v1` | `ModernTCN` | `uncertainty_weighted_seed101` | `modern_fixed_seed101` |

两个候选的 final test 汇总：

| 候选 | 路径数 | rank1 次数 | 总 overall rank | 总 `overall_rank_sum` | 总 tracking rank sum | 总 perception rank sum | 总 control rank sum |
|---|---:|---:|---:|---:|---:|---:|---:|
| `modern_fixed_seed101` | 4 | 0 | 10 | 107 | 51 | 25 | 31 |
| `uncertainty_weighted_seed101` | 4 | 2 | 6 | 95 | 39 | 24 | 32 |

解释：

- `uncertainty_weighted_seed101` 在 4 条路径中有 2 条排名第 1。
- `modern_fixed_seed101` 没有任何路径排名第 1。
- `uncertainty_weighted_seed101` 的总 overall rank 和总 `overall_rank_sum` 都更低。
- final test 层面，`Uncertainty-weighted ModernTCN_small seed101` 优于 `ModernTCN_small seed101`。

主要产物：

- `06_final_test_closed_loop/final_test_execution_summary.md`
- `06_final_test_closed_loop/*/final_test_summary.csv`
- `06_final_test_closed_loop/*/final_test_rank.csv`
- `06_final_test_closed_loop/*/final_test_report.md`

## N9 最终报告

工作内容：

- 汇总训练数量、硬筛通过数量、例外候选数量、最终 seed 和 final test 路径。
- 写出最终报告与 machine-readable decision JSON。

最终汇总：

| 算法 | 训练数 | 硬筛通过数 | 例外候选数 | 最终 seed | 最终候选 | 选择状态 |
|---|---:|---:|---:|---:|---|---|
| `modern_fixed` | 10 | 2 | 0 | 101 | `modern_fixed_seed101` | pass |
| `uncertainty_weighted` | 10 | 1 | 0 | 101 | `uncertainty_weighted_seed101` | pass |

主要产物：

- `09_final_report/final_summary_table.csv`
- `09_final_report/final_decision.json`
- `09_final_report/fair_10seed_selection_final_report.md`

## 最终判断

如果只看 validation sentinel 的平均 `J_control`，`ModernTCN_small seed101` 更低：

- `modern_fixed_seed101`: 1.01353585089277
- `uncertainty_weighted_seed101`: 1.05467388588771

但 validation sentinel 是选种哨兵，不是最终泛化结论。真正的 final test 使用 4 条独立闭环路径。final test 中：

- `uncertainty_weighted_seed101` 的总 overall rank 更低：6 vs 10。
- `uncertainty_weighted_seed101` 的总 `overall_rank_sum` 更低：95 vs 107。
- `uncertainty_weighted_seed101` 有 2 条路径排名第 1，`modern_fixed_seed101` 为 0 条。

因此，本目录的最终实验结论是：

`Uncertainty-weighted ModernTCN_small seed101` 在 final test 层面优于 `ModernTCN_small seed101`。

## 复核建议

后续如果需要复核或继续扩展，建议优先查看以下文件：

1. `03_offline_screen/offline_screen_decision.csv`
2. `04_validation_sentinel_closed_loop/sentinel_candidate_path_metrics.csv`
3. `05_seed_selection/selected_seed_decision.csv`
4. `06_final_test_closed_loop/*/final_test_rank.csv`
5. `09_final_report/final_decision.json`

若要将本轮结果写入论文或正式报告，建议明确区分三层结论：

- 离线硬筛：只决定哪些 seed 有资格进入 validation sentinel。
- validation sentinel：只用于每个算法内部选 seed。
- final test：用于两个算法最终优劣判断。
