# TCN 训练报告

- 生成时间: 2026-04-30 15:13:39
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_transition_rich_v3_auto_probe_base_comp_flat120_seed42.mat`
- 最佳轮次: 15
- 最佳验证损失: 0.356253
- 最佳选择分数: 0.628731
- 主任务基座选择分数: 0.545465
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_max_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
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
| 总损失 | 0.401096 |
| 主工况准确率 | 0.8150 |
| 转弯准确率 | 0.8305 |
| 转弯纯窗口准确率 | 0.8621 |
| 转弯过渡窗口准确率 | 0.6233 |
| 坡度 MAE deg | 0.4582 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 1152 | 33 | 28 | 0.9497 |
| stall | 8 | 188 | 9 | 0.9171 |
| slope | 185 | 264 | 982 | 0.6862 |

| pred class | precision |
|---|---:|
| flat | 0.8565 |
| stall | 0.3876 |
| slope | 0.9637 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 416 | 97 | 5 | 0.8031 |
| straight | 103 | 1548 | 200 | 0.8363 |
| left | 0 | 78 | 402 | 0.8375 |

| pred class | precision |
|---|---:|
| right | 0.8015 |
| straight | 0.8984 |
| left | 0.6623 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.058, 8.036] deg
- Slope 符号准确率: 1.0000

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 871 | 0.5695 | 0.5023 | 1.0000 | [2.006, 7.500] | [1.026, 8.036] |
| downhill | 560 | 0.8679 | 0.3897 | 1.0000 | [-5.500, -2.046] | [-6.058, -1.140] |
