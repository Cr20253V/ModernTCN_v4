# Transition-Rich v3 Guarded Base 复跑计划

更新时间：2026-05-01

## 目标

固定 `data/tcn/TCN_dataset_v3_transition_rich.mat`，不修改路径和数据集，复跑当前最有潜力的 TCN baseline：

```text
base_comp_flat120
```

本轮只解决 `combine_base_and_turn_best=true` 时主任务基座过早选中的问题。full 阶段已有结果显示，部分 seed 的 `base_best_epoch` 落在第 `8-13` 轮，导致 slope recall 和 theta 明显退化。因此新增：

```matlab
cfg.base_selection_start_epoch = 45;
```

使主任务基座只从第 45 轮之后的 base stage 中选择。

## 已修改代码

| 文件 | 修改 |
|---|---|
| `src/TCN/TCN_train.m` | 新增 `cfg.base_selection_start_epoch`，控制 base checkpoint 的最早选模轮次；训练报告写出该参数。 |
| `src/TCN/run_TCN_v3_guarded_base_full.m` | 新增 guarded full 复跑入口，不覆盖 auto screen 旧结果。 |

## 运行命令

建议先跑三个诊断 seed：

```matlab
init_project;
run_TCN_v3_guarded_base_full([42 73 101], false);
```

若结果合理，再跑完整五 seed：

```matlab
init_project;
run_TCN_v3_guarded_base_full([11 21 42 73 101], false);
```

如果需要强制覆盖同名 guarded 结果：

```matlab
init_project;
run_TCN_v3_guarded_base_full([11 21 42 73 101], true);
```

## 输出位置

```text
results/tcn/experiments/transition_rich_v3_guarded_base/
  TCN_v3_guarded_base_full_summary.csv
  TCN_v3_guarded_base_full_summary.md
  base_comp_flat120_guard45/seed*/TCN_train_report.md

data/models/
  TCN_model_transition_rich_v3_guarded_base_comp_flat120_seed*.mat
  TCN_meta_transition_rich_v3_guarded_base_comp_flat120_seed*.mat
```

## 判定标准

guarded full 通过的最低标准：

```text
acc_main >= 0.90
flat_recall >= 0.90
slope_recall >= 0.88
acc_turn_transition >= 0.75
theta_mae_deg <= 0.70
```

进入闭环前的推荐目标：

```text
acc_main mean >= 0.93
flat_recall mean >= 0.91
slope_recall mean >= 0.93
acc_turn_transition mean >= 0.77
theta_mae_deg mean <= 0.45
```

若 guarded full 仍出现多 seed 的 `base_best_epoch < 45`，说明配置没有生效；若 `base_best_epoch` 正常但 slope/theta 仍退化，则再考虑 ModernTCN-small，而不是继续加大 loss 权重。
