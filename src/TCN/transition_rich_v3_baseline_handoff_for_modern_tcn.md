# Transition-Rich v3 Baseline Handoff for ModernTCN

更新时间：2026-05-02

## 1. 当前阶段结论

PG-TCN 仍只作为消融，不作为主线。当前主线对比基线为：

```text
GRU strong baseline
TCN staged baseline
TCN calibrated single-checkpoint upper bound
```

V3 数据集固定为：

```text
data/tcn/TCN_dataset_v3_transition_rich.mat
```

后续 ModernTCN 必须继续使用该数据集、同一 run-level split、同一 19 维输入特征、同一标签定义和同一测试集，不再修改路径/数据。

## 2. GRU Strong Baseline

来源：

```text
results/tcn/experiments/transition_rich_v3_seed*/TCN_GRU_transition_rich_v3_summary.csv
```

使用 seeds：

```text
11, 21, 42, 73, 101
```

### 2.1 多 seed 均值

| metric | GRU mean | GRU std |
|---|---:|---:|
| acc_main | 0.9400 | 0.0050 |
| acc_turn | 0.8875 | 0.0104 |
| acc_turn_transition | 0.6870 | 0.0381 |
| theta_mae_deg | 0.4195 | 0.0653 |
| flat_recall | 0.9070 | 0.0086 |
| stall_recall | 0.9161 | 0.0275 |
| slope_recall | 0.9715 | 0.0066 |
| uphill_recall | 0.9623 | 0.0065 |
| downhill_recall | 0.9857 | 0.0079 |

### 2.2 当前 GRU 最优单模型

按 `acc_main` 和 `theta_mae_deg` 综合看，当前最强单次为 seed73：

| metric | value |
|---|---:|
| seed | 73 |
| best_epoch | 14 |
| acc_main | 0.9459 |
| acc_turn | 0.8852 |
| acc_turn_pure | 0.9146 |
| acc_turn_transition | 0.6923 |
| theta_mae_deg | 0.3437 |
| flat_recall | 0.9151 |
| stall_recall | 0.9463 |
| slope_recall | 0.9720 |
| uphill_recall | 0.9598 |
| downhill_recall | 0.9911 |

文件：

```text
data/models/GRU_model_transition_rich_v3_seed73_h96_l2_inputstats.mat
data/models/GRU_meta_transition_rich_v3_seed73_h96_l2_inputstats.mat
results/tcn/experiments/transition_rich_v3_seed73/gru_h96_l2_inputstats/GRU_train_report.md
```

## 3. TCN Staged Baseline

来源：

```text
results/tcn/experiments/transition_rich_v3_seed*/TCN_GRU_transition_rich_v3_summary.csv
```

### 3.1 多 seed 均值

| metric | TCN mean | TCN std |
|---|---:|---:|
| acc_main | 0.9052 | 0.0350 |
| acc_turn | 0.9063 | 0.0027 |
| acc_turn_transition | 0.7830 | 0.0115 |
| theta_mae_deg | 0.4490 | 0.0846 |
| flat_recall | 0.8594 | 0.0523 |
| stall_recall | 0.9688 | 0.0168 |
| slope_recall | 0.9350 | 0.0458 |
| uphill_recall | 0.9104 | 0.0511 |
| downhill_recall | 0.9732 | 0.0389 |

结论：

- TCN 稳定强于 GRU 的指标是 `acc_turn` 和 `acc_turn_transition`。
- GRU 稳定强于 TCN 的指标是 `acc_main`、`flat_recall`、`slope_recall` 和 `theta_mae_deg`。
- TCN 的主要问题不是转弯，而是 flat/slope 主工况边界不稳定。

### 3.2 当前 TCN staged 最均衡单模型

按原始 V3 staged 多 seed 结果，seed101 是最均衡的 TCN 单模型：

