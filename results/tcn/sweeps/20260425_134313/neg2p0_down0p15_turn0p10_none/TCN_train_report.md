# TCN 训练报告

- 生成时间: 2026-04-25 13:51:34
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_neg2p0_down0p15_turn0p10_none.mat`
- 最佳轮次: 64
- 最佳验证损失: 0.580035
- 最佳选择分数: 0.676572
- 选模指标: `composite`
- Head pooling: `last_mean_max_inputstats`
- 损失权重: 转弯=0.100, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=2.000, 正坡=1.000
- 下坡选模惩罚权重: 0.150
- 类别权重策略: main=`balanced`, turn=`none`
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.789725 |
| 主工况准确率 | 0.9461 |
| 转弯准确率 | 0.8000 |
| 坡度 MAE deg | 0.6025 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 261 | 3 | 1 | 0.9849 |
| stall | 3 | 13 | 2 | 0.7222 |
| slope | 5 | 10 | 147 | 0.9074 |

| pred class | precision |
|---|---:|
| flat | 0.9703 |
| stall | 0.5000 |
| slope | 0.9800 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 56 | 9 | 8 | 0.7671 |
| straight | 28 | 239 | 24 | 0.8213 |
| left | 12 | 8 | 61 | 0.7531 |

| pred class | precision |
|---|---:|
| right | 0.5833 |
| straight | 0.9336 |
| left | 0.6559 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.418, 9.299] deg
- Slope 符号准确率: 1.0000

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9248 | 0.5152 | 1.0000 | [2.884, 7.500] | [1.127, 9.299] |
| downhill | 29 | 0.8276 | 1.0028 | 1.0000 | [-5.500, -2.298] | [-6.418, -0.144] |
