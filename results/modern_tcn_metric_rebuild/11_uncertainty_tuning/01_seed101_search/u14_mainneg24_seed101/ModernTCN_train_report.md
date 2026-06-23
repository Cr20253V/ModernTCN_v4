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
  "main_neg_slope_weight": 2.4,
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
| acc_turn | 0.5913 |
| acc_turn_pure | 0.6114 |
| acc_turn_transition | 0.5037 |
| main_confidence_mean | 0.9906 |
| main_low_conf_0p60_ratio | 0.0044 |
| main_low_conf_0p70_ratio | 0.0108 |
| turn_confidence_mean | 0.8425 |
| turn_low_conf_0p60_ratio | 0.1358 |
| turn_low_conf_0p70_ratio | 0.2238 |
| turn_right_recall | 0.5932 |
| turn_straight_recall | 0.5954 |
| turn_left_recall | 0.5805 |
| theta_mae_deg | 0.6291 |
| theta_abs_le_10_p95_abs_err_deg | 1.7597 |
| theta_neg_10_8_p95_abs_err_deg | 1.6752 |
| theta_pos_8_10_p95_abs_err_deg | 2.5811 |
| theta_abs_le_8_p95_abs_err_deg | 1.6241 |
| theta_neg_8_6_p95_abs_err_deg | 1.4930 |
| theta_pos_6_8_p95_abs_err_deg | 1.7626 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6257 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4535 |
| theta_flat_abs_p95_deg | 2.4365 |
| theta_flat_bias_deg | 0.1114 |
| theta_near_flat_abs_p95_deg | 1.7256 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.0491 |
| theta_flat_turn_abs_p95_deg | 1.3774 |
| flat_recall | 0.9590 |
| stall_recall | 0.6875 |
| slope_recall | 0.9778 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7569 |
| downhill_recall | 0.7946 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    725,
    0,
    31
  ],
  [
    9,
    66,
    21
  ],
  [
    52,
    9,
    2689
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    474,
    199,
    126
  ],
  [
    341,
    1151,
    441
  ],
  [
    170,
    195,
    505
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.318893 |
| test_loss_turn_bundle_base | 0.345713 |
| test_loss_theta_bundle_base | 0.000149 |
| test_loss_transition_focal_raw | 1.566151 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.827115 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 83
- train_seconds: 376.6

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 16 | 0.6875 | 0.5531 |
| [0.60,0.70) | 23 | 0.5652 | 0.6622 |
| [0.70,0.80) | 28 | 0.4643 | 0.7485 |
| [0.80,0.90) | 35 | 0.5143 | 0.8523 |
| [0.90,1.00) | 3500 | 0.0191 | 0.9980 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 489 | 0.6176 | 0.5215 |
| [0.60,0.70) | 317 | 0.5741 | 0.6533 |
| [0.70,0.80) | 426 | 0.4624 | 0.7498 |
| [0.80,0.90) | 490 | 0.4510 | 0.8523 |
| [0.90,1.00) | 1880 | 0.3032 | 0.9764 |


## 验证集最佳点

```json
{
  "loss_total": 0.6418276590487954,
  "acc_main": 0.9412719891745602,
  "acc_turn": 0.6411366711772666,
  "acc_turn_pure": 0.655850540806293,
  "acc_turn_transition": 0.5714285714285714,
  "false_turn_straight": 0.40488565488565487,
  "flat_recall": 0.923896499238965,
  "stall_recall": 0.42857142857142855,
  "slope_recall": 0.9522696929238985,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.923896499238965,
    0.42857142857142855,
    0.9522696929238985
  ],
  "turn_right_recall": 0.6729857819905213,
  "turn_straight_recall": 0.5951143451143451,
  "turn_left_recall": 0.7076591154261057,
  "recall_turn": [
    0.6729857819905213,
    0.5951143451143451,
    0.7076591154261057
  ],
  "cm_turn": [
    [
      568,
      225,
      51
    ],
    [
      359,
      1145,
      420
    ],
    [
      82,
      189,
      656
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      607,
      0,
      50
    ],
    [
      0,
      18,
      24
    ],
    [
      134,
      9,
      2853
    ]
  ],
  "main_confidence_mean": 0.9690472768103526,
  "main_confidence_error_mean": 0.7613144959293833,
  "main_low_conf_0p60_ratio": 0.0530446549391069,
  "main_low_conf_0p70_ratio": 0.0571041948579161,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 196,
      "error_rate": 0.4897959183673469,
      "mean_confidence": 0.5414046598756054
    },
    {
      "bin": "[0.60,0.70)",
      "n": 15,
      "error_rate": 0.4,
      "mean_confidence": 0.6464672241438413
    },
    {
      "bin": "[0.70,0.80)",
      "n": 30,
      "error_rate": 0.36666666666666664,
      "mean_confidence": 0.748051839195695
    },
    {
      "bin": "[0.80,0.90)",
      "n": 33,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.8415259190719976
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3421,
      "error_rate": 0.027185033615901782,
      "mean_confidence": 0.998130796729386
    }
  ],
  "turn_confidence_mean": 0.855774855402433,
  "turn_confidence_error_mean": 0.7807968410155335,
  "turn_low_conf_0p60_ratio": 0.13640054127198917,
  "turn_low_conf_0p70_ratio": 0.21326116373477672,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 504,
      "error_rate": 0.6369047619047619,
      "mean_confidence": 0.48693245316569167
    },
    {
      "bin": "[0.60,0.70)",
      "n": 284,
      "error_rate": 0.4894366197183099,
      "mean_confidence": 0.6538176852554843
    },
    {
      "bin": "[0.70,0.80)",
      "n": 301,
      "error_rate": 0.4883720930232558,
      "mean_confidence": 0.7523478286504449
    },
    {
      "bin": "[0.80,0.90)",
      "n": 379,
      "error_rate": 0.41424802110817943,
      "mean_confidence": 0.8540450881014406
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2227,
      "error_rate": 0.2523574315222272,
      "mean_confidence": 0.9792771113110433
    }
  ],
  "theta_mae_rad": 0.013128860853612423,
  "theta_mae_deg": 0.7522282600402832,
  "uphill_recall": 0.7773584905660378,
  "downhill_recall": 0.8125695216907676,
  "slope_sign_acc": 0.9720777443197371,
  "theta_flat_mae_deg": 0.9788052439689636,
  "theta_flat_abs_p95_deg": 3.9273123741149902,
  "theta_flat_abs_max_deg": 8.462309837341309,
  "theta_flat_bias_deg": 0.3315396010875702,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.417925477027893,
  "theta_near_flat_abs_p95_deg": 4.0548319816589355,
  "theta_near_flat_abs_max_deg": 8.462309837341309,
  "theta_near_flat_bias_deg": 0.7140007615089417,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.0849298238754272,
  "theta_flat_turn_abs_p95_deg": 4.037950038909912,
  "theta_flat_turn_abs_max_deg": 8.462309837341309,
  "theta_flat_turn_bias_deg": -0.009615814313292503,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7522282600402832,
  "theta_slope_control_abs_p95_deg": 9.304803848266602,
  "theta_slope_control_abs_max_deg": 11.971334457397461,
  "theta_slope_control_bias_deg": 0.38895684480667114,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7522282600402832,
  "theta_all_rmse_deg": 1.1747559309005737,
  "theta_all_p95_abs_err_deg": 2.6225075721740723,
  "theta_all_max_abs_err_deg": 7.962310314178467,
  "theta_all_bias_deg": 0.38895684480667114,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7025416493415833,
  "theta_active_abs_ge_2_rmse_deg": 1.0659403800964355,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.302050828933716,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.078514099121094,
  "theta_active_abs_ge_2_bias_deg": 0.40154799818992615,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7598841786384583,
  "theta_abs_le_8_rmse_deg": 1.1818327903747559,
  "theta_abs_le_8_p95_abs_err_deg": 2.779747247695923,
  "theta_abs_le_8_max_abs_err_deg": 7.962310314178467,
  "theta_abs_le_8_bias_deg": 0.3640059530735016,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7522282600402832,
  "theta_abs_le_10_rmse_deg": 1.1747559309005737,
  "theta_abs_le_10_p95_abs_err_deg": 2.6225075721740723,
  "theta_abs_le_10_max_abs_err_deg": 7.962310314178467,
  "theta_abs_le_10_bias_deg": 0.38895684480667114,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.43703484535217285,
  "theta_pos_8_10_rmse_deg": 0.6892275810241699,
  "theta_pos_8_10_p95_abs_err_deg": 1.6955912113189697,
  "theta_pos_8_10_max_abs_err_deg": 3.9405155181884766,
  "theta_pos_8_10_bias_deg": 0.11970937252044678,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 1.0077193975448608,
  "theta_neg_10_8_rmse_deg": 1.469283103942871,
  "theta_neg_10_8_p95_abs_err_deg": 2.477771043777466,
  "theta_neg_10_8_max_abs_err_deg": 7.078514099121094,
  "theta_neg_10_8_bias_deg": 0.8751943707466125,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5086931586265564,
  "theta_pos_6_8_rmse_deg": 0.8029593825340271,
  "theta_pos_6_8_p95_abs_err_deg": 1.6515471935272217,
  "theta_pos_6_8_max_abs_err_deg": 3.733994960784912,
  "theta_pos_6_8_bias_deg": 0.24628503620624542,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8474979400634766,
  "theta_neg_8_6_rmse_deg": 1.1728421449661255,
  "theta_neg_8_6_p95_abs_err_deg": 2.6166491508483887,
  "theta_neg_8_6_max_abs_err_deg": 6.164098739624023,
  "theta_neg_8_6_bias_deg": 0.6214850544929504,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7396019697189331,
  "theta_neg_4_2_rmse_deg": 1.0611586570739746,
  "theta_neg_4_2_p95_abs_err_deg": 2.401931047439575,
  "theta_neg_4_2_max_abs_err_deg": 5.002163410186768,
  "theta_neg_4_2_bias_deg": 0.40258440375328064,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.4707318842411041,
  "theta_neg_2_0p5_rmse_deg": 0.7175197601318359,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.4631189107894897,
  "theta_neg_2_0p5_max_abs_err_deg": 4.454963207244873,
  "theta_neg_2_0p5_bias_deg": -0.06723874807357788,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0071817636489868,
  "theta_pos_0p5_2_rmse_deg": 1.3946459293365479,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.4273126125335693,
  "theta_pos_0p5_2_max_abs_err_deg": 4.140753746032715,
  "theta_pos_0p5_2_bias_deg": 0.39713722467422485,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3366018190354875,
  "loss_turn": 1.524771709113063,
  "loss_theta": 0.00042042601481836204,
  "loss_main_bundle_base": 0.3366018190354875,
  "loss_turn_bundle_base": 0.30495434899452734,
  "loss_theta_bundle_base": 0.0002714853330656473,
  "loss_main_bundle": 0.3366018190354875,
  "loss_turn_bundle": 0.30495434899452734,
  "loss_theta_bundle": 0.0002714853330656473,
  "loss_theta_flat": 0.00017388957774021481,
  "loss_theta_near_flat": 0.001352738673610963,
  "loss_theta_error_excess": 0.00015844124465732153,
  "loss_theta_flat_excess": 0.00010388545745113991,
  "loss_theta_near_flat_excess": 0.0009962853518754487,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00011462209655385633,
  "loss_theta_small_neg": 0.0003397582814898291,
  "loss_theta_small_neg_excess": 8.775888249558158e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.39037492609959656,
  "loss_false_turn_straight": 0.3009354274069666,
  "loss_transition_focal_raw": 1.4278183530890087,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.708153680041533,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
