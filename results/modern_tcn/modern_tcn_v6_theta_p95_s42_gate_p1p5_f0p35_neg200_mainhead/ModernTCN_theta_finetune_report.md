# ModernTCN theta-head fine-tune report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 48
- train seconds: 126.0

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
  "theta_gate_power": 1.5,
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
| acc_turn | 0.9392 |
| acc_turn_transition | 0.6774 |
| turn_left_recall | 0.8760 |
| theta_mae_deg | 0.3749 |
| theta_abs_le_8_mae_deg | 0.3749 |
| theta_abs_le_8_p95_abs_err_deg | 1.4599 |
| theta_abs_le_8_max_abs_err_deg | 6.0428 |
| theta_abs_le_10_mae_deg | 0.3749 |
| theta_abs_le_10_p95_abs_err_deg | 1.4599 |
| theta_pos_6_8_mae_deg | 0.6129 |
| theta_pos_6_8_p95_abs_err_deg | 1.6042 |
| theta_pos_6_8_bias_deg | -0.4108 |
| theta_neg_8_6_mae_deg | 0.5541 |
| theta_neg_8_6_p95_abs_err_deg | 1.0576 |
| theta_neg_8_6_bias_deg | -0.5065 |
| theta_active_abs_ge_2_mae_deg | 0.5821 |
| theta_active_abs_ge_2_p95_abs_err_deg | 2.0182 |
| theta_neg_4_2_mae_deg | 1.2447 |
| theta_neg_4_2_p95_abs_err_deg | 3.7195 |
| theta_neg_4_2_bias_deg | 0.7369 |
| theta_flat_abs_p95_deg | 0.9658 |
| theta_flat_abs_max_deg | 5.1286 |
| theta_flat_bias_deg | -0.0073 |
| theta_near_flat_abs_p95_deg | 0.9784 |
| theta_near_flat_abs_max_deg | 5.1286 |
| theta_near_flat_bias_deg | 0.0045 |
| theta_true_zero_abs_p95_deg | 1.0466 |
| theta_true_zero_abs_max_deg | 5.1286 |
| theta_true_zero_bias_deg | 0.0038 |
| theta_flat_turn_abs_p95_deg | 0.6343 |
| flat_recall | 0.9947 |
| slope_recall | 0.9435 |
| slope_sign_acc | 0.3245 |

## Validation Best Metrics

