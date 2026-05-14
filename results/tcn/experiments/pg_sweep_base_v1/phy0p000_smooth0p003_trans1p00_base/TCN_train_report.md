# TCN 训练报告

- 生成时间: 2026-04-27 10:48:35
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_pg_sweep_base_v1_phy0p000_smooth0p003_trans1p00_base.mat`
- 最佳轮次: 28
- 最佳验证损失: 0.775711
- 最佳选择分数: 0.939142
- 主任务基座选择分数: 0.939142
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_max_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.050, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- Physics-guided loss: lambda_phy=0.000, lambda_smooth=0.003, turn_transition_weight=1.000
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
| 总损失 | 0.862590 |
| 主工况准确率 | 0.7843 |
| 转弯准确率 | 0.8697 |
| 转弯纯窗口准确率 | 0.9010 |
| 转弯过渡窗口准确率 | 0.5610 |
| 坡度 MAE deg | 0.7411 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 214 | 6 | 45 | 0.8075 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 29 | 12 | 121 | 0.7469 |

| pred class | precision |
|---|---:|
| flat | 0.8735 |
| stall | 0.4375 |
| slope | 0.7202 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 63 | 7 | 2 | 0.8750 |
| straight | 15 | 270 | 6 | 0.9278 |
| left | 8 | 20 | 54 | 0.6585 |

| pred class | precision |
|---|---:|
| right | 0.7326 |
| straight | 0.9091 |
| left | 0.8710 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.673, 10.794] deg
- Slope 符号准确率: 0.9815

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.7218 | 0.5599 | 1.0000 | [2.884, 7.500] | [2.698, 10.794] |
| downhill | 29 | 0.8621 | 1.5724 | 0.8966 | [-5.500, -2.298] | [-6.673, 2.529] |
