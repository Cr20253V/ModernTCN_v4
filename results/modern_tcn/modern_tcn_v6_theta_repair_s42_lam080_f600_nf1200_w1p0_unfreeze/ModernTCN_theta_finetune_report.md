# ModernTCN theta-head fine-tune report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_longrun_diag2steer_seed42\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 49
- train seconds: 106.8

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
  "lambda_theta": 0.8,
  "lambda_theta_flat": 6.0,
  "lambda_theta_near_flat": 12.0,
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
| acc_main | 0.9757 |
| acc_turn | 0.9371 |
| acc_turn_transition | 0.6452 |
| turn_left_recall | 0.8708 |
| theta_mae_deg | 0.5942 |
| theta_abs_le_8_mae_deg | 0.5942 |
| theta_abs_le_10_mae_deg | 0.5942 |
| theta_pos_6_8_mae_deg | 1.0329 |
| theta_pos_6_8_bias_deg | -0.9086 |
| theta_neg_8_6_mae_deg | 0.6658 |
| theta_neg_8_6_bias_deg | -0.0552 |
| theta_flat_abs_p95_deg | 2.1139 |
| theta_flat_bias_deg | -0.0412 |
| theta_near_flat_abs_p95_deg | 2.1632 |
| theta_near_flat_bias_deg | -0.0241 |
| theta_flat_turn_abs_p95_deg | 1.7988 |
| flat_recall | 0.9931 |
| slope_recall | 0.9416 |
| slope_sign_acc | 0.3185 |

## Validation Best Metrics

```json
{
  "loss_total": 0.44993973136912463,
  "acc_main": 0.9752275025278059,
  "acc_turn": 0.9317492416582407,
  "acc_turn_pure": 0.9534261241970021,
  "acc_turn_transition": 0.5636363636363636,
  "flat_recall": 0.9938608458390177,
  "stall_recall": 0.8939393939393939,
  "slope_recall": 0.9260089686098655,
  "recall_main": [
    0.9938608458390177,
    0.8939393939393939,
    0.9260089686098655
  ],
  "turn_right_recall": 0.9150141643059491,
  "turn_straight_recall": 0.9502999143101971,
  "turn_left_recall": 0.8973799126637555,
  "recall_turn": [
    0.9150141643059491,
    0.9502999143101971,
    0.8973799126637555
  ],
  "cm_turn": [
    [
      323,
      19,
      11
    ],
    [
      38,
      1109,
      20
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
      33,
      0,
      413
    ]
  ],
  "main_confidence_mean": 0.9963028481143239,
  "main_confidence_error_mean": 0.9404696347898376,
  "main_low_conf_0p60_ratio": 0.0020222446916076846,
  "main_low_conf_0p70_ratio": 0.00455005055611729,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 4,
      "error_rate": 0.75,
      "mean_confidence": 0.5190555725679904
    },
    {
      "bin": "[0.60,0.70)",
      "n": 5,
      "error_rate": 0.4,
      "mean_confidence": 0.6595474606048681
    },
    {
      "bin": "[0.70,0.80)",
      "n": 5,
      "error_rate": 0.0,
      "mean_confidence": 0.7403165563446111
    },
    {
      "bin": "[0.80,0.90)",
      "n": 7,
      "error_rate": 0.42857142857142855,
      "mean_confidence": 0.8595733464570273
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1957,
      "error_rate": 0.020950434338272865,
      "mean_confidence": 0.9992817975318927
    }
  ],
  "turn_confidence_mean": 0.9548726803391405,
  "turn_confidence_error_mean": 0.8455829781458184,
  "turn_low_conf_0p60_ratio": 0.016177957532861477,
  "turn_low_conf_0p70_ratio": 0.03488372093023256,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 32,
      "error_rate": 0.5,
      "mean_confidence": 0.5303058909717664
    },
    {
      "bin": "[0.60,0.70)",
      "n": 37,
      "error_rate": 0.32432432432432434,
      "mean_confidence": 0.6494349680511673
    },
    {
      "bin": "[0.70,0.80)",
      "n": 82,
      "error_rate": 0.1951219512195122,
      "mean_confidence": 0.7471642482816834
    },
    {
      "bin": "[0.80,0.90)",
      "n": 137,
      "error_rate": 0.16058394160583941,
      "mean_confidence": 0.8621470100000176
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1690,
      "error_rate": 0.04082840236686391,
      "mean_confidence": 0.987193887960195
    }
  ],
  "theta_mae_rad": 0.009753328748047352,
  "theta_mae_deg": 0.5588245391845703,
  "uphill_recall": 0.8498293515358362,
  "downhill_recall": 0.6949152542372882,
  "slope_sign_acc": 0.2557531380753138,
  "theta_flat_mae_deg": 0.44555792212486267,
  "theta_flat_abs_p95_deg": 1.6923516988754272,
  "theta_flat_bias_deg": -0.07327615469694138,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.4478098154067993,
  "theta_near_flat_abs_p95_deg": 1.8137106895446777,
  "theta_near_flat_bias_deg": -0.053477391600608826,
  "theta_near_flat_n": 1472.0,
  "theta_flat_turn_mae_deg": 0.4270188510417938,
  "theta_flat_turn_abs_p95_deg": 1.4732110500335693,
  "theta_flat_turn_bias_deg": -0.1459045261144638,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.5588245391845703,
  "theta_slope_control_abs_p95_deg": 5.731823444366455,
  "theta_slope_control_bias_deg": -0.051935259252786636,
  "theta_slope_control_n": 1912.0,
  "theta_abs_le_8_mae_deg": 0.5588245391845703,
  "theta_abs_le_8_rmse_deg": 1.1301881074905396,
  "theta_abs_le_8_p95_abs_err_deg": 2.229076623916626,
  "theta_abs_le_8_bias_deg": -0.05193524435162544,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.5588245391845703,
  "theta_abs_le_10_rmse_deg": 1.1301881074905396,
  "theta_abs_le_10_p95_abs_err_deg": 2.229076623916626,
  "theta_abs_le_10_bias_deg": -0.05193524435162544,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.890911877155304,
  "theta_pos_6_8_rmse_deg": 1.3423268795013428,
  "theta_pos_6_8_p95_abs_err_deg": 3.3783233165740967,
  "theta_pos_6_8_bias_deg": -0.8276419639587402,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.6879867911338806,
  "theta_neg_8_6_rmse_deg": 0.8083342909812927,
  "theta_neg_8_6_p95_abs_err_deg": 1.4776074886322021,
  "theta_neg_8_6_bias_deg": -0.14684449136257172,
  "theta_neg_8_6_n": 47.0
}
```
