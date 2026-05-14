# TCN 训练报告

- 生成时间: 2026-04-26 12:47:38
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_main_recovery_grid_v2_main_neg2p0_down0p25_turn0p00_global_linear_readout.mat`
- 最佳轮次: 64
- 最佳验证损失: 0.525719
- 最佳选择分数: 0.691111
- 主任务基座选择分数: 0.691111
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_max_inputstats`
- Turn head: `linear`, source=`readout`, hidden=64
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.000, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
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
| 总损失 | 0.718736 |
| 主工况准确率 | 0.9348 |
| 转弯准确率 | 0.3461 |
| 转弯纯窗口准确率 | 0.3441 |
| 转弯过渡窗口准确率 | 0.3659 |
| 坡度 MAE deg | 0.7889 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 258 | 4 | 3 | 0.9736 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 7 | 11 | 144 | 0.8889 |

| pred class | precision |
|---|---:|
| flat | 0.9663 |
| stall | 0.4828 |
| slope | 0.9664 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 34 | 10 | 28 | 0.4722 |
| straight | 101 | 51 | 139 | 0.1753 |
| left | 13 | 0 | 69 | 0.8415 |

| pred class | precision |
|---|---:|
| right | 0.2297 |
| straight | 0.8361 |
| left | 0.2924 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-5.672, 10.136] deg
- Slope 符号准确率: 0.9877

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9023 | 0.6864 | 1.0000 | [2.884, 7.500] | [2.740, 10.136] |
| downhill | 29 | 0.8276 | 1.2590 | 0.9310 | [-5.500, -2.298] | [-5.672, 2.019] |
