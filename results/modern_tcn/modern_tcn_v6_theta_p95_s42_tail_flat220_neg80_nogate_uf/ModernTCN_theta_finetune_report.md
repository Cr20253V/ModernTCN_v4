# ModernTCN theta-head fine-tune report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 96
- train seconds: 190.6

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
  "theta_gate_mode": "none",
  "theta_gate_power": 1.0,
  "theta_gate_floor": 0.0,
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
| acc_turn | 0.9382 |
| acc_turn_transition | 0.6667 |
| turn_left_recall | 0.8760 |
| theta_mae_deg | 0.4524 |
| theta_abs_le_8_mae_deg | 0.4524 |
| theta_abs_le_8_p95_abs_err_deg | 1.9220 |
| theta_abs_le_8_max_abs_err_deg | 8.3808 |
| theta_abs_le_10_mae_deg | 0.4524 |
| theta_abs_le_10_p95_abs_err_deg | 1.9220 |
| theta_pos_6_8_mae_deg | 0.5995 |
| theta_pos_6_8_p95_abs_err_deg | 1.2927 |
| theta_pos_6_8_bias_deg | 0.1041 |
| theta_neg_8_6_mae_deg | 0.3792 |
| theta_neg_8_6_p95_abs_err_deg | 1.0088 |
| theta_neg_8_6_bias_deg | 0.0366 |
| theta_active_abs_ge_2_mae_deg | 0.5090 |
| theta_active_abs_ge_2_p95_abs_err_deg | 1.8312 |
| theta_neg_4_2_mae_deg | 1.0895 |
| theta_neg_4_2_p95_abs_err_deg | 3.5870 |
| theta_neg_4_2_bias_deg | 0.2634 |
| theta_flat_abs_p95_deg | 1.9039 |
| theta_flat_abs_max_deg | 8.3808 |
| theta_flat_bias_deg | -0.0502 |
| theta_near_flat_abs_p95_deg | 2.0872 |
| theta_near_flat_abs_max_deg | 8.3808 |
| theta_near_flat_bias_deg | -0.0462 |
| theta_true_zero_abs_p95_deg | 2.1368 |
| theta_true_zero_abs_max_deg | 8.3808 |
| theta_true_zero_bias_deg | -0.0569 |
| theta_flat_turn_abs_p95_deg | 1.5236 |
| flat_recall | 0.9954 |
| slope_recall | 0.9435 |
| slope_sign_acc | 0.3272 |

## Validation Best Metrics

