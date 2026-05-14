# ModernTCN theta-head fine-tune report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 2
- train seconds: 41.3

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
  "lambda_theta_flat_excess": 180.0,
  "lambda_theta_near_flat_excess": 180.0,
  "lambda_theta_true_zero_excess": 260.0,
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
  "theta_gate_floor": 0.15,
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
| acc_turn | 0.9408 |
| acc_turn_transition | 0.6989 |
| turn_left_recall | 0.8760 |
| theta_mae_deg | 0.5209 |
| theta_abs_le_8_mae_deg | 0.5209 |
| theta_abs_le_8_p95_abs_err_deg | 1.6448 |
| theta_abs_le_8_max_abs_err_deg | 9.3690 |
| theta_abs_le_10_mae_deg | 0.5209 |
| theta_abs_le_10_p95_abs_err_deg | 1.6448 |
| theta_pos_6_8_mae_deg | 1.4171 |
| theta_pos_6_8_p95_abs_err_deg | 4.2851 |
| theta_pos_6_8_bias_deg | 1.2450 |
| theta_neg_8_6_mae_deg | 1.0417 |
| theta_neg_8_6_p95_abs_err_deg | 2.5213 |
| theta_neg_8_6_bias_deg | 0.9401 |
| theta_active_abs_ge_2_mae_deg | 0.9357 |
| theta_active_abs_ge_2_p95_abs_err_deg | 3.3149 |
| theta_neg_4_2_mae_deg | 1.9142 |
| theta_neg_4_2_p95_abs_err_deg | 4.2073 |
| theta_neg_4_2_bias_deg | 1.5534 |
| theta_flat_abs_p95_deg | 0.5245 |
| theta_flat_abs_max_deg | 3.6878 |
| theta_flat_bias_deg | -0.2334 |
| theta_near_flat_abs_p95_deg | 0.5295 |
| theta_near_flat_abs_max_deg | 3.6878 |
| theta_near_flat_bias_deg | -0.2118 |
| theta_true_zero_abs_p95_deg | 0.5358 |
| theta_true_zero_abs_max_deg | 3.6878 |
| theta_true_zero_bias_deg | -0.2110 |
| theta_flat_turn_abs_p95_deg | 0.4597 |
| flat_recall | 0.9939 |
| slope_recall | 0.9473 |
| slope_sign_acc | 0.3130 |

## Validation Best Metrics

