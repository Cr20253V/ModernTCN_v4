# TCN 临时最优模型与 GRU 对照计划

更新时间: 2026-04-26

## 1. 当前结论

当前建议把 `staged_bestbase_inputstats_turn_lam050` 作为 TCN 阶段的临时最优候选，用于先跑通 TCN 与 GRU 的公平对照流程。

这个结论不是论文最终最优解。原因是当前数据规模仍偏小，且同一推荐基座配置直接重训时出现过明显随机波动：`main_recovery_best` 直接重训只得到主工况 0.915、转弯 0.807、坡度 MAE 1.298 deg。因此现阶段更稳妥的定位是：先冻结一个综合表现较好的 TCN 候选，完成 GRU 对照链路；后续扩充数据集后，对 TCN 和 GRU 同时做多 seed、多 split 的统计验证。

## 2. 临时最优模型

候选名称:

`staged_bestbase_inputstats_turn_lam050`

模型文件:

`data/models/TCN_model_staged_bestbase_v1_staged_bestbase_inputstats_turn_lam050.mat`

元信息文件:

`data/models/TCN_meta_staged_bestbase_v1_staged_bestbase_inputstats_turn_lam050.mat`

训练报告:

`results/tcn/experiments/staged_bestbase_v1/staged_bestbase_inputstats_turn_lam050/TCN_train_report.md`

流水线汇总:

`results/tcn/experiments/staged_bestbase_v1/TCN_auto_experiment_pipeline_report.md`

## 3. 训练配置

推荐配置入口:

```matlab
init_project;
cfg = TCN_recommended_cfg('production_current');
[model, meta] = TCN_train(cfg);
```

或者通过自动实验流水线复现实验:

```matlab
init_project;
cfg = struct;
cfg.max_epochs = 90;
cfg.batch_size = 64;
cfg.use_gpu = true;
cfg.case_filter = {'staged_combo'};
cfg.run_tag = 'staged_bestbase_v1';
cfg.skip_existing = false;
summary = TCN_auto_experiment_pipeline(cfg);
```

关键参数:

| 参数 | 当前值 | 说明 |
|---|---:|---|
| `mode` | `physics_guided` | 多任务物理约束训练模式 |
| `max_epochs` | 90 | 最大训练轮数 |
| `batch_size` | 64 | batch 大小 |
| `head_pooling` | `last_mean_max_inputstats` | TCN readout 拼接最后时刻、均值、最大值和窗口输入统计特征 |
| `best_metric` | `turn_priority` | staged 阶段优先选择转弯表现，同时设置主工况/坡度底线 |
| `base_best_metric` | `composite` | 基座阶段综合选择 |
| `combine_base_and_turn_best` | 1 | 组合主任务基座和转弯微调候选 |
| `main_neg_slope_weight` | 4.0 | 下坡 slope 主分类样本权重 |
| `select_downhill_error_weight` | 0.25 | 下坡选模惩罚权重 |
| `lambda_turn` | 0.05 | 基座阶段转弯损失权重 |
| `turn_head_type` | `mlp` | 转弯头使用 MLP |
| `turn_head_source` | `inputstats` | 转弯头使用窗口输入统计特征 |
| `turn_head_hidden` | 64 | 转弯 MLP 隐层宽度 |
| `turn_class_multipliers` | `[1.0 1.10 1.0]` | `[right straight left]` 类别乘子 |
| `turn_finetune_start_epoch` | 64 | staged 转弯微调起始轮次 |
| `turn_finetune_lambda_turn` | 0.50 | staged 阶段转弯损失权重 |
| `turn_finetune_disable_other_losses` | 1 | staged 阶段只优化转弯头相关损失 |
| `selection_start_epoch` | 64 | 选模起始轮次 |
| `early_stop_min_epochs` | 75 | 最小训练轮次 |
| `select_main_floor` | 0.92 | 转弯优先选模时的主工况底线 |
| `select_theta_floor_deg` | 1.20 | 转弯优先选模时的坡度 MAE 底线 |
| `select_downhill_floor` | 0.80 | 转弯优先选模时的下坡 recall 底线 |
| `grad_clip_mode` | `global` | 全局梯度裁剪 |

## 4. 测试表现

测试集结果:

