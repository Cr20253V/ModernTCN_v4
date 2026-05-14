# GRU 训练报告

- 生成时间: 2026-04-28 12:58:58
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_main_confirm_v1_h96_l2_inputstats_seed21.mat`
- 最佳轮次: 14
- 最佳验证损失: 0.533293
- 最佳选择分数: 0.630367
- 主任务基座选择分数: 0.630367
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
| 总损失 | 0.663747 |
| 主工况准确率 | 0.9461 |
| 转弯准确率 | 0.8472 |
| 转弯纯窗口准确率 | 0.8861 |
| 转弯过渡窗口准确率 | 0.4634 |
| 坡度 MAE deg | 0.7536 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 253 | 6 | 6 | 0.9547 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 1 | 7 | 154 | 0.9506 |

| pred class | precision |
|---|---:|
| flat | 0.9883 |
| stall | 0.5185 |
| slope | 0.9506 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 60 | 7 | 5 | 0.8333 |
| straight | 15 | 265 | 11 | 0.9107 |
| left | 5 | 25 | 52 | 0.6341 |

| pred class | precision |
|---|---:|
| right | 0.7500 |
| straight | 0.8923 |
| left | 0.7647 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-5.562, 9.261] deg
- Slope 符号准确率: 0.9815

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9699 | 0.6284 | 0.9925 | [2.884, 7.500] | [-0.007, 9.261] |
| downhill | 29 | 0.8621 | 1.3278 | 0.9310 | [-5.500, -2.298] | [-5.562, 1.202] |
