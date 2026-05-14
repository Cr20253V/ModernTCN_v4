# TCN 训练报告

- 生成时间: 2026-04-25 12:09:34
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_neg2p0_down0p05.mat`
- 最佳轮次: 1
- 最佳验证损失: 1.361086
- 最佳选择分数: 1.961058
- 选模指标: `composite`
- Head pooling: `last_mean_max_inputstats`
- 损失权重: 转弯=0.300, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=2.000, 正坡=1.000
- 下坡选模惩罚权重: 0.050
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 1.349309 |
| 主工况准确率 | 0.5596 |
| 转弯准确率 | 0.6944 |
| 坡度 MAE deg | 10.4210 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 195 | 34 | 36 | 0.7358 |
| stall | 4 | 14 | 0 | 0.7778 |
| slope | 108 | 14 | 40 | 0.2469 |

| pred class | precision |
|---|---:|
| flat | 0.6352 |
| stall | 0.2258 |
| slope | 0.5263 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 47 | 19 | 7 | 0.6438 |
| straight | 44 | 238 | 9 | 0.8179 |
| left | 7 | 50 | 24 | 0.2963 |

| pred class | precision |
|---|---:|
| right | 0.4796 |
| straight | 0.7752 |
| left | 0.6000 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-19.503, 13.380] deg
- Slope 符号准确率: 0.2284

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.2707 | 11.4330 | 0.1053 | [2.884, 7.500] | [-17.702, 13.380] |
| downhill | 29 | 0.1379 | 5.7799 | 0.7931 | [-5.500, -2.298] | [-19.503, 4.432] |
