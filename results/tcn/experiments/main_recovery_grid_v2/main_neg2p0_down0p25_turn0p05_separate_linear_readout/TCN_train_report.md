# TCN 训练报告

- 生成时间: 2026-04-26 13:15:11
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_main_recovery_grid_v2_main_neg2p0_down0p25_turn0p05_separate_linear_readout.mat`
- 最佳轮次: 64
- 最佳验证损失: 0.524840
- 最佳选择分数: 0.668359
- 主任务基座选择分数: 0.668359
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_max_inputstats`
- Turn head: `linear`, source=`readout`, hidden=64
- Gradient clip: `separate`, threshold=5.000
- 损失权重: 转弯=0.050, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=2.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`none`
- 转弯类别乘子 [right straight left]: [1.000 1.000 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.665385 |
| 主工况准确率 | 0.9371 |
| 转弯准确率 | 0.8225 |
| 转弯纯窗口准确率 | 0.8589 |
| 转弯过渡窗口准确率 | 0.4634 |
| 坡度 MAE deg | 1.9462 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 254 | 6 | 5 | 0.9585 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 4 | 9 | 149 | 0.9198 |

| pred class | precision |
|---|---:|
| flat | 0.9769 |
| stall | 0.4828 |
| slope | 0.9551 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 58 | 6 | 8 | 0.8056 |
| straight | 26 | 243 | 22 | 0.8351 |
| left | 12 | 5 | 65 | 0.7927 |

| pred class | precision |
|---|---:|
| right | 0.6042 |
| straight | 0.9567 |
| left | 0.6842 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.281, 11.310] deg
- Slope 符号准确率: 0.9877

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9398 | 1.9124 | 1.0000 | [2.884, 7.500] | [2.668, 11.310] |
| downhill | 29 | 0.8276 | 2.1015 | 0.9310 | [-5.500, -2.298] | [-6.281, 2.123] |
