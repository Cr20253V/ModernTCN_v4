# GRU 训练报告

- 生成时间: 2026-04-28 13:24:38
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_main_confirm_v1_h96_l2_inputstats_seed73.mat`
- 最佳轮次: 11
- 最佳验证损失: 0.505500
- 最佳选择分数: 0.599855
- 主任务基座选择分数: 0.599855
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
| 总损失 | 0.622205 |
| 主工况准确率 | 0.9124 |
| 转弯准确率 | 0.8517 |
| 转弯纯窗口准确率 | 0.8911 |
| 转弯过渡窗口准确率 | 0.4634 |
| 坡度 MAE deg | 0.8203 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 238 | 6 | 21 | 0.8981 |
| stall | 2 | 14 | 2 | 0.7778 |
| slope | 0 | 8 | 154 | 0.9506 |

| pred class | precision |
|---|---:|
| flat | 0.9917 |
| stall | 0.5000 |
| slope | 0.8701 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 59 | 6 | 7 | 0.8194 |
| straight | 16 | 265 | 10 | 0.9107 |
| left | 8 | 19 | 55 | 0.6707 |

| pred class | precision |
|---|---:|
| right | 0.7108 |
| straight | 0.9138 |
| left | 0.7639 |

## 坡度回归范围

- Slope 真值范围: [-5.500, 7.500] deg
- Slope 预测范围: [-7.320, 8.834] deg
- Slope 符号准确率: 0.9877

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 133 | 0.9699 | 0.6672 | 1.0000 | [2.884, 7.500] | [1.377, 8.834] |
| downhill | 29 | 0.8621 | 1.5223 | 0.9310 | [-5.500, -2.298] | [-7.320, 1.144] |
