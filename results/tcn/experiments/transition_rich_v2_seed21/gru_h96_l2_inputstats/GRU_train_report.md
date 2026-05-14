# GRU 训练报告

- 生成时间: 2026-04-28 17:53:37
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v2_transition_rich.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_transition_rich_v2_seed21_h96_l2_inputstats.mat`
- 最佳轮次: 41
- 最佳验证损失: 0.170526
- 最佳选择分数: 0.236732
- 主任务基座选择分数: 0.236732
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
| 总损失 | 0.125963 |
| 主工况准确率 | 0.9494 |
| 转弯准确率 | 0.8905 |
| 转弯纯窗口准确率 | 0.9327 |
| 转弯过渡窗口准确率 | 0.5950 |
| 坡度 MAE deg | 0.3582 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 546 | 4 | 23 | 0.9529 |
| stall | 0 | 76 | 2 | 0.9744 |
| slope | 3 | 17 | 297 | 0.9369 |

| pred class | precision |
|---|---:|
| flat | 0.9945 |
| stall | 0.7835 |
| slope | 0.9224 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 110 | 5 | 0 | 0.9565 |
| straight | 17 | 621 | 63 | 0.8859 |
| left | 5 | 16 | 131 | 0.8618 |

| pred class | precision |
|---|---:|
| right | 0.8333 |
| straight | 0.9673 |
| left | 0.6753 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 6.000] deg
- Slope 预测范围: [-6.148, 9.101] deg
- Slope 符号准确率: 0.9968

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 223 | 0.9283 | 0.3615 | 1.0000 | [2.014, 6.000] | [1.698, 9.101] |
| downhill | 94 | 0.9574 | 0.3502 | 0.9894 | [-5.500, -2.074] | [-6.148, 0.867] |
