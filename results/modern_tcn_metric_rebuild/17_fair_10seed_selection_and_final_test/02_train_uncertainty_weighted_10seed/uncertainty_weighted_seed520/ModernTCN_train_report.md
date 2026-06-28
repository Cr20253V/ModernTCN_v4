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
  "lambda_turn": 0.08,
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
    1.08,
    1.0,
    1.08
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 1.4,
  "select_turn_weight": 0.3,
  "select_turn_transition_weight": 1.2,
  "select_turn_transition_target": 0.82,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.88,
  "select_turn_lr_weight": 0.2,
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
  "select_theta_flat_bias_target_deg": 0.15,
  "freeze_mode": "none",
  "freeze_early_blocks": 3,
  "preserve_mode": "none",
  "lambda_preserve_main": 0.0,
  "lambda_preserve_turn": 0.0,
  "lambda_preserve_theta": 0.0,
  "s_range": 0.25,
  "lambda_s_prior": 0.01
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9645 |
| acc_turn | 0.5888 |
| acc_turn_pure | 0.6111 |
| acc_turn_transition | 0.4918 |
| main_confidence_mean | 0.9884 |
| main_low_conf_0p60_ratio | 0.0105 |
| main_low_conf_0p70_ratio | 0.0164 |
| turn_confidence_mean | 0.8302 |
| turn_low_conf_0p60_ratio | 0.1624 |
| turn_low_conf_0p70_ratio | 0.2662 |
| turn_right_recall | 0.6258 |
| turn_straight_recall | 0.5980 |
| turn_left_recall | 0.5345 |
| theta_mae_deg | 0.5782 |
| theta_abs_le_10_p95_abs_err_deg | 1.6103 |
| theta_neg_10_8_p95_abs_err_deg | 1.7667 |
| theta_pos_8_10_p95_abs_err_deg | 2.6491 |
| theta_abs_le_8_p95_abs_err_deg | 1.3947 |
| theta_neg_8_6_p95_abs_err_deg | 1.2662 |
| theta_pos_6_8_p95_abs_err_deg | 1.2480 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.3042 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.2733 |
| theta_flat_abs_p95_deg | 2.2916 |
| theta_flat_bias_deg | 0.0793 |
| theta_near_flat_abs_p95_deg | 1.2173 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.1751 |
| theta_flat_turn_abs_p95_deg | 1.1179 |
| flat_recall | 0.9683 |
| stall_recall | 0.6562 |
| slope_recall | 0.9742 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7494 |
| downhill_recall | 0.7923 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    732,
    0,
    24
  ],
  [
    9,
    63,
    24
  ],
  [
    55,
    16,
    2679
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    500,
    197,
    102
  ],
  [
    432,
    1156,
    345
  ],
  [
    185,
    220,
    465
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.353679 |
| test_loss_turn_bundle_base | 0.125061 |
| test_loss_theta_bundle_base | 0.000129 |
| test_loss_transition_focal_raw | 1.586294 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.909551 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 99
- train_seconds: 1960.4

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 38 | 0.4474 | 0.5478 |
| [0.60,0.70) | 21 | 0.3810 | 0.6507 |
| [0.70,0.80) | 22 | 0.5455 | 0.7653 |
| [0.80,0.90) | 30 | 0.2667 | 0.8546 |
| [0.90,1.00) | 3491 | 0.0238 | 0.9978 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 585 | 0.6274 | 0.5322 |
| [0.60,0.70) | 374 | 0.5481 | 0.6476 |
| [0.70,0.80) | 391 | 0.4399 | 0.7498 |
| [0.80,0.90) | 471 | 0.4544 | 0.8532 |
| [0.90,1.00) | 1781 | 0.2937 | 0.9781 |


## 验证集最佳点

```json
{
  "loss_total": 0.43864712453824095,
  "acc_main": 0.9426251691474966,
  "acc_turn": 0.6303112313937753,
  "acc_turn_pure": 0.6430678466076696,
  "acc_turn_transition": 0.5698757763975155,
  "false_turn_straight": 0.4282744282744283,
  "flat_recall": 0.954337899543379,
  "stall_recall": 0.30952380952380953,
  "slope_recall": 0.9489319092122831,
  "flat_as_stall_ratio": 0.0015220700152207,
  "stall_as_flat_ratio": 0.023809523809523808,
  "recall_main": [
    0.954337899543379,
    0.30952380952380953,
    0.9489319092122831
  ],
  "turn_right_recall": 0.6670616113744076,
  "turn_straight_recall": 0.5717255717255717,
  "turn_left_recall": 0.7184466019417476,
  "recall_turn": [
    0.6670616113744076,
    0.5717255717255717,
    0.7184466019417476
  ],
  "cm_turn": [
    [
      563,
      208,
      73
    ],
    [
      403,
      1100,
      421
    ],
    [
      99,
      162,
      666
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      627,
      1,
      29
    ],
    [
      1,
      13,
      28
    ],
    [
      138,
      15,
      2843
    ]
  ],
  "main_confidence_mean": 0.9710634761107806,
  "main_confidence_error_mean": 0.7840139958874925,
  "main_low_conf_0p60_ratio": 0.05115020297699594,
  "main_low_conf_0p70_ratio": 0.05764546684709066,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 189,
      "error_rate": 0.4603174603174603,
      "mean_confidence": 0.5815560957771106
    },
    {
      "bin": "[0.60,0.70)",
      "n": 24,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.655422195102172
    },
    {
      "bin": "[0.70,0.80)",
      "n": 22,
      "error_rate": 0.5,
      "mean_confidence": 0.751482652057235
    },
    {
      "bin": "[0.80,0.90)",
      "n": 56,
      "error_rate": 0.30357142857142855,
      "mean_confidence": 0.858955713509416
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3404,
      "error_rate": 0.026145710928319625,
      "mean_confidence": 0.9981789574451297
    }
  ],
  "turn_confidence_mean": 0.8453556734482589,
  "turn_confidence_error_mean": 0.7693911776852933,
  "turn_low_conf_0p60_ratio": 0.1499323410013532,
  "turn_low_conf_0p70_ratio": 0.23464140730717187,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 554,
      "error_rate": 0.644404332129964,
      "mean_confidence": 0.5088325668717048
    },
    {
      "bin": "[0.60,0.70)",
      "n": 313,
      "error_rate": 0.5239616613418531,
      "mean_confidence": 0.6524815746576238
    },
    {
      "bin": "[0.70,0.80)",
      "n": 364,
      "error_rate": 0.42032967032967034,
      "mean_confidence": 0.7518620136916462
    },
    {
      "bin": "[0.80,0.90)",
      "n": 413,
      "error_rate": 0.4745762711864407,
      "mean_confidence": 0.8528912444794141
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2051,
      "error_rate": 0.24183325207215992,
      "mean_confidence": 0.9807642035703554
    }
  ],
  "theta_mae_rad": 0.012325281277298927,
  "theta_mae_deg": 0.7061865329742432,
  "uphill_recall": 0.7714285714285715,
  "downhill_recall": 0.8014460511679644,
  "slope_sign_acc": 0.9687927730632357,
  "theta_flat_mae_deg": 0.9508370757102966,
  "theta_flat_abs_p95_deg": 3.861528158187866,
  "theta_flat_abs_max_deg": 6.232158660888672,
  "theta_flat_bias_deg": 0.6899175643920898,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.3854247331619263,
  "theta_near_flat_abs_p95_deg": 3.865595579147339,
  "theta_near_flat_abs_max_deg": 6.554778099060059,
  "theta_near_flat_bias_deg": 1.2063533067703247,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.0258712768554688,
  "theta_flat_turn_abs_p95_deg": 3.861424684524536,
  "theta_flat_turn_abs_max_deg": 5.487067699432373,
  "theta_flat_turn_bias_deg": 0.8368595242500305,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7061865329742432,
  "theta_slope_control_abs_p95_deg": 9.160016059875488,
  "theta_slope_control_abs_max_deg": 13.058046340942383,
  "theta_slope_control_bias_deg": -0.010169423185288906,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7061865329742432,
  "theta_all_rmse_deg": 1.0929434299468994,
  "theta_all_p95_abs_err_deg": 2.361424684524536,
  "theta_all_max_abs_err_deg": 6.808738708496094,
  "theta_all_bias_deg": -0.010169425047934055,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6525365710258484,
  "theta_active_abs_ge_2_rmse_deg": 0.9747712016105652,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.8632763624191284,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.808738708496094,
  "theta_active_abs_ge_2_bias_deg": -0.16369317471981049,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7402252554893494,
  "theta_abs_le_8_rmse_deg": 1.1301816701889038,
  "theta_abs_le_8_p95_abs_err_deg": 2.451901912689209,
  "theta_abs_le_8_max_abs_err_deg": 6.785152912139893,
  "theta_abs_le_8_bias_deg": 0.006518076173961163,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7061865329742432,
  "theta_abs_le_10_rmse_deg": 1.0929434299468994,
  "theta_abs_le_10_p95_abs_err_deg": 2.361424684524536,
  "theta_abs_le_10_max_abs_err_deg": 6.808738708496094,
  "theta_abs_le_10_bias_deg": -0.010169425047934055,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5564610362052917,
  "theta_pos_8_10_rmse_deg": 0.7700579166412354,
  "theta_pos_8_10_p95_abs_err_deg": 1.5162245035171509,
  "theta_pos_8_10_max_abs_err_deg": 4.447385787963867,
  "theta_pos_8_10_bias_deg": -0.288249671459198,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.5688282251358032,
  "theta_neg_10_8_rmse_deg": 1.0497385263442993,
  "theta_neg_10_8_p95_abs_err_deg": 1.668184518814087,
  "theta_neg_10_8_max_abs_err_deg": 6.808738708496094,
  "theta_neg_10_8_bias_deg": 0.1307070553302765,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6166101098060608,
  "theta_pos_6_8_rmse_deg": 0.8648995161056519,
  "theta_pos_6_8_p95_abs_err_deg": 1.7008970975875854,
  "theta_pos_6_8_max_abs_err_deg": 3.867147922515869,
  "theta_pos_6_8_bias_deg": -0.30016234517097473,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.5986518859863281,
  "theta_neg_8_6_rmse_deg": 0.9526720643043518,
  "theta_neg_8_6_p95_abs_err_deg": 1.5916376113891602,
  "theta_neg_8_6_max_abs_err_deg": 6.785152912139893,
  "theta_neg_8_6_bias_deg": -0.08115833252668381,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7602127194404602,
  "theta_neg_4_2_rmse_deg": 1.0240440368652344,
  "theta_neg_4_2_p95_abs_err_deg": 1.9282079935073853,
  "theta_neg_4_2_max_abs_err_deg": 4.555297374725342,
  "theta_neg_4_2_bias_deg": -0.4069969952106476,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.44305700063705444,
  "theta_neg_2_0p5_rmse_deg": 0.7146496176719666,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.0632528066635132,
  "theta_neg_2_0p5_max_abs_err_deg": 5.129671573638916,
  "theta_neg_2_0p5_bias_deg": 0.15244942903518677,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.92146235704422,
  "theta_pos_0p5_2_rmse_deg": 1.3150511980056763,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.361424684524536,
  "theta_pos_0p5_2_max_abs_err_deg": 4.46018648147583,
  "theta_pos_0p5_2_bias_deg": 0.5508927702903748,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.32212140192359645,
  "loss_turn": 1.4535841286908306,
  "loss_theta": 0.0003637880089104236,
  "loss_main_bundle_base": 0.32212140192359645,
  "loss_turn_bundle_base": 0.1162867280239988,
  "loss_theta_bundle_base": 0.0002389933849200959,
  "loss_main_bundle": 0.32212140192359645,
  "loss_turn_bundle": 0.1162867280239988,
  "loss_theta_bundle": 0.0002389933849200959,
  "loss_theta_flat": 0.00019330154013969962,
  "loss_theta_near_flat": 0.0011738029983479415,
  "loss_theta_error_excess": 0.00013229924309885328,
  "loss_theta_flat_excess": 0.00010984380752259691,
  "loss_theta_near_flat_excess": 0.0008218542472944571,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 9.098828315192327e-05,
  "loss_theta_small_neg": 0.000318169749167991,
  "loss_theta_small_neg_excess": 7.692119089518869e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3987428691293616,
  "loss_false_turn_straight": 0.30875287481831926,
  "loss_transition_focal_raw": 1.2875802283680648,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.08856896257207,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
