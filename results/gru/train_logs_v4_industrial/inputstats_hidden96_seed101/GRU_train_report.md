# GRU 训练报告

- 生成时间: 2026-05-06 12:38:27
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_v4_industrial_inputstats_hidden96_seed101.mat`
- 最佳轮次: 59
- 最佳验证损失: 0.074621
- 最佳选择分数: 0.114219
- 主任务基座选择分数: 0.114219
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
| 总损失 | 0.093415 |
| 主工况准确率 | 0.9709 |
| 转弯准确率 | 0.9447 |
| 转弯纯窗口准确率 | 0.9774 |
| 转弯过渡窗口准确率 | 0.7295 |
| 坡度 MAE deg | 0.3278 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 7647 | 42 | 228 | 0.9659 |
| stall | 9 | 1190 | 18 | 0.9778 |
| slope | 52 | 47 | 4363 | 0.9778 |

| pred class | precision |
|---|---:|
| flat | 0.9921 |
| stall | 0.9304 |
| slope | 0.9466 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 2107 | 133 | 21 | 0.9319 |
| straight | 241 | 8806 | 177 | 0.9547 |
| left | 7 | 173 | 1931 | 0.9147 |

| pred class | precision |
|---|---:|
| right | 0.8947 |
| straight | 0.9664 |
| left | 0.9070 |

## 坡度回归范围

- Slope 真值范围: [-8.000, 7.000] deg
- Slope 预测范围: [-8.321, 10.057] deg
- Slope 符号准确率: 0.9969

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 2150 | 0.9763 | 0.3610 | 1.0000 | [2.000, 7.000] | [0.814, 10.057] |
| downhill | 2312 | 0.9792 | 0.2969 | 0.9939 | [-8.000, -2.000] | [-8.321, 2.387] |
