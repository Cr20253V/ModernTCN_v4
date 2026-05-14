# TCN 训练报告

- 生成时间: 2026-04-25 16:15:44
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_neg2p0_down0p25_turn0p45_sqrt_inverse.mat`
- 最佳轮次: 53
- 最佳验证损失: 1.035131
- 最佳选择分数: 1.193975
- 选模指标: `composite`
- Head pooling: `last_mean_max_inputstats`
- 损失权重: 转弯=0.450, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=2.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`sqrt_inverse`
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 1.121600 |
| 主工况准确率 | 0.8494 |
| 转弯准确率 | 0.7933 |
| 坡度 MAE deg | 0.9425 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 228 | 7 | 30 | 0.8604 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 16 | 10 | 136 | 0.8395 |

| pred class | precision |
|---|---:|
| flat | 0.9268 |
| stall | 0.4516 |
| slope | 0.8095 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 56 | 9 | 8 | 0.7671 |
| straight | 29 | 233 | 29 | 0.8007 |
| left | 12 | 5 | 64 | 0.7901 |

| pred class | precision |
|---|---:|
| right | 0.5773 |
| straight | 0.9433 |
| left | 0.6337 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.679, 8.868] deg
- Slope 符号准确率: 0.9877

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.8346 | 0.8667 | 1.0000 | [2.884, 7.500] | [1.744, 8.868] |
| downhill | 29 | 0.8621 | 1.2901 | 0.9310 | [-5.500, -2.298] | [-6.679, 1.155] |
