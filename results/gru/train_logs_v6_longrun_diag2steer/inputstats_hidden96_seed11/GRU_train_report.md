# GRU 训练报告

- 生成时间: 2026-05-10 01:20:58
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v6_longrun_diag2steer.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_v6_longrun_diag2steer_inputstats_hidden96_seed11.mat`
- 最佳轮次: 10
- 最佳验证损失: 0.483932
- 最佳选择分数: 0.616046
- 主任务基座选择分数: 0.616046
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
| 总损失 | 0.400246 |
| 主工况准确率 | 0.9360 |
| 转弯准确率 | 0.9064 |
| 转弯纯窗口准确率 | 0.9261 |
| 转弯过渡窗口准确率 | 0.5269 |
| 坡度 MAE deg | 0.5327 |
| 主工况置信度均值 | 0.9040 |
| 主工况低置信度(<0.60)比例 | 0.0523 |
| 转弯置信度均值 | 0.9221 |
| 转弯低置信度(<0.60)比例 | 0.0338 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 1250 | 7 | 52 | 0.9549 |
| stall | 4 | 48 | 0 | 0.9231 |
| slope | 31 | 27 | 473 | 0.8908 |

| pred class | precision |
|---|---:|
| flat | 0.9728 |
| stall | 0.5854 |
| slope | 0.9010 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 242 | 37 | 6 | 0.8491 |
| straight | 48 | 1146 | 26 | 0.9393 |
| left | 0 | 60 | 327 | 0.8450 |

| pred class | precision |
|---|---:|
| right | 0.8345 |
| straight | 0.9220 |
| left | 0.9109 |

## 坡度回归范围

- Slope 真值范围: [-7.479, 7.500] deg
- Slope 预测范围: [-7.362, 9.149] deg
- Slope 符号准确率: 0.3321

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 363 | 0.7906 | 0.5880 | 0.9725 | [0.000, 7.500] | [-1.129, 9.149] |
| downhill | 283 | 0.7527 | 0.6676 | 0.9117 | [-7.479, -0.000] | [-7.362, 3.257] |

## 置信度分桶

### main

- mean: 0.9040
- error_mean: 0.7265
- low_conf_0p60_ratio: 0.0523
- low_conf_0p70_ratio: 0.0946

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 99 | 0.3939 | 0.5320 |
| [0.60,0.70) | 80 | 0.2125 | 0.6518 |
| [0.70,0.80) | 124 | 0.1855 | 0.7533 |
| [0.80,0.90) | 210 | 0.0714 | 0.8595 |
| [0.90,1.00) | 1379 | 0.0196 | 0.9656 |

### turn

- mean: 0.9221
- error_mean: 0.7765
- low_conf_0p60_ratio: 0.0338
- low_conf_0p70_ratio: 0.0793

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 64 | 0.5469 | 0.5340 |
| [0.60,0.70) | 86 | 0.3488 | 0.6495 |
| [0.70,0.80) | 125 | 0.2000 | 0.7579 |
| [0.80,0.90) | 210 | 0.1476 | 0.8608 |
| [0.90,1.00) | 1407 | 0.0398 | 0.9802 |

