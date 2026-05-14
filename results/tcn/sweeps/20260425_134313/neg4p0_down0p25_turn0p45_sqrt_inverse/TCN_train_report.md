# TCN 训练报告

- 生成时间: 2026-04-25 18:58:06
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_neg4p0_down0p25_turn0p45_sqrt_inverse.mat`
- 最佳轮次: 43
- 最佳验证损失: 1.017916
- 最佳选择分数: 1.199375
- 选模指标: `composite`
- Head pooling: `last_mean_max_inputstats`
- 损失权重: 转弯=0.450, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`sqrt_inverse`
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 1.109175 |
| 主工况准确率 | 0.8000 |
| 转弯准确率 | 0.7888 |
| 坡度 MAE deg | 1.1041 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 216 | 8 | 41 | 0.8151 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 26 | 10 | 126 | 0.7778 |

| pred class | precision |
|---|---:|
| flat | 0.8852 |
| stall | 0.4375 |
| slope | 0.7456 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 56 | 9 | 8 | 0.7671 |
| straight | 29 | 231 | 31 | 0.7938 |
| left | 12 | 5 | 64 | 0.7901 |

| pred class | precision |
|---|---:|
| right | 0.5773 |
| straight | 0.9429 |
| left | 0.6214 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-7.617, 7.245] deg
- Slope 符号准确率: 0.9938

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.7594 | 0.9606 | 1.0000 | [2.884, 7.500] | [1.656, 7.245] |
| downhill | 29 | 0.8621 | 1.7622 | 0.9655 | [-5.500, -2.298] | [-7.617, 0.609] |
