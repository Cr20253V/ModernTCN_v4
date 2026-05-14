# GRU 训练报告

- 生成时间: 2026-04-26 23:10:50
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_fair_v1_h96_l2_turn0p05_last_mean.mat`
- 最佳轮次: 25
- 最佳验证损失: 0.556921
- 最佳选择分数: 0.667463
- 主任务基座选择分数: 0.667463
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean`
- Turn head: `linear`, source=`readout`, hidden=64
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.050, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.000, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`none`
- 转弯类别乘子 [right straight left]: [1.000 1.100 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 128 steps / 1.280 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.759528 |
| 主工况准确率 | 0.9461 |
| 转弯准确率 | 0.7798 |
| 转弯纯窗口准确率 | 0.8267 |
| 转弯过渡窗口准确率 | 0.3171 |
| 坡度 MAE deg | 0.8758 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 256 | 4 | 5 | 0.9660 |
| stall | 1 | 12 | 5 | 0.6667 |
| slope | 0 | 9 | 153 | 0.9444 |

| pred class | precision |
|---|---:|
| flat | 0.9961 |
| stall | 0.4800 |
| slope | 0.9387 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 51 | 14 | 7 | 0.7083 |
| straight | 20 | 250 | 21 | 0.8591 |
| left | 6 | 30 | 46 | 0.5610 |

| pred class | precision |
|---|---:|
| right | 0.6623 |
| straight | 0.8503 |
| left | 0.6216 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-7.253, 8.499] deg
- Slope 符号准确率: 0.9938

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9624 | 0.8181 | 1.0000 | [2.884, 7.500] | [0.588, 8.499] |
| downhill | 29 | 0.8621 | 1.1405 | 0.9655 | [-5.500, -2.298] | [-7.253, 0.628] |
