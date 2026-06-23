# ModernTCN_small 控制导向评价指标重构与局部优化实验技术文档（Codex 执行版）

**项目仓库**：`https://github.com/Cr20253V/ModernTCN_v4`

**文档用途**：指导 Codex 按照“控制导向重评估与候选分层；若没有有价值结果，再进入局部优化”的路线执行分析和实验。

**核心原则**：

```text
1. 不修改当前 ModernTCN_small 最优结论。
2. 不覆盖之前已经完成的 ablation 和 SCI innovation 试验结果。
3. 不先修改训练数据集和闭环测试路径。
4. 不先修改 MPC 代价函数。
5. 先判断旧实验是否被旧 gate 错杀，再决定是否进入局部优化。
6. 新指标必须服务 AGV 路径跟踪目标，不能为了让某个候选通过而定制。
7. 本轮目标是候选分层，不预设任何历史实验晋级。
```

---

# 0. 本轮工作的总逻辑

当前已有事实：

```text
1. 当前最优算法仍为 ModernTCN_small。
2. 当前主线为 22D 输入、seq_len=128。
3. 之前 5 个 SCI 创新实验在原始 gate 下均未成功。
4. 这些实验中部分模型存在局部改善，例如 theta_mae、acc_turn_transition 或某些辅助指标改善。
5. 原始 gate 偏向离线感知保护，不一定完全等价于闭环路径跟踪目标。
```

本轮必须明确分为两个环节：

```text
环节 A：控制导向评价指标重构、历史 5 个实验重评估与候选分层
环节 B：若环节 A 没有选出有效候选，再进行局部残差优化
```

严禁直接跳到环节 B。  
严禁为了让某个实验结果通过而随意修改指标。  
严禁覆盖当前 ModernTCN_small 最优结论和之前负结果。

本轮预期必须写清：

```text
1. 本轮大概率不会直接产生 Class C。
2. 更可能产生 Class B 或 Class D。
3. Class B 只能进入 sandbox closed-loop，不能直接作为正式结论。
4. Class D 只能指导局部优化，不能作为主方法。
```

---

# 1. 当前 baseline 和历史实验定义

## 1.1 当前 baseline

当前 baseline 指：

```text
model: ModernTCN_small
input_dim: 22
seq_len: 128
feature_contract: passive17_plus_all5
plant_revision: agv_physics_v2_plantfix
```

Codex 应从已有结果中读取当前 baseline 的离线指标、闭环指标、checkpoint、ONNX 和相关配置，不得重新定义 baseline。

## 1.2 已有 5 个实验方向

本轮重评估对象来自：

```text
results/modern_tcn_sci_innovation/
```

包括：

```text
E1: Loss-only Optimization
    uncertainty weighting
    GradNorm

E2: Hard-sample + Smooth Loss
    transition focal
    stall focal
    theta smoothness

E3: Physics-Group Residual Gate
    AGV 物理分组全局残差门控

E4: Mode-Conditioned Theta Experts
    flat/stall/slope 条件化 theta expert

E5: Confidence-Aware Scheduling Filter
    confidence-based theta scheduling / rate limit / safety screen
```

这些实验在原始 gate 下没有成功。  
本轮不是删除原结论，而是用新的控制导向评价体系重新分析它们是否仍有价值。

## 1.3 E2/E5 Evidence Degradation Rules

Codex 必须按以下证据有效性规则解释原 E2 和原 E5：

```text
1. 原 E2 只能作为 hard-sample focal only 候选；
2. 原 E2 的 theta_smoothness_claim = invalid_not_run；
3. 原 E2 不得用于证明 theta_smoothness_loss 有效或无效；
4. 原 E5 的 scheduled / smoothness / step 指标均为 advisory_only；
5. 原 E5 不得进入正式 J_control / J_smooth_event 排名；
6. 原 E5 不得作为 confidence scheduling 有效或无效的正式证据；
7. 如果后续生成 replay-capable dataset，必须新增 E5_replay_fixed，而不是覆盖原 E5。
```

这些规则必须进入 `candidate_registry.csv` 和所有重评估报告。原 E2/E5 的负结果仍保留，但证据等级必须降级，不得扩大解释范围。

---

# 2. 本轮输出目录规范

新增根目录：

```text
results/modern_tcn_metric_rebuild/
```

建议目录结构：

```text
results/modern_tcn_metric_rebuild/
    00_baseline_and_artifact_lock/
    01_metric_design/
    02_metric_freeze/
    03_rerank_existing_experiments/
    04_candidate_decision/
    05_sandbox_closed_loop_if_needed/
    06_local_residual_optimization_if_needed/
    07_final_report/
```

所有新分析、表格、报告都写入此目录。不得覆盖：

```text
results/modern_tcn_sci_innovation/
results/modern_tcn_ablation/
results/compare/tcn_gru_modern_closed_loop/
已有 baseline checkpoint
已有 ONNX
已有 MATLAB generated layers
已有 Simulink 配置
```

必须新增或要求生成：