```json
{
  "loss_total": 0.6535917084185733,
  "acc_main": 0.9737108190091001,
  "acc_turn": 0.9332659251769464,
  "acc_turn_pure": 0.9528907922912205,
  "acc_turn_transition": 0.6,
  "flat_recall": 0.9938608458390177,
  "stall_recall": 0.8787878787878788,
  "slope_recall": 0.92152466367713,
  "recall_main": [
    0.9938608458390177,
    0.8787878787878788,
    0.92152466367713
  ],
  "turn_right_recall": 0.9121813031161473,
  "turn_straight_recall": 0.9545844044558698,
  "turn_left_recall": 0.8951965065502183,
  "recall_turn": [
    0.9121813031161473,
    0.9545844044558698,
    0.8951965065502183
  ],
  "cm_turn": [
    [
      322,
      20,
      11
    ],
    [
      35,
      1114,
      18
    ],
    [
      0,
      48,
      410
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
  "main_confidence_mean": 0.9981057324034615,
  "main_confidence_error_mean": 0.9780375470340668,
  "main_low_conf_0p60_ratio": 0.0,
  "main_low_conf_0p70_ratio": 0.0005055611729019212,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 0,
      "error_rate": NaN,
      "mean_confidence": NaN
    },
    {
      "bin": "[0.60,0.70)",
      "n": 1,
      "error_rate": 0.0,
      "mean_confidence": 0.6943618016371228
    },
    {
      "bin": "[0.70,0.80)",
      "n": 3,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.7378898158137277
    },
    {
      "bin": "[0.80,0.90)",
      "n": 10,
      "error_rate": 0.4,
      "mean_confidence": 0.8506067302350322
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1964,
      "error_rate": 0.023930753564154784,
      "mean_confidence": 0.9994088799096834
    }
  ],
  "turn_confidence_mean": 0.9537458379970554,
  "turn_confidence_error_mean": 0.8475566111415427,
  "turn_low_conf_0p60_ratio": 0.020728008088978768,
  "turn_low_conf_0p70_ratio": 0.04701718907987867,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 41,
      "error_rate": 0.4146341463414634,
      "mean_confidence": 0.5395767991705998
    },
    {
      "bin": "[0.60,0.70)",
      "n": 52,
      "error_rate": 0.2692307692307692,
      "mean_confidence": 0.660183304693548
    },
    {
      "bin": "[0.70,0.80)",
      "n": 63,
      "error_rate": 0.14285714285714285,
      "mean_confidence": 0.7561669216761391
    },
    {
      "bin": "[0.80,0.90)",
      "n": 150,
      "error_rate": 0.14666666666666667,
      "mean_confidence": 0.8585468704130645
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1672,
      "error_rate": 0.041866028708133975,
      "mean_confidence": 0.9890170695697129
    }
  ],
  "theta_mae_rad": 0.005993148777633905,
  "theta_mae_deg": 0.3433821201324463,
  "uphill_recall": 0.8498293515358362,
  "downhill_recall": 0.6864406779661016,
  "slope_sign_acc": 0.25889121338912136,
  "theta_flat_mae_deg": 0.24181635677814484,
  "theta_flat_abs_p95_deg": 0.712580144405365,
  "theta_flat_abs_max_deg": 3.978706121444702,
  "theta_flat_bias_deg": -0.06800965964794159,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.22830218076705933,
  "theta_near_flat_abs_p95_deg": 0.7128691077232361,
  "theta_near_flat_abs_max_deg": 4.276038646697998,
  "theta_near_flat_bias_deg": -0.05673786625266075,
  "theta_near_flat_n": 1472.0,
  "theta_true_zero_mae_deg": 0.22548584640026093,
  "theta_true_zero_abs_p95_deg": 0.712073564529419,
  "theta_true_zero_abs_max_deg": 4.276038646697998,
  "theta_true_zero_bias_deg": -0.053107716143131256,
  "theta_true_zero_n": 1433.0,
  "theta_flat_turn_mae_deg": 0.2162429243326187,
  "theta_flat_turn_abs_p95_deg": 0.5202646851539612,
  "theta_flat_turn_abs_max_deg": 2.0968353748321533,
  "theta_flat_turn_bias_deg": -0.12509004771709442,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.3433821201324463,
  "theta_slope_control_abs_p95_deg": 6.0201215744018555,
  "theta_slope_control_abs_max_deg": 7.71564245223999,
  "theta_slope_control_bias_deg": -0.030473053455352783,
  "theta_slope_control_n": 1912.0,
  "theta_all_mae_deg": 0.3433821201324463,
  "theta_all_rmse_deg": 0.6325019001960754,
  "theta_all_p95_abs_err_deg": 1.2070204019546509,
  "theta_all_max_abs_err_deg": 4.568289279937744,
  "theta_all_bias_deg": -0.030473055317997932,
  "theta_all_n": 1912.0,
  "theta_active_abs_ge_2_mae_deg": 0.6772281527519226,
  "theta_active_abs_ge_2_rmse_deg": 1.011403203010559,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.663891315460205,
  "theta_active_abs_ge_2_max_abs_err_deg": 4.568289279937744,
  "theta_active_abs_ge_2_bias_deg": 0.09290959686040878,
  "theta_active_abs_ge_2_n": 446.0,
  "theta_abs_le_8_mae_deg": 0.3433821201324463,
  "theta_abs_le_8_rmse_deg": 0.6325019001960754,
  "theta_abs_le_8_p95_abs_err_deg": 1.2070204019546509,
  "theta_abs_le_8_max_abs_err_deg": 4.568289279937744,
  "theta_abs_le_8_bias_deg": -0.030473055317997932,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.3433821201324463,
  "theta_abs_le_10_rmse_deg": 0.6325019001960754,
  "theta_abs_le_10_p95_abs_err_deg": 1.2070204019546509,
  "theta_abs_le_10_max_abs_err_deg": 4.568289279937744,
  "theta_abs_le_10_bias_deg": -0.030473055317997932,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.4061969518661499,
  "theta_pos_6_8_rmse_deg": 0.5878720283508301,
  "theta_pos_6_8_p95_abs_err_deg": 0.9200311303138733,
  "theta_pos_6_8_max_abs_err_deg": 2.107217311859131,
  "theta_pos_6_8_bias_deg": -0.22792604565620422,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.5597922801971436,
  "theta_neg_8_6_rmse_deg": 0.6387126445770264,
  "theta_neg_8_6_p95_abs_err_deg": 1.0600461959838867,
  "theta_neg_8_6_max_abs_err_deg": 1.3447881937026978,
  "theta_neg_8_6_bias_deg": -0.5214729309082031,
  "theta_neg_8_6_n": 47.0,
  "theta_neg_4_2_mae_deg": 1.0560485124588013,
  "theta_neg_4_2_rmse_deg": 1.4730380773544312,
  "theta_neg_4_2_p95_abs_err_deg": 3.116358757019043,
  "theta_neg_4_2_max_abs_err_deg": 4.568289279937744,
  "theta_neg_4_2_bias_deg": 0.30742818117141724,
  "theta_neg_4_2_n": 145.0
}
```
