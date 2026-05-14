# ModernTCN theta-head fine-tune report

- base checkpoint: `results\modern_tcn\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_tail_neg120_uf\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 17
- train seconds: 83.3

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
  "lambda_theta_near_flat": 8.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 40.0,
  "lambda_theta_flat_excess": 260.0,
  "lambda_theta_near_flat_excess": 320.0,
  "lambda_theta_true_zero_excess": 380.0,
  "lambda_theta_active_excess": 90.0,
  "lambda_theta_small_neg": 18.0,
  "lambda_theta_small_neg_excess": 180.0,
  "theta_excess_target_deg": 0.8,
  "theta_flat_excess_target_deg": 0.35,
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
  "theta_neg_weight": 1.8,
  "theta_pos_weight": 1.2,
  "turn_transition_weight": 1.0,
  "select_turn_weight": 0.3,
  "select_turn_transition_weight": 1.0,
  "select_turn_transition_target": 0.75,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.8,
  "select_theta_weight": 0.7,
  "select_theta_ref_deg": 1.0,
  "select_theta_p95_weight": 14.0,
  "select_theta_p95_target_deg": 1.0,
  "select_theta_flat_p95_weight": 14.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_near_flat_p95_weight": 14.0,
  "select_theta_near_flat_p95_target_deg": 1.0,
  "select_theta_true_zero_p95_weight": 14.0,
  "select_theta_true_zero_p95_target_deg": 1.0,
  "select_theta_flat_peak_weight": 3.0,
  "select_theta_flat_peak_target_deg": 3.0,
  "select_theta_small_neg_p95_weight": 8.0,
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
| theta_mae_deg | 0.3022 |
| theta_abs_le_8_mae_deg | 0.3022 |
| theta_abs_le_8_p95_abs_err_deg | 1.1261 |
| theta_abs_le_8_max_abs_err_deg | 4.3202 |
| theta_abs_le_10_mae_deg | 0.3022 |
| theta_abs_le_10_p95_abs_err_deg | 1.1261 |
| theta_pos_6_8_mae_deg | 0.3648 |
| theta_pos_6_8_p95_abs_err_deg | 1.1118 |
| theta_pos_6_8_bias_deg | -0.2173 |
| theta_neg_8_6_mae_deg | 0.4472 |
| theta_neg_8_6_p95_abs_err_deg | 0.9675 |
| theta_neg_8_6_bias_deg | -0.3065 |
| theta_active_abs_ge_2_mae_deg | 0.4878 |
| theta_active_abs_ge_2_p95_abs_err_deg | 2.3887 |
| theta_neg_4_2_mae_deg | 1.2658 |
| theta_neg_4_2_p95_abs_err_deg | 3.4792 |
| theta_neg_4_2_bias_deg | 0.5841 |
| theta_flat_abs_p95_deg | 0.5794 |
| theta_flat_abs_max_deg | 2.5064 |
| theta_flat_bias_deg | -0.1598 |
| theta_near_flat_abs_p95_deg | 0.5798 |
| theta_near_flat_abs_max_deg | 2.5064 |
| theta_near_flat_bias_deg | -0.1532 |
| theta_true_zero_abs_p95_deg | 0.5826 |
| theta_true_zero_abs_max_deg | 2.5064 |
| theta_true_zero_bias_deg | -0.1532 |
| theta_flat_turn_abs_p95_deg | 0.4696 |
| flat_recall | 0.9947 |
| slope_recall | 0.9416 |
| slope_sign_acc | 0.3310 |

## Validation Best Metrics

```json
{
  "loss_total": 0.651949723581694,
  "acc_main": 0.9732052578361982,
  "acc_turn": 0.9317492416582407,
  "acc_turn_pure": 0.9475374732334048,
  "acc_turn_transition": 0.6636363636363637,
  "flat_recall": 0.9938608458390177,
  "stall_recall": 0.8787878787878788,
  "slope_recall": 0.9192825112107623,
  "recall_main": [
    0.9938608458390177,
    0.8787878787878788,
    0.9192825112107623
  ],
  "turn_right_recall": 0.9036827195467422,
  "turn_straight_recall": 0.9545844044558698,
  "turn_left_recall": 0.8951965065502183,
  "recall_turn": [
    0.9036827195467422,
    0.9545844044558698,
    0.8951965065502183
  ],
  "cm_turn": [
    [
      319,
      24,
      10
    ],
    [
      32,
      1114,
      21
    ],
    [
      1,
      47,
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
      1,
      410
    ]
  ],
  "main_confidence_mean": 0.9979144763645261,
  "main_confidence_error_mean": 0.9704676089495378,
  "main_low_conf_0p60_ratio": 0.0010111223458038423,
  "main_low_conf_0p70_ratio": 0.0020222446916076846,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 2,
      "error_rate": 0.0,
      "mean_confidence": 0.566662538999051
    },
    {
      "bin": "[0.60,0.70)",
      "n": 2,
      "error_rate": 1.0,
      "mean_confidence": 0.6527468771316185
    },
    {
      "bin": "[0.70,0.80)",
      "n": 2,
      "error_rate": 0.0,
      "mean_confidence": 0.704750476404554
    },
    {
      "bin": "[0.80,0.90)",
      "n": 6,
      "error_rate": 0.6666666666666666,
      "mean_confidence": 0.8696993462482888
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1966,
      "error_rate": 0.023906408952187184,
      "mean_confidence": 0.9993938547235361
    }
  ],
  "turn_confidence_mean": 0.9545430968136838,
  "turn_confidence_error_mean": 0.8380357333648856,
  "turn_low_conf_0p60_ratio": 0.01870576339737108,
  "turn_low_conf_0p70_ratio": 0.04499494438827098,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 37,
      "error_rate": 0.4864864864864865,
      "mean_confidence": 0.5430980605033219
    },
    {
      "bin": "[0.60,0.70)",
      "n": 52,
      "error_rate": 0.3076923076923077,
      "mean_confidence": 0.6459171896092164
    },
    {
      "bin": "[0.70,0.80)",
      "n": 59,
      "error_rate": 0.23728813559322035,
      "mean_confidence": 0.7560947713530465
    },
    {
      "bin": "[0.80,0.90)",
      "n": 136,
      "error_rate": 0.125,
      "mean_confidence": 0.8541271471979286
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1694,
      "error_rate": 0.04132231404958678,
      "mean_confidence": 0.9879770011041419
    }
  ],
  "theta_mae_rad": 0.005383624229580164,
  "theta_mae_deg": 0.30845892429351807,
  "uphill_recall": 0.8464163822525598,
  "downhill_recall": 0.6864406779661016,
  "slope_sign_acc": 0.26359832635983266,
  "theta_flat_mae_deg": 0.21451951563358307,
  "theta_flat_abs_p95_deg": 0.5384795069694519,
  "theta_flat_abs_max_deg": 3.9134974479675293,
  "theta_flat_bias_deg": -0.1583762913942337,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.19959405064582825,
  "theta_near_flat_abs_p95_deg": 0.5325244665145874,
  "theta_near_flat_abs_max_deg": 4.851539611816406,
  "theta_near_flat_bias_deg": -0.15130944550037384,
  "theta_near_flat_n": 1472.0,
  "theta_true_zero_mae_deg": 0.19749432802200317,
  "theta_true_zero_abs_p95_deg": 0.5159892439842224,
  "theta_true_zero_abs_max_deg": 4.851539611816406,
  "theta_true_zero_bias_deg": -0.14896276593208313,
  "theta_true_zero_n": 1433.0,
  "theta_flat_turn_mae_deg": 0.1861901730298996,
  "theta_flat_turn_abs_p95_deg": 0.4374818503856659,
  "theta_flat_turn_abs_max_deg": 1.4922248125076294,
  "theta_flat_turn_bias_deg": -0.17357616126537323,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.30845892429351807,
  "theta_slope_control_abs_p95_deg": 5.567123889923096,
  "theta_slope_control_abs_max_deg": 7.268787860870361,
  "theta_slope_control_bias_deg": -0.11183158308267593,
  "theta_slope_control_n": 1912.0,
  "theta_all_mae_deg": 0.30845892429351807,
  "theta_all_rmse_deg": 0.5861158967018127,
  "theta_all_p95_abs_err_deg": 1.02655029296875,
  "theta_all_max_abs_err_deg": 3.9602348804473877,
  "theta_all_bias_deg": -0.11183157563209534,
  "theta_all_n": 1912.0,
  "theta_active_abs_ge_2_mae_deg": 0.6172373294830322,
  "theta_active_abs_ge_2_rmse_deg": 1.0063468217849731,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.796128988265991,
  "theta_active_abs_ge_2_max_abs_err_deg": 3.9602348804473877,
  "theta_active_abs_ge_2_bias_deg": 0.04116068780422211,
  "theta_active_abs_ge_2_n": 446.0,
  "theta_abs_le_8_mae_deg": 0.30845892429351807,
  "theta_abs_le_8_rmse_deg": 0.5861158967018127,
  "theta_abs_le_8_p95_abs_err_deg": 1.02655029296875,
  "theta_abs_le_8_max_abs_err_deg": 3.9602348804473877,
  "theta_abs_le_8_bias_deg": -0.11183157563209534,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.30845892429351807,
  "theta_abs_le_10_rmse_deg": 0.5861158967018127,
  "theta_abs_le_10_p95_abs_err_deg": 1.02655029296875,
  "theta_abs_le_10_max_abs_err_deg": 3.9602348804473877,
  "theta_abs_le_10_bias_deg": -0.11183157563209534,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.610261857509613,
  "theta_pos_6_8_rmse_deg": 0.729699432849884,
  "theta_pos_6_8_p95_abs_err_deg": 1.080277681350708,
  "theta_pos_6_8_max_abs_err_deg": 2.326972246170044,
  "theta_pos_6_8_bias_deg": -0.5542006492614746,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.4784221947193146,
  "theta_neg_8_6_rmse_deg": 0.5517531037330627,
  "theta_neg_8_6_p95_abs_err_deg": 0.9731274247169495,
  "theta_neg_8_6_max_abs_err_deg": 1.2687878608703613,
  "theta_neg_8_6_bias_deg": -0.40062209963798523,
  "theta_neg_8_6_n": 47.0,
  "theta_neg_4_2_mae_deg": 1.006421685218811,
  "theta_neg_4_2_rmse_deg": 1.544294834136963,
  "theta_neg_4_2_p95_abs_err_deg": 3.3008639812469482,
  "theta_neg_4_2_max_abs_err_deg": 3.9602348804473877,
  "theta_neg_4_2_bias_deg": 0.4862746596336365,
  "theta_neg_4_2_n": 145.0
}
```