```text
results/modern_tcn_metric_rebuild/01_metric_design/metric_dictionary.csv
results/modern_tcn_metric_rebuild/02_metric_freeze/hard_constraint_thresholds.json
```


# 3. 环节 A：评价指标重构与已有实验重评估

---

## Phase A0：锁定 baseline 和历史实验结果

### A0.1 任务目标

冻结当前最优结论，锁定所有待重评估候选，防止重评估过程变成结果重写。

### A0.2 执行内容

生成：

```text
results/modern_tcn_metric_rebuild/00_baseline_and_artifact_lock/artifact_lock.md
results/modern_tcn_metric_rebuild/00_baseline_and_artifact_lock/artifact_inventory.csv
results/modern_tcn_metric_rebuild/00_baseline_and_artifact_lock/baseline_metrics_snapshot.csv
results/modern_tcn_metric_rebuild/00_baseline_and_artifact_lock/previous_experiment_inventory.csv
```

`artifact_inventory.csv` 字段：

```text
artifact_type
path
exists
size_bytes
modified_time
role
readonly_required
```

必须检查：

```text
results/modern_tcn_sci_innovation/00_baseline_lock/
results/modern_tcn_sci_innovation/01_loss_optimization/
results/modern_tcn_sci_innovation/02_hard_sample_loss/
results/modern_tcn_sci_innovation/03_physics_group_gate/
results/modern_tcn_sci_innovation/04_mode_conditioned_theta/
results/modern_tcn_sci_innovation/05_confidence_scheduling/
results/modern_tcn_sci_innovation/07_ablation_summary/
results/modern_tcn_ablation/
```

### A0.3 停止条件

如出现以下情况，必须停止并生成 failure report：

```text
1. 当前 baseline 无法定位。
2. 当前 baseline 不是 22D seq128 ModernTCN_small。
3. 历史 5 个实验结果无法读取。
4. 脚本试图覆盖旧结果。
```

---

## Phase A1：metric dictionary + hard threshold definition

### A1.1 设计目标

新评价体系应服务于论文最终目标：

```text
1. 离线感知是否足够好；
2. 闭环路径跟踪是否更稳；
3. 控制输入是否更平滑；
4. 约束触碰是否更少；
5. 相对真实坡度 oracle 的差距是否缩小；
6. 模型是否在关键局部事件上更可靠。
```

新指标不能只为了让某一个历史候选获胜。

Phase A1 的关键输出不是候选排名，而是先冻结指标字典和硬约束阈值。任何候选排名必须发生在 `metric_dictionary.csv` 和 `hard_constraint_thresholds.json` 冻结之后。

---

## A1.2 metric dictionary

生成：

```text
results/modern_tcn_metric_rebuild/01_metric_design/metric_dictionary.csv
```

字段：

```text
canonical_metric
source_priority
allowed_source_fields
unit
direction
normalization
missing_policy
used_in
hard_constraint_threshold
notes
```

必须至少定义以下 canonical metrics：

```text
xy_rmse
ey_rmse
epsi_rmse
control_smoothness
omega_cmd_rms
delta_u_proxy
theta_sched_mae_deg
theta_mae_deg
theta_edge_p95_abs_err
flat_peak_theta_error
constraint_penalty
gap_to_oracle
acc_main
acc_turn
acc_turn_transition
stall_recall
slope_recall
flat_recall
```

字段映射规则：

```text
delta_u_proxy:
    source_priority = j_du > delta_u_rms > domega_cmd_rms > dF_rms

control_smoothness:
    source_priority = delta_u_proxy > omega_cmd_rms > theta_sched_smoothness

constraint_penalty:
    source_priority = viol_rate > constraint_touch_count > max(F_limit_hit_pct, omega_limit_hit_pct)

gap_to_oracle:
    only valid when same path, same scenario, same metric, same closed-loop protocol
```

缺失处理：

```text
1. 不得虚构；
2. 不得用 0 填充；
3. 不得用 baseline 值填充；
4. 缺失则该候选不能计算对应 score component；
5. 缺失比例必须写入 report。
```

`metric_dictionary.csv` 冻结后，后续脚本只能按 canonical metric 读取和映射字段，不得临时新增同义指标绕过缺失规则。

---

## A1.3 hard constraint threshold definition

生成：

```text
results/modern_tcn_metric_rebuild/02_metric_freeze/hard_constraint_thresholds.json
```

建议初始阈值：

```json
{
  "closed_loop_unstable_must_be_false": true,
  "constraint_penalty_max_ratio": 1.00,
  "viol_rate_max_abs_increase": 0.001,
  "acc_main_min_drop": 0.010,
  "stall_recall_min_drop": 0.050,
  "slope_recall_min_drop": 0.010,
  "theta_edge_p95_max_ratio": 1.05,
  "flat_peak_theta_error_max_ratio": 1.05,
  "omega_cmd_rms_max_ratio": 1.10,
  "delta_u_proxy_max_ratio": 1.10
}
```

说明：

