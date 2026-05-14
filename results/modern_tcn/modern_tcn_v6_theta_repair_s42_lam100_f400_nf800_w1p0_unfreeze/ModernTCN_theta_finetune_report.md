# ModernTCN theta-head fine-tune report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_longrun_diag2steer_seed42\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 106
- train seconds: 192.9

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
  "lambda_theta_flat": 4.0,
  "lambda_theta_near_flat": 8.0,
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
| acc_main | 0.9773 |
| acc_turn | 0.9387 |
| acc_turn_transition | 0.6559 |
| turn_left_recall | 0.8708 |
| theta_mae_deg | 0.5101 |
| theta_abs_le_8_mae_deg | 0.5101 |
| theta_abs_le_10_mae_deg | 0.5101 |
| theta_pos_6_8_mae_deg | 0.7196 |
| theta_pos_6_8_bias_deg | -0.3700 |
| theta_neg_8_6_mae_deg | 0.3824 |
| theta_neg_8_6_bias_deg | 0.2079 |
| theta_flat_abs_p95_deg | 2.0906 |
| theta_flat_bias_deg | -0.0622 |
| theta_near_flat_abs_p95_deg | 2.2106 |
| theta_near_flat_bias_deg | -0.0537 |
| theta_flat_turn_abs_p95_deg | 1.5490 |
| flat_recall | 0.9939 |
| slope_recall | 0.9435 |
| slope_sign_acc | 0.3239 |

## Validation Best Metrics

```json
{
  "loss_total": 0.49953924401223476,
  "acc_main": 0.9762386248736097,
  "acc_turn": 0.9302325581395349,
  "acc_turn_pure": 0.9512847965738758,
  "acc_turn_transition": 0.5727272727272728,
  "flat_recall": 0.9938608458390177,
  "stall_recall": 0.8939393939393939,
  "slope_recall": 0.9304932735426009,
  "recall_main": [
    0.9938608458390177,
    0.8939393939393939,
    0.9304932735426009
  ],
  "turn_right_recall": 0.9121813031161473,
  "turn_straight_recall": 0.9528706083976007,
  "turn_left_recall": 0.8864628820960698,
  "recall_turn": [
    0.9121813031161473,
    0.9528706083976007,
    0.8864628820960698
  ],
  "cm_turn": [
    [
      322,
      20,
      11
    ],
    [
      36,
      1112,
      19
    ],
    [
      1,
      51,
      406
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
      31,
      0,
      415
    ]
  ],
  "main_confidence_mean": 0.9970541390254849,
  "main_confidence_error_mean": 0.9607507432280685,
  "main_low_conf_0p60_ratio": 0.0020222446916076846,
  "main_low_conf_0p70_ratio": 0.003033367037411527,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 4,
      "error_rate": 0.5,
      "mean_confidence": 0.5747291158358997
    },
    {
      "bin": "[0.60,0.70)",
      "n": 2,
      "error_rate": 0.0,
      "mean_confidence": 0.6878261374342554
    },
    {
      "bin": "[0.70,0.80)",
      "n": 8,
      "error_rate": 0.25,
      "mean_confidence": 0.7457908984933285
    },
    {
      "bin": "[0.80,0.90)",
      "n": 5,
      "error_rate": 0.4,
      "mean_confidence": 0.8650793989518346
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1959,
      "error_rate": 0.02092904543134252,
      "mean_confidence": 0.9995950965142885
    }
  ],
  "turn_confidence_mean": 0.9555821846373788,
  "turn_confidence_error_mean": 0.8292792659508951,
  "turn_low_conf_0p60_ratio": 0.01870576339737108,
  "turn_low_conf_0p70_ratio": 0.03538928210313448,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 37,
      "error_rate": 0.5945945945945946,
      "mean_confidence": 0.5363271194839635
    },
    {
      "bin": "[0.60,0.70)",
      "n": 33,
      "error_rate": 0.45454545454545453,
      "mean_confidence": 0.6510774094229481
    },
    {
      "bin": "[0.70,0.80)",
      "n": 85,
      "error_rate": 0.15294117647058825,
      "mean_confidence": 0.74742766121262
    },
    {
      "bin": "[0.80,0.90)",
      "n": 123,
      "error_rate": 0.17886178861788618,
      "mean_confidence": 0.8625302900097891
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1700,
      "error_rate": 0.03882352941176471,
      "mean_confidence": 0.9877584272979967
    }
  ],
  "theta_mae_rad": 0.00869176909327507,
  "theta_mae_deg": 0.49800166487693787,
  "uphill_recall": 0.8498293515358362,
  "downhill_recall": 0.7033898305084746,
  "slope_sign_acc": 0.2567991631799163,
  "theta_flat_mae_deg": 0.39837509393692017,
  "theta_flat_abs_p95_deg": 1.6029930114746094,
  "theta_flat_bias_deg": -0.0929512232542038,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.3975411057472229,
  "theta_near_flat_abs_p95_deg": 1.6875805854797363,
  "theta_near_flat_bias_deg": -0.082339346408844,
  "theta_near_flat_n": 1472.0,
  "theta_flat_turn_mae_deg": 0.34612488746643066,
  "theta_flat_turn_abs_p95_deg": 1.239664912223816,
  "theta_flat_turn_bias_deg": -0.05476459860801697,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.49800166487693787,
  "theta_slope_control_abs_p95_deg": 5.7752509117126465,
  "theta_slope_control_bias_deg": -0.05427578091621399,
  "theta_slope_control_n": 1912.0,
  "theta_abs_le_8_mae_deg": 0.4980016350746155,
  "theta_abs_le_8_rmse_deg": 1.112648606300354,
  "theta_abs_le_8_p95_abs_err_deg": 1.9488344192504883,
  "theta_abs_le_8_bias_deg": -0.05427579581737518,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.4980016350746155,
  "theta_abs_le_10_rmse_deg": 1.112648606300354,
  "theta_abs_le_10_p95_abs_err_deg": 1.9488344192504883,
  "theta_abs_le_10_bias_deg": -0.05427579581737518,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.8539910316467285,
  "theta_pos_6_8_rmse_deg": 1.2003384828567505,
  "theta_pos_6_8_p95_abs_err_deg": 3.170274257659912,
  "theta_pos_6_8_bias_deg": -0.7559045553207397,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.3372708261013031,
  "theta_neg_8_6_rmse_deg": 0.4332544803619385,
  "theta_neg_8_6_p95_abs_err_deg": 0.8666146993637085,
  "theta_neg_8_6_bias_deg": 0.13314010202884674,
  "theta_neg_8_6_n": 47.0
}
```
