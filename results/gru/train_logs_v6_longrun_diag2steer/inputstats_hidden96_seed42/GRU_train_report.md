# GRU 训练报告

- 生成时间: 2026-05-10 01:44:56
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v6_longrun_diag2steer.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_v6_longrun_diag2steer_inputstats_hidden96_seed42.mat`
- 最佳轮次: 7
- 最佳验证损失: 0.481413
- 最佳选择分数: 0.610991
- 主任务基座选择分数: 0.610991
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.080, 坡度=0.350, 平地坡度约束=0.250, 辅助=0.000, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`none`
- 转弯类别乘子 [right straight left]: [1.050 1.000 1.050]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 128 steps / 1.280 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.402552 |
| 主工况准确率 | 0.9186 |
| 转弯准确率 | 0.9012 |
| 转弯纯窗口准确率 | 0.9211 |
| 转弯过渡窗口准确率 | 0.5161 |
| 坡度 MAE deg | 0.5180 |
| 主工况置信度均值 | 0.8680 |
| 主工况低置信度(<0.60)比例 | 0.0708 |
| 转弯置信度均值 | 0.9112 |
| 转弯低置信度(<0.60)比例 | 0.0486 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 1227 | 10 | 72 | 0.9374 |
| stall | 3 | 49 | 0 | 0.9423 |
| slope | 35 | 34 | 462 | 0.8701 |

| pred class | precision |
|---|---:|
| flat | 0.9700 |
| stall | 0.5269 |
| slope | 0.8652 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 242 | 28 | 15 | 0.8491 |
| straight | 56 | 1134 | 30 | 0.9295 |
| left | 0 | 58 | 329 | 0.8501 |

| pred class | precision |
|---|---:|
| right | 0.8121 |
| straight | 0.9295 |
| left | 0.8797 |

## 坡度回归范围

- Slope 真值范围: [-7.479, 7.500] deg
- Slope 预测范围: [-9.218, 10.420] deg
- Slope 符号准确率: 0.3375

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 363 | 0.7631 | 0.4490 | 0.9862 | [0.000, 7.500] | [-0.932, 10.420] |
| downhill | 283 | 0.7668 | 0.5918 | 0.9293 | [-7.479, -0.000] | [-9.218, 1.596] |

## 置信度分桶

### main

- mean: 0.8680
- error_mean: 0.7087
- low_conf_0p60_ratio: 0.0708
- low_conf_0p70_ratio: 0.1411

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 134 | 0.4254 | 0.5325 |
| [0.60,0.70) | 133 | 0.1955 | 0.6527 |
| [0.70,0.80) | 174 | 0.1092 | 0.7569 |
| [0.80,0.90) | 363 | 0.0551 | 0.8531 |
| [0.90,1.00) | 1088 | 0.0294 | 0.9583 |

### turn

- mean: 0.9112
- error_mean: 0.7593
- low_conf_0p60_ratio: 0.0486
- low_conf_0p70_ratio: 0.0925

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 92 | 0.4783 | 0.5395 |
| [0.60,0.70) | 83 | 0.3855 | 0.6527 |
| [0.70,0.80) | 143 | 0.1958 | 0.7533 |
| [0.80,0.90) | 215 | 0.1581 | 0.8571 |
| [0.90,1.00) | 1359 | 0.0361 | 0.9773 |

