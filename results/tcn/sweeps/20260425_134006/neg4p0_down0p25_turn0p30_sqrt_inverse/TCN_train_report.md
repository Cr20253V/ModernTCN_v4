# TCN 训练报告

- 生成时间: 2026-04-25 13:40:53
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_neg4p0_down0p25_turn0p30_sqrt_inverse.mat`
- 最佳轮次: 1
- 最佳验证损失: 1.332292
- 最佳选择分数: 1.936349
- 选模指标: `composite`
- Head pooling: `last_mean_max_inputstats`
- 损失权重: 转弯=0.300, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`sqrt_inverse`
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 1.330225 |
| 主工况准确率 | 0.4764 |
| 转弯准确率 | 0.6921 |
| 坡度 MAE deg | 10.5442 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 102 | 20 | 143 | 0.3849 |
| stall | 2 | 13 | 3 | 0.7222 |
| slope | 60 | 5 | 97 | 0.5988 |

| pred class | precision |
|---|---:|
| flat | 0.6220 |
| stall | 0.3421 |
| slope | 0.3992 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 47 | 19 | 7 | 0.6438 |
| straight | 47 | 235 | 9 | 0.8076 |
| left | 8 | 47 | 26 | 0.3210 |

| pred class | precision |
|---|---:|
| right | 0.4608 |
| straight | 0.7807 |
| left | 0.6190 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-18.999, 10.585] deg
- Slope 符号准确率: 0.2037

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.5639 | 11.5793 | 0.0827 | [2.884, 7.500] | [-18.999, 10.585] |
| downhill | 29 | 0.7586 | 5.7970 | 0.7586 | [-5.500, -2.298] | [-17.354, 5.204] |
