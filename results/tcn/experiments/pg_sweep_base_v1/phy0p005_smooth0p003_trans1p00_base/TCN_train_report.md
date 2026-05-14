# TCN 训练报告

- 生成时间: 2026-04-27 12:12:49
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_pg_sweep_base_v1_phy0p005_smooth0p003_trans1p00_base.mat`
- 最佳轮次: 37
- 最佳验证损失: 0.755050
- 最佳选择分数: 0.921312
- 主任务基座选择分数: 0.921312
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_max_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.050, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- Physics-guided loss: lambda_phy=0.005, lambda_smooth=0.003, turn_transition_weight=1.000
- Physics thresholds: pitch=1.000 deg, turn_signal=0.0100, turn_gyro_weight=0.250, theta_mag_weight=0.250
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`none`
- 转弯类别乘子 [right straight left]: [1.000 1.100 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.863904 |
| 主工况准确率 | 0.7843 |
| 转弯准确率 | 0.8607 |
| 转弯纯窗口准确率 | 0.8911 |
| 转弯过渡窗口准确率 | 0.5610 |
| 坡度 MAE deg | 1.2924 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 211 | 8 | 46 | 0.7962 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 26 | 12 | 124 | 0.7654 |

| pred class | precision |
|---|---:|
| flat | 0.8828 |
| stall | 0.4118 |
| slope | 0.7209 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 62 | 3 | 7 | 0.8611 |
| straight | 17 | 264 | 10 | 0.9072 |
| left | 13 | 12 | 57 | 0.6951 |

| pred class | precision |
|---|---:|
| right | 0.6739 |
| straight | 0.9462 |
| left | 0.7703 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-7.460, 10.370] deg
- Slope 符号准确率: 0.9815

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.7444 | 1.1416 | 1.0000 | [2.884, 7.500] | [1.467, 10.370] |
| downhill | 29 | 0.8621 | 1.9838 | 0.8966 | [-5.500, -2.298] | [-7.460, 3.314] |
