# GRU 训练报告

- 生成时间: 2026-05-12 22:36:12
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed101.mat`
- 最佳轮次: 73
- 最佳验证损失: 0.166225
- 最佳选择分数: 0.581197
- 主任务基座选择分数: 0.581197
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
| 总损失 | 0.379202 |
| 主工况准确率 | 0.9767 |
| 转弯准确率 | 0.7680 |
| 转弯纯窗口准确率 | 0.8083 |
| 转弯过渡窗口准确率 | 0.5271 |
| 坡度 MAE deg | 0.2601 |
| |theta|<=10 P95 deg | 0.7790 |
| [-10,-8] P95 deg | 0.7239 |
| [8,10] P95 deg | 0.6718 |
| [-2,-0.5] P95 deg | 0.6792 |
| [0.5,2] P95 deg | 1.1057 |
| near-flat abs P95 deg | 0.9190 |
| flat theta bias deg | 0.1341 |
| 主工况置信度均值 | 0.9857 |
| 主工况低置信度(<0.60)比例 | 0.0070 |
| 转弯置信度均值 | 0.7969 |
| 转弯低置信度(<0.60)比例 | 0.1942 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 727 | 2 | 28 | 0.9604 |
| stall | 4 | 79 | 34 | 0.6752 |
| slope | 6 | 13 | 2840 | 0.9934 |

| pred class | precision |
|---|---:|
| flat | 0.9864 |
| stall | 0.8404 |
| slope | 0.9786 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 597 | 191 | 25 | 0.7343 |
| straight | 231 | 1735 | 222 | 0.7930 |
| left | 18 | 179 | 535 | 0.7309 |

| pred class | precision |
|---|---:|
| right | 0.7057 |
| straight | 0.8242 |
| left | 0.6841 |

## 坡度回归范围

- Slope 真值范围: [-9.900, 9.500] deg
- Slope 预测范围: [-10.415, 10.397] deg
- Slope 符号准确率: 0.9931

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 1753 | 0.8066 | 0.2890 | 1.0000 | [0.019, 9.500] | [0.034, 10.397] |
| downhill | 1863 | 0.7805 | 0.2328 | 0.9866 | [-9.900, -0.130] | [-10.415, 1.653] |

## 置信度分桶

### main

- mean: 0.9857
- error_mean: 0.8424
- low_conf_0p60_ratio: 0.0070
- low_conf_0p70_ratio: 0.0153

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 26 | 0.4231 | 0.5351 |
| [0.60,0.70) | 31 | 0.4194 | 0.6460 |
| [0.70,0.80) | 30 | 0.1667 | 0.7509 |
| [0.80,0.90) | 61 | 0.1967 | 0.8538 |
| [0.90,1.00) | 3585 | 0.0128 | 0.9962 |

### turn

- mean: 0.7969
- error_mean: 0.6718
- low_conf_0p60_ratio: 0.1942
- low_conf_0p70_ratio: 0.3169

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 725 | 0.4910 | 0.5182 |
| [0.60,0.70) | 458 | 0.3166 | 0.6509 |
| [0.70,0.80) | 486 | 0.2840 | 0.7527 |
| [0.80,0.90) | 567 | 0.2575 | 0.8520 |
| [0.90,1.00) | 1497 | 0.0541 | 0.9701 |

