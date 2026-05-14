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
  "turn_head_source": "kinematic_stats",
  "turn_feature_indices": [
    1,
    4,
    5,
    6,
    7,
    9,
    10,
    11,
    16
  ],
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
| acc_main | 0.9752 |
| acc_turn | 0.7894 |
| acc_turn_pure | 0.8298 |
| acc_turn_transition | 0.5944 |
| turn_right_recall | 0.9565 |
| turn_straight_recall | 0.6617 |
| turn_left_recall | 0.9596 |
| theta_mae_deg | 0.3931 |
| flat_recall | 0.9867 |
| stall_recall | 0.8852 |
| slope_recall | 0.9776 |
| uphill_recall | 0.9669 |
| downhill_recall | 0.9933 |

- best_epoch: 74
- train_seconds: 3251.9


## 验证集最佳点

```json
{
  "loss_total": 0.11279154833791134,
  "acc_main": 0.9836544074722708,
  "acc_turn": 0.819614711033275,
  "acc_turn_pure": 0.8491600959890299,
  "acc_turn_transition": 0.650294695481336,
  "flat_recall": 0.983494593056346,
  "stall_recall": 0.9635036496350365,
  "slope_recall": 0.9878136200716846,
  "recall_main": [
    0.983494593056346,
    0.9635036496350365,
    0.9878136200716846
  ],
  "turn_right_recall": 0.8610271903323263,
  "turn_straight_recall": 0.7482758620689656,
  "turn_left_recall": 0.9795640326975477,
  "recall_turn": [
    0.8610271903323263,
    0.7482758620689656,
    0.9795640326975477
  ],
  "cm_turn": [
    [
      570,
      69,
      23
    ],
    [
      230,
      1519,
      281
    ],
    [
      0,
      15,
      719
    ]
  ],
  "n_turn_transition": 509,
  "n_turn_pure": 2917,
  "cm_main": [
    [
      1728,
      5,
      24
    ],
    [
      8,
      264,
      2
    ],
    [
      10,
      7,
      1378
    ]
  ],
  "theta_mae_rad": 0.00567835895344615,
  "theta_mae_deg": 0.3253459930419922,
  "uphill_recall": 0.9840546697038725,
  "downhill_recall": 0.9941972920696325,
  "slope_sign_acc": 0.9978494623655914
}
```
