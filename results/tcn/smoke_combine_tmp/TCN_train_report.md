# TCN 训练报告

- 生成时间: 2026-04-26 10:47:10
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_combine_smoke_tmp.mat`
- 最佳轮次: 2
- 主任务基座最佳轮次: 1
- 最佳验证损失: 1.417508
- 最佳选择分数: 8.956050
- 主任务基座选择分数: 1.637991
- 选模指标: `turn_priority`
- Base best metric: `composite`, combine_base_and_turn_best=1
- Head pooling: `last_mean_max_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Turn finetune: start_epoch=2, lambda_turn=0.600, disable_other_losses=1
- Gradient clip: `separate`, threshold=5.000
- 损失权重: 转弯=0.150, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=2.000, 正坡=1.000
- 下坡选模惩罚权重: 0.150
- 类别权重策略: main=`balanced`, turn=`none`
- 转弯类别乘子 [right straight left]: [1.000 1.200 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 1.040019 |
| 主工况准确率 | 0.6539 |
| 转弯准确率 | 0.7910 |
| 转弯纯窗口准确率 | 0.8292 |
| 转弯过渡窗口准确率 | 0.4146 |
| 坡度 MAE deg | 5.8416 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 206 | 29 | 30 | 0.7774 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 75 | 16 | 71 | 0.4383 |

| pred class | precision |
|---|---:|
| flat | 0.7279 |
| stall | 0.2373 |
| slope | 0.6893 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 54 | 14 | 4 | 0.7500 |
| straight | 23 | 256 | 12 | 0.8797 |
| left | 10 | 30 | 42 | 0.5122 |

| pred class | precision |
|---|---:|
| right | 0.6207 |
| straight | 0.8533 |
| left | 0.7241 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-14.460, 8.450] deg
- Slope 符号准确率: 0.4938

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.5113 | 6.1999 | 0.3835 | [2.884, 7.500] | [-8.847, 8.450] |
| downhill | 29 | 0.1034 | 4.1986 | 1.0000 | [-5.500, -2.298] | [-14.460, -5.147] |
