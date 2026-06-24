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
  "select_stall_weight": 0.2,
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
  "select_theta_flat_peak_weight": 1.0,
  "select_theta_flat_peak_target_deg": 5.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 1.2,
  "select_theta_edge_p95_target_deg": 1.15,
  "select_theta_small_nonzero_p95_weight": 0.8,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.3,
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9667 |
| acc_turn | 0.6177 |
| acc_turn_pure | 0.6343 |
| acc_turn_transition | 0.5455 |
| main_confidence_mean | 0.9889 |
| main_low_conf_0p60_ratio | 0.0086 |
| main_low_conf_0p70_ratio | 0.0155 |
| turn_confidence_mean | 0.8548 |
| turn_low_conf_0p60_ratio | 0.1249 |
| turn_low_conf_0p70_ratio | 0.2171 |
| turn_right_recall | 0.5895 |
| turn_straight_recall | 0.6477 |
| turn_left_recall | 0.5770 |
| theta_mae_deg | 0.5487 |
| theta_abs_le_10_p95_abs_err_deg | 1.4969 |
| theta_neg_10_8_p95_abs_err_deg | 1.1269 |
| theta_pos_8_10_p95_abs_err_deg | 2.6209 |
| theta_abs_le_8_p95_abs_err_deg | 1.4191 |
| theta_neg_8_6_p95_abs_err_deg | 1.4814 |
| theta_pos_6_8_p95_abs_err_deg | 1.4180 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.0795 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.1980 |
| theta_flat_abs_p95_deg | 2.1905 |
| theta_flat_bias_deg | -0.0195 |
| theta_near_flat_abs_p95_deg | 1.5233 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.0307 |
| theta_flat_turn_abs_p95_deg | 1.5014 |
| flat_recall | 0.9563 |
| stall_recall | 0.6667 |
| slope_recall | 0.9800 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7603 |
| downhill_recall | 0.7957 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    723,
    0,
    33
  ],
  [
    9,
    64,
    23
  ],
  [
    50,
    5,
    2695
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    471,
    199,
    129
  ],
  [
    270,
    1252,
    411
  ],
  [
    122,
    246,
    502
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.341432 |
| test_loss_turn_bundle_base | 0.371013 |
| test_loss_theta_bundle_base | 0.000123 |
| test_loss_transition_focal_raw | 1.716168 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.645226 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 90
- train_seconds: 482.9

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 31 | 0.3871 | 0.5325 |
| [0.60,0.70) | 25 | 0.6000 | 0.6527 |
| [0.70,0.80) | 21 | 0.3810 | 0.7448 |
| [0.80,0.90) | 39 | 0.3846 | 0.8522 |
| [0.90,1.00) | 3486 | 0.0201 | 0.9984 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 450 | 0.5756 | 0.5353 |
| [0.60,0.70) | 332 | 0.4669 | 0.6506 |
| [0.70,0.80) | 373 | 0.4477 | 0.7523 |
| [0.80,0.90) | 436 | 0.4037 | 0.8534 |
| [0.90,1.00) | 2011 | 0.3083 | 0.9793 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.5455

## 验证集最佳点

```json
{
  "loss_total": 0.6688412716166092,
  "acc_main": 0.9502029769959405,
  "acc_turn": 0.6587280108254397,
  "acc_turn_pure": 0.6683054736152081,
  "acc_turn_transition": 0.6133540372670807,
  "false_turn_straight": 0.36174636174636177,
  "flat_recall": 0.9649923896499238,
  "stall_recall": 0.38095238095238093,
  "slope_recall": 0.9549399198931909,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9649923896499238,
    0.38095238095238093,
    0.9549399198931909
  ],
  "turn_right_recall": 0.6255924170616114,
  "turn_straight_recall": 0.6382536382536382,
  "turn_left_recall": 0.7313915857605178,
  "recall_turn": [
    0.6255924170616114,
    0.6382536382536382,
    0.7313915857605178
  ],
  "cm_turn": [
    [
      528,
      229,
      87
    ],
    [
      258,
      1228,
      438
    ],
    [
      42,
      207,
      678
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      634,
      0,
      23
    ],
    [
      0,
      16,
      26
    ],
    [
      130,
      5,
      2861
    ]
  ],
  "main_confidence_mean": 0.9727770828350861,
  "main_confidence_error_mean": 0.7693602138735508,
  "main_low_conf_0p60_ratio": 0.04844384303112314,
  "main_low_conf_0p70_ratio": 0.05196211096075778,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 179,
      "error_rate": 0.45251396648044695,
      "mean_confidence": 0.5384851298597656
    },
    {
      "bin": "[0.60,0.70)",
      "n": 13,
      "error_rate": 0.38461538461538464,
      "mean_confidence": 0.6465767010864849
    },
    {
      "bin": "[0.70,0.80)",
      "n": 11,
      "error_rate": 0.2727272727272727,
      "mean_confidence": 0.7498697721795057
    },
    {
      "bin": "[0.80,0.90)",
      "n": 33,
      "error_rate": 0.2727272727272727,
      "mean_confidence": 0.8532063850827816
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3459,
      "error_rate": 0.02486267707429893,
      "mean_confidence": 0.9983268596458267
    }
  ],
  "turn_confidence_mean": 0.8608275278585433,
  "turn_confidence_error_mean": 0.7887894349380677,
  "turn_low_conf_0p60_ratio": 0.13261163734776726,
  "turn_low_conf_0p70_ratio": 0.2070365358592693,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 490,
      "error_rate": 0.6,
      "mean_confidence": 0.4989238523398849
    },
    {
      "bin": "[0.60,0.70)",
      "n": 275,
      "error_rate": 0.45454545454545453,
      "mean_confidence": 0.6487666192582663
    },
    {
      "bin": "[0.70,0.80)",
      "n": 308,
      "error_rate": 0.4902597402597403,
      "mean_confidence": 0.7527334082408954
    },
    {
      "bin": "[0.80,0.90)",
      "n": 401,
      "error_rate": 0.35910224438902744,
      "mean_confidence": 0.8537437617232282
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2221,
      "error_rate": 0.24628545700135074,
      "mean_confidence": 0.9831972396693113
    }
  ],
  "theta_mae_rad": 0.012628059834241867,
  "theta_mae_deg": 0.7235344648361206,
  "uphill_recall": 0.783288409703504,
  "downhill_recall": 0.7958843159065628,
  "slope_sign_acc": 0.9778264440186148,
  "theta_flat_mae_deg": 0.9815976023674011,
  "theta_flat_abs_p95_deg": 4.366877555847168,
  "theta_flat_abs_max_deg": 6.028069972991943,
  "theta_flat_bias_deg": 0.5863177180290222,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.324965000152588,
  "theta_near_flat_abs_p95_deg": 4.366877555847168,
  "theta_near_flat_abs_max_deg": 6.305301189422607,
  "theta_near_flat_bias_deg": 0.9477241039276123,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.8402942419052124,
  "theta_flat_turn_abs_p95_deg": 4.366877555847168,
  "theta_flat_turn_abs_max_deg": 5.5092315673828125,
  "theta_flat_turn_bias_deg": 0.44388848543167114,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7235344648361206,
  "theta_slope_control_abs_p95_deg": 9.213513374328613,
  "theta_slope_control_abs_max_deg": 11.97067642211914,
  "theta_slope_control_bias_deg": -0.04916457459330559,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7235345840454102,
  "theta_all_rmse_deg": 1.124069094657898,
  "theta_all_p95_abs_err_deg": 2.5569374561309814,
  "theta_all_max_abs_err_deg": 6.584372520446777,
  "theta_all_bias_deg": -0.049164578318595886,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6669433116912842,
  "theta_active_abs_ge_2_rmse_deg": 0.9823111295700073,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.8234714269638062,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.584372520446777,
  "theta_active_abs_ge_2_bias_deg": -0.18852099776268005,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7473680973052979,
  "theta_abs_le_8_rmse_deg": 1.153356909751892,
  "theta_abs_le_8_p95_abs_err_deg": 2.8001363277435303,
  "theta_abs_le_8_max_abs_err_deg": 6.4155168533325195,
  "theta_abs_le_8_bias_deg": 0.0032573987264186144,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7235345840454102,
  "theta_abs_le_10_rmse_deg": 1.124069094657898,
  "theta_abs_le_10_p95_abs_err_deg": 2.5569374561309814,
  "theta_abs_le_10_max_abs_err_deg": 6.584372520446777,
  "theta_abs_le_10_bias_deg": -0.049164578318595886,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7227993011474609,
  "theta_pos_8_10_rmse_deg": 0.8956253528594971,
  "theta_pos_8_10_p95_abs_err_deg": 1.4833191633224487,
  "theta_pos_8_10_max_abs_err_deg": 5.611458778381348,
  "theta_pos_8_10_bias_deg": -0.588523805141449,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.5214564204216003,
  "theta_neg_10_8_rmse_deg": 1.0794751644134521,
  "theta_neg_10_8_p95_abs_err_deg": 1.8073921203613281,
  "theta_neg_10_8_max_abs_err_deg": 6.584372520446777,
  "theta_neg_10_8_bias_deg": 0.053405195474624634,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6250215768814087,
  "theta_pos_6_8_rmse_deg": 0.7801888585090637,
  "theta_pos_6_8_p95_abs_err_deg": 1.366092562675476,
  "theta_pos_6_8_max_abs_err_deg": 2.7952098846435547,
  "theta_pos_6_8_bias_deg": -0.3870919644832611,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.6292458772659302,
  "theta_neg_8_6_rmse_deg": 1.0174427032470703,
  "theta_neg_8_6_p95_abs_err_deg": 1.8921855688095093,
  "theta_neg_8_6_max_abs_err_deg": 6.35235071182251,
  "theta_neg_8_6_bias_deg": -0.27357617020606995,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6978859305381775,
  "theta_neg_4_2_rmse_deg": 1.0246655941009521,
  "theta_neg_4_2_p95_abs_err_deg": 2.1650021076202393,
  "theta_neg_4_2_max_abs_err_deg": 6.02850341796875,
  "theta_neg_4_2_bias_deg": -0.24263150990009308,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5175570249557495,
  "theta_neg_2_0p5_rmse_deg": 0.7327646613121033,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.3199542760849,
  "theta_neg_2_0p5_max_abs_err_deg": 4.330657482147217,
  "theta_neg_2_0p5_bias_deg": -0.005416857078671455,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1214392185211182,
  "theta_pos_0p5_2_rmse_deg": 1.573596715927124,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.866877317428589,
  "theta_pos_0p5_2_max_abs_err_deg": 4.256097793579102,
  "theta_pos_0p5_2_bias_deg": 0.8628758192062378,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.33121866542689693,
  "loss_turn": 1.686853885876471,
  "loss_theta": 0.00038480691284732704,
  "loss_main_bundle_base": 0.33121866542689693,
  "loss_turn_bundle_base": 0.33737078579256113,
  "loss_theta_bundle_base": 0.000251808815780039,
  "loss_main_bundle": 0.33121866542689693,
  "loss_turn_bundle": 0.33737078579256113,
  "loss_theta_bundle": 0.000251808815780039,
  "loss_theta_flat": 0.00019841950817760958,
  "loss_theta_near_flat": 0.0012966713089248888,
  "loss_theta_error_excess": 0.00014535211947357788,
  "loss_theta_flat_excess": 0.0001348206675416098,
  "loss_theta_near_flat_excess": 0.0009608449328045521,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 9.087060677372511e-05,
  "loss_theta_small_neg": 0.0003158655026121032,
  "loss_theta_small_neg_excess": 9.446813855016181e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3322102309241185,
  "loss_false_turn_straight": 0.26472360500624764,
  "loss_transition_focal_raw": 1.4835807695763037,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.725421693263744,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
