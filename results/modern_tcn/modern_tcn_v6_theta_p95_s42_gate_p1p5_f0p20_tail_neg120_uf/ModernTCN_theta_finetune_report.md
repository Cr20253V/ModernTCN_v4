# ModernTCN theta-head fine-tune report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 79
- train seconds: 172.1

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
  "lambda_theta_flat_excess": 140.0,
  "lambda_theta_near_flat_excess": 180.0,
  "lambda_theta_true_zero_excess": 220.0,
  "lambda_theta_active_excess": 55.0,
  "lambda_theta_small_neg": 12.0,
  "lambda_theta_small_neg_excess": 120.0,
  "theta_excess_target_deg": 1.0,
  "theta_flat_excess_target_deg": 0.45,
  "theta_true_zero_tol_deg": 0.0001,
  "theta_small_neg_min_deg": -4.0,
  "theta_small_neg_max_deg": -2.0,
  "theta_gate_mode": "main_slope_prob",
  "theta_gate_power": 1.5,
  "theta_gate_floor": 0.2,
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
| acc_main | 0.9778 |
| acc_turn | 0.9392 |
| acc_turn_transition | 0.6667 |
| turn_left_recall | 0.8760 |
| theta_mae_deg | 0.3153 |
| theta_abs_le_8_mae_deg | 0.3153 |
| theta_abs_le_8_p95_abs_err_deg | 1.1843 |
| theta_abs_le_8_max_abs_err_deg | 5.1537 |
| theta_abs_le_10_mae_deg | 0.3153 |
| theta_abs_le_10_p95_abs_err_deg | 1.1843 |
| theta_pos_6_8_mae_deg | 0.4440 |
| theta_pos_6_8_p95_abs_err_deg | 1.2608 |
| theta_pos_6_8_bias_deg | -0.1455 |
| theta_neg_8_6_mae_deg | 0.5118 |
| theta_neg_8_6_p95_abs_err_deg | 0.9655 |
| theta_neg_8_6_bias_deg | -0.4493 |
| theta_active_abs_ge_2_mae_deg | 0.6092 |
| theta_active_abs_ge_2_p95_abs_err_deg | 2.3069 |
| theta_neg_4_2_mae_deg | 1.4185 |
| theta_neg_4_2_p95_abs_err_deg | 3.6282 |
| theta_neg_4_2_bias_deg | 0.8542 |
| theta_flat_abs_p95_deg | 0.4667 |
| theta_flat_abs_max_deg | 2.5202 |
| theta_flat_bias_deg | -0.0580 |
| theta_near_flat_abs_p95_deg | 0.4667 |
| theta_near_flat_abs_max_deg | 2.5202 |
| theta_near_flat_bias_deg | -0.0491 |
| theta_true_zero_abs_p95_deg | 0.4797 |
| theta_true_zero_abs_max_deg | 2.5202 |
| theta_true_zero_bias_deg | -0.0481 |
| theta_flat_turn_abs_p95_deg | 0.3556 |
| flat_recall | 0.9947 |
| slope_recall | 0.9435 |
| slope_sign_acc | 0.3299 |

## Validation Best Metrics

