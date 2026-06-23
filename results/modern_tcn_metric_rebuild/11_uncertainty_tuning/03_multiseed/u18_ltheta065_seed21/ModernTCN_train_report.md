# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
- loss_mode: `uncertainty_weighting`
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

- lambda_transition_focal: `0.0`
- lambda_stall_focal: `0.0`
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
  "lambda_theta": 0.65,
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
  "lambda_transition_focal": 0.0,
  "lambda_stall_focal": 0.0,
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
| acc_main | 0.9661 |
| acc_turn | 0.5561 |
| acc_turn_pure | 0.5715 |
| acc_turn_transition | 0.4888 |
| main_confidence_mean | 0.9874 |
| main_low_conf_0p60_ratio | 0.0089 |
| main_low_conf_0p70_ratio | 0.0178 |
| turn_confidence_mean | 0.8049 |
| turn_low_conf_0p60_ratio | 0.1877 |
| turn_low_conf_0p70_ratio | 0.3187 |
| turn_right_recall | 0.6708 |
| turn_straight_recall | 0.5297 |
| turn_left_recall | 0.5092 |
| theta_mae_deg | 0.7000 |
| theta_abs_le_10_p95_abs_err_deg | 1.9722 |
| theta_neg_10_8_p95_abs_err_deg | 3.0318 |
| theta_pos_8_10_p95_abs_err_deg | 2.4950 |
| theta_abs_le_8_p95_abs_err_deg | 1.8980 |
| theta_neg_8_6_p95_abs_err_deg | 1.5378 |
| theta_pos_6_8_p95_abs_err_deg | 1.4943 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.8546 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.9826 |
| theta_flat_abs_p95_deg | 2.7890 |
| theta_flat_bias_deg | -0.4555 |
| theta_near_flat_abs_p95_deg | 1.6925 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.2950 |
| theta_flat_turn_abs_p95_deg | 1.6177 |
| flat_recall | 0.9603 |
| stall_recall | 0.6979 |
| slope_recall | 0.9771 |
| flat_as_stall_ratio | 0.0013 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7523 |
| downhill_recall | 0.7968 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    726,
    1,
    29
  ],
  [
    10,
    67,
    19
  ],
  [
    55,
    8,
    2687
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    536,
    158,
    105
  ],
  [
    503,
    1024,
    406
  ],
  [
    205,
    222,
    443
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.308258 |
| test_loss_turn_bundle_base | 0.292443 |
| test_loss_theta_bundle_base | 0.000210 |
| test_loss_transition_focal_raw | 1.248365 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.430749 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 67
- train_seconds: 327.6

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 32 | 0.7188 | 0.5477 |
| [0.60,0.70) | 32 | 0.4375 | 0.6522 |
| [0.70,0.80) | 27 | 0.2963 | 0.7485 |
| [0.80,0.90) | 32 | 0.2500 | 0.8571 |
| [0.90,1.00) | 3479 | 0.0198 | 0.9976 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 676 | 0.6405 | 0.5261 |
| [0.60,0.70) | 472 | 0.5487 | 0.6478 |
| [0.70,0.80) | 433 | 0.5335 | 0.7513 |
| [0.80,0.90) | 472 | 0.4703 | 0.8505 |
| [0.90,1.00) | 1549 | 0.2931 | 0.9756 |


## 验证集最佳点

```json
{
  "loss_total": 0.6368324408834455,
  "acc_main": 0.9350473612990527,
  "acc_turn": 0.6227334235453316,
  "acc_turn_pure": 0.6361848574237955,
  "acc_turn_transition": 0.5590062111801242,
  "false_turn_straight": 0.45426195426195426,
  "flat_recall": 0.9041095890410958,
  "stall_recall": 0.47619047619047616,
  "slope_recall": 0.94826435246996,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9041095890410958,
    0.47619047619047616,
    0.94826435246996
  ],
  "turn_right_recall": 0.7274881516587678,
  "turn_straight_recall": 0.5457380457380457,
  "turn_left_recall": 0.6871628910463862,
  "recall_turn": [
    0.7274881516587678,
    0.5457380457380457,
    0.6871628910463862
  ],
  "cm_turn": [
    [
      614,
      190,
      40
    ],
    [
      527,
      1050,
      347
    ],
    [
      123,
      167,
      637
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      594,
      0,
      63
    ],
    [
      0,
      20,
      22
    ],
    [
      141,
      14,
      2841
    ]
  ],
  "main_confidence_mean": 0.969526252612064,
  "main_confidence_error_mean": 0.7998200238960347,
  "main_low_conf_0p60_ratio": 0.052232746955345064,
  "main_low_conf_0p70_ratio": 0.06062246278755074,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 193,
      "error_rate": 0.47150259067357514,
      "mean_confidence": 0.580506760451614
    },
    {
      "bin": "[0.60,0.70)",
      "n": 31,
      "error_rate": 0.22580645161290322,
      "mean_confidence": 0.6588150459036143
    },
    {
      "bin": "[0.70,0.80)",
      "n": 26,
      "error_rate": 0.46153846153846156,
      "mean_confidence": 0.7669140137941194
    },
    {
      "bin": "[0.80,0.90)",
      "n": 50,
      "error_rate": 0.36,
      "mean_confidence": 0.8494326851783637
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3395,
      "error_rate": 0.032989690721649485,
      "mean_confidence": 0.997798831691852
    }
  ],
  "turn_confidence_mean": 0.8201736965009765,
  "turn_confidence_error_mean": 0.7378561930143017,
  "turn_low_conf_0p60_ratio": 0.17564276048714478,
  "turn_low_conf_0p70_ratio": 0.26874154262516914,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 649,
      "error_rate": 0.6055469953775039,
      "mean_confidence": 0.4896842545317533
    },
    {
      "bin": "[0.60,0.70)",
      "n": 344,
      "error_rate": 0.5290697674418605,
      "mean_confidence": 0.6478821952862938
    },
    {
      "bin": "[0.70,0.80)",
      "n": 398,
      "error_rate": 0.5728643216080402,
      "mean_confidence": 0.7531359092599196
    },
    {
      "bin": "[0.80,0.90)",
      "n": 489,
      "error_rate": 0.3946830265848671,
      "mean_confidence": 0.8502800245513294
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1815,
      "error_rate": 0.21928374655647384,
      "mean_confidence": 0.9775924122922686
    }
  ],
  "theta_mae_rad": 0.013382996432483196,
  "theta_mae_deg": 0.7667891979217529,
  "uphill_recall": 0.7714285714285715,
  "downhill_recall": 0.8192436040044494,
  "slope_sign_acc": 0.9704352586914865,
  "theta_flat_mae_deg": 1.1257895231246948,
  "theta_flat_abs_p95_deg": 3.6585137844085693,
  "theta_flat_abs_max_deg": 6.803863525390625,
  "theta_flat_bias_deg": 0.3998279869556427,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4550936222076416,
  "theta_near_flat_abs_p95_deg": 3.8662075996398926,
  "theta_near_flat_abs_max_deg": 7.134827136993408,
  "theta_near_flat_bias_deg": 0.8934389352798462,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.130199909210205,
  "theta_flat_turn_abs_p95_deg": 3.865682601928711,
  "theta_flat_turn_abs_max_deg": 6.398118019104004,
  "theta_flat_turn_bias_deg": 0.4602639973163605,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7667891979217529,
  "theta_slope_control_abs_p95_deg": 9.543461799621582,
  "theta_slope_control_abs_max_deg": 11.950092315673828,
  "theta_slope_control_bias_deg": 0.27511391043663025,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7667891383171082,
  "theta_all_rmse_deg": 1.1663835048675537,
  "theta_all_p95_abs_err_deg": 2.375880002975464,
  "theta_all_max_abs_err_deg": 8.829646110534668,
  "theta_all_bias_deg": 0.27511391043663025,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6880631446838379,
  "theta_active_abs_ge_2_rmse_deg": 1.0402374267578125,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.08902645111084,
  "theta_active_abs_ge_2_max_abs_err_deg": 8.829646110534668,
  "theta_active_abs_ge_2_bias_deg": 0.24776506423950195,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8058624863624573,
  "theta_abs_le_8_rmse_deg": 1.1982518434524536,
  "theta_abs_le_8_p95_abs_err_deg": 2.516427755355835,
  "theta_abs_le_8_max_abs_err_deg": 8.829646110534668,
  "theta_abs_le_8_bias_deg": 0.2737853229045868,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7667891383171082,
  "theta_abs_le_10_rmse_deg": 1.1663835048675537,
  "theta_abs_le_10_p95_abs_err_deg": 2.375880002975464,
  "theta_abs_le_10_max_abs_err_deg": 8.829646110534668,
  "theta_abs_le_10_bias_deg": 0.27511391043663025,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5192179679870605,
  "theta_pos_8_10_rmse_deg": 0.7766104936599731,
  "theta_pos_8_10_p95_abs_err_deg": 1.793552279472351,
  "theta_pos_8_10_max_abs_err_deg": 4.387369155883789,
  "theta_pos_8_10_bias_deg": 0.26315784454345703,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6861235499382019,
  "theta_neg_10_8_rmse_deg": 1.2204818725585938,
  "theta_neg_10_8_p95_abs_err_deg": 1.9143378734588623,
  "theta_neg_10_8_max_abs_err_deg": 7.956966876983643,
  "theta_neg_10_8_bias_deg": 0.2985829710960388,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5592296123504639,
  "theta_pos_6_8_rmse_deg": 0.8666337132453918,
  "theta_pos_6_8_p95_abs_err_deg": 1.7375229597091675,
  "theta_pos_6_8_max_abs_err_deg": 4.578139781951904,
  "theta_pos_6_8_bias_deg": 0.362680584192276,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7497426271438599,
  "theta_neg_8_6_rmse_deg": 1.1260733604431152,
  "theta_neg_8_6_p95_abs_err_deg": 2.122004985809326,
  "theta_neg_8_6_max_abs_err_deg": 8.829646110534668,
  "theta_neg_8_6_bias_deg": 0.19779475033283234,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.766050398349762,
  "theta_neg_4_2_rmse_deg": 1.0466896295547485,
  "theta_neg_4_2_p95_abs_err_deg": 2.1196162700653076,
  "theta_neg_4_2_max_abs_err_deg": 6.372956275939941,
  "theta_neg_4_2_bias_deg": -0.21299563348293304,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6347047090530396,
  "theta_neg_2_0p5_rmse_deg": 0.9090051054954529,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.6882188320159912,
  "theta_neg_2_0p5_max_abs_err_deg": 5.464580535888672,
  "theta_neg_2_0p5_bias_deg": -0.4276253879070282,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.3219022750854492,
  "theta_pos_0p5_2_rmse_deg": 1.577588677406311,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.1585137844085693,
  "theta_pos_0p5_2_max_abs_err_deg": 5.031890869140625,
  "theta_pos_0p5_2_bias_deg": 0.7014368772506714,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.400423749470743,
  "loss_turn": 1.1804223250794315,
  "loss_theta": 0.00041446633305664,
  "loss_main_bundle_base": 0.400423749470743,
  "loss_turn_bundle_base": 0.23608446882203402,
  "loss_theta_bundle_base": 0.00032422651748799283,
  "loss_main_bundle": 0.400423749470743,
  "loss_turn_bundle": 0.23608446882203402,
  "loss_theta_bundle": 0.00032422651748799283,
  "loss_theta_flat": 0.00030760175793611915,
  "loss_theta_near_flat": 0.0011806832535724194,
  "loss_theta_error_excess": 0.0001475994049498045,
  "loss_theta_flat_excess": 0.0001394254694252019,
  "loss_theta_near_flat_excess": 0.0008254319987371967,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010531233902926102,
  "loss_theta_small_neg": 0.0003304741194431389,
  "loss_theta_small_neg_excess": 8.281215117817067e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3895880215787436,
  "loss_false_turn_straight": 0.3200531274281916,
  "loss_transition_focal_raw": 0.9449966312422643,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.471317592792847,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
