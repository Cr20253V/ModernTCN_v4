# TCN 训练报告

- 生成时间: 2026-04-25 12:09:41
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_neg3p0_down0p05.mat`
- 最佳轮次: 1
- 最佳验证损失: 1.348504
- 最佳选择分数: 1.914469
- 选模指标: `composite`
- Head pooling: `last_mean_max_inputstats`
- 损失权重: 转弯=0.300, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=3.000, 正坡=1.000
- 下坡选模惩罚权重: 0.050
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 1.341163 |
| 主工况准确率 | 0.4944 |
| 转弯准确率 | 0.6989 |
| 坡度 MAE deg | 10.3027 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 144 | 21 | 100 | 0.5434 |
| stall | 4 | 14 | 0 | 0.7778 |
| slope | 92 | 8 | 62 | 0.3827 |

| pred class | precision |
|---|---:|
| flat | 0.6000 |
| stall | 0.3256 |
| slope | 0.3827 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 48 | 18 | 7 | 0.6575 |
| straight | 43 | 238 | 10 | 0.8179 |
| left | 8 | 48 | 25 | 0.3086 |

| pred class | precision |
|---|---:|
| right | 0.4848 |
| straight | 0.7829 |
| left | 0.5952 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-19.396, 12.575] deg
- Slope 符号准确率: 0.2160

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.3985 | 11.2658 | 0.0977 | [2.884, 7.500] | [-18.345, 12.575] |
| downhill | 29 | 0.3103 | 5.8861 | 0.7586 | [-5.500, -2.298] | [-19.396, 5.488] |
