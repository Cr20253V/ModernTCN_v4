# ModernTCN theta-head fine-tune report

- base checkpoint: `results\modern_tcn\modern_tcn_v4_turn_focus_A_seed21\modern_tcn_seed21.pt`
- augment npz: ``
- best epoch: 1
- train seconds: 72.9

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
  "theta_pos_weight": 1.5,
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
| acc_turn | 0.9521 |
| acc_turn_transition | 0.7624 |
| turn_left_recall | 0.9270 |
| theta_mae_deg | 0.4680 |
| theta_abs_le_8_mae_deg | 0.4680 |
| theta_abs_le_10_mae_deg | 0.4680 |
| theta_pos_6_8_mae_deg | 0.7727 |
| theta_pos_6_8_bias_deg | -0.7289 |
| theta_neg_8_6_mae_deg | 0.7780 |
| theta_neg_8_6_bias_deg | 0.7590 |
| theta_flat_abs_p95_deg | 1.0423 |
| theta_flat_bias_deg | 0.1005 |
| theta_near_flat_abs_p95_deg | 0.9554 |
| theta_near_flat_bias_deg | 0.1384 |
| theta_flat_turn_abs_p95_deg | 0.9191 |
| flat_recall | 0.9900 |
| slope_recall | 0.9883 |
| slope_sign_acc | 0.9989 |

## Validation Best Metrics

```json
{
  "loss_total": 0.09845558024212048,
  "acc_main": 0.9851609466555057,
  "acc_turn": 0.9526672247165361,
  "acc_turn_pure": 0.9773617762298651,
  "acc_turn_transition": 0.7814009661835749,
  "flat_recall": 0.9924782264449723,
  "stall_recall": 0.948318293683347,
  "slope_recall": 0.9827348066298343,
  "recall_main": [
    0.9924782264449723,
    0.948318293683347,
    0.9827348066298343
  ],
  "turn_right_recall": 0.9547596606974552,
  "turn_straight_recall": 0.9493986839119583,
  "turn_left_recall": 0.963718820861678,
  "recall_turn": [
    0.9547596606974552,
    0.9493986839119583,
    0.963718820861678
  ],
  "cm_turn": [
    [
      2026,
      86,
      10
    ],
    [
      243,
      8368,
      203
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
      8,
      4269
    ]
  ],
  "theta_mae_rad": 0.00902669969946146,
  "theta_mae_deg": 0.5171917676925659,
  "uphill_recall": 0.9821506312581628,
  "downhill_recall": 0.9833903273082559,
  "slope_sign_acc": 0.9993093922651933,
  "theta_flat_mae_deg": 0.35735172033309937,
  "theta_flat_abs_p95_deg": 0.9909229278564453,
  "theta_flat_bias_deg": 0.1081153154373169,
  "theta_flat_n": 7578.0,
  "theta_near_flat_mae_deg": 0.2839377224445343,
  "theta_near_flat_abs_p95_deg": 0.8053158521652222,
  "theta_near_flat_bias_deg": 0.161152645945549,
  "theta_near_flat_n": 6542.0,
  "theta_flat_turn_mae_deg": 0.2802383005619049,
  "theta_flat_turn_abs_p95_deg": 0.7599315047264099,
  "theta_flat_turn_bias_deg": 0.17078475654125214,
  "theta_flat_turn_n": 2411.0,
  "theta_slope_control_mae_deg": 0.5171917676925659,
  "theta_slope_control_abs_p95_deg": 6.20111608505249,
  "theta_slope_control_bias_deg": 0.1288953423500061,
  "theta_slope_control_n": 4344.0,
  "theta_abs_le_8_mae_deg": 0.5171917080879211,
  "theta_abs_le_8_rmse_deg": 0.7444486021995544,
  "theta_abs_le_8_p95_abs_err_deg": 1.5657910108566284,
  "theta_abs_le_8_bias_deg": 0.1288953423500061,
  "theta_abs_le_8_n": 4344.0,
  "theta_abs_le_10_mae_deg": 0.5171917080879211,
  "theta_abs_le_10_rmse_deg": 0.7444486021995544,
  "theta_abs_le_10_p95_abs_err_deg": 1.5657910108566284,
  "theta_abs_le_10_bias_deg": 0.1288953423500061,
  "theta_abs_le_10_n": 4344.0,
  "theta_pos_6_8_mae_deg": 0.978520929813385,
  "theta_pos_6_8_rmse_deg": 1.1768431663513184,
  "theta_pos_6_8_p95_abs_err_deg": 2.3618855476379395,
  "theta_pos_6_8_bias_deg": -0.9311719536781311,
  "theta_pos_6_8_n": 414.0,
  "theta_neg_8_6_mae_deg": 0.5112130045890808,
  "theta_neg_8_6_rmse_deg": 0.7070782780647278,
  "theta_neg_8_6_p95_abs_err_deg": 1.4397540092468262,
  "theta_neg_8_6_bias_deg": 0.45101699233055115,
  "theta_neg_8_6_n": 331.0
}
```
