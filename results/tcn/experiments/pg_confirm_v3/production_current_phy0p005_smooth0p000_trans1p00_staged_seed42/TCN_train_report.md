# TCN 训练报告

- 生成时间: 2026-04-28 01:21:48
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_pg_confirm_v3_production_current_phy0p005_smooth0p000_trans1p00_staged_seed42.mat`
- 最佳轮次: 67
- 主任务基座最佳轮次: 62
- 最佳验证损失: 0.901248
- 最佳选择分数: 2.146799
- 主任务基座选择分数: 0.876210
- 选模指标: `turn_priority`
- Base best metric: `composite`, combine_base_and_turn_best=1
- Head pooling: `last_mean_max_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Turn finetune: start_epoch=64, lambda_turn=0.500, disable_other_losses=1
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.050, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- Physics-guided loss: lambda_phy=0.005, lambda_smooth=0.000, turn_transition_weight=1.000
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
| 总损失 | 0.864423 |
| 主工况准确率 | 0.8112 |
| 转弯准确率 | 0.8944 |
| 转弯纯窗口准确率 | 0.9233 |
| 转弯过渡窗口准确率 | 0.6098 |
| 坡度 MAE deg | 0.8250 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 223 | 8 | 34 | 0.8415 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 28 | 10 | 124 | 0.7654 |

| pred class | precision |
|---|---:|
| flat | 0.8814 |
| stall | 0.4375 |
| slope | 0.7750 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 63 | 5 | 4 | 0.8750 |
| straight | 11 | 272 | 8 | 0.9347 |
| left | 6 | 13 | 63 | 0.7683 |

| pred class | precision |
|---|---:|
| right | 0.7875 |
| straight | 0.9379 |
| left | 0.8400 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.126, 11.041] deg
- Slope 符号准确率: 0.9815

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.7444 | 0.6815 | 1.0000 | [2.884, 7.500] | [2.285, 11.041] |
| downhill | 29 | 0.8621 | 1.4828 | 0.8966 | [-5.500, -2.298] | [-6.126, 2.886] |
