# ModernTCN-small 第一阶段训练报告

## 固定约束

- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v3_transition_rich.mat`
- split: 使用 MAT 文件已有 run-level split，不重划分。
- scaler: 使用 MAT 文件已有归一化后 X，不重新拟合。
- input: `[batch, time=128, feature=19]`
- output: `logits_main`, `logits_turn`, `theta_hat`

## 配置

```json
{
  "input_dim": 19,
  "seq_len": 128,
  "channels": 64,
  "blocks": 5,
  "kernel_size": 31,
  "dropout": 0.15,
  "expansion": 2,
  "readout_input_stats": true,
  "lambda_turn": 0.05,
  "lambda_theta": 0.35,
  "lambda_theta_flat": 0.2,
  "main_class_multipliers": [
    1.2,
    1.0,
    0.95
  ],
  "turn_class_multipliers": [
    1.0,
    1.1,
    1.0
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 2.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 1.0
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9670 |
| acc_turn | 0.8940 |
| acc_turn_pure | 0.9219 |
| acc_turn_transition | 0.7109 |
| theta_mae_deg | 0.4381 |
| flat_recall | 0.9514 |
| stall_recall | 0.8878 |
| slope_recall | 0.9916 |
| uphill_recall | 0.9908 |
| downhill_recall | 0.9929 |

- best_epoch: 50
- train_seconds: 1842.7


## 验证集最佳点

```json
{
  "loss_total": 0.0836570664689178,
  "acc_main": 0.9882645803698435,
  "acc_turn": 0.9238975817923186,
  "acc_turn_pure": 0.9530477759472817,
  "acc_turn_transition": 0.7395833333333334,
  "flat_recall": 0.994069681245367,
  "stall_recall": 0.9365079365079365,
  "slope_recall": 0.9897959183673469,
  "recall_main": [
    0.994069681245367,
    0.9365079365079365,
    0.9897959183673469
  ],
  "n_turn_transition": 384,
  "n_turn_pure": 2428,
  "cm_main": [
    [
      1341,
      2,
      6
    ],
    [
      1,
      177,
      11
    ],
    [
      8,
      5,
      1261
    ]
  ],
  "theta_mae_rad": 0.008251135237514973,
  "theta_mae_deg": 0.47275519371032715,
  "uphill_recall": 0.9852348993288591,
  "downhill_recall": 0.996219281663516,
  "slope_sign_acc": 0.9945054945054945
}
```