| 指标 | 数值 |
|---|---:|
| best epoch | 60 |
| base best epoch | 62 |
| 主工况准确率 | 0.9303 |
| 转弯准确率 | 0.8989 |
| 转弯纯窗口准确率 | 0.9257 |
| 转弯过渡窗口准确率 | 0.6341 |
| 坡度 MAE | 0.7380 deg |
| 平地 recall | 0.9585 |
| 停滞 recall | 0.7778 |
| 坡道 recall | 0.9012 |
| 上坡 recall | 0.9173 |
| 下坡 recall | 0.8276 |
| flat -> slope 误判率 | 0.0189 |
| slope 符号准确率 | 0.9877 |

主工况混淆矩阵:

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 254 | 6 | 5 | 0.9585 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 4 | 12 | 146 | 0.9012 |

主工况 precision:

| pred class | precision |
|---|---:|
| flat | 0.9769 |
| stall | 0.4375 |
| slope | 0.9542 |

转弯混淆矩阵:

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 62 | 7 | 3 | 0.8611 |
| straight | 10 | 273 | 8 | 0.9381 |
| left | 5 | 12 | 65 | 0.7927 |

转弯 precision:

| pred class | precision |
|---|---:|
| right | 0.8052 |
| straight | 0.9349 |
| left | 0.8553 |

坡度子项:

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9173 | 0.5961 | 1.0000 | [2.884, 7.500] | [2.918, 10.394] |
| downhill | 29 | 0.8276 | 1.3885 | 0.9310 | [-5.500, -2.298] | [-7.101, 3.923] |

## 5. 与其他候选的关系

`main_recovery_grid_v2` 中主工况最强的基座配置是:

`main_neg4p0_down0p25_turn0p20_global_linear_readout`

该配置曾达到主工况 0.9438、转弯 0.8225、坡度 MAE 0.8038 deg。它适合作为“主工况优先”的 TCN 基座参考。

当前 staged 候选牺牲了约 1.3 个百分点主工况准确率，换来了约 7.6 个百分点转弯准确率提升，并且坡度 MAE 也更低。因此对当前多任务目标而言，`staged_bestbase_inputstats_turn_lam050` 更适合作为临时综合候选。

需要注意: `main_recovery_best` 直接重训曾掉到主工况 0.9146、转弯 0.8067、坡度 MAE 1.298 deg，说明当前实验仍存在随机性和小样本不稳定。后续论文结果不能只引用单次训练。

## 6. 数据与预处理要点

当前 TCN/GRU 应复用同一窗口数据和同一 run-level split:

`data/tcn/TCN_dataset_processed.mat`

共享切分文件:

`data/tcn/TCN_GRU_shared_run_split.mat`

预处理脚本:

`src/TCN/TCN_prepare_dataset.m`

关键预处理约定:

| 项目 | 当前做法 |
|---|---|
| 切分策略 | run-level split，避免同一 run 的窗口同时进入 train/val/test |
| 转弯窗口标签 | `tail_majority` |
| 转弯尾部长度 | `turn_tail_sec = 0.50` |
| 转弯低纯度样本 | 通过 `turn_sample_weight_*` 降权 |
| 转弯纯度记录 | `turn_purity_*` 和 `turn_transition_*` |
| GRU 公平对照 | 必须使用同一 `X_train/X_val/X_test`、同一标签、同一 scaler、同一 split |

当前数据规模和短板:

| 项目 | 数量/现象 |
|---|---:|
| train/val/test windows | 1875 / 424 / 445 |
| test flat/stall/slope | 265 / 18 / 162 |
| test right/straight/left | 72 / 291 / 82 |
| test negative/positive slope | 29 / 133 |
| test transition turn ratio | 约 0.092 |

诊断脚本 `TCN_diagnose_dataset.m` 的传统模型基线显示，窗口统计特征下主工况和转弯本身是可分的: bagged trees 主工况约 0.9685，转弯约 0.9596。这说明当前主要问题不是标签完全不可分，而是神经模型训练稳定性、样本量、任务权重和模型结构之间的折中。

## 7. GRU 对照实验必须保持一致的内容

为了让 TCN/GRU 对比公平，GRU 部分至少需要保持以下一致:

1. 同一数据文件: `data/tcn/TCN_dataset_processed.mat`。
2. 同一 run-level split: 复用 `dataset.split_info` 或 `data/tcn/TCN_GRU_shared_run_split.mat`。
3. 同一输入特征和 scaler: 不重新拟合测试集归一化，不单独改 GRU 特征列。
4. 同一窗口长度和 stride: 不为 GRU 单独换窗口，除非作为额外消融实验单独报告。
5. 同一任务定义: 主工况三分类、转弯三分类、坡度回归。
6. 同一转弯标签策略: `tail_majority`。
7. 同一低纯度转弯样本处理: 读取并使用 `turn_sample_weight_train`，至少在报告中说明是否使用。
8. 同一主指标: `acc_main`、`acc_turn`、`acc_turn_pure`、`acc_turn_transition`、`theta_mae_deg`。
9. 同一子项指标: flat/stall/slope recall，uphill/downhill recall 和 theta MAE。
10. 同一报告格式: 混淆矩阵、precision/recall、模型文件、meta 文件、训练配置。

