# Transition-Rich v2 Seed Record

本记录由 `results/tcn/experiments/transition_rich_v2_seed*/TCN_GRU_transition_rich_v2_summary.csv` 汇总得到。

## Multi-Seed Summary

使用的 seeds：`11, 21, 42, 73, 101`

| model | acc_main mean/std | acc_turn mean/std | turn_trans mean/std | theta_mae_deg mean/std | slope_recall mean/std |
|---|---:|---:|---:|---:|---:|
| TCN | 0.9093 / 0.0331 | 0.9021 / 0.0085 | 0.7256 / 0.0594 | 0.5114 / 0.0728 | 0.8246 / 0.0938 |
| GRU | 0.9403 / 0.0088 | 0.8849 / 0.0059 | 0.6380 / 0.0487 | 0.3873 / 0.0631 | 0.9237 / 0.0145 |

结论：GRU 仍然是更稳定的强 baseline，在 `acc_main`、`theta_mae_deg` 和 `slope_recall` 上整体更强。TCN 的优势集中在 `acc_turn` 和转弯过渡准确率上，并且该优势在五个 seed 中都保持成立。

## Best Single Runs

| metric | best model | seed | value |
|---|---|---:|---:|
| acc_main | GRU | 21 | 0.9494 |
| acc_turn | TCN | 11 | 0.9143 |
| acc_turn_transition | TCN | 73 | 0.7851 |
| theta_mae_deg 越低越好 | GRU | 101 | 0.3296 |
| slope_recall | GRU | 21 | 0.9369 |
| uphill_recall | GRU | 21 | 0.9283 |
| downhill_recall | GRU | 11/21/42/73/101 | 0.9574 |

## TCN 相对 GRU 占优的 Seed

| seed | TCN 优于 GRU 的指标 |
|---:|---|
| 11 | acc_turn, acc_turn_transition, theta_mae_deg |
| 21 | acc_turn, acc_turn_transition |
| 42 | acc_main, acc_turn, acc_turn_transition |
| 73 | acc_turn, acc_turn_transition |
| 101 | acc_turn, acc_turn_transition |

说明：

- TCN 在五个 seed 上都赢了 `acc_turn` 和 `acc_turn_transition`。
- TCN 只有在 seed `42` 上赢了 `acc_main`。
- TCN 只有在 seed `11` 上赢了 `theta_mae_deg`。
- 在这五个 seed 中，TCN 没有赢过 GRU 的 `slope_recall`。
- seed `42` 是后续最值得保留的 TCN 候选，因为它是唯一同时赢下 `acc_main` 的 TCN seed。
- 如果目标是转弯过渡鲁棒性，seed `73` 是最强的 TCN 候选。
- seed `11` 也值得保留，因为它给出了最高的 TCN `acc_turn`，并且是唯一让 TCN 在 theta MAE 上优于 GRU 的 seed。

## Recommended Seed Set For Larger Data

大规模数据训练时，建议使用 GRU seed `21` 或 `101` 作为强 baseline 参考：

- `21`：`acc_main`、`slope_recall` 和 `uphill_recall` 最优。
- `101`：`theta_mae_deg` 最优。

TCN 建议优先保留 seeds `42, 73, 11`：

- `42`：相对 GRU 最均衡的 TCN 候选。
- `73`：转弯过渡指标最强的 TCN 候选。
- `11`：本轮 sweep 中 TCN 的 `acc_turn` 最优，同时也是 TCN 自身 theta MAE 最优。

最终结论不应只依赖单个最优 seed。建议正式报告中使用多 seed 均值和标准差作为主要结论，同时单独记录最优 checkpoint 作为工程候选模型。
