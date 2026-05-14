# TCN 训练报告

- 生成时间: 2026-04-26 11:11:47
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_main_linear_separate_clip.mat`
- 最佳轮次: 1
- 最佳验证损失: 1.037325
- 最佳选择分数: 1.488861
- 主任务基座选择分数: 1.488861
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_max_inputstats`
- Turn head: `linear`, source=`readout`, hidden=64
- Gradient clip: `separate`, threshold=5.000
- 损失权重: 转弯=0.100, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=2.000, 正坡=1.000
- 下坡选模惩罚权重: 0.150
- 类别权重策略: main=`balanced`, turn=`none`
- 转弯类别乘子 [right straight left]: [1.000 1.000 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 1.010662 |
| 主工况准确率 | 0.4652 |
| 转弯准确率 | 0.7236 |
| 转弯纯窗口准确率 | 0.7649 |
| 转弯过渡窗口准确率 | 0.3171 |
| 坡度 MAE deg | 4.5750 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 53 | 15 | 197 | 0.2000 |
| stall | 2 | 9 | 7 | 0.5000 |
| slope | 12 | 5 | 145 | 0.8951 |

| pred class | precision |
|---|---:|
| flat | 0.7910 |
| stall | 0.3103 |
| slope | 0.4155 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 51 | 12 | 9 | 0.7083 |
| straight | 31 | 214 | 46 | 0.7354 |
| left | 12 | 13 | 57 | 0.6951 |

| pred class | precision |
|---|---:|
| right | 0.5426 |
| straight | 0.8954 |
| left | 0.5089 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-13.848, 8.872] deg
- Slope 符号准确率: 0.6728

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9098 | 4.7340 | 0.6165 | [2.884, 7.500] | [-8.127, 8.872] |
| downhill | 29 | 0.8276 | 3.8458 | 0.9310 | [-5.500, -2.298] | [-13.848, 1.305] |
