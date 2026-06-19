# GRU 训练报告

- 生成时间: 2026-06-16 05:07:08
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\models\GRU_model_full_gru_v5_plantfix_passive17_plus_all5_seed101.mat`
- 最佳轮次: 48
- 最佳验证损失: 0.430719
- 最佳选择分数: 1.170772
- 主任务基座选择分数: 1.170772
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
| 总损失 | 0.404369 |
| 主工况准确率 | 0.9603 |
| 转弯准确率 | 0.5380 |
| 转弯纯窗口准确率 | 0.5711 |
| 转弯过渡窗口准确率 | 0.3934 |
| 坡度 MAE deg | 0.7158 |
| |theta|<=10 P95 deg | 2.2352 |
| [-10,-8] P95 deg | 1.3146 |
| [8,10] P95 deg | 2.6859 |
| [-2,-0.5] P95 deg | 3.3237 |
| [0.5,2] P95 deg | 3.0085 |
| near-flat abs P95 deg | 2.2389 |
| flat theta bias deg | 0.5988 |
| 主工况置信度均值 | 0.9693 |
| 主工况低置信度(<0.60)比例 | 0.0200 |
| 转弯置信度均值 | 0.6741 |
| 转弯低置信度(<0.60)比例 | 0.4248 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 700 | 2 | 54 | 0.9259 |
| stall | 11 | 61 | 24 | 0.6354 |
| slope | 33 | 19 | 2698 | 0.9811 |

| pred class | precision |
|---|---:|
| flat | 0.9409 |
| stall | 0.7439 |
| slope | 0.9719 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 323 | 326 | 150 | 0.4043 |
| straight | 352 | 1212 | 369 | 0.6270 |
| left | 149 | 318 | 403 | 0.4632 |

| pred class | precision |
|---|---:|
| right | 0.3920 |
| straight | 0.6530 |
| left | 0.4371 |

## 坡度回归范围

- Slope 真值范围: [-9.750, 9.750] deg
- Slope 预测范围: [-10.514, 13.197] deg
- Slope 符号准确率: 0.9595

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 1744 | 0.7804 | 0.8034 | 0.9834 | [0.056, 9.750] | [-1.859, 13.197] |
| downhill | 1762 | 0.7894 | 0.6291 | 0.9359 | [-9.750, -0.235] | [-10.514, 3.286] |

## 置信度分桶

### main

- mean: 0.9693
- error_mean: 0.7587
- low_conf_0p60_ratio: 0.0200
- low_conf_0p70_ratio: 0.0375

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 72 | 0.5278 | 0.5454 |
| [0.60,0.70) | 63 | 0.4921 | 0.6437 |
| [0.70,0.80) | 62 | 0.1774 | 0.7471 |
| [0.80,0.90) | 121 | 0.0992 | 0.8601 |
| [0.90,1.00) | 3284 | 0.0155 | 0.9930 |

### turn

- mean: 0.6741
- error_mean: 0.6154
- low_conf_0p60_ratio: 0.4248
- low_conf_0p70_ratio: 0.5888

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1530 | 0.5797 | 0.5008 |
| [0.60,0.70) | 591 | 0.5093 | 0.6461 |
| [0.70,0.80) | 449 | 0.4722 | 0.7454 |
| [0.80,0.90) | 387 | 0.4289 | 0.8459 |
| [0.90,1.00) | 645 | 0.1519 | 0.9579 |

