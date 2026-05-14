# GRU 训练报告

- 生成时间: 2026-05-05 15:29:12
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_v4_industrial_smoke_baseline_seed42.mat`
- 最佳轮次: 1
- 最佳验证损失: 0.269840
- 最佳选择分数: 0.398141
- 主任务基座选择分数: 0.398141
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean`
- Turn head: `linear`, source=`readout`, hidden=64
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
| 总损失 | 0.277890 |
| 主工况准确率 | 0.8950 |
| 转弯准确率 | 0.8513 |
| 转弯纯窗口准确率 | 0.9265 |
| 转弯过渡窗口准确率 | 0.3564 |
| 坡度 MAE deg | 0.6940 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 7236 | 152 | 529 | 0.9140 |
| stall | 14 | 1186 | 17 | 0.9745 |
| slope | 553 | 163 | 3746 | 0.8395 |

| pred class | precision |
|---|---:|
| flat | 0.9273 |
| stall | 0.7901 |
| slope | 0.8728 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 1688 | 537 | 36 | 0.7466 |
| straight | 527 | 8183 | 514 | 0.8871 |
| left | 8 | 400 | 1703 | 0.8067 |

| pred class | precision |
|---|---:|
| right | 0.7593 |
| straight | 0.8973 |
| left | 0.7559 |

## 坡度回归范围

- Slope 真值范围: [-8.000, 7.000] deg
- Slope 预测范围: [-8.359, 7.979] deg
- Slope 符号准确率: 0.9975

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 2150 | 0.7516 | 0.7344 | 0.9991 | [2.000, 7.000] | [-0.630, 7.979] |
| downhill | 2312 | 0.9213 | 0.6565 | 0.9961 | [-8.000, -2.000] | [-8.359, 1.044] |
