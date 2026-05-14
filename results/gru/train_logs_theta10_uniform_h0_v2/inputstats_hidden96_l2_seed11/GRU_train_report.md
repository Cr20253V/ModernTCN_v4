# GRU 训练报告

- 生成时间: 2026-05-12 16:58:55
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed11.mat`
- 最佳轮次: 74
- 最佳验证损失: 0.181728
- 最佳选择分数: 0.611057
- 主任务基座选择分数: 0.611057
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.080, 坡度=0.550, 平地坡度约束=0.120, 辅助=0.000, pitch一致性=0.000
- 平地坡度约束模式: `near_zero`, near-zero tol=0.300 deg
- 坡度符号权重: 负坡=1.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=1.000, 正坡=1.000
- 下坡选模惩罚权重: 0.000
- 转弯过渡选模: weight=1.200, target=0.750
- 左右转最小召回选模: weight=0.200, target=0.850
- 类别权重策略: main=`sqrt_inverse`, turn=`sqrt_inverse`
- 转弯类别乘子 [right straight left]: [1.080 1.000 1.080]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 128 steps / 1.280 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.392608 |
| 主工况准确率 | 0.9743 |
| 转弯准确率 | 0.7688 |
| 转弯纯窗口准确率 | 0.8089 |
| 转弯过渡窗口准确率 | 0.5290 |
| 坡度 MAE deg | 0.3385 |
| |theta|<=10 P95 deg | 1.0614 |
| [-10,-8] P95 deg | 0.7740 |
| [8,10] P95 deg | 0.8141 |
| [-2,-0.5] P95 deg | 0.7669 |
| [0.5,2] P95 deg | 1.8059 |
| near-flat abs P95 deg | 1.3009 |
| flat theta bias deg | 0.2886 |
| 主工况置信度均值 | 0.9835 |
| 主工况低置信度(<0.60)比例 | 0.0091 |
| 转弯置信度均值 | 0.8014 |
| 转弯低置信度(<0.60)比例 | 0.1864 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 727 | 1 | 29 | 0.9604 |
| stall | 4 | 78 | 35 | 0.6667 |
| slope | 9 | 18 | 2832 | 0.9906 |

| pred class | precision |
|---|---:|
| flat | 0.9824 |
| stall | 0.8041 |
| slope | 0.9779 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 611 | 160 | 42 | 0.7515 |
| straight | 255 | 1685 | 248 | 0.7701 |
| left | 11 | 147 | 574 | 0.7842 |

| pred class | precision |
|---|---:|
| right | 0.6967 |
| straight | 0.8459 |
| left | 0.6644 |

## 坡度回归范围

- Slope 真值范围: [-9.900, 9.500] deg
- Slope 预测范围: [-10.557, 10.619] deg
- Slope 符号准确率: 0.9873

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 1753 | 0.8072 | 0.4242 | 1.0000 | [0.019, 9.500] | [0.222, 10.619] |
| downhill | 1863 | 0.7762 | 0.2578 | 0.9753 | [-9.900, -0.130] | [-10.557, 1.953] |

## 置信度分桶

### main

- mean: 0.9835
- error_mean: 0.8229
- low_conf_0p60_ratio: 0.0091
- low_conf_0p70_ratio: 0.0190

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 34 | 0.4706 | 0.5418 |
| [0.60,0.70) | 37 | 0.2703 | 0.6503 |
| [0.70,0.80) | 46 | 0.3043 | 0.7505 |
| [0.80,0.90) | 62 | 0.1935 | 0.8586 |
| [0.90,1.00) | 3554 | 0.0124 | 0.9964 |

### turn

- mean: 0.8014
- error_mean: 0.6684
- low_conf_0p60_ratio: 0.1864
- low_conf_0p70_ratio: 0.3078

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 696 | 0.4741 | 0.5144 |
| [0.60,0.70) | 453 | 0.3775 | 0.6523 |
| [0.70,0.80) | 444 | 0.3514 | 0.7487 |
| [0.80,0.90) | 589 | 0.1919 | 0.8544 |
| [0.90,1.00) | 1551 | 0.0600 | 0.9687 |

