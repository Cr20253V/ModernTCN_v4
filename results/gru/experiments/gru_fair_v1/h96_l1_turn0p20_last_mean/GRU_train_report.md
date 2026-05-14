# GRU 训练报告

- 生成时间: 2026-04-26 23:03:10
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_fair_v1_h96_l1_turn0p20_last_mean.mat`
- 最佳轮次: 24
- 最佳验证损失: 0.646033
- 最佳选择分数: 0.751721
- 主任务基座选择分数: 0.751721
- 选模指标: `composite`
- Base best metric: `composite`, combine_base_and_turn_best=0
- Head pooling: `last_mean`
- Turn head: `linear`, source=`readout`, hidden=64
- Gradient clip: `global`, threshold=5.000
- 损失权重: 转弯=0.200, 坡度=0.350, 平地坡度约束=0.200, 辅助=0.000, pitch一致性=0.000
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
| 总损失 | 0.817481 |
| 主工况准确率 | 0.9281 |
| 转弯准确率 | 0.7865 |
| 转弯纯窗口准确率 | 0.8317 |
| 转弯过渡窗口准确率 | 0.3415 |
| 坡度 MAE deg | 0.6917 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 249 | 3 | 13 | 0.9396 |
| stall | 1 | 11 | 6 | 0.6111 |
| slope | 1 | 8 | 153 | 0.9444 |

| pred class | precision |
|---|---:|
| flat | 0.9920 |
| stall | 0.5000 |
| slope | 0.8895 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 50 | 15 | 7 | 0.6944 |
| straight | 24 | 242 | 25 | 0.8316 |
| left | 9 | 15 | 58 | 0.7073 |

| pred class | precision |
|---|---:|
| right | 0.6024 |
| straight | 0.8897 |
| left | 0.6444 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-6.455, 8.493] deg
- Slope 符号准确率: 1.0000

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9699 | 0.6178 | 1.0000 | [2.884, 7.500] | [1.799, 8.493] |
| downhill | 29 | 0.8276 | 1.0307 | 1.0000 | [-5.500, -2.298] | [-6.455, -0.115] |
