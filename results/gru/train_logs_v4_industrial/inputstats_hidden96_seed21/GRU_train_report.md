# GRU 训练报告

- 生成时间: 2026-05-05 20:46:45
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_v4_industrial_inputstats_hidden96_seed21.mat`
- 最佳轮次: 56
- 最佳验证损失: 0.073923
- 最佳选择分数: 0.113448
- 主任务基座选择分数: 0.113448
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
| 总损失 | 0.092816 |
| 主工况准确率 | 0.9695 |
| 转弯准确率 | 0.9433 |
| 转弯纯窗口准确率 | 0.9751 |
| 转弯过渡窗口准确率 | 0.7340 |
| 坡度 MAE deg | 0.3350 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 7645 | 41 | 231 | 0.9656 |
| stall | 7 | 1183 | 27 | 0.9721 |
| slope | 45 | 63 | 4354 | 0.9758 |

| pred class | precision |
|---|---:|
| flat | 0.9932 |
| stall | 0.9192 |
| slope | 0.9441 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 2106 | 129 | 26 | 0.9314 |
| straight | 239 | 8815 | 170 | 0.9557 |
| left | 8 | 199 | 1904 | 0.9019 |

| pred class | precision |
|---|---:|
| right | 0.8950 |
| straight | 0.9641 |
| left | 0.9067 |

## 坡度回归范围

- Slope 真值范围: [-8.000, 7.000] deg
- Slope 预测范围: [-8.634, 9.732] deg
- Slope 符号准确率: 0.9982

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 2150 | 0.9721 | 0.3711 | 1.0000 | [2.000, 7.000] | [1.112, 9.732] |
| downhill | 2312 | 0.9792 | 0.3015 | 0.9965 | [-8.000, -2.000] | [-8.634, 2.289] |
