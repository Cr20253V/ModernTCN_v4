# TCN 训练报告

- 生成时间: 2026-04-25 11:59:20
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_smoke.mat`
- 最佳轮次: 1
- 最佳验证损失: 1.311431
- 最佳选择分数: 1.882196
- 选模指标: `composite`
- Head pooling: `last_mean_max_inputstats`
- 损失权重: 转弯=0.300, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=5.000, 正坡=1.000
- 下坡选模惩罚权重: 0.300
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 1.314731 |
| 主工况准确率 | 0.4674 |
| 转弯准确率 | 0.6899 |
| 坡度 MAE deg | 10.8738 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 78 | 16 | 171 | 0.2943 |
| stall | 2 | 11 | 5 | 0.6111 |
| slope | 38 | 5 | 119 | 0.7346 |

| pred class | precision |
|---|---:|
| flat | 0.6610 |
| stall | 0.3438 |
| slope | 0.4034 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 45 | 21 | 7 | 0.6164 |
| straight | 46 | 237 | 8 | 0.8144 |
| left | 7 | 49 | 25 | 0.3086 |

| pred class | precision |
|---|---:|
| right | 0.4592 |
| straight | 0.7720 |
| left | 0.6250 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-19.448, 10.224] deg
- Slope 符号准确率: 0.2160

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.6842 | 11.9679 | 0.0902 | [2.884, 7.500] | [-19.448, 10.224] |
| downhill | 29 | 0.9655 | 5.8558 | 0.7931 | [-5.500, -2.298] | [-16.274, 7.166] |
