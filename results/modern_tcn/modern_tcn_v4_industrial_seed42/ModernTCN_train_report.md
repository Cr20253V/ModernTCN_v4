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
| acc_main | 0.9818 |
| acc_turn | 0.9476 |
| acc_turn_pure | 0.9785 |
| acc_turn_transition | 0.7446 |
| turn_right_recall | 0.9292 |
| turn_straight_recall | 0.9576 |
| turn_left_recall | 0.9237 |
| theta_mae_deg | 0.4335 |
| theta_flat_abs_p95_deg | 1.3194 |
| theta_flat_bias_deg | -0.1885 |
| theta_near_flat_abs_p95_deg | 1.9939 |
| theta_near_flat_bias_deg | -0.1185 |
| theta_flat_turn_abs_p95_deg | 0.9367 |
| flat_recall | 0.9864 |
| stall_recall | 0.9729 |
| slope_recall | 0.9760 |
| uphill_recall | 0.9721 |
| downhill_recall | 0.9797 |

- best_epoch: 42
- train_seconds: 2226.2

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.7446

## 验证集最佳点

```json
{
  "loss_total": 0.056662323978287236,
  "acc_main": 0.9864546077163078,
  "acc_turn": 0.948634046115212,
  "acc_turn_pure": 0.9764910753156291,
  "acc_turn_transition": 0.7554347826086957,
  "flat_recall": 0.9908946951702297,
  "stall_recall": 0.9844134536505332,
  "slope_recall": 0.9792817679558011,
  "recall_main": [
    0.9908946951702297,
    0.9844134536505332,
    0.9792817679558011
  ],
  "turn_right_recall": 0.9382657869934025,
  "turn_straight_recall": 0.9484910369866122,
  "turn_left_recall": 0.9591836734693877,
  "recall_turn": [
    0.9382657869934025,
    0.9484910369866122,
    0.9591836734693877
  ],
  "cm_turn": [
    [
      1991,
      114,
      17
    ],
    [
      243,
      8360,
      211
    ],
    [
      7,
      83,
      2115
    ]
  ],
  "n_turn_transition": 1656,
  "n_turn_pure": 11485,
  "cm_main": [
    [
      7509,
      31,
      38
    ],
    [
      11,
      1200,
      8
    ],
    [
      67,
      23,
      4254
    ]
  ],
  "theta_mae_rad": 0.008150092326104641,
  "theta_mae_deg": 0.46696585416793823,
  "uphill_recall": 0.9725729212015672,
  "downhill_recall": 0.986809965803615,
  "slope_sign_acc": 0.9988489871086557,
  "theta_flat_mae_deg": 0.4050601124763489,
  "theta_flat_abs_p95_deg": 1.1979438066482544,
  "theta_flat_bias_deg": -0.18819153308868408,
  "theta_flat_n": 7578.0,
  "theta_near_flat_mae_deg": 0.5138393044471741,
  "theta_near_flat_abs_p95_deg": 1.663557529449463,
  "theta_near_flat_bias_deg": -0.09202879667282104,
  "theta_near_flat_n": 6542.0,
  "theta_flat_turn_mae_deg": 0.35524219274520874,
  "theta_flat_turn_abs_p95_deg": 0.819747805595398,
  "theta_flat_turn_bias_deg": -0.04865863919258118,
  "theta_flat_turn_n": 2411.0,
  "theta_slope_control_mae_deg": 0.46696585416793823,
  "theta_slope_control_abs_p95_deg": 6.941854953765869,
  "theta_slope_control_bias_deg": 0.2926618456840515,
  "theta_slope_control_n": 4344.0
}
```
