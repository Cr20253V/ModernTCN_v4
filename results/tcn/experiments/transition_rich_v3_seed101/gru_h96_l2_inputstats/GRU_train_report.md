# GRU 训练报告

- 生成时间: 2026-04-29 05:12:43
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_transition_rich_v3_seed101_h96_l2_inputstats.mat`
- 最佳轮次: 14
- 最佳验证损失: 0.143640
- 最佳选择分数: 0.203400
- 主任务基座选择分数: 0.203400
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.050, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.000, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`none`
- 转弯类别乘子 [right straight left]: [1.000 1.100 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 128 steps / 1.280 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.177280 |
| 主工况准确率 | 0.9330 |
| 转弯准确率 | 0.8989 |
| 转弯纯窗口准确率 | 0.9296 |
| 转弯过渡窗口准确率 | 0.6976 |
| 坡度 MAE deg | 0.4339 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 1085 | 51 | 77 | 0.8945 |
| stall | 8 | 191 | 6 | 0.9317 |
| slope | 38 | 11 | 1382 | 0.9658 |

| pred class | precision |
|---|---:|
| flat | 0.9593 |
| stall | 0.7549 |
| slope | 0.9433 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 481 | 34 | 3 | 0.9286 |
| straight | 104 | 1686 | 61 | 0.9109 |
| left | 0 | 86 | 394 | 0.8208 |

| pred class | precision |
|---|---:|
| right | 0.8222 |
| straight | 0.9336 |
| left | 0.8603 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.516, 8.153] deg
- Slope 符号准确率: 1.0000

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 871 | 0.9575 | 0.4354 | 1.0000 | [2.006, 7.500] | [0.538, 8.153] |
| downhill | 560 | 0.9786 | 0.4314 | 1.0000 | [-5.500, -2.046] | [-6.516, -1.428] |