```text
1. 这些阈值必须在候选重排前冻结；
2. 冻结后不得根据结果修改；
3. 如某指标缺失，则不能作为 hard constraint，仅记录 unavailable；
4. hard constraint 判断必须引用 metric_dictionary.csv 中的 canonical metric。
```

---

## A1.4 新评价体系分层

新评价体系分为四层：

```text
Layer 1: 安全硬约束
Layer 2: 闭环控制主评分
Layer 3: 离线感知辅助评分
Layer 4: 局部事件专项评分
```

### Layer 1：安全硬约束

这是不可违反的 hard filter。

候选必须满足：

```text
closed_loop_unstable == false
constraint_penalty <= baseline_constraint_penalty * constraint_penalty_max_ratio
viol_rate <= baseline_viol_rate + viol_rate_max_abs_increase
acc_main >= baseline_acc_main - acc_main_min_drop
stall_recall >= baseline_stall_recall - stall_recall_min_drop
slope_recall >= baseline_slope_recall - slope_recall_min_drop
theta_edge_p95_abs_err <= baseline_theta_edge_p95_abs_err * theta_edge_p95_max_ratio
flat_peak_theta_error <= baseline_flat_peak_theta_error * flat_peak_theta_error_max_ratio
omega_cmd_rms <= baseline_omega_cmd_rms * omega_cmd_rms_max_ratio
delta_u_proxy <= baseline_delta_u_proxy * delta_u_proxy_max_ratio
```

阈值来自：

```text
results/modern_tcn_metric_rebuild/02_metric_freeze/hard_constraint_thresholds.json
```

如果某项 hard constraint 所需指标缺失，则该项不得被判为 pass，只能记录为：

```text
hard_constraint_unavailable
```

如果某候选没有闭环结果，则不能正式通过 Layer 1，只能标记：

```text
offline_only_candidate
```

对应处理：

```text
可以进入 sandbox closed-loop；
不能直接作为最终主方法；
不能宣称闭环优于 baseline。
```

---

### Layer 2：闭环控制主评分

定义控制导向综合评分 `J_control`，分数越低越好。

建议公式：

```text
J_control =
    w_xy       * N(xy_rmse)
  + w_ey       * N(ey_rmse)
  + w_epsi     * N(epsi_rmse)
  + w_omega    * N(omega_cmd_rms)
  + w_du       * N(delta_u_proxy)
  + w_theta    * N(theta_sched_mae_deg)
  + w_oracle   * N(gap_to_oracle)
  + w_const    * constraint_penalty
```

其中：

```text
N(metric) = metric / baseline_metric
```

若 baseline_metric 接近 0，使用：

```text
N(metric) = metric / max(abs(baseline_metric), epsilon)
epsilon = 1e-6 或由指标尺度指定
```

建议初始权重：

```text
w_xy     = 0.20
w_ey     = 0.20
w_epsi   = 0.10
w_omega  = 0.15
w_du     = 0.15
w_theta  = 0.10
w_oracle = 0.05
w_const  = 0.05
```

说明：

```text
1. 路径跟踪误差是主目标，因此 xy_rmse 和 ey_rmse 权重最高。
2. 控制平滑性是闭环稳定的重要目标，因此 omega_cmd_rms 和 delta_u_proxy 权重较高。
3. theta_sched_mae 和 gap_to_oracle 用于衡量调度接近真实坡度上界的程度。
4. constraint_penalty 是安全惩罚，不应被小误差收益抵消。
```

---

### Layer 3：离线感知辅助评分

定义 `J_perception`，分数越低越好。

```text
J_perception =
    v_main       * P_drop(acc_main)
  + v_turn       * P_drop(acc_turn)
  + v_transition * P_drop(acc_turn_transition)
  + v_theta      * N(theta_mae_deg)
  + v_stall      * P_drop(stall_recall)
  + v_slope      * P_drop(slope_recall)
  + v_edge       * N(theta_edge_p95_abs_err)
  + v_flatpeak   * N(flat_peak_theta_error)
```

其中：

```text
P_drop(metric) = max(0, baseline_metric - metric) / max(abs(baseline_metric), epsilon)
```

建议初始权重：

```text
v_main       = 0.15
v_turn       = 0.10
v_transition = 0.15
v_theta      = 0.15
v_stall      = 0.20
v_slope      = 0.10
v_edge       = 0.10
v_flatpeak   = 0.05
```

说明：

```text
1. stall_recall 权重较高，因为 stall 误判会影响安全。
2. transition 权重较高，因为转向过渡对路径跟踪影响大。
3. theta_edge 和 flat_peak 是闭环调度风险指标，不能被平均 theta_mae 掩盖。
```

---

### Layer 4：局部事件专项评分

定义若干局部评分：

```text
J_turn_event
J_stall_event
J_theta_event
J_smooth_event
```

示例：

