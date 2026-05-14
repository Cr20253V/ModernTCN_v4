# GRU 训练报告

- 生成时间: 2026-05-10 01:33:10
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v6_longrun_diag2steer.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_v6_longrun_diag2steer_inputstats_hidden96_seed21.mat`
- 最佳轮次: 9
- 最佳验证损失: 0.528333
- 最佳选择分数: 0.665401
- 主任务基座选择分数: 0.665401
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
| 总损失 | 0.398639 |
| 主工况准确率 | 0.9387 |
| 转弯准确率 | 0.9006 |
| 转弯纯窗口准确率 | 0.9200 |
| 转弯过渡窗口准确率 | 0.5269 |
| 坡度 MAE deg | 0.6333 |
| 主工况置信度均值 | 0.9039 |
| 主工况低置信度(<0.60)比例 | 0.0407 |
| 转弯置信度均值 | 0.9254 |
| 转弯低置信度(<0.60)比例 | 0.0396 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 1247 | 8 | 54 | 0.9526 |
| stall | 4 | 47 | 1 | 0.9038 |
| slope | 30 | 19 | 482 | 0.9077 |

| pred class | precision |
|---|---:|
| flat | 0.9735 |
| stall | 0.6351 |
| slope | 0.8976 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 232 | 38 | 15 | 0.8140 |
| straight | 46 | 1146 | 28 | 0.9393 |
| left | 0 | 61 | 326 | 0.8424 |

| pred class | precision |
|---|---:|
| right | 0.8345 |
| straight | 0.9205 |
| left | 0.8835 |

## 坡度回归范围

- Slope 真值范围: [-7.479, 7.500] deg
- Slope 预测范围: [-7.925, 9.871] deg
- Slope 符号准确率: 0.3310

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 363 | 0.7851 | 0.4167 | 0.9532 | [0.000, 7.500] | [-0.894, 9.871] |
| downhill | 283 | 0.7809 | 0.5200 | 0.9293 | [-7.479, -0.000] | [-7.925, 1.465] |

## 置信度分桶

### main

- mean: 0.9039
- error_mean: 0.7600
- low_conf_0p60_ratio: 0.0407
- low_conf_0p70_ratio: 0.0862

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 77 | 0.3766 | 0.5291 |
| [0.60,0.70) | 86 | 0.2326 | 0.6553 |
| [0.70,0.80) | 108 | 0.1019 | 0.7587 |
| [0.80,0.90) | 278 | 0.0755 | 0.8511 |
| [0.90,1.00) | 1343 | 0.0261 | 0.9639 |

### turn

- mean: 0.9254
- error_mean: 0.7626
- low_conf_0p60_ratio: 0.0396
- low_conf_0p70_ratio: 0.0751

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 75 | 0.6267 | 0.5340 |
| [0.60,0.70) | 67 | 0.4179 | 0.6476 |
| [0.70,0.80) | 115 | 0.2348 | 0.7524 |
| [0.80,0.90) | 149 | 0.2148 | 0.8522 |
| [0.90,1.00) | 1486 | 0.0363 | 0.9784 |

