# TCN 训练报告

- 生成时间: 2026-05-02 00:06:15
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_transition_rich_v3_select_stability_flat110_slope100_guard_seed42.mat`
- 最佳轮次: 71
- 主任务基座最佳轮次: 9
- 最佳验证损失: 1.012195
- 最佳选择分数: 8.216005
- 主任务基座选择分数: 0.884444
- 选模指标: `turn_priority`
- Base best metric: `composite_guarded`, combine_base_and_turn_best=1
- Base selection start epoch: 1
- Composite guard floors [flat stall slope]: [0.900 0.900 0.920], weights: [3.000 1.500 4.000]
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
- 主工况类别乘子 [flat stall slope]: [1.100 1.000 1.000]
- 转弯类别乘子 [right straight left]: [1.000 1.100 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.394264 |
| 主工况准确率 | 0.8621 |
| 转弯准确率 | 0.9042 |
| 转弯纯窗口准确率 | 0.9215 |
| 转弯过渡窗口准确率 | 0.7905 |
| 坡度 MAE deg | 0.5700 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 1087 | 41 | 85 | 0.8961 |
| stall | 1 | 193 | 11 | 0.9415 |
| slope | 205 | 50 | 1176 | 0.8218 |

| pred class | precision |
|---|---:|
| flat | 0.8407 |
| stall | 0.6796 |
| slope | 0.9245 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 499 | 19 | 0 | 0.9633 |
| straight | 92 | 1672 | 87 | 0.9033 |
| left | 0 | 75 | 405 | 0.8438 |

| pred class | precision |
|---|---:|
| right | 0.8443 |
| straight | 0.9468 |
| left | 0.8232 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-5.562, 8.690] deg
- Slope 符号准确率: 1.0000

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 871 | 0.8301 | 0.5644 | 1.0000 | [2.006, 7.500] | [0.425, 8.690] |
| downhill | 560 | 0.8089 | 0.5788 | 1.0000 | [-5.500, -2.046] | [-5.562, -0.956] |
