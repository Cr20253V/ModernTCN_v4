# TCN 训练报告

- 生成时间: 2026-04-30 14:47:51
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_transition_rich_v3_auto_probe_base_comp_t060_seed42.mat`
- 最佳轮次: 15
- 最佳验证损失: 0.332695
- 最佳选择分数: 0.655922
- 主任务基座选择分数: 0.599961
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
- 主工况类别乘子 [flat stall slope]: [1.150 1.000 0.950]
- 转弯类别乘子 [right straight left]: [1.000 1.100 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.366363 |
| 主工况准确率 | 0.8413 |
| 转弯准确率 | 0.8301 |
| 转弯纯窗口准确率 | 0.8621 |
| 转弯过渡窗口准确率 | 0.6207 |
| 坡度 MAE deg | 0.5446 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 1125 | 38 | 50 | 0.9275 |
| stall | 3 | 192 | 10 | 0.9366 |
| slope | 167 | 184 | 1080 | 0.7547 |

| pred class | precision |
|---|---:|
| flat | 0.8687 |
| stall | 0.4638 |
| slope | 0.9474 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 421 | 92 | 5 | 0.8127 |
| straight | 110 | 1549 | 192 | 0.8368 |
| left | 0 | 85 | 395 | 0.8229 |

| pred class | precision |
|---|---:|
| right | 0.7928 |
| straight | 0.8975 |
| left | 0.6672 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-5.739, 8.571] deg
- Slope 符号准确率: 0.9993

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 871 | 0.6854 | 0.5327 | 1.0000 | [2.006, 7.500] | [0.982, 8.571] |
| downhill | 560 | 0.8625 | 0.5632 | 0.9982 | [-5.500, -2.046] | [-5.739, 0.067] |
