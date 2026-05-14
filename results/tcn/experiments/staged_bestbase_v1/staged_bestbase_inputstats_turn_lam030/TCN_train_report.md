# TCN 训练报告

- 生成时间: 2026-04-26 19:41:03
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_staged_bestbase_v1_staged_bestbase_inputstats_turn_lam030.mat`
- 最佳轮次: 76
- 主任务基座最佳轮次: 58
- 最佳验证损失: 0.866706
- 最佳选择分数: 2.127240
- 主任务基座选择分数: 0.908280
- 选模指标: `turn_priority`
- Base best metric: `composite`, combine_base_and_turn_best=1
- Head pooling: `last_mean_max_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Turn finetune: start_epoch=64, lambda_turn=0.300, disable_other_losses=1
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.100, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`none`
- 转弯类别乘子 [right straight left]: [1.000 1.000 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.871411 |
| 主工况准确率 | 0.8090 |
| 转弯准确率 | 0.9011 |
| 转弯纯窗口准确率 | 0.9257 |
| 转弯过渡窗口准确率 | 0.6585 |
| 坡度 MAE deg | 0.6556 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 222 | 8 | 35 | 0.8377 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 27 | 11 | 124 | 0.7654 |

| pred class | precision |
|---|---:|
| flat | 0.8845 |
| stall | 0.4242 |
| slope | 0.7702 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 64 | 6 | 2 | 0.8889 |
| straight | 10 | 273 | 8 | 0.9381 |
| left | 5 | 13 | 64 | 0.7805 |

| pred class | precision |
|---|---:|
| right | 0.8101 |
| straight | 0.9349 |
| left | 0.8649 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.074, 10.762] deg
- Slope 符号准确率: 0.9877

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.7444 | 0.5282 | 1.0000 | [2.884, 7.500] | [2.613, 10.762] |
| downhill | 29 | 0.8621 | 1.2397 | 0.9310 | [-5.500, -2.298] | [-6.074, 2.413] |
