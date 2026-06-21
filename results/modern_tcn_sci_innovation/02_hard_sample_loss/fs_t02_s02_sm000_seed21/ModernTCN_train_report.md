# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
- loss_mode: `fixed`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- vehicle: `diagonal_dual_steer_drive_agv`; active=`LF,RR`; passive=`RF,LR`
- feature_policy: `keep_current_algorithm_inputs_unchanged`
- label_time_policy: `current_window_end`, horizon_steps=0
- split: 使用 MAT 文件已有 run-level split，不重划分。
- scaler: 使用 MAT 文件已有归一化后 X，不重新拟合。
- confidence_policy: `derive_classification_confidence_from_softmax_and_export`
- input: `[batch, time=128, feature=22]`
- output: `logits_main`, `logits_turn`, `theta_hat`

## E2 hard-sample focal settings

- lambda_transition_focal: `0.2`
- lambda_stall_focal: `0.2`
- lambda_theta_smooth: `0.0`
- focal_gamma: `2.0`
- theta_smooth_mode: `off`
- theta_smooth_status: `disabled_contract_limited`

## 配置

```json
{
  "input_dim": 22,
  "seq_len": 128,
  "channels": 64,
  "blocks": 5,
  "kernel_size": 31,
  "temporal_padding": "same",
  "dropout": 0.15,
  "command_dropout_prob": 0.0,
  "command_dropout_start_index": -1,
  "command_dropout_feature_count": 0,
  "command_dropout_mode": "window_block",
  "expansion": 2,
  "readout_input_stats": true,
  "turn_head_source": "full",
  "turn_feature_indices": [
    0,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    13,
    21
  ],
  "lambda_turn": 0.2,
  "lambda_theta": 0.55,
  "lambda_theta_flat": 0.12,
  "theta_flat_loss_mode": "near_zero",
  "theta_flat_zero_tol_deg": 0.3,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 0.05,
  "lambda_theta_flat_excess": 0.0,
  "lambda_theta_near_flat_excess": 0.0,
  "lambda_theta_true_zero_excess": 0.1,
  "lambda_theta_active_excess": 0.1,
  "lambda_theta_small_neg": 0.0,
  "lambda_theta_small_neg_excess": 0.0,
  "lambda_turn_release": 0.0,
  "lambda_false_turn_straight": 0.0,
  "lambda_transition_focal": 0.2,
  "lambda_stall_focal": 0.2,
  "lambda_theta_smooth": 0.0,
  "focal_gamma": 2.0,
  "theta_smooth_mode": "off",
  "theta_excess_target_deg": 1.0,
  "theta_flat_excess_target_deg": 0.5,
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
    1.4,
    0.8,
    1.4
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 2.5,
  "select_turn_weight": 0.55,
  "select_turn_transition_weight": 1.2,
  "select_turn_transition_target": 0.82,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.88,
  "select_turn_lr_weight": 0.6,
  "select_turn_lr_target": 0.88,
  "select_stall_weight": 0.0,
  "select_stall_target": 0.7,
  "select_theta_weight": 0.3,
  "select_theta_ref_deg": 2.0,
  "select_theta_p95_weight": 0.8,
  "select_theta_p95_target_deg": 1.2,
  "select_theta_flat_p95_weight": 0.35,
  "select_theta_flat_p95_target_deg": 0.7,
  "select_theta_near_flat_p95_weight": 0.2,
  "select_theta_near_flat_p95_target_deg": 0.7,
  "select_theta_true_zero_p95_weight": 0.45,
  "select_theta_true_zero_p95_target_deg": 0.5,
  "select_theta_flat_peak_weight": 0.0,
  "select_theta_flat_peak_target_deg": 3.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 0.7,
  "select_theta_edge_p95_target_deg": 1.5,
  "select_theta_small_nonzero_p95_weight": 0.8,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.3,
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9697 |
| acc_turn | 0.4944 |
| acc_turn_pure | 0.5036 |
| acc_turn_transition | 0.4545 |
| main_confidence_mean | 0.9745 |
| main_low_conf_0p60_ratio | 0.0111 |
| main_low_conf_0p70_ratio | 0.0272 |
| turn_confidence_mean | 0.5965 |
| turn_low_conf_0p60_ratio | 0.5822 |
| turn_low_conf_0p70_ratio | 0.7762 |
| turn_right_recall | 0.4556 |
| turn_straight_recall | 0.4868 |
| turn_left_recall | 0.5471 |
| theta_mae_deg | 0.8160 |
| theta_abs_le_10_p95_abs_err_deg | 2.3671 |
| theta_neg_10_8_p95_abs_err_deg | 1.7866 |
| theta_pos_8_10_p95_abs_err_deg | 3.4368 |
| theta_abs_le_8_p95_abs_err_deg | 2.2758 |
| theta_neg_8_6_p95_abs_err_deg | 2.2588 |
| theta_pos_6_8_p95_abs_err_deg | 1.8562 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.4447 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.9603 |
| theta_flat_abs_p95_deg | 3.1531 |
| theta_flat_bias_deg | 0.0606 |
| theta_near_flat_abs_p95_deg | 2.1674 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.0868 |
| theta_flat_turn_abs_p95_deg | 1.8976 |
| flat_recall | 0.9775 |
| stall_recall | 0.6667 |
| slope_recall | 0.9782 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1146 |
| uphill_recall | 0.7552 |
| downhill_recall | 0.7889 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    739,
    0,
    17
  ],
  [
    11,
    64,
    21
  ],
  [
    47,
    13,
    2690
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    364,
    283,
    152
  ],
  [
    363,
    941,
    629
  ],
  [
    182,
    212,
    476
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.266881 |
| test_loss_turn_bundle_base | 0.212793 |
| test_loss_theta_bundle_base | 0.000266 |
| test_loss_transition_focal_raw | 0.582417 |
| test_loss_transition_focal_weighted | 0.116483 |
| test_loss_stall_focal_raw | 2.900883 |
| test_loss_stall_focal_weighted | 0.580177 |
| test_loss_theta_smooth | 0.000000 |

- best_epoch: 24
- train_seconds: 159.6

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 40 | 0.3750 | 0.5439 |
| [0.60,0.70) | 58 | 0.2241 | 0.6412 |
| [0.70,0.80) | 72 | 0.2083 | 0.7529 |
| [0.80,0.90) | 93 | 0.1505 | 0.8527 |
| [0.90,1.00) | 3339 | 0.0156 | 0.9937 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 2097 | 0.5660 | 0.4917 |
| [0.60,0.70) | 699 | 0.5608 | 0.6461 |
| [0.70,0.80) | 375 | 0.4213 | 0.7508 |
| [0.80,0.90) | 235 | 0.2638 | 0.8431 |
| [0.90,1.00) | 196 | 0.1122 | 0.9507 |


## 验证集最佳点

```json
{
  "loss_total": 0.9470970297053315,
  "acc_main": 0.9453315290933694,
  "acc_turn": 0.5420838971583221,
  "acc_turn_pure": 0.5460504752540151,
  "acc_turn_transition": 0.5232919254658385,
  "false_turn_straight": 0.5161122661122661,
  "flat_recall": 0.9619482496194824,
  "stall_recall": 0.5714285714285714,
  "slope_recall": 0.9469292389853138,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9619482496194824,
    0.5714285714285714,
    0.9469292389853138
  ],
  "turn_right_recall": 0.5296208530805687,
  "turn_straight_recall": 0.4838877338877339,
  "turn_left_recall": 0.674217907227616,
  "recall_turn": [
    0.5296208530805687,
    0.4838877338877339,
    0.674217907227616
  ],
  "cm_turn": [
    [
      447,
      229,
      168
    ],
    [
      437,
      931,
      556
    ],
    [
      118,
      184,
      625
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      632,
      0,
      25
    ],
    [
      0,
      24,
      18
    ],
    [
      148,
      11,
      2837
    ]
  ],
  "main_confidence_mean": 0.9614826231062672,
  "main_confidence_error_mean": 0.7528722287764926,
  "main_low_conf_0p60_ratio": 0.0530446549391069,
  "main_low_conf_0p70_ratio": 0.06387009472259811,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 196,
      "error_rate": 0.4642857142857143,
      "mean_confidence": 0.5511030930581589
    },
    {
      "bin": "[0.60,0.70)",
      "n": 40,
      "error_rate": 0.2,
      "mean_confidence": 0.6634545521875186
    },
    {
      "bin": "[0.70,0.80)",
      "n": 42,
      "error_rate": 0.2857142857142857,
      "mean_confidence": 0.7509170214892539
    },
    {
      "bin": "[0.80,0.90)",
      "n": 102,
      "error_rate": 0.1568627450980392,
      "mean_confidence": 0.8564036294699559
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3315,
      "error_rate": 0.02262443438914027,
      "mean_confidence": 0.9952435049599617
    }
  ],
  "turn_confidence_mean": 0.6108715976177618,
  "turn_confidence_error_mean": 0.5678240427776305,
  "turn_low_conf_0p60_ratio": 0.5299052774018944,
  "turn_low_conf_0p70_ratio": 0.7339648173207036,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 1958,
      "error_rate": 0.54341164453524,
      "mean_confidence": 0.4908091640359737
    },
    {
      "bin": "[0.60,0.70)",
      "n": 754,
      "error_rate": 0.46153846153846156,
      "mean_confidence": 0.6473147347420393
    },
    {
      "bin": "[0.70,0.80)",
      "n": 435,
      "error_rate": 0.38620689655172413,
      "mean_confidence": 0.7443986071930652
    },
    {
      "bin": "[0.80,0.90)",
      "n": 323,
      "error_rate": 0.32507739938080493,
      "mean_confidence": 0.8421839397150191
    },
    {
      "bin": "[0.90,1.00)",
      "n": 225,
      "error_rate": 0.03111111111111111,
      "mean_confidence": 0.9433426371678274
    }
  ],
  "theta_mae_rad": 0.017349060624837875,
  "theta_mae_deg": 0.9940279126167297,
  "uphill_recall": 0.7735849056603774,
  "downhill_recall": 0.7936596218020022,
  "slope_sign_acc": 0.9674240350396934,
  "theta_flat_mae_deg": 1.1886030435562134,
  "theta_flat_abs_p95_deg": 3.1309564113616943,
  "theta_flat_abs_max_deg": 7.673685550689697,
  "theta_flat_bias_deg": 0.564279317855835,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5833978652954102,
  "theta_near_flat_abs_p95_deg": 3.249711275100708,
  "theta_near_flat_abs_max_deg": 7.673685550689697,
  "theta_near_flat_bias_deg": 1.1943196058273315,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.608602523803711,
  "theta_flat_turn_abs_p95_deg": 3.46734881401062,
  "theta_flat_turn_abs_max_deg": 7.673685550689697,
  "theta_flat_turn_bias_deg": 1.1547355651855469,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9940279126167297,
  "theta_slope_control_abs_p95_deg": 9.708102226257324,
  "theta_slope_control_abs_max_deg": 13.196510314941406,
  "theta_slope_control_bias_deg": 0.04659320041537285,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.9940279722213745,
  "theta_all_rmse_deg": 1.3731818199157715,
  "theta_all_p95_abs_err_deg": 2.6772801876068115,
  "theta_all_max_abs_err_deg": 9.243603706359863,
  "theta_all_bias_deg": 0.04659320041537285,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.9513591527938843,
  "theta_active_abs_ge_2_rmse_deg": 1.307995319366455,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.6765897274017334,
  "theta_active_abs_ge_2_max_abs_err_deg": 9.243603706359863,
  "theta_active_abs_ge_2_bias_deg": -0.06693141162395477,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 1.0283697843551636,
  "theta_abs_le_8_rmse_deg": 1.4120336771011353,
  "theta_abs_le_8_p95_abs_err_deg": 2.713421583175659,
  "theta_abs_le_8_max_abs_err_deg": 9.243603706359863,
  "theta_abs_le_8_bias_deg": 0.08593719452619553,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.9940279722213745,
  "theta_abs_le_10_rmse_deg": 1.3731818199157715,
  "theta_abs_le_10_p95_abs_err_deg": 2.6772801876068115,
  "theta_abs_le_10_max_abs_err_deg": 9.243603706359863,
  "theta_abs_le_10_bias_deg": 0.04659320041537285,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7143639922142029,
  "theta_pos_8_10_rmse_deg": 1.0103387832641602,
  "theta_pos_8_10_p95_abs_err_deg": 2.1387455463409424,
  "theta_pos_8_10_max_abs_err_deg": 4.977357864379883,
  "theta_pos_8_10_bias_deg": -0.12289417535066605,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.9862753748893738,
  "theta_neg_10_8_rmse_deg": 1.3581393957138062,
  "theta_neg_10_8_p95_abs_err_deg": 2.8865787982940674,
  "theta_neg_10_8_max_abs_err_deg": 6.74163818359375,
  "theta_neg_10_8_bias_deg": -0.11580956727266312,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.8381358981132507,
  "theta_pos_6_8_rmse_deg": 1.1721395254135132,
  "theta_pos_6_8_p95_abs_err_deg": 2.270477771759033,
  "theta_pos_6_8_max_abs_err_deg": 5.4399943351745605,
  "theta_pos_6_8_bias_deg": -0.08526501804590225,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.1435843706130981,
  "theta_neg_8_6_rmse_deg": 1.4913296699523926,
  "theta_neg_8_6_p95_abs_err_deg": 2.6266698837280273,
  "theta_neg_8_6_max_abs_err_deg": 9.243603706359863,
  "theta_neg_8_6_bias_deg": -0.8173618912696838,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.9252039194107056,
  "theta_neg_4_2_rmse_deg": 1.2782032489776611,
  "theta_neg_4_2_p95_abs_err_deg": 2.770432710647583,
  "theta_neg_4_2_max_abs_err_deg": 7.821513652801514,
  "theta_neg_4_2_bias_deg": -0.2943865656852722,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.7110359072685242,
  "theta_neg_2_0p5_rmse_deg": 0.9870327711105347,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.98147714138031,
  "theta_neg_2_0p5_max_abs_err_deg": 5.348873138427734,
  "theta_neg_2_0p5_bias_deg": -0.2514651417732239,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1695204973220825,
  "theta_pos_0p5_2_rmse_deg": 1.3633190393447876,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.2394440174102783,
  "theta_pos_0p5_2_max_abs_err_deg": 5.842947006225586,
  "theta_pos_0p5_2_bias_deg": 0.5046696662902832,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.26598945759307385,
  "loss_turn": 1.0381223284020638,
  "loss_theta": 0.000574605732920538,
  "loss_main_bundle_base": 0.26598945759307385,
  "loss_turn_bundle_base": 0.20762446904617976,
  "loss_theta_bundle_base": 0.00037147410413853986,
  "loss_main_bundle": 0.6236905679167204,
  "loss_turn_bundle": 0.32303498734963276,
  "loss_theta_bundle": 0.00037147410413853986,
  "loss_theta_flat": 0.00023242019555444484,
  "loss_theta_near_flat": 0.0013373939517673725,
  "loss_theta_error_excess": 0.00020312305591201489,
  "loss_theta_flat_excess": 0.00010926794961339186,
  "loss_theta_near_flat_excess": 0.0009263814413017077,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.0001739436787443175,
  "loss_theta_small_neg": 0.0004879609418274263,
  "loss_theta_small_neg_excess": 0.00016274350906974455,
  "loss_turn_release": 0.38665785837076677,
  "loss_false_turn_straight": 0.3180768003321791,
  "loss_transition_focal_raw": 0.5770525897630012,
  "loss_transition_focal_weighted": 0.11541051900919139,
  "loss_stall_focal_raw": 1.788505513244208,
  "loss_stall_focal_weighted": 0.35770110657345294,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
