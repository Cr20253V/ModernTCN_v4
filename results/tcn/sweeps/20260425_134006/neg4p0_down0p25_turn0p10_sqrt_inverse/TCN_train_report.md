# TCN 训练报告

- 生成时间: 2026-04-25 13:40:39
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_neg4p0_down0p25_turn0p10_sqrt_inverse.mat`
- 最佳轮次: 1
- 最佳验证损失: 1.147289
- 最佳选择分数: 1.821840
- 选模指标: `composite`
- Head pooling: `last_mean_max_inputstats`
- 损失权重: 转弯=0.100, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`sqrt_inverse`
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 1.140731 |
| 主工况准确率 | 0.4899 |
| 转弯准确率 | 0.6944 |
| 坡度 MAE deg | 11.3855 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 115 | 23 | 127 | 0.4340 |
| stall | 4 | 13 | 1 | 0.7222 |
| slope | 66 | 6 | 90 | 0.5556 |

| pred class | precision |
|---|---:|
| flat | 0.6216 |
| stall | 0.3095 |
| slope | 0.4128 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 43 | 23 | 7 | 0.5890 |
| straight | 40 | 245 | 6 | 0.8419 |
| left | 6 | 54 | 21 | 0.2593 |

| pred class | precision |
|---|---:|
| right | 0.4831 |
| straight | 0.7609 |
| left | 0.6176 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-19.838, 10.205] deg
- Slope 符号准确率: 0.2099

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.5338 | 12.5785 | 0.0752 | [2.884, 7.500] | [-19.838, 10.205] |
| downhill | 29 | 0.6552 | 5.9140 | 0.8276 | [-5.500, -2.298] | [-19.466, 5.826] |
