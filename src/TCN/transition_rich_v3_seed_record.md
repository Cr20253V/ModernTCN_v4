# Transition-Rich v3 Seed Record

本记录由 `results/tcn/experiments/transition_rich_v3_seed*/TCN_GRU_transition_rich_v3_summary.csv` 汇总得到。

## Multi-Seed Summary

使用的 seeds：`11, 21, 42, 73, 101`

| model | acc_main mean/std | acc_turn mean/std | turn_trans mean/std | theta_mae_deg mean/std | slope_recall mean/std |
|---|---:|---:|---:|---:|---:|
| TCN | 0.9052 / 0.0350 | 0.9063 / 0.0027 | 0.7830 / 0.0115 | 0.4490 / 0.0846 | 0.9350 / 0.0458 |
| GRU | 0.9400 / 0.0050 | 0.8875 / 0.0104 | 0.6870 / 0.0381 | 0.4195 / 0.0653 | 0.9715 / 0.0066 |

结论：V3 数据增强达到了“补坡度/过渡覆盖”的目标。TCN 的 `slope_recall`、`uphill_recall`、`theta_mae_deg` 和 `acc_turn_transition` 相比 V2 明显改善；但 TCN 的 `acc_main` 没有提升，主要问题转移为 flat/slope 主工况边界校准。

## V2 到 V3 的 TCN 变化

| metric | V2 TCN | V3 TCN | delta |
|---|---:|---:|---:|
| acc_main | 0.9093 | 0.9052 | -0.0041 |
| acc_turn | 0.9021 | 0.9063 | +0.0042 |
| acc_turn_transition | 0.7256 | 0.7830 | +0.0574 |
| theta_mae_deg | 0.5114 | 0.4490 | -0.0624 |
| slope_recall | 0.8246 | 0.9350 | +0.1104 |
| uphill_recall | 0.7767 | 0.9104 | +0.1338 |
| downhill_recall | 0.9383 | 0.9732 | +0.0349 |
| flat_recall | 0.9445 | 0.8594 | -0.0851 |

## Best Single Runs

| metric | best model | seed | value |
|---|---|---:|---:|
| acc_main | GRU | 73 | 0.9459 |
| acc_turn | TCN | 21 | 0.9091 |
| acc_turn_transition | TCN | 101 | 0.7984 |
| theta_mae_deg 越低越好 | GRU | 73 | 0.3437 |
| TCN theta_mae_deg 越低越好 | TCN | 73 | 0.4019 |
| slope_recall | GRU | 21 | 0.9825 |
| TCN slope_recall | TCN | 21 | 0.9797 |
| uphill_recall | GRU | 21 | 0.9736 |
| downhill_recall | TCN | 21 | 1.0000 |

## TCN 相对 GRU 占优的 Seed

| seed | TCN 优于 GRU 的指标 |
|---:|---|
| 11 | acc_turn, acc_turn_transition, downhill_recall, stall_recall, theta_mae_deg |
| 21 | acc_turn, acc_turn_transition, downhill_recall, stall_recall |
| 42 | acc_turn, acc_turn_transition, stall_recall |
| 73 | acc_turn, acc_turn_transition, stall_recall |
| 101 | acc_turn, acc_turn_transition, downhill_recall, stall_recall, flat_recall, theta_mae_deg |

说明：

- TCN 仍然在五个 seed 上都赢了 `acc_turn` 和 `acc_turn_transition`。
- TCN 的坡度召回已接近 GRU，但均值仍略低。
- TCN 的 theta MAE 与 GRU 的差距明显缩小，但均值仍略差。
- TCN 的主要短板从 V2 的坡度识别不足，转移为 V3 的 flat recall 下降。
- seed `101` 是当前 V3 最均衡的 TCN 候选。
- seed `42` 是主工况退化最明显的坏例，适合作为校准实验的压力测试 seed。

## 下一步

固定 V3 数据集，不再修改路径，先做 TCN 主工况校准：

- 降低 `main_neg_slope_weight`，避免负坡样本过度推高 slope 偏置。
- 将 main class weighting 从 `balanced` 调整为更温和的 `sqrt_inverse`。
- 增加 flat 类别乘子，保护 `flat_recall`。
- 使用 `main_guard` 选模指标选择主任务基座，避免 early base checkpoint 的 flat/slope 边界过差。
- 优先跑 seeds `42, 101, 73`，再根据结果决定是否扩展到全部五个 seeds。
