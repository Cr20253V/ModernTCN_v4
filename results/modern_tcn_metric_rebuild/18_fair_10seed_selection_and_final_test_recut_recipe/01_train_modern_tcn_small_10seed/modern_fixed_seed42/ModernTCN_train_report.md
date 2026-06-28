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
| acc_main | 0.9620 |
| acc_turn | 0.5558 |
| acc_turn_pure | 0.5691 |
| acc_turn_transition | 0.4978 |
| main_confidence_mean | 0.9826 |
| main_low_conf_0p60_ratio | 0.0089 |
| main_low_conf_0p70_ratio | 0.0219 |
| turn_confidence_mean | 0.7855 |
| turn_low_conf_0p60_ratio | 0.2165 |
| turn_low_conf_0p70_ratio | 0.3426 |
| turn_right_recall | 0.5569 |
| turn_straight_recall | 0.5660 |
| turn_left_recall | 0.5322 |
| theta_mae_deg | 0.6701 |
| theta_abs_le_10_p95_abs_err_deg | 1.8696 |
| theta_neg_10_8_p95_abs_err_deg | 1.8935 |
| theta_pos_8_10_p95_abs_err_deg | 2.5473 |
| theta_abs_le_8_p95_abs_err_deg | 1.7915 |
| theta_neg_8_6_p95_abs_err_deg | 1.9282 |
| theta_pos_6_8_p95_abs_err_deg | 1.4653 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.4016 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.1481 |
| theta_flat_abs_p95_deg | 2.4343 |
| theta_flat_bias_deg | 0.0672 |
| theta_near_flat_abs_p95_deg | 1.6481 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.0087 |
| theta_flat_turn_abs_p95_deg | 1.5937 |
| flat_recall | 0.9630 |
| stall_recall | 0.6771 |
| slope_recall | 0.9716 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7437 |
| downhill_recall | 0.7963 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    728,
    0,
    28
  ],
  [
    9,
    65,
    22
  ],
  [
    68,
    10,
    2672
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    445,
    244,
    110
  ],
  [
    406,
    1094,
    433
  ],
  [
    183,
    224,
    463
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.340114 |
| test_loss_turn_bundle_base | 0.296143 |
| test_loss_theta_bundle_base | 0.000174 |
| test_loss_transition_focal_raw | 1.133894 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.771589 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 53
- train_seconds: 273.5

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 32 | 0.5000 | 0.5466 |
| [0.60,0.70) | 47 | 0.3830 | 0.6567 |
| [0.70,0.80) | 46 | 0.5000 | 0.7415 |
| [0.80,0.90) | 60 | 0.1500 | 0.8573 |
| [0.90,1.00) | 3417 | 0.0208 | 0.9967 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 780 | 0.6256 | 0.5229 |
| [0.60,0.70) | 454 | 0.5661 | 0.6509 |
| [0.70,0.80) | 489 | 0.4908 | 0.7470 |
| [0.80,0.90) | 540 | 0.4593 | 0.8506 |
| [0.90,1.00) | 1339 | 0.2741 | 0.9719 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.4978

## 验证集最佳点

```json
{
  "loss_total": 0.4928462319509586,
  "acc_main": 0.9453315290933694,
  "acc_turn": 0.6368064952638701,
  "acc_turn_pure": 0.6473287446738775,
  "acc_turn_transition": 0.5869565217391305,
  "false_turn_straight": 0.41632016632016633,
  "flat_recall": 0.9710806697108066,
  "stall_recall": 0.5238095238095238,
  "slope_recall": 0.9455941255006676,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9710806697108066,
    0.5238095238095238,
    0.9455941255006676
  ],
  "turn_right_recall": 0.6445497630331753,
  "turn_straight_recall": 0.5836798336798337,
  "turn_left_recall": 0.7400215749730313,
  "recall_turn": [
    0.6445497630331753,
    0.5836798336798337,
    0.7400215749730313
  ],
  "cm_turn": [
    [
      544,
      213,
      87
    ],
    [
      346,
      1123,
      455
    ],
    [
      47,
      194,
      686
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      638,
      0,
      19
    ],
    [
      0,
      22,
      20
    ],
    [
      147,
      16,
      2833
    ]
  ],
  "main_confidence_mean": 0.9664479427350697,
  "main_confidence_error_mean": 0.7470700313191626,
  "main_low_conf_0p60_ratio": 0.053585926928281465,
  "main_low_conf_0p70_ratio": 0.06278755074424898,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 198,
      "error_rate": 0.4797979797979798,
      "mean_confidence": 0.5576812348420975
    },
    {
      "bin": "[0.60,0.70)",
      "n": 34,
      "error_rate": 0.29411764705882354,
      "mean_confidence": 0.652713865133628
    },
    {
      "bin": "[0.70,0.80)",
      "n": 33,
      "error_rate": 0.2727272727272727,
      "mean_confidence": 0.7575503161708211
    },
    {
      "bin": "[0.80,0.90)",
      "n": 45,
      "error_rate": 0.26666666666666666,
      "mean_confidence": 0.8491549387217104
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3385,
      "error_rate": 0.022451994091580503,
      "mean_confidence": 0.9971051284539706
    }
  ],
  "turn_confidence_mean": 0.8106076777434833,
  "turn_confidence_error_mean": 0.7364949808009432,
  "turn_low_conf_0p60_ratio": 0.19079837618403248,
  "turn_low_conf_0p70_ratio": 0.28525033829499324,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 705,
      "error_rate": 0.5645390070921986,
      "mean_confidence": 0.5000832331401414
    },
    {
      "bin": "[0.60,0.70)",
      "n": 349,
      "error_rate": 0.49283667621776506,
      "mean_confidence": 0.648585025111771
    },
    {
      "bin": "[0.70,0.80)",
      "n": 396,
      "error_rate": 0.4090909090909091,
      "mean_confidence": 0.7519161625291393
    },
    {
      "bin": "[0.80,0.90)",
      "n": 585,
      "error_rate": 0.37435897435897436,
      "mean_confidence": 0.8550862534151668
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1660,
      "error_rate": 0.2355421686746988,
      "mean_confidence": 0.974877263569248
    }
  ],
  "theta_mae_rad": 0.014212889596819878,
  "theta_mae_deg": 0.8143385648727417,
  "uphill_recall": 0.7628032345013477,
  "downhill_recall": 0.7992213570634038,
  "slope_sign_acc": 0.9641390637831919,
  "theta_flat_mae_deg": 1.0688940286636353,
  "theta_flat_abs_p95_deg": 3.797908067703247,
  "theta_flat_abs_max_deg": 7.465181350708008,
  "theta_flat_bias_deg": 0.7644081115722656,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4262642860412598,
  "theta_near_flat_abs_p95_deg": 3.797912359237671,
  "theta_near_flat_abs_max_deg": 7.465181350708008,
  "theta_near_flat_bias_deg": 1.0958048105239868,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1648858785629272,
  "theta_flat_turn_abs_p95_deg": 3.797908067703247,
  "theta_flat_turn_abs_max_deg": 7.465181350708008,
  "theta_flat_turn_bias_deg": 0.7375082969665527,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8143385648727417,
  "theta_slope_control_abs_p95_deg": 9.513328552246094,
  "theta_slope_control_abs_max_deg": 13.081070899963379,
  "theta_slope_control_bias_deg": -0.07712069898843765,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8143385052680969,
  "theta_all_rmse_deg": 1.2185574769973755,
  "theta_all_p95_abs_err_deg": 2.3510143756866455,
  "theta_all_max_abs_err_deg": 7.96518087387085,
  "theta_all_bias_deg": -0.07712069153785706,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7585164904594421,
  "theta_active_abs_ge_2_rmse_deg": 1.1201872825622559,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.0651655197143555,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.353701591491699,
  "theta_active_abs_ge_2_bias_deg": -0.261661559343338,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8279693126678467,
  "theta_abs_le_8_rmse_deg": 1.2362452745437622,
  "theta_abs_le_8_p95_abs_err_deg": 2.4597768783569336,
  "theta_abs_le_8_max_abs_err_deg": 7.96518087387085,
  "theta_abs_le_8_bias_deg": -0.016015535220503807,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8143385052680969,
  "theta_abs_le_10_rmse_deg": 1.2185574769973755,
  "theta_abs_le_10_p95_abs_err_deg": 2.3510143756866455,
  "theta_abs_le_10_max_abs_err_deg": 7.96518087387085,
  "theta_abs_le_10_bias_deg": -0.07712069153785706,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6769661903381348,
  "theta_pos_8_10_rmse_deg": 0.8849796056747437,
  "theta_pos_8_10_p95_abs_err_deg": 1.5448673963546753,
  "theta_pos_8_10_max_abs_err_deg": 5.5215229988098145,
  "theta_pos_8_10_bias_deg": -0.4288531541824341,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8380868434906006,
  "theta_neg_10_8_rmse_deg": 1.3524792194366455,
  "theta_neg_10_8_p95_abs_err_deg": 2.6667747497558594,
  "theta_neg_10_8_max_abs_err_deg": 7.353701591491699,
  "theta_neg_10_8_bias_deg": -0.23931658267974854,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.7254603505134583,
  "theta_pos_6_8_rmse_deg": 0.9308449625968933,
  "theta_pos_6_8_p95_abs_err_deg": 1.6802865266799927,
  "theta_pos_6_8_max_abs_err_deg": 4.141118049621582,
  "theta_pos_6_8_bias_deg": -0.38360196352005005,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8330286145210266,
  "theta_neg_8_6_rmse_deg": 1.2675637006759644,
  "theta_neg_8_6_p95_abs_err_deg": 2.516691207885742,
  "theta_neg_8_6_max_abs_err_deg": 6.63795280456543,
  "theta_neg_8_6_bias_deg": -0.4643721282482147,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7760252952575684,
  "theta_neg_4_2_rmse_deg": 1.1639530658721924,
  "theta_neg_4_2_p95_abs_err_deg": 2.3884034156799316,
  "theta_neg_4_2_max_abs_err_deg": 6.878750801086426,
  "theta_neg_4_2_bias_deg": -0.2198094129562378,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.548336386680603,
  "theta_neg_2_0p5_rmse_deg": 0.7986800670623779,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.4202601909637451,
  "theta_neg_2_0p5_max_abs_err_deg": 4.916294097900391,
  "theta_neg_2_0p5_bias_deg": 0.36325156688690186,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1880221366882324,
  "theta_pos_0p5_2_rmse_deg": 1.43998384475708,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.297908067703247,
  "theta_pos_0p5_2_max_abs_err_deg": 4.46944522857666,
  "theta_pos_0p5_2_bias_deg": 0.8233698606491089,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.24702300736642818,
  "loss_turn": 1.2276226668945023,
  "loss_theta": 0.00045219452469452145,
  "loss_main_bundle_base": 0.24702300736642818,
  "loss_turn_bundle_base": 0.24552454087424505,
  "loss_theta_bundle_base": 0.00029868284034472164,
  "loss_main_bundle": 0.24702300736642818,
  "loss_turn_bundle": 0.24552454087424505,
  "loss_theta_bundle": 0.00029868284034472164,
  "loss_theta_flat": 0.00023793084750138477,
  "loss_theta_near_flat": 0.0012863407619436132,
  "loss_theta_error_excess": 0.00016823544756777796,
  "loss_theta_flat_excess": 0.0001239051082371879,
  "loss_theta_near_flat_excess": 0.0009145808581033462,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00013012374669432524,
  "loss_theta_small_neg": 0.00041119007881118314,
  "loss_theta_small_neg_excess": 0.0001485852224620611,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.374572733339018,
  "loss_false_turn_straight": 0.2942650828858351,
  "loss_transition_focal_raw": 0.9955319557686781,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.681471720302981,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
