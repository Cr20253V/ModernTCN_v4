# ModernTCN theta-head fine-tune report

- base checkpoint: `results\modern_tcn\modern_tcn_v4_turn_focus_A_seed21\modern_tcn_seed21.pt`
- augment npz: ``
- best epoch: 9
- train seconds: 96.4

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
  "lambda_theta": 1.0,
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
| theta_mae_deg | 0.4590 |
| theta_abs_le_8_mae_deg | 0.4590 |
| theta_abs_le_10_mae_deg | 0.4590 |
| theta_pos_6_8_mae_deg | 0.8530 |
| theta_pos_6_8_bias_deg | -0.7048 |
| theta_neg_8_6_mae_deg | 0.5434 |
| theta_neg_8_6_bias_deg | 0.3768 |
| theta_flat_abs_p95_deg | 1.0853 |
| theta_flat_bias_deg | -0.0349 |
| theta_near_flat_abs_p95_deg | 0.8873 |
| theta_near_flat_bias_deg | -0.0111 |
| theta_flat_turn_abs_p95_deg | 0.8406 |
| flat_recall | 0.9876 |
| slope_recall | 0.9890 |
| slope_sign_acc | 0.9987 |

## Validation Best Metrics

```json
{
  "loss_total": 0.08386607005025379,
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
  "theta_mae_rad": 0.00863339938223362,
  "theta_mae_deg": 0.4946573078632355,
  "uphill_recall": 0.9830213321723987,
  "downhill_recall": 0.9848558866634098,
  "slope_sign_acc": 1.0,
  "theta_flat_mae_deg": 0.3438052237033844,
  "theta_flat_abs_p95_deg": 1.0675454139709473,
  "theta_flat_bias_deg": -0.0391978994011879,
  "theta_flat_n": 7578.0,
  "theta_near_flat_mae_deg": 0.2772476077079773,
  "theta_near_flat_abs_p95_deg": 0.7730472087860107,
  "theta_near_flat_bias_deg": 0.008552209474146366,
  "theta_near_flat_n": 6542.0,
  "theta_flat_turn_mae_deg": 0.28250646591186523,
  "theta_flat_turn_abs_p95_deg": 0.7813905477523804,
  "theta_flat_turn_bias_deg": 0.018419135361909866,
  "theta_flat_turn_n": 2411.0,
  "theta_slope_control_mae_deg": 0.4946573078632355,
  "theta_slope_control_abs_p95_deg": 6.559820175170898,
  "theta_slope_control_bias_deg": -0.05227252468466759,
  "theta_slope_control_n": 4344.0,
  "theta_abs_le_8_mae_deg": 0.49465733766555786,
  "theta_abs_le_8_rmse_deg": 0.73847496509552,
  "theta_abs_le_8_p95_abs_err_deg": 1.6054362058639526,
  "theta_abs_le_8_bias_deg": -0.05227252468466759,
  "theta_abs_le_8_n": 4344.0,
  "theta_abs_le_10_mae_deg": 0.49465733766555786,
  "theta_abs_le_10_rmse_deg": 0.73847496509552,
  "theta_abs_le_10_p95_abs_err_deg": 1.6054362058639526,
  "theta_abs_le_10_bias_deg": -0.05227252468466759,
  "theta_abs_le_10_n": 4344.0,
  "theta_pos_6_8_mae_deg": 1.0397489070892334,
  "theta_pos_6_8_rmse_deg": 1.3046972751617432,
  "theta_pos_6_8_p95_abs_err_deg": 2.7128820419311523,
  "theta_pos_6_8_bias_deg": -0.8946087956428528,
  "theta_pos_6_8_n": 414.0,
  "theta_neg_8_6_mae_deg": 0.37274420261383057,
  "theta_neg_8_6_rmse_deg": 0.5501984357833862,
  "theta_neg_8_6_p95_abs_err_deg": 1.107283592224121,
  "theta_neg_8_6_bias_deg": -0.013164080679416656,
  "theta_neg_8_6_n": 331.0
}
```