| metric | value |
|---|---:|
| seed | 101 |
| best_epoch | 79 |
| acc_main | 0.9326 |
| acc_turn | 0.9056 |
| acc_turn_pure | 0.9219 |
| acc_turn_transition | 0.7984 |
| theta_mae_deg | 0.4077 |
| flat_recall | 0.9101 |
| stall_recall | 0.9805 |
| slope_recall | 0.9448 |
| uphill_recall | 0.9185 |
| downhill_recall | 0.9857 |

文件：

```text
data/models/TCN_model_transition_rich_v3_seed101_staged.mat
data/models/TCN_meta_transition_rich_v3_seed101_staged.mat
results/tcn/experiments/transition_rich_v3_seed101/tcn_staged/TCN_train_report.md
```

## 4. TCN Calibrated Single-Checkpoint Upper Bound

自动参数筛选中，`base_comp_flat120` 在 confirm/validate 阶段给出了更好的单模型结果，但 full 复跑和后续 stability screen 表明该训练 recipe 不稳定。因此该模型只能作为 TCN 当前单 checkpoint 上限参考，不能作为稳定多 seed 结论。

### 4.1 推荐保留的 calibrated 单模型

`base_comp_flat120` validate seed73：

| metric | value |
|---|---:|
| seed | 73 |
| best_epoch | 83 |
| base_best_epoch | 54 |
| acc_main | 0.9442 |
| acc_turn | 0.9077 |
| acc_turn_pure | 0.9264 |
| acc_turn_transition | 0.7851 |
| theta_mae_deg | 0.3998 |
| flat_recall | 0.9233 |
| stall_recall | 0.9756 |
| slope_recall | 0.9574 |
| uphill_recall | 0.9564 |
| downhill_recall | 0.9589 |

文件：

```text
data/models/TCN_model_transition_rich_v3_auto_validate_base_comp_flat120_seed73.mat
data/models/TCN_meta_transition_rich_v3_auto_validate_base_comp_flat120_seed73.mat
results/tcn/experiments/transition_rich_v3_auto_screen/validate/base_comp_flat120/seed73/TCN_train_report.md
```

### 4.2 theta 最优 calibrated 单模型

`base_comp_flat120` confirm seed42：

| metric | value |
|---|---:|
| seed | 42 |
| best_epoch | 81 |
| base_best_epoch | 60 |
| acc_main | 0.9365 |
| acc_turn | 0.8982 |
| acc_turn_transition | 0.7586 |
| theta_mae_deg | 0.3505 |
| flat_recall | 0.9176 |
| stall_recall | 0.9805 |
| slope_recall | 0.9462 |
| uphill_recall | 0.9323 |
| downhill_recall | 0.9679 |

文件：

```text
data/models/TCN_model_transition_rich_v3_auto_confirm_base_comp_flat120_seed42.mat
data/models/TCN_meta_transition_rich_v3_auto_confirm_base_comp_flat120_seed42.mat
results/tcn/experiments/transition_rich_v3_auto_screen/confirm/base_comp_flat120/seed42/TCN_train_report.md
```

注意：该结果后续无法稳定复现，不应用作正式多 seed baseline。

## 5. 最近 seed42 selection stability 结果

入口：

```matlab
run_TCN_v3_selection_stability_screen(42)
```

输出：

```text
results/tcn/experiments/transition_rich_v3_selection_stability/TCN_v3_selection_stability_summary.csv
```

结果：

| config | acc_main | flat_recall | slope_recall | turnT | theta_mae_deg | pass |
|---|---:|---:|---:|---:|---:|---:|
| flat120_comp_ref | 0.8617 | 0.9349 | 0.7876 | 0.7772 | 0.5394 | 0 |
| flat120_base_main_guard | 0.8635 | 0.8599 | 0.8539 | 0.7798 | 0.9087 | 0 |
| flat120_comp_guard_s090 | 0.8670 | 0.8937 | 0.8337 | 0.7533 | 0.6102 | 0 |
| flat115_comp_guard_s092 | 0.8484 | 0.8599 | 0.8246 | 0.7719 | 1.1389 | 0 |
| flat110_slope100_guard | 0.8621 | 0.8961 | 0.8218 | 0.7905 | 0.5700 | 0 |

