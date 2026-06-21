# Phase 7 Negative Result Analysis

## 总体规律

E1-E5 的共同结论不是“代码失败”，而是 full gate 下的负结果：局部指标提升不足以晋级。当前保护指标反复暴露出 main/turn/theta 多任务冲突，尤其是 stall、transition、theta edge 和 flat peak 之间的互相牵制。

晋级原则保持不变：只有 full gate 通过且不破坏保护指标，才算 promotable。单点指标改善不能写成成功。

## E1 Loss Optimization

E1 状态为 PASS，但 dynamic loss 是负结果。`uncertainty_weighting` 和 `gradnorm` 都没有 eligible run，decision 中两个方法均记录为 `protection metrics failed or no eligible runs`。

主要规律是动态权重没有解决多任务冲突。它们可能改善个别指标，但整体仍出现多项保护指标退化，因此后续应固定使用 `loss_mode=fixed`，不能把 dynamic loss 作为主线。

## E2 Hard-Sample Focal Loss

E2 状态为 PASS，但 hard-sample focal only 是负结果。4 个 formal seed21 run 的 eligible/promotable 数量均为 0。

`fs_t05_s02_sm000_seed21` 是唯一提升 `acc_turn_transition` 的 run，但同时破坏 `acc_main`、`acc_turn`、`theta_mae_deg`、`flat_recall`、`theta_edge_p95_abs_err` 和 `flat_peak_theta_error`，不能晋级。这说明 transition 或 stall 的局部加权会把误差转移到主分类和 theta 保护指标上。

`theta_smooth_status=disabled_contract_limited` 不是实验失败，而是数据契约限制。当前 test split 的 `run_id` 非连续，缺少可靠 window/order 字段，不能安全构造同一 run 的相邻窗口 smoothness loss。

## E3 Physics-Group Residual Gate

E3 状态为 PASS，但 physics-group residual gate 是负结果。最佳 run `pg_alpha01_seed21` 有 `alpha_final=0.3643222153186798`，gate interpretability score 为 2，说明物理分支和 gate 有学习迹象。

问题在于局部解释性没有转化为 full-gate 可晋级结果。`pg_alpha01_seed21` 提升了 `acc_turn_transition` 和 `theta_mae_deg`，但 `stall_recall=0.635417` 低于 gate，`theta_edge_p95_abs_err=3.253798` 和 `flat_peak_theta_error=5.831338` 也超过保护线。物理分支可解释，但仍会破坏闭环敏感保护指标。

## E4 Mode-Conditioned Theta Experts

E4 状态为 PASS，但 mode-conditioned theta experts 是负结果。最佳 run `mode_theta_detach_flatreg001_seed21` 将 `theta_mae_deg` 降到 0.616433，且 `theta_edge_p95_abs_err=2.651289` 有局部改善。

它仍不能晋级，因为 `stall_recall=0.666667` 低于 safe gate，`acc_turn_transition=0.482861` 不达标，`flat_peak_theta_error=6.068908` 也超过保护线。E4 说明 theta expert 可以改善平均回归误差，但平均 MAE 的收益会伴随 edge/flat peak 或 transition/stall 风险，当前不建议继续救 E4。

## E5 Confidence-Aware Scheduling

E5 状态为 PASS，但 confidence-aware scheduling 未通过 offline safety screen。所有 scheduling 配置均显著恶化 `theta_sched_mae_deg`、`flat_peak_theta_error` 和 `theta_edge_p95_abs_err`。

最佳排序 run `cs_main_c06_d02` 的 `theta_sched_mae_deg=1.294800`，显著高于 raw baseline 0.679395；`flat_peak_theta_error=9.631826`，`theta_edge_p95_abs_err=9.725619`，均远超 safety screen。虽然 rate limit 可把 step p95 压到 0.1 或 0.2 deg/step，但当前 split-order replay 的 `run_id` 非连续，step/smoothness 只能作为 advisory 指标，不能作为闭环收益证据。

E5 因此只能作为 deployment-side offline safety screen，不应进入 Phase 6 sandbox expansion，更不能进入 formal closed-loop。

## Phase 7 归因结论

- 单点改善不足以晋级，必须同时守住 main、turn、theta 和保护指标。
- 多任务冲突反复出现，尤其是 theta MAE 与 edge/flat peak、transition/stall 之间。
- stall recall 和 turn transition 是主要保护指标风险。
- confidence scheduling 在当前非连续 test split 上只能做 safety screen，不能证明闭环平滑收益。
- 当前数据契约不支持可靠 offline temporal smoothness 判断；继续研究前应优先补齐连续序列顺序信息。
