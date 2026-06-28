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
  "freeze_mode": "trunk",
  "freeze_early_blocks": 3,
  "preserve_mode": "baseline",
  "lambda_preserve_main": 0.05,
  "lambda_preserve_turn": 0.05,
  "lambda_preserve_theta": 0.05,
  "s_range": 0.25,
  "lambda_s_prior": 0.01
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9661 |
| acc_turn | 0.6124 |
| acc_turn_pure | 0.6370 |
| acc_turn_transition | 0.5052 |
| main_confidence_mean | 0.9876 |
| main_low_conf_0p60_ratio | 0.0086 |
| main_low_conf_0p70_ratio | 0.0167 |
| turn_confidence_mean | 0.8230 |
| turn_low_conf_0p60_ratio | 0.1652 |
| turn_low_conf_0p70_ratio | 0.2779 |
| turn_right_recall | 0.5469 |
| turn_straight_recall | 0.6813 |
| turn_left_recall | 0.5195 |
| theta_mae_deg | 0.7049 |
| theta_abs_le_10_p95_abs_err_deg | 1.9301 |
| theta_neg_10_8_p95_abs_err_deg | 1.6009 |
| theta_pos_8_10_p95_abs_err_deg | 3.0212 |
| theta_abs_le_8_p95_abs_err_deg | 1.8846 |
| theta_neg_8_6_p95_abs_err_deg | 1.7791 |
| theta_pos_6_8_p95_abs_err_deg | 1.8589 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.7048 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.9601 |
| theta_flat_abs_p95_deg | 2.4152 |
| theta_flat_bias_deg | -0.2160 |
| theta_near_flat_abs_p95_deg | 2.3157 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.4229 |
| theta_flat_turn_abs_p95_deg | 2.3186 |
| flat_recall | 0.9722 |
| stall_recall | 0.6979 |
| slope_recall | 0.9738 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7477 |
| downhill_recall | 0.7917 |

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
    9,
    67,
    20
  ],
  [
    66,
    6,
    2678
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    437,
    253,
    109
  ],
  [
    298,
    1317,
    318
  ],
  [
    156,
    262,
    452
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.330642 |
| test_loss_turn_bundle_base | 0.297942 |
| test_loss_theta_bundle_base | 0.000172 |
| test_loss_transition_focal_raw | 1.447773 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.614239 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 1
- train_seconds: 3.7

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 31 | 0.7742 | 0.5492 |
| [0.60,0.70) | 29 | 0.4483 | 0.6476 |
| [0.70,0.80) | 29 | 0.3103 | 0.7602 |
| [0.80,0.90) | 41 | 0.2927 | 0.8535 |
| [0.90,1.00) | 3472 | 0.0184 | 0.9978 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 595 | 0.5630 | 0.5119 |
| [0.60,0.70) | 406 | 0.4433 | 0.6511 |
| [0.70,0.80) | 406 | 0.4729 | 0.7518 |
| [0.80,0.90) | 430 | 0.4512 | 0.8546 |
| [0.90,1.00) | 1765 | 0.2805 | 0.9760 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.5052
- theta_mae_deg <= 0.7000 未满足，实际 0.7049

## 验证集最佳点

```json
{
  "loss_total": 0.5653892212694811,
  "acc_main": 0.9499323410013532,
  "acc_turn": 0.6479025710419486,
  "acc_turn_pure": 0.6637168141592921,
  "acc_turn_transition": 0.5729813664596274,
  "false_turn_straight": 0.3305613305613306,
  "flat_recall": 0.954337899543379,
  "stall_recall": 0.5714285714285714,
  "slope_recall": 0.9542723631508678,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.954337899543379,
    0.5714285714285714,
    0.9542723631508678
  ],
  "turn_right_recall": 0.6137440758293838,
  "turn_straight_recall": 0.6694386694386695,
  "turn_left_recall": 0.6343042071197411,
  "recall_turn": [
    0.6137440758293838,
    0.6694386694386695,
    0.6343042071197411
  ],
  "cm_turn": [
    [
      518,
      297,
      29
    ],
    [
      279,
      1288,
      357
    ],
    [
      63,
      276,
      588
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      627,
      0,
      30
    ],
    [
      0,
      24,
      18
    ],
    [
      130,
      7,
      2859
    ]
  ],
  "main_confidence_mean": 0.9693659052478358,
  "main_confidence_error_mean": 0.7602339777187848,
  "main_low_conf_0p60_ratio": 0.05087956698240866,
  "main_low_conf_0p70_ratio": 0.05629228687415426,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 188,
      "error_rate": 0.44680851063829785,
      "mean_confidence": 0.5706871449838974
    },
    {
      "bin": "[0.60,0.70)",
      "n": 20,
      "error_rate": 0.55,
      "mean_confidence": 0.6426777253675622
    },
    {
      "bin": "[0.70,0.80)",
      "n": 44,
      "error_rate": 0.2727272727272727,
      "mean_confidence": 0.7593104511481598
    },
    {
      "bin": "[0.80,0.90)",
      "n": 40,
      "error_rate": 0.125,
      "mean_confidence": 0.866349764944124
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3403,
      "error_rate": 0.02145166029973553,
      "mean_confidence": 0.9972379170373629
    }
  ],
  "turn_confidence_mean": 0.8316238210178509,
  "turn_confidence_error_mean": 0.7681271441636506,
  "turn_low_conf_0p60_ratio": 0.16400541271989175,
  "turn_low_conf_0p70_ratio": 0.2614343707713126,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 606,
      "error_rate": 0.5132013201320133,
      "mean_confidence": 0.4999456135977017
    },
    {
      "bin": "[0.60,0.70)",
      "n": 360,
      "error_rate": 0.5027777777777778,
      "mean_confidence": 0.6539715039553643
    },
    {
      "bin": "[0.70,0.80)",
      "n": 362,
      "error_rate": 0.43370165745856354,
      "mean_confidence": 0.7499711448704401
    },
    {
      "bin": "[0.80,0.90)",
      "n": 434,
      "error_rate": 0.4447004608294931,
      "mean_confidence": 0.8531869140307647
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1933,
      "error_rate": 0.23745473357475427,
      "mean_confidence": 0.9791415210886549
    }
  ],
  "theta_mae_rad": 0.014217576943337917,
  "theta_mae_deg": 0.8146070837974548,
  "uphill_recall": 0.7795148247978436,
  "downhill_recall": 0.8025583982202447,
  "slope_sign_acc": 0.9660552970161511,
  "theta_flat_mae_deg": 1.1731623411178589,
  "theta_flat_abs_p95_deg": 4.292579174041748,
  "theta_flat_abs_max_deg": 8.643890380859375,
  "theta_flat_bias_deg": 0.08295733481645584,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.6120924949645996,
  "theta_near_flat_abs_p95_deg": 4.296814441680908,
  "theta_near_flat_abs_max_deg": 8.643890380859375,
  "theta_near_flat_bias_deg": 0.36885520815849304,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.2425537109375,
  "theta_flat_turn_abs_p95_deg": 4.292579174041748,
  "theta_flat_turn_abs_max_deg": 8.643890380859375,
  "theta_flat_turn_bias_deg": -0.3435742259025574,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8146070837974548,
  "theta_slope_control_abs_p95_deg": 9.09968090057373,
  "theta_slope_control_abs_max_deg": 12.052152633666992,
  "theta_slope_control_bias_deg": 0.14051473140716553,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8146070837974548,
  "theta_all_rmse_deg": 1.2247384786605835,
  "theta_all_p95_abs_err_deg": 2.792578935623169,
  "theta_all_max_abs_err_deg": 8.143890380859375,
  "theta_all_bias_deg": 0.14051470160484314,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7359786033630371,
  "theta_active_abs_ge_2_rmse_deg": 1.0742594003677368,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.1592633724212646,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.187395095825195,
  "theta_active_abs_ge_2_bias_deg": 0.15313661098480225,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8436382412910461,
  "theta_abs_le_8_rmse_deg": 1.2556487321853638,
  "theta_abs_le_8_p95_abs_err_deg": 2.792578935623169,
  "theta_abs_le_8_max_abs_err_deg": 8.143890380859375,
  "theta_abs_le_8_bias_deg": 0.1265449821949005,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8146070837974548,
  "theta_abs_le_10_rmse_deg": 1.2247384786605835,
  "theta_abs_le_10_p95_abs_err_deg": 2.792578935623169,
  "theta_abs_le_10_max_abs_err_deg": 8.143890380859375,
  "theta_abs_le_10_bias_deg": 0.14051470160484314,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.4946211278438568,
  "theta_pos_8_10_rmse_deg": 0.6952937245368958,
  "theta_pos_8_10_p95_abs_err_deg": 1.3789328336715698,
  "theta_pos_8_10_max_abs_err_deg": 4.041074275970459,
  "theta_pos_8_10_bias_deg": -0.1783323436975479,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8930681943893433,
  "theta_neg_10_8_rmse_deg": 1.3717327117919922,
  "theta_neg_10_8_p95_abs_err_deg": 2.478252410888672,
  "theta_neg_10_8_max_abs_err_deg": 7.187395095825195,
  "theta_neg_10_8_bias_deg": 0.583758533000946,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5872540473937988,
  "theta_pos_6_8_rmse_deg": 0.7543672919273376,
  "theta_pos_6_8_p95_abs_err_deg": 1.3923156261444092,
  "theta_pos_6_8_max_abs_err_deg": 3.2261672019958496,
  "theta_pos_6_8_bias_deg": 0.045360222458839417,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8082814812660217,
  "theta_neg_8_6_rmse_deg": 1.1949127912521362,
  "theta_neg_8_6_p95_abs_err_deg": 2.249783515930176,
  "theta_neg_8_6_max_abs_err_deg": 6.573958873748779,
  "theta_neg_8_6_bias_deg": 0.22731509804725647,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6474792957305908,
  "theta_neg_4_2_rmse_deg": 0.9088603854179382,
  "theta_neg_4_2_p95_abs_err_deg": 1.8013782501220703,
  "theta_neg_4_2_max_abs_err_deg": 4.560223579406738,
  "theta_neg_4_2_bias_deg": 0.13698731362819672,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6769176721572876,
  "theta_neg_2_0p5_rmse_deg": 0.9546737670898438,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.056629180908203,
  "theta_neg_2_0p5_max_abs_err_deg": 4.444238185882568,
  "theta_neg_2_0p5_bias_deg": -0.4653301239013672,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0782045125961304,
  "theta_pos_0p5_2_rmse_deg": 1.5723296403884888,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.792578935623169,
  "theta_pos_0p5_2_max_abs_err_deg": 4.559389114379883,
  "theta_pos_0p5_2_bias_deg": 0.42993655800819397,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3000720371896746,
  "loss_turn": 1.3251286708614984,
  "loss_theta": 0.0004570562829306357,
  "loss_main_bundle_base": 0.3000720371896746,
  "loss_turn_bundle_base": 0.26502573980933436,
  "loss_theta_bundle_base": 0.0002914331719409725,
  "loss_main_bundle": 0.3000720371896746,
  "loss_turn_bundle": 0.26502573980933436,
  "loss_theta_bundle": 0.0002914331719409725,
  "loss_theta_flat": 0.0003337684283817517,
  "loss_theta_near_flat": 0.0016164495415622634,
  "loss_theta_error_excess": 0.00017147187120879778,
  "loss_theta_flat_excess": 0.00018877287252575502,
  "loss_theta_near_flat_excess": 0.001184578052014919,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00011158171387897182,
  "loss_theta_small_neg": 0.0002487293034284697,
  "loss_theta_small_neg_excess": 5.3129691655964353e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.31477813763450707,
  "loss_false_turn_straight": 0.2587746160359441,
  "loss_transition_focal_raw": 1.1502947539212094,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.794000582080621,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0,
  "preserve_loss": 0.0021099746227264404
}
```
