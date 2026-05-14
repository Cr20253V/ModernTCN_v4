# TCN 训练报告

- 生成时间: 2026-04-27 13:10:11
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_pg_sweep_base_v1_phy0p020_smooth0p000_trans1p00_base.mat`
- 最佳轮次: 47
- 最佳验证损失: 0.761509
- 最佳选择分数: 0.917309
- 主任务基座选择分数: 0.917309
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_max_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.050, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- Physics-guided loss: lambda_phy=0.020, lambda_smooth=0.000, turn_transition_weight=1.000
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
| 总损失 | 0.878061 |
| 主工况准确率 | 0.7933 |
| 转弯准确率 | 0.8180 |
| 转弯纯窗口准确率 | 0.8490 |
| 转弯过渡窗口准确率 | 0.5122 |
| 坡度 MAE deg | 0.6873 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 216 | 8 | 41 | 0.8151 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 27 | 12 | 123 | 0.7593 |

| pred class | precision |
|---|---:|
| flat | 0.8816 |
| stall | 0.4118 |
| slope | 0.7410 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 61 | 1 | 10 | 0.8472 |
| straight | 26 | 238 | 27 | 0.8179 |
| left | 14 | 3 | 65 | 0.7927 |

| pred class | precision |
|---|---:|
| right | 0.6040 |
| straight | 0.9835 |
| left | 0.6373 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.050, 10.546] deg
- Slope 符号准确率: 0.9877

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.7368 | 0.5594 | 1.0000 | [2.884, 7.500] | [2.829, 10.546] |
| downhill | 29 | 0.8621 | 1.2738 | 0.9310 | [-5.500, -2.298] | [-6.050, 2.599] |
