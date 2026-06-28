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
  "freeze_mode": "early_blocks",
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
| acc_main | 0.9706 |
| acc_turn | 0.6102 |
| acc_turn_pure | 0.6339 |
| acc_turn_transition | 0.5067 |
| main_confidence_mean | 0.9865 |
| main_low_conf_0p60_ratio | 0.0111 |
| main_low_conf_0p70_ratio | 0.0200 |
| turn_confidence_mean | 0.8225 |
| turn_low_conf_0p60_ratio | 0.1699 |
| turn_low_conf_0p70_ratio | 0.2760 |
| turn_right_recall | 0.5720 |
| turn_straight_recall | 0.6689 |
| turn_left_recall | 0.5149 |
| theta_mae_deg | 0.7006 |
| theta_abs_le_10_p95_abs_err_deg | 1.9639 |
| theta_neg_10_8_p95_abs_err_deg | 1.6608 |
| theta_pos_8_10_p95_abs_err_deg | 2.8622 |
| theta_abs_le_8_p95_abs_err_deg | 1.9452 |
| theta_neg_8_6_p95_abs_err_deg | 1.8768 |
| theta_pos_6_8_p95_abs_err_deg | 2.0555 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6183 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.0915 |
| theta_flat_abs_p95_deg | 2.3738 |
| theta_flat_bias_deg | -0.1399 |
| theta_near_flat_abs_p95_deg | 2.1431 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.3641 |
| theta_flat_turn_abs_p95_deg | 2.0752 |
| flat_recall | 0.9683 |
| stall_recall | 0.7083 |
| slope_recall | 0.9804 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7592 |
| downhill_recall | 0.7923 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    732,
    0,
    24
  ],
  [
    9,
    68,
    19
  ],
  [
    46,
    8,
    2696
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    457,
    230,
    112
  ],
  [
    322,
    1293,
    318
  ],
  [
    160,
    262,
    448
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.325306 |
| test_loss_turn_bundle_base | 0.288681 |
| test_loss_theta_bundle_base | 0.000175 |
| test_loss_transition_focal_raw | 1.431326 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.460063 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 1
- train_seconds: 5.9

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 40 | 0.3000 | 0.5544 |
| [0.60,0.70) | 32 | 0.4062 | 0.6455 |
| [0.70,0.80) | 23 | 0.4348 | 0.7537 |
| [0.80,0.90) | 39 | 0.2051 | 0.8552 |
| [0.90,1.00) | 3468 | 0.0182 | 0.9976 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 612 | 0.5572 | 0.5136 |
| [0.60,0.70) | 382 | 0.4895 | 0.6492 |
| [0.70,0.80) | 376 | 0.4441 | 0.7494 |
| [0.80,0.90) | 478 | 0.4728 | 0.8520 |
| [0.90,1.00) | 1754 | 0.2754 | 0.9757 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.5067
- theta_mae_deg <= 0.7000 未满足，实际 0.7006

## 验证集最佳点

```json
{
  "loss_total": 0.5811777951752866,
  "acc_main": 0.945872801082544,
  "acc_turn": 0.6497970230040595,
  "acc_turn_pure": 0.6647000983284169,
  "acc_turn_transition": 0.5791925465838509,
  "false_turn_straight": 0.34563409563409564,
  "flat_recall": 0.9528158295281582,
  "stall_recall": 0.7142857142857143,
  "slope_recall": 0.9475967957276369,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9528158295281582,
    0.7142857142857143,
    0.9475967957276369
  ],
  "turn_right_recall": 0.6255924170616114,
  "turn_straight_recall": 0.6543659043659044,
  "turn_left_recall": 0.6623516720604099,
  "recall_turn": [
    0.6255924170616114,
    0.6543659043659044,
    0.6623516720604099
  ],
  "cm_turn": [
    [
      528,
      283,
      33
    ],
    [
      311,
      1259,
      354
    ],
    [
      59,
      254,
      614
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      626,
      0,
      31
    ],
    [
      0,
      30,
      12
    ],
    [
      141,
      16,
      2839
    ]
  ],
  "main_confidence_mean": 0.9688366269795533,
  "main_confidence_error_mean": 0.7721304587964917,
  "main_low_conf_0p60_ratio": 0.05277401894451962,
  "main_low_conf_0p70_ratio": 0.06035182679296346,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 195,
      "error_rate": 0.4564102564102564,
      "mean_confidence": 0.5869304111423258
    },
    {
      "bin": "[0.60,0.70)",
      "n": 28,
      "error_rate": 0.32142857142857145,
      "mean_confidence": 0.653035237341139
    },
    {
      "bin": "[0.70,0.80)",
      "n": 35,
      "error_rate": 0.37142857142857144,
      "mean_confidence": 0.7521790511482465
    },
    {
      "bin": "[0.80,0.90)",
      "n": 57,
      "error_rate": 0.22807017543859648,
      "mean_confidence": 0.8531521897950664
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3380,
      "error_rate": 0.022485207100591716,
      "mean_confidence": 0.9976801710836203
    }
  ],
  "turn_confidence_mean": 0.8347385273626249,
  "turn_confidence_error_mean": 0.7729392943342303,
  "turn_low_conf_0p60_ratio": 0.15723951285520973,
  "turn_low_conf_0p70_ratio": 0.2449255751014885,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 581,
      "error_rate": 0.5283993115318416,
      "mean_confidence": 0.4935354442332808
    },
    {
      "bin": "[0.60,0.70)",
      "n": 324,
      "error_rate": 0.49074074074074076,
      "mean_confidence": 0.6517438736281498
    },
    {
      "bin": "[0.70,0.80)",
      "n": 387,
      "error_rate": 0.4134366925064599,
      "mean_confidence": 0.7481974079024658
    },
    {
      "bin": "[0.80,0.90)",
      "n": 462,
      "error_rate": 0.4264069264069264,
      "mean_confidence": 0.8550150553583025
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1941,
      "error_rate": 0.2426584234930448,
      "mean_confidence": 0.9798456455518043
    }
  ],
  "theta_mae_rad": 0.014319744892418385,
  "theta_mae_deg": 0.8204609155654907,
  "uphill_recall": 0.7800539083557951,
  "downhill_recall": 0.7914349276974416,
  "slope_sign_acc": 0.9657815494114427,
  "theta_flat_mae_deg": 1.1723624467849731,
  "theta_flat_abs_p95_deg": 4.340750694274902,
  "theta_flat_abs_max_deg": 8.9046049118042,
  "theta_flat_bias_deg": 0.14751268923282623,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.6210103034973145,
  "theta_near_flat_abs_p95_deg": 4.345109939575195,
  "theta_near_flat_abs_max_deg": 8.9046049118042,
  "theta_near_flat_bias_deg": 0.41659867763519287,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.2988252639770508,
  "theta_flat_turn_abs_p95_deg": 4.340750694274902,
  "theta_flat_turn_abs_max_deg": 8.9046049118042,
  "theta_flat_turn_bias_deg": -0.31158363819122314,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8204609155654907,
  "theta_slope_control_abs_p95_deg": 9.171304702758789,
  "theta_slope_control_abs_max_deg": 11.621826171875,
  "theta_slope_control_bias_deg": 0.21767981350421906,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.820460855960846,
  "theta_all_rmse_deg": 1.242199182510376,
  "theta_all_p95_abs_err_deg": 2.8407506942749023,
  "theta_all_max_abs_err_deg": 8.4046049118042,
  "theta_all_bias_deg": 0.21767984330654144,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7432914972305298,
  "theta_active_abs_ge_2_rmse_deg": 1.0925750732421875,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.145202398300171,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.082420349121094,
  "theta_active_abs_ge_2_bias_deg": 0.23306694626808167,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.850509524345398,
  "theta_abs_le_8_rmse_deg": 1.2720600366592407,
  "theta_abs_le_8_p95_abs_err_deg": 2.8407506942749023,
  "theta_abs_le_8_max_abs_err_deg": 8.4046049118042,
  "theta_abs_le_8_bias_deg": 0.196761816740036,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.820460855960846,
  "theta_abs_le_10_rmse_deg": 1.242199182510376,
  "theta_abs_le_10_p95_abs_err_deg": 2.8407506942749023,
  "theta_abs_le_10_max_abs_err_deg": 8.4046049118042,
  "theta_abs_le_10_bias_deg": 0.21767984330654144,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.48813480138778687,
  "theta_pos_8_10_rmse_deg": 0.7041904926300049,
  "theta_pos_8_10_p95_abs_err_deg": 1.4733480215072632,
  "theta_pos_8_10_max_abs_err_deg": 3.926825761795044,
  "theta_pos_8_10_bias_deg": -0.08300463855266571,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.902816653251648,
  "theta_neg_10_8_rmse_deg": 1.4033602476119995,
  "theta_neg_10_8_p95_abs_err_deg": 2.593493700027466,
  "theta_neg_10_8_max_abs_err_deg": 7.082420349121094,
  "theta_neg_10_8_bias_deg": 0.7015774250030518,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5698941946029663,
  "theta_pos_6_8_rmse_deg": 0.7562255859375,
  "theta_pos_6_8_p95_abs_err_deg": 1.292251706123352,
  "theta_pos_6_8_max_abs_err_deg": 3.0837976932525635,
  "theta_pos_6_8_bias_deg": 0.16644428670406342,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.806199848651886,
  "theta_neg_8_6_rmse_deg": 1.1980547904968262,
  "theta_neg_8_6_p95_abs_err_deg": 2.13155198097229,
  "theta_neg_8_6_max_abs_err_deg": 6.6541972160339355,
  "theta_neg_8_6_bias_deg": 0.28240203857421875,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7000524997711182,
  "theta_neg_4_2_rmse_deg": 0.958057701587677,
  "theta_neg_4_2_p95_abs_err_deg": 1.8350536823272705,
  "theta_neg_4_2_max_abs_err_deg": 4.723578453063965,
  "theta_neg_4_2_bias_deg": 0.21353021264076233,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6377823948860168,
  "theta_neg_2_0p5_rmse_deg": 0.9119243621826172,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.9370101690292358,
  "theta_neg_2_0p5_max_abs_err_deg": 4.55374813079834,
  "theta_neg_2_0p5_bias_deg": -0.31885337829589844,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.096026062965393,
  "theta_pos_0p5_2_rmse_deg": 1.5839648246765137,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.8407506942749023,
  "theta_pos_0p5_2_max_abs_err_deg": 4.532905578613281,
  "theta_pos_0p5_2_bias_deg": 0.4258604347705841,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.30960338831109185,
  "loss_turn": 1.3563708035645852,
  "loss_theta": 0.00047020813556078,
  "loss_main_bundle_base": 0.30960338831109185,
  "loss_turn_bundle_base": 0.2712741646981207,
  "loss_theta_bundle_base": 0.00030024179519898937,
  "loss_main_bundle": 0.30960338831109185,
  "loss_turn_bundle": 0.2712741646981207,
  "loss_theta_bundle": 0.00030024179519898937,
  "loss_theta_flat": 0.0003468942693472463,
  "loss_theta_near_flat": 0.0016589578104373043,
  "loss_theta_error_excess": 0.0001797732454047227,
  "loss_theta_flat_excess": 0.00019815870334963907,
  "loss_theta_near_flat_excess": 0.0012210087259003895,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00011773398112557975,
  "loss_theta_small_neg": 0.0002765663083550093,
  "loss_theta_small_neg_excess": 6.1620495154356e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3264389234482839,
  "loss_false_turn_straight": 0.26703217586903194,
  "loss_transition_focal_raw": 1.2054631308709172,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.4305830592889937,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0,
  "preserve_loss": 0.0037820166908204556
}
```
