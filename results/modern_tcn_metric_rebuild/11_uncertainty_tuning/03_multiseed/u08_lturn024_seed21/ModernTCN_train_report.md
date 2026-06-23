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
  "lambda_turn": 0.24,
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
| acc_main | 0.9731 |
| acc_turn | 0.5719 |
| acc_turn_pure | 0.5868 |
| acc_turn_transition | 0.5067 |
| main_confidence_mean | 0.9902 |
| main_low_conf_0p60_ratio | 0.0056 |
| main_low_conf_0p70_ratio | 0.0122 |
| turn_confidence_mean | 0.8333 |
| turn_low_conf_0p60_ratio | 0.1419 |
| turn_low_conf_0p70_ratio | 0.2468 |
| turn_right_recall | 0.6295 |
| turn_straight_recall | 0.5566 |
| turn_left_recall | 0.5529 |
| theta_mae_deg | 0.7798 |
| theta_abs_le_10_p95_abs_err_deg | 2.1956 |
| theta_neg_10_8_p95_abs_err_deg | 2.7015 |
| theta_pos_8_10_p95_abs_err_deg | 3.0288 |
| theta_abs_le_8_p95_abs_err_deg | 2.0505 |
| theta_neg_8_6_p95_abs_err_deg | 2.0612 |
| theta_pos_6_8_p95_abs_err_deg | 1.4471 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.7001 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.5453 |
| theta_flat_abs_p95_deg | 2.1916 |
| theta_flat_bias_deg | -0.5399 |
| theta_near_flat_abs_p95_deg | 1.8470 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.5602 |
| theta_flat_turn_abs_p95_deg | 1.7889 |
| flat_recall | 0.9802 |
| stall_recall | 0.6979 |
| slope_recall | 0.9807 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7609 |
| downhill_recall | 0.7860 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    741,
    0,
    15
  ],
  [
    9,
    67,
    20
  ],
  [
    43,
    10,
    2697
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    503,
    192,
    104
  ],
  [
    396,
    1076,
    461
  ],
  [
    149,
    240,
    481
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.288649 |
| test_loss_turn_bundle_base | 0.382493 |
| test_loss_theta_bundle_base | 0.000230 |
| test_loss_transition_focal_raw | 1.480540 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.422636 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 74
- train_seconds: 351.9

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 20 | 0.7000 | 0.5646 |
| [0.60,0.70) | 24 | 0.5000 | 0.6413 |
| [0.70,0.80) | 23 | 0.2609 | 0.7533 |
| [0.80,0.90) | 33 | 0.2727 | 0.8521 |
| [0.90,1.00) | 3502 | 0.0160 | 0.9979 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 511 | 0.6341 | 0.5318 |
| [0.60,0.70) | 378 | 0.5767 | 0.6493 |
| [0.70,0.80) | 460 | 0.5174 | 0.7522 |
| [0.80,0.90) | 482 | 0.4959 | 0.8505 |
| [0.90,1.00) | 1771 | 0.2953 | 0.9759 |


## 验证集最佳点

```json
{
  "loss_total": 0.6080063840210519,
  "acc_main": 0.9523680649526387,
  "acc_turn": 0.6411366711772666,
  "acc_turn_pure": 0.6522451655195018,
  "acc_turn_transition": 0.5885093167701864,
  "false_turn_straight": 0.4282744282744283,
  "flat_recall": 0.9573820395738204,
  "stall_recall": 0.5714285714285714,
  "slope_recall": 0.9566088117489987,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9573820395738204,
    0.5714285714285714,
    0.9566088117489987
  ],
  "turn_right_recall": 0.7274881516587678,
  "turn_straight_recall": 0.5717255717255717,
  "turn_left_recall": 0.7065803667745415,
  "recall_turn": [
    0.7274881516587678,
    0.5717255717255717,
    0.7065803667745415
  ],
  "cm_turn": [
    [
      614,
      192,
      38
    ],
    [
      426,
      1100,
      398
    ],
    [
      94,
      178,
      655
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      629,
      0,
      28
    ],
    [
      0,
      24,
      18
    ],
    [
      124,
      6,
      2866
    ]
  ],
  "main_confidence_mean": 0.9700020769976586,
  "main_confidence_error_mean": 0.7529221284666631,
  "main_low_conf_0p60_ratio": 0.04925575101488498,
  "main_low_conf_0p70_ratio": 0.05602165087956698,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 182,
      "error_rate": 0.46153846153846156,
      "mean_confidence": 0.5449193071183375
    },
    {
      "bin": "[0.60,0.70)",
      "n": 25,
      "error_rate": 0.32,
      "mean_confidence": 0.6551848191921233
    },
    {
      "bin": "[0.70,0.80)",
      "n": 30,
      "error_rate": 0.23333333333333334,
      "mean_confidence": 0.7583395940147447
    },
    {
      "bin": "[0.80,0.90)",
      "n": 33,
      "error_rate": 0.09090909090909091,
      "mean_confidence": 0.856249197985125
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3425,
      "error_rate": 0.021605839416058394,
      "mean_confidence": 0.9978383441684836
    }
  ],
  "turn_confidence_mean": 0.8461841221739774,
  "turn_confidence_error_mean": 0.7701421744822732,
  "turn_low_conf_0p60_ratio": 0.15209742895805142,
  "turn_low_conf_0p70_ratio": 0.24167794316644114,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 562,
      "error_rate": 0.6192170818505338,
      "mean_confidence": 0.530946990658392
    },
    {
      "bin": "[0.60,0.70)",
      "n": 331,
      "error_rate": 0.5468277945619335,
      "mean_confidence": 0.6518018452015437
    },
    {
      "bin": "[0.70,0.80)",
      "n": 326,
      "error_rate": 0.44785276073619634,
      "mean_confidence": 0.7501649289378203
    },
    {
      "bin": "[0.80,0.90)",
      "n": 441,
      "error_rate": 0.40589569160997735,
      "mean_confidence": 0.8540786844047228
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2035,
      "error_rate": 0.23194103194103194,
      "mean_confidence": 0.978530341653517
    }
  ],
  "theta_mae_rad": 0.014709187671542168,
  "theta_mae_deg": 0.8427743315696716,
  "uphill_recall": 0.7876010781671159,
  "downhill_recall": 0.7969966629588432,
  "slope_sign_acc": 0.9655078018067342,
  "theta_flat_mae_deg": 1.1811892986297607,
  "theta_flat_abs_p95_deg": 3.5293707847595215,
  "theta_flat_abs_max_deg": 7.869700908660889,
  "theta_flat_bias_deg": 0.19468212127685547,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.638199806213379,
  "theta_near_flat_abs_p95_deg": 4.717684268951416,
  "theta_near_flat_abs_max_deg": 7.869700908660889,
  "theta_near_flat_bias_deg": 0.6144925951957703,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.4473284482955933,
  "theta_flat_turn_abs_p95_deg": 5.190623760223389,
  "theta_flat_turn_abs_max_deg": 7.869700908660889,
  "theta_flat_turn_bias_deg": 0.23564893007278442,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8427743315696716,
  "theta_slope_control_abs_p95_deg": 9.167709350585938,
  "theta_slope_control_abs_max_deg": 12.409180641174316,
  "theta_slope_control_bias_deg": 0.3915330171585083,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8427743911743164,
  "theta_all_rmse_deg": 1.2821165323257446,
  "theta_all_p95_abs_err_deg": 2.7243003845214844,
  "theta_all_max_abs_err_deg": 8.36970043182373,
  "theta_all_bias_deg": 0.3915330171585083,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7685624957084656,
  "theta_active_abs_ge_2_rmse_deg": 1.1715441942214966,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.4948463439941406,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.283936977386475,
  "theta_active_abs_ge_2_bias_deg": 0.43470093607902527,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8771870732307434,
  "theta_abs_le_8_rmse_deg": 1.3323832750320435,
  "theta_abs_le_8_p95_abs_err_deg": 2.80564284324646,
  "theta_abs_le_8_max_abs_err_deg": 8.36970043182373,
  "theta_abs_le_8_bias_deg": 0.3963255286216736,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8427743911743164,
  "theta_abs_le_10_rmse_deg": 1.2821165323257446,
  "theta_abs_le_10_p95_abs_err_deg": 2.7243003845214844,
  "theta_abs_le_10_max_abs_err_deg": 8.36970043182373,
  "theta_abs_le_10_bias_deg": 0.3915330171585083,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5477190613746643,
  "theta_pos_8_10_rmse_deg": 0.7378095984458923,
  "theta_pos_8_10_p95_abs_err_deg": 1.3698073625564575,
  "theta_pos_8_10_max_abs_err_deg": 3.909181833267212,
  "theta_pos_8_10_bias_deg": -0.00046133488649502397,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8500761985778809,
  "theta_neg_10_8_rmse_deg": 1.2821377515792847,
  "theta_neg_10_8_p95_abs_err_deg": 2.073113203048706,
  "theta_neg_10_8_max_abs_err_deg": 7.283936977386475,
  "theta_neg_10_8_bias_deg": 0.749521017074585,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6584741473197937,
  "theta_pos_6_8_rmse_deg": 0.97640061378479,
  "theta_pos_6_8_p95_abs_err_deg": 1.561320424079895,
  "theta_pos_6_8_max_abs_err_deg": 4.675330638885498,
  "theta_pos_6_8_bias_deg": 0.22710038721561432,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8099900484085083,
  "theta_neg_8_6_rmse_deg": 1.2211008071899414,
  "theta_neg_8_6_p95_abs_err_deg": 2.4259045124053955,
  "theta_neg_8_6_max_abs_err_deg": 6.304941177368164,
  "theta_neg_8_6_bias_deg": 0.6260374188423157,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6352514624595642,
  "theta_neg_4_2_rmse_deg": 0.9536522030830383,
  "theta_neg_4_2_p95_abs_err_deg": 2.0833334922790527,
  "theta_neg_4_2_max_abs_err_deg": 6.061767578125,
  "theta_neg_4_2_bias_deg": 0.3106369078159332,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6453695297241211,
  "theta_neg_2_0p5_rmse_deg": 0.8585798740386963,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.84369695186615,
  "theta_neg_2_0p5_max_abs_err_deg": 3.231757640838623,
  "theta_neg_2_0p5_bias_deg": -0.4875093996524811,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1734068393707275,
  "theta_pos_0p5_2_rmse_deg": 1.4252047538757324,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.363433599472046,
  "theta_pos_0p5_2_max_abs_err_deg": 5.359801292419434,
  "theta_pos_0p5_2_bias_deg": 0.4975731372833252,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3104185901652815,
  "loss_turn": 1.2385022166617345,
  "loss_theta": 0.000500688466973759,
  "loss_main_bundle_base": 0.3104185901652815,
  "loss_turn_bundle_base": 0.29724052888372754,
  "loss_theta_bundle_base": 0.0003472669693847415,
  "loss_main_bundle": 0.3104185901652815,
  "loss_turn_bundle": 0.29724052888372754,
  "loss_theta_bundle": 0.0003472669693847415,
  "loss_theta_flat": 0.00038456419251335557,
  "loss_theta_near_flat": 0.00137733124260802,
  "loss_theta_error_excess": 0.0001998932924482679,
  "loss_theta_flat_excess": 0.00016065174653746007,
  "loss_theta_near_flat_excess": 0.0009587266445235527,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00015745933953085372,
  "loss_theta_small_neg": 0.0002683146807221136,
  "loss_theta_small_neg_excess": 7.580118761273449e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3782664325305025,
  "loss_false_turn_straight": 0.30926729731856567,
  "loss_transition_focal_raw": 1.0195170549643056,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.174033238901455,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