判定：

- 没有候选满足进入 3 seed 验证的门槛。
- 不继续 selection stability 的 3 seed 或 5 seed。
- seed42 反复出问题不是数据重写或 split 改变，而是训练轨迹进入坏 basin；同一 cfg 除输出路径外一致，confirm good 与后续 bad 的 history 明显不同。

## 6. ModernTCN 比较门槛

ModernTCN 第一阶段只跑 seed42。进入 3 seed 的最低门槛：

```text
acc_main >= 0.90
flat_recall >= 0.90
slope_recall >= 0.88
acc_turn_transition >= 0.75
theta_mae_deg <= 0.70
```

若 seed42 过线，再跑：

```text
seeds = [42, 73, 101]
```

进入完整 5 seed 的推荐目标：

```text
acc_main mean >= 0.93
flat_recall mean >= 0.90
slope_recall mean >= 0.94
acc_turn_transition mean >= 0.77
theta_mae_deg mean <= 0.43
```

最终要同时对比：

```text
GRU strong baseline mean/std
TCN staged baseline mean/std
TCN calibrated single-checkpoint upper bound
ModernTCN mean/std
```

## 7. PyTorch -> ONNX -> MATLAB 要求

当前本机 MATLAB 为 R2024b，存在以下函数：

```text
importONNXNetwork
importONNXLayers
importNetworkFromONNX
exportONNXNetwork
```

因此 PyTorch -> ONNX -> MATLAB 路线可行。实现要求：

1. Python 端必须使用固定 V3 数据集导出的 train/val/test，不重新划分 split。
2. 不在 Python 中重新拟合 scaler；使用 MAT 文件中已有的 scaler 或导出的归一化后 X。
3. 输入特征固定为 19 维，窗口长度固定为 128。
4. 输出固定为 `logits_main`、`logits_turn`、`theta_hat`。MATLAB 端再做 softmax 和标签映射。
5. ONNX 模型尽量只使用标准算子：Conv1d、Linear、ReLU/GELU、BatchNorm/LayerNorm、Add、Mul、Mean、Concat、Transpose、Reshape。
6. 避免自定义 CUDA op、复杂 dynamic control flow、Python-only layer、非标准 padding。
7. export 前必须 `model.eval()`，禁用 dropout/stochastic depth。
8. ONNX opset 建议从 17 开始；如果 MATLAB import 报算子不支持，再降级或替换算子。
9. 导出后必须做三方一致性检查：

```text
PyTorch output
ONNXRuntime output
MATLAB imported network output
```

推荐容差：

```text
max_abs_error <= 1e-4
mean_abs_error <= 1e-5
```

10. MATLAB 集成前先只做离线 test set 推理，不直接进入 Simulink。

## 8. ModernTCN 第一版训练配置建议

第一版不要追求大模型，建议 `ModernTCN-small`：

```text
input: [batch, time=128, features=19]
channels: 64 or 96
blocks: 4-6
large kernel: 15-31
dropout: 0.10-0.20
heads:
  main classifier: 3 classes
  turn classifier: 3 classes
  theta regressor: 1 scalar, rad
```

损失和评估必须对齐当前 TCN：

```text
L = L_main + lambda_turn * L_turn + lambda_theta * L_theta + lambda_theta_flat * L_theta_flat
```

第一版建议：

```text
lambda_turn = 0.05
lambda_theta = 0.35
lambda_theta_flat = 0.20
main_class_multipliers = [1.20, 1.00, 0.95] or [1.10, 1.00, 1.00]
turn_class_multipliers = [1.00, 1.10, 1.00]
```

ModernTCN 的重点观察不是单次最高分，而是 seed42 是否不再出现 TCN baseline 中的 flat/slope 崩塌。
