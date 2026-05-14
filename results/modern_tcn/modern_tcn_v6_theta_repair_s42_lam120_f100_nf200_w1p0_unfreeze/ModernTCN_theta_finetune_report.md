# ModernTCN theta-head fine-tune report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_longrun_diag2steer_seed42\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 79
- train seconds: 135.0

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
  "lambda_theta": 1.2,
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
| acc_main | 0.9783 |
| acc_turn | 0.9408 |
| acc_turn_transition | 0.6989 |
| turn_left_recall | 0.8760 |
| theta_mae_deg | 0.4906 |
| theta_abs_le_8_mae_deg | 0.4906 |
| theta_abs_le_10_mae_deg | 0.4906 |
| theta_pos_6_8_mae_deg | 0.5310 |
| theta_pos_6_8_bias_deg | -0.1825 |
| theta_neg_8_6_mae_deg | 0.3880 |
| theta_neg_8_6_bias_deg | 0.2578 |
| theta_flat_abs_p95_deg | 2.0334 |
| theta_flat_bias_deg | -0.0701 |
| theta_near_flat_abs_p95_deg | 2.1599 |
| theta_near_flat_bias_deg | -0.0457 |
| theta_flat_turn_abs_p95_deg | 1.8525 |
| flat_recall | 0.9939 |
| slope_recall | 0.9473 |
| slope_sign_acc | 0.3288 |

## Validation Best Metrics

```json
{
  "loss_total": 0.5497434292030046,
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
  "theta_mae_rad": 0.008583523333072662,
  "theta_mae_deg": 0.49179962277412415,
  "uphill_recall": 0.8498293515358362,
  "downhill_recall": 0.6991525423728814,
  "slope_sign_acc": 0.2583682008368201,
  "theta_flat_mae_deg": 0.4356469213962555,
  "theta_flat_abs_p95_deg": 1.8429954051971436,
  "theta_flat_bias_deg": -0.10482362657785416,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.4438745081424713,
  "theta_near_flat_abs_p95_deg": 1.9011623859405518,
  "theta_near_flat_bias_deg": -0.085201196372509,
  "theta_near_flat_n": 1472.0,
  "theta_flat_turn_mae_deg": 0.4087933301925659,
  "theta_flat_turn_abs_p95_deg": 1.3726099729537964,
  "theta_flat_turn_bias_deg": -0.08060983568429947,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.49179962277412415,
  "theta_slope_control_abs_p95_deg": 5.690699577331543,
  "theta_slope_control_bias_deg": -0.047911107540130615,
  "theta_slope_control_n": 1912.0,
  "theta_abs_le_8_mae_deg": 0.49179959297180176,
  "theta_abs_le_8_rmse_deg": 1.1113595962524414,
  "theta_abs_le_8_p95_abs_err_deg": 2.0833802223205566,
  "theta_abs_le_8_bias_deg": -0.04791111499071121,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.49179959297180176,
  "theta_abs_le_10_rmse_deg": 1.1113595962524414,
  "theta_abs_le_10_p95_abs_err_deg": 2.0833802223205566,
  "theta_abs_le_10_bias_deg": -0.04791111499071121,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.7731125354766846,
  "theta_pos_6_8_rmse_deg": 0.9860507249832153,
  "theta_pos_6_8_p95_abs_err_deg": 1.8366256952285767,
  "theta_pos_6_8_bias_deg": -0.6534903645515442,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.33325496315956116,
  "theta_neg_8_6_rmse_deg": 0.40095555782318115,
  "theta_neg_8_6_p95_abs_err_deg": 0.6364365220069885,
  "theta_neg_8_6_bias_deg": 0.18085800111293793,
  "theta_neg_8_6_n": 47.0
}
```
