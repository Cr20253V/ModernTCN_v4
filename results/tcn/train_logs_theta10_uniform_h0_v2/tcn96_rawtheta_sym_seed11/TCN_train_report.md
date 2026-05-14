# TCN 训练报告

- 生成时间: 2026-05-14 12:51:31
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_tcn_theta10_uniform_h0_v2_tcn96_rawtheta_sym_seed11.mat`
- 最佳轮次: 72
- 主任务基座最佳轮次: 55
- 最佳验证损失: 1.009306
- 最佳选择分数: 3.603850
- 主任务基座选择分数: 0.845429
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
- 坡度符号权重: 负坡=1.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=1.000, 正坡=1.000
- 下坡选模惩罚权重: 0.000
- 类别权重策略: main=`sqrt_inverse`, turn=`sqrt_inverse`
- 主工况类别乘子 [flat stall slope]: [1.000 1.000 1.000]
- 转弯类别乘子 [right straight left]: [1.080 1.000 1.080]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.776645 |
| 主工况准确率 | 0.7383 |
| 转弯准确率 | 0.7533 |
| 转弯纯窗口准确率 | 0.7924 |
| 转弯过渡窗口准确率 | 0.5196 |
| 坡度 MAE deg | 0.3181 |
| |theta|<=10 P95 deg | 0.9084 |
| [-10,-8] P95 deg | 0.7526 |
| [8,10] P95 deg | 0.6189 |
| [-2,-0.5] P95 deg | 0.8217 |
| [0.5,2] P95 deg | 1.3984 |
| near-flat abs P95 deg | 1.0758 |
| flat theta bias deg | 0.0972 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 448 | 3 | 306 | 0.5918 |
| stall | 6 | 67 | 44 | 0.5726 |
| slope | 558 | 60 | 2241 | 0.7838 |

| pred class | precision |
|---|---:|
| flat | 0.4427 |
| stall | 0.5154 |
| slope | 0.8649 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 599 | 172 | 42 | 0.7368 |
| straight | 240 | 1662 | 286 | 0.7596 |
| left | 17 | 164 | 551 | 0.7527 |

| pred class | precision |
|---|---:|
| right | 0.6998 |
| straight | 0.8318 |
| left | 0.6268 |

## 坡度回归范围

- Slope 真值范围: [-9.900, 9.500] deg
- Slope 预测范围: [-9.928, 10.847] deg
- Slope 符号准确率: 0.9950

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 1753 | 0.7815 | 0.3428 | 0.9994 | [0.019, 9.500] | [-0.016, 10.847] |
| downhill | 1863 | 0.6318 | 0.2948 | 0.9909 | [-9.900, -0.130] | [-9.928, 1.584] |
