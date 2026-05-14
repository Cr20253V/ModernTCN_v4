# GRU 训练报告

- 生成时间: 2026-05-12 21:03:40
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed73.mat`
- 最佳轮次: 82
- 最佳验证损失: 0.180125
- 最佳选择分数: 0.592676
- 主任务基座选择分数: 0.592676
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
| 总损失 | 0.425379 |
| 主工况准确率 | 0.9796 |
| 转弯准确率 | 0.7758 |
| 转弯纯窗口准确率 | 0.8208 |
| 转弯过渡窗口准确率 | 0.5065 |
| 坡度 MAE deg | 0.2775 |
| |theta|<=10 P95 deg | 0.8468 |
| [-10,-8] P95 deg | 0.6573 |
| [8,10] P95 deg | 0.6025 |
| [-2,-0.5] P95 deg | 0.7144 |
| [0.5,2] P95 deg | 1.5143 |
| near-flat abs P95 deg | 1.2347 |
| flat theta bias deg | 0.0727 |
| 主工况置信度均值 | 0.9870 |
| 主工况低置信度(<0.60)比例 | 0.0054 |
| 转弯置信度均值 | 0.8024 |
| 转弯低置信度(<0.60)比例 | 0.1768 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 730 | 0 | 27 | 0.9643 |
| stall | 5 | 81 | 31 | 0.6923 |
| slope | 4 | 9 | 2846 | 0.9955 |

| pred class | precision |
|---|---:|
| flat | 0.9878 |
| stall | 0.9000 |
| slope | 0.9800 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 602 | 179 | 32 | 0.7405 |
| straight | 250 | 1707 | 231 | 0.7802 |
| left | 23 | 122 | 587 | 0.8019 |

| pred class | precision |
|---|---:|
| right | 0.6880 |
| straight | 0.8501 |
| left | 0.6906 |

## 坡度回归范围

- Slope 真值范围: [-9.900, 9.500] deg
- Slope 预测范围: [-10.247, 10.372] deg
- Slope 符号准确率: 0.9953

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 1753 | 0.8055 | 0.3215 | 0.9994 | [0.019, 9.500] | [-0.020, 10.372] |
| downhill | 1863 | 0.7842 | 0.2360 | 0.9914 | [-9.900, -0.130] | [-10.247, 1.488] |

## 置信度分桶

### main

- mean: 0.9870
- error_mean: 0.8518
- low_conf_0p60_ratio: 0.0054
- low_conf_0p70_ratio: 0.0104

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 20 | 0.5500 | 0.5299 |
| [0.60,0.70) | 19 | 0.2632 | 0.6523 |
| [0.70,0.80) | 42 | 0.2381 | 0.7562 |
| [0.80,0.90) | 66 | 0.1212 | 0.8599 |
| [0.90,1.00) | 3586 | 0.0117 | 0.9964 |

### turn

- mean: 0.8024
- error_mean: 0.6791
- low_conf_0p60_ratio: 0.1768
- low_conf_0p70_ratio: 0.2877

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 660 | 0.4864 | 0.5204 |
| [0.60,0.70) | 414 | 0.3309 | 0.6490 |
| [0.70,0.80) | 509 | 0.2947 | 0.7524 |
| [0.80,0.90) | 634 | 0.2098 | 0.8520 |
| [0.90,1.00) | 1516 | 0.0633 | 0.9630 |

