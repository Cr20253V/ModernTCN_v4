# GRU 训练报告

- 生成时间: 2026-04-26 22:36:37
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_fair_v1_h64_l2_turn0p10_last_mean_inputstats.mat`
- 最佳轮次: 30
- 最佳验证损失: 0.595197
- 最佳选择分数: 0.681534
- 主任务基座选择分数: 0.681534
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.100, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.000, pitch一致性=0.000
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
| 总损失 | 0.745041 |
| 主工况准确率 | 0.9461 |
| 转弯准确率 | 0.8787 |
| 转弯纯窗口准确率 | 0.9059 |
| 转弯过渡窗口准确率 | 0.6098 |
| 坡度 MAE deg | 0.5629 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 255 | 6 | 4 | 0.9623 |
| stall | 3 | 12 | 3 | 0.6667 |
| slope | 0 | 8 | 154 | 0.9506 |

| pred class | precision |
|---|---:|
| flat | 0.9884 |
| stall | 0.4615 |
| slope | 0.9565 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 64 | 6 | 2 | 0.8889 |
| straight | 15 | 267 | 9 | 0.9175 |
| left | 7 | 15 | 60 | 0.7317 |

| pred class | precision |
|---|---:|
| right | 0.7442 |
| straight | 0.9271 |
| left | 0.8451 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.636, 7.639] deg
- Slope 符号准确率: 1.0000

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9699 | 0.4461 | 1.0000 | [2.884, 7.500] | [2.523, 7.639] |
| downhill | 29 | 0.8621 | 1.0983 | 1.0000 | [-5.500, -2.298] | [-6.636, -0.191] |
