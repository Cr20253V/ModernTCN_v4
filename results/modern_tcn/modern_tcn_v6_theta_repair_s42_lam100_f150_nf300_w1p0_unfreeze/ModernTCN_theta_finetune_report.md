# ModernTCN theta-head fine-tune report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_longrun_diag2steer_seed42\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 81
- train seconds: 157.4

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
  "lambda_theta_flat": 1.5,
  "lambda_theta_near_flat": 3.0,
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
| acc_main | 0.9783 |
| acc_turn | 0.9392 |
| acc_turn_transition | 0.6882 |
| turn_left_recall | 0.8734 |
| theta_mae_deg | 0.4717 |
| theta_abs_le_8_mae_deg | 0.4717 |
| theta_abs_le_10_mae_deg | 0.4717 |
| theta_pos_6_8_mae_deg | 0.5227 |
| theta_pos_6_8_bias_deg | -0.0349 |
| theta_neg_8_6_mae_deg | 0.5320 |
| theta_neg_8_6_bias_deg | 0.4696 |
| theta_flat_abs_p95_deg | 1.9229 |
| theta_flat_bias_deg | -0.1025 |
| theta_near_flat_abs_p95_deg | 2.0810 |
| theta_near_flat_bias_deg | -0.0748 |
| theta_flat_turn_abs_p95_deg | 1.6389 |
| flat_recall | 0.9947 |
| slope_recall | 0.9454 |
| slope_sign_acc | 0.3277 |

## Validation Best Metrics

```json
{
  "loss_total": 0.5705957126147344,
  "acc_main": 0.974721941354904,
  "acc_turn": 0.9337714863498483,
  "acc_turn_pure": 0.9507494646680942,
  "acc_turn_transition": 0.6454545454545455,
  "flat_recall": 0.9938608458390177,
  "stall_recall": 0.8636363636363636,
  "slope_recall": 0.9282511210762332,
  "recall_main": [
    0.9938608458390177,
    0.8636363636363636,
    0.9282511210762332
  ],
  "turn_right_recall": 0.9065155807365439,
  "turn_straight_recall": 0.9580119965724079,
  "turn_left_recall": 0.8930131004366813,
  "recall_turn": [
    0.9065155807365439,
    0.9580119965724079,
    0.8930131004366813
  ],
  "cm_turn": [
    [
      320,
      23,
      10
    ],
    [
      32,
      1118,
      17
    ],
    [
      1,
      48,
      409
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
      57,
      4
    ],
    [
      32,
      0,
      414
    ]
  ],
  "main_confidence_mean": 0.99788316601983,
  "main_confidence_error_mean": 0.9735467872965028,
  "main_low_conf_0p60_ratio": 0.0010111223458038423,
  "main_low_conf_0p70_ratio": 0.0020222446916076846,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 2,
      "error_rate": 0.0,
      "mean_confidence": 0.5720034900779067
    },
    {
      "bin": "[0.60,0.70)",
      "n": 2,
      "error_rate": 0.5,
      "mean_confidence": 0.6400716152109416
    },
    {
      "bin": "[0.70,0.80)",
      "n": 5,
      "error_rate": 0.4,
      "mean_confidence": 0.7456974113197394
    },
    {
      "bin": "[0.80,0.90)",
      "n": 2,
      "error_rate": 0.5,
      "mean_confidence": 0.8641739928057535
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1967,
      "error_rate": 0.02338586680223691,
      "mean_confidence": 0.9994569990515686
    }
  ],
  "turn_confidence_mean": 0.9582648896107842,
  "turn_confidence_error_mean": 0.8524646447115406,
  "turn_low_conf_0p60_ratio": 0.017189079878665317,
  "turn_low_conf_0p70_ratio": 0.036905965621840245,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 34,
      "error_rate": 0.4411764705882353,
      "mean_confidence": 0.5403055731815843
    },
    {
      "bin": "[0.60,0.70)",
      "n": 39,
      "error_rate": 0.38461538461538464,
      "mean_confidence": 0.6525002320387391
    },
    {
      "bin": "[0.70,0.80)",
      "n": 70,
      "error_rate": 0.14285714285714285,
      "mean_confidence": 0.74435948964667
    },
    {
      "bin": "[0.80,0.90)",
      "n": 122,
      "error_rate": 0.14754098360655737,
      "mean_confidence": 0.8602082640800256
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1713,
      "error_rate": 0.04261529480443666,
      "mean_confidence": 0.9892466320019943
    }
  ],
  "theta_mae_rad": 0.008176113478839397,
  "theta_mae_deg": 0.46845677495002747,
  "uphill_recall": 0.8498293515358362,
  "downhill_recall": 0.6991525423728814,
  "slope_sign_acc": 0.25732217573221755,
  "theta_flat_mae_deg": 0.4055728614330292,
  "theta_flat_abs_p95_deg": 1.6374026536941528,
  "theta_flat_bias_deg": -0.13866403698921204,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.4159298539161682,
  "theta_near_flat_abs_p95_deg": 1.711719274520874,
  "theta_near_flat_bias_deg": -0.11302576214075089,
  "theta_near_flat_n": 1472.0,
  "theta_flat_turn_mae_deg": 0.4019569754600525,
  "theta_flat_turn_abs_p95_deg": 1.4340476989746094,
  "theta_flat_turn_bias_deg": -0.16856518387794495,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.46845677495002747,
  "theta_slope_control_abs_p95_deg": 5.613492488861084,
  "theta_slope_control_bias_deg": -0.04433481767773628,
  "theta_slope_control_n": 1912.0,
  "theta_abs_le_8_mae_deg": 0.46845680475234985,
  "theta_abs_le_8_rmse_deg": 1.0374163389205933,
  "theta_abs_le_8_p95_abs_err_deg": 1.9022178649902344,
  "theta_abs_le_8_bias_deg": -0.044334810227155685,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.46845680475234985,
  "theta_abs_le_10_rmse_deg": 1.0374163389205933,
  "theta_abs_le_10_p95_abs_err_deg": 1.9022178649902344,
  "theta_abs_le_10_bias_deg": -0.044334810227155685,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.7059447765350342,
  "theta_pos_6_8_rmse_deg": 0.9706558585166931,
  "theta_pos_6_8_p95_abs_err_deg": 1.9895415306091309,
  "theta_pos_6_8_bias_deg": -0.4917573034763336,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.4933386445045471,
  "theta_neg_8_6_rmse_deg": 0.5957130193710327,
  "theta_neg_8_6_p95_abs_err_deg": 0.8806172609329224,
  "theta_neg_8_6_bias_deg": 0.42034897208213806,
  "theta_neg_8_6_n": 47.0
}
```
