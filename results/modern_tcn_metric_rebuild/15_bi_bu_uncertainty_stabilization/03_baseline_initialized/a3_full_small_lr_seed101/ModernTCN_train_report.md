# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
- loss_mode: `bounded_uncertainty`
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
  "lambda_theta_error_excess": 0.0,
  "lambda_theta_flat_excess": 0.0,
  "lambda_theta_near_flat_excess": 0.0,
  "lambda_theta_true_zero_excess": 0.0,
  "lambda_theta_active_excess": 0.0,
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
    1.0,
    1.1,
    1.0
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 1.0,
  "select_turn_weight": 0.3,
  "select_turn_transition_weight": 1.0,
  "select_turn_transition_target": 0.75,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.8,
  "select_turn_lr_weight": 0.0,
  "select_turn_lr_target": 0.8,
  "select_stall_weight": 0.0,
  "select_stall_target": 0.7,
  "select_theta_weight": 0.15,
  "select_theta_ref_deg": 5.0,
  "select_theta_p95_weight": 0.0,
  "select_theta_p95_target_deg": 1.0,
  "select_theta_flat_p95_weight": 0.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_near_flat_p95_weight": 0.0,
  "select_theta_near_flat_p95_target_deg": 1.0,
  "select_theta_true_zero_p95_weight": 0.0,
  "select_theta_true_zero_p95_target_deg": 1.0,
  "select_theta_flat_peak_weight": 0.0,
  "select_theta_flat_peak_target_deg": 3.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.0,
  "select_theta_extreme_p95_target_deg": 1.0,
  "select_theta_edge_p95_weight": 0.0,
  "select_theta_edge_p95_target_deg": 1.2,
  "select_theta_small_nonzero_p95_weight": 0.0,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.0,
  "select_theta_flat_bias_target_deg": 0.2,
  "freeze_mode": "none",
  "freeze_early_blocks": 3,
  "preserve_mode": "baseline",
  "lambda_preserve_main": 0.1,
  "lambda_preserve_turn": 0.05,
  "lambda_preserve_theta": 0.1,
  "s_range": 0.5,
  "lambda_s_prior": 0.03
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9606 |
| acc_turn | 0.6124 |
| acc_turn_pure | 0.6308 |
| acc_turn_transition | 0.5320 |
| main_confidence_mean | 0.9857 |
| main_low_conf_0p60_ratio | 0.0105 |
| main_low_conf_0p70_ratio | 0.0205 |
| turn_confidence_mean | 0.8080 |
| turn_low_conf_0p60_ratio | 0.1852 |
| turn_low_conf_0p70_ratio | 0.3104 |
| turn_right_recall | 0.5569 |
| turn_straight_recall | 0.6348 |
| turn_left_recall | 0.6138 |
| theta_mae_deg | 0.7719 |
| theta_abs_le_10_p95_abs_err_deg | 2.2820 |
| theta_neg_10_8_p95_abs_err_deg | 2.4154 |
| theta_pos_8_10_p95_abs_err_deg | 3.1961 |
| theta_abs_le_8_p95_abs_err_deg | 2.2144 |
| theta_neg_8_6_p95_abs_err_deg | 2.2840 |
| theta_pos_6_8_p95_abs_err_deg | 1.9651 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.0941 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.8976 |
| theta_flat_abs_p95_deg | 2.5322 |
| theta_flat_bias_deg | 0.3614 |
| theta_near_flat_abs_p95_deg | 1.4380 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.2043 |
| theta_flat_turn_abs_p95_deg | 1.3533 |
| flat_recall | 0.9590 |
| stall_recall | 0.6875 |
| slope_recall | 0.9705 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7420 |
| downhill_recall | 0.7980 |

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
    10,
    66,
    20
  ],
  [
    75,
    6,
    2669
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    445,
    243,
    111
  ],
  [
    307,
    1227,
    399
  ],
  [
    118,
    218,
    534
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.364272 |
| test_loss_turn_bundle_base | 0.281409 |
| test_loss_theta_bundle_base | 0.000220 |
| test_loss_transition_focal_raw | 1.393349 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.567723 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 1
- train_seconds: 4.1

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 38 | 0.6053 | 0.5433 |
| [0.60,0.70) | 36 | 0.3611 | 0.6471 |
| [0.70,0.80) | 32 | 0.4062 | 0.7504 |
| [0.80,0.90) | 35 | 0.2286 | 0.8549 |
| [0.90,1.00) | 3461 | 0.0246 | 0.9975 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 667 | 0.5217 | 0.5137 |
| [0.60,0.70) | 451 | 0.4767 | 0.6487 |
| [0.70,0.80) | 401 | 0.4464 | 0.7505 |
| [0.80,0.90) | 465 | 0.4538 | 0.8498 |
| [0.90,1.00) | 1618 | 0.2738 | 0.9760 |


## 验证集最佳点

```json
{
  "loss_total": 0.5689683201348508,
  "acc_main": 0.9483085250338295,
  "acc_turn": 0.638700947225981,
  "acc_turn_pure": 0.6594559160930842,
  "acc_turn_transition": 0.5403726708074534,
  "false_turn_straight": 0.38565488565488565,
  "flat_recall": 0.9665144596651446,
  "stall_recall": 0.47619047619047616,
  "slope_recall": 0.9509345794392523,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9665144596651446,
    0.47619047619047616,
    0.9509345794392523
  ],
  "turn_right_recall": 0.6066350710900474,
  "turn_straight_recall": 0.6143451143451143,
  "turn_left_recall": 0.7184466019417476,
  "recall_turn": [
    0.6066350710900474,
    0.6143451143451143,
    0.7184466019417476
  ],
  "cm_turn": [
    [
      512,
      279,
      53
    ],
    [
      293,
      1182,
      449
    ],
    [
      49,
      212,
      666
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
      20,
      22
    ],
    [
      136,
      11,
      2849
    ]
  ],
  "main_confidence_mean": 0.9725991591210114,
  "main_confidence_error_mean": 0.7861020737461232,
  "main_low_conf_0p60_ratio": 0.003247631935047361,
  "main_low_conf_0p70_ratio": 0.05548037889039242,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 12,
      "error_rate": 0.4166666666666667,
      "mean_confidence": 0.5442471096324998
    },
    {
      "bin": "[0.60,0.70)",
      "n": 193,
      "error_rate": 0.47150259067357514,
      "mean_confidence": 0.6379950500605979
    },
    {
      "bin": "[0.70,0.80)",
      "n": 37,
      "error_rate": 0.32432432432432434,
      "mean_confidence": 0.7475587633629874
    },
    {
      "bin": "[0.80,0.90)",
      "n": 53,
      "error_rate": 0.20754716981132076,
      "mean_confidence": 0.8517445571036857
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3400,
      "error_rate": 0.021176470588235293,
      "mean_confidence": 0.9974375727070369
    }
  ],
  "turn_confidence_mean": 0.8268953812346704,
  "turn_confidence_error_mean": 0.7610479183484748,
  "turn_low_conf_0p60_ratio": 0.17645466847090663,
  "turn_low_conf_0p70_ratio": 0.25656292286874155,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 652,
      "error_rate": 0.5337423312883436,
      "mean_confidence": 0.4793637075557782
    },
    {
      "bin": "[0.60,0.70)",
      "n": 296,
      "error_rate": 0.4966216216216216,
      "mean_confidence": 0.6480340565663059
    },
    {
      "bin": "[0.70,0.80)",
      "n": 375,
      "error_rate": 0.496,
      "mean_confidence": 0.7515425623837748
    },
    {
      "bin": "[0.80,0.90)",
      "n": 424,
      "error_rate": 0.4363207547169811,
      "mean_confidence": 0.8545220409620682
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1948,
      "error_rate": 0.24075975359342916,
      "mean_confidence": 0.9788857337424439
    }
  ],
  "theta_mae_rad": 0.016116222366690636,
  "theta_mae_deg": 0.9233914613723755,
  "uphill_recall": 0.7730458221024259,
  "downhill_recall": 0.7992213570634038,
  "slope_sign_acc": 0.9698877634820695,
  "theta_flat_mae_deg": 1.1625845432281494,
  "theta_flat_abs_p95_deg": 3.974780559539795,
  "theta_flat_abs_max_deg": 8.407821655273438,
  "theta_flat_bias_deg": 0.6638070940971375,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.470509648323059,
  "theta_near_flat_abs_p95_deg": 4.049386978149414,
  "theta_near_flat_abs_max_deg": 8.407821655273438,
  "theta_near_flat_bias_deg": 0.9734917879104614,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.2223402261734009,
  "theta_flat_turn_abs_p95_deg": 4.152314186096191,
  "theta_flat_turn_abs_max_deg": 8.407821655273438,
  "theta_flat_turn_bias_deg": 0.4050140082836151,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9233914613723755,
  "theta_slope_control_abs_p95_deg": 9.446992874145508,
  "theta_slope_control_abs_max_deg": 12.421990394592285,
  "theta_slope_control_bias_deg": 0.5780478119850159,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.9233915209770203,
  "theta_all_rmse_deg": 1.4080246686935425,
  "theta_all_p95_abs_err_deg": 3.138044595718384,
  "theta_all_max_abs_err_deg": 7.9078216552734375,
  "theta_all_bias_deg": 0.5780477523803711,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.870938241481781,
  "theta_active_abs_ge_2_rmse_deg": 1.3310023546218872,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.6972899436950684,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.42730712890625,
  "theta_active_abs_ge_2_bias_deg": 0.5592414140701294,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9663073420524597,
  "theta_abs_le_8_rmse_deg": 1.451595425605774,
  "theta_abs_le_8_p95_abs_err_deg": 3.461763620376587,
  "theta_abs_le_8_max_abs_err_deg": 7.9078216552734375,
  "theta_abs_le_8_bias_deg": 0.5954533219337463,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.9233915209770203,
  "theta_abs_le_10_rmse_deg": 1.4080246686935425,
  "theta_abs_le_10_p95_abs_err_deg": 3.138044595718384,
  "theta_abs_le_10_max_abs_err_deg": 7.9078216552734375,
  "theta_abs_le_10_bias_deg": 0.5780477523803711,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5949769020080566,
  "theta_pos_8_10_rmse_deg": 0.8263126015663147,
  "theta_pos_8_10_p95_abs_err_deg": 1.4760912656784058,
  "theta_pos_8_10_max_abs_err_deg": 3.7866010665893555,
  "theta_pos_8_10_bias_deg": 0.2558976411819458,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8922671675682068,
  "theta_neg_10_8_rmse_deg": 1.4981411695480347,
  "theta_neg_10_8_p95_abs_err_deg": 2.7827131748199463,
  "theta_neg_10_8_max_abs_err_deg": 7.383050918579102,
  "theta_neg_10_8_bias_deg": 0.757645845413208,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6398691534996033,
  "theta_pos_6_8_rmse_deg": 0.9180149435997009,
  "theta_pos_6_8_p95_abs_err_deg": 1.8899089097976685,
  "theta_pos_6_8_max_abs_err_deg": 4.001501083374023,
  "theta_pos_6_8_bias_deg": 0.43555930256843567,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.9280290603637695,
  "theta_neg_8_6_rmse_deg": 1.320160984992981,
  "theta_neg_8_6_p95_abs_err_deg": 2.631755828857422,
  "theta_neg_8_6_max_abs_err_deg": 7.169078826904297,
  "theta_neg_8_6_bias_deg": 0.5491936802864075,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8603569269180298,
  "theta_neg_4_2_rmse_deg": 1.1594706773757935,
  "theta_neg_4_2_p95_abs_err_deg": 2.341209650039673,
  "theta_neg_4_2_max_abs_err_deg": 5.6805033683776855,
  "theta_neg_4_2_bias_deg": 0.38522598147392273,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5765042901039124,
  "theta_neg_2_0p5_rmse_deg": 0.9198669791221619,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.6204156875610352,
  "theta_neg_2_0p5_max_abs_err_deg": 5.942341327667236,
  "theta_neg_2_0p5_bias_deg": -0.1877196878194809,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.4746885299682617,
  "theta_pos_0p5_2_rmse_deg": 1.7294434309005737,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.474743127822876,
  "theta_pos_0p5_2_max_abs_err_deg": 5.083621978759766,
  "theta_pos_0p5_2_bias_deg": 1.3071609735488892,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2991203025164882,
  "loss_turn": 1.347445169934078,
  "loss_theta": 0.0006040463592990709,
  "loss_main_bundle_base": 0.2991203025164882,
  "loss_turn_bundle_base": 0.2694890387084068,
  "loss_theta_bundle_base": 0.000358980333263052,
  "loss_main_bundle": 0.2991203025164882,
  "loss_turn_bundle": 0.2694890387084068,
  "loss_theta_bundle": 0.000358980333263052,
  "loss_theta_flat": 0.00022295692742453114,
  "loss_theta_near_flat": 0.0014534198103097037,
  "loss_theta_error_excess": 0.0002529809961813163,
  "loss_theta_flat_excess": 0.00011614308519742902,
  "loss_theta_near_flat_excess": 0.0010572636994647924,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00021846797675255394,
  "loss_theta_small_neg": 0.0004026321235840008,
  "loss_theta_small_neg_excess": 0.00010839707619184187,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3841868340727118,
  "loss_false_turn_straight": 0.29929876385586834,
  "loss_transition_focal_raw": 1.2153971095530365,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.735578749213965,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0,
  "preserve_loss": 0.0052779316902160645
}
```
