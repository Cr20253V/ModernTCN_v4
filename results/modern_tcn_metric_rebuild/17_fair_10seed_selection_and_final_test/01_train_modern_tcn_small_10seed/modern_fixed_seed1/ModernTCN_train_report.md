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
| acc_main | 0.9645 |
| acc_turn | 0.6138 |
| acc_turn_pure | 0.6308 |
| acc_turn_transition | 0.5395 |
| main_confidence_mean | 0.9898 |
| main_low_conf_0p60_ratio | 0.0075 |
| main_low_conf_0p70_ratio | 0.0139 |
| turn_confidence_mean | 0.8508 |
| turn_low_conf_0p60_ratio | 0.1385 |
| turn_low_conf_0p70_ratio | 0.2315 |
| turn_right_recall | 0.5257 |
| turn_straight_recall | 0.6689 |
| turn_left_recall | 0.5724 |
| theta_mae_deg | 0.5342 |
| theta_abs_le_10_p95_abs_err_deg | 1.5876 |
| theta_neg_10_8_p95_abs_err_deg | 1.4355 |
| theta_pos_8_10_p95_abs_err_deg | 2.5614 |
| theta_abs_le_8_p95_abs_err_deg | 1.4351 |
| theta_neg_8_6_p95_abs_err_deg | 1.3330 |
| theta_pos_6_8_p95_abs_err_deg | 1.5209 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.0423 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.1386 |
| theta_flat_abs_p95_deg | 2.2856 |
| theta_flat_bias_deg | 0.1668 |
| theta_near_flat_abs_p95_deg | 1.9902 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.4139 |
| theta_flat_turn_abs_p95_deg | 1.8939 |
| flat_recall | 0.9656 |
| stall_recall | 0.6979 |
| slope_recall | 0.9735 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7489 |
| downhill_recall | 0.7928 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    730,
    0,
    26
  ],
  [
    10,
    67,
    19
  ],
  [
    65,
    8,
    2677
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    420,
    262,
    117
  ],
  [
    258,
    1293,
    382
  ],
  [
    131,
    241,
    498
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.356692 |
| test_loss_turn_bundle_base | 0.144160 |
| test_loss_theta_bundle_base | 0.000128 |
| test_loss_transition_focal_raw | 1.716452 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.921388 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 113
- train_seconds: 1404.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 27 | 0.5556 | 0.5329 |
| [0.60,0.70) | 23 | 0.4783 | 0.6624 |
| [0.70,0.80) | 22 | 0.7727 | 0.7469 |
| [0.80,0.90) | 38 | 0.1579 | 0.8571 |
| [0.90,1.00) | 3492 | 0.0226 | 0.9984 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 499 | 0.5671 | 0.5261 |
| [0.60,0.70) | 335 | 0.5433 | 0.6493 |
| [0.70,0.80) | 343 | 0.4927 | 0.7497 |
| [0.80,0.90) | 400 | 0.4775 | 0.8553 |
| [0.90,1.00) | 2025 | 0.2795 | 0.9804 |


## 验证集最佳点

```json
{
  "loss_total": 0.4577659543376814,
  "acc_main": 0.9396481732070365,
  "acc_turn": 0.6638700947225981,
  "acc_turn_pure": 0.6728941330711242,
  "acc_turn_transition": 0.6211180124223602,
  "false_turn_straight": 0.3196465696465696,
  "flat_recall": 0.943683409436834,
  "stall_recall": 0.4523809523809524,
  "slope_recall": 0.9455941255006676,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.07142857142857142,
  "recall_main": [
    0.943683409436834,
    0.4523809523809524,
    0.9455941255006676
  ],
  "turn_right_recall": 0.6149289099526066,
  "turn_straight_recall": 0.6803534303534303,
  "turn_left_recall": 0.674217907227616,
  "recall_turn": [
    0.6149289099526066,
    0.6803534303534303,
    0.674217907227616
  ],
  "cm_turn": [
    [
      519,
      245,
      80
    ],
    [
      232,
      1309,
      383
    ],
    [
      59,
      243,
      625
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      620,
      0,
      37
    ],
    [
      3,
      19,
      20
    ],
    [
      155,
      8,
      2833
    ]
  ],
  "main_confidence_mean": 0.9701009288565464,
  "main_confidence_error_mean": 0.7762696431988791,
  "main_low_conf_0p60_ratio": 0.0503382949932341,
  "main_low_conf_0p70_ratio": 0.0571041948579161,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 186,
      "error_rate": 0.46236559139784944,
      "mean_confidence": 0.554652306486447
    },
    {
      "bin": "[0.60,0.70)",
      "n": 25,
      "error_rate": 0.4,
      "mean_confidence": 0.659570453054855
    },
    {
      "bin": "[0.70,0.80)",
      "n": 28,
      "error_rate": 0.5357142857142857,
      "mean_confidence": 0.7554001390649638
    },
    {
      "bin": "[0.80,0.90)",
      "n": 44,
      "error_rate": 0.36363636363636365,
      "mean_confidence": 0.8588965908246308
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3412,
      "error_rate": 0.02813599062133646,
      "mean_confidence": 0.9982197209560334
    }
  ],
  "turn_confidence_mean": 0.8653275184140438,
  "turn_confidence_error_mean": 0.7868555481770453,
  "turn_low_conf_0p60_ratio": 0.13721244925575102,
  "turn_low_conf_0p70_ratio": 0.20974289580514208,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 507,
      "error_rate": 0.6055226824457594,
      "mean_confidence": 0.517864685060522
    },
    {
      "bin": "[0.60,0.70)",
      "n": 268,
      "error_rate": 0.5261194029850746,
      "mean_confidence": 0.6508243215849855
    },
    {
      "bin": "[0.70,0.80)",
      "n": 262,
      "error_rate": 0.44656488549618323,
      "mean_confidence": 0.7470449654724444
    },
    {
      "bin": "[0.80,0.90)",
      "n": 370,
      "error_rate": 0.3918918918918919,
      "mean_confidence": 0.8530354234170208
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2288,
      "error_rate": 0.23251748251748253,
      "mean_confidence": 0.9829798861063604
    }
  ],
  "theta_mae_rad": 0.012531876564025879,
  "theta_mae_deg": 0.7180235981941223,
  "uphill_recall": 0.7768194070080863,
  "downhill_recall": 0.7947719688542826,
  "slope_sign_acc": 0.9644128113879004,
  "theta_flat_mae_deg": 1.0291553735733032,
  "theta_flat_abs_p95_deg": 3.94124436378479,
  "theta_flat_abs_max_deg": 10.261805534362793,
  "theta_flat_bias_deg": 0.6989301443099976,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4568918943405151,
  "theta_near_flat_abs_p95_deg": 3.941376209259033,
  "theta_near_flat_abs_max_deg": 10.261805534362793,
  "theta_near_flat_bias_deg": 1.1448131799697876,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.2157442569732666,
  "theta_flat_turn_abs_p95_deg": 4.130555152893066,
  "theta_flat_turn_abs_max_deg": 10.261805534362793,
  "theta_flat_turn_bias_deg": 0.7869270443916321,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7180235981941223,
  "theta_slope_control_abs_p95_deg": 9.398451805114746,
  "theta_slope_control_abs_max_deg": 11.618338584899902,
  "theta_slope_control_bias_deg": 0.056127361953258514,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7180236577987671,
  "theta_all_rmse_deg": 1.169894814491272,
  "theta_all_p95_abs_err_deg": 2.44124436378479,
  "theta_all_max_abs_err_deg": 10.761805534362793,
  "theta_all_bias_deg": 0.05612736940383911,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6497947573661804,
  "theta_active_abs_ge_2_rmse_deg": 0.9994418025016785,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.0363869667053223,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.656764984130859,
  "theta_active_abs_ge_2_bias_deg": -0.08483438193798065,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7440387010574341,
  "theta_abs_le_8_rmse_deg": 1.218169927597046,
  "theta_abs_le_8_p95_abs_err_deg": 2.6106691360473633,
  "theta_abs_le_8_max_abs_err_deg": 10.761805534362793,
  "theta_abs_le_8_bias_deg": 0.11944489926099777,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7180236577987671,
  "theta_abs_le_10_rmse_deg": 1.169894814491272,
  "theta_abs_le_10_p95_abs_err_deg": 2.44124436378479,
  "theta_abs_le_10_max_abs_err_deg": 10.761805534362793,
  "theta_abs_le_10_bias_deg": 0.05612736940383911,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5796314477920532,
  "theta_pos_8_10_rmse_deg": 0.7791833281517029,
  "theta_pos_8_10_p95_abs_err_deg": 1.2331660985946655,
  "theta_pos_8_10_max_abs_err_deg": 5.323930740356445,
  "theta_pos_8_10_bias_deg": -0.3538660705089569,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6374181509017944,
  "theta_neg_10_8_rmse_deg": 1.078086495399475,
  "theta_neg_10_8_p95_abs_err_deg": 1.6330393552780151,
  "theta_neg_10_8_max_abs_err_deg": 6.656764984130859,
  "theta_neg_10_8_bias_deg": -0.06562769412994385,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5185088515281677,
  "theta_pos_6_8_rmse_deg": 0.7945080399513245,
  "theta_pos_6_8_p95_abs_err_deg": 1.5401341915130615,
  "theta_pos_6_8_max_abs_err_deg": 3.5942161083221436,
  "theta_pos_6_8_bias_deg": -0.1398547887802124,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7317031621932983,
  "theta_neg_8_6_rmse_deg": 1.1067111492156982,
  "theta_neg_8_6_p95_abs_err_deg": 2.3474555015563965,
  "theta_neg_8_6_max_abs_err_deg": 6.633626937866211,
  "theta_neg_8_6_bias_deg": -0.02084929496049881,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6623328924179077,
  "theta_neg_4_2_rmse_deg": 1.012380838394165,
  "theta_neg_4_2_p95_abs_err_deg": 1.804227590560913,
  "theta_neg_4_2_max_abs_err_deg": 4.968661785125732,
  "theta_neg_4_2_bias_deg": -0.18294201791286469,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5022862553596497,
  "theta_neg_2_0p5_rmse_deg": 0.6809734106063843,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.0775715112686157,
  "theta_neg_2_0p5_max_abs_err_deg": 3.782405376434326,
  "theta_neg_2_0p5_bias_deg": 0.0008781933574937284,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.9803524017333984,
  "theta_pos_0p5_2_rmse_deg": 1.3539319038391113,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.44124436378479,
  "theta_pos_0p5_2_max_abs_err_deg": 3.459784746170044,
  "theta_pos_0p5_2_bias_deg": 0.8306658267974854,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.32778071696606637,
  "loss_turn": 1.6214242484153365,
  "loss_theta": 0.00041676531144114104,
  "loss_main_bundle_base": 0.32778071696606637,
  "loss_turn_bundle_base": 0.1297139365392383,
  "loss_theta_bundle_base": 0.00027130555705084177,
  "loss_main_bundle": 0.32778071696606637,
  "loss_turn_bundle": 0.1297139365392383,
  "loss_theta_bundle": 0.00027130555705084177,
  "loss_theta_flat": 0.00019107136875942365,
  "loss_theta_near_flat": 0.0015869796311064385,
  "loss_theta_error_excess": 0.00017605367543066175,
  "loss_theta_flat_excess": 0.00010737528827095578,
  "loss_theta_near_flat_excess": 0.001235645769494151,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010353384774363523,
  "loss_theta_small_neg": 0.00031170438813154003,
  "loss_theta_small_neg_excess": 0.00010731064559953572,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.2967117852141957,
  "loss_false_turn_straight": 0.23491359985407054,
  "loss_transition_focal_raw": 1.4194395159352293,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.384943402014476,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
