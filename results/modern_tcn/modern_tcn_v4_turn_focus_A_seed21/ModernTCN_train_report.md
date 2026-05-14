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
| acc_main | 0.9867 |
| acc_turn | 0.9529 |
| acc_turn_pure | 0.9819 |
| acc_turn_transition | 0.7624 |
| turn_right_recall | 0.9363 |
| turn_straight_recall | 0.9584 |
| turn_left_recall | 0.9469 |
| theta_mae_deg | 0.3603 |
| theta_flat_abs_p95_deg | 1.1972 |
| theta_flat_bias_deg | -0.1549 |
| theta_near_flat_abs_p95_deg | 1.0479 |
| theta_near_flat_bias_deg | -0.0978 |
| theta_flat_turn_abs_p95_deg | 0.8884 |
| flat_recall | 0.9876 |
| stall_recall | 0.9721 |
| slope_recall | 0.9890 |
| uphill_recall | 0.9944 |
| downhill_recall | 0.9840 |

- best_epoch: 77
- train_seconds: 1044.6


## 验证集最佳点

```json
{
  "loss_total": 0.08363620203903195,
  "acc_main": 0.9851609466555057,
  "acc_turn": 0.9511452705273571,
  "acc_turn_pure": 0.9759686547670875,
  "acc_turn_transition": 0.7789855072463768,
  "flat_recall": 0.9891792029559251,
  "stall_recall": 0.9647251845775225,
  "slope_recall": 0.9838858195211786,
  "recall_main": [
    0.9891792029559251,
    0.9647251845775225,
    0.9838858195211786
  ],
  "turn_right_recall": 0.9349670122525919,
  "turn_straight_recall": 0.949739051508963,
  "turn_left_recall": 0.9723356009070295,
  "recall_turn": [
    0.9349670122525919,
    0.949739051508963,
    0.9723356009070295
  ],
  "cm_turn": [
    [
      1984,
      127,
      11
    ],
    [
      200,
      8371,
      243
    ],
    [
      13,
      48,
      2144
    ]
  ],
  "n_turn_transition": 1656,
  "n_turn_pure": 11485,
  "cm_main": [
    [
      7496,
      29,
      53
    ],
    [
      18,
      1176,
      25
    ],
    [
      60,
      10,
      4274
    ]
  ],
  "theta_mae_rad": 0.007069976534694433,
  "theta_mae_deg": 0.40507978200912476,
  "uphill_recall": 0.9830213321723987,
  "downhill_recall": 0.9848558866634098,
  "slope_sign_acc": 0.9990791896869244,
  "theta_flat_mae_deg": 0.34592679142951965,
  "theta_flat_abs_p95_deg": 1.1283953189849854,
  "theta_flat_bias_deg": -0.15151573717594147,
  "theta_flat_n": 7578.0,
  "theta_near_flat_mae_deg": 0.3496719002723694,
  "theta_near_flat_abs_p95_deg": 0.8869189023971558,
  "theta_near_flat_bias_deg": -0.07689157873392105,
  "theta_near_flat_n": 6542.0,
  "theta_flat_turn_mae_deg": 0.2672170102596283,
  "theta_flat_turn_abs_p95_deg": 0.7301356792449951,
  "theta_flat_turn_bias_deg": -0.06863389164209366,
  "theta_flat_turn_n": 2411.0,
  "theta_slope_control_mae_deg": 0.40507978200912476,
  "theta_slope_control_abs_p95_deg": 6.54356050491333,
  "theta_slope_control_bias_deg": 0.004096158314496279,
  "theta_slope_control_n": 4344.0
}
```
