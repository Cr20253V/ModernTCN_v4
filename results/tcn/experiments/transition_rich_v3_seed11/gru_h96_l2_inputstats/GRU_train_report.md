# GRU 训练报告

- 生成时间: 2026-04-28 23:12:10
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_transition_rich_v3_seed11_h96_l2_inputstats.mat`
- 最佳轮次: 8
- 最佳验证损失: 0.137687
- 最佳选择分数: 0.204180
- 主任务基座选择分数: 0.204180
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
| 总损失 | 0.188763 |
| 主工况准确率 | 0.9375 |
| 转弯准确率 | 0.8736 |
| 转弯纯窗口准确率 | 0.9122 |
| 转弯过渡窗口准确率 | 0.6207 |
| 坡度 MAE deg | 0.5203 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 1098 | 33 | 82 | 0.9052 |
| stall | 10 | 187 | 8 | 0.9122 |
| slope | 30 | 15 | 1386 | 0.9686 |

| pred class | precision |
|---|---:|
| flat | 0.9649 |
| stall | 0.7957 |
| slope | 0.9390 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 478 | 36 | 4 | 0.9228 |
| straight | 121 | 1626 | 104 | 0.8784 |
| left | 4 | 91 | 385 | 0.8021 |

| pred class | precision |
|---|---:|
| right | 0.7927 |
| straight | 0.9276 |
| left | 0.7809 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-7.363, 8.560] deg
- Slope 符号准确率: 1.0000

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 871 | 0.9587 | 0.4860 | 1.0000 | [2.006, 7.500] | [0.232, 8.560] |
| downhill | 560 | 0.9839 | 0.5735 | 1.0000 | [-5.500, -2.046] | [-7.363, -0.981] |
