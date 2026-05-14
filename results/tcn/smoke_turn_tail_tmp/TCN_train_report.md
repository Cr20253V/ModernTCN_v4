# TCN 训练报告

- 生成时间: 2026-04-26 01:15:54
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed_turn_tail_tmp.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_turn_tail_smoke_tmp.mat`
- 最佳轮次: 1
- 最佳验证损失: 1.055929
- 最佳选择分数: 1.396960
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
| 总损失 | 1.055461 |
| 主工况准确率 | 0.4989 |
| 转弯准确率 | 0.7303 |
| 坡度 MAE deg | 4.5143 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 106 | 12 | 147 | 0.4000 |
| stall | 2 | 9 | 7 | 0.5000 |
| slope | 51 | 4 | 107 | 0.6605 |

| pred class | precision |
|---|---:|
| flat | 0.6667 |
| stall | 0.3600 |
| slope | 0.4100 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 50 | 15 | 7 | 0.6944 |
| straight | 29 | 232 | 30 | 0.7973 |
| left | 12 | 27 | 43 | 0.5244 |

| pred class | precision |
|---|---:|
| right | 0.5495 |
| straight | 0.8467 |
| left | 0.5375 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-14.013, 7.582] deg
- Slope 符号准确率: 0.6605

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.6015 | 4.9063 | 0.5865 | [2.884, 7.500] | [-9.858, 7.582] |
| downhill | 29 | 0.9310 | 2.7165 | 1.0000 | [-5.500, -2.298] | [-14.013, -3.749] |
