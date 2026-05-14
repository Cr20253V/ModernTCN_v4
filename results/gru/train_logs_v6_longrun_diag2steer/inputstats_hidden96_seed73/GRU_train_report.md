# GRU 训练报告

- 生成时间: 2026-05-10 01:58:43
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v6_longrun_diag2steer.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_v6_longrun_diag2steer_inputstats_hidden96_seed73.mat`
- 最佳轮次: 11
- 最佳验证损失: 0.561451
- 最佳选择分数: 0.691199
- 主任务基座选择分数: 0.691199
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
| 总损失 | 0.430428 |
| 主工况准确率 | 0.9366 |
| 转弯准确率 | 0.9096 |
| 转弯纯窗口准确率 | 0.9283 |
| 转弯过渡窗口准确率 | 0.5484 |
| 坡度 MAE deg | 0.5556 |
| 主工况置信度均值 | 0.9057 |
| 主工况低置信度(<0.60)比例 | 0.0354 |
| 转弯置信度均值 | 0.9247 |
| 转弯低置信度(<0.60)比例 | 0.0375 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 1242 | 12 | 55 | 0.9488 |
| stall | 4 | 47 | 1 | 0.9038 |
| slope | 27 | 21 | 483 | 0.9096 |

| pred class | precision |
|---|---:|
| flat | 0.9756 |
| stall | 0.5875 |
| slope | 0.8961 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 244 | 33 | 8 | 0.8561 |
| straight | 44 | 1147 | 29 | 0.9402 |
| left | 0 | 57 | 330 | 0.8527 |

| pred class | precision |
|---|---:|
| right | 0.8472 |
| straight | 0.9272 |
| left | 0.8992 |

## 坡度回归范围

- Slope 真值范围: [-7.479, 7.500] deg
- Slope 预测范围: [-7.511, 7.812] deg
- Slope 符号准确率: 0.3380

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 363 | 0.8099 | 0.6784 | 0.9752 | [0.000, 7.500] | [-0.934, 7.812] |
| downhill | 283 | 0.7880 | 0.5116 | 0.9470 | [-7.479, -0.000] | [-7.511, 1.241] |

## 置信度分桶

### main

- mean: 0.9057
- error_mean: 0.7553
- low_conf_0p60_ratio: 0.0354
- low_conf_0p70_ratio: 0.0819

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 67 | 0.4179 | 0.5372 |
| [0.60,0.70) | 88 | 0.2500 | 0.6570 |
| [0.70,0.80) | 135 | 0.1556 | 0.7546 |
| [0.80,0.90) | 238 | 0.0714 | 0.8553 |
| [0.90,1.00) | 1364 | 0.0235 | 0.9636 |

### turn

- mean: 0.9247
- error_mean: 0.7721
- low_conf_0p60_ratio: 0.0375
- low_conf_0p70_ratio: 0.0766

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 71 | 0.5211 | 0.5363 |
| [0.60,0.70) | 74 | 0.3784 | 0.6532 |
| [0.70,0.80) | 107 | 0.2243 | 0.7550 |
| [0.80,0.90) | 210 | 0.1476 | 0.8570 |
| [0.90,1.00) | 1430 | 0.0357 | 0.9807 |