```text
J_turn_event =
    N(transition_error_rate)
  + N(turn_delay_proxy)
  + N(ey_rmse_transition_if_available)

J_stall_event =
    P_drop(stall_recall)
  + N(stall_detection_delay_if_available)
  + N(constraint_touch_count_in_stall_if_available)

J_theta_event =
    N(theta_edge_p95_abs_err)
  + N(flat_peak_theta_error)
  + N(theta_jump_p95_if_available)

J_smooth_event =
    N(omega_cmd_rms)
  + N(delta_u_proxy)
  + N(theta_sched_smoothness_if_available)
```

如果某些指标当前不存在，Codex 应写明：

```text
metric_unavailable
reason
needed_artifact
future_action
```

不得用不存在的指标虚构分数。

---

## A1.5 总综合评分

定义：

```text
J_total = a * J_control + b * J_perception + c * J_event
```

第一版建议：

```text
a = 0.60
b = 0.25
c = 0.15
```

如果候选没有闭环结果：

```text
不能计算正式 J_control；
只能计算 J_perception + offline event proxy；
标记为 offline_proxy_only。
```

对于没有闭环结果的候选，定义：

```text
J_total_proxy = b * J_perception + c * J_event_proxy
```

但报告必须说明：

```text
该分数不能替代闭环验证。
```


# 4. Phase A2：metric weight version design + sensitivity analysis

## A2.1 为什么需要指标调优

新评价指标不是一次就完美。不同权重会影响排序。  
但指标调优必须遵守严格规则，防止变成“为了让某个实验赢而调指标”。

---

## A2.2 指标调优原则

Codex 必须遵守：

```text
1. 指标权重必须基于 AGV 控制目标，而不是基于某个候选结果。
2. 每次修改指标版本必须生成 metric_version。
3. 每个 metric_version 必须有变更原因。
4. 指标开发阶段和最终评估阶段必须分离。
5. 最终用于论文主结论的指标版本必须在最终重评估前冻结。
6. 冻结后不得因为结果不理想继续改权重。
```

---

## A2.3 指标版本管理

输出：

```text
results/modern_tcn_metric_rebuild/01_metric_design/metric_versions/
```

每个版本一个文件：

```text
metric_v0_baseline_gate.json
metric_v1_control_oriented.json
metric_v2_safety_heavy.json
metric_v3_smoothness_heavy.json
```

每个版本必须包含：

```json
{
  "metric_version": "metric_v1_control_oriented",
  "created_time": "...",
  "purpose": "...",
  "hard_constraints": {},
  "weights_control": {},
  "weights_perception": {},
  "weights_event": {},
  "normalization": {},
  "change_reason": "...",
  "allowed_use": "development_or_final"
}
```

---

## A2.4 指标调优流程

### Step A2.4.1：建立初始版本 v1

使用上述建议权重建立：

```text
metric_v1_control_oriented
```

目的：

```text
与最终路径跟踪目标对齐。
```

---

### Step A2.4.2：敏感性分析

建立两个敏感性版本：

```text
metric_v2_safety_heavy
metric_v3_smoothness_heavy
```

示例：

```text
v2_safety_heavy:
    提高 constraint_penalty、stall_recall、theta_edge 权重

v3_smoothness_heavy:
    提高 omega_cmd_rms、delta_u_proxy、theta_sched_smoothness 权重
```

目的：

```text
检验候选排序是否对权重极端敏感。
```

---

### Step A2.4.3：候选排序稳定性分析

对每个 metric_version 计算开发期 sensitivity 排名。

前置条件：

```text
metric_dictionary.csv 已冻结
hard_constraint_thresholds.json 已冻结
```

输出：

```text
results/modern_tcn_metric_rebuild/01_metric_design/metric_sensitivity_ranking.csv
results/modern_tcn_metric_rebuild/01_metric_design/metric_sensitivity_report.md
```

字段：

```text
candidate_id
metric_version
rank
J_total_or_proxy
J_control
J_perception
J_event
hard_constraint_status
notes
```

若某候选只在一个极端权重版本下胜出，则标记：

```text
rank_unstable
```

不得直接作为主方法。

---

### Step A2.4.4：提出待冻结版本

根据敏感性分析提出一个待冻结版本：

```text
metric_vFinal_control_oriented_candidate.json
```

输出：

```text
results/modern_tcn_metric_rebuild/01_metric_design/metric_final_candidate_report.md
results/modern_tcn_metric_rebuild/01_metric_design/metric_vFinal_control_oriented_candidate.json
```

候选报告必须说明：

```text
1. 为什么选择该权重；
2. 该权重如何对应路径跟踪、平滑性、安全性和 oracle gap；
3. 哪些指标是 hard constraints；
4. 哪些候选没有闭环结果，只能 proxy ranking；
5. 是否存在 rank_unstable 或 sensitivity-dependent 候选。
```

---

## A2.5 如何平衡“指标调优”和“实验结果调优”

Codex 必须采用以下规则：

