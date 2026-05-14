# TCN 训练报告

- 生成时间: 2026-04-25 16:07:47
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_neg2p0_down0p25_turn0p45_none.mat`
- 最佳轮次: 68
- 最佳验证损失: 0.783141
- 最佳选择分数: 0.924190
- 选模指标: `composite`
- Head pooling: `last_mean_max_inputstats`
- 损失权重: 转弯=0.450, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=2.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`none`
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.898603 |
| 主工况准确率 | 0.9371 |
| 转弯准确率 | 0.7933 |
| 坡度 MAE deg | 1.5628 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 256 | 6 | 3 | 0.9660 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 4 | 11 | 147 | 0.9074 |

| pred class | precision |
|---|---:|
| flat | 0.9771 |
| stall | 0.4516 |
| slope | 0.9671 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 56 | 9 | 8 | 0.7671 |
| straight | 28 | 235 | 28 | 0.8076 |
| left | 12 | 7 | 62 | 0.7654 |

| pred class | precision |
|---|---:|
| right | 0.5833 |
| straight | 0.9363 |
| left | 0.6327 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-7.843, 8.041] deg
- Slope 符号准确率: 0.9877

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9248 | 1.4494 | 1.0000 | [2.884, 7.500] | [1.294, 8.041] |
| downhill | 29 | 0.8276 | 2.0827 | 0.9310 | [-5.500, -2.298] | [-7.843, 1.722] |
