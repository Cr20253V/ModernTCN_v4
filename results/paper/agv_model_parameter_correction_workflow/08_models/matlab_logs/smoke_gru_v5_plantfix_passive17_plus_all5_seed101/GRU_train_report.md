# GRU 训练报告

- 生成时间: 2026-06-15 23:02:43
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\models\GRU_model_smoke_gru_v5_plantfix_passive17_plus_all5_seed101.mat`
- 最佳轮次: 20
- 最佳验证损失: 0.402271
- 最佳选择分数: 1.224153
- 主任务基座选择分数: 1.224153
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
| 总损失 | 0.354828 |
| 主工况准确率 | 0.9498 |
| 转弯准确率 | 0.5108 |
| 转弯纯窗口准确率 | 0.5401 |
| 转弯过渡窗口准确率 | 0.3830 |
| 坡度 MAE deg | 0.6102 |
| |theta|<=10 P95 deg | 1.9146 |
| [-10,-8] P95 deg | 1.5057 |
| [8,10] P95 deg | 2.9096 |
| [-2,-0.5] P95 deg | 2.7011 |
| [0.5,2] P95 deg | 1.7534 |
| near-flat abs P95 deg | 2.4739 |
| flat theta bias deg | 0.3099 |
| 主工况置信度均值 | 0.9351 |
| 主工况低置信度(<0.60)比例 | 0.0378 |
| 转弯置信度均值 | 0.6023 |
| 转弯低置信度(<0.60)比例 | 0.5788 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 716 | 4 | 36 | 0.9471 |
| stall | 11 | 59 | 26 | 0.6146 |
| slope | 74 | 30 | 2646 | 0.9622 |

| pred class | precision |
|---|---:|
| flat | 0.8939 |
| stall | 0.6344 |
| slope | 0.9771 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 356 | 281 | 162 | 0.4456 |
| straight | 399 | 1088 | 446 | 0.5629 |
| left | 180 | 294 | 396 | 0.4552 |

| pred class | precision |
|---|---:|
| right | 0.3807 |
| straight | 0.6542 |
| left | 0.3944 |

## 坡度回归范围

- Slope 真值范围: [-9.750, 9.750] deg
- Slope 预测范围: [-10.087, 12.188] deg
- Slope 符号准确率: 0.9675

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 1744 | 0.7345 | 0.6347 | 0.9845 | [0.056, 9.750] | [-1.123, 12.188] |
| downhill | 1762 | 0.7951 | 0.5860 | 0.9506 | [-9.750, -0.235] | [-10.087, 2.597] |

## 置信度分桶

### main

- mean: 0.9351
- error_mean: 0.7332
- low_conf_0p60_ratio: 0.0378
- low_conf_0p70_ratio: 0.0738

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 136 | 0.3529 | 0.5233 |
| [0.60,0.70) | 130 | 0.2692 | 0.6506 |
| [0.70,0.80) | 152 | 0.1776 | 0.7543 |
| [0.80,0.90) | 248 | 0.1210 | 0.8577 |
| [0.90,1.00) | 2936 | 0.0140 | 0.9827 |

### turn

- mean: 0.6023
- error_mean: 0.5573
- low_conf_0p60_ratio: 0.5788
- low_conf_0p70_ratio: 0.7493

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 2085 | 0.5746 | 0.4910 |
| [0.60,0.70) | 614 | 0.5098 | 0.6447 |
| [0.70,0.80) | 318 | 0.4182 | 0.7479 |
| [0.80,0.90) | 405 | 0.2272 | 0.8461 |
| [0.90,1.00) | 180 | 0.1444 | 0.9420 |

