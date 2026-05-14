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
  "lambda_turn": 0.08,
  "lambda_theta": 0.35,
  "lambda_theta_flat": 0.25,
  "lambda_theta_near_flat": 0.1,
  "theta_near_flat_deg": 0.5,
  "main_class_multipliers": [
    1.2,
    1.0,
    0.95
  ],
  "turn_class_multipliers": [
    1.15,
    1.0,
    1.15
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 2.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 1.5,
  "select_turn_weight": 0.35,
  "select_turn_transition_weight": 2.0,
  "select_turn_transition_target": 0.75,
  "select_turn_left_weight": 0.2,
  "select_turn_left_target": 0.9,
  "select_theta_flat_p95_weight": 1.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.5,
  "select_theta_flat_bias_target_deg": 0.2
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9805 |
| acc_turn | 0.9437 |
| acc_turn_pure | 0.9727 |
| acc_turn_transition | 0.7524 |
| turn_right_recall | 0.9368 |
| turn_straight_recall | 0.9451 |
| turn_left_recall | 0.9446 |
| theta_mae_deg | 0.5390 |
| theta_flat_abs_p95_deg | 1.0052 |
| theta_flat_bias_deg | 0.1185 |
| theta_near_flat_abs_p95_deg | 1.0262 |
| theta_near_flat_bias_deg | 0.2064 |
| theta_flat_turn_abs_p95_deg | 0.7829 |
| flat_recall | 0.9864 |
| stall_recall | 0.9565 |
| slope_recall | 0.9767 |
| uphill_recall | 0.9786 |
| downhill_recall | 0.9749 |

- best_epoch: 37
- train_seconds: 755.8


## 验证集最佳点

```json
{
  "loss_total": 0.07072661582900164,
  "acc_main": 0.9852370443649646,
  "acc_turn": 0.9474925804733277,
  "acc_turn_pure": 0.9736177622986504,
  "acc_turn_transition": 0.7663043478260869,
  "flat_recall": 0.9891792029559251,
  "stall_recall": 0.9770303527481542,
  "slope_recall": 0.9806629834254144,
  "recall_main": [
    0.9891792029559251,
    0.9770303527481542,
    0.9806629834254144
  ],
  "turn_right_recall": 0.941564561734213,
  "turn_straight_recall": 0.9406625822555026,
  "turn_left_recall": 0.980498866213152,
  "recall_turn": [
    0.941564561734213,
    0.9406625822555026,
    0.980498866213152
  ],
  "cm_turn": [
    [
      1998,
      104,
      20
    ],
    [
      244,
      8291,
      279
    ],
    [
      10,
      33,
      2162
    ]
  ],
  "n_turn_transition": 1656,
  "n_turn_pure": 11485,
  "cm_main": [
    [
      7496,
      32,
      50
    ],
    [
      16,
      1191,
      12
    ],
    [
      58,
      26,
      4260
    ]
  ],
  "theta_mae_rad": 0.010739625431597233,
  "theta_mae_deg": 0.6153351664543152,
  "uphill_recall": 0.9791031780583369,
  "downhill_recall": 0.9824132877381534,
  "slope_sign_acc": 0.9988489871086557,
  "theta_flat_mae_deg": 0.3775824010372162,
  "theta_flat_abs_p95_deg": 0.9714455604553223,
  "theta_flat_bias_deg": 0.11147908121347427,
  "theta_flat_n": 7578.0,
  "theta_near_flat_mae_deg": 0.376166969537735,
  "theta_near_flat_abs_p95_deg": 0.9146339893341064,
  "theta_near_flat_bias_deg": 0.2108704000711441,
  "theta_near_flat_n": 6542.0,
  "theta_flat_turn_mae_deg": 0.28939148783683777,
  "theta_flat_turn_abs_p95_deg": 0.705588161945343,
  "theta_flat_turn_bias_deg": 0.022864149883389473,
  "theta_flat_turn_n": 2411.0,
  "theta_slope_control_mae_deg": 0.6153351664543152,
  "theta_slope_control_abs_p95_deg": 6.143816947937012,
  "theta_slope_control_bias_deg": -0.07625547796487808,
  "theta_slope_control_n": 4344.0
}
```