```text
1. 指标调优阶段只允许使用 baseline、TCN、GRU、oracle 和历史候选的汇总结果，不允许单独为某个候选定制权重。
2. 指标调优的目标是让评分与控制目标一致，而不是让某个模型获胜。
3. 指标冻结前，可以比较多个权重版本的排序稳定性。
4. 指标冻结后，重新评估已有 5 个实验时不得再修改权重。
5. 如果冻结指标下没有候选胜出，不允许继续改指标；应进入环节 B 局部优化。
6. 如果某候选只因某个权重大幅调整而胜出，必须标记为 sensitivity-dependent，不可直接作为主结论。
7. 论文中应同时报告至少两个辅助排序：control-oriented score 和 original gate status。
```


# 5. Phase A3：metric freeze

## A3.1 冻结输入

冻结前必须确认以下文件已经存在并通过人工或脚本检查：

```text
results/modern_tcn_metric_rebuild/01_metric_design/metric_dictionary.csv
results/modern_tcn_metric_rebuild/02_metric_freeze/hard_constraint_thresholds.json
results/modern_tcn_metric_rebuild/01_metric_design/metric_vFinal_control_oriented_candidate.json
```

## A3.2 冻结输出

生成：

```text
results/modern_tcn_metric_rebuild/02_metric_freeze/metric_freeze_report.md
results/modern_tcn_metric_rebuild/02_metric_freeze/metric_vFinal_control_oriented_frozen.json
```

冻结报告必须说明：

```text
1. 为什么选择该权重；
2. 该权重如何对应路径跟踪、平滑性、安全性和 oracle gap；
3. 哪些指标是 hard constraints；
4. 哪些候选没有闭环结果，只能 proxy ranking；
5. 冻结后不得再修改指标来适配结果；
6. hard_constraint_thresholds.json 已在候选重排前冻结；
7. metric_dictionary.csv 已在候选重排前冻结。
```

## A3.3 冻结后禁止事项

```text
1. 不得根据重排结果修改 canonical metric。
2. 不得根据重排结果修改 hard constraint 数值阈值。
3. 不得根据重排结果修改 vFinal 权重。
4. 如发现字段缺失，只能记录 missing/unavailable，不能回填或改定义。
```


# 6. Phase A4：用冻结新指标重评估已有 5 个实验

## A4.1 候选收集

Codex 应从以下位置收集所有历史候选：

```text
results/modern_tcn_sci_innovation/01_loss_optimization/
results/modern_tcn_sci_innovation/02_hard_sample_loss/
results/modern_tcn_sci_innovation/03_physics_group_gate/
results/modern_tcn_sci_innovation/04_mode_conditioned_theta/
results/modern_tcn_sci_innovation/05_confidence_scheduling/
results/modern_tcn_sci_innovation/07_ablation_summary/
```

并可视情况加入：

```text
results/modern_tcn_ablation/
```

每个候选建立统一表：

```text
results/modern_tcn_metric_rebuild/03_rerank_existing_experiments/candidate_registry.csv
```

字段：

```text
candidate_id
source_phase
run_tag
model_family
loss_mode
checkpoint_path_if_available
has_offline_metrics
has_closed_loop_metrics
has_onnx
has_matlab
original_gate_status
original_promotion_status
notes
evidence_validity
actual_method
smoothness_loss_valid
scheduling_replay_valid
advisory_only
invalid_reason
repair_required_for_formal_use
```

E2/E5 字段填写规则：

```text
E2:
    evidence_validity = degraded
    actual_method = hard_sample_focal_only
    smoothness_loss_valid = false
    scheduling_replay_valid = not_applicable
    advisory_only = false
    invalid_reason = theta_smoothness_claim_invalid_not_run
    repair_required_for_formal_use = rerun_with_valid_theta_smoothness_loss_and_replay_capable_order

E5:
    evidence_validity = advisory_only
    actual_method = confidence_scheduling_offline_screen
    smoothness_loss_valid = not_applicable
    scheduling_replay_valid = false
    advisory_only = true
    invalid_reason = non_replay_capable_dataset_run_id_interleaved
    repair_required_for_formal_use = create_E5_replay_fixed_on_replay_capable_dataset
```

---

## A4.2 统一指标抽取

生成：

```text
results/modern_tcn_metric_rebuild/03_rerank_existing_experiments/candidate_metric_matrix.csv
```

字段包括：

```text
candidate_id
acc_main
acc_turn
acc_turn_transition
theta_mae_deg
flat_recall
stall_recall
slope_recall
theta_edge_p95_abs_err
flat_peak_theta_error
ey_rmse
xy_rmse
epsi_rmse
omega_cmd_rms
control_smoothness
delta_u_proxy
theta_sched_mae_deg
constraint_penalty
gap_to_oracle
closed_loop_available
metric_missing_notes
metric_missing_ratio
```

如果某指标缺失：

```text
写 NaN
记录原因
不得虚构
```

---

## A4.3 根据冻结指标打分

使用：

```text
metric_vFinal_control_oriented_frozen.json
metric_dictionary.csv
hard_constraint_thresholds.json
```

计算：

