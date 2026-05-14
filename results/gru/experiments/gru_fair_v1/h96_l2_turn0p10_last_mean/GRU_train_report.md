# GRU 训练报告

- 生成时间: 2026-04-26 23:20:55
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_fair_v1_h96_l2_turn0p10_last_mean.mat`
- 最佳轮次: 20
- 最佳验证损失: 0.565297
- 最佳选择分数: 0.681742
- 主任务基座选择分数: 0.681742
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean`
- Turn head: `linear`, source=`readout`, hidden=64
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
| 总损失 | 0.852073 |
| 主工况准确率 | 0.9326 |
| 转弯准确率 | 0.7843 |
| 转弯纯窗口准确率 | 0.8342 |
| 转弯过渡窗口准确率 | 0.2927 |
| 坡度 MAE deg | 0.9751 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 250 | 6 | 9 | 0.9434 |
| stall | 2 | 11 | 5 | 0.6111 |
| slope | 1 | 7 | 154 | 0.9506 |

| pred class | precision |
|---|---:|
| flat | 0.9881 |
| stall | 0.4583 |
| slope | 0.9167 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 51 | 14 | 7 | 0.7083 |
| straight | 21 | 246 | 24 | 0.8454 |
| left | 10 | 20 | 52 | 0.6341 |

| pred class | precision |
|---|---:|
| right | 0.6220 |
| straight | 0.8786 |
| left | 0.6265 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.952, 9.555] deg
- Slope 符号准确率: 0.9938

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9774 | 0.9234 | 1.0000 | [2.884, 7.500] | [1.144, 9.555] |
| downhill | 29 | 0.8276 | 1.2124 | 0.9655 | [-5.500, -2.298] | [-6.952, 0.196] |
