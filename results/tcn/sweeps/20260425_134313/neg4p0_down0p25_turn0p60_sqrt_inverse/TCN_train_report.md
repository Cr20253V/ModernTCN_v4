# TCN 训练报告

- 生成时间: 2026-04-25 19:15:20
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_neg4p0_down0p25_turn0p60_sqrt_inverse.mat`
- 最佳轮次: 70
- 最佳验证损失: 1.105961
- 最佳选择分数: 1.280150
- 选模指标: `composite`
- Head pooling: `last_mean_max_inputstats`
- 损失权重: 转弯=0.600, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`sqrt_inverse`
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 1.192641 |
| 主工况准确率 | 0.8090 |
| 转弯准确率 | 0.7910 |
| 坡度 MAE deg | 0.9091 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 224 | 8 | 33 | 0.8453 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 30 | 10 | 122 | 0.7531 |

| pred class | precision |
|---|---:|
| flat | 0.8750 |
| stall | 0.4375 |
| slope | 0.7771 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 56 | 9 | 8 | 0.7671 |
| straight | 29 | 232 | 30 | 0.7973 |
| left | 12 | 5 | 64 | 0.7901 |

| pred class | precision |
|---|---:|
| right | 0.5773 |
| straight | 0.9431 |
| left | 0.6275 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-7.091, 8.848] deg
- Slope 符号准确率: 0.9938

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.7293 | 0.7998 | 1.0000 | [2.884, 7.500] | [2.012, 8.848] |
| downhill | 29 | 0.8621 | 1.4105 | 0.9655 | [-5.500, -2.298] | [-7.091, 1.043] |
