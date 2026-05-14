# ModernTCN theta-head fine-tune report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_longrun_diag2steer_seed42\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 5
- train seconds: 35.4

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
  "select_theta_flat_p95_weight": 2.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 1.0,
  "select_theta_flat_bias_target_deg": 0.2
}
```

## Test Metrics

| metric | value |
|---|---:|
| acc_main | 0.9752 |
| acc_turn | 0.9345 |
| acc_turn_transition | 0.6344 |
| turn_left_recall | 0.8708 |
| theta_mae_deg | 1.3560 |
| theta_abs_le_8_mae_deg | 1.3560 |
| theta_abs_le_10_mae_deg | 1.3560 |
| theta_pos_6_8_mae_deg | 0.8135 |
| theta_pos_6_8_bias_deg | -0.5882 |
| theta_neg_8_6_mae_deg | 0.4936 |
| theta_neg_8_6_bias_deg | -0.1260 |
| theta_flat_abs_p95_deg | 5.5191 |
| theta_flat_bias_deg | -0.0037 |
| theta_near_flat_abs_p95_deg | 6.4300 |
| theta_near_flat_bias_deg | -0.0066 |
| theta_flat_turn_abs_p95_deg | 3.2372 |
| flat_recall | 0.9924 |
| slope_recall | 0.9416 |
| slope_sign_acc | 0.3299 |

## Validation Best Metrics

```json
{
  "loss_total": 0.44529654011808345,
  "acc_main": 0.9732052578361982,
  "acc_turn": 0.9307381193124368,
  "acc_turn_pure": 0.952355460385439,
  "acc_turn_transition": 0.5636363636363636,
  "flat_recall": 0.9918144611186903,
  "stall_recall": 0.8939393939393939,
  "slope_recall": 0.9237668161434978,
  "recall_main": [
    0.9918144611186903,
    0.8939393939393939,
    0.9237668161434978
  ],
  "turn_right_recall": 0.9150141643059491,
  "turn_straight_recall": 0.9485861182519281,
  "turn_left_recall": 0.8973799126637555,
  "recall_turn": [
    0.9150141643059491,
    0.9485861182519281,
    0.8973799126637555
  ],
  "cm_turn": [
    [
      323,
      17,
      13
    ],
    [
      38,
      1107,
      22
    ],
    [
      0,
      47,
      411
    ]
  ],
  "n_turn_transition": 110,
  "n_turn_pure": 1868,
  "cm_main": [
    [
      1454,
      3,
      9
    ],
    [
      5,
      59,
      2
    ],
    [
      34,
      0,
      412
    ]
  ],
  "main_confidence_mean": 0.9949896138572175,
  "main_confidence_error_mean": 0.9469408065352681,
  "main_low_conf_0p60_ratio": 0.0025278058645096056,
  "main_low_conf_0p70_ratio": 0.004044489383215369,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 5,
      "error_rate": 0.2,
      "mean_confidence": 0.514502939697375
    },
    {
      "bin": "[0.60,0.70)",
      "n": 3,
      "error_rate": 1.0,
      "mean_confidence": 0.6555869714573398
    },
    {
      "bin": "[0.70,0.80)",
      "n": 7,
      "error_rate": 0.14285714285714285,
      "mean_confidence": 0.7568760966895741
    },
    {
      "bin": "[0.80,0.90)",
      "n": 11,
      "error_rate": 0.36363636363636365,
      "mean_confidence": 0.8563741272010025
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1952,
      "error_rate": 0.022540983606557378,
      "mean_confidence": 0.9983770146110037
    }
  ],
  "turn_confidence_mean": 0.9547234995362082,
  "turn_confidence_error_mean": 0.8609506947861049,
  "turn_low_conf_0p60_ratio": 0.017189079878665317,
  "turn_low_conf_0p70_ratio": 0.036905965621840245,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 34,
      "error_rate": 0.38235294117647056,
      "mean_confidence": 0.5446110591465864
    },
    {
      "bin": "[0.60,0.70)",
      "n": 39,
      "error_rate": 0.23076923076923078,
      "mean_confidence": 0.6502074772498119
    },
    {
      "bin": "[0.70,0.80)",
      "n": 74,
      "error_rate": 0.24324324324324326,
      "mean_confidence": 0.7446686958691228
    },
    {
      "bin": "[0.80,0.90)",
      "n": 142,
      "error_rate": 0.16901408450704225,
      "mean_confidence": 0.8607670825168
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1689,
      "error_rate": 0.04322084073416223,
      "mean_confidence": 0.9871129693589061
    }
  ],
  "theta_mae_rad": 0.021787740290164948,
  "theta_mae_deg": 1.2483454942703247,
  "uphill_recall": 0.8532423208191127,
  "downhill_recall": 0.690677966101695,
  "slope_sign_acc": 0.2567991631799163,
  "theta_flat_mae_deg": 1.3400307893753052,
  "theta_flat_abs_p95_deg": 3.666827440261841,
  "theta_flat_bias_deg": 0.29057055711746216,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 1.357430100440979,
  "theta_near_flat_abs_p95_deg": 3.736727476119995,
  "theta_near_flat_bias_deg": 0.3119542598724365,
  "theta_near_flat_n": 1472.0,
  "theta_flat_turn_mae_deg": 1.2159281969070435,
  "theta_flat_turn_abs_p95_deg": 2.894573450088501,
  "theta_flat_turn_bias_deg": 0.40442273020744324,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 1.2483454942703247,
  "theta_slope_control_abs_p95_deg": 6.093288898468018,
  "theta_slope_control_bias_deg": 0.2359219193458557,
  "theta_slope_control_n": 1912.0,
  "theta_abs_le_8_mae_deg": 1.2483453750610352,
  "theta_abs_le_8_rmse_deg": 2.3522026538848877,
  "theta_abs_le_8_p95_abs_err_deg": 3.2271080017089844,
  "theta_abs_le_8_bias_deg": 0.2359219193458557,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 1.2483453750610352,
  "theta_abs_le_10_rmse_deg": 2.3522026538848877,
  "theta_abs_le_10_p95_abs_err_deg": 3.2271080017089844,
  "theta_abs_le_10_bias_deg": 0.2359219193458557,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.8619638085365295,
  "theta_pos_6_8_rmse_deg": 1.075112223625183,
  "theta_pos_6_8_p95_abs_err_deg": 2.0399625301361084,
  "theta_pos_6_8_bias_deg": -0.7275651693344116,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.5051664113998413,
  "theta_neg_8_6_rmse_deg": 0.7767956256866455,
  "theta_neg_8_6_p95_abs_err_deg": 1.8344545364379883,
  "theta_neg_8_6_bias_deg": -0.1203220784664154,
  "theta_neg_8_6_n": 47.0
}
```
