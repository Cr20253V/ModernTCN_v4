# TCN 训练报告

- 生成时间: 2026-04-29 22:26:07
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_transition_rich_v3_sqrt_theta045_seed42.mat`
- 最佳轮次: 76
- 主任务基座最佳轮次: 7
- 最佳验证损失: 0.962329
- 最佳选择分数: 9.293891
- 主任务基座选择分数: 0.609869
- 选模指标: `turn_priority`
- Base best metric: `main_guard`, combine_base_and_turn_best=1
- Head pooling: `last_mean_max_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Turn finetune: start_epoch=64, lambda_turn=0.500, disable_other_losses=1
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.050, 坡度=0.450, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- Physics-guided loss: lambda_phy=0.000, lambda_smooth=0.000, turn_transition_weight=1.000
- Physics thresholds: pitch=1.000 deg, turn_signal=0.0100, turn_gyro_weight=0.250, theta_mag_weight=0.250
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=2.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`sqrt_inverse`, turn=`none`
- 主工况类别乘子 [flat stall slope]: [1.150 1.000 0.950]
- 转弯类别乘子 [right straight left]: [1.000 1.100 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.379626 |
| 主工况准确率 | 0.8592 |
| 转弯准确率 | 0.9017 |
| 转弯纯窗口准确率 | 0.9211 |
| 转弯过渡窗口准确率 | 0.7745 |
| 坡度 MAE deg | 0.9467 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 1064 | 33 | 116 | 0.8772 |
| stall | 1 | 192 | 12 | 0.9366 |
| slope | 195 | 44 | 1192 | 0.8330 |

| pred class | precision |
|---|---:|
| flat | 0.8444 |
| stall | 0.7138 |
| slope | 0.9030 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 492 | 23 | 3 | 0.9498 |
| straight | 87 | 1672 | 92 | 0.9033 |
| left | 0 | 75 | 405 | 0.8438 |

| pred class | precision |
|---|---:|
| right | 0.8497 |
| straight | 0.9446 |
| left | 0.8100 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-5.992, 10.267] deg
- Slope 符号准确率: 0.9832

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 871 | 0.8370 | 0.8370 | 1.0000 | [2.006, 7.500] | [1.428, 10.267] |
| downhill | 560 | 0.8268 | 1.1173 | 0.9571 | [-5.500, -2.046] | [-5.992, 1.265] |
