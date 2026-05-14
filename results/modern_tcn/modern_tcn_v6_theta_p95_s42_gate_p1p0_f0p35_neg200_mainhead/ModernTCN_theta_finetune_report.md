# ModernTCN theta-head fine-tune report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 10
- train seconds: 65.1

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
  "lambda_theta_flat": 2.0,
  "lambda_theta_near_flat": 6.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 20.0,
  "lambda_theta_flat_excess": 220.0,
  "lambda_theta_near_flat_excess": 260.0,
  "lambda_theta_true_zero_excess": 320.0,
  "lambda_theta_active_excess": 80.0,
  "lambda_theta_small_neg": 20.0,
  "lambda_theta_small_neg_excess": 200.0,
  "theta_excess_target_deg": 1.0,
  "theta_flat_excess_target_deg": 0.45,
  "theta_true_zero_tol_deg": 0.0001,
  "theta_small_neg_min_deg": -4.0,
  "theta_small_neg_max_deg": -2.0,
  "theta_gate_mode": "main_slope_prob",
  "theta_gate_power": 1.0,
  "theta_gate_floor": 0.35,
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
  "theta_neg_weight": 1.6,
  "theta_pos_weight": 1.1,
  "turn_transition_weight": 1.0,
  "select_turn_weight": 0.3,
  "select_turn_transition_weight": 1.0,
  "select_turn_transition_target": 0.75,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.8,
  "select_theta_weight": 0.7,
  "select_theta_ref_deg": 1.0,
  "select_theta_p95_weight": 10.0,
  "select_theta_p95_target_deg": 1.0,
  "select_theta_flat_p95_weight": 12.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_near_flat_p95_weight": 12.0,
  "select_theta_near_flat_p95_target_deg": 1.0,
  "select_theta_true_zero_p95_weight": 12.0,
  "select_theta_true_zero_p95_target_deg": 1.0,
  "select_theta_flat_peak_weight": 3.0,
  "select_theta_flat_peak_target_deg": 3.0,
  "select_theta_small_neg_p95_weight": 6.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 1.0,
  "select_theta_flat_bias_target_deg": 0.2
}
```

## Test Metrics

| metric | value |
|---|---:|
| acc_main | 0.9773 |
| acc_turn | 0.9376 |
| acc_turn_transition | 0.6667 |
| turn_left_recall | 0.8734 |
| theta_mae_deg | 0.4404 |
| theta_abs_le_8_mae_deg | 0.4404 |
| theta_abs_le_8_p95_abs_err_deg | 1.4058 |
| theta_abs_le_8_max_abs_err_deg | 5.1649 |
| theta_abs_le_10_mae_deg | 0.4404 |
| theta_abs_le_10_p95_abs_err_deg | 1.4058 |
| theta_pos_6_8_mae_deg | 0.6330 |
| theta_pos_6_8_p95_abs_err_deg | 1.5915 |
| theta_pos_6_8_bias_deg | 0.0345 |
| theta_neg_8_6_mae_deg | 0.4098 |
| theta_neg_8_6_p95_abs_err_deg | 1.0715 |
| theta_neg_8_6_bias_deg | -0.1275 |
| theta_active_abs_ge_2_mae_deg | 0.6018 |
| theta_active_abs_ge_2_p95_abs_err_deg | 2.1381 |
| theta_neg_4_2_mae_deg | 1.2558 |
| theta_neg_4_2_p95_abs_err_deg | 3.0954 |
| theta_neg_4_2_bias_deg | 0.6210 |
| theta_flat_abs_p95_deg | 1.1223 |
| theta_flat_abs_max_deg | 2.8551 |
| theta_flat_bias_deg | -0.2611 |
| theta_near_flat_abs_p95_deg | 1.1339 |
| theta_near_flat_abs_max_deg | 2.9871 |
| theta_near_flat_bias_deg | -0.2502 |
| theta_true_zero_abs_p95_deg | 1.1355 |
| theta_true_zero_abs_max_deg | 2.9871 |
| theta_true_zero_bias_deg | -0.2505 |
| theta_flat_turn_abs_p95_deg | 0.9002 |
| flat_recall | 0.9947 |
| slope_recall | 0.9435 |
| slope_sign_acc | 0.3239 |

## Validation Best Metrics

```json
{
  "loss_total": 0.661796503047731,
  "acc_main": 0.9737108190091001,
  "acc_turn": 0.9332659251769464,
  "acc_turn_pure": 0.9534261241970021,
  "acc_turn_transition": 0.5909090909090909,
  "flat_recall": 0.9938608458390177,
  "stall_recall": 0.8787878787878788,
  "slope_recall": 0.92152466367713,
  "recall_main": [
    0.9938608458390177,
    0.8787878787878788,
    0.92152466367713
  ],
  "turn_right_recall": 0.9263456090651558,
  "turn_straight_recall": 0.9528706083976007,
  "turn_left_recall": 0.888646288209607,
  "recall_turn": [
    0.9263456090651558,
    0.9528706083976007,
    0.888646288209607
  ],
  "cm_turn": [
    [
      327,
      17,
      9
    ],
    [
      37,
      1112,
      18
    ],
    [
      1,
      50,
      407
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
      58,
      3
    ],
    [
      35,
      0,
      411
    ]
  ],
  "main_confidence_mean": 0.997909342236772,
  "main_confidence_error_mean": 0.977087382232092,
  "main_low_conf_0p60_ratio": 0.0005055611729019212,
  "main_low_conf_0p70_ratio": 0.0015166835187057635,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 1,
      "error_rate": 0.0,
      "mean_confidence": 0.5892623481310217
    },
    {
      "bin": "[0.60,0.70)",
      "n": 2,
      "error_rate": 0.5,
      "mean_confidence": 0.6719652311445223
    },
    {
      "bin": "[0.70,0.80)",
      "n": 3,
      "error_rate": 0.0,
      "mean_confidence": 0.7347417656708902
    },
    {
      "bin": "[0.80,0.90)",
      "n": 8,
      "error_rate": 0.375,
      "mean_confidence": 0.8510616735500836
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1964,
      "error_rate": 0.024439918533604887,
      "mean_confidence": 0.9994494742609477
    }
  ],
  "turn_confidence_mean": 0.9533067091990447,
  "turn_confidence_error_mean": 0.8517130253617191,
  "turn_low_conf_0p60_ratio": 0.023761375126390292,
  "turn_low_conf_0p70_ratio": 0.052072800808897875,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 47,
      "error_rate": 0.23404255319148937,
      "mean_confidence": 0.5438605564177396
    },
    {
      "bin": "[0.60,0.70)",
      "n": 56,
      "error_rate": 0.3392857142857143,
      "mean_confidence": 0.6612779181386496
    },
    {
      "bin": "[0.70,0.80)",
      "n": 67,
      "error_rate": 0.19402985074626866,
      "mean_confidence": 0.7529634509451412
    },
    {
      "bin": "[0.80,0.90)",
      "n": 119,
      "error_rate": 0.13445378151260504,
      "mean_confidence": 0.8571396002702195
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1689,
      "error_rate": 0.04322084073416223,
      "mean_confidence": 0.9891056824054657
    }
  ],
  "theta_mae_rad": 0.0079667242243886,
  "theta_mae_deg": 0.456459641456604,
  "uphill_recall": 0.8498293515358362,
  "downhill_recall": 0.6864406779661016,
  "slope_sign_acc": 0.25784518828451886,
  "theta_flat_mae_deg": 0.36036214232444763,
  "theta_flat_abs_p95_deg": 0.9318779110908508,
  "theta_flat_abs_max_deg": 4.158724784851074,
  "theta_flat_bias_deg": -0.2708395719528198,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.3502257168292999,
  "theta_near_flat_abs_p95_deg": 0.9808545708656311,
  "theta_near_flat_abs_max_deg": 4.684220314025879,
  "theta_near_flat_bias_deg": -0.2636471092700958,
  "theta_near_flat_n": 1472.0,
  "theta_true_zero_mae_deg": 0.34606990218162537,
  "theta_true_zero_abs_p95_deg": 0.9639895558357239,
  "theta_true_zero_abs_max_deg": 4.684220314025879,
  "theta_true_zero_bias_deg": -0.2582765221595764,
  "theta_true_zero_n": 1433.0,
  "theta_flat_turn_mae_deg": 0.28061527013778687,
  "theta_flat_turn_abs_p95_deg": 0.6867586970329285,
  "theta_flat_turn_abs_max_deg": 2.3504955768585205,
  "theta_flat_turn_bias_deg": -0.20921200513839722,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.456459641456604,
  "theta_slope_control_abs_p95_deg": 5.645761966705322,
  "theta_slope_control_abs_max_deg": 8.27857780456543,
  "theta_slope_control_bias_deg": -0.2057238221168518,
  "theta_slope_control_n": 1912.0,
  "theta_all_mae_deg": 0.456459641456604,
  "theta_all_rmse_deg": 0.694697380065918,
  "theta_all_p95_abs_err_deg": 1.4030214548110962,
  "theta_all_max_abs_err_deg": 4.294521331787109,
  "theta_all_bias_deg": -0.2057238072156906,
  "theta_all_n": 1912.0,
  "theta_active_abs_ge_2_mae_deg": 0.7723317742347717,
  "theta_active_abs_ge_2_rmse_deg": 1.0557453632354736,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2075445652008057,
  "theta_active_abs_ge_2_max_abs_err_deg": 4.294521331787109,
  "theta_active_abs_ge_2_bias_deg": 0.008311431854963303,
  "theta_active_abs_ge_2_n": 446.0,
  "theta_abs_le_8_mae_deg": 0.456459641456604,
  "theta_abs_le_8_rmse_deg": 0.694697380065918,
  "theta_abs_le_8_p95_abs_err_deg": 1.4030214548110962,
  "theta_abs_le_8_max_abs_err_deg": 4.294521331787109,
  "theta_abs_le_8_bias_deg": -0.2057238072156906,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.456459641456604,
  "theta_abs_le_10_rmse_deg": 0.694697380065918,
  "theta_abs_le_10_p95_abs_err_deg": 1.4030214548110962,
  "theta_abs_le_10_max_abs_err_deg": 4.294521331787109,
  "theta_abs_le_10_bias_deg": -0.2057238072156906,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.718243420124054,
  "theta_pos_6_8_rmse_deg": 0.822664737701416,
  "theta_pos_6_8_p95_abs_err_deg": 1.208614468574524,
  "theta_pos_6_8_max_abs_err_deg": 2.656254529953003,
  "theta_pos_6_8_bias_deg": -0.5706748366355896,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.40461763739585876,
  "theta_neg_8_6_rmse_deg": 0.5465521812438965,
  "theta_neg_8_6_p95_abs_err_deg": 1.084913730621338,
  "theta_neg_8_6_max_abs_err_deg": 1.4553577899932861,
  "theta_neg_8_6_bias_deg": -0.16591615974903107,
  "theta_neg_8_6_n": 47.0,
  "theta_neg_4_2_mae_deg": 1.0784683227539062,
  "theta_neg_4_2_rmse_deg": 1.424608588218689,
  "theta_neg_4_2_p95_abs_err_deg": 2.911975622177124,
  "theta_neg_4_2_max_abs_err_deg": 4.294521331787109,
  "theta_neg_4_2_bias_deg": 0.34989532828330994,
  "theta_neg_4_2_n": 145.0
}
```
