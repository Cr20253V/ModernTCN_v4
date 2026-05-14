# TCN 训练报告

- 生成时间: 2026-04-28 12:56:00
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_main_confirm_v1_staged_seed21.mat`
- 最佳轮次: 64
- 主任务基座最佳轮次: 58
- 最佳验证损失: 0.811237
- 最佳选择分数: 0.593104
- 主任务基座选择分数: 0.610426
- 选模指标: `turn_priority`
- Base best metric: `composite`, combine_base_and_turn_best=1
- Head pooling: `last_mean_max_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Turn finetune: start_epoch=64, lambda_turn=0.500, disable_other_losses=1
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.050, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- Physics-guided loss: lambda_phy=0.000, lambda_smooth=0.000, turn_transition_weight=1.000
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
| 总损失 | 0.765858 |
| 主工况准确率 | 0.9371 |
| 转弯准确率 | 0.8764 |
| 转弯纯窗口准确率 | 0.9035 |
| 转弯过渡窗口准确率 | 0.6098 |
| 坡度 MAE deg | 0.7319 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 257 | 2 | 6 | 0.9698 |
| stall | 3 | 13 | 2 | 0.7222 |
| slope | 4 | 11 | 147 | 0.9074 |

| pred class | precision |
|---|---:|
| flat | 0.9735 |
| stall | 0.5000 |
| slope | 0.9484 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 63 | 7 | 2 | 0.8750 |
| straight | 15 | 267 | 9 | 0.9175 |
| left | 9 | 13 | 60 | 0.7317 |

| pred class | precision |
|---|---:|
| right | 0.7241 |
| straight | 0.9303 |
| left | 0.8451 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.051, 10.986] deg
- Slope 符号准确率: 0.9877

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9248 | 0.6014 | 1.0000 | [2.884, 7.500] | [2.510, 10.986] |
| downhill | 29 | 0.8276 | 1.3302 | 0.9310 | [-5.500, -2.298] | [-6.051, 3.421] |
