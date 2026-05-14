# GRU 训练报告

- 生成时间: 2026-04-26 22:51:40
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_fair_v1_h96_l1_turn0p05_last_mean_inputstats.mat`
- 最佳轮次: 27
- 最佳验证损失: 0.522816
- 最佳选择分数: 0.614946
- 主任务基座选择分数: 0.614946
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
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
| 总损失 | 0.648587 |
| 主工况准确率 | 0.9438 |
| 转弯准确率 | 0.8742 |
| 转弯纯窗口准确率 | 0.9010 |
| 转弯过渡窗口准确率 | 0.6098 |
| 坡度 MAE deg | 0.8871 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 252 | 5 | 8 | 0.9509 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 0 | 8 | 154 | 0.9506 |

| pred class | precision |
|---|---:|
| flat | 0.9921 |
| stall | 0.5185 |
| slope | 0.9390 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 63 | 4 | 5 | 0.8750 |
| straight | 15 | 269 | 7 | 0.9244 |
| left | 9 | 16 | 57 | 0.6951 |

| pred class | precision |
|---|---:|
| right | 0.7241 |
| straight | 0.9308 |
| left | 0.8261 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.471, 9.411] deg
- Slope 符号准确率: 0.9877

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9699 | 0.8191 | 1.0000 | [2.884, 7.500] | [3.121, 9.411] |
| downhill | 29 | 0.8621 | 1.1986 | 0.9310 | [-5.500, -2.298] | [-6.471, 1.301] |
