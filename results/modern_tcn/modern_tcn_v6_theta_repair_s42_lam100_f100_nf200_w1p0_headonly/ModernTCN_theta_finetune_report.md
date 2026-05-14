# ModernTCN theta-head fine-tune report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_longrun_diag2steer_seed42\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 105
- train seconds: 168.5

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
  "select_theta_flat_p95_weight": 5.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 2.0,
  "select_theta_flat_bias_target_deg": 0.2
}
```

## Test Metrics

| metric | value |
|---|---:|
| acc_main | 0.9778 |
| acc_turn | 0.9334 |
| acc_turn_transition | 0.6344 |
| turn_left_recall | 0.8630 |
| theta_mae_deg | 0.5601 |
| theta_abs_le_8_mae_deg | 0.5601 |
| theta_abs_le_10_mae_deg | 0.5601 |
| theta_pos_6_8_mae_deg | 1.0897 |
| theta_pos_6_8_bias_deg | -0.9785 |
| theta_neg_8_6_mae_deg | 0.3918 |
| theta_neg_8_6_bias_deg | 0.0455 |
| theta_flat_abs_p95_deg | 1.9359 |
| theta_flat_bias_deg | -0.1104 |
| theta_near_flat_abs_p95_deg | 2.2979 |
| theta_near_flat_bias_deg | -0.0885 |
| theta_flat_turn_abs_p95_deg | 1.6169 |
| flat_recall | 0.9908 |
| slope_recall | 0.9529 |
| slope_sign_acc | 0.3293 |

## Validation Best Metrics

```json
{
  "loss_total": 0.33031768821127133,
  "acc_main": 0.9772497472194136,
  "acc_turn": 0.9292214357937311,
  "acc_turn_pure": 0.949678800856531,
  "acc_turn_transition": 0.5818181818181818,
  "flat_recall": 0.9924965893587995,
  "stall_recall": 0.8939393939393939,
  "slope_recall": 0.9394618834080718,
  "recall_main": [
    0.9924965893587995,
    0.8939393939393939,
    0.9394618834080718
  ],
  "turn_right_recall": 0.9235127478753541,
  "turn_straight_recall": 0.9502999143101971,
  "turn_left_recall": 0.8799126637554585,
  "recall_turn": [
    0.9235127478753541,
    0.9502999143101971,
    0.8799126637554585
  ],
  "cm_turn": [
    [
      326,
      16,
      11
    ],
    [
      41,
      1109,
      17
    ],
    [
      4,
      51,
      403
    ]
  ],
  "n_turn_transition": 110,
  "n_turn_pure": 1868,
  "cm_main": [
    [
      1455,
      3,
      8
    ],
    [
      5,
      59,
      2
    ],
    [
      27,
      0,
      419
    ]
  ],
  "main_confidence_mean": 0.9947603096777267,
  "main_confidence_error_mean": 0.9330638335287249,
  "main_low_conf_0p60_ratio": 0.0025278058645096056,
  "main_low_conf_0p70_ratio": 0.00455005055611729,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 5,
      "error_rate": 0.2,
      "mean_confidence": 0.4962799581816709
    },
    {
      "bin": "[0.60,0.70)",
      "n": 4,
      "error_rate": 0.5,
      "mean_confidence": 0.663867458310124
    },
    {
      "bin": "[0.70,0.80)",
      "n": 8,
      "error_rate": 0.5,
      "mean_confidence": 0.7604079528524142
    },
    {
      "bin": "[0.80,0.90)",
      "n": 15,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.8574464482269416
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1946,
      "error_rate": 0.01695786228160329,
      "mean_confidence": 0.9987430948469533
    }
  ],
  "turn_confidence_mean": 0.9531343225830688,
  "turn_confidence_error_mean": 0.8471502427005299,
  "turn_low_conf_0p60_ratio": 0.01870576339737108,
  "turn_low_conf_0p70_ratio": 0.03741152679474216,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 37,
      "error_rate": 0.43243243243243246,
      "mean_confidence": 0.5335223696027127
    },
    {
      "bin": "[0.60,0.70)",
      "n": 37,
      "error_rate": 0.35135135135135137,
      "mean_confidence": 0.6581468671899707
    },
    {
      "bin": "[0.70,0.80)",
      "n": 100,
      "error_rate": 0.15,
      "mean_confidence": 0.7600573415029923
    },
    {
      "bin": "[0.80,0.90)",
      "n": 130,
      "error_rate": 0.17692307692307693,
      "mean_confidence": 0.8588424650569054
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1674,
      "error_rate": 0.04360812425328554,
      "mean_confidence": 0.987785348685952
    }
  ],
  "theta_mae_rad": 0.009299475699663162,
  "theta_mae_deg": 0.5328207015991211,
  "uphill_recall": 0.8498293515358362,
  "downhill_recall": 0.7245762711864406,
  "slope_sign_acc": 0.26359832635983266,
  "theta_flat_mae_deg": 0.43678855895996094,
  "theta_flat_abs_p95_deg": 1.6165766716003418,
  "theta_flat_bias_deg": -0.05292276293039322,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.46270227432250977,
  "theta_near_flat_abs_p95_deg": 1.8827383518218994,
  "theta_near_flat_bias_deg": -0.027063805609941483,
  "theta_near_flat_n": 1472.0,
  "theta_flat_turn_mae_deg": 0.439486563205719,
  "theta_flat_turn_abs_p95_deg": 1.3760331869125366,
  "theta_flat_turn_bias_deg": -0.027332590892910957,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.5328207015991211,
  "theta_slope_control_abs_p95_deg": 5.566381454467773,
  "theta_slope_control_bias_deg": -0.04994264617562294,
  "theta_slope_control_n": 1912.0,
  "theta_abs_le_8_mae_deg": 0.5328207015991211,
  "theta_abs_le_8_rmse_deg": 1.0589385032653809,
  "theta_abs_le_8_p95_abs_err_deg": 1.8886771202087402,
  "theta_abs_le_8_bias_deg": -0.04994264617562294,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.5328207015991211,
  "theta_abs_le_10_rmse_deg": 1.0589385032653809,
  "theta_abs_le_10_p95_abs_err_deg": 1.8886771202087402,
  "theta_abs_le_10_bias_deg": -0.04994264617562294,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.9369327425956726,
  "theta_pos_6_8_rmse_deg": 1.0145083665847778,
  "theta_pos_6_8_p95_abs_err_deg": 1.5401098728179932,
  "theta_pos_6_8_bias_deg": -0.860846996307373,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.42323458194732666,
  "theta_neg_8_6_rmse_deg": 0.4967189133167267,
  "theta_neg_8_6_p95_abs_err_deg": 0.7774854302406311,
  "theta_neg_8_6_bias_deg": 0.043608408421278,
  "theta_neg_8_6_n": 47.0
}
```
