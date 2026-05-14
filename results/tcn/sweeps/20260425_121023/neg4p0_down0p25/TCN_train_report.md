# TCN 训练报告

- 生成时间: 2026-04-25 13:34:18
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_neg4p0_down0p25.mat`
- 最佳轮次: 65
- 最佳验证损失: 0.686030
- 最佳选择分数: 0.774622
- 选模指标: `composite`
- Head pooling: `last_mean_max_inputstats`
- 损失权重: 转弯=0.300, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.862799 |
| 主工况准确率 | 0.9348 |
| 转弯准确率 | 0.7843 |
| 坡度 MAE deg | 0.5627 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 255 | 5 | 5 | 0.9623 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 5 | 10 | 147 | 0.9074 |

| pred class | precision |
|---|---:|
| flat | 0.9733 |
| stall | 0.4828 |
| slope | 0.9545 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 57 | 8 | 8 | 0.7808 |
| straight | 30 | 227 | 34 | 0.7801 |
| left | 12 | 4 | 65 | 0.8025 |

| pred class | precision |
|---|---:|
| right | 0.5758 |
| straight | 0.9498 |
| left | 0.6075 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-5.795, 9.631] deg
- Slope 符号准确率: 0.9877

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9248 | 0.4512 | 1.0000 | [2.884, 7.500] | [1.619, 9.631] |
| downhill | 29 | 0.8276 | 1.0739 | 0.9310 | [-5.500, -2.298] | [-5.795, 1.900] |
