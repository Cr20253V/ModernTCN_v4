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
  "lambda_theta_flat": 0.08,
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
| acc_main | 0.9714 |
| acc_turn | 0.5522 |
| acc_turn_pure | 0.5664 |
| acc_turn_transition | 0.4903 |
| main_confidence_mean | 0.9889 |
| main_low_conf_0p60_ratio | 0.0061 |
| main_low_conf_0p70_ratio | 0.0136 |
| turn_confidence_mean | 0.8169 |
| turn_low_conf_0p60_ratio | 0.1635 |
| turn_low_conf_0p70_ratio | 0.2735 |
| turn_right_recall | 0.6208 |
| turn_straight_recall | 0.5106 |
| turn_left_recall | 0.5816 |
| theta_mae_deg | 0.6836 |
| theta_abs_le_10_p95_abs_err_deg | 1.8335 |
| theta_neg_10_8_p95_abs_err_deg | 1.4286 |
| theta_pos_8_10_p95_abs_err_deg | 2.9514 |
| theta_abs_le_8_p95_abs_err_deg | 1.7235 |
| theta_neg_8_6_p95_abs_err_deg | 1.4695 |
| theta_pos_6_8_p95_abs_err_deg | 1.7913 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6970 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.6806 |
| theta_flat_abs_p95_deg | 2.3101 |
| theta_flat_bias_deg | 0.1854 |
| theta_near_flat_abs_p95_deg | 1.3999 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.2353 |
| theta_flat_turn_abs_p95_deg | 1.3048 |
| flat_recall | 0.9709 |
| stall_recall | 0.7188 |
| slope_recall | 0.9804 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7609 |
| downhill_recall | 0.7894 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    734,
    0,
    22
  ],
  [
    9,
    69,
    18
  ],
  [
    43,
    11,
    2696
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    496,
    166,
    137
  ],
  [
    444,
    987,
    502
  ],
  [
    222,
    142,
    506
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.303021 |
| test_loss_turn_bundle_base | 0.304793 |
| test_loss_theta_bundle_base | 0.000169 |
| test_loss_transition_focal_raw | 1.221463 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.381751 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 60
- train_seconds: 302.3

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 22 | 0.4545 | 0.5562 |
| [0.60,0.70) | 27 | 0.5185 | 0.6579 |
| [0.70,0.80) | 25 | 0.1600 | 0.7538 |
| [0.80,0.90) | 47 | 0.1915 | 0.8504 |
| [0.90,1.00) | 3481 | 0.0190 | 0.9978 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 589 | 0.6282 | 0.5268 |
| [0.60,0.70) | 396 | 0.5707 | 0.6492 |
| [0.70,0.80) | 440 | 0.6068 | 0.7521 |
| [0.80,0.90) | 590 | 0.5237 | 0.8531 |
| [0.90,1.00) | 1587 | 0.2779 | 0.9709 |


## 验证集最佳点

```json
{
  "loss_total": 0.6076243013425835,
  "acc_main": 0.9474966170500677,
  "acc_turn": 0.6043301759133964,
  "acc_turn_pure": 0.6175024582104228,
  "acc_turn_transition": 0.5419254658385093,
  "false_turn_straight": 0.47765072765072764,
  "flat_recall": 0.9680365296803652,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.9506008010680908,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9680365296803652,
    0.40476190476190477,
    0.9506008010680908
  ],
  "turn_right_recall": 0.6457345971563981,
  "turn_straight_recall": 0.5223492723492723,
  "turn_left_recall": 0.7367853290183387,
  "recall_turn": [
    0.6457345971563981,
    0.5223492723492723,
    0.7367853290183387
  ],
  "cm_turn": [
    [
      545,
      193,
      106
    ],
    [
      394,
      1005,
      525
    ],
    [
      78,
      166,
      683
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      636,
      0,
      21
    ],
    [
      0,
      17,
      25
    ],
    [
      134,
      14,
      2848
    ]
  ],
  "main_confidence_mean": 0.9826930135305799,
  "main_confidence_error_mean": 0.8814410525855976,
  "main_low_conf_0p60_ratio": 0.0035182679296346412,
  "main_low_conf_0p70_ratio": 0.009201623815967524,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 13,
      "error_rate": 0.46153846153846156,
      "mean_confidence": 0.5462235908041658
    },
    {
      "bin": "[0.60,0.70)",
      "n": 21,
      "error_rate": 0.42857142857142855,
      "mean_confidence": 0.665141947872374
    },
    {
      "bin": "[0.70,0.80)",
      "n": 29,
      "error_rate": 0.2413793103448276,
      "mean_confidence": 0.7493830155198548
    },
    {
      "bin": "[0.80,0.90)",
      "n": 208,
      "error_rate": 0.39903846153846156,
      "mean_confidence": 0.8311040717141819
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3424,
      "error_rate": 0.025992990654205607,
      "mean_confidence": 0.9974824892065107
    }
  ],
  "turn_confidence_mean": 0.8304417240451472,
  "turn_confidence_error_mean": 0.7545869889770325,
  "turn_low_conf_0p60_ratio": 0.159404600811908,
  "turn_low_conf_0p70_ratio": 0.2522327469553451,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 589,
      "error_rate": 0.6621392190152802,
      "mean_confidence": 0.5130109819401528
    },
    {
      "bin": "[0.60,0.70)",
      "n": 343,
      "error_rate": 0.5043731778425656,
      "mean_confidence": 0.6491038644701382
    },
    {
      "bin": "[0.70,0.80)",
      "n": 398,
      "error_rate": 0.5628140703517588,
      "mean_confidence": 0.7550608400859189
    },
    {
      "bin": "[0.80,0.90)",
      "n": 522,
      "error_rate": 0.446360153256705,
      "mean_confidence": 0.8490980775012463
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1843,
      "error_rate": 0.23982637004883342,
      "mean_confidence": 0.9766319401307458
    }
  ],
  "theta_mae_rad": 0.013671088963747025,
  "theta_mae_deg": 0.7832956314086914,
  "uphill_recall": 0.7768194070080863,
  "downhill_recall": 0.7942157953281423,
  "slope_sign_acc": 0.9624965781549412,
  "theta_flat_mae_deg": 0.8606334328651428,
  "theta_flat_abs_p95_deg": 2.744948148727417,
  "theta_flat_abs_max_deg": 6.330395698547363,
  "theta_flat_bias_deg": 0.4889236390590668,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.183795690536499,
  "theta_near_flat_abs_p95_deg": 3.028108835220337,
  "theta_near_flat_abs_max_deg": 6.685359954833984,
  "theta_near_flat_bias_deg": 0.6773720383644104,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.9247052073478699,
  "theta_flat_turn_abs_p95_deg": 2.741588830947876,
  "theta_flat_turn_abs_max_deg": 6.330395698547363,
  "theta_flat_turn_bias_deg": 0.11119615286588669,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7832956314086914,
  "theta_slope_control_abs_p95_deg": 9.443819046020508,
  "theta_slope_control_abs_max_deg": 12.000056266784668,
  "theta_slope_control_bias_deg": -0.03125772252678871,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7832956314086914,
  "theta_all_rmse_deg": 1.154008150100708,
  "theta_all_p95_abs_err_deg": 2.5155506134033203,
  "theta_all_max_abs_err_deg": 7.500397682189941,
  "theta_all_bias_deg": -0.03125771880149841,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7663360834121704,
  "theta_active_abs_ge_2_rmse_deg": 1.1373072862625122,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.54079270362854,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.500397682189941,
  "theta_active_abs_ge_2_bias_deg": -0.1453295350074768,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7980574369430542,
  "theta_abs_le_8_rmse_deg": 1.185409426689148,
  "theta_abs_le_8_p95_abs_err_deg": 2.692309856414795,
  "theta_abs_le_8_max_abs_err_deg": 7.500397682189941,
  "theta_abs_le_8_bias_deg": 0.04571103677153587,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7832956314086914,
  "theta_abs_le_10_rmse_deg": 1.154008150100708,
  "theta_abs_le_10_p95_abs_err_deg": 2.5155506134033203,
  "theta_abs_le_10_max_abs_err_deg": 7.500397682189941,
  "theta_abs_le_10_bias_deg": -0.03125771880149841,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7360037565231323,
  "theta_pos_8_10_rmse_deg": 0.9110541939735413,
  "theta_pos_8_10_p95_abs_err_deg": 1.7199630737304688,
  "theta_pos_8_10_max_abs_err_deg": 3.752875328063965,
  "theta_pos_8_10_bias_deg": -0.4768512547016144,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7057809233665466,
  "theta_neg_10_8_rmse_deg": 1.1031626462936401,
  "theta_neg_10_8_p95_abs_err_deg": 2.3608763217926025,
  "theta_neg_10_8_max_abs_err_deg": 6.216537952423096,
  "theta_neg_10_8_bias_deg": -0.23297017812728882,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5944635272026062,
  "theta_pos_6_8_rmse_deg": 0.8417997360229492,
  "theta_pos_6_8_p95_abs_err_deg": 1.724234700202942,
  "theta_pos_6_8_max_abs_err_deg": 3.524888038635254,
  "theta_pos_6_8_bias_deg": -0.15774208307266235,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8244742155075073,
  "theta_neg_8_6_rmse_deg": 1.2075276374816895,
  "theta_neg_8_6_p95_abs_err_deg": 2.715353488922119,
  "theta_neg_8_6_max_abs_err_deg": 5.468981742858887,
  "theta_neg_8_6_bias_deg": -0.2760779857635498,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7744688987731934,
  "theta_neg_4_2_rmse_deg": 1.0709561109542847,
  "theta_neg_4_2_p95_abs_err_deg": 2.2813496589660645,
  "theta_neg_4_2_max_abs_err_deg": 4.831003665924072,
  "theta_neg_4_2_bias_deg": -0.09352676570415497,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.61954665184021,
  "theta_neg_2_0p5_rmse_deg": 0.9229536652565002,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.805226445198059,
  "theta_neg_2_0p5_max_abs_err_deg": 4.9070587158203125,
  "theta_neg_2_0p5_bias_deg": 0.3318520486354828,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.7328068017959595,
  "theta_pos_0p5_2_rmse_deg": 0.9628466367721558,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.7597020864486694,
  "theta_pos_0p5_2_max_abs_err_deg": 4.122258186340332,
  "theta_pos_0p5_2_bias_deg": 0.5610868334770203,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.34378358245057244,
  "loss_turn": 1.3179375906274509,
  "loss_theta": 0.00040572500229701,
  "loss_main_bundle_base": 0.34378358245057244,
  "loss_turn_bundle_base": 0.26358752346651804,
  "loss_theta_bundle_base": 0.000253195837010908,
  "loss_main_bundle": 0.34378358245057244,
  "loss_turn_bundle": 0.26358752346651804,
  "loss_theta_bundle": 0.000253195837010908,
  "loss_theta_flat": 0.00011918098482132243,
  "loss_theta_near_flat": 0.0007426822093644347,
  "loss_theta_error_excess": 0.00013796429351288497,
  "loss_theta_flat_excess": 5.287936255454547e-05,
  "loss_theta_near_flat_excess": 0.0004597545517621126,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00013614389660241428,
  "loss_theta_small_neg": 0.000345885374950981,
  "loss_theta_small_neg_excess": 9.099924709258477e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4197347419832976,
  "loss_false_turn_straight": 0.34350089550179624,
  "loss_transition_focal_raw": 1.1636200053282133,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.0181300151831945,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