```json
{
  "loss_total": 0.6301750431649003,
  "acc_main": 0.974721941354904,
  "acc_turn": 0.9312436804853387,
  "acc_turn_pure": 0.9507494646680942,
  "acc_turn_transition": 0.6,
  "flat_recall": 0.9938608458390177,
  "stall_recall": 0.8787878787878788,
  "slope_recall": 0.9260089686098655,
  "recall_main": [
    0.9938608458390177,
    0.8787878787878788,
    0.9260089686098655
  ],
  "turn_right_recall": 0.9093484419263456,
  "turn_straight_recall": 0.9528706083976007,
  "turn_left_recall": 0.8930131004366813,
  "recall_turn": [
    0.9093484419263456,
    0.9528706083976007,
    0.8930131004366813
  ],
  "cm_turn": [
    [
      321,
      20,
      12
    ],
    [
      35,
      1112,
      20
    ],
    [
      0,
      49,
      409
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
      33,
      0,
      413
    ]
  ],
  "main_confidence_mean": 0.9971263018186207,
  "main_confidence_error_mean": 0.9638525946683568,
  "main_low_conf_0p60_ratio": 0.0010111223458038423,
  "main_low_conf_0p70_ratio": 0.0025278058645096056,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 2,
      "error_rate": 0.5,
      "mean_confidence": 0.5854030926997147
    },
    {
      "bin": "[0.60,0.70)",
      "n": 3,
      "error_rate": 0.0,
      "mean_confidence": 0.6362204084866655
    },
    {
      "bin": "[0.70,0.80)",
      "n": 3,
      "error_rate": 0.0,
      "mean_confidence": 0.7566433922390617
    },
    {
      "bin": "[0.80,0.90)",
      "n": 12,
      "error_rate": 0.5,
      "mean_confidence": 0.8515900006247427
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1958,
      "error_rate": 0.021961184882533197,
      "mean_confidence": 0.9993602387140748
    }
  ],
  "turn_confidence_mean": 0.9539699885557141,
  "turn_confidence_error_mean": 0.8383793978223137,
  "turn_low_conf_0p60_ratio": 0.01769464105156724,
  "turn_low_conf_0p70_ratio": 0.050050556117290194,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 35,
      "error_rate": 0.5714285714285714,
      "mean_confidence": 0.5455309469819113
    },
    {
      "bin": "[0.60,0.70)",
      "n": 64,
      "error_rate": 0.265625,
      "mean_confidence": 0.6553857297308396
    },
    {
      "bin": "[0.70,0.80)",
      "n": 57,
      "error_rate": 0.12280701754385964,
      "mean_confidence": 0.751657876638661
    },
    {
      "bin": "[0.80,0.90)",
      "n": 137,
      "error_rate": 0.16058394160583941,
      "mean_confidence": 0.8599036482526358
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1685,
      "error_rate": 0.04154302670623145,
      "mean_confidence": 0.9882866876777725
    }
  ],
  "theta_mae_rad": 0.007510253228247166,
  "theta_mae_deg": 0.4303057789802551,
  "uphill_recall": 0.8498293515358362,
  "downhill_recall": 0.6949152542372882,
  "slope_sign_acc": 0.25732217573221755,
  "theta_flat_mae_deg": 0.3630896210670471,
  "theta_flat_abs_p95_deg": 1.422851324081421,
  "theta_flat_abs_max_deg": 8.431964874267578,
  "theta_flat_bias_deg": -0.06219422444701195,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.35684987902641296,
  "theta_near_flat_abs_p95_deg": 1.4594519138336182,
  "theta_near_flat_abs_max_deg": 8.431964874267578,
  "theta_near_flat_bias_deg": -0.05340372771024704,
  "theta_near_flat_n": 1472.0,
  "theta_true_zero_mae_deg": 0.35298582911491394,
  "theta_true_zero_abs_p95_deg": 1.4495384693145752,
  "theta_true_zero_abs_max_deg": 8.431964874267578,
  "theta_true_zero_bias_deg": -0.04718403518199921,
  "theta_true_zero_n": 1433.0,
  "theta_flat_turn_mae_deg": 0.3380592465400696,
  "theta_flat_turn_abs_p95_deg": 1.0752227306365967,
  "theta_flat_turn_abs_max_deg": 8.431964874267578,
  "theta_flat_turn_bias_deg": -0.04052019491791725,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.4303057789802551,
  "theta_slope_control_abs_p95_deg": 5.796498775482178,
  "theta_slope_control_abs_max_deg": 8.431964874267578,
  "theta_slope_control_bias_deg": -0.010401949286460876,
  "theta_slope_control_n": 1912.0,
  "theta_all_mae_deg": 0.4303057789802551,
  "theta_all_rmse_deg": 0.9672959446907043,
  "theta_all_p95_abs_err_deg": 1.5683064460754395,
  "theta_all_max_abs_err_deg": 8.844852447509766,
  "theta_all_bias_deg": -0.010401953011751175,
  "theta_all_n": 1912.0,
  "theta_active_abs_ge_2_mae_deg": 0.6512450575828552,
  "theta_active_abs_ge_2_rmse_deg": 1.1395900249481201,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.3640224933624268,
  "theta_active_abs_ge_2_max_abs_err_deg": 8.844852447509766,
  "theta_active_abs_ge_2_bias_deg": 0.15983903408050537,
  "theta_active_abs_ge_2_n": 446.0,
  "theta_abs_le_8_mae_deg": 0.4303057789802551,
  "theta_abs_le_8_rmse_deg": 0.9672959446907043,
  "theta_abs_le_8_p95_abs_err_deg": 1.5683064460754395,
  "theta_abs_le_8_max_abs_err_deg": 8.844852447509766,
  "theta_abs_le_8_bias_deg": -0.010401953011751175,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.4303057789802551,
  "theta_abs_le_10_rmse_deg": 0.9672959446907043,
  "theta_abs_le_10_p95_abs_err_deg": 1.5683064460754395,
  "theta_abs_le_10_max_abs_err_deg": 8.844852447509766,
  "theta_abs_le_10_bias_deg": -0.010401953011751175,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.687325656414032,
  "theta_pos_6_8_rmse_deg": 0.8475949168205261,
  "theta_pos_6_8_p95_abs_err_deg": 1.3648871183395386,
  "theta_pos_6_8_max_abs_err_deg": 2.4197845458984375,
  "theta_pos_6_8_bias_deg": -0.573039710521698,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.3487701117992401,
  "theta_neg_8_6_rmse_deg": 0.4520975649356842,
  "theta_neg_8_6_p95_abs_err_deg": 0.9563959240913391,
  "theta_neg_8_6_max_abs_err_deg": 1.0591257810592651,
  "theta_neg_8_6_bias_deg": -0.05215074121952057,
  "theta_neg_8_6_n": 47.0,
  "theta_neg_4_2_mae_deg": 0.907204270362854,
  "theta_neg_4_2_rmse_deg": 1.7252334356307983,
  "theta_neg_4_2_p95_abs_err_deg": 3.711463212966919,
  "theta_neg_4_2_max_abs_err_deg": 8.844852447509766,
  "theta_neg_4_2_bias_deg": 0.5157367587089539,
  "theta_neg_4_2_n": 145.0
}
```
