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
  "lambda_theta_flat": 0.16,
  "theta_flat_loss_mode": "near_zero",
  "theta_flat_zero_tol_deg": 0.3,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 0.05,
  "lambda_theta_flat_excess": 0.06,
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
  "select_theta_flat_peak_weight": 1.4,
  "select_theta_flat_peak_target_deg": 4.8,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 0.6,
  "select_theta_edge_p95_target_deg": 1.25,
  "select_theta_small_nonzero_p95_weight": 0.8,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.3,
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9622 |
| acc_turn | 0.5825 |
| acc_turn_pure | 0.5937 |
| acc_turn_transition | 0.5335 |
| main_confidence_mean | 0.9853 |
| main_low_conf_0p60_ratio | 0.0114 |
| main_low_conf_0p70_ratio | 0.0183 |
| turn_confidence_mean | 0.8257 |
| turn_low_conf_0p60_ratio | 0.1524 |
| turn_low_conf_0p70_ratio | 0.2643 |
| turn_right_recall | 0.6283 |
| turn_straight_recall | 0.5908 |
| turn_left_recall | 0.5218 |
| theta_mae_deg | 0.9419 |
| theta_abs_le_10_p95_abs_err_deg | 2.4117 |
| theta_neg_10_8_p95_abs_err_deg | 2.0881 |
| theta_pos_8_10_p95_abs_err_deg | 3.1537 |
| theta_abs_le_8_p95_abs_err_deg | 2.3452 |
| theta_neg_8_6_p95_abs_err_deg | 2.6249 |
| theta_pos_6_8_p95_abs_err_deg | 1.8814 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.1982 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.6004 |
| theta_flat_abs_p95_deg | 2.8369 |
| theta_flat_bias_deg | -0.0056 |
| theta_near_flat_abs_p95_deg | 2.1161 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1673 |
| theta_flat_turn_abs_p95_deg | 3.5263 |
| flat_recall | 0.9537 |
| stall_recall | 0.6667 |
| slope_recall | 0.9749 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1146 |
| uphill_recall | 0.7517 |
| downhill_recall | 0.7974 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    721,
    0,
    35
  ],
  [
    11,
    64,
    21
  ],
  [
    53,
    16,
    2681
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    502,
    187,
    110
  ],
  [
    370,
    1142,
    421
  ],
  [
    150,
    266,
    454
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.337752 |
| test_loss_turn_bundle_base | 0.328338 |
| test_loss_theta_bundle_base | 0.000290 |
| test_loss_transition_focal_raw | 1.468491 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.385015 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 69
- train_seconds: 408.9

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 41 | 0.4390 | 0.5192 |
| [0.60,0.70) | 25 | 0.5200 | 0.6484 |
| [0.70,0.80) | 31 | 0.4194 | 0.7480 |
| [0.80,0.90) | 56 | 0.1786 | 0.8562 |
| [0.90,1.00) | 3449 | 0.0238 | 0.9975 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 549 | 0.5920 | 0.5242 |
| [0.60,0.70) | 403 | 0.5434 | 0.6487 |
| [0.70,0.80) | 448 | 0.5513 | 0.7483 |
| [0.80,0.90) | 490 | 0.4837 | 0.8524 |
| [0.90,1.00) | 1712 | 0.2780 | 0.9766 |


## 验证集最佳点

```json
{
  "loss_total": 0.6805788513610747,
  "acc_main": 0.9364005412719891,
  "acc_turn": 0.6465493910690122,
  "acc_turn_pure": 0.6571615863651262,
  "acc_turn_transition": 0.5962732919254659,
  "false_turn_straight": 0.39604989604989604,
  "flat_recall": 0.923896499238965,
  "stall_recall": 0.42857142857142855,
  "slope_recall": 0.9462616822429907,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.023809523809523808,
  "recall_main": [
    0.923896499238965,
    0.42857142857142855,
    0.9462616822429907
  ],
  "turn_right_recall": 0.6883886255924171,
  "turn_straight_recall": 0.603950103950104,
  "turn_left_recall": 0.6968716289104638,
  "recall_turn": [
    0.6883886255924171,
    0.603950103950104,
    0.6968716289104638
  ],
  "cm_turn": [
    [
      581,
      214,
      49
    ],
    [
      397,
      1162,
      365
    ],
    [
      90,
      191,
      646
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
      1,
      18,
      23
    ],
    [
      148,
      13,
      2835
    ]
  ],
  "main_confidence_mean": 0.9647562066055164,
  "main_confidence_error_mean": 0.7576645777426109,
  "main_low_conf_0p60_ratio": 0.05142083897158322,
  "main_low_conf_0p70_ratio": 0.05899864682002706,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 190,
      "error_rate": 0.4789473684210526,
      "mean_confidence": 0.5089418990330468
    },
    {
      "bin": "[0.60,0.70)",
      "n": 28,
      "error_rate": 0.42857142857142855,
      "mean_confidence": 0.6419738858948312
    },
    {
      "bin": "[0.70,0.80)",
      "n": 45,
      "error_rate": 0.4,
      "mean_confidence": 0.75179763960745
    },
    {
      "bin": "[0.80,0.90)",
      "n": 53,
      "error_rate": 0.2830188679245283,
      "mean_confidence": 0.853997265795489
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3379,
      "error_rate": 0.02929860905593371,
      "mean_confidence": 0.9976345678948071
    }
  ],
  "turn_confidence_mean": 0.846733938821535,
  "turn_confidence_error_mean": 0.7807893127920301,
  "turn_low_conf_0p60_ratio": 0.12043301759133965,
  "turn_low_conf_0p70_ratio": 0.24330175913396482,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 445,
      "error_rate": 0.5415730337078651,
      "mean_confidence": 0.5276206887613343
    },
    {
      "bin": "[0.60,0.70)",
      "n": 454,
      "error_rate": 0.552863436123348,
      "mean_confidence": 0.6319709239349501
    },
    {
      "bin": "[0.70,0.80)",
      "n": 320,
      "error_rate": 0.415625,
      "mean_confidence": 0.7533089053798028
    },
    {
      "bin": "[0.80,0.90)",
      "n": 480,
      "error_rate": 0.475,
      "mean_confidence": 0.854541064577334
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1996,
      "error_rate": 0.22695390781563127,
      "mean_confidence": 0.9798283252813895
    }
  ],
  "theta_mae_rad": 0.018790027126669884,
  "theta_mae_deg": 1.0765892267227173,
  "uphill_recall": 0.7703504043126684,
  "downhill_recall": 0.8097886540600667,
  "slope_sign_acc": 0.9690665206679442,
  "theta_flat_mae_deg": 1.211794137954712,
  "theta_flat_abs_p95_deg": 3.6676840782165527,
  "theta_flat_abs_max_deg": 7.368956565856934,
  "theta_flat_bias_deg": 0.46606332063674927,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.556433081626892,
  "theta_near_flat_abs_p95_deg": 3.7121188640594482,
  "theta_near_flat_abs_max_deg": 7.368956565856934,
  "theta_near_flat_bias_deg": 1.1064887046813965,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.366745948791504,
  "theta_flat_turn_abs_p95_deg": 4.973458290100098,
  "theta_flat_turn_abs_max_deg": 7.368956565856934,
  "theta_flat_turn_bias_deg": 1.0090523958206177,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 1.0765892267227173,
  "theta_slope_control_abs_p95_deg": 9.503257751464844,
  "theta_slope_control_abs_max_deg": 12.535506248474121,
  "theta_slope_control_bias_deg": -0.4764794111251831,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 1.0765892267227173,
  "theta_all_rmse_deg": 1.42031729221344,
  "theta_all_p95_abs_err_deg": 2.68135142326355,
  "theta_all_max_abs_err_deg": 7.868956565856934,
  "theta_all_bias_deg": -0.4764794409275055,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 1.0469398498535156,
  "theta_active_abs_ge_2_rmse_deg": 1.3395824432373047,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.421919822692871,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.986528396606445,
  "theta_active_abs_ge_2_bias_deg": -0.6831718683242798,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 1.1190377473831177,
  "theta_abs_le_8_rmse_deg": 1.4697507619857788,
  "theta_abs_le_8_p95_abs_err_deg": 2.8903632164001465,
  "theta_abs_le_8_max_abs_err_deg": 7.868956565856934,
  "theta_abs_le_8_bias_deg": -0.4349638521671295,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 1.0765892267227173,
  "theta_abs_le_10_rmse_deg": 1.42031729221344,
  "theta_abs_le_10_p95_abs_err_deg": 2.68135142326355,
  "theta_abs_le_10_max_abs_err_deg": 7.868956565856934,
  "theta_abs_le_10_bias_deg": -0.4764794409275055,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.9474634528160095,
  "theta_pos_8_10_rmse_deg": 1.1358767747879028,
  "theta_pos_8_10_p95_abs_err_deg": 1.9449169635772705,
  "theta_pos_8_10_max_abs_err_deg": 5.312478065490723,
  "theta_pos_8_10_bias_deg": -0.8286737203598022,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.846707284450531,
  "theta_neg_10_8_rmse_deg": 1.241433024406433,
  "theta_neg_10_8_p95_abs_err_deg": 2.3214476108551025,
  "theta_neg_10_8_max_abs_err_deg": 6.986528396606445,
  "theta_neg_10_8_bias_deg": -0.4714967906475067,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.9608989357948303,
  "theta_pos_6_8_rmse_deg": 1.1674482822418213,
  "theta_pos_6_8_p95_abs_err_deg": 2.1148102283477783,
  "theta_pos_6_8_max_abs_err_deg": 3.2874927520751953,
  "theta_pos_6_8_bias_deg": -0.7556155323982239,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.1162941455841064,
  "theta_neg_8_6_rmse_deg": 1.4212161302566528,
  "theta_neg_8_6_p95_abs_err_deg": 2.521237850189209,
  "theta_neg_8_6_max_abs_err_deg": 6.795576095581055,
  "theta_neg_8_6_bias_deg": -0.8692211508750916,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 1.2334189414978027,
  "theta_neg_4_2_rmse_deg": 1.5026929378509521,
  "theta_neg_4_2_p95_abs_err_deg": 2.4773757457733154,
  "theta_neg_4_2_max_abs_err_deg": 5.801115036010742,
  "theta_neg_4_2_bias_deg": -0.9579615592956543,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.843681812286377,
  "theta_neg_2_0p5_rmse_deg": 1.0698493719100952,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.7366968393325806,
  "theta_neg_2_0p5_max_abs_err_deg": 5.249819278717041,
  "theta_neg_2_0p5_bias_deg": -0.6599754691123962,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1344128847122192,
  "theta_pos_0p5_2_rmse_deg": 1.4120092391967773,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.1676833629608154,
  "theta_pos_0p5_2_max_abs_err_deg": 4.234947681427002,
  "theta_pos_0p5_2_bias_deg": 0.708376944065094,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.36443588486866313,
  "loss_turn": 1.578675094734832,
  "loss_theta": 0.0006146056531406738,
  "loss_main_bundle_base": 0.36443588486866313,
  "loss_turn_bundle_base": 0.3157350233104458,
  "loss_theta_bundle_base": 0.000407943248711602,
  "loss_main_bundle": 0.36443588486866313,
  "loss_turn_bundle": 0.3157350233104458,
  "loss_theta_bundle": 0.000407943248711602,
  "loss_theta_flat": 0.00023023096583333285,
  "loss_theta_near_flat": 0.001470932985954642,
  "loss_theta_error_excess": 0.000203298693283364,
  "loss_theta_flat_excess": 0.00012568860804392415,
  "loss_theta_near_flat_excess": 0.0010955039703845473,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00015366920475209703,
  "loss_theta_small_neg": 0.0006867633196613493,
  "loss_theta_small_neg_excess": 0.00020067112187789412,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.36923348151137286,
  "loss_false_turn_straight": 0.29847262955002274,
  "loss_transition_focal_raw": 1.3222167314792679,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.8555736857385114,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
