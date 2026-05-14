# TCN 训练报告

- 生成时间: 2026-04-29 19:09:51
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_transition_rich_v3_main_guard_seed42.mat`
- 最佳轮次: 7
- 最佳验证损失: 0.323765
- 最佳选择分数: 0.728051
- 主任务基座选择分数: 0.728051
- 选模指标: `main_guard`
- Base best metric: `main_guard`, combine_base_and_turn_best=0
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
- 主工况类别乘子 [flat stall slope]: [1.250 1.000 0.900]
- 转弯类别乘子 [right straight left]: [1.000 1.100 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.360714 |
| 主工况准确率 | 0.8617 |
| 转弯准确率 | 0.8315 |
| 转弯纯窗口准确率 | 0.8693 |
| 转弯过渡窗口准确率 | 0.5836 |
| 坡度 MAE deg | 0.9616 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 1056 | 38 | 119 | 0.8706 |
| stall | 0 | 195 | 10 | 0.9512 |
| slope | 196 | 31 | 1204 | 0.8414 |

| pred class | precision |
|---|---:|
| flat | 0.8435 |
| stall | 0.7386 |
| slope | 0.9032 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 415 | 99 | 4 | 0.8012 |
| straight | 138 | 1610 | 103 | 0.8698 |
| left | 1 | 135 | 344 | 0.7167 |

| pred class | precision |
|---|---:|
| right | 0.7491 |
| straight | 0.8731 |
| left | 0.7627 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.089, 9.790] deg
- Slope 符号准确率: 0.9965

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 871 | 0.8553 | 1.0738 | 1.0000 | [2.006, 7.500] | [0.958, 9.790] |
| downhill | 560 | 0.8196 | 0.7872 | 0.9911 | [-5.500, -2.046] | [-6.089, 0.146] |
