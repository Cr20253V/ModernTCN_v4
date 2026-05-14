# GRU 训练报告

- 生成时间: 2026-05-05 23:57:26
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_v4_industrial_inputstats_hidden96_seed42.mat`
- 最佳轮次: 52
- 最佳验证损失: 0.070690
- 最佳选择分数: 0.109558
- 主任务基座选择分数: 0.109558
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.080, 坡度=0.350, 平地坡度约束=0.250, 辅助=0.000, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`none`
- 转弯类别乘子 [right straight left]: [1.150 1.000 1.150]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 128 steps / 1.280 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.096218 |
| 主工况准确率 | 0.9694 |
| 转弯准确率 | 0.9430 |
| 转弯纯窗口准确率 | 0.9759 |
| 转弯过渡窗口准确率 | 0.7262 |
| 坡度 MAE deg | 0.3323 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 7625 | 45 | 247 | 0.9631 |
| stall | 9 | 1193 | 15 | 0.9803 |
| slope | 49 | 51 | 4362 | 0.9776 |

| pred class | precision |
|---|---:|
| flat | 0.9925 |
| stall | 0.9255 |
| slope | 0.9433 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 2105 | 134 | 22 | 0.9310 |
| straight | 252 | 8782 | 190 | 0.9521 |
| left | 6 | 171 | 1934 | 0.9162 |

| pred class | precision |
|---|---:|
| right | 0.8908 |
| straight | 0.9664 |
| left | 0.9012 |

## 坡度回归范围

- Slope 真值范围: [-8.000, 7.000] deg
- Slope 预测范围: [-8.237, 9.467] deg
- Slope 符号准确率: 0.9978

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 2150 | 0.9749 | 0.3691 | 1.0000 | [2.000, 7.000] | [0.098, 9.467] |
| downhill | 2312 | 0.9801 | 0.2981 | 0.9957 | [-8.000, -2.000] | [-8.237, 1.568] |
