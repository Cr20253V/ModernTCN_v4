# TCN 训练报告

- 生成时间: 2026-05-14 15:17:42
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_tcn_theta10_uniform_h0_v2_tcn96_rawtheta_sym_seed21.mat`
- 最佳轮次: 98
- 主任务基座最佳轮次: 60
- 最佳验证损失: 1.048860
- 最佳选择分数: 3.685266
- 主任务基座选择分数: 0.832593
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
| 总损失 | 0.777691 |
| 主工况准确率 | 0.7479 |
| 转弯准确率 | 0.7771 |
| 转弯纯窗口准确率 | 0.8127 |
| 转弯过渡窗口准确率 | 0.5645 |
| 坡度 MAE deg | 0.2902 |
| |theta|<=10 P95 deg | 0.8473 |
| [-10,-8] P95 deg | 0.8262 |
| [8,10] P95 deg | 0.5090 |
| [-2,-0.5] P95 deg | 0.7838 |
| [0.5,2] P95 deg | 1.6262 |
| near-flat abs P95 deg | 1.2314 |
| flat theta bias deg | 0.2003 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 409 | 2 | 346 | 0.5403 |
| stall | 4 | 65 | 48 | 0.5556 |
| slope | 478 | 63 | 2318 | 0.8108 |

| pred class | precision |
|---|---:|
| flat | 0.4590 |
| stall | 0.5000 |
| slope | 0.8547 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 605 | 160 | 48 | 0.7442 |
| straight | 251 | 1721 | 216 | 0.7866 |
| left | 18 | 139 | 575 | 0.7855 |

| pred class | precision |
|---|---:|
| right | 0.6922 |
| straight | 0.8520 |
| left | 0.6853 |

## 坡度回归范围

- Slope 真值范围: [-9.900, 9.500] deg
- Slope 预测范围: [-10.835, 10.494] deg
- Slope 符号准确率: 0.9925

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 1753 | 0.8163 | 0.2914 | 0.9994 | [0.019, 9.500] | [-0.010, 10.494] |
| downhill | 1863 | 0.6618 | 0.2891 | 0.9860 | [-9.900, -0.130] | [-10.835, 1.554] |
