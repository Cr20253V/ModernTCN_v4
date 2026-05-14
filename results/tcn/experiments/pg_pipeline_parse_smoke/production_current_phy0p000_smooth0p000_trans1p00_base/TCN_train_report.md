# TCN 训练报告

- 生成时间: 2026-04-27 15:09:45
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_pg_pipeline_parse_smoke_production_current_phy0p000_smooth0p000_trans1p00_base.mat`
- 最佳轮次: 1
- 最佳验证损失: 1.002002
- 最佳选择分数: 1.356549
- 主任务基座选择分数: 1.356549
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_max_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
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
| 总损失 | 0.984140 |
| 主工况准确率 | 0.5079 |
| 转弯准确率 | 0.6899 |
| 转弯纯窗口准确率 | 0.7327 |
| 转弯过渡窗口准确率 | 0.2683 |
| 坡度 MAE deg | 3.7039 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 116 | 24 | 125 | 0.4377 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 50 | 16 | 96 | 0.5926 |

| pred class | precision |
|---|---:|
| flat | 0.6905 |
| stall | 0.2593 |
| slope | 0.4305 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 51 | 15 | 6 | 0.7083 |
| straight | 43 | 211 | 37 | 0.7251 |
| left | 11 | 26 | 45 | 0.5488 |

| pred class | precision |
|---|---:|
| right | 0.4857 |
| straight | 0.8373 |
| left | 0.5114 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-11.960, 13.976] deg
- Slope 符号准确率: 0.7407

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.5414 | 3.9930 | 0.6917 | [2.884, 7.500] | [-9.681, 13.976] |
| downhill | 29 | 0.8276 | 2.3781 | 0.9655 | [-5.500, -2.298] | [-11.960, 0.556] |
