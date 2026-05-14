# GRU 训练报告

- 生成时间: 2026-05-05 17:37:16
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_v4_industrial_inputstats_hidden96_seed11.mat`
- 最佳轮次: 28
- 最佳验证损失: 0.072321
- 最佳选择分数: 0.117584
- 主任务基座选择分数: 0.117584
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
| 总损失 | 0.108889 |
| 主工况准确率 | 0.9633 |
| 转弯准确率 | 0.9389 |
| 转弯纯窗口准确率 | 0.9712 |
| 转弯过渡窗口准确率 | 0.7262 |
| 坡度 MAE deg | 0.4616 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 7613 | 53 | 251 | 0.9616 |
| stall | 6 | 1190 | 21 | 0.9778 |
| slope | 69 | 99 | 4294 | 0.9623 |

| pred class | precision |
|---|---:|
| flat | 0.9902 |
| stall | 0.8867 |
| slope | 0.9404 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 2110 | 135 | 16 | 0.9332 |
| straight | 271 | 8774 | 179 | 0.9512 |
| left | 10 | 220 | 1881 | 0.8910 |

| pred class | precision |
|---|---:|
| right | 0.8825 |
| straight | 0.9611 |
| left | 0.9061 |

## 坡度回归范围

- Slope 真值范围: [-8.000, 7.000] deg
- Slope 预测范围: [-8.927, 9.484] deg
- Slope 符号准确率: 0.9989

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 2150 | 0.9470 | 0.4842 | 1.0000 | [2.000, 7.000] | [0.500, 9.484] |
| downhill | 2312 | 0.9766 | 0.4405 | 0.9978 | [-8.000, -2.000] | [-8.927, 1.898] |
