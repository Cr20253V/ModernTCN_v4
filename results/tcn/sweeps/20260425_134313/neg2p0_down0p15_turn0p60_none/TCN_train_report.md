# TCN 训练报告

- 生成时间: 2026-04-25 14:55:32
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_neg2p0_down0p15_turn0p60_none.mat`
- 最佳轮次: 76
- 最佳验证损失: 0.931848
- 最佳选择分数: 1.051484
- 选模指标: `composite`
- Head pooling: `last_mean_max_inputstats`
- 损失权重: 转弯=0.600, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=2.000, 正坡=1.000
- 下坡选模惩罚权重: 0.150
- 类别权重策略: main=`balanced`, turn=`none`
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.976490 |
| 主工况准确率 | 0.9034 |
| 转弯准确率 | 0.7888 |
| 坡度 MAE deg | 0.9221 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 244 | 8 | 13 | 0.9208 |
| stall | 1 | 14 | 3 | 0.7778 |
| slope | 5 | 13 | 144 | 0.8889 |

| pred class | precision |
|---|---:|
| flat | 0.9760 |
| stall | 0.4000 |
| slope | 0.9000 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 56 | 9 | 8 | 0.7671 |
| straight | 30 | 233 | 28 | 0.8007 |
| left | 12 | 7 | 62 | 0.7654 |

| pred class | precision |
|---|---:|
| right | 0.5714 |
| straight | 0.9357 |
| left | 0.6327 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.541, 10.029] deg
- Slope 符号准确率: 0.9815

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.8947 | 0.8239 | 1.0000 | [2.884, 7.500] | [0.943, 10.029] |
| downhill | 29 | 0.8621 | 1.3728 | 0.8966 | [-5.500, -2.298] | [-6.541, 1.096] |