```json
{
  "loss_total": 0.633192052674848,
  "acc_main": 0.9752275025278059,
  "acc_turn": 0.9327603640040445,
  "acc_turn_pure": 0.9512847965738758,
  "acc_turn_transition": 0.6181818181818182,
  "flat_recall": 0.9938608458390177,
  "stall_recall": 0.8787878787878788,
  "slope_recall": 0.9282511210762332,
  "recall_main": [
    0.9938608458390177,
    0.8787878787878788,
    0.9282511210762332
  ],
  "turn_right_recall": 0.9150141643059491,
  "turn_straight_recall": 0.9545844044558698,
  "turn_left_recall": 0.8908296943231441,
  "recall_turn": [
    0.9150141643059491,
    0.9545844044558698,
    0.8908296943231441
  ],
  "cm_turn": [
    [
      323,
      20,
      10
    ],
    [
      35,
      1114,
      18
    ],
    [
      1,
      49,
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
      58,
      3
    ],
    [
      32,
      0,
      414
    ]
  ],
  "main_confidence_mean": 0.9979510026541858,
  "main_confidence_error_mean": 0.9649350680938675,
  "main_low_conf_0p60_ratio": 0.0015166835187057635,
  "main_low_conf_0p70_ratio": 0.0020222446916076846,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 3,
      "error_rate": 0.6666666666666666,
      "mean_confidence": 0.5481074428149125
    },
    {
      "bin": "[0.60,0.70)",
      "n": 1,
      "error_rate": 0.0,
      "mean_confidence": 0.6487723724179127
    },
    {
      "bin": "[0.70,0.80)",
      "n": 2,
      "error_rate": 0.0,
      "mean_confidence": 0.763203705512334
    },
    {
      "bin": "[0.80,0.90)",
      "n": 6,
      "error_rate": 0.6666666666666666,
      "mean_confidence": 0.8670164087339859
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1966,
      "error_rate": 0.02187182095625636,
      "mean_confidence": 0.9994534499927203
    }
  ],
  "turn_confidence_mean": 0.9567893120720095,
  "turn_confidence_error_mean": 0.8434269652814348,
  "turn_low_conf_0p60_ratio": 0.01870576339737108,
  "turn_low_conf_0p70_ratio": 0.038928210313447925,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 37,
      "error_rate": 0.43243243243243246,
      "mean_confidence": 0.5396151696726506
    },
    {
      "bin": "[0.60,0.70)",
      "n": 40,
      "error_rate": 0.45,
      "mean_confidence": 0.6512252582280398
    },
    {
      "bin": "[0.70,0.80)",
      "n": 65,
      "error_rate": 0.13846153846153847,
      "mean_confidence": 0.7356352151579728
    },
    {
      "bin": "[0.80,0.90)",
      "n": 129,
      "error_rate": 0.14728682170542637,
      "mean_confidence": 0.8598382024891184
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1707,
      "error_rate": 0.04159343878148799,
      "mean_confidence": 0.9887399358904865
    }
  ],
  "theta_mae_rad": 0.008755174465477467,
  "theta_mae_deg": 0.5016345381736755,
  "uphill_recall": 0.8498293515358362,
  "downhill_recall": 0.6991525423728814,
  "slope_sign_acc": 0.25052301255230125,
  "theta_flat_mae_deg": 0.3374575972557068,
  "theta_flat_abs_p95_deg": 0.4713815152645111,
  "theta_flat_abs_max_deg": 4.904329776763916,
  "theta_flat_bias_deg": -0.24012945592403412,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.3193647265434265,
  "theta_near_flat_abs_p95_deg": 0.48392197489738464,
  "theta_near_flat_abs_max_deg": 7.1388773918151855,
  "theta_near_flat_bias_deg": -0.2226579189300537,
  "theta_near_flat_n": 1472.0,
  "theta_true_zero_mae_deg": 0.31817322969436646,
  "theta_true_zero_abs_p95_deg": 0.48620426654815674,
  "theta_true_zero_abs_max_deg": 7.1388773918151855,
  "theta_true_zero_bias_deg": -0.21998579800128937,
  "theta_true_zero_n": 1433.0,
  "theta_flat_turn_mae_deg": 0.21309487521648407,
  "theta_flat_turn_abs_p95_deg": 0.406784325838089,
  "theta_flat_turn_abs_max_deg": 0.9721418619155884,
  "theta_flat_turn_bias_deg": -0.13023526966571808,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.5016345381736755,
  "theta_slope_control_abs_p95_deg": 5.627864360809326,
  "theta_slope_control_abs_max_deg": 9.460525512695312,
  "theta_slope_control_bias_deg": -0.04871327802538872,
  "theta_slope_control_n": 1912.0,
  "theta_all_mae_deg": 0.5016344785690308,
  "theta_all_rmse_deg": 0.8130106925964355,
  "theta_all_p95_abs_err_deg": 1.6218652725219727,
  "theta_all_max_abs_err_deg": 5.160704135894775,
  "theta_all_bias_deg": -0.04871327802538872,
  "theta_all_n": 1912.0,
  "theta_active_abs_ge_2_mae_deg": 1.0412832498550415,
  "theta_active_abs_ge_2_rmse_deg": 1.4724760055541992,
  "theta_active_abs_ge_2_p95_abs_err_deg": 3.373749256134033,
  "theta_active_abs_ge_2_max_abs_err_deg": 5.160704135894775,
  "theta_active_abs_ge_2_bias_deg": 0.5804707407951355,
  "theta_active_abs_ge_2_n": 446.0,
  "theta_abs_le_8_mae_deg": 0.5016344785690308,
  "theta_abs_le_8_rmse_deg": 0.8130106925964355,
  "theta_abs_le_8_p95_abs_err_deg": 1.6218652725219727,
  "theta_abs_le_8_max_abs_err_deg": 5.160704135894775,
  "theta_abs_le_8_bias_deg": -0.04871327802538872,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.5016344785690308,
  "theta_abs_le_10_rmse_deg": 0.8130106925964355,
  "theta_abs_le_10_p95_abs_err_deg": 1.6218652725219727,
  "theta_abs_le_10_max_abs_err_deg": 5.160704135894775,
  "theta_abs_le_10_bias_deg": -0.04871327802538872,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.7014402747154236,
  "theta_pos_6_8_rmse_deg": 0.8461057543754578,
  "theta_pos_6_8_p95_abs_err_deg": 1.6311776638031006,
  "theta_pos_6_8_max_abs_err_deg": 2.4373528957366943,
  "theta_pos_6_8_bias_deg": -0.5470439791679382,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.9776137471199036,
  "theta_neg_8_6_rmse_deg": 1.2570860385894775,
  "theta_neg_8_6_p95_abs_err_deg": 2.6093640327453613,
  "theta_neg_8_6_max_abs_err_deg": 3.0000338554382324,
  "theta_neg_8_6_bias_deg": 0.8587623238563538,
  "theta_neg_8_6_n": 47.0,
  "theta_neg_4_2_mae_deg": 1.5611910820007324,
  "theta_neg_4_2_rmse_deg": 2.0820817947387695,
  "theta_neg_4_2_p95_abs_err_deg": 3.869168519973755,
  "theta_neg_4_2_max_abs_err_deg": 4.448087215423584,
  "theta_neg_4_2_bias_deg": 1.3693757057189941,
  "theta_neg_4_2_n": 145.0
}
```
