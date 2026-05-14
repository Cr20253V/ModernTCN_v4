# TCN 数据集诊断报告

- Raw file: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_train_data_full.mat`
- Dataset file: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_processed_turn_tail_tmp.mat`

## 窗口纯度

### 主工况

- 窗口数: 2744
- 平均纯度: 0.9333
- 中位数纯度: 1.0000
- 低纯度窗口比例 `<0.8`: 0.1192

| class | windows | mean purity | low purity ratio | theta range mean deg |
|---|---:|---:|---:|---:|
| flat | 1753 | 0.9555 | 0.0804 | 0.3090 |
| stall | 106 | 0.7011 | 0.4528 | 0.2231 |
| slope | 885 | 0.9170 | 0.1559 | 0.7585 |

### 转弯方向

- 窗口数: 2744
- 平均纯度: 0.9601
- 中位数纯度: 1.0000
- 低纯度窗口比例 `<0.8`: 0.0656
- 过渡窗口比例: 0.0743
- 末端标签与多数标签不一致比例: 0.0379

| class | windows | mean purity | low purity ratio | transition ratio | end != majority |
|---|---:|---:|---:|---:|---:|
| right | 460 | 0.9308 | 0.1130 | 0.1217 | 0.0609 |
| straight | 1804 | 0.9725 | 0.0443 | 0.0510 | 0.0266 |
| left | 480 | 0.9415 | 0.1000 | 0.1167 | 0.0583 |

## 传统模型可分性基线

- Bagged trees 主工况准确率: 0.9685
- Bagged trees 转弯准确率: 0.9506
- ECOC 主工况准确率: 0.8989

### Bagged Trees 混淆矩阵

| true \ pred | flat | stall | slope |
|---|---:|---:|---:|
| flat | 265 | 0 | 0 |
| stall | 7 | 10 | 1 |
| slope | 1 | 5 | 156 |

### Bagged Trees 转弯混淆矩阵

| true \ pred | right | straight | left |
|---|---:|---:|---:|
| right | 64 | 3 | 5 |
| straight | 2 | 288 | 1 |
| left | 3 | 8 | 71 |
