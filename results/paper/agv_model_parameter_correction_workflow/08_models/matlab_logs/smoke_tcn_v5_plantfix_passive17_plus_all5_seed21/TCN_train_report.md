# TCN 训练报告

- 生成时间: 2026-06-15 23:22:34
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\models\TCN_model_smoke_tcn_v5_plantfix_passive17_plus_all5_seed21.mat`
- 最佳轮次: 20
- 主任务基座最佳轮次: 13
- 最佳验证损失: 0.559792
- 最佳选择分数: 4.027163
- 主任务基座选择分数: 0.878637
- 选模指标: `turn_priority`
- Base best metric: `composite`, combine_base_and_turn_best=1
- Base selection start epoch: 10
- Composite guard floors [flat stall slope]: [0.900 0.900 0.900], weights: [3.000 1.500 3.000]
- Head pooling: `last_mean_max_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Turn finetune: start_epoch=64, lambda_turn=0.500, disable_other_losses=1
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.080, 坡度=0.550, 平地坡度约束=0.120, 辅助=0.000, pitch一致性=0.000
- 平地坡度约束模式: `near_zero`, near-zero tol=0.300 deg
- Physics-guided loss: lambda_phy=0.000, lambda_smooth=0.000, turn_transition_weight=1.250
- Physics thresholds: pitch=1.000 deg, turn_signal=0.0100, turn_gyro_weight=0.250, theta_mag_weight=0.250
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`sqrt_inverse`, turn=`sqrt_inverse`
- 主工况类别乘子 [flat stall slope]: [1.000 1.000 1.000]
- 转弯类别乘子 [right straight left]: [1.080 1.000 1.080]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.574023 |
| 主工况准确率 | 0.7102 |
| 转弯准确率 | 0.4989 |
| 转弯纯窗口准确率 | 0.5343 |
| 转弯过渡窗口准确率 | 0.3443 |
| 坡度 MAE deg | 0.9028 |
| |theta|<=10 P95 deg | 2.5975 |
| [-10,-8] P95 deg | 1.8414 |
| [8,10] P95 deg | 2.8189 |
| [-2,-0.5] P95 deg | 2.1051 |
| [0.5,2] P95 deg | 2.2533 |
| near-flat abs P95 deg | 2.2456 |
| flat theta bias deg | 0.2835 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 99 | 1 | 656 | 0.1310 |
| stall | 17 | 46 | 33 | 0.4792 |
| slope | 238 | 99 | 2413 | 0.8775 |

| pred class | precision |
|---|---:|
| flat | 0.2797 |
| stall | 0.3151 |
| slope | 0.7779 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 325 | 333 | 141 | 0.4068 |
| straight | 407 | 1097 | 429 | 0.5675 |
| left | 193 | 302 | 375 | 0.4310 |

| pred class | precision |
|---|---:|
| right | 0.3514 |
| straight | 0.6334 |
| left | 0.3968 |

## 坡度回归范围

- Slope 真值范围: [-9.750, 9.750] deg
- Slope 预测范围: [-11.104, 17.490] deg
- Slope 符号准确率: 0.9564

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 1744 | 0.7701 | 1.0075 | 0.9725 | [0.056, 9.750] | [-2.845, 17.490] |
| downhill | 1762 | 0.9796 | 0.7992 | 0.9404 | [-9.750, -0.235] | [-11.104, 2.908] |
