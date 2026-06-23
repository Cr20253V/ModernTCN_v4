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
  "turn_transition_weight": 3.5,
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
| acc_main | 0.9597 |
| acc_turn | 0.5733 |
| acc_turn_pure | 0.5882 |
| acc_turn_transition | 0.5082 |
| main_confidence_mean | 0.9917 |
| main_low_conf_0p60_ratio | 0.0036 |
| main_low_conf_0p70_ratio | 0.0078 |
| turn_confidence_mean | 0.8299 |
| turn_low_conf_0p60_ratio | 0.1544 |
| turn_low_conf_0p70_ratio | 0.2562 |
| turn_right_recall | 0.6258 |
| turn_straight_recall | 0.5644 |
| turn_left_recall | 0.5448 |
| theta_mae_deg | 0.6892 |
| theta_abs_le_10_p95_abs_err_deg | 1.7672 |
| theta_neg_10_8_p95_abs_err_deg | 1.4345 |
| theta_pos_8_10_p95_abs_err_deg | 2.4698 |
| theta_abs_le_8_p95_abs_err_deg | 1.7530 |
| theta_neg_8_6_p95_abs_err_deg | 1.4187 |
| theta_pos_6_8_p95_abs_err_deg | 1.6390 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6081 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.7157 |
| theta_flat_abs_p95_deg | 2.7036 |
| theta_flat_bias_deg | -0.4118 |
| theta_near_flat_abs_p95_deg | 2.0606 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.5797 |
| theta_flat_turn_abs_p95_deg | 1.9613 |
| flat_recall | 0.9405 |
| stall_recall | 0.7083 |
| slope_recall | 0.9738 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7477 |
| downhill_recall | 0.8053 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    711,
    0,
    45
  ],
  [
    9,
    68,
    19
  ],
  [
    60,
    12,
    2678
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    500,
    182,
    117
  ],
  [
    400,
    1091,
    442
  ],
  [
    197,
    199,
    474
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.408387 |
| test_loss_turn_bundle_base | 0.353319 |
| test_loss_theta_bundle_base | 0.000177 |
| test_loss_transition_focal_raw | 1.602722 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.257182 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 76
- train_seconds: 362.3

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 13 | 0.6923 | 0.5479 |
| [0.60,0.70) | 15 | 0.5333 | 0.6505 |
| [0.70,0.80) | 17 | 0.4706 | 0.7549 |
| [0.80,0.90) | 46 | 0.4348 | 0.8492 |
| [0.90,1.00) | 3511 | 0.0285 | 0.9978 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 556 | 0.5701 | 0.5214 |
| [0.60,0.70) | 367 | 0.5504 | 0.6488 |
| [0.70,0.80) | 397 | 0.5592 | 0.7510 |
| [0.80,0.90) | 522 | 0.4693 | 0.8532 |
| [0.90,1.00) | 1760 | 0.3131 | 0.9761 |


## 验证集最佳点

```json
{
  "loss_total": 0.6279277586807901,
  "acc_main": 0.9450608930987822,
  "acc_turn": 0.6230040595399188,
  "acc_turn_pure": 0.6348738118649623,
  "acc_turn_transition": 0.5667701863354038,
  "false_turn_straight": 0.4371101871101871,
  "flat_recall": 0.9665144596651446,
  "stall_recall": 0.38095238095238093,
  "slope_recall": 0.94826435246996,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9665144596651446,
    0.38095238095238093,
    0.94826435246996
  ],
  "turn_right_recall": 0.6943127962085308,
  "turn_straight_recall": 0.5628898128898129,
  "turn_left_recall": 0.6828478964401294,
  "recall_turn": [
    0.6943127962085308,
    0.5628898128898129,
    0.6828478964401294
  ],
  "cm_turn": [
    [
      586,
      211,
      47
    ],
    [
      423,
      1083,
      418
    ],
    [
      122,
      172,
      633
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      635,
      0,
      22
    ],
    [
      0,
      16,
      26
    ],
    [
      142,
      13,
      2841
    ]
  ],
  "main_confidence_mean": 0.9713875365138329,
  "main_confidence_error_mean": 0.7796959956658385,
  "main_low_conf_0p60_ratio": 0.050608930987821384,
  "main_low_conf_0p70_ratio": 0.05764546684709066,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 187,
      "error_rate": 0.47593582887700536,
      "mean_confidence": 0.5815030179205446
    },
    {
      "bin": "[0.60,0.70)",
      "n": 26,
      "error_rate": 0.38461538461538464,
      "mean_confidence": 0.6509941269522395
    },
    {
      "bin": "[0.70,0.80)",
      "n": 29,
      "error_rate": 0.27586206896551724,
      "mean_confidence": 0.754849319278047
    },
    {
      "bin": "[0.80,0.90)",
      "n": 34,
      "error_rate": 0.20588235294117646,
      "mean_confidence": 0.8573336326959394
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3419,
      "error_rate": 0.026031003217315003,
      "mean_confidence": 0.9981193512711282
    }
  ],
  "turn_confidence_mean": 0.8440612917446362,
  "turn_confidence_error_mean": 0.773842203014703,
  "turn_low_conf_0p60_ratio": 0.13558863328822734,
  "turn_low_conf_0p70_ratio": 0.21732070365358594,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 501,
      "error_rate": 0.6407185628742516,
      "mean_confidence": 0.47270157284752007
    },
    {
      "bin": "[0.60,0.70)",
      "n": 302,
      "error_rate": 0.4966887417218543,
      "mean_confidence": 0.6514418175387542
    },
    {
      "bin": "[0.70,0.80)",
      "n": 380,
      "error_rate": 0.4921052631578947,
      "mean_confidence": 0.753931990799055
    },
    {
      "bin": "[0.80,0.90)",
      "n": 490,
      "error_rate": 0.42244897959183675,
      "mean_confidence": 0.8529311619633319
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2022,
      "error_rate": 0.26112759643916916,
      "mean_confidence": 0.9796326064477971
    }
  ],
  "theta_mae_rad": 0.015232284553349018,
  "theta_mae_deg": 0.8727455735206604,
  "uphill_recall": 0.77088948787062,
  "downhill_recall": 0.7969966629588432,
  "slope_sign_acc": 0.9761839583903641,
  "theta_flat_mae_deg": 1.116594910621643,
  "theta_flat_abs_p95_deg": 3.9447362422943115,
  "theta_flat_abs_max_deg": 6.879410743713379,
  "theta_flat_bias_deg": 0.18959584832191467,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4507935047149658,
  "theta_near_flat_abs_p95_deg": 4.23027229309082,
  "theta_near_flat_abs_max_deg": 6.879410743713379,
  "theta_near_flat_bias_deg": 0.693943202495575,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.059450387954712,
  "theta_flat_turn_abs_p95_deg": 4.0391340255737305,
  "theta_flat_turn_abs_max_deg": 6.879410743713379,
  "theta_flat_turn_bias_deg": 0.15062715113162994,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8727455735206604,
  "theta_slope_control_abs_p95_deg": 9.37575912475586,
  "theta_slope_control_abs_max_deg": 13.02464485168457,
  "theta_slope_control_bias_deg": -0.273288756608963,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8727455735206604,
  "theta_all_rmse_deg": 1.2230521440505981,
  "theta_all_p95_abs_err_deg": 2.6292481422424316,
  "theta_all_max_abs_err_deg": 6.379410266876221,
  "theta_all_bias_deg": -0.2732887864112854,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.8192713260650635,
  "theta_active_abs_ge_2_rmse_deg": 1.111623764038086,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2047691345214844,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.272665977478027,
  "theta_active_abs_ge_2_bias_deg": -0.3747958838939667,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.904964804649353,
  "theta_abs_le_8_rmse_deg": 1.2634508609771729,
  "theta_abs_le_8_p95_abs_err_deg": 2.7647995948791504,
  "theta_abs_le_8_max_abs_err_deg": 6.379410266876221,
  "theta_abs_le_8_bias_deg": -0.23624685406684875,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8727455735206604,
  "theta_abs_le_10_rmse_deg": 1.2230521440505981,
  "theta_abs_le_10_p95_abs_err_deg": 2.6292481422424316,
  "theta_abs_le_10_max_abs_err_deg": 6.379410266876221,
  "theta_abs_le_10_bias_deg": -0.2732887864112854,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.742331862449646,
  "theta_pos_8_10_rmse_deg": 0.9069096446037292,
  "theta_pos_8_10_p95_abs_err_deg": 1.6218900680541992,
  "theta_pos_8_10_max_abs_err_deg": 3.783553123474121,
  "theta_pos_8_10_bias_deg": -0.5576814413070679,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7312261462211609,
  "theta_neg_10_8_rmse_deg": 1.1515287160873413,
  "theta_neg_10_8_p95_abs_err_deg": 1.9800299406051636,
  "theta_neg_10_8_max_abs_err_deg": 6.272665977478027,
  "theta_neg_10_8_bias_deg": -0.29920879006385803,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6749886870384216,
  "theta_pos_6_8_rmse_deg": 0.8808851838111877,
  "theta_pos_6_8_p95_abs_err_deg": 1.8078422546386719,
  "theta_pos_6_8_max_abs_err_deg": 2.9671595096588135,
  "theta_pos_6_8_bias_deg": -0.4384633004665375,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.9150952696800232,
  "theta_neg_8_6_rmse_deg": 1.2365349531173706,
  "theta_neg_8_6_p95_abs_err_deg": 2.207301378250122,
  "theta_neg_8_6_max_abs_err_deg": 5.600768566131592,
  "theta_neg_8_6_bias_deg": -0.5644401907920837,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.81697016954422,
  "theta_neg_4_2_rmse_deg": 1.0497405529022217,
  "theta_neg_4_2_p95_abs_err_deg": 2.1556293964385986,
  "theta_neg_4_2_max_abs_err_deg": 3.9726929664611816,
  "theta_neg_4_2_bias_deg": -0.3251607418060303,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6891366243362427,
  "theta_neg_2_0p5_rmse_deg": 0.8632184267044067,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.6896923780441284,
  "theta_neg_2_0p5_max_abs_err_deg": 3.022432804107666,
  "theta_neg_2_0p5_bias_deg": -0.5253419280052185,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1956380605697632,
  "theta_pos_0p5_2_rmse_deg": 1.4908955097198486,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.4447264671325684,
  "theta_pos_0p5_2_max_abs_err_deg": 3.6221566200256348,
  "theta_pos_0p5_2_bias_deg": 0.3224717676639557,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.34151322833578707,
  "loss_turn": 1.430589292755953,
  "loss_theta": 0.0004555217352889841,
  "loss_main_bundle_base": 0.34151322833578707,
  "loss_turn_bundle_base": 0.28611786513109166,
  "loss_theta_bundle_base": 0.00029665932896722196,
  "loss_main_bundle": 0.34151322833578707,
  "loss_turn_bundle": 0.28611786513109166,
  "loss_theta_bundle": 0.00029665932896722196,
  "loss_theta_flat": 0.00023779103369661494,
  "loss_theta_near_flat": 0.001375043803589048,
  "loss_theta_error_excess": 0.00014798365018540977,
  "loss_theta_flat_excess": 0.00012453328692058104,
  "loss_theta_near_flat_excess": 0.0009891996808231622,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010188261497701507,
  "loss_theta_small_neg": 0.0003338711291831365,
  "loss_theta_small_neg_excess": 6.526445848876749e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.36936140436280884,
  "loss_false_turn_straight": 0.3288072972400908,
  "loss_transition_focal_raw": 1.1895584372286867,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.392217307645671,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
