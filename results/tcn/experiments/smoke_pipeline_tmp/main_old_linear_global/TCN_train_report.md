# TCN 训练报告

- 生成时间: 2026-04-26 11:11:23
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_main_old_linear_global.mat`
- 最佳轮次: 1
- 最佳验证损失: 1.032548
- 最佳选择分数: 1.456928
- 主任务基座选择分数: 1.456928
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_max_inputstats`
- Turn head: `linear`, source=`readout`, hidden=64
- Gradient clip: `global`, threshold=5.000
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
| 总损失 | 1.012294 |
| 主工况准确率 | 0.5169 |
| 转弯准确率 | 0.7303 |
| 转弯纯窗口准确率 | 0.7723 |
| 转弯过渡窗口准确率 | 0.3171 |
| 坡度 MAE deg | 4.7913 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 83 | 16 | 166 | 0.3132 |
| stall | 2 | 9 | 7 | 0.5000 |
| slope | 19 | 5 | 138 | 0.8519 |

| pred class | precision |
|---|---:|
| flat | 0.7981 |
| stall | 0.3000 |
| slope | 0.4437 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 53 | 10 | 9 | 0.7361 |
| straight | 31 | 213 | 47 | 0.7320 |
| left | 12 | 11 | 59 | 0.7195 |

| pred class | precision |
|---|---:|
| right | 0.5521 |
| straight | 0.9103 |
| left | 0.5130 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-14.860, 10.564] deg
- Slope 符号准确率: 0.6543

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.8947 | 4.8225 | 0.6015 | [2.884, 7.500] | [-9.238, 10.564] |
| downhill | 29 | 0.6552 | 4.6480 | 0.8966 | [-5.500, -2.298] | [-14.860, 4.248] |
