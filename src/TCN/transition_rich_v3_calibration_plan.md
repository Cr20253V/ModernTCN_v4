# Transition-Rich v3 TCN 主工况校准计划

## 背景

V3 数据增强已经显著改善 TCN 的坡度和转弯过渡能力，但 `flat_recall` 从 V2 的 `0.9445` 下降到 V3 的 `0.8594`，导致 `acc_main` 均值没有提升。

当前判断：不继续改路径，也不立即进入 ModernTCN。先固定 `TCN_dataset_v3_transition_rich.mat`，调整 TCN 主工况训练权重和选模策略。

## 已新增能力

`TCN_train.m` 新增：

- `cfg.main_class_multipliers`：主工况类别乘子，顺序为 `[flat stall slope]`。
- `cfg.best_metric = 'main_guard'`：显式保护 `flat/stall/slope` recall 的选模指标。

新增入口：

- `run_TCN_v3_main_calibration.m`

## 校准配置

| config | 目的 |
|---|---|
| `sqrt_mild` | 将 main class weight 从 `balanced` 改为 `sqrt_inverse`，并温和降低负坡主分类权重。 |
| `flat_guard` | 更强保护 flat recall，适合验证是否能修复 seed42 的主工况坍塌。 |
| `main_guard` | 直接用 `main_guard` 作为最终选模指标，牺牲部分 turn priority，观察主工况上限。 |

## 推荐先跑

先跑三个压力测试 seed，不必立刻跑五个：

```matlab
init_project;
run_TCN_v3_main_calibration([42 101 73], {'sqrt_mild','flat_guard','main_guard'}, true);
```

如果时间有限，先跑最关键的坏例和均衡例：

```matlab
init_project;
run_TCN_v3_main_calibration([42 101], {'sqrt_mild','flat_guard'}, true);
```

## 判定标准

进入完整五 seed 复跑的条件：

- `acc_main` 尽量回到 `0.92+`；
- `flat_recall` 回到 `0.90+`；
- `slope_recall` 不低于 `0.92`；
- `acc_turn_transition` 不低于 `0.75`。

如果上述条件满足，再跑：

```matlab
init_project;
run_TCN_v3_main_calibration([11 21 42 73 101], {'最佳config名'}, true);
```

如果所有校准配置都无法同时保住主工况和转弯过渡，再进入 ModernTCN-small。
