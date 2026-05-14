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
| acc_main | 0.9645 |
| acc_turn | 0.9049 |
| acc_turn_pure | 0.9260 |
| acc_turn_transition | 0.7666 |
| theta_mae_deg | 0.5354 |
| flat_recall | 0.9547 |
| stall_recall | 0.8146 |
| slope_recall | 0.9944 |
| uphill_recall | 0.9931 |
| downhill_recall | 0.9964 |

- best_epoch: 56
- train_seconds: 2001.0


## 验证集最佳点

```json
{
  "loss_total": 0.1290950391701241,
  "acc_main": 0.9829302987197724,
  "acc_turn": 0.9174964438122333,
  "acc_turn_pure": 0.9476935749588138,
  "acc_turn_transition": 0.7265625,
  "flat_recall": 0.9903632320237212,
  "stall_recall": 0.873015873015873,
  "slope_recall": 0.9913657770800628,
  "recall_main": [
    0.9903632320237212,
    0.873015873015873,
    0.9913657770800628
  ],
  "n_turn_transition": 384,
  "n_turn_pure": 2428,
  "cm_main": [
    [
      1336,
      2,
      11
    ],
    [
      3,
      165,
      21
    ],
    [
      9,
      2,
      1263
    ]
  ],
  "theta_mae_rad": 0.009501069784164429,
  "theta_mae_deg": 0.5443711876869202,
  "uphill_recall": 0.9892617449664429,
  "downhill_recall": 0.994328922495274,
  "slope_sign_acc": 0.9968602825745683
}
```
