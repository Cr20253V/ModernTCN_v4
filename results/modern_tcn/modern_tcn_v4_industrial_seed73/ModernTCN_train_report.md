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
| acc_main | 0.9845 |
| acc_turn | 0.9440 |
| acc_turn_pure | 0.9740 |
| acc_turn_transition | 0.7468 |
| turn_right_recall | 0.8969 |
| turn_straight_recall | 0.9614 |
| turn_left_recall | 0.9185 |
| theta_mae_deg | 0.5804 |
| theta_flat_abs_p95_deg | 1.4233 |
| theta_flat_bias_deg | -0.2927 |
| theta_near_flat_abs_p95_deg | 1.7014 |
| theta_near_flat_bias_deg | -0.2169 |
| theta_flat_turn_abs_p95_deg | 1.1026 |
| flat_recall | 0.9856 |
| stall_recall | 0.9753 |
| slope_recall | 0.9850 |
| uphill_recall | 0.9898 |
| downhill_recall | 0.9805 |

- best_epoch: 44
- train_seconds: 2291.5


## 验证集最佳点

```json
{
  "loss_total": 0.05456831352016274,
  "acc_main": 0.9867589985541435,
  "acc_turn": 0.9503081957233087,
  "acc_turn_pure": 0.9742272529386156,
  "acc_turn_transition": 0.7844202898550725,
  "flat_recall": 0.9908946951702297,
  "stall_recall": 0.970467596390484,
  "slope_recall": 0.9841160220994475,
  "recall_main": [
    0.9908946951702297,
    0.970467596390484,
    0.9841160220994475
  ],
  "turn_right_recall": 0.9005655042412818,
  "turn_straight_recall": 0.9582482414340822,
  "turn_left_recall": 0.9664399092970521,
  "recall_turn": [
    0.9005655042412818,
    0.9582482414340822,
    0.9664399092970521
  ],
  "cm_turn": [
    [
      1911,
      196,
      15
    ],
    [
      163,
      8446,
      205
    ],
    [
      5,
      69,
      2131
    ]
  ],
  "n_turn_transition": 1656,
  "n_turn_pure": 11485,
  "cm_main": [
    [
      7509,
      20,
      49
    ],
    [
      17,
      1183,
      19
    ],
    [
      51,
      18,
      4275
    ]
  ],
  "theta_mae_rad": 0.009910407476127148,
  "theta_mae_deg": 0.5678244829177856,
  "uphill_recall": 0.9791031780583369,
  "downhill_recall": 0.9897410845139228,
  "slope_sign_acc": 0.9995395948434622,
  "theta_flat_mae_deg": 0.47973406314849854,
  "theta_flat_abs_p95_deg": 1.3583382368087769,
  "theta_flat_bias_deg": -0.2442816197872162,
  "theta_flat_n": 7578.0,
  "theta_near_flat_mae_deg": 0.5811424255371094,
  "theta_near_flat_abs_p95_deg": 1.4802923202514648,
  "theta_near_flat_bias_deg": -0.1386410892009735,
  "theta_near_flat_n": 6542.0,
  "theta_flat_turn_mae_deg": 0.4597350060939789,
  "theta_flat_turn_abs_p95_deg": 1.0589864253997803,
  "theta_flat_turn_bias_deg": -0.05495719984173775,
  "theta_flat_turn_n": 2411.0,
  "theta_slope_control_mae_deg": 0.5678244829177856,
  "theta_slope_control_abs_p95_deg": 7.183150768280029,
  "theta_slope_control_bias_deg": -0.23005534708499908,
  "theta_slope_control_n": 4344.0
}
```
