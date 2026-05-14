# ModernTCN theta-head fine-tune report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 26
- train seconds: 84.3

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
  "theta_gate_power": 1.0,
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
| acc_main | 0.9783 |
| acc_turn | 0.9387 |
| acc_turn_transition | 0.6667 |
| turn_left_recall | 0.8734 |
| theta_mae_deg | 0.3557 |
| theta_abs_le_8_mae_deg | 0.3557 |
| theta_abs_le_8_p95_abs_err_deg | 1.2881 |
| theta_abs_le_8_max_abs_err_deg | 9.4563 |
| theta_abs_le_10_mae_deg | 0.3557 |
| theta_abs_le_10_p95_abs_err_deg | 1.2881 |
| theta_pos_6_8_mae_deg | 0.6053 |
| theta_pos_6_8_p95_abs_err_deg | 1.5480 |
| theta_pos_6_8_bias_deg | 0.0279 |
| theta_neg_8_6_mae_deg | 0.5728 |
| theta_neg_8_6_p95_abs_err_deg | 1.1139 |
| theta_neg_8_6_bias_deg | -0.5061 |
| theta_active_abs_ge_2_mae_deg | 0.6899 |
| theta_active_abs_ge_2_p95_abs_err_deg | 2.3866 |
| theta_neg_4_2_mae_deg | 1.5154 |
| theta_neg_4_2_p95_abs_err_deg | 3.4975 |
| theta_neg_4_2_bias_deg | 0.2423 |
| theta_flat_abs_p95_deg | 0.6979 |
| theta_flat_abs_max_deg | 1.7190 |
| theta_flat_bias_deg | -0.1583 |
| theta_near_flat_abs_p95_deg | 0.7033 |
| theta_near_flat_abs_max_deg | 1.7190 |
| theta_near_flat_bias_deg | -0.1515 |
| theta_true_zero_abs_p95_deg | 0.7098 |
| theta_true_zero_abs_max_deg | 1.7190 |
| theta_true_zero_bias_deg | -0.1527 |
| theta_flat_turn_abs_p95_deg | 0.4663 |
| flat_recall | 0.9947 |
| slope_recall | 0.9435 |
| slope_sign_acc | 0.3348 |

## Validation Best Metrics

