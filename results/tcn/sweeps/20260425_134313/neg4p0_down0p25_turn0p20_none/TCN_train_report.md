# TCN 训练报告

- 生成时间: 2026-04-25 18:21:56
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_neg4p0_down0p25_turn0p20_none.mat`
- 最佳轮次: 76
- 最佳验证损失: 0.664980
- 最佳选择分数: 0.794200
- 选模指标: `composite`
- Head pooling: `last_mean_max_inputstats`
- 损失权重: 转弯=0.200, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`none`
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.778701 |
| 主工况准确率 | 0.8989 |
| 转弯准确率 | 0.7888 |
| 坡度 MAE deg | 1.0598 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 245 | 8 | 12 | 0.9245 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 9 | 12 | 141 | 0.8704 |

| pred class | precision |
|---|---:|
| flat | 0.9570 |
| stall | 0.4118 |
| slope | 0.9097 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 56 | 9 | 8 | 0.7671 |
| straight | 31 | 233 | 27 | 0.8007 |
| left | 12 | 7 | 62 | 0.7654 |

| pred class | precision |
|---|---:|
| right | 0.5657 |
| straight | 0.9357 |
| left | 0.6392 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-8.079, 9.016] deg
- Slope 符号准确率: 0.9877

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.8797 | 0.9727 | 1.0000 | [2.884, 7.500] | [0.668, 9.016] |
| downhill | 29 | 0.8276 | 1.4592 | 0.9310 | [-5.500, -2.298] | [-8.079, 1.193] |
