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
| acc_main | 0.9596 |
| acc_turn | 0.9224 |
| acc_turn_pure | 0.9466 |
| acc_turn_transition | 0.7639 |
| theta_mae_deg | 0.3838 |
| flat_recall | 0.9365 |
| stall_recall | 0.8732 |
| slope_recall | 0.9916 |
| uphill_recall | 0.9897 |
| downhill_recall | 0.9946 |

- best_epoch: 76
- train_seconds: 2483.3

## seed42 进入三 seed 判定

- pass: `1`
- seed42 已满足进入 `[42, 73, 101]` 的最低门槛。

## 验证集最佳点

```json
{
  "loss_total": 0.07186969391906245,
  "acc_main": 0.9836415362731152,
  "acc_turn": 0.9242532005689901,
  "acc_turn_pure": 0.9518121911037891,
  "acc_turn_transition": 0.75,
  "flat_recall": 0.9814677538917717,
  "stall_recall": 0.9576719576719577,
  "slope_recall": 0.9897959183673469,
  "recall_main": [
    0.9814677538917717,
    0.9576719576719577,
    0.9897959183673469
  ],
  "n_turn_transition": 384,
  "n_turn_pure": 2428,
  "cm_main": [
    [
      1324,
      1,
      24
    ],
    [
      1,
      181,
      7
    ],
    [
      8,
      5,
      1261
    ]
  ],
  "theta_mae_rad": 0.007080924231559038,
  "theta_mae_deg": 0.40570706129074097,
  "uphill_recall": 0.9838926174496644,
  "downhill_recall": 0.998109640831758,
  "slope_sign_acc": 0.9992150706436421
}
```