```json
{
  "loss_total": 0.5499613758466603,
  "acc_main": 0.9732052578361982,
  "acc_turn": 0.9332659251769464,
  "acc_turn_pure": 0.9534261241970021,
  "acc_turn_transition": 0.5909090909090909,
  "flat_recall": 0.9924965893587995,
  "stall_recall": 0.8787878787878788,
  "slope_recall": 0.9237668161434978,
  "recall_main": [
    0.9924965893587995,
    0.8787878787878788,
    0.9237668161434978
  ],
  "turn_right_recall": 0.9235127478753541,
  "turn_straight_recall": 0.9537275064267352,
  "turn_left_recall": 0.888646288209607,
  "recall_turn": [
    0.9235127478753541,
    0.9537275064267352,
    0.888646288209607
  ],
  "cm_turn": [
    [
      326,
      18,
      9
    ],
    [
      38,
      1113,
      16
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
      1455,
      4,
      7
    ],
    [
      5,
      58,
      3
    ],
    [
      34,
      0,
      412
    ]
  ],
  "main_confidence_mean": 0.9972947458505802,
  "main_confidence_error_mean": 0.9654976055098865,
  "main_low_conf_0p60_ratio": 0.0010111223458038423,
  "main_low_conf_0p70_ratio": 0.0020222446916076846,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 2,
      "error_rate": 0.5,
      "mean_confidence": 0.5805475148407804
    },
    {
      "bin": "[0.60,0.70)",
      "n": 2,
      "error_rate": 0.0,
      "mean_confidence": 0.6564449267934818
    },
    {
      "bin": "[0.70,0.80)",
      "n": 5,
      "error_rate": 0.2,
      "mean_confidence": 0.7682796788077584
    },
    {
      "bin": "[0.80,0.90)",
      "n": 8,
      "error_rate": 0.625,
      "mean_confidence": 0.8500907735539383
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1961,
      "error_rate": 0.023457419683834777,
      "mean_confidence": 0.9992518601870009
    }
  ],
  "turn_confidence_mean": 0.954774633402207,
  "turn_confidence_error_mean": 0.8467574316721141,
  "turn_low_conf_0p60_ratio": 0.01769464105156724,
  "turn_low_conf_0p70_ratio": 0.04499494438827098,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 35,
      "error_rate": 0.42857142857142855,
      "mean_confidence": 0.5257957152091524
    },
    {
      "bin": "[0.60,0.70)",
      "n": 54,
      "error_rate": 0.25925925925925924,
      "mean_confidence": 0.6565303968265153
    },
    {
      "bin": "[0.70,0.80)",
      "n": 72,
      "error_rate": 0.20833333333333334,
      "mean_confidence": 0.757307241290876
    },
    {
      "bin": "[0.80,0.90)",
      "n": 119,
      "error_rate": 0.14285714285714285,
      "mean_confidence": 0.8587187985715999
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1698,
      "error_rate": 0.04181389870435807,
      "mean_confidence": 0.9882067579538575
    }
  ],
  "theta_mae_rad": 0.0058725737035274506,
  "theta_mae_deg": 0.336473673582077,
  "uphill_recall": 0.856655290102389,
  "downhill_recall": 0.6864406779661016,
  "slope_sign_acc": 0.2630753138075314,
  "theta_flat_mae_deg": 0.19310402870178223,
  "theta_flat_abs_p95_deg": 0.6265370845794678,
  "theta_flat_abs_max_deg": 4.08186149597168,
  "theta_flat_bias_deg": -0.14060798287391663,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.1753999888896942,
  "theta_near_flat_abs_p95_deg": 0.626038670539856,
  "theta_near_flat_abs_max_deg": 4.60310697555542,
  "theta_near_flat_bias_deg": -0.1283518224954605,
  "theta_near_flat_n": 1472.0,
  "theta_true_zero_mae_deg": 0.17363113164901733,
  "theta_true_zero_abs_p95_deg": 0.6259557008743286,
  "theta_true_zero_abs_max_deg": 4.60310697555542,
  "theta_true_zero_bias_deg": -0.12659133970737457,
  "theta_true_zero_n": 1433.0,
  "theta_flat_turn_mae_deg": 0.1373160183429718,
  "theta_flat_turn_abs_p95_deg": 0.3468208312988281,
  "theta_flat_turn_abs_max_deg": 1.023073673248291,
  "theta_flat_turn_bias_deg": -0.12796154618263245,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.336473673582077,
  "theta_slope_control_abs_p95_deg": 5.769811153411865,
  "theta_slope_control_abs_max_deg": 14.293344497680664,
  "theta_slope_control_bias_deg": -0.11895771324634552,
  "theta_slope_control_n": 1912.0,
  "theta_all_mae_deg": 0.336473673582077,
  "theta_all_rmse_deg": 0.6864046454429626,
  "theta_all_p95_abs_err_deg": 1.195365071296692,
  "theta_all_max_abs_err_deg": 10.29334545135498,
  "theta_all_bias_deg": -0.11895771324634552,
  "theta_all_n": 1912.0,
  "theta_active_abs_ge_2_mae_deg": 0.8077290654182434,
  "theta_active_abs_ge_2_rmse_deg": 1.2514151334762573,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.832953929901123,
  "theta_active_abs_ge_2_max_abs_err_deg": 10.29334545135498,
  "theta_active_abs_ge_2_bias_deg": -0.047793351113796234,
  "theta_active_abs_ge_2_n": 446.0,
  "theta_abs_le_8_mae_deg": 0.336473673582077,
  "theta_abs_le_8_rmse_deg": 0.6864046454429626,
  "theta_abs_le_8_p95_abs_err_deg": 1.195365071296692,
  "theta_abs_le_8_max_abs_err_deg": 10.29334545135498,
  "theta_abs_le_8_bias_deg": -0.11895771324634552,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.336473673582077,
  "theta_abs_le_10_rmse_deg": 0.6864046454429626,
  "theta_abs_le_10_p95_abs_err_deg": 1.195365071296692,
  "theta_abs_le_10_max_abs_err_deg": 10.29334545135498,
  "theta_abs_le_10_bias_deg": -0.11895771324634552,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.5757240056991577,
  "theta_pos_6_8_rmse_deg": 0.6863552331924438,
  "theta_pos_6_8_p95_abs_err_deg": 1.1275107860565186,
  "theta_pos_6_8_max_abs_err_deg": 2.217036247253418,
  "theta_pos_6_8_bias_deg": -0.43450257182121277,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.6223530173301697,
  "theta_neg_8_6_rmse_deg": 0.6995478272438049,
  "theta_neg_8_6_p95_abs_err_deg": 1.1248379945755005,
  "theta_neg_8_6_max_abs_err_deg": 1.192257285118103,
  "theta_neg_8_6_bias_deg": -0.5788146257400513,
  "theta_neg_8_6_n": 47.0,
  "theta_neg_4_2_mae_deg": 1.1006035804748535,
  "theta_neg_4_2_rmse_deg": 1.8686203956604004,
  "theta_neg_4_2_p95_abs_err_deg": 3.2999675273895264,
  "theta_neg_4_2_max_abs_err_deg": 10.29334545135498,
  "theta_neg_4_2_bias_deg": 0.29080721735954285,
  "theta_neg_4_2_n": 145.0
}
```
