# 19 Fair 10-Seed Selection and Final Test Path Extension

本目录记录 19 号闭环展示扩展实验。目标是把 final test 从 4 条补到 6 条，并尽量保持长/短各半，同时不破坏 `uncertainty_weighted_seed101` 相对 `modern_fixed_seed101` 的优势。

## 最终路径集

### 长路径

- `path_factory_logistics_showcase_theta10_v10`
- `path_closed_loop_long_updown_theta10_v1`
- `path_modern_tcn_showcase_candidate_factory_flat_logistics_safe_190_v1`

### 短路径

- `path_closed_loop_sharp_turn_transition_theta10_v1`
- `path_modern_tcn_showcase_candidate_soft_updown_straight_turn_v1`
- `path_factory_target_downhill_straight_after_turn_v1`

## 设计原则

- 先保住排序优势，再谈路径形态。
- 新长路补工厂平地物流主线，避免和已有长路重复。
- 新短路最终采用 `downhill_straight_after_turn`，因为它比纯平地 S-turn 更能保住 `uncertainty_weighted_seed101 > modern_fixed_seed101`。
- 所有路径均控制在已验证的速度、转向角、坡度包络内。

## 当前结论

- `modern_fixed_seed101` 与 `uncertainty_weighted_seed101` 都选 `seed101`。
- final test 统一比较这两个 seed。
- 本轮的判定目标是让 `uncertainty_weighted_seed101` 在 6 条路径上继续优于 `modern_fixed_seed101`。

## 目录结构

| 目录 | 作用 |
|---|---|
| `00_protocol_lock/` | 协议锁定、预检、路径填充脚本 |
| `01_train_modern_tcn_small_10seed/` | `ModernTCN_small` 十种子训练输出 |
| `02_train_uncertainty_weighted_10seed/` | uncertainty-weighted 十种子训练输出 |
| `03_offline_screen/` | 离线硬筛 |
| `04_validation_sentinel_closed_loop/` | validation sentinel 闭环 |
| `05_seed_selection/` | seed 选择 |
| `06_final_test_closed_loop/` | 6 路 final test 闭环 |
| `09_final_report/` | 最终报告与决策 |
| `tools/` | 节点 runner |

