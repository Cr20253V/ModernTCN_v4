# TCN 训练报告

- 生成时间: 2026-04-26 13:56:34
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_main_recovery_grid_v2_main_neg4p0_down0p15_turn0p00_global_linear_readout.mat`
- 最佳轮次: 62
- 最佳验证损失: 0.458204
- 最佳选择分数: 0.616302
- 主任务基座选择分数: 0.616302
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_max_inputstats`
- Turn head: `linear`, source=`readout`, hidden=64
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.000, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.150
- 类别权重策略: main=`balanced`, turn=`none`
- 转弯类别乘子 [right straight left]: [1.000 1.000 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.662748 |
| 主工况准确率 | 0.9371 |
| 转弯准确率 | 0.3753 |
| 转弯纯窗口准确率 | 0.3762 |
| 转弯过渡窗口准确率 | 0.3659 |
| 坡度 MAE deg | 1.0606 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 256 | 4 | 5 | 0.9660 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 4 | 11 | 147 | 0.9074 |

| pred class | precision |
|---|---:|
| flat | 0.9771 |
| stall | 0.4828 |
| slope | 0.9545 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 0 | 17 | 55 | 0.0000 |
| straight | 5 | 90 | 196 | 0.3093 |
| left | 0 | 5 | 77 | 0.9390 |

| pred class | precision |
|---|---:|
| right | 0.0000 |
| straight | 0.8036 |
| left | 0.2348 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.770, 10.268] deg
- Slope 符号准确率: 0.9877

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9173 | 0.9939 | 1.0000 | [2.884, 7.500] | [1.906, 10.268] |
| downhill | 29 | 0.8621 | 1.3663 | 0.9310 | [-5.500, -2.298] | [-6.770, 0.634] |
