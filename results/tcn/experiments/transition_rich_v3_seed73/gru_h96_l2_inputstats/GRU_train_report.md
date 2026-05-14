# GRU 训练报告

- 生成时间: 2026-04-29 03:38:35
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_transition_rich_v3_seed73_h96_l2_inputstats.mat`
- 最佳轮次: 14
- 最佳验证损失: 0.121411
- 最佳选择分数: 0.175612
- 主任务基座选择分数: 0.175612
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
| 总损失 | 0.143292 |
| 主工况准确率 | 0.9459 |
| 转弯准确率 | 0.8852 |
| 转弯纯窗口准确率 | 0.9146 |
| 转弯过渡窗口准确率 | 0.6923 |
| 坡度 MAE deg | 0.3437 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 1110 | 30 | 73 | 0.9151 |
| stall | 0 | 194 | 11 | 0.9463 |
| slope | 24 | 16 | 1391 | 0.9720 |

| pred class | precision |
|---|---:|
| flat | 0.9788 |
| stall | 0.8083 |
| slope | 0.9431 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 449 | 65 | 4 | 0.8668 |
| straight | 94 | 1675 | 82 | 0.9049 |
| left | 0 | 82 | 398 | 0.8292 |

| pred class | precision |
|---|---:|
| right | 0.8269 |
| straight | 0.9193 |
| left | 0.8223 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.112, 8.012] deg
- Slope 符号准确率: 1.0000

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 871 | 0.9598 | 0.3794 | 1.0000 | [2.006, 7.500] | [0.727, 8.012] |
| downhill | 560 | 0.9911 | 0.2882 | 1.0000 | [-5.500, -2.046] | [-6.112, -0.696] |
