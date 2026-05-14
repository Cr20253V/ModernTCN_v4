# GRU 训练报告

- 生成时间: 2026-05-06 05:51:17
- 训练模式: `physics_guided`
- 数据集: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v4_industrial.mat`
- 模型文件: `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_v4_industrial_inputstats_hidden96_seed73.mat`
- 最佳轮次: 53
- 最佳验证损失: 0.072756
- 最佳选择分数: 0.111602
- 主任务基座选择分数: 0.111602
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
| 总损失 | 0.097146 |
| 主工况准确率 | 0.9688 |
| 转弯准确率 | 0.9403 |
| 转弯纯窗口准确率 | 0.9720 |
| 转弯过渡窗口准确率 | 0.7317 |
| 坡度 MAE deg | 0.3486 |

## 测试集混淆矩阵

### 主工况

| true \ pred | flat | stall | slope | recall |
|---|---:|---:|---:|---:|
| flat | 7641 | 43 | 233 | 0.9651 |
| stall | 9 | 1188 | 20 | 0.9762 |
| slope | 54 | 65 | 4343 | 0.9733 |

| pred class | precision |
|---|---:|
| flat | 0.9918 |
| stall | 0.9167 |
| slope | 0.9450 |

### 转弯方向

| true \ pred | right | straight | left | recall |
|---|---:|---:|---:|---:|
| right | 2104 | 139 | 18 | 0.9306 |
| straight | 252 | 8768 | 204 | 0.9506 |
| left | 3 | 196 | 1912 | 0.9057 |

| pred class | precision |
|---|---:|
| right | 0.8919 |
| straight | 0.9632 |
| left | 0.8960 |

## 坡度回归范围

- Slope 真值范围: [-8.000, 7.000] deg
- Slope 预测范围: [-8.619, 9.600] deg
- Slope 符号准确率: 0.9975

## 上坡/下坡子项指标

| 子项 | n | slope recall | theta MAE deg | theta sign acc | true theta range deg | pred theta range deg |
|---|---:|---:|---:|---:|---:|---:|
| uphill | 2150 | 0.9684 | 0.3897 | 1.0000 | [2.000, 7.000] | [0.184, 9.600] |
| downhill | 2312 | 0.9779 | 0.3105 | 0.9952 | [-8.000, -2.000] | [-8.619, 2.834] |
