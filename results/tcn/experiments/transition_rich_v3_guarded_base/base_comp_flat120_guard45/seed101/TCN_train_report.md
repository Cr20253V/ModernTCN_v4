# TCN 训练报告

- 生成时间: 2026-05-01 18:06:35
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_transition_rich_v3_guarded_base_comp_flat120_seed101.mat`
- 最佳轮次: 70
- 主任务基座最佳轮次: 50
- 最佳验证损失: 0.867256
- 最佳选择分数: 7.884740
- 主任务基座选择分数: 1.075100
- 选模指标: `turn_priority`
- Base best metric: `composite`, combine_base_and_turn_best=1
- Base selection start epoch: 45
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
- 主工况类别乘子 [flat stall slope]: [1.200 1.000 0.950]
- 转弯类别乘子 [right straight left]: [1.000 1.100 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.756845 |
| 主工况准确率 | 0.6922 |
| 转弯准确率 | 0.9052 |
| 转弯纯窗口准确率 | 0.9227 |
| 转弯过渡窗口准确率 | 0.7905 |
| 坡度 MAE deg | 0.4237 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 1173 | 25 | 15 | 0.9670 |
| stall | 14 | 189 | 2 | 0.9220 |
| slope | 537 | 284 | 610 | 0.4263 |

| pred class | precision |
|---|---:|
| flat | 0.6804 |
| stall | 0.3795 |
| slope | 0.9729 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 500 | 18 | 0 | 0.9653 |
| straight | 98 | 1672 | 81 | 0.9033 |
| left | 0 | 73 | 407 | 0.8479 |

| pred class | precision |
|---|---:|
| right | 0.8361 |
| straight | 0.9484 |
| left | 0.8340 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-5.846, 8.380] deg
- Slope 符号准确率: 1.0000

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 871 | 0.2411 | 0.4259 | 1.0000 | [2.006, 7.500] | [1.180, 8.380] |
| downhill | 560 | 0.7143 | 0.4202 | 1.0000 | [-5.500, -2.046] | [-5.846, -1.134] |
