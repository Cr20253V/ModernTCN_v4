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
  "lambda_turn": 0.05,
  "lambda_theta": 0.35,
  "lambda_theta_flat": 0.2,
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
  "turn_transition_weight": 1.0
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9589 |
| acc_turn | 0.8912 |
| acc_turn_pure | 0.9171 |
| acc_turn_transition | 0.7215 |
| theta_mae_deg | 0.6312 |
| flat_recall | 0.9481 |
| stall_recall | 0.8390 |
| slope_recall | 0.9853 |
| uphill_recall | 0.9828 |
| downhill_recall | 0.9893 |

- best_epoch: 37
- train_seconds: 1519.0


## 验证集最佳点

```json
{
  "loss_total": 0.06829587469780937,
  "acc_main": 0.9864864864864865,
  "acc_turn": 0.9182076813655761,
  "acc_turn_pure": 0.9411037891268533,
  "acc_turn_transition": 0.7734375,
  "flat_recall": 0.9911045218680504,
  "stall_recall": 0.9365079365079365,
  "slope_recall": 0.989010989010989,
  "recall_main": [
    0.9911045218680504,
    0.9365079365079365,
    0.989010989010989
  ],
  "n_turn_transition": 384,
  "n_turn_pure": 2428,
  "cm_main": [
    [
      1337,
      1,
      11
    ],
    [
      7,
      177,
      5
    ],
    [
      12,
      2,
      1260
    ]
  ],
  "theta_mae_rad": 0.011500719003379345,
  "theta_mae_deg": 0.6589426398277283,
  "uphill_recall": 0.9865771812080537,
  "downhill_recall": 0.9924385633270322,
  "slope_sign_acc": 0.9952904238618524
}
```
