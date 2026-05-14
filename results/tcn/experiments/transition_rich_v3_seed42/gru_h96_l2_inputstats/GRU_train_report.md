# GRU 训练报告

- 生成时间: 2026-04-29 02:04:40
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_transition_rich_v3_seed42_h96_l2_inputstats.mat`
- 最佳轮次: 16
- 最佳验证损失: 0.152763
- 最佳选择分数: 0.211811
- 主任务基座选择分数: 0.211811
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
| 总损失 | 0.171488 |
| 主工况准确率 | 0.9421 |
| 转弯准确率 | 0.8831 |
| 转弯纯窗口准确率 | 0.9094 |
| 转弯过渡窗口准确率 | 0.7109 |
| 坡度 MAE deg | 0.4092 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 1110 | 35 | 68 | 0.9151 |
| stall | 10 | 188 | 7 | 0.9171 |
| slope | 38 | 7 | 1386 | 0.9686 |

| pred class | precision |
|---|---:|
| flat | 0.9585 |
| stall | 0.8174 |
| slope | 0.9487 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 442 | 72 | 4 | 0.8533 |
| straight | 80 | 1663 | 108 | 0.8984 |
| left | 0 | 69 | 411 | 0.8562 |

| pred class | precision |
|---|---:|
| right | 0.8467 |
| straight | 0.9218 |
| left | 0.7859 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.227, 8.216] deg
- Slope 符号准确率: 1.0000

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 871 | 0.9621 | 0.4468 | 1.0000 | [2.006, 7.500] | [1.286, 8.216] |
| downhill | 560 | 0.9786 | 0.3508 | 1.0000 | [-5.500, -2.046] | [-6.227, -0.950] |
