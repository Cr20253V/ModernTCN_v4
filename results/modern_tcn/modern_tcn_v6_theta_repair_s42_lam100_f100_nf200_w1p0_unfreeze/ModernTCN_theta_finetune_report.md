# ModernTCN theta-head fine-tune report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_longrun_diag2steer_seed42\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 10
- train seconds: 44.4

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
| acc_main | 0.9767 |
| acc_turn | 0.9355 |
| acc_turn_transition | 0.6237 |
| turn_left_recall | 0.8682 |
| theta_mae_deg | 0.9055 |
| theta_abs_le_8_mae_deg | 0.9055 |
| theta_abs_le_10_mae_deg | 0.9055 |
| theta_pos_6_8_mae_deg | 0.7399 |
| theta_pos_6_8_bias_deg | 0.0762 |
| theta_neg_8_6_mae_deg | 0.9995 |
| theta_neg_8_6_bias_deg | 0.9362 |
| theta_flat_abs_p95_deg | 3.9650 |
| theta_flat_bias_deg | 0.0765 |
| theta_near_flat_abs_p95_deg | 4.1157 |
| theta_near_flat_bias_deg | 0.1064 |
| theta_flat_turn_abs_p95_deg | 2.3630 |
| flat_recall | 0.9947 |
| slope_recall | 0.9397 |
| slope_sign_acc | 0.3261 |

## Validation Best Metrics

```json
{
  "loss_total": 0.44725168022516404,
  "acc_main": 0.9742163801820021,
  "acc_turn": 0.929726996966633,
  "acc_turn_pure": 0.9502141327623126,
  "acc_turn_transition": 0.5818181818181818,
  "flat_recall": 0.9938608458390177,
  "stall_recall": 0.8939393939393939,
  "slope_recall": 0.92152466367713,
  "recall_main": [
    0.9938608458390177,
    0.8939393939393939,
    0.92152466367713
  ],
  "turn_right_recall": 0.9093484419263456,
  "turn_straight_recall": 0.9511568123393316,
  "turn_left_recall": 0.8908296943231441,
  "recall_turn": [
    0.9093484419263456,
    0.9511568123393316,
    0.8908296943231441
  ],
  "cm_turn": [
    [
      321,
      19,
      13
    ],
    [
      36,
      1110,
      21
    ],
    [
      2,
      48,
      408
    ]
  ],
  "n_turn_transition": 110,
  "n_turn_pure": 1868,
  "cm_main": [
    [
      1457,
      3,
      6
    ],
    [
      5,
      59,
      2
    ],
    [
      35,
      0,
      411
    ]
  ],
  "main_confidence_mean": 0.9960142011651076,
  "main_confidence_error_mean": 0.9623280216585549,
  "main_low_conf_0p60_ratio": 0.0010111223458038423,
  "main_low_conf_0p70_ratio": 0.00455005055611729,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 2,
      "error_rate": 0.0,
      "mean_confidence": 0.5968769123127575
    },
    {
      "bin": "[0.60,0.70)",
      "n": 7,
      "error_rate": 0.2857142857142857,
      "mean_confidence": 0.6464924888795708
    },
    {
      "bin": "[0.70,0.80)",
      "n": 1,
      "error_rate": 0.0,
      "mean_confidence": 0.757854133357907
    },
    {
      "bin": "[0.80,0.90)",
      "n": 14,
      "error_rate": 0.2857142857142857,
      "mean_confidence": 0.8623808681469407
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1954,
      "error_rate": 0.02302968270214944,
      "mean_confidence": 0.9987541977330529
    }
  ],
  "turn_confidence_mean": 0.9527585389385397,
  "turn_confidence_error_mean": 0.8497408989470798,
  "turn_low_conf_0p60_ratio": 0.01820020222446916,
  "turn_low_conf_0p70_ratio": 0.03943377148634985,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 36,
      "error_rate": 0.4722222222222222,
      "mean_confidence": 0.5389603937834971
    },
    {
      "bin": "[0.60,0.70)",
      "n": 42,
      "error_rate": 0.2619047619047619,
      "mean_confidence": 0.6543305118277283
    },
    {
      "bin": "[0.70,0.80)",
      "n": 80,
      "error_rate": 0.1875,
      "mean_confidence": 0.7461417936184201
    },
    {
      "bin": "[0.80,0.90)",
      "n": 161,
      "error_rate": 0.17391304347826086,
      "mean_confidence": 0.8638093857470078
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1659,
      "error_rate": 0.040988547317661245,
      "mean_confidence": 0.9878886556677028
    }
  ],
  "theta_mae_rad": 0.014786875806748867,
  "theta_mae_deg": 0.847225546836853,
  "uphill_recall": 0.8464163822525598,
  "downhill_recall": 0.690677966101695,
  "slope_sign_acc": 0.24947698744769875,
  "theta_flat_mae_deg": 0.7295368909835815,
  "theta_flat_abs_p95_deg": 3.1339759826660156,
  "theta_flat_bias_deg": 0.12348339706659317,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.7498061656951904,
  "theta_near_flat_abs_p95_deg": 3.2117226123809814,
  "theta_near_flat_bias_deg": 0.14345605671405792,
  "theta_near_flat_n": 1472.0,
  "theta_flat_turn_mae_deg": 0.6788042187690735,
  "theta_flat_turn_abs_p95_deg": 2.3685758113861084,
  "theta_flat_turn_bias_deg": 0.26053547859191895,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.847225546836853,
  "theta_slope_control_abs_p95_deg": 5.7575531005859375,
  "theta_slope_control_bias_deg": 0.301040381193161,
  "theta_slope_control_n": 1912.0,
  "theta_abs_le_8_mae_deg": 0.8472254872322083,
  "theta_abs_le_8_rmse_deg": 1.6454271078109741,
  "theta_abs_le_8_p95_abs_err_deg": 3.392235279083252,
  "theta_abs_le_8_bias_deg": 0.3010403513908386,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.8472254872322083,
  "theta_abs_le_10_rmse_deg": 1.6454271078109741,
  "theta_abs_le_10_p95_abs_err_deg": 3.392235279083252,
  "theta_abs_le_10_bias_deg": 0.3010403513908386,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.7638969421386719,
  "theta_pos_6_8_rmse_deg": 0.9403761625289917,
  "theta_pos_6_8_p95_abs_err_deg": 1.5064494609832764,
  "theta_pos_6_8_bias_deg": -0.6092404127120972,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 1.0279510021209717,
  "theta_neg_8_6_rmse_deg": 1.181220531463623,
  "theta_neg_8_6_p95_abs_err_deg": 1.94573974609375,
  "theta_neg_8_6_bias_deg": 0.9538483023643494,
  "theta_neg_8_6_n": 47.0
}
```
