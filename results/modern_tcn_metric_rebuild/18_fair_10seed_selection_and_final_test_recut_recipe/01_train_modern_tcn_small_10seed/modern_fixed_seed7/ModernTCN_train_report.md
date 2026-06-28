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
| acc_main | 0.9697 |
| acc_turn | 0.5791 |
| acc_turn_pure | 0.5977 |
| acc_turn_transition | 0.4978 |
| main_confidence_mean | 0.9852 |
| main_low_conf_0p60_ratio | 0.0089 |
| main_low_conf_0p70_ratio | 0.0186 |
| turn_confidence_mean | 0.8043 |
| turn_low_conf_0p60_ratio | 0.1813 |
| turn_low_conf_0p70_ratio | 0.2996 |
| turn_right_recall | 0.6083 |
| turn_straight_recall | 0.5779 |
| turn_left_recall | 0.5552 |
| theta_mae_deg | 0.6813 |
| theta_abs_le_10_p95_abs_err_deg | 1.8927 |
| theta_neg_10_8_p95_abs_err_deg | 1.9966 |
| theta_pos_8_10_p95_abs_err_deg | 3.1048 |
| theta_abs_le_8_p95_abs_err_deg | 1.6771 |
| theta_neg_8_6_p95_abs_err_deg | 1.5495 |
| theta_pos_6_8_p95_abs_err_deg | 1.5094 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6008 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5795 |
| theta_flat_abs_p95_deg | 2.4727 |
| theta_flat_bias_deg | -0.0391 |
| theta_near_flat_abs_p95_deg | 1.7441 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.0123 |
| theta_flat_turn_abs_p95_deg | 1.5114 |
| flat_recall | 0.9788 |
| stall_recall | 0.6875 |
| slope_recall | 0.9771 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7557 |
| downhill_recall | 0.7860 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    740,
    0,
    16
  ],
  [
    9,
    66,
    21
  ],
  [
    44,
    19,
    2687
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    486,
    195,
    118
  ],
  [
    389,
    1117,
    427
  ],
  [
    169,
    218,
    483
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.319180 |
| test_loss_turn_bundle_base | 0.292888 |
| test_loss_theta_bundle_base | 0.000194 |
| test_loss_transition_focal_raw | 1.208009 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.803666 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 54
- train_seconds: 273.8

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 32 | 0.5000 | 0.5493 |
| [0.60,0.70) | 35 | 0.2286 | 0.6451 |
| [0.70,0.80) | 32 | 0.3750 | 0.7569 |
| [0.80,0.90) | 53 | 0.1509 | 0.8562 |
| [0.90,1.00) | 3450 | 0.0188 | 0.9968 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 653 | 0.5942 | 0.5186 |
| [0.60,0.70) | 426 | 0.5587 | 0.6488 |
| [0.70,0.80) | 499 | 0.5130 | 0.7506 |
| [0.80,0.90) | 518 | 0.4131 | 0.8506 |
| [0.90,1.00) | 1506 | 0.2789 | 0.9740 |


## 验证集最佳点

```json
{
  "loss_total": 0.5657154090833599,
  "acc_main": 0.9447902571041948,
  "acc_turn": 0.6392422192151556,
  "acc_turn_pure": 0.650278597181252,
  "acc_turn_transition": 0.5869565217391305,
  "false_turn_straight": 0.4022869022869023,
  "flat_recall": 0.9512937595129376,
  "stall_recall": 0.2857142857142857,
  "slope_recall": 0.9526034712950601,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.11904761904761904,
  "recall_main": [
    0.9512937595129376,
    0.2857142857142857,
    0.9526034712950601
  ],
  "turn_right_recall": 0.6208530805687204,
  "turn_straight_recall": 0.5977130977130977,
  "turn_left_recall": 0.7421790722761596,
  "recall_turn": [
    0.6208530805687204,
    0.5977130977130977,
    0.7421790722761596
  ],
  "cm_turn": [
    [
      524,
      221,
      99
    ],
    [
      324,
      1150,
      450
    ],
    [
      61,
      178,
      688
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      625,
      0,
      32
    ],
    [
      5,
      12,
      25
    ],
    [
      127,
      15,
      2854
    ]
  ],
  "main_confidence_mean": 0.9688137349743563,
  "main_confidence_error_mean": 0.7707358186339107,
  "main_low_conf_0p60_ratio": 0.05142083897158322,
  "main_low_conf_0p70_ratio": 0.05899864682002706,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 190,
      "error_rate": 0.45789473684210524,
      "mean_confidence": 0.5779334719433972
    },
    {
      "bin": "[0.60,0.70)",
      "n": 28,
      "error_rate": 0.35714285714285715,
      "mean_confidence": 0.6532974999632041
    },
    {
      "bin": "[0.70,0.80)",
      "n": 28,
      "error_rate": 0.25,
      "mean_confidence": 0.7559210593058177
    },
    {
      "bin": "[0.80,0.90)",
      "n": 60,
      "error_rate": 0.31666666666666665,
      "mean_confidence": 0.8611476276618266
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3389,
      "error_rate": 0.023900855709648863,
      "mean_confidence": 0.9969998270114365
    }
  ],
  "turn_confidence_mean": 0.8189878273066205,
  "turn_confidence_error_mean": 0.7490435702908789,
  "turn_low_conf_0p60_ratio": 0.18105548037889038,
  "turn_low_conf_0p70_ratio": 0.2838971583220568,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 669,
      "error_rate": 0.6038863976083707,
      "mean_confidence": 0.5169228329669845
    },
    {
      "bin": "[0.60,0.70)",
      "n": 380,
      "error_rate": 0.4368421052631579,
      "mean_confidence": 0.6483095542457423
    },
    {
      "bin": "[0.70,0.80)",
      "n": 422,
      "error_rate": 0.3981042654028436,
      "mean_confidence": 0.7527676001671765
    },
    {
      "bin": "[0.80,0.90)",
      "n": 444,
      "error_rate": 0.36486486486486486,
      "mean_confidence": 0.8515356135533472
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1780,
      "error_rate": 0.24325842696629213,
      "mean_confidence": 0.9765344249109174
    }
  ],
  "theta_mae_rad": 0.014093082398176193,
  "theta_mae_deg": 0.8074740767478943,
  "uphill_recall": 0.7795148247978436,
  "downhill_recall": 0.8008898776418243,
  "slope_sign_acc": 0.9756364631809472,
  "theta_flat_mae_deg": 0.9959209561347961,
  "theta_flat_abs_p95_deg": 3.7197012901306152,
  "theta_flat_abs_max_deg": 4.97751522064209,
  "theta_flat_bias_deg": 0.5923856496810913,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.1862940788269043,
  "theta_near_flat_abs_p95_deg": 3.7197012901306152,
  "theta_near_flat_abs_max_deg": 5.358504772186279,
  "theta_near_flat_bias_deg": 0.7783293128013611,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.8463162183761597,
  "theta_flat_turn_abs_p95_deg": 3.7197012901306152,
  "theta_flat_turn_abs_max_deg": 3.7197012901306152,
  "theta_flat_turn_bias_deg": 0.47045043110847473,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8074740767478943,
  "theta_slope_control_abs_p95_deg": 8.979283332824707,
  "theta_slope_control_abs_max_deg": 12.622162818908691,
  "theta_slope_control_bias_deg": 0.053077083081007004,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8074740171432495,
  "theta_all_rmse_deg": 1.1409721374511719,
  "theta_all_p95_abs_err_deg": 2.4597625732421875,
  "theta_all_max_abs_err_deg": 7.122163772583008,
  "theta_all_bias_deg": 0.0530770868062973,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7661491632461548,
  "theta_active_abs_ge_2_rmse_deg": 1.0691629648208618,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.1564223766326904,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.122163772583008,
  "theta_active_abs_ge_2_bias_deg": -0.0651891753077507,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8129900097846985,
  "theta_abs_le_8_rmse_deg": 1.1539783477783203,
  "theta_abs_le_8_p95_abs_err_deg": 2.628538131713867,
  "theta_abs_le_8_max_abs_err_deg": 7.122163772583008,
  "theta_abs_le_8_bias_deg": 0.08860624581575394,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8074740171432495,
  "theta_abs_le_10_rmse_deg": 1.1409721374511719,
  "theta_abs_le_10_p95_abs_err_deg": 2.4597625732421875,
  "theta_abs_le_10_max_abs_err_deg": 7.122163772583008,
  "theta_abs_le_10_bias_deg": 0.0530770868062973,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7518945932388306,
  "theta_pos_8_10_rmse_deg": 0.9573009014129639,
  "theta_pos_8_10_p95_abs_err_deg": 1.7377362251281738,
  "theta_pos_8_10_max_abs_err_deg": 5.089497089385986,
  "theta_pos_8_10_bias_deg": -0.560592770576477,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8170735836029053,
  "theta_neg_10_8_rmse_deg": 1.1999411582946777,
  "theta_neg_10_8_p95_abs_err_deg": 2.4337613582611084,
  "theta_neg_10_8_max_abs_err_deg": 6.425479888916016,
  "theta_neg_10_8_bias_deg": 0.3750017285346985,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.8078924417495728,
  "theta_pos_6_8_rmse_deg": 1.0595391988754272,
  "theta_pos_6_8_p95_abs_err_deg": 2.21893310546875,
  "theta_pos_6_8_max_abs_err_deg": 3.6698825359344482,
  "theta_pos_6_8_bias_deg": -0.48995324969291687,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8257710337638855,
  "theta_neg_8_6_rmse_deg": 1.160223126411438,
  "theta_neg_8_6_p95_abs_err_deg": 2.5874342918395996,
  "theta_neg_8_6_max_abs_err_deg": 6.040690898895264,
  "theta_neg_8_6_bias_deg": 0.25121191143989563,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6872733235359192,
  "theta_neg_4_2_rmse_deg": 0.9765961766242981,
  "theta_neg_4_2_p95_abs_err_deg": 1.9392116069793701,
  "theta_neg_4_2_max_abs_err_deg": 4.431097030639648,
  "theta_neg_4_2_bias_deg": -0.006279380992054939,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6010456681251526,
  "theta_neg_2_0p5_rmse_deg": 0.827631413936615,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.6523319482803345,
  "theta_neg_2_0p5_max_abs_err_deg": 3.460063934326172,
  "theta_neg_2_0p5_bias_deg": 0.12607663869857788,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.271036982536316,
  "theta_pos_0p5_2_rmse_deg": 1.549516201019287,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.285539150238037,
  "theta_pos_0p5_2_max_abs_err_deg": 3.20554256439209,
  "theta_pos_0p5_2_bias_deg": 0.9861852526664734,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3018548938757028,
  "loss_turn": 1.3180143121453518,
  "loss_theta": 0.00039657894150178796,
  "loss_main_bundle_base": 0.3018548938757028,
  "loss_turn_bundle_base": 0.2636028675087734,
  "loss_theta_bundle_base": 0.00025764718263930516,
  "loss_main_bundle": 0.3018548938757028,
  "loss_turn_bundle": 0.2636028675087734,
  "loss_theta_bundle": 0.00025764718263930516,
  "loss_theta_flat": 0.0001951038348653917,
  "loss_theta_near_flat": 0.0009747079638316874,
  "loss_theta_error_excess": 0.00012198039009572915,
  "loss_theta_flat_excess": 0.00010098170539989735,
  "loss_theta_near_flat_excess": 0.0006555879702278021,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010017288241633724,
  "loss_theta_small_neg": 0.00028708042508855723,
  "loss_theta_small_neg_excess": 7.773094122686847e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3871122861586017,
  "loss_false_turn_straight": 0.2960760873289973,
  "loss_transition_focal_raw": 1.0840885827280027,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.461812220648919,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
