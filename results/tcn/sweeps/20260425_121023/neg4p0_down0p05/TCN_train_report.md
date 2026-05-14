# TCN 训练报告

- 生成时间: 2026-04-25 13:18:45
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_neg4p0_down0p05.mat`
- 最佳轮次: 74
- 最佳验证损失: 0.783598
- 最佳选择分数: 0.953959
- 选模指标: `composite`
- Head pooling: `last_mean_max_inputstats`
- 损失权重: 转弯=0.300, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.050
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.862147 |
| 主工况准确率 | 0.8854 |
| 转弯准确率 | 0.7888 |
| 坡度 MAE deg | 2.3130 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 238 | 8 | 19 | 0.8981 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 7 | 13 | 142 | 0.8765 |

| pred class | precision |
|---|---:|
| flat | 0.9636 |
| stall | 0.4000 |
| slope | 0.8712 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 56 | 9 | 8 | 0.7671 |
| straight | 31 | 230 | 30 | 0.7904 |
| left | 12 | 4 | 65 | 0.8025 |

| pred class | precision |
|---|---:|
| right | 0.5657 |
| straight | 0.9465 |
| left | 0.6311 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-10.035, 7.651] deg
- Slope 符号准确率: 0.9753

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.8797 | 2.3345 | 0.9699 | [2.884, 7.500] | [-2.629, 7.651] |
| downhill | 29 | 0.8621 | 2.2140 | 1.0000 | [-5.500, -2.298] | [-10.035, -1.379] |
