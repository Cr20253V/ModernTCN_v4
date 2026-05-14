# TCN 训练报告

- 生成时间: 2026-04-26 15:41:30
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_main_recovery_grid_v2_main_neg4p0_down0p25_turn0p10_separate_linear_readout.mat`
- 最佳轮次: 64
- 最佳验证损失: 0.527111
- 最佳选择分数: 0.615046
- 主任务基座选择分数: 0.615046
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_max_inputstats`
- Turn head: `linear`, source=`readout`, hidden=64
- Gradient clip: `separate`, threshold=5.000
- 损失权重: 转弯=0.100, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`none`
- 转弯类别乘子 [right straight left]: [1.000 1.000 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.693817 |
| 主工况准确率 | 0.9371 |
| 转弯准确率 | 0.8180 |
| 转弯纯窗口准确率 | 0.8589 |
| 转弯过渡窗口准确率 | 0.4146 |
| 坡度 MAE deg | 0.9091 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 255 | 5 | 5 | 0.9623 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 2 | 12 | 148 | 0.9136 |

| pred class | precision |
|---|---:|
| flat | 0.9846 |
| stall | 0.4516 |
| slope | 0.9548 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 58 | 6 | 8 | 0.8056 |
| straight | 25 | 242 | 24 | 0.8316 |
| left | 12 | 6 | 64 | 0.7805 |

| pred class | precision |
|---|---:|
| right | 0.6105 |
| straight | 0.9528 |
| left | 0.6667 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-5.602, 9.454] deg
- Slope 符号准确率: 0.9815

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9248 | 0.7669 | 1.0000 | [2.884, 7.500] | [3.754, 9.454] |
| downhill | 29 | 0.8621 | 1.5614 | 0.8966 | [-5.500, -2.298] | [-5.602, 4.034] |