```text
J_control
J_perception
J_event
J_total
J_total_proxy
hard_constraint_status
rank_control
rank_proxy
```

E2/E5 降级处理：

```text
1. E2 只按 hard_sample_focal_only 候选计算，不得把 theta_smoothness_loss 写入有效实验因素。
2. E5 只能进入 advisory appendix / evidence_validity report。
3. E5 不得计算正式 J_control。
4. E5 不得进入正式 J_smooth_event 排名。
5. E5 不得进入 Class B 或 Class C。
6. 如果后续要正式评价 confidence scheduling，必须新增 E5_replay_fixed。
```

输出：

```text
results/modern_tcn_metric_rebuild/03_rerank_existing_experiments/rerank_results.csv
results/modern_tcn_metric_rebuild/03_rerank_existing_experiments/rerank_report.md
```

---

# 7. Phase A5：candidate decision

## A5.1 候选分类

Codex 将候选分为：

```text
Class A: 新指标下仍无价值
Class B: 离线 proxy 有潜力，但无闭环结果
Class C: 有闭环结果且 J_control 优于 baseline
Class D: 有局部指标亮点，但违反安全硬约束
Class E: 排名对权重高度敏感
```

分类标准：

```text
Class A:
    J_total_proxy 不优于 baseline，且无局部亮点。

Class B:
    J_total_proxy 优于 baseline 或进入 top 3，
    但没有闭环结果。

Class C:
    有闭环结果，
    hard constraints 通过，
    J_control 优于 baseline。

Class D:
    有 theta/transition 等亮点，
    但 stall、flat_peak、theta_edge 或 constraint 明显恶化。

Class E:
    只在某个权重版本下排名靠前，
    在 vFinal 下不稳定。
```

输出：

```text
results/modern_tcn_metric_rebuild/04_candidate_decision/candidate_classes.csv
results/modern_tcn_metric_rebuild/04_candidate_decision/candidate_decision_report.md
```

---

## A5.2 根据重评估结果采取不同对策

## 情况 A：发现 Class C 候选

含义：

```text
某个历史全局实验在新控制导向评价体系下确实优于 baseline，
且有闭环结果、通过 hard constraints。
```

处理：

```text
1. 将该候选作为 strict Class C global candidate。
2. 不需要立即进入局部优化。
3. 补齐 ONNX / MATLAB / 多路径 / 扰动验证。
4. 与 baseline、TCN、GRU、oracle 重新做完整对比。
5. 在论文中说明：旧 gate 下未晋级，但新控制导向评价显示其闭环价值。
```

输出：

```text
results/modern_tcn_metric_rebuild/04_candidate_decision/class_c_global_candidate.md
```

---

## 情况 B：发现 Class B 候选

含义：

```text
某个历史全局实验在 proxy score 下有潜力，
但没有闭环结果。
```

处理：

```text
1. 不可直接宣布成功。
2. 选择最多 2 个 Class B 候选进入 sandbox closed-loop。
3. sandbox 目录必须独立。
4. 若 sandbox 闭环优于 baseline，再补正式闭环。
5. 若 sandbox 不优于 baseline，进入环节 B 局部优化。
```

输出：

```text
results/modern_tcn_metric_rebuild/05_sandbox_closed_loop_if_needed/
```

sandbox 注意事项：

```text
不得写入旧 compare 目录。
不得替代 baseline。
不得在论文中作为正式结论，除非后续补齐 formal validation。
```

---

## 情况 C：只有 Class D 候选

含义：

```text
某些候选局部指标好，但违反安全保护。
```

处理：

```text
1. 不进入正式闭环。
2. 抽取其有价值的局部能力。
3. 用于指导环节 B 的局部 residual correction。
```

示例：

```text
如果 physics group gate 提升 transition，但破坏 stall：
    后续只让 physics branch 修正 turn_head，不影响 main_head。

如果 mode theta experts 降低 theta_mae，但 flat_peak 变差：
    后续只做 residual theta correction，并加入 flat_peak protection。
```

---

## 情况 D：所有候选都是 Class A/E

含义：

```text
新评价体系也无法证明已有全局实验有价值。
```

处理：

```text
1. 不继续全局算法重训。
2. 进入环节 B：局部 residual correction。
3. 报告中说明：全局改动在控制导向评价下仍无法稳定超越 ModernTCN_small。
```


# 8. 环节 B：局部优化实验

只有在环节 A 没有选出有效全局候选时，才执行环节 B。

---

## Phase B0：局部优化设计原则

局部优化的核心思想：

```text
保留当前 ModernTCN_small baseline；
冻结或弱冻结 baseline 主干；
新增小型、门控、任务专属 residual corrector；
只在 baseline 薄弱区域修正；
避免破坏 baseline 已经做对的样本。
所有 residual 输出必须默认接近 baseline；
不得使用共享 global residual 同时无差别影响所有 head。
```

禁止：

```text
1. 再做全局替换式模型；
2. 新模块无差别影响所有 head；
3. 重新调 loss 让所有任务一起漂移；
4. 放宽 hard constraints；
5. 为了通过新指标而过拟合某一个候选。
```

