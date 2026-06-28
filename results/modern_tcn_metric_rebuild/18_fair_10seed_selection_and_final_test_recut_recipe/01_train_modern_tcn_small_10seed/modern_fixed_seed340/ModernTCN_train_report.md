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
| acc_main | 0.9689 |
| acc_turn | 0.6058 |
| acc_turn_pure | 0.6237 |
| acc_turn_transition | 0.5276 |
| main_confidence_mean | 0.9892 |
| main_low_conf_0p60_ratio | 0.0061 |
| main_low_conf_0p70_ratio | 0.0136 |
| turn_confidence_mean | 0.8506 |
| turn_low_conf_0p60_ratio | 0.1302 |
| turn_low_conf_0p70_ratio | 0.2179 |
| turn_right_recall | 0.5845 |
| turn_straight_recall | 0.6146 |
| turn_left_recall | 0.6057 |
| theta_mae_deg | 0.6348 |
| theta_abs_le_10_p95_abs_err_deg | 1.7648 |
| theta_neg_10_8_p95_abs_err_deg | 1.9175 |
| theta_pos_8_10_p95_abs_err_deg | 2.8348 |
| theta_abs_le_8_p95_abs_err_deg | 1.6660 |
| theta_neg_8_6_p95_abs_err_deg | 1.5864 |
| theta_pos_6_8_p95_abs_err_deg | 1.4149 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.1897 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4496 |
| theta_flat_abs_p95_deg | 2.7001 |
| theta_flat_bias_deg | 0.1327 |
| theta_near_flat_abs_p95_deg | 1.8880 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.1584 |
| theta_flat_turn_abs_p95_deg | 1.9194 |
| flat_recall | 0.9722 |
| stall_recall | 0.6458 |
| slope_recall | 0.9793 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0833 |
| uphill_recall | 0.7632 |
| downhill_recall | 0.7849 |

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
    8,
    62,
    26
  ],
  [
    50,
    7,
    2693
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    467,
    198,
    134
  ],
  [
    280,
    1188,
    465
  ],
  [
    139,
    204,
    527
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.391004 |
| test_loss_turn_bundle_base | 0.364157 |
| test_loss_theta_bundle_base | 0.000171 |
| test_loss_transition_focal_raw | 1.604625 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.726443 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 84
- train_seconds: 382.7

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 22 | 0.5909 | 0.5412 |
| [0.60,0.70) | 27 | 0.1852 | 0.6608 |
| [0.70,0.80) | 30 | 0.2667 | 0.7444 |
| [0.80,0.90) | 33 | 0.3636 | 0.8578 |
| [0.90,1.00) | 3490 | 0.0212 | 0.9979 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 469 | 0.5480 | 0.5137 |
| [0.60,0.70) | 316 | 0.5032 | 0.6495 |
| [0.70,0.80) | 348 | 0.5287 | 0.7481 |
| [0.80,0.90) | 480 | 0.4500 | 0.8558 |
| [0.90,1.00) | 1989 | 0.3037 | 0.9787 |


## 验证集最佳点

```json
{
  "loss_total": 0.6526253011939651,
  "acc_main": 0.9377537212449256,
  "acc_turn": 0.6598105548037889,
  "acc_turn_pure": 0.671583087512291,
  "acc_turn_transition": 0.6040372670807453,
  "false_turn_straight": 0.3685031185031185,
  "flat_recall": 0.9147640791476408,
  "stall_recall": 0.2857142857142857,
  "slope_recall": 0.951935914552737,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.07142857142857142,
  "recall_main": [
    0.9147640791476408,
    0.2857142857142857,
    0.951935914552737
  ],
  "turn_right_recall": 0.6658767772511849,
  "turn_straight_recall": 0.6314968814968815,
  "turn_left_recall": 0.7130528586839266,
  "recall_turn": [
    0.6658767772511849,
    0.6314968814968815,
    0.7130528586839266
  ],
  "cm_turn": [
    [
      562,
      241,
      41
    ],
    [
      322,
      1215,
      387
    ],
    [
      85,
      181,
      661
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      601,
      0,
      56
    ],
    [
      3,
      12,
      27
    ],
    [
      135,
      9,
      2852
    ]
  ],
  "main_confidence_mean": 0.9689363605080731,
  "main_confidence_error_mean": 0.7690207759783916,
  "main_low_conf_0p60_ratio": 0.0530446549391069,
  "main_low_conf_0p70_ratio": 0.05899864682002706,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 196,
      "error_rate": 0.4744897959183674,
      "mean_confidence": 0.5607174140839467
    },
    {
      "bin": "[0.60,0.70)",
      "n": 22,
      "error_rate": 0.5909090909090909,
      "mean_confidence": 0.6519323661374119
    },
    {
      "bin": "[0.70,0.80)",
      "n": 34,
      "error_rate": 0.5,
      "mean_confidence": 0.7479539645917956
    },
    {
      "bin": "[0.80,0.90)",
      "n": 39,
      "error_rate": 0.38461538461538464,
      "mean_confidence": 0.852371803101484
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3404,
      "error_rate": 0.02702702702702703,
      "mean_confidence": 0.9980328412881242
    }
  ],
  "turn_confidence_mean": 0.861872969560618,
  "turn_confidence_error_mean": 0.788651615056532,
  "turn_low_conf_0p60_ratio": 0.14262516914749662,
  "turn_low_conf_0p70_ratio": 0.20324763193504736,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 527,
      "error_rate": 0.5996204933586338,
      "mean_confidence": 0.48964462525648483
    },
    {
      "bin": "[0.60,0.70)",
      "n": 224,
      "error_rate": 0.46875,
      "mean_confidence": 0.6487771949475414
    },
    {
      "bin": "[0.70,0.80)",
      "n": 269,
      "error_rate": 0.43866171003717475,
      "mean_confidence": 0.7543855918012097
    },
    {
      "bin": "[0.80,0.90)",
      "n": 384,
      "error_rate": 0.3723958333333333,
      "mean_confidence": 0.8559489138496317
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2291,
      "error_rate": 0.2509821038847665,
      "mean_confidence": 0.9819457469381419
    }
  ],
  "theta_mae_rad": 0.013922806829214096,
  "theta_mae_deg": 0.7977180480957031,
  "uphill_recall": 0.7795148247978436,
  "downhill_recall": 0.8131256952169077,
  "slope_sign_acc": 0.9687927730632357,
  "theta_flat_mae_deg": 1.1317099332809448,
  "theta_flat_abs_p95_deg": 4.264669418334961,
  "theta_flat_abs_max_deg": 6.614357948303223,
  "theta_flat_bias_deg": 0.8038343787193298,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4271012544631958,
  "theta_near_flat_abs_p95_deg": 4.264955520629883,
  "theta_near_flat_abs_max_deg": 5.774164199829102,
  "theta_near_flat_bias_deg": 1.2086118459701538,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1468291282653809,
  "theta_flat_turn_abs_p95_deg": 4.264669418334961,
  "theta_flat_turn_abs_max_deg": 4.264669418334961,
  "theta_flat_turn_bias_deg": 0.9104259610176086,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7977180480957031,
  "theta_slope_control_abs_p95_deg": 9.360931396484375,
  "theta_slope_control_abs_max_deg": 12.612760543823242,
  "theta_slope_control_bias_deg": 0.012969288043677807,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7977180480957031,
  "theta_all_rmse_deg": 1.182540774345398,
  "theta_all_p95_abs_err_deg": 2.744612693786621,
  "theta_all_max_abs_err_deg": 7.241846084594727,
  "theta_all_bias_deg": 0.012969289906322956,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7244760394096375,
  "theta_active_abs_ge_2_rmse_deg": 1.0452982187271118,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.120635986328125,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.241846084594727,
  "theta_active_abs_ge_2_bias_deg": -0.16046138107776642,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8209563493728638,
  "theta_abs_le_8_rmse_deg": 1.2073434591293335,
  "theta_abs_le_8_p95_abs_err_deg": 2.76466965675354,
  "theta_abs_le_8_max_abs_err_deg": 6.1038289070129395,
  "theta_abs_le_8_bias_deg": 0.06841465085744858,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7977180480957031,
  "theta_abs_le_10_rmse_deg": 1.182540774345398,
  "theta_abs_le_10_p95_abs_err_deg": 2.744612693786621,
  "theta_abs_le_10_max_abs_err_deg": 7.241846084594727,
  "theta_abs_le_10_bias_deg": 0.012969289906322956,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6011500954627991,
  "theta_pos_8_10_rmse_deg": 0.8451370000839233,
  "theta_pos_8_10_p95_abs_err_deg": 1.6355518102645874,
  "theta_pos_8_10_max_abs_err_deg": 5.930673122406006,
  "theta_pos_8_10_bias_deg": -0.26554447412490845,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7999244928359985,
  "theta_neg_10_8_rmse_deg": 1.2609277963638306,
  "theta_neg_10_8_p95_abs_err_deg": 2.4406063556671143,
  "theta_neg_10_8_max_abs_err_deg": 7.241846084594727,
  "theta_neg_10_8_bias_deg": -0.1755460500717163,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5826656222343445,
  "theta_pos_6_8_rmse_deg": 0.808698296546936,
  "theta_pos_6_8_p95_abs_err_deg": 1.7100167274475098,
  "theta_pos_6_8_max_abs_err_deg": 3.315474033355713,
  "theta_pos_6_8_bias_deg": -0.2216694951057434,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8345410227775574,
  "theta_neg_8_6_rmse_deg": 1.1754587888717651,
  "theta_neg_8_6_p95_abs_err_deg": 2.209238052368164,
  "theta_neg_8_6_max_abs_err_deg": 5.224598407745361,
  "theta_neg_8_6_bias_deg": -0.2843908965587616,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7938026189804077,
  "theta_neg_4_2_rmse_deg": 1.1094696521759033,
  "theta_neg_4_2_p95_abs_err_deg": 2.2142395973205566,
  "theta_neg_4_2_max_abs_err_deg": 6.1038289070129395,
  "theta_neg_4_2_bias_deg": -0.4880971312522888,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5346684455871582,
  "theta_neg_2_0p5_rmse_deg": 0.7923276424407959,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.3513656854629517,
  "theta_neg_2_0p5_max_abs_err_deg": 4.974406719207764,
  "theta_neg_2_0p5_bias_deg": 0.3102835416793823,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.4409525394439697,
  "theta_pos_0p5_2_rmse_deg": 1.7743961811065674,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.76466965675354,
  "theta_pos_0p5_2_max_abs_err_deg": 4.842385292053223,
  "theta_pos_0p5_2_bias_deg": 0.8042669892311096,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.35163330798704023,
  "loss_turn": 1.5035487232092108,
  "loss_theta": 0.00042589362820985956,
  "loss_main_bundle_base": 0.35163330798704023,
  "loss_turn_bundle_base": 0.30070974977639114,
  "loss_theta_bundle_base": 0.0002822378497187638,
  "loss_main_bundle": 0.35163330798704023,
  "loss_turn_bundle": 0.30070974977639114,
  "loss_theta_bundle": 0.0002822378497187638,
  "loss_theta_flat": 0.00025412168507231084,
  "loss_theta_near_flat": 0.0013169232870581912,
  "loss_theta_error_excess": 0.00014945364068309538,
  "loss_theta_flat_excess": 0.00014564779516240502,
  "loss_theta_near_flat_excess": 0.0009440436940520488,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010029064287073628,
  "loss_theta_small_neg": 0.0003705405827715025,
  "loss_theta_small_neg_excess": 0.00011286825132720092,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.36083653497437823,
  "loss_false_turn_straight": 0.27780165783607264,
  "loss_transition_focal_raw": 1.344249273169186,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.878211697887664,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
