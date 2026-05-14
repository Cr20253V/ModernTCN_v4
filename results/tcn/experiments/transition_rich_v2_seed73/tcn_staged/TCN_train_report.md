# TCN 训练报告

- 生成时间: 2026-04-28 18:46:27
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v2_transition_rich.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_transition_rich_v2_seed73_staged.mat`
- 最佳轮次: 65
- 主任务基座最佳轮次: 54
- 最佳验证损失: 0.503412
- 最佳选择分数: 1.009727
- 主任务基座选择分数: 0.356443
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
| 总损失 | 0.165634 |
| 主工况准确率 | 0.9246 |
| 转弯准确率 | 0.9060 |
| 转弯纯窗口准确率 | 0.9233 |
| 转弯过渡窗口准确率 | 0.7851 |
| 坡度 MAE deg | 0.4763 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 536 | 9 | 28 | 0.9354 |
| stall | 0 | 76 | 2 | 0.9744 |
| slope | 1 | 33 | 283 | 0.8927 |

| pred class | precision |
|---|---:|
| flat | 0.9981 |
| stall | 0.6441 |
| slope | 0.9042 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 109 | 6 | 0 | 0.9478 |
| straight | 18 | 658 | 25 | 0.9387 |
| left | 4 | 38 | 110 | 0.7237 |

| pred class | precision |
|---|---:|
| right | 0.8321 |
| straight | 0.9373 |
| left | 0.8148 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 6.000] deg
- Slope 预测范围: [-5.876, 8.327] deg
- Slope 符号准确率: 0.9968

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 223 | 0.8655 | 0.5224 | 1.0000 | [2.014, 6.000] | [1.611, 8.327] |
| downhill | 94 | 0.9574 | 0.3670 | 0.9894 | [-5.500, -2.074] | [-5.876, 1.359] |