---

## Phase B1：构建 baseline error map

### B1.1 目标

识别 ModernTCN_small 的真实薄弱区域。

### B1.2 输出

```text
results/modern_tcn_metric_rebuild/06_local_residual_optimization_if_needed/01_baseline_error_map/baseline_error_map.csv
results/modern_tcn_metric_rebuild/06_local_residual_optimization_if_needed/01_baseline_error_map/error_map_report.md
```

字段：

```text
sample_id
run_id_if_available
main_true
main_pred
turn_true
turn_pred
theta_true
theta_pred
theta_abs_err
is_main_error
is_turn_error
is_transition_window
is_stall
is_slope
is_flat
is_theta_edge
is_flat_peak
main_conf
turn_conf
theta_error_rank
input_feature_stats
```

### B1.3 必须回答

```text
1. baseline 错误是否集中在 turn transition？
2. stall 错误是否集中在特定电流/速度组合？
3. theta 大误差是否集中在 slope edge 或 flat peak？
4. baseline 低置信度是否能预测错误？
5. baseline 高置信度错误占比多少？
```

---

## Phase B2：Residual Turn Corrector

### B2.1 目标

只修正 turn_head，不碰 main 和 theta。

### B2.2 结构

```text
baseline_model = pretrained ModernTCN_small
baseline_model frozen

main_logits = main_logits_0
theta_hat = theta_0
turn_logits = turn_logits_0 + g_turn * delta_turn_logits
```

实现约束：

```text
baseline frozen
main_logits = main_logits_0
theta_hat = theta_0
only turn_logits receives residual correction
```

其中：

```text
g_turn = sigmoid(gate_turn)
gate_turn 初始化 bias = -4
```

保证初始输出接近 baseline。

### B2.3 训练目标

```text
L =
  L_turn(final)
+ lambda_preserve * KL(turn_logits_final || turn_logits_0) on baseline-correct samples
+ lambda_gate * mean(g_turn)
+ lambda_transition * transition_weighted_CE
```

### B2.4 判断标准

必须满足：

```text
acc_turn_transition >= baseline
acc_turn >= baseline - 0.005
main 指标完全等于 baseline 或不变
theta 指标完全等于 baseline 或不变
```

如果失败：

```text
说明 turn transition 不是简单 residual 可修正；
停止该分支。
```

---

## Phase B3：Residual Theta Corrector

### B3.1 目标

只修正 theta，不碰 main 和 turn。

### B3.2 结构

```text
baseline_model = pretrained ModernTCN_small
baseline_model frozen

main_logits = main_logits_0
turn_logits = turn_logits_0
theta_hat = theta_0 + g_theta * delta_theta
```

实现约束：

```text
baseline frozen
main_logits = main_logits_0
turn_logits = turn_logits_0
only theta_hat receives residual correction
```

### B3.3 保护损失

```text
L =
  L_theta(final)
+ lambda_preserve * |theta_hat - theta_0| on baseline-good samples
+ lambda_gate * mean(g_theta)
+ lambda_flat * flat_peak_protection
+ lambda_edge * theta_edge_protection
```

### B3.4 判断标准

必须满足：

```text
theta_mae_deg <= baseline
theta_edge_p95_abs_err <= baseline
flat_peak_theta_error <= baseline
main/turn 完全不变
```

如果 theta_mae 下降但 edge/flat_peak 变坏：

```text
停止，不进入闭环。
```

---

## Phase B4：Head-Specific Physics Residual Corrector

### B4.1 目标

把 E3 中有价值的物理分组能力改造成任务专属 correction，而不是全局 residual。

### B4.2 结构

```text
baseline_model = pretrained ModernTCN_small
baseline_model frozen_or_weak_frozen

h_base = ModernTCN_small_trunk(x)
h_phys = physics_group_branch(x)

main_logits = main_logits_0 + g_main * delta_main_logits
turn_logits = turn_logits_0 + g_turn * delta_turn_logits
theta_hat = theta_0 + g_theta * delta_theta
```

约束：

```text
g_main 初始最小；
g_turn 可相对更大；
g_theta 受 flat/edge protection 约束；
物理分支不得无差别影响所有 head。
each head has independent gate；
no shared global residual that affects all heads equally。
```

### B4.3 判断标准

必须同时优于或不劣于：

```text
baseline
Residual Turn Corrector
Residual Theta Corrector
```

否则不作为最终模型。

---

# 9. 局部优化与新指标的关系

局部优化的训练和筛选也必须使用冻结指标：

```text
metric_vFinal_control_oriented_frozen.json
```

不得因为局部优化结果不理想重新修改指标。

局部优化报告必须包含：

```text
1. 原始 gate status
2. new control-oriented score
3. local event score
4. hard constraint status
5. 与 baseline 的变化
6. 与历史 5 个全局实验候选的变化
```


# 10. 最终决策树

Codex 最终按以下决策树输出结论：

