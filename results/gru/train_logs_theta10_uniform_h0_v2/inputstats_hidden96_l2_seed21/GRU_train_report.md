# GRU 训练报告

- 生成时间: 2026-05-12 18:00:44
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed21.mat`
- 最佳轮次: 45
- 最佳验证损失: 0.166155
- 最佳选择分数: 0.656458
- 主任务基座选择分数: 0.656458
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
| 总损失 | 0.396240 |
| 主工况准确率 | 0.9719 |
| 转弯准确率 | 0.7568 |
| 转弯纯窗口准确率 | 0.7967 |
| 转弯过渡窗口准确率 | 0.5178 |
| 坡度 MAE deg | 0.5346 |
| |theta|<=10 P95 deg | 1.3598 |
| [-10,-8] P95 deg | 1.7504 |
| [8,10] P95 deg | 1.3607 |
| [-2,-0.5] P95 deg | 1.1232 |
| [0.5,2] P95 deg | 1.2909 |
| near-flat abs P95 deg | 1.5682 |
| flat theta bias deg | -0.0958 |
| 主工况置信度均值 | 0.9782 |
| 主工况低置信度(<0.60)比例 | 0.0094 |
| 转弯置信度均值 | 0.7846 |
| 转弯低置信度(<0.60)比例 | 0.2116 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 730 | 2 | 25 | 0.9643 |
| stall | 4 | 79 | 34 | 0.6752 |
| slope | 6 | 34 | 2819 | 0.9860 |

| pred class | precision |
|---|---:|
| flat | 0.9865 |
| stall | 0.6870 |
| slope | 0.9795 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 643 | 133 | 37 | 0.7909 |
| straight | 303 | 1623 | 262 | 0.7418 |
| left | 25 | 148 | 559 | 0.7637 |

| pred class | precision |
|---|---:|
| right | 0.6622 |
| straight | 0.8524 |
| left | 0.6515 |

## 坡度回归范围

- Slope 真值范围: [-9.900, 9.500] deg
- Slope 预测范围: [-11.553, 9.937] deg
- Slope 符号准确率: 0.9812

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 1753 | 0.8038 | 0.5396 | 0.9772 | [0.019, 9.500] | [-3.333, 9.937] |
| downhill | 1863 | 0.7703 | 0.5299 | 0.9850 | [-9.900, -0.130] | [-11.553, 1.298] |

## 置信度分桶

### main

- mean: 0.9782
- error_mean: 0.8279
- low_conf_0p60_ratio: 0.0094
- low_conf_0p70_ratio: 0.0228

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 35 | 0.3429 | 0.5411 |
| [0.60,0.70) | 50 | 0.3400 | 0.6413 |
| [0.70,0.80) | 58 | 0.1724 | 0.7503 |
| [0.80,0.90) | 81 | 0.1852 | 0.8539 |
| [0.90,1.00) | 3509 | 0.0145 | 0.9940 |

### turn

- mean: 0.7846
- error_mean: 0.6438
- low_conf_0p60_ratio: 0.2116
- low_conf_0p70_ratio: 0.3415

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 790 | 0.5241 | 0.5086 |
| [0.60,0.70) | 485 | 0.3361 | 0.6530 |
| [0.70,0.80) | 502 | 0.2749 | 0.7507 |
| [0.80,0.90) | 560 | 0.2143 | 0.8514 |
| [0.90,1.00) | 1396 | 0.0523 | 0.9719 |

