# TCN 训练报告

- 生成时间: 2026-04-26 01:52:48
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_turn_inputstats_clip_smoke_tmp.mat`
- 最佳轮次: 1
- 最佳验证损失: 1.275870
- 最佳选择分数: 3.557642
- 选模指标: `turn_priority`
- Head pooling: `last_mean_max_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Gradient clip: `separate`, threshold=5.000
- 损失权重: 转弯=0.300, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=2.000, 正坡=1.000
- 下坡选模惩罚权重: 0.150
- 类别权重策略: main=`balanced`, turn=`none`
- 转弯类别乘子 [right straight left]: [1.000 1.200 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 1.157153 |
| 主工况准确率 | 0.6360 |
| 转弯准确率 | 0.7393 |
| 转弯纯窗口准确率 | 0.7822 |
| 转弯过渡窗口准确率 | 0.3171 |
| 坡度 MAE deg | 4.0048 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 228 | 29 | 8 | 0.8604 |
| stall | 4 | 14 | 0 | 0.7778 |
| slope | 104 | 17 | 41 | 0.2531 |

| pred class | precision |
|---|---:|
| flat | 0.6786 |
| stall | 0.2333 |
| slope | 0.8367 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 37 | 30 | 5 | 0.5139 |
| straight | 21 | 248 | 22 | 0.8522 |
| left | 9 | 29 | 44 | 0.5366 |

| pred class | precision |
|---|---:|
| right | 0.5522 |
| straight | 0.8078 |
| left | 0.6197 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-8.339, 22.739] deg
- Slope 符号准确率: 0.8951

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.3008 | 3.6924 | 0.9774 | [2.884, 7.500] | [-2.473, 22.739] |
| downhill | 29 | 0.0345 | 5.4373 | 0.5172 | [-5.500, -2.298] | [-8.339, 8.383] |