```text
Start
 |
 |-- A0: 锁定 baseline 和历史实验结果
 |
 |-- A1: 冻结 metric dictionary + hard thresholds
 |
 |-- A2: 设计 metric weight versions + sensitivity analysis
 |
 |-- A3: freeze metric_vFinal_control_oriented_frozen
 |
 |-- A4: 用冻结指标重评估已有 5 个实验
 |
 |-- A5: candidate decision
       |
       |-- 有 Class C 候选？
       |       |
       |       |-- Yes:
       |       |       进入 formal validation；
       |       |       暂停局部优化；
       |       |       输出 strict Class C global candidate。
       |       |
       |       |-- No:
       |               |
       |               |-- 有 Class B 候选？
       |                       |
       |                       |-- Yes:
       |                       |       进入 sandbox closed-loop；
       |                       |       若 sandbox 成功，补 formal validation；
       |                       |       若失败，进入局部优化。
       |                       |
       |                       |-- No:
       |                               进入局部优化。
 |
 |-- Phase B: 局部 residual correction
       |
       |-- Residual Turn 成功？
       |-- Residual Theta 成功？
       |-- Head-Specific Physics 成功？
       |
       |-- 若有成功：
       |       进入 ONNX / MATLAB / closed-loop。
       |
       |-- 若都失败：
               维持 ModernTCN_small 为最优；
               论文创新点转向评价体系、负结果分析或 MPC cost adaptation。
```

---

# 11. 最终报告要求

生成：

```text
results/modern_tcn_metric_rebuild/07_final_report/final_metric_rebuild_and_local_optimization_report.md
results/modern_tcn_metric_rebuild/07_final_report/final_decision.json
results/modern_tcn_metric_rebuild/07_final_report/master_candidate_ranking.csv
results/modern_tcn_metric_rebuild/07_final_report/metric_version_history.csv
```

报告必须回答：

```text
1. 新评价体系如何构建？
2. 新评价体系与 AGV 路径跟踪目标如何对应？
3. 指标权重如何调优并冻结？
4. 指标调优是否存在 candidate-specific bias？
5. metric_dictionary.csv 和 hard_constraint_thresholds.json 是否在候选排名前冻结？
6. E2/E5 的证据降级如何处理？
7. 之前 5 个全局实验在新指标下如何分层？
8. 是否有严格 Class C 全局候选？
9. 是否更可能只是 Class B/D？
10. Class B 是否仅进入 sandbox？
11. Class D 是否仅用于指导局部优化？
12. 是否需要进入局部优化？
13. 局部 residual correction 是否带来收益？
14. 最终是否替代 ModernTCN_small？
15. 如果没有替代，为什么？
16. 哪些结果可以写入论文？
```

---

# 12. Codex 硬性停止条件

遇到以下情况必须停止：

```text
1. 当前 baseline 无法锁定。
2. 候选排名前未冻结 metric_dictionary.csv。
3. 候选排名前未冻结 hard_constraint_thresholds.json。
4. 指标冻结前未生成 metric_version。
5. 指标冻结后仍修改权重。
6. 为某个候选单独定制权重。
7. 缺失指标被虚构填充。
8. 无闭环结果的候选被宣称闭环优于 baseline。
9. E2 被用于证明 theta_smoothness_loss 有效或无效。
10. E5 被用于正式 J_control / J_smooth_event 排名。
11. 新分析覆盖历史实验结果。
12. 局部优化修改了 baseline small 默认行为。
13. sandbox 结果被写入 formal compare。
14. 未通过 hard constraints 的候选被列为最终主方法。
```

---

# 13. 最简执行摘要

Codex 应按以下顺序执行：

```text
1. 锁定 baseline 和历史 5 个实验结果。
2. 建立并冻结 metric_dictionary.csv。
3. 建立并冻结 hard_constraint_thresholds.json。
4. 构建 metric weight versions 并做敏感性分析。
5. 冻结 metric_vFinal_control_oriented_frozen.json。
6. 用冻结指标重新评估已有 5 个全局实验。
7. 将候选分为 Class A/B/C/D/E。
8. 若发现严格 Class C，进入 formal validation。
9. 若只有 Class B，最多选择 2 个进入 sandbox。
10. 若只有 Class D/A/E，进入局部 residual correction 或维持 baseline。
11. 局部优化只做 baseline-preserving、head-specific、gated residual correction。
12. 所有结果按新指标、证据有效性和原始 gate 三重报告。
13. 不因结果不理想而再次修改指标。
```

本轮核心思想：

```text
先判断“过去的全局改动是否只是被旧离线 gate 错杀”，
再决定是否需要“局部 residual correction”。
```

若重新评价后已有全局候选有效，则优先保留全局改动作为论文方法；  
若重新评价后仍无有效结果，再进入局部优化，避免盲目增加实验复杂度。

报告必须明确：

```text
本轮大概率不会直接产生 Class C；
更可能产生 Class B/D；
Class B 只能进入 sandbox；
Class D 只能指导局部优化。
```
