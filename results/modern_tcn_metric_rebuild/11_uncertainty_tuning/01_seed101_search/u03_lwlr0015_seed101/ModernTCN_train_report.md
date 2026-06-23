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
| acc_main | 0.9650 |
| acc_turn | 0.5844 |
| acc_turn_pure | 0.6025 |
| acc_turn_transition | 0.5052 |
| main_confidence_mean | 0.9884 |
| main_low_conf_0p60_ratio | 0.0092 |
| main_low_conf_0p70_ratio | 0.0155 |
| turn_confidence_mean | 0.8243 |
| turn_low_conf_0p60_ratio | 0.1682 |
| turn_low_conf_0p70_ratio | 0.2707 |
| turn_right_recall | 0.6095 |
| turn_straight_recall | 0.5572 |
| turn_left_recall | 0.6218 |
| theta_mae_deg | 0.6115 |
| theta_abs_le_10_p95_abs_err_deg | 1.5391 |
| theta_neg_10_8_p95_abs_err_deg | 1.2428 |
| theta_pos_8_10_p95_abs_err_deg | 2.4365 |
| theta_abs_le_8_p95_abs_err_deg | 1.4862 |
| theta_neg_8_6_p95_abs_err_deg | 1.5387 |
| theta_pos_6_8_p95_abs_err_deg | 1.2991 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.5511 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.3508 |
| theta_flat_abs_p95_deg | 2.4236 |
| theta_flat_bias_deg | -0.1468 |
| theta_near_flat_abs_p95_deg | 1.5220 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1623 |
| theta_flat_turn_abs_p95_deg | 1.3119 |
| flat_recall | 0.9524 |
| stall_recall | 0.6979 |
| slope_recall | 0.9778 |
| flat_as_stall_ratio | 0.0013 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7557 |
| downhill_recall | 0.7980 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    720,
    1,
    35
  ],
  [
    10,
    67,
    19
  ],
  [
    52,
    9,
    2689
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    487,
    187,
    125
  ],
  [
    369,
    1077,
    487
  ],
  [
    151,
    178,
    541
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.363108 |
| test_loss_turn_bundle_base | 0.315516 |
| test_loss_theta_bundle_base | 0.000131 |
| test_loss_transition_focal_raw | 1.379578 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.114120 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 83
- train_seconds: 385.7

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 33 | 0.6061 | 0.5522 |
| [0.60,0.70) | 23 | 0.6522 | 0.6553 |
| [0.70,0.80) | 23 | 0.4348 | 0.7540 |
| [0.80,0.90) | 40 | 0.3250 | 0.8520 |
| [0.90,1.00) | 3483 | 0.0195 | 0.9979 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 606 | 0.6254 | 0.5266 |
| [0.60,0.70) | 369 | 0.4417 | 0.6473 |
| [0.70,0.80) | 403 | 0.4739 | 0.7542 |
| [0.80,0.90) | 492 | 0.4472 | 0.8532 |
| [0.90,1.00) | 1732 | 0.3141 | 0.9742 |


## 验证集最佳点

```json
{
  "loss_total": 0.6329530757076847,
  "acc_main": 0.9428958051420839,
  "acc_turn": 0.6278755074424899,
  "acc_turn_pure": 0.6427400852179613,
  "acc_turn_transition": 0.5574534161490683,
  "false_turn_straight": 0.45114345114345117,
  "flat_recall": 0.9330289193302892,
  "stall_recall": 0.3333333333333333,
  "slope_recall": 0.9536048064085447,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9330289193302892,
    0.3333333333333333,
    0.9536048064085447
  ],
  "turn_right_recall": 0.6860189573459715,
  "turn_straight_recall": 0.5488565488565489,
  "turn_left_recall": 0.7389428263214671,
  "recall_turn": [
    0.6860189573459715,
    0.5488565488565489,
    0.7389428263214671
  ],
  "cm_turn": [
    [
      579,
      194,
      71
    ],
    [
      419,
      1056,
      449
    ],
    [
      84,
      158,
      685
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      613,
      0,
      44
    ],
    [
      0,
      14,
      28
    ],
    [
      128,
      11,
      2857
    ]
  ],
  "main_confidence_mean": 0.9722920304568472,
  "main_confidence_error_mean": 0.7853374349274411,
  "main_low_conf_0p60_ratio": 0.005953991880920162,
  "main_low_conf_0p70_ratio": 0.05602165087956698,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 22,
      "error_rate": 0.5454545454545454,
      "mean_confidence": 0.5509855527390527
    },
    {
      "bin": "[0.60,0.70)",
      "n": 185,
      "error_rate": 0.4918918918918919,
      "mean_confidence": 0.606568423107507
    },
    {
      "bin": "[0.70,0.80)",
      "n": 33,
      "error_rate": 0.24242424242424243,
      "mean_confidence": 0.7626530159336751
    },
    {
      "bin": "[0.80,0.90)",
      "n": 34,
      "error_rate": 0.29411764705882354,
      "mean_confidence": 0.8558917614882402
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3421,
      "error_rate": 0.026308097047646885,
      "mean_confidence": 0.9979580072161621
    }
  ],
  "turn_confidence_mean": 0.845598334226406,
  "turn_confidence_error_mean": 0.7769543608253243,
  "turn_low_conf_0p60_ratio": 0.14100135317997295,
  "turn_low_conf_0p70_ratio": 0.22138024357239514,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 521,
      "error_rate": 0.5950095969289827,
      "mean_confidence": 0.4888250347938313
    },
    {
      "bin": "[0.60,0.70)",
      "n": 297,
      "error_rate": 0.5488215488215489,
      "mean_confidence": 0.6504440325572567
    },
    {
      "bin": "[0.70,0.80)",
      "n": 329,
      "error_rate": 0.42857142857142855,
      "mean_confidence": 0.7532280312281456
    },
    {
      "bin": "[0.80,0.90)",
      "n": 465,
      "error_rate": 0.4731182795698925,
      "mean_confidence": 0.8513928097887179
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2083,
      "error_rate": 0.2597215554488718,
      "mean_confidence": 0.9759560467324361
    }
  ],
  "theta_mae_rad": 0.012185143306851387,
  "theta_mae_deg": 0.6981572508811951,
  "uphill_recall": 0.7789757412398922,
  "downhill_recall": 0.8097886540600667,
  "slope_sign_acc": 0.9707090062961949,
  "theta_flat_mae_deg": 1.0096765756607056,
  "theta_flat_abs_p95_deg": 3.842243194580078,
  "theta_flat_abs_max_deg": 7.428805351257324,
  "theta_flat_bias_deg": 0.23475174605846405,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4260615110397339,
  "theta_near_flat_abs_p95_deg": 3.974825143814087,
  "theta_near_flat_abs_max_deg": 7.428805351257324,
  "theta_near_flat_bias_deg": 0.665482759475708,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.071562647819519,
  "theta_flat_turn_abs_p95_deg": 3.842243194580078,
  "theta_flat_turn_abs_max_deg": 7.428805351257324,
  "theta_flat_turn_bias_deg": -0.0783858448266983,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.6981572508811951,
  "theta_slope_control_abs_p95_deg": 9.158769607543945,
  "theta_slope_control_abs_max_deg": 11.267101287841797,
  "theta_slope_control_bias_deg": 0.18579699099063873,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.6981572508811951,
  "theta_all_rmse_deg": 1.080830454826355,
  "theta_all_p95_abs_err_deg": 2.5190765857696533,
  "theta_all_max_abs_err_deg": 6.928805351257324,
  "theta_all_bias_deg": 0.18579699099063873,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6298434138298035,
  "theta_active_abs_ge_2_rmse_deg": 0.9488587379455566,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.039268970489502,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.856233596801758,
  "theta_active_abs_ge_2_bias_deg": 0.17506158351898193,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7127783298492432,
  "theta_abs_le_8_rmse_deg": 1.1026725769042969,
  "theta_abs_le_8_p95_abs_err_deg": 2.7310891151428223,
  "theta_abs_le_8_max_abs_err_deg": 6.928805351257324,
  "theta_abs_le_8_bias_deg": 0.16425183415412903,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.6981572508811951,
  "theta_abs_le_10_rmse_deg": 1.080830454826355,
  "theta_abs_le_10_p95_abs_err_deg": 2.5190765857696533,
  "theta_abs_le_10_max_abs_err_deg": 6.928805351257324,
  "theta_abs_le_10_bias_deg": 0.18579699099063873,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.4795107841491699,
  "theta_pos_8_10_rmse_deg": 0.6904013752937317,
  "theta_pos_8_10_p95_abs_err_deg": 1.6368718147277832,
  "theta_pos_8_10_max_abs_err_deg": 3.2004587650299072,
  "theta_pos_8_10_bias_deg": -0.053124766796827316,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7961575984954834,
  "theta_neg_10_8_rmse_deg": 1.2107133865356445,
  "theta_neg_10_8_p95_abs_err_deg": 2.2064177989959717,
  "theta_neg_10_8_max_abs_err_deg": 6.856233596801758,
  "theta_neg_10_8_bias_deg": 0.6122011542320251,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5107558965682983,
  "theta_pos_6_8_rmse_deg": 0.7907949090003967,
  "theta_pos_6_8_p95_abs_err_deg": 1.6470364332199097,
  "theta_pos_6_8_max_abs_err_deg": 3.6757454872131348,
  "theta_pos_6_8_bias_deg": 0.2158077359199524,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.6528093814849854,
  "theta_neg_8_6_rmse_deg": 0.9784476161003113,
  "theta_neg_8_6_p95_abs_err_deg": 1.849348783493042,
  "theta_neg_8_6_max_abs_err_deg": 6.519791603088379,
  "theta_neg_8_6_bias_deg": 0.25565335154533386,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6759006977081299,
  "theta_neg_4_2_rmse_deg": 0.9107201099395752,
  "theta_neg_4_2_p95_abs_err_deg": 1.723647117614746,
  "theta_neg_4_2_max_abs_err_deg": 5.0954179763793945,
  "theta_neg_4_2_bias_deg": -0.1533263772726059,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5442947745323181,
  "theta_neg_2_0p5_rmse_deg": 0.7634679675102234,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.2953739166259766,
  "theta_neg_2_0p5_max_abs_err_deg": 3.8955235481262207,
  "theta_neg_2_0p5_bias_deg": -0.38268929719924927,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0207518339157104,
  "theta_pos_0p5_2_rmse_deg": 1.3643451929092407,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.3422434329986572,
  "theta_pos_0p5_2_max_abs_err_deg": 5.097578525543213,
  "theta_pos_0p5_2_bias_deg": 0.4451653063297272,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.34596525385512067,
  "loss_turn": 1.4337432671303032,
  "loss_theta": 0.00035585621417549227,
  "loss_main_bundle_base": 0.34596525385512067,
  "loss_turn_bundle_base": 0.2867486573765823,
  "loss_theta_bundle_base": 0.00023916122134641336,
  "loss_main_bundle": 0.34596525385512067,
  "loss_turn_bundle": 0.2867486573765823,
  "loss_theta_bundle": 0.00023916122134641336,
  "loss_theta_flat": 0.00024159493764291527,
  "loss_theta_near_flat": 0.0012152180493417346,
  "loss_theta_error_excess": 0.00012553284810043125,
  "loss_theta_flat_excess": 0.00011571185637430184,
  "loss_theta_near_flat_excess": 0.0008768914145806928,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 8.172270999742477e-05,
  "loss_theta_small_neg": 0.0002489388999368501,
  "loss_theta_small_neg_excess": 5.2876410018451035e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4105000480666696,
  "loss_false_turn_straight": 0.3346984286592197,
  "loss_transition_focal_raw": 1.258425328566999,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.4224163442531585,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
