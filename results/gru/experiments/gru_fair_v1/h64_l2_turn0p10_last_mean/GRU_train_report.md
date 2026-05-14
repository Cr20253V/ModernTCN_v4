# GRU 训练报告

- 生成时间: 2026-04-26 22:32:06
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_fair_v1_h64_l2_turn0p10_last_mean.mat`
- 最佳轮次: 20
- 最佳验证损失: 0.541339
- 最佳选择分数: 0.681136
- 主任务基座选择分数: 0.681136
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
| 总损失 | 0.721353 |
| 主工况准确率 | 0.9348 |
| 转弯准确率 | 0.7775 |
| 转弯纯窗口准确率 | 0.8218 |
| 转弯过渡窗口准确率 | 0.3415 |
| 坡度 MAE deg | 1.5316 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 251 | 4 | 10 | 0.9472 |
| stall | 1 | 13 | 4 | 0.7222 |
| slope | 1 | 9 | 152 | 0.9383 |

| pred class | precision |
|---|---:|
| flat | 0.9921 |
| stall | 0.5000 |
| slope | 0.9157 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 51 | 13 | 8 | 0.7083 |
| straight | 23 | 247 | 21 | 0.8488 |
| left | 10 | 24 | 48 | 0.5854 |

| pred class | precision |
|---|---:|
| right | 0.6071 |
| straight | 0.8697 |
| left | 0.6234 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-7.619, 7.178] deg
- Slope 符号准确率: 0.9815

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9549 | 1.4806 | 1.0000 | [2.884, 7.500] | [0.883, 7.178] |
| downhill | 29 | 0.8621 | 1.7653 | 0.8966 | [-5.500, -2.298] | [-7.619, 2.253] |
