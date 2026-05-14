# ModernTCN-small 第一阶段训练报告

## 固定约束

- dataset: `data\tcn\TCN_dataset_v3_transition_rich_clean_turn_aug.mat`
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
  "lambda_turn": 0.1,
  "lambda_theta": 0.35,
  "lambda_theta_flat": 0.2,
  "main_class_multipliers": [
    1.2,
    1.0,
    0.95
  ],
  "turn_class_multipliers": [
    1.2,
    0.8,
    1.2
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 2.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 1.5,
  "select_turn_weight": 0.5,
  "select_turn_transition_weight": 1.5,
  "select_turn_transition_target": 0.75,
  "select_turn_left_weight": 1.0,
  "select_turn_left_target": 0.85
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9755 |
| acc_turn | 0.8855 |
| acc_turn_pure | 0.9180 |
| acc_turn_transition | 0.7291 |
| turn_right_recall | 0.9034 |
| turn_straight_recall | 0.8806 |
| turn_left_recall | 0.8815 |
| theta_mae_deg | 0.4284 |
| flat_recall | 0.9867 |
| stall_recall | 0.9111 |
| slope_recall | 0.9735 |
| uphill_recall | 0.9590 |
| downhill_recall | 0.9949 |

- best_epoch: 55
- train_seconds: 2609.7


## 验证集最佳点

```json
{
  "loss_total": 0.10685243114385422,
  "acc_main": 0.9854057209573847,
  "acc_turn": 0.8937536485697607,
  "acc_turn_pure": 0.9163524168666438,
  "acc_turn_transition": 0.7642436149312377,
  "flat_recall": 0.9846328969834945,
  "stall_recall": 0.9744525547445255,
  "slope_recall": 0.9885304659498207,
  "recall_main": [
    0.9846328969834945,
    0.9744525547445255,
    0.9885304659498207
  ],
  "turn_right_recall": 0.8277945619335347,
  "turn_straight_recall": 0.9054187192118227,
  "turn_left_recall": 0.9209809264305178,
  "recall_turn": [
    0.8277945619335347,
    0.9054187192118227,
    0.9209809264305178
  ],
  "cm_turn": [
    [
      548,
      106,
      8
    ],
    [
      74,
      1838,
      118
    ],
    [
      0,
      58,
      676
    ]
  ],
  "n_turn_transition": 509,
  "n_turn_pure": 2917,
  "cm_main": [
    [
      1730,
      5,
      22
    ],
    [
      5,
      267,
      2
    ],
    [
      7,
      9,
      1379
    ]
  ],
  "theta_mae_rad": 0.0069443229585886,
  "theta_mae_deg": 0.3978803753852844,
  "uphill_recall": 0.9840546697038725,
  "downhill_recall": 0.9961315280464217,
  "slope_sign_acc": 0.996415770609319
}
```
