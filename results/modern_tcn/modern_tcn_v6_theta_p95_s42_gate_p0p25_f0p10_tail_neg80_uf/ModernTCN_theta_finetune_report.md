# ModernTCN theta-head fine-tune report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 17
- train seconds: 70.8

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
  "lambda_theta_active_excess": 35.0,
  "lambda_theta_small_neg": 8.0,
  "lambda_theta_small_neg_excess": 80.0,
  "theta_excess_target_deg": 1.0,
  "theta_flat_excess_target_deg": 0.45,
  "theta_true_zero_tol_deg": 0.0001,
  "theta_small_neg_min_deg": -4.0,
  "theta_small_neg_max_deg": -2.0,
  "theta_gate_mode": "main_slope_prob",
  "theta_gate_power": 0.25,
  "theta_gate_floor": 0.1,
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
| acc_turn | 0.9397 |
| acc_turn_transition | 0.6882 |
| turn_left_recall | 0.8760 |
| theta_mae_deg | 0.2965 |
| theta_abs_le_8_mae_deg | 0.2965 |
| theta_abs_le_8_p95_abs_err_deg | 1.3244 |
| theta_abs_le_8_max_abs_err_deg | 4.8522 |
| theta_abs_le_10_mae_deg | 0.2965 |
| theta_abs_le_10_p95_abs_err_deg | 1.3244 |
| theta_pos_6_8_mae_deg | 0.7833 |
| theta_pos_6_8_p95_abs_err_deg | 2.5725 |
| theta_pos_6_8_bias_deg | -0.7234 |
| theta_neg_8_6_mae_deg | 0.4837 |
| theta_neg_8_6_p95_abs_err_deg | 1.2355 |
| theta_neg_8_6_bias_deg | -0.0423 |
| theta_active_abs_ge_2_mae_deg | 0.6279 |
| theta_active_abs_ge_2_p95_abs_err_deg | 2.5747 |
| theta_neg_4_2_mae_deg | 1.3154 |
| theta_neg_4_2_p95_abs_err_deg | 3.6087 |
| theta_neg_4_2_bias_deg | 0.9524 |
| theta_flat_abs_p95_deg | 0.4347 |
| theta_flat_abs_max_deg | 1.8632 |
| theta_flat_bias_deg | -0.0127 |
| theta_near_flat_abs_p95_deg | 0.4263 |
| theta_near_flat_abs_max_deg | 2.7379 |
| theta_near_flat_bias_deg | -0.0054 |
| theta_true_zero_abs_p95_deg | 0.4268 |
| theta_true_zero_abs_max_deg | 2.7379 |
| theta_true_zero_bias_deg | -0.0055 |
| theta_flat_turn_abs_p95_deg | 0.3540 |
| flat_recall | 0.9947 |
| slope_recall | 0.9416 |
| slope_sign_acc | 0.3326 |

## Validation Best Metrics

