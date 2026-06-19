# GRU 训练报告

- 生成时间: 2026-06-16 02:24:05
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\models\GRU_model_full_gru_v5_plantfix_passive17_plus_all5_seed21.mat`
- 最佳轮次: 29
- 最佳验证损失: 0.408493
- 最佳选择分数: 1.147118
- 主任务基座选择分数: 1.147118
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.080, 坡度=0.550, 平地坡度约束=0.120, 辅助=0.000, pitch一致性=0.000
- 平地坡度约束模式: `near_zero`, near-zero tol=0.300 deg
- 坡度符号权重: 负坡=1.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=1.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 转弯过渡选模: weight=1.200, target=0.750
- 左右转最小召回选模: weight=0.200, target=0.850
- 类别权重策略: main=`sqrt_inverse`, turn=`sqrt_inverse`
- 转弯类别乘子 [right straight left]: [1.080 1.000 1.080]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 128 steps / 1.280 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.383276 |
| 主工况准确率 | 0.9581 |
| 转弯准确率 | 0.5294 |
| 转弯纯窗口准确率 | 0.5595 |
| 转弯过渡窗口准确率 | 0.3979 |
| 坡度 MAE deg | 0.7310 |
| |theta|<=10 P95 deg | 2.0301 |
| [-10,-8] P95 deg | 2.0790 |
| [8,10] P95 deg | 3.3989 |
| [-2,-0.5] P95 deg | 2.3589 |
| [0.5,2] P95 deg | 2.1880 |
| near-flat abs P95 deg | 1.8749 |
| flat theta bias deg | 0.1629 |
| 主工况置信度均值 | 0.9584 |
| 主工况低置信度(<0.60)比例 | 0.0308 |
| 转弯置信度均值 | 0.6513 |
| 转弯低置信度(<0.60)比例 | 0.4620 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 724 | 4 | 28 | 0.9577 |
| stall | 13 | 58 | 25 | 0.6042 |
| slope | 52 | 29 | 2669 | 0.9705 |

| pred class | precision |
|---|---:|
| flat | 0.9176 |
| stall | 0.6374 |
| slope | 0.9805 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 263 | 390 | 146 | 0.3292 |
| straight | 265 | 1264 | 404 | 0.6539 |
| left | 153 | 337 | 380 | 0.4368 |

| pred class | precision |
|---|---:|
| right | 0.3862 |
| straight | 0.6349 |
| left | 0.4086 |

## 坡度回归范围

- Slope 真值范围: [-9.750, 9.750] deg
- Slope 预测范围: [-10.188, 14.244] deg
- Slope 符号准确率: 0.9546

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 1744 | 0.7494 | 0.7647 | 0.9679 | [0.056, 9.750] | [-1.862, 14.244] |
| downhill | 1762 | 0.7889 | 0.6976 | 0.9415 | [-9.750, -0.235] | [-10.188, 2.959] |

## 置信度分桶

### main

- mean: 0.9584
- error_mean: 0.7530
- low_conf_0p60_ratio: 0.0308
- low_conf_0p70_ratio: 0.0519

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 111 | 0.3514 | 0.5358 |
| [0.60,0.70) | 76 | 0.3421 | 0.6499 |
| [0.70,0.80) | 85 | 0.2471 | 0.7488 |
| [0.80,0.90) | 149 | 0.1611 | 0.8578 |
| [0.90,1.00) | 3181 | 0.0129 | 0.9908 |

### turn

- mean: 0.6513
- error_mean: 0.6027
- low_conf_0p60_ratio: 0.4620
- low_conf_0p70_ratio: 0.6416

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1664 | 0.5721 | 0.4965 |
| [0.60,0.70) | 647 | 0.4961 | 0.6461 |
| [0.70,0.80) | 426 | 0.4859 | 0.7474 |
| [0.80,0.90) | 379 | 0.3588 | 0.8507 |
| [0.90,1.00) | 486 | 0.1626 | 0.9485 |

