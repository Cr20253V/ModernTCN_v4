# ModernTCN theta-head fine-tune report

- base checkpoint: `results\modern_tcn\modern_tcn_v4_turn_focus_A_seed21\modern_tcn_seed21.pt`
- augment npz: ``
- best epoch: 1
- train seconds: 46.1

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
  "lambda_theta": 0.75,
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
  "theta_pos_weight": 1.25,
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
| acc_main | 0.9870 |
| acc_turn | 0.9522 |
| acc_turn_transition | 0.7624 |
| turn_left_recall | 0.9270 |
| theta_mae_deg | 0.4580 |
| theta_abs_le_8_mae_deg | 0.4580 |
| theta_abs_le_10_mae_deg | 0.4580 |
| theta_pos_6_8_mae_deg | 0.7972 |
| theta_pos_6_8_bias_deg | -0.7583 |
| theta_neg_8_6_mae_deg | 0.7359 |
| theta_neg_8_6_bias_deg | 0.7141 |
| theta_flat_abs_p95_deg | 1.0428 |
| theta_flat_bias_deg | 0.0946 |
| theta_near_flat_abs_p95_deg | 0.9300 |
| theta_near_flat_bias_deg | 0.1278 |
| theta_flat_turn_abs_p95_deg | 0.9078 |
| flat_recall | 0.9900 |
| slope_recall | 0.9883 |
| slope_sign_acc | 0.9989 |

## Validation Best Metrics

```json
{
  "loss_total": 0.09846913199890205,
  "acc_main": 0.9852370443649646,
  "acc_turn": 0.952819420135454,
  "acc_turn_pure": 0.9773617762298651,
  "acc_turn_transition": 0.782608695652174,
  "flat_recall": 0.9924782264449723,
  "stall_recall": 0.948318293683347,
  "slope_recall": 0.9829650092081031,
  "recall_main": [
    0.9924782264449723,
    0.948318293683347,
    0.9829650092081031
  ],
  "turn_right_recall": 0.9547596606974552,
  "turn_straight_recall": 0.9496255956432947,
  "turn_left_recall": 0.963718820861678,
  "recall_turn": [
    0.9547596606974552,
    0.9496255956432947,
    0.963718820861678
  ],
  "cm_turn": [
    [
      2026,
      86,
      10
    ],
    [
      242,
      8370,
      202
    ],
    [
      14,
      66,
      2125
    ]
  ],
  "n_turn_transition": 1656,
  "n_turn_pure": 11485,
  "cm_main": [
    [
      7521,
      19,
      38
    ],
    [
      25,
      1156,
      38
    ],
    [
      67,
      7,
      4270
    ]
  ],
  "theta_mae_rad": 0.008886057883501053,
  "theta_mae_deg": 0.5091335773468018,
  "uphill_recall": 0.9825859817152808,
  "downhill_recall": 0.9833903273082559,
  "slope_sign_acc": 0.9993093922651933,
  "theta_flat_mae_deg": 0.3556598424911499,
  "theta_flat_abs_p95_deg": 0.9956101775169373,
  "theta_flat_bias_deg": 0.10196959972381592,
  "theta_flat_n": 7578.0,
  "theta_near_flat_mae_deg": 0.28036606311798096,
  "theta_near_flat_abs_p95_deg": 0.7862392067909241,
  "theta_near_flat_bias_deg": 0.1505317986011505,
  "theta_near_flat_n": 6542.0,
  "theta_flat_turn_mae_deg": 0.2768326699733734,
  "theta_flat_turn_abs_p95_deg": 0.76153564453125,
  "theta_flat_turn_bias_deg": 0.16680312156677246,
  "theta_flat_turn_n": 2411.0,
  "theta_slope_control_mae_deg": 0.5091335773468018,
  "theta_slope_control_abs_p95_deg": 6.190746307373047,
  "theta_slope_control_bias_deg": 0.09599586576223373,
  "theta_slope_control_n": 4344.0,
  "theta_abs_le_8_mae_deg": 0.509133517742157,
  "theta_abs_le_8_rmse_deg": 0.7380478978157043,
  "theta_abs_le_8_p95_abs_err_deg": 1.5515302419662476,
  "theta_abs_le_8_bias_deg": 0.09599586576223373,
  "theta_abs_le_8_n": 4344.0,
  "theta_abs_le_10_mae_deg": 0.509133517742157,
  "theta_abs_le_10_rmse_deg": 0.7380478978157043,
  "theta_abs_le_10_p95_abs_err_deg": 1.5515302419662476,
  "theta_abs_le_10_bias_deg": 0.09599586576223373,
  "theta_abs_le_10_n": 4344.0,
  "theta_pos_6_8_mae_deg": 1.0096173286437988,
  "theta_pos_6_8_rmse_deg": 1.2103739976882935,
  "theta_pos_6_8_p95_abs_err_deg": 2.4133143424987793,
  "theta_pos_6_8_bias_deg": -0.9682484269142151,
  "theta_pos_6_8_n": 414.0,
  "theta_neg_8_6_mae_deg": 0.4908793866634369,
  "theta_neg_8_6_rmse_deg": 0.6861595511436462,
  "theta_neg_8_6_p95_abs_err_deg": 1.4027291536331177,
  "theta_neg_8_6_bias_deg": 0.42410945892333984,
  "theta_neg_8_6_n": 331.0
}
```
