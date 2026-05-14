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
| acc_turn | 0.9483 |
| acc_turn_pure | 0.9825 |
| acc_turn_transition | 0.7234 |
| turn_right_recall | 0.9368 |
| turn_straight_recall | 0.9445 |
| turn_left_recall | 0.9773 |
| theta_mae_deg | 0.4814 |
| theta_flat_abs_p95_deg | 1.1831 |
| theta_flat_bias_deg | 0.0302 |
| theta_near_flat_abs_p95_deg | 2.0180 |
| theta_near_flat_bias_deg | 0.0378 |
| theta_flat_turn_abs_p95_deg | 1.0767 |
| flat_recall | 0.9888 |
| stall_recall | 0.9482 |
| slope_recall | 0.9868 |
| uphill_recall | 0.9916 |
| downhill_recall | 0.9823 |

- best_epoch: 80
- train_seconds: 3376.7


## 验证集最佳点

```json
{
  "loss_total": 0.05835329558624916,
  "acc_main": 0.9890419298379118,
  "acc_turn": 0.947188189635492,
  "acc_turn_pure": 0.9749238136700044,
  "acc_turn_transition": 0.7548309178743962,
  "flat_recall": 0.9914225389284772,
  "stall_recall": 0.970467596390484,
  "slope_recall": 0.9901012891344383,
  "recall_main": [
    0.9914225389284772,
    0.970467596390484,
    0.9901012891344383
  ],
  "turn_right_recall": 0.94062205466541,
  "turn_straight_recall": 0.9410029498525073,
  "turn_left_recall": 0.9782312925170068,
  "recall_turn": [
    0.94062205466541,
    0.9410029498525073,
    0.9782312925170068
  ],
  "cm_turn": [
    [
      1996,
      99,
      27
    ],
    [
      216,
      8294,
      304
    ],
    [
      8,
      40,
      2157
    ]
  ],
  "n_turn_transition": 1656,
  "n_turn_pure": 11485,
  "cm_main": [
    [
      7513,
      19,
      46
    ],
    [
      15,
      1183,
      21
    ],
    [
      33,
      10,
      4301
    ]
  ],
  "theta_mae_rad": 0.008845852687954903,
  "theta_mae_deg": 0.5068299770355225,
  "uphill_recall": 0.9869394862864606,
  "downhill_recall": 0.9936492427943332,
  "slope_sign_acc": 0.9976979742173112,
  "theta_flat_mae_deg": 0.41613519191741943,
  "theta_flat_abs_p95_deg": 1.258879542350769,
  "theta_flat_bias_deg": 0.009028463624417782,
  "theta_flat_n": 7578.0,
  "theta_near_flat_mae_deg": 0.47899216413497925,
  "theta_near_flat_abs_p95_deg": 1.685159683227539,
  "theta_near_flat_bias_deg": 0.06106765568256378,
  "theta_near_flat_n": 6542.0,
  "theta_flat_turn_mae_deg": 0.33668118715286255,
  "theta_flat_turn_abs_p95_deg": 1.1460670232772827,
  "theta_flat_turn_bias_deg": 0.09224463254213333,
  "theta_flat_turn_n": 2411.0,
  "theta_slope_control_mae_deg": 0.5068299770355225,
  "theta_slope_control_abs_p95_deg": 6.637754917144775,
  "theta_slope_control_bias_deg": -0.25038421154022217,
  "theta_slope_control_n": 4344.0
}
```
