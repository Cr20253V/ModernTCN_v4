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
| acc_main | 0.9847 |
| acc_turn | 0.9448 |
| acc_turn_pure | 0.9725 |
| acc_turn_transition | 0.7630 |
| turn_right_recall | 0.8885 |
| turn_straight_recall | 0.9579 |
| turn_left_recall | 0.9479 |
| theta_mae_deg | 0.4669 |
| theta_flat_abs_p95_deg | 1.0079 |
| theta_flat_bias_deg | -0.0022 |
| theta_near_flat_abs_p95_deg | 1.1477 |
| theta_near_flat_bias_deg | 0.0185 |
| theta_flat_turn_abs_p95_deg | 0.8017 |
| flat_recall | 0.9886 |
| stall_recall | 0.9688 |
| slope_recall | 0.9821 |
| uphill_recall | 0.9851 |
| downhill_recall | 0.9792 |

- best_epoch: 55
- train_seconds: 816.9

## seed42 进入三 seed 判定

- pass: `1`
- seed42 已满足进入 `[42, 73, 101]` 的最低门槛。

## 验证集最佳点

```json
{
  "loss_total": 0.07406101489184327,
  "acc_main": 0.9854653374933414,
  "acc_turn": 0.951221368236816,
  "acc_turn_pure": 0.9750979538528516,
  "acc_turn_transition": 0.7856280193236715,
  "flat_recall": 0.9928741092636579,
  "stall_recall": 0.9614438063986874,
  "slope_recall": 0.9792817679558011,
  "recall_main": [
    0.9928741092636579,
    0.9614438063986874,
    0.9792817679558011
  ],
  "turn_right_recall": 0.9123468426013195,
  "turn_straight_recall": 0.9560925799863853,
  "turn_left_recall": 0.9691609977324263,
  "recall_turn": [
    0.9123468426013195,
    0.9560925799863853,
    0.9691609977324263
  ],
  "cm_turn": [
    [
      1936,
      168,
      18
    ],
    [
      162,
      8427,
      225
    ],
    [
      7,
      61,
      2137
    ]
  ],
  "n_turn_transition": 1656,
  "n_turn_pure": 11485,
  "cm_main": [
    [
      7524,
      21,
      33
    ],
    [
      21,
      1172,
      26
    ],
    [
      63,
      27,
      4254
    ]
  ],
  "theta_mae_rad": 0.008968149311840534,
  "theta_mae_deg": 0.5138370990753174,
  "uphill_recall": 0.979538528515455,
  "downhill_recall": 0.9789936492427943,
  "slope_sign_acc": 0.9990791896869244,
  "theta_flat_mae_deg": 0.31885191798210144,
  "theta_flat_abs_p95_deg": 0.9873116612434387,
  "theta_flat_bias_deg": -0.008204392157495022,
  "theta_flat_n": 7578.0,
  "theta_near_flat_mae_deg": 0.2928515076637268,
  "theta_near_flat_abs_p95_deg": 1.014731526374817,
  "theta_near_flat_bias_deg": 0.03538336977362633,
  "theta_near_flat_n": 6542.0,
  "theta_flat_turn_mae_deg": 0.23083645105361938,
  "theta_flat_turn_abs_p95_deg": 0.7410539984703064,
  "theta_flat_turn_bias_deg": -0.028707943856716156,
  "theta_flat_turn_n": 2411.0,
  "theta_slope_control_mae_deg": 0.5138370990753174,
  "theta_slope_control_abs_p95_deg": 6.600299835205078,
  "theta_slope_control_bias_deg": -0.24062415957450867,
  "theta_slope_control_n": 4344.0
}
```
