# TCN 训练报告

- 生成时间: 2026-04-26 19:20:51
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model.mat`
- 最佳轮次: 41
- 最佳验证损失: 0.638420
- 最佳选择分数: 0.773342
- 主任务基座选择分数: 0.773342
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_max_inputstats`
- Turn head: `linear`, source=`readout`, hidden=64
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.200, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
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
| 总损失 | 0.722026 |
| 主工况准确率 | 0.9146 |
| 转弯准确率 | 0.8067 |
| 转弯纯窗口准确率 | 0.8465 |
| 转弯过渡窗口准确率 | 0.4146 |
| 坡度 MAE deg | 1.2980 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 249 | 5 | 11 | 0.9396 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 7 | 11 | 144 | 0.8889 |

| pred class | precision |
|---|---:|
| flat | 0.9651 |
| stall | 0.4667 |
| slope | 0.9172 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 58 | 6 | 8 | 0.8056 |
| straight | 27 | 235 | 29 | 0.8076 |
| left | 12 | 4 | 66 | 0.8049 |

| pred class | precision |
|---|---:|
| right | 0.5979 |
| straight | 0.9592 |
| left | 0.6408 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.645, 11.691] deg
- Slope 符号准确率: 0.9815

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.8947 | 1.1507 | 1.0000 | [2.884, 7.500] | [0.636, 11.691] |
| downhill | 29 | 0.8621 | 1.9738 | 0.8966 | [-5.500, -2.298] | [-6.645, 2.635] |
