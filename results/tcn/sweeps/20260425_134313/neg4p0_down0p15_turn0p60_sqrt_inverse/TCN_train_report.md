# TCN 训练报告

- 生成时间: 2026-04-25 17:55:23
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_neg4p0_down0p15_turn0p60_sqrt_inverse.mat`
- 最佳轮次: 70
- 最佳验证损失: 0.965839
- 最佳选择分数: 1.146124
- 选模指标: `composite`
- Head pooling: `last_mean_max_inputstats`
- 损失权重: 转弯=0.600, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.150
- 类别权重策略: main=`balanced`, turn=`sqrt_inverse`
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 1.050262 |
| 主工况准确率 | 0.9011 |
| 转弯准确率 | 0.7843 |
| 坡度 MAE deg | 2.5451 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 246 | 7 | 12 | 0.9283 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 9 | 12 | 141 | 0.8704 |

| pred class | precision |
|---|---:|
| flat | 0.9572 |
| stall | 0.4242 |
| slope | 0.9097 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 58 | 7 | 8 | 0.7945 |
| straight | 32 | 226 | 33 | 0.7766 |
| left | 12 | 4 | 65 | 0.8025 |

| pred class | precision |
|---|---:|
| right | 0.5686 |
| straight | 0.9536 |
| left | 0.6132 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-10.609, 8.062] deg
- Slope 符号准确率: 0.9691

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.8797 | 2.5157 | 0.9624 | [2.884, 7.500] | [-1.842, 8.062] |
| downhill | 29 | 0.8276 | 2.6797 | 1.0000 | [-5.500, -2.298] | [-10.609, -0.685] |
