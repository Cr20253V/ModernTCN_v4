# TCN 训练报告

- 生成时间: 2026-04-26 01:40:25
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\TCN_model_turn_mlp_smoke_tmp.mat`
- 最佳轮次: 1
- 最佳验证损失: 1.072571
- 最佳选择分数: 1.251443
- 选模指标: `turn_priority`
- Head pooling: `last_mean_max_inputstats`
- Turn head: `mlp`, hidden=64
- 损失权重: 转弯=0.200, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.150, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`none`
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 127 steps / 1.270 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 1.056415 |
| 主工况准确率 | 0.5079 |
| 转弯准确率 | 0.7551 |
| 转弯纯窗口准确率 | 0.8069 |
| 转弯过渡窗口准确率 | 0.2439 |
| 坡度 MAE deg | 6.2148 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 113 | 20 | 132 | 0.4264 |
| stall | 2 | 13 | 3 | 0.7222 |
| slope | 54 | 8 | 100 | 0.6173 |

| pred class | precision |
|---|---:|
| flat | 0.6686 |
| stall | 0.3171 |
| slope | 0.4255 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 49 | 15 | 8 | 0.6806 |
| straight | 29 | 229 | 33 | 0.7869 |
| left | 12 | 12 | 58 | 0.7073 |

| pred class | precision |
|---|---:|
| right | 0.5444 |
| straight | 0.8945 |
| left | 0.5859 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-18.642, 10.354] deg
- Slope 符号准确率: 0.5185

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.5639 | 6.5558 | 0.4211 | [2.884, 7.500] | [-15.591, 10.354] |
| downhill | 29 | 0.8621 | 4.6508 | 0.9655 | [-5.500, -2.298] | [-18.642, 0.819] |