```json
{
  "loss_total": 0.585078332373539,
  "acc_main": 0.9732052578361982,
  "acc_turn": 0.9342770475227502,
  "acc_turn_pure": 0.9502141327623126,
  "acc_turn_transition": 0.6636363636363637,
  "flat_recall": 0.9938608458390177,
  "stall_recall": 0.8787878787878788,
  "slope_recall": 0.9192825112107623,
  "recall_main": [
    0.9938608458390177,
    0.8787878787878788,
    0.9192825112107623
  ],
  "turn_right_recall": 0.9065155807365439,
  "turn_straight_recall": 0.9571550985432733,
  "turn_left_recall": 0.8973799126637555,
  "recall_turn": [
    0.9065155807365439,
    0.9571550985432733,
    0.8973799126637555
  ],
  "cm_turn": [
    [
      320,
      23,
      10
    ],
    [
      32,
      1117,
      18
    ],
    [
      1,
      46,
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
      58,
      3
    ],
    [
      35,
      1,
      410
    ]
  ],
  "main_confidence_mean": 0.9977875354809013,
  "main_confidence_error_mean": 0.9618028293484728,
  "main_low_conf_0p60_ratio": 0.0005055611729019212,
  "main_low_conf_0p70_ratio": 0.0015166835187057635,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 1,
      "error_rate": 1.0,
      "mean_confidence": 0.5438391142893335
    },
    {
      "bin": "[0.60,0.70)",
      "n": 2,
      "error_rate": 0.0,
      "mean_confidence": 0.6247127987451833
    },
    {
      "bin": "[0.70,0.80)",
      "n": 5,
      "error_rate": 0.6,
      "mean_confidence": 0.748018355046818
    },
    {
      "bin": "[0.80,0.90)",
      "n": 5,
      "error_rate": 0.6,
      "mean_confidence": 0.8346638319115165
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1965,
      "error_rate": 0.02340966921119593,
      "mean_confidence": 0.9994488903484231
    }
  ],
  "turn_confidence_mean": 0.9566101246183106,
  "turn_confidence_error_mean": 0.8543893263625925,
  "turn_low_conf_0p60_ratio": 0.01820020222446916,
  "turn_low_conf_0p70_ratio": 0.043478260869565216,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 36,
      "error_rate": 0.3055555555555556,
      "mean_confidence": 0.537502079099872
    },
    {
      "bin": "[0.60,0.70)",
      "n": 50,
      "error_rate": 0.32,
      "mean_confidence": 0.6512900196974338
    },
    {
      "bin": "[0.70,0.80)",
      "n": 58,
      "error_rate": 0.2413793103448276,
      "mean_confidence": 0.753052791463981
    },
    {
      "bin": "[0.80,0.90)",
      "n": 128,
      "error_rate": 0.1484375,
      "mean_confidence": 0.8576509975103174
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1706,
      "error_rate": 0.041031652989449004,
      "mean_confidence": 0.9887478669849472
    }
  ],
  "theta_mae_rad": 0.00547269219532609,
  "theta_mae_deg": 0.31356215476989746,
  "uphill_recall": 0.8464163822525598,
  "downhill_recall": 0.6864406779661016,
  "slope_sign_acc": 0.25732217573221755,
  "theta_flat_mae_deg": 0.18087579309940338,
  "theta_flat_abs_p95_deg": 0.4089704751968384,
  "theta_flat_abs_max_deg": 3.790627956390381,
  "theta_flat_bias_deg": -0.08401545882225037,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.16351206600666046,
  "theta_near_flat_abs_p95_deg": 0.43401581048965454,
  "theta_near_flat_abs_max_deg": 4.809633255004883,
  "theta_near_flat_bias_deg": -0.07772528380155563,
  "theta_near_flat_n": 1472.0,
  "theta_true_zero_mae_deg": 0.16071082651615143,
  "theta_true_zero_abs_p95_deg": 0.4337300956249237,
  "theta_true_zero_abs_max_deg": 4.809633255004883,
  "theta_true_zero_bias_deg": -0.07496622204780579,
  "theta_true_zero_n": 1433.0,
  "theta_flat_turn_mae_deg": 0.1345018446445465,
  "theta_flat_turn_abs_p95_deg": 0.3541378378868103,
  "theta_flat_turn_abs_max_deg": 0.9042430520057678,
  "theta_flat_turn_bias_deg": -0.08958399295806885,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.31356215476989746,
  "theta_slope_control_abs_p95_deg": 5.616073131561279,
  "theta_slope_control_abs_max_deg": 7.181210994720459,
  "theta_slope_control_bias_deg": -0.09226836264133453,
  "theta_slope_control_n": 1912.0,
  "theta_all_mae_deg": 0.3135621249675751,
  "theta_all_rmse_deg": 0.6064262390136719,
  "theta_all_p95_abs_err_deg": 1.0839591026306152,
  "theta_all_max_abs_err_deg": 4.210416793823242,
  "theta_all_bias_deg": -0.09226836264133453,
  "theta_all_n": 1912.0,
  "theta_active_abs_ge_2_mae_deg": 0.7497015595436096,
  "theta_active_abs_ge_2_rmse_deg": 1.0990675687789917,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.8786797523498535,
  "theta_active_abs_ge_2_max_abs_err_deg": 4.210416793823242,
  "theta_active_abs_ge_2_bias_deg": -0.11939564347267151,
  "theta_active_abs_ge_2_n": 446.0,
  "theta_abs_le_8_mae_deg": 0.3135621249675751,
  "theta_abs_le_8_rmse_deg": 0.6064262390136719,
  "theta_abs_le_8_p95_abs_err_deg": 1.0839591026306152,
  "theta_abs_le_8_max_abs_err_deg": 4.210416793823242,
  "theta_abs_le_8_bias_deg": -0.09226836264133453,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.3135621249675751,
  "theta_abs_le_10_rmse_deg": 0.6064262390136719,
  "theta_abs_le_10_p95_abs_err_deg": 1.0839591026306152,
  "theta_abs_le_10_max_abs_err_deg": 4.210416793823242,
  "theta_abs_le_10_bias_deg": -0.09226836264133453,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.6408048272132874,
  "theta_pos_6_8_rmse_deg": 0.7580893635749817,
  "theta_pos_6_8_p95_abs_err_deg": 1.2002722024917603,
  "theta_pos_6_8_max_abs_err_deg": 2.1501591205596924,
  "theta_pos_6_8_bias_deg": -0.5747216939926147,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.5376743674278259,
  "theta_neg_8_6_rmse_deg": 0.6093561053276062,
  "theta_neg_8_6_p95_abs_err_deg": 0.9815402626991272,
  "theta_neg_8_6_max_abs_err_deg": 1.164318323135376,
  "theta_neg_8_6_bias_deg": -0.5035618543624878,
  "theta_neg_8_6_n": 47.0,
  "theta_neg_4_2_mae_deg": 1.1521142721176147,
  "theta_neg_4_2_rmse_deg": 1.643518328666687,
  "theta_neg_4_2_p95_abs_err_deg": 3.430067300796509,
  "theta_neg_4_2_max_abs_err_deg": 4.210416793823242,
  "theta_neg_4_2_bias_deg": 0.3946930766105652,
  "theta_neg_4_2_n": 145.0
}
```
