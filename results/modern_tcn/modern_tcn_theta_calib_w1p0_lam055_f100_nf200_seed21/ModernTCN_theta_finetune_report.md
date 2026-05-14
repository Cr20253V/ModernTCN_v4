# ModernTCN theta-head fine-tune report

- base checkpoint: `results\modern_tcn\modern_tcn_v4_turn_focus_A_seed21\modern_tcn_seed21.pt`
- augment npz: ``
- best epoch: 1
- train seconds: 50.3

## Config

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
  "lambda_theta": 0.55,
  "lambda_theta_flat": 1.0,
  "lambda_theta_near_flat": 2.0,
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
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 1.5,
  "select_turn_weight": 0.35,
  "select_turn_transition_weight": 2.0,
  "select_turn_transition_target": 0.75,
  "select_turn_left_weight": 0.2,
  "select_turn_left_target": 0.9,
  "select_theta_flat_p95_weight": 2.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 1.0,
  "select_theta_flat_bias_target_deg": 0.2
}
```

## Test Metrics

| metric | value |
|---|---:|
| acc_main | 0.9867 |
| acc_turn | 0.9529 |
| acc_turn_transition | 0.7624 |
| turn_left_recall | 0.9469 |
| theta_mae_deg | 0.4679 |
| theta_abs_le_8_mae_deg | 0.4679 |
| theta_abs_le_10_mae_deg | 0.4679 |
| theta_pos_6_8_mae_deg | 0.9694 |
| theta_pos_6_8_bias_deg | -0.9598 |
| theta_neg_8_6_mae_deg | 0.7361 |
| theta_neg_8_6_bias_deg | 0.7110 |
| theta_flat_abs_p95_deg | 1.0065 |
| theta_flat_bias_deg | 0.0606 |
| theta_near_flat_abs_p95_deg | 0.8474 |
| theta_near_flat_bias_deg | 0.0982 |
| theta_flat_turn_abs_p95_deg | 0.7968 |
| flat_recall | 0.9876 |
| slope_recall | 0.9890 |
| slope_sign_acc | 0.9987 |

## Validation Best Metrics

```json
{
  "loss_total": 0.08379629982503416,
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
  "theta_mae_rad": 0.009312178939580917,
  "theta_mae_deg": 0.5335485339164734,
  "uphill_recall": 0.9830213321723987,
  "downhill_recall": 0.9848558866634098,
  "slope_sign_acc": 1.0,
  "theta_flat_mae_deg": 0.33655881881713867,
  "theta_flat_abs_p95_deg": 0.9592937231063843,
  "theta_flat_bias_deg": 0.07433641701936722,
  "theta_flat_n": 7578.0,
  "theta_near_flat_mae_deg": 0.2651295065879822,
  "theta_near_flat_abs_p95_deg": 0.751996636390686,
  "theta_near_flat_bias_deg": 0.12620387971401215,
  "theta_near_flat_n": 6542.0,
  "theta_flat_turn_mae_deg": 0.2668791115283966,
  "theta_flat_turn_abs_p95_deg": 0.7286971807479858,
  "theta_flat_turn_bias_deg": 0.17197024822235107,
  "theta_flat_turn_n": 2411.0,
  "theta_slope_control_mae_deg": 0.5335485339164734,
  "theta_slope_control_abs_p95_deg": 6.119600296020508,
  "theta_slope_control_bias_deg": 0.023182708770036697,
  "theta_slope_control_n": 4344.0,
  "theta_abs_le_8_mae_deg": 0.5335485339164734,
  "theta_abs_le_8_rmse_deg": 0.7792803645133972,
  "theta_abs_le_8_p95_abs_err_deg": 1.729824423789978,
  "theta_abs_le_8_bias_deg": 0.023182706907391548,
  "theta_abs_le_8_n": 4344.0,
  "theta_abs_le_10_mae_deg": 0.5335485339164734,
  "theta_abs_le_10_rmse_deg": 0.7792803645133972,
  "theta_abs_le_10_p95_abs_err_deg": 1.729824423789978,
  "theta_abs_le_10_bias_deg": 0.023182706907391548,
  "theta_abs_le_10_n": 4344.0,
  "theta_pos_6_8_mae_deg": 1.1651318073272705,
  "theta_pos_6_8_rmse_deg": 1.3713068962097168,
  "theta_pos_6_8_p95_abs_err_deg": 2.6075572967529297,
  "theta_pos_6_8_bias_deg": -1.1461044549942017,
  "theta_pos_6_8_n": 414.0,
  "theta_neg_8_6_mae_deg": 0.4643602967262268,
  "theta_neg_8_6_rmse_deg": 0.6215769052505493,
  "theta_neg_8_6_p95_abs_err_deg": 1.1177785396575928,
  "theta_neg_8_6_bias_deg": 0.38481706380844116,
  "theta_neg_8_6_n": 331.0
}
```
