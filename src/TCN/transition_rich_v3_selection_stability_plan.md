# Transition-Rich v3 Selection Stability 筛选计划

更新时间：2026-05-01

## 背景

`base_comp_flat120` 在 confirm/validate 阶段表现最好，但 full 复跑出现训练不稳定。随后 `guard45` 实验已验证：

- `base_selection_start_epoch=45` 生效；
- 但后期 base checkpoint 严重偏向 flat，导致 slope recall 坍塌；
- 因此不继续 `guard45` 五 seed。

当前判断：问题不是“base checkpoint 过早”这一单因子，而是 base 选模指标没有稳定约束 flat/slope 边界。下一步改为测试 base 选模指标，而不是强制推迟选模轮次。

## 已新增能力

`TCN_train.m` 新增选模指标：

```text
composite_guarded
```

该指标在原 `composite` 基础上增加主工况 per-class recall 底线惩罚：

```text
flat_recall >= floor_flat
stall_recall >= floor_stall
slope_recall >= floor_slope
```

默认不影响旧实验。只有显式设置：

```matlab
cfg.base_best_metric = 'composite_guarded';
```

或：

```matlab
cfg.best_metric = 'composite_guarded';
```

才会启用。

## 新增入口

```matlab
run_TCN_v3_selection_stability_screen
```

输出目录：

```text
results/tcn/experiments/transition_rich_v3_selection_stability
```

候选配置：

| config | 目的 |
|---|---|
| `flat120_comp_ref` | 复现 `base_comp_flat120` 原始 base composite 选择，用作参照。 |
| `flat120_base_main_guard` | 只把 base 选模改为 `main_guard`，保留 turn-priority 后段。 |
| `flat120_comp_guard_s090` | base 选模改为 `composite_guarded`，flat/slope floor 都为 0.90。 |
| `flat115_comp_guard_s092` | 降低 flat 乘子，slope floor 提到 0.92。 |
| `flat110_slope100_guard` | 进一步降低 flat 偏置，并取消 slope 乘子削弱。 |

## 推荐运行

先只跑 seed42，避免无效长跑：

```matlab
init_project;
run_TCN_v3_selection_stability_screen(42);
```

如果 seed42 有候选满足：

```text
acc_main >= 0.90
flat_recall >= 0.90
slope_recall >= 0.88
acc_turn_transition >= 0.75
theta_mae_deg <= 0.70
```

再跑三 seed：

```matlab
run_TCN_v3_selection_stability_screen([42 73 101], {'候选名'});
```

三 seed 稳定后再考虑完整五 seed。若 seed42 没有任何候选通过，不要继续扩 seed，应转入 ModernTCN-small 或闭环前的单模型 smoke test。

## 输出文件

```text
results/tcn/experiments/transition_rich_v3_selection_stability/
  TCN_v3_selection_stability_summary.csv
  TCN_v3_selection_stability_summary.md
  <config>/seed*/TCN_train_report.md

data/models/
  TCN_model_transition_rich_v3_select_stability_<config>_seed*.mat
  TCN_meta_transition_rich_v3_select_stability_<config>_seed*.mat
```
