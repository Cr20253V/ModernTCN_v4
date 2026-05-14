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
| acc_main | 0.9820 |
| acc_turn | 0.9427 |
| acc_turn_pure | 0.9739 |
| acc_turn_transition | 0.7373 |
| turn_right_recall | 0.8846 |
| turn_straight_recall | 0.9535 |
| turn_left_recall | 0.9578 |
| theta_mae_deg | 0.5395 |
| theta_flat_abs_p95_deg | 1.3117 |
| theta_flat_bias_deg | 0.0516 |
| theta_near_flat_abs_p95_deg | 1.9177 |
| theta_near_flat_bias_deg | 0.1998 |
| theta_flat_turn_abs_p95_deg | 1.2713 |
| flat_recall | 0.9804 |
| stall_recall | 0.9704 |
| slope_recall | 0.9879 |
| uphill_recall | 0.9865 |
| downhill_recall | 0.9892 |

- best_epoch: 22
- train_seconds: 1607.9


## 验证集最佳点

```json
{
  "loss_total": 0.05696267901461456,
  "acc_main": 0.9862263145879309,
  "acc_turn": 0.94444867209497,
  "acc_turn_pure": 0.9714410100130605,
  "acc_turn_transition": 0.7572463768115942,
  "flat_recall": 0.9885193982581156,
  "stall_recall": 0.9712879409351928,
  "slope_recall": 0.9864180478821363,
  "recall_main": [
    0.9885193982581156,
    0.9712879409351928,
    0.9864180478821363
  ],
  "turn_right_recall": 0.8892554194156456,
  "turn_straight_recall": 0.9486044928522804,
  "turn_left_recall": 0.9809523809523809,
  "recall_turn": [
    0.8892554194156456,
    0.9486044928522804,
    0.9809523809523809
  ],
  "cm_turn": [
    [
      1887,
      209,
      26
    ],
    [
      185,
      8361,
      268
    ],
    [
      6,
      36,
      2163
    ]
  ],
  "n_turn_transition": 1656,
  "n_turn_pure": 11485,
  "cm_main": [
    [
      7491,
      26,
      61
    ],
    [
      11,
      1184,
      24
    ],
    [
      46,
      13,
      4285
    ]
  ],
  "theta_mae_rad": 0.010266306810081005,
  "theta_mae_deg": 0.5882160067558289,
  "uphill_recall": 0.9821506312581628,
  "downhill_recall": 0.9912066438690766,
  "slope_sign_acc": 0.9990791896869244,
  "theta_flat_mae_deg": 0.36574313044548035,
  "theta_flat_abs_p95_deg": 1.255997657775879,
  "theta_flat_bias_deg": 0.06549987941980362,
  "theta_flat_n": 7578.0,
  "theta_near_flat_mae_deg": 0.45409196615219116,
  "theta_near_flat_abs_p95_deg": 1.7836699485778809,
  "theta_near_flat_bias_deg": 0.22086521983146667,
  "theta_near_flat_n": 6542.0,
  "theta_flat_turn_mae_deg": 0.38100630044937134,
  "theta_flat_turn_abs_p95_deg": 1.1772078275680542,
  "theta_flat_turn_bias_deg": 0.09670180827379227,
  "theta_flat_turn_n": 2411.0,
  "theta_slope_control_mae_deg": 0.5882160067558289,
  "theta_slope_control_abs_p95_deg": 6.526995658874512,
  "theta_slope_control_bias_deg": -0.285041868686676,
  "theta_slope_control_n": 4344.0
}
```