```json
{
  "loss_total": 0.597046026506125,
  "acc_main": 0.9726996966632963,
  "acc_turn": 0.9342770475227502,
  "acc_turn_pure": 0.9528907922912205,
  "acc_turn_transition": 0.6181818181818182,
  "flat_recall": 0.9938608458390177,
  "stall_recall": 0.8787878787878788,
  "slope_recall": 0.9170403587443946,
  "recall_main": [
    0.9938608458390177,
    0.8787878787878788,
    0.9170403587443946
  ],
  "turn_right_recall": 0.9121813031161473,
  "turn_straight_recall": 0.9554413024850043,
  "turn_left_recall": 0.8973799126637555,
  "recall_turn": [
    0.9121813031161473,
    0.9554413024850043,
    0.8973799126637555
  ],
  "cm_turn": [
    [
      322,
      22,
      9
    ],
    [
      34,
      1115,
      18
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
      58,
      3
    ],
    [
      36,
      1,
      409
    ]
  ],
  "main_confidence_mean": 0.9976099897887467,
  "main_confidence_error_mean": 0.9597195227123791,
  "main_low_conf_0p60_ratio": 0.0025278058645096056,
  "main_low_conf_0p70_ratio": 0.003033367037411527,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 5,
      "error_rate": 0.6,
      "mean_confidence": 0.5550876905138576
    },
    {
      "bin": "[0.60,0.70)",
      "n": 1,
      "error_rate": 0.0,
      "mean_confidence": 0.6904170921107495
    },
    {
      "bin": "[0.70,0.80)",
      "n": 2,
      "error_rate": 0.5,
      "mean_confidence": 0.7854005162412128
    },
    {
      "bin": "[0.80,0.90)",
      "n": 4,
      "error_rate": 0.25,
      "mean_confidence": 0.8558947650986553
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1966,
      "error_rate": 0.024923702950152594,
      "mean_confidence": 0.9993958922505514
    }
  ],
  "turn_confidence_mean": 0.9551447862236399,
  "turn_confidence_error_mean": 0.8536740754915095,
  "turn_low_conf_0p60_ratio": 0.021739130434782608,
  "turn_low_conf_0p70_ratio": 0.046511627906976744,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 43,
      "error_rate": 0.3953488372093023,
      "mean_confidence": 0.5447192795256796
    },
    {
      "bin": "[0.60,0.70)",
      "n": 49,
      "error_rate": 0.2653061224489796,
      "mean_confidence": 0.6608085267595892
    },
    {
      "bin": "[0.70,0.80)",
      "n": 64,
      "error_rate": 0.15625,
      "mean_confidence": 0.7591497911962541
    },
    {
      "bin": "[0.80,0.90)",
      "n": 128,
      "error_rate": 0.15625,
      "mean_confidence": 0.8555675338604563
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1694,
      "error_rate": 0.04132231404958678,
      "mean_confidence": 0.9890056725790064
    }
  ],
  "theta_mae_rad": 0.004801705479621887,
  "theta_mae_deg": 0.2751174569129944,
  "uphill_recall": 0.8464163822525598,
  "downhill_recall": 0.6822033898305084,
  "slope_sign_acc": 0.2641213389121339,
  "theta_flat_mae_deg": 0.13737818598747253,
  "theta_flat_abs_p95_deg": 0.3626386523246765,
  "theta_flat_abs_max_deg": 4.487179756164551,
  "theta_flat_bias_deg": -0.02659144066274166,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.11662296205759048,
  "theta_near_flat_abs_p95_deg": 0.37718841433525085,
  "theta_near_flat_abs_max_deg": 4.487179756164551,
  "theta_near_flat_bias_deg": -0.020375946536660194,
  "theta_near_flat_n": 1472.0,
  "theta_true_zero_mae_deg": 0.11426103115081787,
  "theta_true_zero_abs_p95_deg": 0.37464049458503723,
  "theta_true_zero_abs_max_deg": 4.487179756164551,
  "theta_true_zero_bias_deg": -0.018331581726670265,
  "theta_true_zero_n": 1433.0,
  "theta_flat_turn_mae_deg": 0.12728562951087952,
  "theta_flat_turn_abs_p95_deg": 0.3314054012298584,
  "theta_flat_turn_abs_max_deg": 0.6764768362045288,
  "theta_flat_turn_bias_deg": -0.0970078557729721,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.2751174569129944,
  "theta_slope_control_abs_p95_deg": 5.534592151641846,
  "theta_slope_control_abs_max_deg": 7.582976341247559,
  "theta_slope_control_bias_deg": -0.026521632447838783,
  "theta_slope_control_n": 1912.0,
  "theta_all_mae_deg": 0.275117427110672,
  "theta_all_rmse_deg": 0.594237744808197,
  "theta_all_p95_abs_err_deg": 1.2432423830032349,
  "theta_all_max_abs_err_deg": 4.487179756164551,
  "theta_all_bias_deg": -0.02652163803577423,
  "theta_all_n": 1912.0,
  "theta_active_abs_ge_2_mae_deg": 0.7278658747673035,
  "theta_active_abs_ge_2_rmse_deg": 1.088753581047058,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.87637996673584,
  "theta_active_abs_ge_2_max_abs_err_deg": 4.064518928527832,
  "theta_active_abs_ge_2_bias_deg": -0.026292182505130768,
  "theta_active_abs_ge_2_n": 446.0,
  "theta_abs_le_8_mae_deg": 0.275117427110672,
  "theta_abs_le_8_rmse_deg": 0.594237744808197,
  "theta_abs_le_8_p95_abs_err_deg": 1.2432423830032349,
  "theta_abs_le_8_max_abs_err_deg": 4.487179756164551,
  "theta_abs_le_8_bias_deg": -0.02652163803577423,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.275117427110672,
  "theta_abs_le_10_rmse_deg": 0.594237744808197,
  "theta_abs_le_10_p95_abs_err_deg": 1.2432423830032349,
  "theta_abs_le_10_max_abs_err_deg": 4.487179756164551,
  "theta_abs_le_10_bias_deg": -0.02652163803577423,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.7636606693267822,
  "theta_pos_6_8_rmse_deg": 0.9299496412277222,
  "theta_pos_6_8_p95_abs_err_deg": 1.4721570014953613,
  "theta_pos_6_8_max_abs_err_deg": 3.1056039333343506,
  "theta_pos_6_8_bias_deg": -0.7306265830993652,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.4698421061038971,
  "theta_neg_8_6_rmse_deg": 0.6059902310371399,
  "theta_neg_8_6_p95_abs_err_deg": 1.291324257850647,
  "theta_neg_8_6_max_abs_err_deg": 1.5829764604568481,
  "theta_neg_8_6_bias_deg": -0.1456318348646164,
  "theta_neg_8_6_n": 47.0,
  "theta_neg_4_2_mae_deg": 1.0152902603149414,
  "theta_neg_4_2_rmse_deg": 1.5345664024353027,
  "theta_neg_4_2_p95_abs_err_deg": 3.4992330074310303,
  "theta_neg_4_2_max_abs_err_deg": 4.064518928527832,
  "theta_neg_4_2_bias_deg": 0.5227831602096558,
  "theta_neg_4_2_n": 145.0
}
```
