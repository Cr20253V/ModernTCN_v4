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
| acc_main | 0.9632 |
| acc_turn | 0.8981 |
| acc_turn_pure | 0.9310 |
| acc_turn_transition | 0.7076 |
| theta_mae_deg | 0.5015 |
| flat_recall | 0.9563 |
| stall_recall | 0.8612 |
| slope_recall | 0.9893 |
| uphill_recall | 0.9859 |
| downhill_recall | 0.9948 |

- best_epoch: 34
- train_seconds: 1831.8


## 验证集最佳点

```json
{
  "loss_total": 0.1359647991453729,
  "acc_main": 0.9689024390243902,
  "acc_turn": 0.8899390243902439,
  "acc_turn_pure": 0.9316725978647686,
  "acc_turn_transition": 0.6404255319148936,
  "flat_recall": 0.9595898673100121,
  "stall_recall": 0.9300699300699301,
  "slope_recall": 0.9887724550898204,
  "recall_main": [
    0.9595898673100121,
    0.9300699300699301,
    0.9887724550898204
  ],
  "n_turn_transition": 470,
  "n_turn_pure": 2810,
  "cm_main": [
    [
      1591,
      4,
      63
    ],
    [
      1,
      266,
      19
    ],
    [
      14,
      1,
      1321
    ]
  ],
  "theta_mae_rad": 0.009741655550897121,
  "theta_mae_deg": 0.5581557154655457,
  "uphill_recall": 0.9860935524652339,
  "downhill_recall": 0.9926605504587156,
  "slope_sign_acc": 0.999251497005988
}
```
