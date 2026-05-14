# GRU 训练报告

- 生成时间: 2026-04-28 18:25:39
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v2_transition_rich.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_transition_rich_v2_seed42_h96_l2_inputstats.mat`
- 最佳轮次: 21
- 最佳验证损失: 0.167427
- 最佳选择分数: 0.230840
- 主任务基座选择分数: 0.230840
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
| 总损失 | 0.158876 |
| 主工况准确率 | 0.9277 |
| 转弯准确率 | 0.8812 |
| 转弯纯窗口准确率 | 0.9091 |
| 转弯过渡窗口准确率 | 0.6860 |
| 坡度 MAE deg | 0.4687 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 535 | 4 | 34 | 0.9337 |
| stall | 0 | 78 | 0 | 1.0000 |
| slope | 4 | 28 | 285 | 0.8991 |

| pred class | precision |
|---|---:|
| flat | 0.9926 |
| stall | 0.7091 |
| slope | 0.8934 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 110 | 5 | 0 | 0.9565 |
| straight | 22 | 653 | 26 | 0.9315 |
| left | 11 | 51 | 90 | 0.5921 |

| pred class | precision |
|---|---:|
| right | 0.7692 |
| straight | 0.9210 |
| left | 0.7759 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 6.000] deg
- Slope 预测范围: [-6.037, 8.474] deg
- Slope 符号准确率: 0.9968

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 223 | 0.8744 | 0.4562 | 1.0000 | [2.014, 6.000] | [1.425, 8.474] |
| downhill | 94 | 0.9574 | 0.4983 | 0.9894 | [-5.500, -2.074] | [-6.037, 0.911] |