## 8. GRU 建议实现方向

GRU 不应照搬 TCN 的 staged 训练细节，但应保留相同任务目标，并发挥循环模型对时间顺序建模的优势。

建议的第一版 GRU:

| 模块 | 建议 |
|---|---|
| 输入 | `X_train/X_val/X_test`，格式统一为 batch x time x feature |
| 主干 | 1 到 2 层 GRU，hidden size 64 或 96 |
| pooling | last hidden + mean pooling，必要时拼接 inputstats |
| 多任务头 | main classifier、turn classifier、theta regressor |
| 损失 | main CE + lambda_turn * turn CE + lambda_theta * theta MSE/Huber |
| 类别权重 | 主工况 balanced；转弯先 none，再测试 balanced/sqrt_inverse |
| 下坡处理 | 复用 TCN 的 `main_neg_slope_weight` 思路 |
| 梯度裁剪 | global clip，阈值 5 |
| 选模 | 先 composite，再增加 turn_priority 作为消融 |

建议先跑的 GRU 最小候选:

| case | 目的 |
|---|---|
| `gru_base_last_mean` | 公平基线，last hidden + mean pooling |
| `gru_inputstats_head` | 与 TCN 最强 head 对齐，拼接窗口统计特征 |
| `gru_hidden96` | 检查容量是否不足 |
| `gru_turn_lam005/010/020` | 检查转弯损失权重 |
| `gru_staged_turn` | 如果转弯低于 TCN，再尝试冻结/半冻结主干后转弯微调 |

## 9. GRU 下一步执行计划

第一步: 建立 GRU 训练脚本和报告脚本。

建议文件:

- `src/GRU/GRU_train.m`
- `src/GRU/GRU_recommended_cfg.m`
- `src/GRU/GRU_auto_experiment_pipeline.m`
- `results/gru/experiments/<run_tag>/...`

第二步: 用同一 TCN 数据集跑通单组 GRU。

目标不是马上超过 TCN，而是确认数据读取、标签、loss、metric 和报告完全对齐。

第三步: 小范围自动实验。

建议先扫:

```matlab
cfg.hidden_sizes = [64 96];
cfg.num_layers = [1 2];
cfg.lambda_turns = [0.05 0.10 0.20];
cfg.head_poolings = {'last_mean', 'last_mean_inputstats'};
cfg.grad_clip_modes = {'global'};
```

第四步: 固定 TCN 与 GRU 的对照表。

最低要求表头:

| model | case | seed | acc_main | acc_turn | acc_turn_pure | acc_turn_transition | theta_mae_deg | flat_recall | stall_recall | slope_recall | uphill_recall | downhill_recall |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|

第五步: 数据扩充后重新训练。

当前结果可以支撑“流程与方法可行”，但不足以作为论文最终强结论。扩充数据后应同时重训 TCN 和 GRU，并至少报告:

- 3 到 5 个随机 seed 的 mean ± std。
- 至少 1 组固定 split 的公平对照。
- 如果数据量足够，再加多 split 或跨 run 泛化验证。
- 对 stall、downhill、turn transition 这些少样本子项单独报告。

## 10. 当前建议

短期内不要继续大范围只调 TCN 参数。更高优先级是:

1. 冻结 `staged_bestbase_inputstats_turn_lam050` 作为 TCN 临时候选。
2. 跑通 GRU 使用同一数据集、同一 split、同一指标的训练和报告。
3. 完成 TCN vs GRU 的第一版对照表。
4. 再扩充训练数据集，尤其补足 stall、downhill 和转弯过渡窗口。
5. 最后对两个模型一起做多 seed/多 split 自动实验。

如果需要把 staged 候选提升为默认 `TCN_model.mat`，可以运行:

```matlab
copyfile('data/models/TCN_model_staged_bestbase_v1_staged_bestbase_inputstats_turn_lam050.mat', ...
         'data/models/TCN_model.mat');
copyfile('data/models/TCN_meta_staged_bestbase_v1_staged_bestbase_inputstats_turn_lam050.mat', ...
         'data/models/TCN_meta.mat');
```
