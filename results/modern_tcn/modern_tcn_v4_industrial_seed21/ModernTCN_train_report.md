# ModernTCN-small 第一阶段训练报告

## 固定约束

- dataset: `data\tcn\ModernTCN_dataset_v4_industrial.mat`
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
  "turn_head_source": "full",
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
  "lambda_turn": 0.05,
  "lambda_theta": 0.35,
  "lambda_theta_flat": 0.2,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
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
  "turn_transition_weight": 1.0,
  "select_turn_weight": 0.3,
  "select_turn_transition_weight": 1.0,
  "select_turn_transition_target": 0.75,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.8,
  "select_theta_flat_p95_weight": 0.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.0,
  "select_theta_flat_bias_target_deg": 0.2
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9821 |
| acc_turn | 0.9409 |
| acc_turn_pure | 0.9697 |
| acc_turn_transition | 0.7513 |
| turn_right_recall | 0.8717 |
| turn_straight_recall | 0.9624 |
| turn_left_recall | 0.9209 |
| theta_mae_deg | 0.3965 |
| theta_flat_abs_p95_deg | 1.3551 |
| theta_flat_bias_deg | -0.1397 |
| theta_near_flat_abs_p95_deg | 1.6603 |
| theta_near_flat_bias_deg | 0.0023 |
| theta_flat_turn_abs_p95_deg | 1.0736 |
| flat_recall | 0.9864 |
| stall_recall | 0.9696 |
| slope_recall | 0.9780 |
| uphill_recall | 0.9823 |
| downhill_recall | 0.9740 |

- best_epoch: 26
- train_seconds: 1732.8


## 验证集最佳点

```json
{
  "loss_total": 0.06746420293584887,
  "acc_main": 0.9840194810136215,
  "acc_turn": 0.9467316033787383,
  "acc_turn_pure": 0.9711797997387898,
  "acc_turn_transition": 0.7771739130434783,
  "flat_recall": 0.9895750857746107,
  "stall_recall": 0.9688269073010665,
  "slope_recall": 0.9785911602209945,
  "recall_main": [
    0.9895750857746107,
    0.9688269073010665,
    0.9785911602209945
  ],
  "turn_right_recall": 0.8906691800188501,
  "turn_straight_recall": 0.9571136827773996,
  "turn_left_recall": 0.9591836734693877,
  "recall_turn": [
    0.8906691800188501,
    0.9571136827773996,
    0.9591836734693877
  ],
  "cm_turn": [
    [
      1890,
      220,
      12
    ],
    [
      164,
      8436,
      214
    ],
    [
      11,
      79,
      2115
    ]
  ],
  "n_turn_transition": 1656,
  "n_turn_pure": 11485,
  "cm_main": [
    [
      7499,
      30,
      49
    ],
    [
      16,
      1181,
      22
    ],
    [
      78,
      15,
      4251
    ]
  ],
  "theta_mae_rad": 0.0074372319504618645,
  "theta_mae_deg": 0.4261219799518585,
  "uphill_recall": 0.976926425772747,
  "downhill_recall": 0.9804592085979482,
  "slope_sign_acc": 0.9990791896869244,
  "theta_flat_mae_deg": 0.40795958042144775,
  "theta_flat_abs_p95_deg": 1.33078932762146,
  "theta_flat_bias_deg": -0.1375856101512909,
  "theta_flat_n": 7578.0,
  "theta_near_flat_mae_deg": 0.5151737928390503,
  "theta_near_flat_abs_p95_deg": 1.5548793077468872,
  "theta_near_flat_bias_deg": 0.033956754952669144,
  "theta_near_flat_n": 6542.0,
  "theta_flat_turn_mae_deg": 0.3386107385158539,
  "theta_flat_turn_abs_p95_deg": 0.9643891453742981,
  "theta_flat_turn_bias_deg": 0.1870313584804535,
  "theta_flat_turn_n": 2411.0,
  "theta_slope_control_mae_deg": 0.4261219799518585,
  "theta_slope_control_abs_p95_deg": 6.861861705780029,
  "theta_slope_control_bias_deg": -0.12024224549531937,
  "theta_slope_control_n": 4344.0
}
```
