# GRU 训练报告

- 生成时间: 2026-05-12 19:24:27
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed42.mat`
- 最佳轮次: 70
- 最佳验证损失: 0.142439
- 最佳选择分数: 0.617189
- 主任务基座选择分数: 0.617189
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
| 总损失 | 0.404361 |
| 主工况准确率 | 0.9751 |
| 转弯准确率 | 0.7645 |
| 转弯纯窗口准确率 | 0.8039 |
| 转弯过渡窗口准确率 | 0.5290 |
| 坡度 MAE deg | 0.3217 |
| |theta|<=10 P95 deg | 1.1098 |
| [-10,-8] P95 deg | 0.6406 |
| [8,10] P95 deg | 1.0093 |
| [-2,-0.5] P95 deg | 0.8706 |
| [0.5,2] P95 deg | 1.3514 |
| near-flat abs P95 deg | 1.4166 |
| flat theta bias deg | 0.0093 |
| 主工况置信度均值 | 0.9849 |
| 主工况低置信度(<0.60)比例 | 0.0067 |
| 转弯置信度均值 | 0.7973 |
| 转弯低置信度(<0.60)比例 | 0.1969 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 723 | 4 | 30 | 0.9551 |
| stall | 5 | 76 | 36 | 0.6496 |
| slope | 3 | 15 | 2841 | 0.9937 |

| pred class | precision |
|---|---:|
| flat | 0.9891 |
| stall | 0.8000 |
| slope | 0.9773 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 617 | 147 | 49 | 0.7589 |
| straight | 249 | 1652 | 287 | 0.7550 |
| left | 21 | 126 | 585 | 0.7992 |

| pred class | precision |
|---|---:|
| right | 0.6956 |
| straight | 0.8582 |
| left | 0.6352 |

## 坡度回归范围

- Slope 真值范围: [-9.900, 9.500] deg
- Slope 预测范围: [-10.380, 11.256] deg
- Slope 符号准确率: 0.9945

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 1753 | 0.8100 | 0.3462 | 0.9954 | [0.019, 9.500] | [-0.521, 11.256] |
| downhill | 1863 | 0.7789 | 0.2987 | 0.9936 | [-9.900, -0.130] | [-10.380, 1.508] |

## 置信度分桶

### main

- mean: 0.9849
- error_mean: 0.8410
- low_conf_0p60_ratio: 0.0067
- low_conf_0p70_ratio: 0.0150

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 25 | 0.4400 | 0.5427 |
| [0.60,0.70) | 31 | 0.5161 | 0.6494 |
| [0.70,0.80) | 43 | 0.1628 | 0.7553 |
| [0.80,0.90) | 54 | 0.1852 | 0.8607 |
| [0.90,1.00) | 3580 | 0.0137 | 0.9955 |

### turn

- mean: 0.7973
- error_mean: 0.6598
- low_conf_0p60_ratio: 0.1969
- low_conf_0p70_ratio: 0.3134

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 735 | 0.5007 | 0.5064 |
| [0.60,0.70) | 435 | 0.3678 | 0.6490 |
| [0.70,0.80) | 452 | 0.2876 | 0.7518 |
| [0.80,0.90) | 508 | 0.2165 | 0.8524 |
| [0.90,1.00) | 1603 | 0.0692 | 0.9662 |

