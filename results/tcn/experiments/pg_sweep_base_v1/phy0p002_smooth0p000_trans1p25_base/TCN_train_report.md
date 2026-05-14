# TCN 训练报告

- 生成时间: 2026-04-27 11:09:38
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_pg_sweep_base_v1_phy0p002_smooth0p000_trans1p25_base.mat`
- 最佳轮次: 37
- 最佳验证损失: 0.756560
- 最佳选择分数: 0.903532
- 主任务基座选择分数: 0.903532
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_max_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.050, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- Physics-guided loss: lambda_phy=0.002, lambda_smooth=0.000, turn_transition_weight=1.250
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
| 总损失 | 0.864233 |
| 主工况准确率 | 0.7820 |
| 转弯准确率 | 0.8719 |
| 转弯纯窗口准确率 | 0.8985 |
| 转弯过渡窗口准确率 | 0.6098 |
| 坡度 MAE deg | 0.6216 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 211 | 8 | 46 | 0.7962 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 27 | 12 | 123 | 0.7593 |

| pred class | precision |
|---|---:|
| flat | 0.8792 |
| stall | 0.4118 |
| slope | 0.7193 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 64 | 4 | 4 | 0.8889 |
| straight | 16 | 269 | 6 | 0.9244 |
| left | 10 | 17 | 55 | 0.6707 |

| pred class | precision |
|---|---:|
| right | 0.7111 |
| straight | 0.9276 |
| left | 0.8462 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.138, 10.228] deg
- Slope 符号准确率: 0.9877

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.7368 | 0.4837 | 1.0000 | [2.884, 7.500] | [2.930, 10.228] |
| downhill | 29 | 0.8621 | 1.2541 | 0.9310 | [-5.500, -2.298] | [-6.138, 2.370] |
