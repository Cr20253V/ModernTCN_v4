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
  "lambda_turn": 0.2,
  "lambda_theta": 0.35,
  "lambda_theta_flat": 0.2,
  "main_class_multipliers": [
    1.2,
    1.0,
    0.95
  ],
  "turn_class_multipliers": [
    1.3,
    0.7,
    1.3
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 2.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 2.0,
  "select_turn_weight": 0.7,
  "select_turn_transition_weight": 2.0,
  "select_turn_transition_target": 0.75,
  "select_turn_left_weight": 2.0,
  "select_turn_left_target": 0.85
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9662 |
| acc_turn | 0.9044 |
| acc_turn_pure | 0.9353 |
| acc_turn_transition | 0.7260 |
| turn_right_recall | 0.8629 |
| turn_straight_recall | 0.8976 |
| turn_left_recall | 0.9610 |
| theta_mae_deg | 0.3993 |
| flat_recall | 0.9596 |
| stall_recall | 0.8826 |
| slope_recall | 0.9887 |
| uphill_recall | 0.9859 |
| downhill_recall | 0.9931 |

- best_epoch: 53
- train_seconds: 2394.4


## 验证集最佳点

```json
{
  "loss_total": 0.23036436016966658,
  "acc_main": 0.9698170731707317,
  "acc_turn": 0.9057926829268292,
  "acc_turn_pure": 0.9373665480427046,
  "acc_turn_transition": 0.7170212765957447,
  "flat_recall": 0.9607961399276237,
  "stall_recall": 0.9090909090909091,
  "slope_recall": 0.9940119760479041,
  "recall_main": [
    0.9607961399276237,
    0.9090909090909091,
    0.9940119760479041
  ],
  "turn_right_recall": 0.9102402022756005,
  "turn_straight_recall": 0.8856410256410256,
  "turn_left_recall": 0.9721706864564007,
  "recall_turn": [
    0.9102402022756005,
    0.8856410256410256,
    0.9721706864564007
  ],
  "cm_turn": [
    [
      720,
      40,
      31
    ],
    [
      84,
      1727,
      139
    ],
    [
      0,
      15,
      524
    ]
  ],
  "n_turn_transition": 470,
  "n_turn_pure": 2810,
  "cm_main": [
    [
      1593,
      3,
      62
    ],
    [
      7,
      260,
      19
    ],
    [
      6,
      2,
      1328
    ]
  ],
  "theta_mae_rad": 0.007017569616436958,
  "theta_mae_deg": 0.4020771086215973,
  "uphill_recall": 0.9962073324905183,
  "downhill_recall": 0.9908256880733946,
  "slope_sign_acc": 1.0
}
```
