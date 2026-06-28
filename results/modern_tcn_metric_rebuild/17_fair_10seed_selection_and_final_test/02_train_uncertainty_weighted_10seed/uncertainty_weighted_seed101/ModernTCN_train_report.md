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
| acc_main | 0.9622 |
| acc_turn | 0.5949 |
| acc_turn_pure | 0.6186 |
| acc_turn_transition | 0.4918 |
| main_confidence_mean | 0.9898 |
| main_low_conf_0p60_ratio | 0.0050 |
| main_low_conf_0p70_ratio | 0.0130 |
| turn_confidence_mean | 0.8123 |
| turn_low_conf_0p60_ratio | 0.1749 |
| turn_low_conf_0p70_ratio | 0.2976 |
| turn_right_recall | 0.5957 |
| turn_straight_recall | 0.6363 |
| turn_left_recall | 0.5023 |
| theta_mae_deg | 0.5443 |
| theta_abs_le_10_p95_abs_err_deg | 1.5899 |
| theta_neg_10_8_p95_abs_err_deg | 1.2955 |
| theta_pos_8_10_p95_abs_err_deg | 2.7441 |
| theta_abs_le_8_p95_abs_err_deg | 1.4599 |
| theta_neg_8_6_p95_abs_err_deg | 1.3694 |
| theta_pos_6_8_p95_abs_err_deg | 1.8794 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.2199 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.2949 |
| theta_flat_abs_p95_deg | 2.4712 |
| theta_flat_bias_deg | 0.1189 |
| theta_near_flat_abs_p95_deg | 1.7500 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.1955 |
| theta_flat_turn_abs_p95_deg | 1.2138 |
| flat_recall | 0.9299 |
| stall_recall | 0.7188 |
| slope_recall | 0.9796 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7586 |
| downhill_recall | 0.8082 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    703,
    0,
    53
  ],
  [
    10,
    69,
    17
  ],
  [
    45,
    11,
    2694
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    476,
    232,
    91
  ],
  [
    373,
    1230,
    330
  ],
  [
    178,
    255,
    437
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.355490 |
| test_loss_turn_bundle_base | 0.114918 |
| test_loss_theta_bundle_base | 0.000142 |
| test_loss_transition_focal_raw | 1.403920 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.382710 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 81
- train_seconds: 1752.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 18 | 0.5000 | 0.5519 |
| [0.60,0.70) | 29 | 0.2759 | 0.6619 |
| [0.70,0.80) | 29 | 0.4138 | 0.7522 |
| [0.80,0.90) | 26 | 0.3846 | 0.8561 |
| [0.90,1.00) | 3500 | 0.0277 | 0.9977 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 630 | 0.6175 | 0.5135 |
| [0.60,0.70) | 442 | 0.5204 | 0.6521 |
| [0.70,0.80) | 397 | 0.4962 | 0.7521 |
| [0.80,0.90) | 511 | 0.4207 | 0.8526 |
| [0.90,1.00) | 1622 | 0.2639 | 0.9742 |


## 验证集最佳点

```json
{
  "loss_total": 0.3919653533598728,
  "acc_main": 0.9461434370771312,
  "acc_turn": 0.6365358592692828,
  "acc_turn_pure": 0.647984267453294,
  "acc_turn_transition": 0.5822981366459627,
  "false_turn_straight": 0.3788981288981289,
  "flat_recall": 0.9573820395738204,
  "stall_recall": 0.5238095238095238,
  "slope_recall": 0.9495994659546061,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9573820395738204,
    0.5238095238095238,
    0.9495994659546061
  ],
  "turn_right_recall": 0.6765402843601895,
  "turn_straight_recall": 0.6211018711018711,
  "turn_left_recall": 0.6321467098166127,
  "recall_turn": [
    0.6765402843601895,
    0.6211018711018711,
    0.6321467098166127
  ],
  "cm_turn": [
    [
      571,
      244,
      29
    ],
    [
      410,
      1195,
      319
    ],
    [
      104,
      237,
      586
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      629,
      0,
      28
    ],
    [
      0,
      22,
      20
    ],
    [
      133,
      18,
      2845
    ]
  ],
  "main_confidence_mean": 0.9716480887173421,
  "main_confidence_error_mean": 0.7760140647309928,
  "main_low_conf_0p60_ratio": 0.0062246278755074425,
  "main_low_conf_0p70_ratio": 0.05737483085250338,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 23,
      "error_rate": 0.4782608695652174,
      "mean_confidence": 0.5563598670142366
    },
    {
      "bin": "[0.60,0.70)",
      "n": 189,
      "error_rate": 0.455026455026455,
      "mean_confidence": 0.6100727775526109
    },
    {
      "bin": "[0.70,0.80)",
      "n": 19,
      "error_rate": 0.47368421052631576,
      "mean_confidence": 0.7561263617969326
    },
    {
      "bin": "[0.80,0.90)",
      "n": 65,
      "error_rate": 0.3384615384615385,
      "mean_confidence": 0.861023130112088
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3399,
      "error_rate": 0.020888496616651958,
      "mean_confidence": 0.9978837162637192
    }
  ],
  "turn_confidence_mean": 0.8306788485162977,
  "turn_confidence_error_mean": 0.748917618422916,
  "turn_low_conf_0p60_ratio": 0.17158322056833558,
  "turn_low_conf_0p70_ratio": 0.26224627875507445,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 634,
      "error_rate": 0.6025236593059937,
      "mean_confidence": 0.5134984174732398
    },
    {
      "bin": "[0.60,0.70)",
      "n": 335,
      "error_rate": 0.5373134328358209,
      "mean_confidence": 0.651985054397605
    },
    {
      "bin": "[0.70,0.80)",
      "n": 371,
      "error_rate": 0.49595687331536387,
      "mean_confidence": 0.7486608669234294
    },
    {
      "bin": "[0.80,0.90)",
      "n": 445,
      "error_rate": 0.3955056179775281,
      "mean_confidence": 0.8521555220972976
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1910,
      "error_rate": 0.22041884816753926,
      "mean_confidence": 0.9782319195835594
    }
  ],
  "theta_mae_rad": 0.01245761290192604,
  "theta_mae_deg": 0.7137686014175415,
  "uphill_recall": 0.77088948787062,
  "downhill_recall": 0.8025583982202447,
  "slope_sign_acc": 0.9778264440186148,
  "theta_flat_mae_deg": 0.9880161285400391,
  "theta_flat_abs_p95_deg": 4.445345401763916,
  "theta_flat_abs_max_deg": 7.605860233306885,
  "theta_flat_bias_deg": 0.6452018022537231,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.319300651550293,
  "theta_near_flat_abs_p95_deg": 4.445441722869873,
  "theta_near_flat_abs_max_deg": 7.605860233306885,
  "theta_near_flat_bias_deg": 0.9120467305183411,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.0210273265838623,
  "theta_flat_turn_abs_p95_deg": 4.445345401763916,
  "theta_flat_turn_abs_max_deg": 7.605860233306885,
  "theta_flat_turn_bias_deg": 0.35214996337890625,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7137686014175415,
  "theta_slope_control_abs_p95_deg": 9.532602310180664,
  "theta_slope_control_abs_max_deg": 12.07835865020752,
  "theta_slope_control_bias_deg": 0.17184863984584808,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7137686610221863,
  "theta_all_rmse_deg": 1.1439653635025024,
  "theta_all_p95_abs_err_deg": 2.8320939540863037,
  "theta_all_max_abs_err_deg": 7.105859756469727,
  "theta_all_bias_deg": 0.17184865474700928,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6536282300949097,
  "theta_active_abs_ge_2_rmse_deg": 0.9995154738426208,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.166905403137207,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.024847030639648,
  "theta_active_abs_ge_2_bias_deg": 0.06804589927196503,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7421808838844299,
  "theta_abs_le_8_rmse_deg": 1.1750785112380981,
  "theta_abs_le_8_p95_abs_err_deg": 2.945345640182495,
  "theta_abs_le_8_max_abs_err_deg": 7.105859756469727,
  "theta_abs_le_8_bias_deg": 0.20302213728427887,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7137686610221863,
  "theta_abs_le_10_rmse_deg": 1.1439653635025024,
  "theta_abs_le_10_p95_abs_err_deg": 2.8320939540863037,
  "theta_abs_le_10_max_abs_err_deg": 7.105859756469727,
  "theta_abs_le_10_bias_deg": 0.17184865474700928,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5480259656906128,
  "theta_pos_8_10_rmse_deg": 0.8047940731048584,
  "theta_pos_8_10_p95_abs_err_deg": 1.843155026435852,
  "theta_pos_8_10_max_abs_err_deg": 4.254099369049072,
  "theta_pos_8_10_bias_deg": 0.06414095312356949,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6405861377716064,
  "theta_neg_10_8_rmse_deg": 1.1691974401474,
  "theta_neg_10_8_p95_abs_err_deg": 2.229076862335205,
  "theta_neg_10_8_max_abs_err_deg": 7.024847030639648,
  "theta_neg_10_8_bias_deg": 0.016129760071635246,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6072665452957153,
  "theta_pos_6_8_rmse_deg": 0.8460673689842224,
  "theta_pos_6_8_p95_abs_err_deg": 1.7850470542907715,
  "theta_pos_6_8_max_abs_err_deg": 3.282362461090088,
  "theta_pos_6_8_bias_deg": 0.1756763905286789,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.6597484946250916,
  "theta_neg_8_6_rmse_deg": 0.9889228343963623,
  "theta_neg_8_6_p95_abs_err_deg": 2.178264856338501,
  "theta_neg_8_6_max_abs_err_deg": 6.1698479652404785,
  "theta_neg_8_6_bias_deg": -0.1407974511384964,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6415950059890747,
  "theta_neg_4_2_rmse_deg": 0.9560304880142212,
  "theta_neg_4_2_p95_abs_err_deg": 2.0938010215759277,
  "theta_neg_4_2_max_abs_err_deg": 6.47865104675293,
  "theta_neg_4_2_bias_deg": 0.009650236926972866,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.4134889245033264,
  "theta_neg_2_0p5_rmse_deg": 0.6315371990203857,
  "theta_neg_2_0p5_p95_abs_err_deg": 0.890598714351654,
  "theta_neg_2_0p5_max_abs_err_deg": 4.628536224365234,
  "theta_neg_2_0p5_bias_deg": 0.06369467079639435,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1654531955718994,
  "theta_pos_0p5_2_rmse_deg": 1.6152708530426025,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.945345640182495,
  "theta_pos_0p5_2_max_abs_err_deg": 5.489968776702881,
  "theta_pos_0p5_2_bias_deg": 0.9834063053131104,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2813008577881711,
  "loss_turn": 1.3800234248738166,
  "loss_theta": 0.0003987187071494173,
  "loss_main_bundle_base": 0.2813008577881711,
  "loss_turn_bundle_base": 0.11040187113702862,
  "loss_theta_bundle_base": 0.00026262615254736115,
  "loss_main_bundle": 0.2813008577881711,
  "loss_turn_bundle": 0.11040187113702862,
  "loss_theta_bundle": 0.00026262615254736115,
  "loss_theta_flat": 0.00021718275358348913,
  "loss_theta_near_flat": 0.0014196965410544237,
  "loss_theta_error_excess": 0.00015427814171957015,
  "loss_theta_flat_excess": 0.00013973030393391202,
  "loss_theta_near_flat_excess": 0.001060536226411432,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 9.555021807846282e-05,
  "loss_theta_small_neg": 0.00027301247801609003,
  "loss_theta_small_neg_excess": 7.255619605607762e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3321254990258946,
  "loss_false_turn_straight": 0.25743081208333596,
  "loss_transition_focal_raw": 1.1466848854121723,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.4177578304734633,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
