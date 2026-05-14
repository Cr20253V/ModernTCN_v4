# TCN 训练报告

- 生成时间: 2026-04-30 18:59:38
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_transition_rich_v3_auto_confirm_base_comp_flat120_seed42.mat`
- 最佳轮次: 81
- 主任务基座最佳轮次: 60
- 最佳验证损失: 0.296910
- 最佳选择分数: 0.150030
- 主任务基座选择分数: 0.288420
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
- 主分类 slope 样本权重: 负坡=2.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`sqrt_inverse`, turn=`none`
- 主工况类别乘子 [flat stall slope]: [1.200 1.000 0.950]
- 转弯类别乘子 [right straight left]: [1.000 1.100 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.244085 |
| 主工况准确率 | 0.9365 |
| 转弯准确率 | 0.8982 |
| 转弯纯窗口准确率 | 0.9195 |
| 转弯过渡窗口准确率 | 0.7586 |
| 坡度 MAE deg | 0.3505 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 1113 | 49 | 51 | 0.9176 |
| stall | 0 | 201 | 4 | 0.9805 |
| slope | 46 | 31 | 1354 | 0.9462 |

| pred class | precision |
|---|---:|
| flat | 0.9603 |
| stall | 0.7153 |
| slope | 0.9610 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 494 | 21 | 3 | 0.9537 |
| straight | 94 | 1665 | 92 | 0.8995 |
| left | 0 | 80 | 400 | 0.8333 |

| pred class | precision |
|---|---:|
| right | 0.8401 |
| straight | 0.9428 |
| left | 0.8081 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-5.679, 8.537] deg
- Slope 符号准确率: 1.0000

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 871 | 0.9323 | 0.3693 | 1.0000 | [2.006, 7.500] | [1.189, 8.537] |
| downhill | 560 | 0.9679 | 0.3212 | 1.0000 | [-5.500, -2.046] | [-5.679, -1.213] |
