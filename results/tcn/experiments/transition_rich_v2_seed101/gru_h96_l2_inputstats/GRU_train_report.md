# GRU 训练报告

- 生成时间: 2026-04-28 19:36:00
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v2_transition_rich.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_transition_rich_v2_seed101_h96_l2_inputstats.mat`
- 最佳轮次: 49
- 最佳验证损失: 0.159395
- 最佳选择分数: 0.219491
- 主任务基座选择分数: 0.219491
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean_inputstats`
- Turn head: `mlp`, source=`inputstats`, hidden=64
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.050, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.000, pitch一致性=0.000
- 坡度符号权重: 负坡=2.000, 正坡=1.000
- 主分类 slope 样本权重: 负坡=4.000, 正坡=1.000
- 下坡选模惩罚权重: 0.250
- 类别权重策略: main=`balanced`, turn=`none`
- 转弯类别乘子 [right straight left]: [1.000 1.100 1.000]
- Focal loss: enable=0, gamma_main=1.000, gamma_turn=0.500
- 感受野: 128 steps / 1.280 s

## 测试指标

| 指标 | 数值 |
|---|---:|
| 总损失 | 0.131715 |
| 主工况准确率 | 0.9442 |
| 转弯准确率 | 0.8915 |
| 转弯纯窗口准确率 | 0.9197 |
| 转弯过渡窗口准确率 | 0.6942 |
| 坡度 MAE deg | 0.3296 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 542 | 5 | 26 | 0.9459 |
| stall | 0 | 77 | 1 | 0.9872 |
| slope | 3 | 19 | 295 | 0.9306 |

| pred class | precision |
|---|---:|
| flat | 0.9945 |
| stall | 0.7624 |
| slope | 0.9161 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 111 | 4 | 0 | 0.9652 |
| straight | 17 | 651 | 33 | 0.9287 |
| left | 7 | 44 | 101 | 0.6645 |

| pred class | precision |
|---|---:|
| right | 0.8222 |
| straight | 0.9313 |
| left | 0.7537 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 6.000] deg
- Slope 预测范围: [-6.232, 8.368] deg
- Slope 符号准确率: 0.9968

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 223 | 0.9193 | 0.3026 | 1.0000 | [2.014, 6.000] | [1.784, 8.368] |
| downhill | 94 | 0.9574 | 0.3934 | 0.9894 | [-5.500, -2.074] | [-6.232, 0.589] |
