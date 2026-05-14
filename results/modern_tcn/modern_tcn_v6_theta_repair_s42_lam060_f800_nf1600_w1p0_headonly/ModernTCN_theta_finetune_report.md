# ModernTCN theta-head fine-tune report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_longrun_diag2steer_seed42\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 110
- train seconds: 169.1

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
  "lambda_turn": 0.05,
  "lambda_theta": 0.6,
  "lambda_theta_flat": 8.0,
  "lambda_theta_near_flat": 16.0,
  "theta_near_flat_deg": 0.5,
  "main_class_multipliers": [
    1.2,
    1.0,
    0.95
  ],
  "turn_class_multipliers": [
    1.0,
    1.0,
    1.0
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 1.0,
  "select_turn_weight": 0.3,
  "select_turn_transition_weight": 1.0,
  "select_turn_transition_target": 0.75,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.8,
  "select_theta_weight": 0.7,
  "select_theta_ref_deg": 1.0,
  "select_theta_flat_p95_weight": 5.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 2.0,
  "select_theta_flat_bias_target_deg": 0.2
}
```

## Test Metrics

| metric | value |
|---|---:|
| acc_main | 0.9778 |
| acc_turn | 0.9334 |
| acc_turn_transition | 0.6344 |
| turn_left_recall | 0.8630 |
| theta_mae_deg | 0.7620 |
| theta_abs_le_8_mae_deg | 0.7620 |
| theta_abs_le_10_mae_deg | 0.7620 |
| theta_pos_6_8_mae_deg | 3.6128 |
| theta_pos_6_8_bias_deg | -3.6128 |
| theta_neg_8_6_mae_deg | 0.6672 |
| theta_neg_8_6_bias_deg | 0.5475 |
| theta_flat_abs_p95_deg | 1.7540 |
| theta_flat_bias_deg | -0.0626 |
| theta_near_flat_abs_p95_deg | 1.9903 |
| theta_near_flat_bias_deg | -0.0511 |
| theta_flat_turn_abs_p95_deg | 1.4325 |
| flat_recall | 0.9908 |
| slope_recall | 0.9529 |
| slope_sign_acc | 0.3201 |

## Validation Best Metrics

```json
{
  "loss_total": 0.33465714278066844,
  "acc_main": 0.9772497472194136,
  "acc_turn": 0.9292214357937311,
  "acc_turn_pure": 0.949678800856531,
  "acc_turn_transition": 0.5818181818181818,
  "flat_recall": 0.9924965893587995,
  "stall_recall": 0.8939393939393939,
  "slope_recall": 0.9394618834080718,
  "recall_main": [
    0.9924965893587995,
    0.8939393939393939,
    0.9394618834080718
  ],
  "turn_right_recall": 0.9235127478753541,
  "turn_straight_recall": 0.9502999143101971,
  "turn_left_recall": 0.8799126637554585,
  "recall_turn": [
    0.9235127478753541,
    0.9502999143101971,
    0.8799126637554585
  ],
  "cm_turn": [
    [
      326,
      16,
      11
    ],
    [
      41,
      1109,
      17
    ],
    [
      4,
      51,
      403
    ]
  ],
  "n_turn_transition": 110,
  "n_turn_pure": 1868,
  "cm_main": [
    [
      1455,
      3,
      8
    ],
    [
      5,
      59,
      2
    ],
    [
      27,
      0,
      419
    ]
  ],
  "main_confidence_mean": 0.9947603096777267,
  "main_confidence_error_mean": 0.9330638335287249,
  "main_low_conf_0p60_ratio": 0.0025278058645096056,
  "main_low_conf_0p70_ratio": 0.00455005055611729,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 5,
      "error_rate": 0.2,
      "mean_confidence": 0.4962799581816709
    },
    {
      "bin": "[0.60,0.70)",
      "n": 4,
      "error_rate": 0.5,
      "mean_confidence": 0.663867458310124
    },
    {
      "bin": "[0.70,0.80)",
      "n": 8,
      "error_rate": 0.5,
      "mean_confidence": 0.7604079528524142
    },
    {
      "bin": "[0.80,0.90)",
      "n": 15,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.8574464482269416
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1946,
      "error_rate": 0.01695786228160329,
      "mean_confidence": 0.9987430948469533
    }
  ],
  "turn_confidence_mean": 0.9531343225830688,
  "turn_confidence_error_mean": 0.8471502427005299,
  "turn_low_conf_0p60_ratio": 0.01870576339737108,
  "turn_low_conf_0p70_ratio": 0.03741152679474216,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 37,
      "error_rate": 0.43243243243243246,
      "mean_confidence": 0.5335223696027127
    },
    {
      "bin": "[0.60,0.70)",
      "n": 37,
      "error_rate": 0.35135135135135137,
      "mean_confidence": 0.6581468671899707
    },
    {
      "bin": "[0.70,0.80)",
      "n": 100,
      "error_rate": 0.15,
      "mean_confidence": 0.7600573415029923
    },
    {
      "bin": "[0.80,0.90)",
      "n": 130,
      "error_rate": 0.17692307692307693,
      "mean_confidence": 0.8588424650569054
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1674,
      "error_rate": 0.04360812425328554,
      "mean_confidence": 0.987785348685952
    }
  ],
  "theta_mae_rad": 0.012448049150407314,
  "theta_mae_deg": 0.7132206559181213,
  "uphill_recall": 0.8498293515358362,
  "downhill_recall": 0.7245762711864406,
  "slope_sign_acc": 0.25889121338912136,
  "theta_flat_mae_deg": 0.39738622307777405,
  "theta_flat_abs_p95_deg": 1.4478915929794312,
  "theta_flat_bias_deg": -0.05208840221166611,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.4027523398399353,
  "theta_near_flat_abs_p95_deg": 1.5953699350357056,
  "theta_near_flat_bias_deg": -0.036528170108795166,
  "theta_near_flat_n": 1472.0,
  "theta_flat_turn_mae_deg": 0.39787986874580383,
  "theta_flat_turn_abs_p95_deg": 1.2342424392700195,
  "theta_flat_turn_bias_deg": -0.022889981046319008,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.7132206559181213,
  "theta_slope_control_abs_p95_deg": 4.092839241027832,
  "theta_slope_control_bias_deg": -0.23310540616512299,
  "theta_slope_control_n": 1912.0,
  "theta_abs_le_8_mae_deg": 0.7132206559181213,
  "theta_abs_le_8_rmse_deg": 1.2553209066390991,
  "theta_abs_le_8_p95_abs_err_deg": 2.93094539642334,
  "theta_abs_le_8_bias_deg": -0.2331053912639618,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.7132206559181213,
  "theta_abs_le_10_rmse_deg": 1.2553209066390991,
  "theta_abs_le_10_p95_abs_err_deg": 2.93094539642334,
  "theta_abs_le_10_bias_deg": -0.2331053912639618,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 2.6645302772521973,
  "theta_pos_6_8_rmse_deg": 2.7240781784057617,
  "theta_pos_6_8_p95_abs_err_deg": 3.3477983474731445,
  "theta_pos_6_8_bias_deg": -2.6645302772521973,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.7000546455383301,
  "theta_neg_8_6_rmse_deg": 0.8210071921348572,
  "theta_neg_8_6_p95_abs_err_deg": 1.2683240175247192,
  "theta_neg_8_6_bias_deg": 0.5610072016716003,
  "theta_neg_8_6_n": 47.0
}
```
