# GRU 训练报告

- 生成时间: 2026-06-16 03:47:16
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\models\GRU_model_full_gru_v5_plantfix_passive17_plus_all5_seed73.mat`
- 最佳轮次: 51
- 最佳验证损失: 0.445164
- 最佳选择分数: 1.165327
- 主任务基座选择分数: 1.165327
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
| 总损失 | 0.414044 |
| 主工况准确率 | 0.9589 |
| 转弯准确率 | 0.5186 |
| 转弯纯窗口准确率 | 0.5394 |
| 转弯过渡窗口准确率 | 0.4277 |
| 坡度 MAE deg | 1.0090 |
| |theta|<=10 P95 deg | 3.0440 |
| [-10,-8] P95 deg | 1.5906 |
| [8,10] P95 deg | 5.2482 |
| [-2,-0.5] P95 deg | 2.8358 |
| [0.5,2] P95 deg | 4.0492 |
| near-flat abs P95 deg | 2.9081 |
| flat theta bias deg | -0.4946 |
| 主工况置信度均值 | 0.9627 |
| 主工况低置信度(<0.60)比例 | 0.0292 |
| 转弯置信度均值 | 0.6579 |
| 转弯低置信度(<0.60)比例 | 0.4634 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 708 | 3 | 45 | 0.9365 |
| stall | 10 | 65 | 21 | 0.6771 |
| slope | 37 | 32 | 2681 | 0.9749 |

| pred class | precision |
|---|---:|
| flat | 0.9377 |
| stall | 0.6500 |
| slope | 0.9760 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 357 | 313 | 129 | 0.4468 |
| straight | 393 | 1057 | 483 | 0.5468 |
| left | 182 | 234 | 454 | 0.5218 |

| pred class | precision |
|---|---:|
| right | 0.3830 |
| straight | 0.6590 |
| left | 0.4259 |

## 坡度回归范围

- Slope 真值范围: [-9.750, 9.750] deg
- Slope 预测范围: [-10.771, 13.137] deg
- Slope 符号准确率: 0.9412

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 1744 | 0.7557 | 1.2278 | 0.9083 | [0.056, 9.750] | [-4.455, 13.137] |
| downhill | 1762 | 0.7991 | 0.7925 | 0.9739 | [-9.750, -0.235] | [-10.771, 2.749] |

## 置信度分桶

### main

- mean: 0.9627
- error_mean: 0.7725
- low_conf_0p60_ratio: 0.0292
- low_conf_0p70_ratio: 0.0478

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 105 | 0.3810 | 0.5433 |
| [0.60,0.70) | 67 | 0.3284 | 0.6447 |
| [0.70,0.80) | 55 | 0.3091 | 0.7544 |
| [0.80,0.90) | 129 | 0.1085 | 0.8572 |
| [0.90,1.00) | 3246 | 0.0169 | 0.9906 |

### turn

- mean: 0.6579
- error_mean: 0.6056
- low_conf_0p60_ratio: 0.4634
- low_conf_0p70_ratio: 0.6416

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1669 | 0.5752 | 0.4988 |
| [0.60,0.70) | 642 | 0.5249 | 0.6446 |
| [0.70,0.80) | 403 | 0.4963 | 0.7486 |
| [0.80,0.90) | 302 | 0.5166 | 0.8440 |
| [0.90,1.00) | 586 | 0.1382 | 0.9672 |

