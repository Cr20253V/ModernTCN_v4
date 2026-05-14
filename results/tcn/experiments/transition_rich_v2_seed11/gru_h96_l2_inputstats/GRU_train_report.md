# GRU 训练报告

- 生成时间: 2026-04-28 17:17:13
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v2_transition_rich.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_transition_rich_v2_seed11_h96_l2_inputstats.mat`
- 最佳轮次: 35
- 最佳验证损失: 0.169789
- 最佳选择分数: 0.237195
- 主任务基座选择分数: 0.237195
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
| 总损失 | 0.146816 |
| 主工况准确率 | 0.9349 |
| 转弯准确率 | 0.8781 |
| 转弯纯窗口准确率 | 0.9185 |
| 转弯过渡窗口准确率 | 0.5950 |
| 坡度 MAE deg | 0.4407 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 536 | 8 | 29 | 0.9354 |
| stall | 0 | 76 | 2 | 0.9744 |
| slope | 3 | 21 | 293 | 0.9243 |

| pred class | precision |
|---|---:|
| flat | 0.9944 |
| stall | 0.7238 |
| slope | 0.9043 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 108 | 7 | 0 | 0.9391 |
| straight | 23 | 616 | 62 | 0.8787 |
| left | 5 | 21 | 126 | 0.8289 |

| pred class | precision |
|---|---:|
| right | 0.7941 |
| straight | 0.9565 |
| left | 0.6702 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 6.000] deg
- Slope 预测范围: [-5.482, 7.581] deg
- Slope 符号准确率: 0.9968

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 223 | 0.9103 | 0.4036 | 1.0000 | [2.014, 6.000] | [1.841, 7.581] |
| downhill | 94 | 0.9574 | 0.5287 | 0.9894 | [-5.500, -2.074] | [-5.482, 0.222] |
