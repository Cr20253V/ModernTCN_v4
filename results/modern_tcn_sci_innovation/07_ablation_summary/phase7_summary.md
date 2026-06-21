# Phase 7 Summary

## 结论

Phase 7 状态：PASS。

当前 frozen baseline 仍是最优主线：

- `ModernTCN_small`
- `input_dim=22`
- `seq_len=128`
- `feature_contract=passive17_plus_all5`
- `plant_revision=agv_physics_v2_plantfix`

E1-E5 均为流程 PASS，但没有任何 promotable candidate。当前不建议进入 Phase 6，也不得把 E5 的 sandbox/formal gate 改为 true。

## Phase Decisions

| phase | conclusion | promotable candidate | next action |
|---|---|---:|---|
| E0 | baseline lock PASS | reference | preserve frozen baseline |
| E1 | loss optimization PASS, negative result | false | use `loss_mode=fixed` |
| E2 | hard-sample focal PASS, negative result | false | do not expand seeds |
| E3 | physics-group gate PASS, negative result | false | do not promote PG gate |
| E4 | mode theta experts PASS, negative result | false | do not rescue E4 |
| E5 | confidence scheduling PASS, offline safety failed | false | do not enter Phase 6 |

## Phase 6 / Phase 8

Phase 6 不应执行：E5 明确 `can_enter_phase6_sandbox_expansion=false` 且 `can_enter_phase6_formal=false`，没有选出 sandbox candidate，也没有执行 closed-loop。

Phase 8 可以执行。Phase 8 应以 `negative_ablation_and_baseline_preservation` 为论文定位，说明当前增强模块均没有超过 frozen ModernTCN_small baseline，最终主线应保留 baseline，而不是包装局部指标提升为成功。

## 后续研究优先方向

1. 优先补齐数据契约中的连续序列顺序信息，支持可靠的 offline temporal smoothness 与 replay 评估。
2. 继续研究前应把 stall/transition、theta edge、flat peak 作为硬保护指标，而不是只优化 theta MAE。
3. 多任务冲突需要单独诊断，例如分类 head 与 theta head 的梯度冲突、样本分布边界、工况标签噪声。
4. 不建议继续扩展 E4/E5 seeds，也不建议进入 Phase 6 来补救未过 offline safety screen 的候选。
