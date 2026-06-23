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
| acc_turn | 0.5330 |
| acc_turn_pure | 0.5462 |
| acc_turn_transition | 0.4754 |
| main_confidence_mean | 0.9862 |
| main_low_conf_0p60_ratio | 0.0056 |
| main_low_conf_0p70_ratio | 0.0142 |
| turn_confidence_mean | 0.7325 |
| turn_low_conf_0p60_ratio | 0.2904 |
| turn_low_conf_0p70_ratio | 0.4503 |
| turn_right_recall | 0.6896 |
| turn_straight_recall | 0.4909 |
| turn_left_recall | 0.4828 |
| theta_mae_deg | 0.5460 |
| theta_abs_le_10_p95_abs_err_deg | 1.6165 |
| theta_neg_10_8_p95_abs_err_deg | 1.0609 |
| theta_pos_8_10_p95_abs_err_deg | 2.0654 |
| theta_abs_le_8_p95_abs_err_deg | 1.6299 |
| theta_neg_8_6_p95_abs_err_deg | 1.1470 |
| theta_pos_6_8_p95_abs_err_deg | 1.7266 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.3141 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.3008 |
| theta_flat_abs_p95_deg | 2.2983 |
| theta_flat_bias_deg | -0.0850 |
| theta_near_flat_abs_p95_deg | 1.4481 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1093 |
| theta_flat_turn_abs_p95_deg | 1.3086 |
| flat_recall | 0.9722 |
| stall_recall | 0.6667 |
| slope_recall | 0.9796 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7569 |
| downhill_recall | 0.7917 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    735,
    0,
    21
  ],
  [
    9,
    64,
    23
  ],
  [
    48,
    8,
    2694
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    551,
    171,
    77
  ],
  [
    645,
    949,
    339
  ],
  [
    228,
    222,
    420
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.251948 |
| test_loss_turn_bundle_base | 0.231254 |
| test_loss_theta_bundle_base | 0.000116 |
| test_loss_transition_focal_raw | 0.891714 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 2.854977 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 68
- train_seconds: 327.6

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 20 | 0.4500 | 0.5518 |
| [0.60,0.70) | 31 | 0.5806 | 0.6417 |
| [0.70,0.80) | 34 | 0.2647 | 0.7534 |
| [0.80,0.90) | 53 | 0.1887 | 0.8545 |
| [0.90,1.00) | 3464 | 0.0182 | 0.9961 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1046 | 0.6300 | 0.5164 |
| [0.60,0.70) | 576 | 0.5747 | 0.6519 |
| [0.70,0.80) | 588 | 0.4524 | 0.7534 |
| [0.80,0.90) | 530 | 0.3868 | 0.8480 |
| [0.90,1.00) | 862 | 0.2564 | 0.9633 |


## 验证集最佳点

```json
{
  "loss_total": 0.5162224878800254,
  "acc_main": 0.9418132611637348,
  "acc_turn": 0.5897158322056834,
  "acc_turn_pure": 0.5971812520485087,
  "acc_turn_transition": 0.5543478260869565,
  "false_turn_straight": 0.4922037422037422,
  "flat_recall": 0.9208523592085236,
  "stall_recall": 0.47619047619047616,
  "slope_recall": 0.9529372496662216,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9208523592085236,
    0.47619047619047616,
    0.9529372496662216
  ],
  "turn_right_recall": 0.7322274881516587,
  "turn_straight_recall": 0.5077962577962578,
  "turn_left_recall": 0.6299892125134844,
  "recall_turn": [
    0.7322274881516587,
    0.5077962577962578,
    0.6299892125134844
  ],
  "cm_turn": [
    [
      618,
      197,
      29
    ],
    [
      612,
      977,
      335
    ],
    [
      178,
      165,
      584
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      605,
      0,
      52
    ],
    [
      0,
      20,
      22
    ],
    [
      132,
      9,
      2855
    ]
  ],
  "main_confidence_mean": 0.9646734675761626,
  "main_confidence_error_mean": 0.7608783326752868,
  "main_low_conf_0p60_ratio": 0.05142083897158322,
  "main_low_conf_0p70_ratio": 0.056833558863328824,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 190,
      "error_rate": 0.45263157894736844,
      "mean_confidence": 0.512794769242612
    },
    {
      "bin": "[0.60,0.70)",
      "n": 20,
      "error_rate": 0.55,
      "mean_confidence": 0.6404452251420472
    },
    {
      "bin": "[0.70,0.80)",
      "n": 51,
      "error_rate": 0.2549019607843137,
      "mean_confidence": 0.7428584813678408
    },
    {
      "bin": "[0.80,0.90)",
      "n": 52,
      "error_rate": 0.15384615384615385,
      "mean_confidence": 0.8599306965522844
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3382,
      "error_rate": 0.028681253696037846,
      "mean_confidence": 0.9969326946376419
    }
  ],
  "turn_confidence_mean": 0.7394150284879597,
  "turn_confidence_error_mean": 0.6761353334597822,
  "turn_low_conf_0p60_ratio": 0.28227334235453316,
  "turn_low_conf_0p70_ratio": 0.43951285520974287,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 1043,
      "error_rate": 0.5656759348034516,
      "mean_confidence": 0.500119016133959
    },
    {
      "bin": "[0.60,0.70)",
      "n": 581,
      "error_rate": 0.4457831325301205,
      "mean_confidence": 0.6489646401258178
    },
    {
      "bin": "[0.70,0.80)",
      "n": 511,
      "error_rate": 0.4520547945205479,
      "mean_confidence": 0.7520740518940908
    },
    {
      "bin": "[0.80,0.90)",
      "n": 502,
      "error_rate": 0.450199203187251,
      "mean_confidence": 0.850245551803577
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1058,
      "error_rate": 0.19848771266540643,
      "mean_confidence": 0.9662881219271411
    }
  ],
  "theta_mae_rad": 0.011922964826226234,
  "theta_mae_deg": 0.6831355094909668,
  "uphill_recall": 0.7800539083557951,
  "downhill_recall": 0.8120133481646273,
  "slope_sign_acc": 0.9537366548042705,
  "theta_flat_mae_deg": 1.2108932733535767,
  "theta_flat_abs_p95_deg": 4.381598949432373,
  "theta_flat_abs_max_deg": 6.267033100128174,
  "theta_flat_bias_deg": 0.2728675603866577,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5861817598342896,
  "theta_near_flat_abs_p95_deg": 4.38341760635376,
  "theta_near_flat_abs_max_deg": 6.267033100128174,
  "theta_near_flat_bias_deg": 0.9340590238571167,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.206107258796692,
  "theta_flat_turn_abs_p95_deg": 4.381580352783203,
  "theta_flat_turn_abs_max_deg": 6.267033100128174,
  "theta_flat_turn_bias_deg": 0.49423983693122864,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.6831355094909668,
  "theta_slope_control_abs_p95_deg": 9.44742202758789,
  "theta_slope_control_abs_max_deg": 10.948179244995117,
  "theta_slope_control_bias_deg": 0.10853274166584015,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.6831355690956116,
  "theta_all_rmse_deg": 1.0795780420303345,
  "theta_all_p95_abs_err_deg": 2.329982280731201,
  "theta_all_max_abs_err_deg": 6.767033576965332,
  "theta_all_bias_deg": 0.10853275656700134,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.5674022436141968,
  "theta_active_abs_ge_2_rmse_deg": 0.8425664305686951,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.7722172737121582,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.743040084838867,
  "theta_active_abs_ge_2_bias_deg": 0.07249537110328674,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7298469543457031,
  "theta_abs_le_8_rmse_deg": 1.1391901969909668,
  "theta_abs_le_8_p95_abs_err_deg": 2.6259915828704834,
  "theta_abs_le_8_max_abs_err_deg": 6.767033576965332,
  "theta_abs_le_8_bias_deg": 0.08329270780086517,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.6831355690956116,
  "theta_abs_le_10_rmse_deg": 1.0795780420303345,
  "theta_abs_le_10_p95_abs_err_deg": 2.329982280731201,
  "theta_abs_le_10_max_abs_err_deg": 6.767033576965332,
  "theta_abs_le_10_bias_deg": 0.10853275656700134,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.36770007014274597,
  "theta_pos_8_10_rmse_deg": 0.5669922828674316,
  "theta_pos_8_10_p95_abs_err_deg": 1.2942155599594116,
  "theta_pos_8_10_max_abs_err_deg": 3.523050308227539,
  "theta_pos_8_10_bias_deg": 0.1421554684638977,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6065069437026978,
  "theta_neg_10_8_rmse_deg": 0.9478932023048401,
  "theta_neg_10_8_p95_abs_err_deg": 1.3722703456878662,
  "theta_neg_10_8_max_abs_err_deg": 6.387816905975342,
  "theta_neg_10_8_bias_deg": 0.2891235947608948,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.4715084433555603,
  "theta_pos_6_8_rmse_deg": 0.7555992007255554,
  "theta_pos_6_8_p95_abs_err_deg": 1.297431468963623,
  "theta_pos_6_8_max_abs_err_deg": 3.998802423477173,
  "theta_pos_6_8_bias_deg": 0.22185881435871124,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.5815193057060242,
  "theta_neg_8_6_rmse_deg": 0.8475709557533264,
  "theta_neg_8_6_p95_abs_err_deg": 1.5205193758010864,
  "theta_neg_8_6_max_abs_err_deg": 5.821737766265869,
  "theta_neg_8_6_bias_deg": 0.10305459052324295,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.5702966451644897,
  "theta_neg_4_2_rmse_deg": 0.8355004191398621,
  "theta_neg_4_2_p95_abs_err_deg": 1.5815391540527344,
  "theta_neg_4_2_max_abs_err_deg": 6.743040084838867,
  "theta_neg_4_2_bias_deg": -0.2972451448440552,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.7523799538612366,
  "theta_neg_2_0p5_rmse_deg": 0.9097921848297119,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.536346673965454,
  "theta_neg_2_0p5_max_abs_err_deg": 3.7803049087524414,
  "theta_neg_2_0p5_bias_deg": -0.5918309092521667,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.244583010673523,
  "theta_pos_0p5_2_rmse_deg": 1.6619149446487427,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.881580352783203,
  "theta_pos_0p5_2_max_abs_err_deg": 4.472943305969238,
  "theta_pos_0p5_2_bias_deg": 0.2650940418243408,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3106829132859536,
  "loss_turn": 1.026525704092844,
  "loss_theta": 0.0003550404981670319,
  "loss_main_bundle_base": 0.3106829132859536,
  "loss_turn_bundle_base": 0.20530514217439297,
  "loss_theta_bundle_base": 0.00023443125697096662,
  "loss_main_bundle": 0.3106829132859536,
  "loss_turn_bundle": 0.20530514217439297,
  "loss_theta_bundle": 0.00023443125697096662,
  "loss_theta_flat": 0.00022837024544343178,
  "loss_theta_near_flat": 0.0015169771684646223,
  "loss_theta_error_excess": 0.00012965880143213563,
  "loss_theta_flat_excess": 0.00014044944239344814,
  "loss_theta_near_flat_excess": 0.0011330307782369293,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 5.271610573139098e-05,
  "loss_theta_small_neg": 0.0002079229781099158,
  "loss_theta_small_neg_excess": 4.7302775950840876e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.404892436093342,
  "loss_false_turn_straight": 0.3337034816670966,
  "loss_transition_focal_raw": 0.6240385167169635,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.2785475465861,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
