# GRU 训练报告

- 生成时间: 2026-05-10 02:11:04
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v6_longrun_diag2steer.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_v6_longrun_diag2steer_inputstats_hidden96_seed101.mat`
- 最佳轮次: 8
- 最佳验证损失: 0.488773
- 最佳选择分数: 0.633987
- 主任务基座选择分数: 0.633987
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
| 总损失 | 0.395649 |
| 主工况准确率 | 0.9149 |
| 转弯准确率 | 0.9064 |
| 转弯纯窗口准确率 | 0.9250 |
| 转弯过渡窗口准确率 | 0.5484 |
| 坡度 MAE deg | 0.6453 |
| 主工况置信度均值 | 0.8683 |
| 主工况低置信度(<0.60)比例 | 0.0698 |
| 转弯置信度均值 | 0.9267 |
| 转弯低置信度(<0.60)比例 | 0.0359 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 1224 | 9 | 76 | 0.9351 |
| stall | 4 | 48 | 0 | 0.9231 |
| slope | 33 | 39 | 459 | 0.8644 |

| pred class | precision |
|---|---:|
| flat | 0.9707 |
| stall | 0.5000 |
| slope | 0.8579 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 240 | 34 | 11 | 0.8421 |
| straight | 47 | 1146 | 27 | 0.9393 |
| left | 0 | 58 | 329 | 0.8501 |

| pred class | precision |
|---|---:|
| right | 0.8362 |
| straight | 0.9257 |
| left | 0.8965 |

## 坡度回归范围

- Slope 真值范围: [-7.479, 7.500] deg
- Slope 预测范围: [-8.532, 10.002] deg
- Slope 符号准确率: 0.3375

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 363 | 0.7493 | 0.5866 | 0.9835 | [0.000, 7.500] | [-0.824, 10.002] |
| downhill | 283 | 0.7774 | 0.6946 | 0.9329 | [-7.479, -0.000] | [-8.329, 4.329] |

## 置信度分桶

### main

- mean: 0.8683
- error_mean: 0.6916
- low_conf_0p60_ratio: 0.0698
- low_conf_0p70_ratio: 0.1369

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 132 | 0.5000 | 0.5169 |
| [0.60,0.70) | 127 | 0.1732 | 0.6513 |
| [0.70,0.80) | 193 | 0.1399 | 0.7466 |
| [0.80,0.90) | 251 | 0.0398 | 0.8563 |
| [0.90,1.00) | 1189 | 0.0303 | 0.9528 |

### turn

- mean: 0.9267
- error_mean: 0.7868
- low_conf_0p60_ratio: 0.0359
- low_conf_0p70_ratio: 0.0782

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 68 | 0.4706 | 0.5431 |
| [0.60,0.70) | 80 | 0.3625 | 0.6621 |
| [0.70,0.80) | 79 | 0.3038 | 0.7533 |
| [0.80,0.90) | 203 | 0.1872 | 0.8534 |
| [0.90,1.00) | 1462 | 0.0369 | 0.9786 |

