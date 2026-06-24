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
  "lambda_theta_flat": 0.16,
  "theta_flat_loss_mode": "near_zero",
  "theta_flat_zero_tol_deg": 0.3,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 0.05,
  "lambda_theta_flat_excess": 0.06,
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
  "main_neg_slope_weight": 2.4,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 3.0,
  "select_turn_weight": 0.55,
  "select_turn_transition_weight": 1.2,
  "select_turn_transition_target": 0.82,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.88,
  "select_turn_lr_weight": 0.6,
  "select_turn_lr_target": 0.88,
  "select_stall_weight": 0.25,
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
  "select_theta_flat_peak_weight": 1.1,
  "select_theta_flat_peak_target_deg": 5.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 1.1,
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
| acc_main | 0.9575 |
| acc_turn | 0.5689 |
| acc_turn_pure | 0.5824 |
| acc_turn_transition | 0.5097 |
| main_confidence_mean | 0.9844 |
| main_low_conf_0p60_ratio | 0.0103 |
| main_low_conf_0p70_ratio | 0.0189 |
| turn_confidence_mean | 0.7961 |
| turn_low_conf_0p60_ratio | 0.1999 |
| turn_low_conf_0p70_ratio | 0.3287 |
| turn_right_recall | 0.6133 |
| turn_straight_recall | 0.5711 |
| turn_left_recall | 0.5230 |
| theta_mae_deg | 0.7941 |
| theta_abs_le_10_p95_abs_err_deg | 2.0926 |
| theta_neg_10_8_p95_abs_err_deg | 1.7431 |
| theta_pos_8_10_p95_abs_err_deg | 2.9904 |
| theta_abs_le_8_p95_abs_err_deg | 1.9974 |
| theta_neg_8_6_p95_abs_err_deg | 1.6789 |
| theta_pos_6_8_p95_abs_err_deg | 2.4307 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.0265 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.7097 |
| theta_flat_abs_p95_deg | 2.7006 |
| theta_flat_bias_deg | -0.1946 |
| theta_near_flat_abs_p95_deg | 1.7169 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1811 |
| theta_flat_turn_abs_p95_deg | 1.7606 |
| flat_recall | 0.9497 |
| stall_recall | 0.6562 |
| slope_recall | 0.9702 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1146 |
| uphill_recall | 0.7420 |
| downhill_recall | 0.8014 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    718,
    0,
    38
  ],
  [
    11,
    63,
    22
  ],
  [
    68,
    14,
    2668
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    490,
    196,
    113
  ],
  [
    371,
    1104,
    458
  ],
  [
    176,
    239,
    455
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.328752 |
| test_loss_turn_bundle_base | 0.360203 |
| test_loss_theta_bundle_base | 0.000240 |
| test_loss_transition_focal_raw | 1.209551 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.684011 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 54
- train_seconds: 284.4

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 37 | 0.4054 | 0.5548 |
| [0.60,0.70) | 31 | 0.4194 | 0.6499 |
| [0.70,0.80) | 37 | 0.3514 | 0.7553 |
| [0.80,0.90) | 52 | 0.2308 | 0.8495 |
| [0.90,1.00) | 3445 | 0.0290 | 0.9966 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 720 | 0.5819 | 0.5169 |
| [0.60,0.70) | 464 | 0.5496 | 0.6474 |
| [0.70,0.80) | 458 | 0.5371 | 0.7524 |
| [0.80,0.90) | 493 | 0.4868 | 0.8533 |
| [0.90,1.00) | 1467 | 0.2679 | 0.9746 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.5097
- theta_mae_deg <= 0.7000 未满足，实际 0.7941

## 验证集最佳点

```json
{
  "loss_total": 0.5862089208078965,
  "acc_main": 0.9366711772665764,
  "acc_turn": 0.6311231393775372,
  "acc_turn_pure": 0.6430678466076696,
  "acc_turn_transition": 0.5745341614906833,
  "false_turn_straight": 0.41476091476091476,
  "flat_recall": 0.832572298325723,
  "stall_recall": 0.38095238095238093,
  "slope_recall": 0.9672897196261683,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.832572298325723,
    0.38095238095238093,
    0.9672897196261683
  ],
  "turn_right_recall": 0.6386255924170616,
  "turn_straight_recall": 0.5852390852390852,
  "turn_left_recall": 0.7195253505933118,
  "recall_turn": [
    0.6386255924170616,
    0.5852390852390852,
    0.7195253505933118
  ],
  "cm_turn": [
    [
      539,
      217,
      88
    ],
    [
      373,
      1126,
      425
    ],
    [
      76,
      184,
      667
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      547,
      0,
      110
    ],
    [
      0,
      16,
      26
    ],
    [
      87,
      11,
      2898
    ]
  ],
  "main_confidence_mean": 0.9651875435676873,
  "main_confidence_error_mean": 0.744361399270459,
  "main_low_conf_0p60_ratio": 0.05142083897158322,
  "main_low_conf_0p70_ratio": 0.05953991880920163,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 190,
      "error_rate": 0.5368421052631579,
      "mean_confidence": 0.5086821873344851
    },
    {
      "bin": "[0.60,0.70)",
      "n": 30,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.6608227278306346
    },
    {
      "bin": "[0.70,0.80)",
      "n": 30,
      "error_rate": 0.3,
      "mean_confidence": 0.7532454830222051
    },
    {
      "bin": "[0.80,0.90)",
      "n": 51,
      "error_rate": 0.27450980392156865,
      "mean_confidence": 0.849006819150233
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3394,
      "error_rate": 0.029169121979964643,
      "mean_confidence": 0.9970527294598719
    }
  ],
  "turn_confidence_mean": 0.8274289645139331,
  "turn_confidence_error_mean": 0.7582969959846182,
  "turn_low_conf_0p60_ratio": 0.16400541271989175,
  "turn_low_conf_0p70_ratio": 0.26305818673883624,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 606,
      "error_rate": 0.6023102310231023,
      "mean_confidence": 0.5281260614295508
    },
    {
      "bin": "[0.60,0.70)",
      "n": 366,
      "error_rate": 0.4890710382513661,
      "mean_confidence": 0.6472789006543677
    },
    {
      "bin": "[0.70,0.80)",
      "n": 411,
      "error_rate": 0.5036496350364964,
      "mean_confidence": 0.7502339470066665
    },
    {
      "bin": "[0.80,0.90)",
      "n": 529,
      "error_rate": 0.3497164461247637,
      "mean_confidence": 0.8524085940735269
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1783,
      "error_rate": 0.23948401570386987,
      "mean_confidence": 0.976517809606585
    }
  ],
  "theta_mae_rad": 0.01750955544412136,
  "theta_mae_deg": 1.0032235383987427,
  "uphill_recall": 0.8436657681940701,
  "downhill_recall": 0.8025583982202447,
  "slope_sign_acc": 0.9611278401313988,
  "theta_flat_mae_deg": 1.175189733505249,
  "theta_flat_abs_p95_deg": 3.782163143157959,
  "theta_flat_abs_max_deg": 6.740325927734375,
  "theta_flat_bias_deg": 0.6706939339637756,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4017493724822998,
  "theta_near_flat_abs_p95_deg": 3.782212734222412,
  "theta_near_flat_abs_max_deg": 6.740325927734375,
  "theta_near_flat_bias_deg": 0.7720889449119568,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1457107067108154,
  "theta_flat_turn_abs_p95_deg": 3.782163143157959,
  "theta_flat_turn_abs_max_deg": 6.740325927734375,
  "theta_flat_turn_bias_deg": 0.2551007866859436,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 1.0032235383987427,
  "theta_slope_control_abs_p95_deg": 9.619462013244629,
  "theta_slope_control_abs_max_deg": 12.797467231750488,
  "theta_slope_control_bias_deg": -0.23256541788578033,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 1.0032235383987427,
  "theta_all_rmse_deg": 1.3650386333465576,
  "theta_all_p95_abs_err_deg": 2.649092435836792,
  "theta_all_max_abs_err_deg": 7.240326404571533,
  "theta_all_bias_deg": -0.23256541788578033,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.9655126333236694,
  "theta_active_abs_ge_2_rmse_deg": 1.2916351556777954,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.383466958999634,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.101848602294922,
  "theta_active_abs_ge_2_bias_deg": -0.43064332008361816,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 1.0182048082351685,
  "theta_abs_le_8_rmse_deg": 1.3895823955535889,
  "theta_abs_le_8_p95_abs_err_deg": 2.7781074047088623,
  "theta_abs_le_8_max_abs_err_deg": 7.240326404571533,
  "theta_abs_le_8_bias_deg": -0.15050958096981049,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 1.0032235383987427,
  "theta_abs_le_10_rmse_deg": 1.3650386333465576,
  "theta_abs_le_10_p95_abs_err_deg": 2.649092435836792,
  "theta_abs_le_10_max_abs_err_deg": 7.240326404571533,
  "theta_abs_le_10_bias_deg": -0.23256541788578033,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.9481033682823181,
  "theta_pos_8_10_rmse_deg": 1.1180847883224487,
  "theta_pos_8_10_p95_abs_err_deg": 1.8481426239013672,
  "theta_pos_8_10_max_abs_err_deg": 5.8141865730285645,
  "theta_pos_8_10_bias_deg": -0.76134192943573,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.9318047165870667,
  "theta_neg_10_8_rmse_deg": 1.3826768398284912,
  "theta_neg_10_8_p95_abs_err_deg": 2.567734479904175,
  "theta_neg_10_8_max_abs_err_deg": 6.582688331604004,
  "theta_neg_10_8_bias_deg": -0.39294806122779846,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 1.0020731687545776,
  "theta_pos_6_8_rmse_deg": 1.149816870689392,
  "theta_pos_6_8_p95_abs_err_deg": 2.0544657707214355,
  "theta_pos_6_8_max_abs_err_deg": 3.8082144260406494,
  "theta_pos_6_8_bias_deg": -0.7412344813346863,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.066431999206543,
  "theta_neg_8_6_rmse_deg": 1.451871395111084,
  "theta_neg_8_6_p95_abs_err_deg": 2.672025680541992,
  "theta_neg_8_6_max_abs_err_deg": 6.8948588371276855,
  "theta_neg_8_6_bias_deg": -0.648120105266571,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.779459536075592,
  "theta_neg_4_2_rmse_deg": 1.1450860500335693,
  "theta_neg_4_2_p95_abs_err_deg": 2.3299355506896973,
  "theta_neg_4_2_max_abs_err_deg": 5.522965431213379,
  "theta_neg_4_2_bias_deg": -0.2432691603899002,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.7906374335289001,
  "theta_neg_2_0p5_rmse_deg": 1.0766422748565674,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.1012604236602783,
  "theta_neg_2_0p5_max_abs_err_deg": 4.363604545593262,
  "theta_neg_2_0p5_bias_deg": 0.6058448553085327,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.4158742427825928,
  "theta_pos_0p5_2_rmse_deg": 1.665977120399475,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.5288825035095215,
  "theta_pos_0p5_2_max_abs_err_deg": 3.9770188331604004,
  "theta_pos_0p5_2_bias_deg": 0.8376150131225586,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.27349838160371587,
  "loss_turn": 1.301336848590629,
  "loss_theta": 0.0005674441667974338,
  "loss_main_bundle_base": 0.27349838160371587,
  "loss_turn_bundle_base": 0.31232083774548586,
  "loss_theta_bundle_base": 0.00038969919390482413,
  "loss_main_bundle": 0.27349838160371587,
  "loss_turn_bundle": 0.31232083774548586,
  "loss_theta_bundle": 0.00038969919390482413,
  "loss_theta_flat": 0.000267589972529331,
  "loss_theta_near_flat": 0.0012313427082206222,
  "loss_theta_error_excess": 0.00019485859267466546,
  "loss_theta_flat_excess": 0.00014972355181218347,
  "loss_theta_near_flat_excess": 0.0008768791404044878,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.0001606415640457227,
  "loss_theta_small_neg": 0.0003976915769231114,
  "loss_theta_small_neg_excess": 0.00013654977170635815,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.366018861903228,
  "loss_false_turn_straight": 0.2990112715144925,
  "loss_transition_focal_raw": 1.0472694229208568,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.2182334618574875,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
