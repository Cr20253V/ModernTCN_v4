# ModernTCN theta-head fine-tune report

- base checkpoint: `results\modern_tcn\modern_tcn_v4_turn_focus_A_seed21\modern_tcn_seed21.pt`
- augment npz: ``
- best epoch: 1
- train seconds: 46.9

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
| acc_main | 0.9870 |
| acc_turn | 0.9523 |
| acc_turn_transition | 0.7624 |
| turn_left_recall | 0.9275 |
| theta_mae_deg | 0.4184 |
| theta_abs_le_8_mae_deg | 0.4184 |
| theta_abs_le_10_mae_deg | 0.4184 |
| theta_pos_6_8_mae_deg | 0.8247 |
| theta_pos_6_8_bias_deg | -0.7939 |
| theta_neg_8_6_mae_deg | 0.5424 |
| theta_neg_8_6_bias_deg | 0.5006 |
| theta_flat_abs_p95_deg | 1.0533 |
| theta_flat_bias_deg | 0.0671 |
| theta_near_flat_abs_p95_deg | 0.8827 |
| theta_near_flat_bias_deg | 0.0964 |
| theta_flat_turn_abs_p95_deg | 0.8670 |
| flat_recall | 0.9900 |
| slope_recall | 0.9883 |
| slope_sign_acc | 0.9989 |

## Validation Best Metrics

```json
{
  "loss_total": 0.09837911057967536,
  "acc_main": 0.9851609466555057,
  "acc_turn": 0.9524389315881592,
  "acc_turn_pure": 0.9772747061384415,
  "acc_turn_transition": 0.7801932367149759,
  "flat_recall": 0.9924782264449723,
  "stall_recall": 0.948318293683347,
  "slope_recall": 0.9827348066298343,
  "recall_main": [
    0.9924782264449723,
    0.948318293683347,
    0.9827348066298343
  ],
  "turn_right_recall": 0.9547596606974552,
  "turn_straight_recall": 0.9491717721806218,
  "turn_left_recall": 0.963265306122449,
  "recall_turn": [
    0.9547596606974552,
    0.9491717721806218,
    0.963265306122449
  ],
  "cm_turn": [
    [
      2026,
      86,
      10
    ],
    [
      244,
      8366,
      204
    ],
    [
      14,
      67,
      2124
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
      8,
      4269
    ]
  ],
  "theta_mae_rad": 0.008104387670755386,
  "theta_mae_deg": 0.4643471837043762,
  "uphill_recall": 0.9821506312581628,
  "downhill_recall": 0.9833903273082559,
  "slope_sign_acc": 1.0,
  "theta_flat_mae_deg": 0.3473733365535736,
  "theta_flat_abs_p95_deg": 1.0128138065338135,
  "theta_flat_bias_deg": 0.07669223099946976,
  "theta_flat_n": 7578.0,
  "theta_near_flat_mae_deg": 0.27359631657600403,
  "theta_near_flat_abs_p95_deg": 0.7741560339927673,
  "theta_near_flat_bias_deg": 0.12317714840173721,
  "theta_near_flat_n": 6542.0,
  "theta_flat_turn_mae_deg": 0.26620417833328247,
  "theta_flat_turn_abs_p95_deg": 0.7490138411521912,
  "theta_flat_turn_bias_deg": 0.14850400388240814,
  "theta_flat_turn_n": 2411.0,
  "theta_slope_control_mae_deg": 0.4643471837043762,
  "theta_slope_control_abs_p95_deg": 6.22484827041626,
  "theta_slope_control_bias_deg": -0.03070000186562538,
  "theta_slope_control_n": 4344.0,
  "theta_abs_le_8_mae_deg": 0.4643471837043762,
  "theta_abs_le_8_rmse_deg": 0.6929060816764832,
  "theta_abs_le_8_p95_abs_err_deg": 1.4870914220809937,
  "theta_abs_le_8_bias_deg": -0.030699998140335083,
  "theta_abs_le_8_n": 4344.0,
  "theta_abs_le_10_mae_deg": 0.4643471837043762,
  "theta_abs_le_10_rmse_deg": 0.6929060816764832,
  "theta_abs_le_10_p95_abs_err_deg": 1.4870914220809937,
  "theta_abs_le_10_bias_deg": -0.030699998140335083,
  "theta_abs_le_10_n": 4344.0,
  "theta_pos_6_8_mae_deg": 1.0357575416564941,
  "theta_pos_6_8_rmse_deg": 1.2188823223114014,
  "theta_pos_6_8_p95_abs_err_deg": 2.345364809036255,
  "theta_pos_6_8_bias_deg": -1.0019221305847168,
  "theta_pos_6_8_n": 414.0,
  "theta_neg_8_6_mae_deg": 0.38671454787254333,
  "theta_neg_8_6_rmse_deg": 0.5844552516937256,
  "theta_neg_8_6_p95_abs_err_deg": 1.1570444107055664,
  "theta_neg_8_6_bias_deg": 0.27471551299095154,
  "theta_neg_8_6_n": 331.0
}
```
