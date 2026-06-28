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
| acc_main | 0.9600 |
| acc_turn | 0.5067 |
| acc_turn_pure | 0.5193 |
| acc_turn_transition | 0.4516 |
| main_confidence_mean | 0.9817 |
| main_low_conf_0p60_ratio | 0.0081 |
| main_low_conf_0p70_ratio | 0.0164 |
| turn_confidence_mean | 0.7019 |
| turn_low_conf_0p60_ratio | 0.3570 |
| turn_low_conf_0p70_ratio | 0.5258 |
| turn_right_recall | 0.5432 |
| turn_straight_recall | 0.4459 |
| turn_left_recall | 0.6080 |
| theta_mae_deg | 0.8770 |
| theta_abs_le_10_p95_abs_err_deg | 2.4224 |
| theta_neg_10_8_p95_abs_err_deg | 2.3571 |
| theta_pos_8_10_p95_abs_err_deg | 2.4369 |
| theta_abs_le_8_p95_abs_err_deg | 2.4229 |
| theta_neg_8_6_p95_abs_err_deg | 2.2145 |
| theta_pos_6_8_p95_abs_err_deg | 1.8887 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.4632 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.5134 |
| theta_flat_abs_p95_deg | 2.9389 |
| theta_flat_bias_deg | -0.1610 |
| theta_near_flat_abs_p95_deg | 2.1454 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.0426 |
| theta_flat_turn_abs_p95_deg | 2.1346 |
| flat_recall | 0.9339 |
| stall_recall | 0.6875 |
| slope_recall | 0.9767 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7506 |
| downhill_recall | 0.8099 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    706,
    0,
    50
  ],
  [
    10,
    66,
    20
  ],
  [
    51,
    13,
    2686
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    434,
    158,
    207
  ],
  [
    420,
    862,
    651
  ],
  [
    136,
    205,
    529
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.297511 |
| test_loss_turn_bundle_base | 0.225435 |
| test_loss_theta_bundle_base | 0.000308 |
| test_loss_transition_focal_raw | 0.859605 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.010035 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 28
- train_seconds: 178.6

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 29 | 0.4138 | 0.5416 |
| [0.60,0.70) | 30 | 0.3667 | 0.6600 |
| [0.70,0.80) | 47 | 0.2553 | 0.7533 |
| [0.80,0.90) | 108 | 0.2870 | 0.8548 |
| [0.90,1.00) | 3388 | 0.0230 | 0.9955 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1286 | 0.6267 | 0.5094 |
| [0.60,0.70) | 608 | 0.5214 | 0.6509 |
| [0.70,0.80) | 561 | 0.4866 | 0.7481 |
| [0.80,0.90) | 431 | 0.4664 | 0.8538 |
| [0.90,1.00) | 716 | 0.2514 | 0.9635 |


## 验证集最佳点

```json
{
  "loss_total": 0.49238963980474715,
  "acc_main": 0.9493910690121786,
  "acc_turn": 0.5431664411366712,
  "acc_turn_pure": 0.5585054080629301,
  "acc_turn_transition": 0.4704968944099379,
  "false_turn_straight": 0.6148648648648649,
  "flat_recall": 0.958904109589041,
  "stall_recall": 0.5238095238095238,
  "slope_recall": 0.9532710280373832,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.958904109589041,
    0.5238095238095238,
    0.9532710280373832
  ],
  "turn_right_recall": 0.6670616113744076,
  "turn_straight_recall": 0.38513513513513514,
  "turn_left_recall": 0.7583603020496225,
  "recall_turn": [
    0.6670616113744076,
    0.38513513513513514,
    0.7583603020496225
  ],
  "cm_turn": [
    [
      563,
      163,
      118
    ],
    [
      551,
      741,
      632
    ],
    [
      127,
      97,
      703
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      630,
      0,
      27
    ],
    [
      0,
      22,
      20
    ],
    [
      127,
      13,
      2856
    ]
  ],
  "main_confidence_mean": 0.9726233531134557,
  "main_confidence_error_mean": 0.8237493298773557,
  "main_low_conf_0p60_ratio": 0.005412719891745603,
  "main_low_conf_0p70_ratio": 0.014073071718538565,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 20,
      "error_rate": 0.4,
      "mean_confidence": 0.5448218489156256
    },
    {
      "bin": "[0.60,0.70)",
      "n": 32,
      "error_rate": 0.28125,
      "mean_confidence": 0.6565532277201671
    },
    {
      "bin": "[0.70,0.80)",
      "n": 222,
      "error_rate": 0.3963963963963964,
      "mean_confidence": 0.7272622964631409
    },
    {
      "bin": "[0.80,0.90)",
      "n": 63,
      "error_rate": 0.1111111111111111,
      "mean_confidence": 0.857971680582179
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3358,
      "error_rate": 0.022334723049434187,
      "mean_confidence": 0.996555301905112
    }
  ],
  "turn_confidence_mean": 0.7191770847526866,
  "turn_confidence_error_mean": 0.6590449654407153,
  "turn_low_conf_0p60_ratio": 0.310148849797023,
  "turn_low_conf_0p70_ratio": 0.46062246278755076,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 1146,
      "error_rate": 0.6178010471204188,
      "mean_confidence": 0.49357040416665043
    },
    {
      "bin": "[0.60,0.70)",
      "n": 556,
      "error_rate": 0.49640287769784175,
      "mean_confidence": 0.6502912069905733
    },
    {
      "bin": "[0.70,0.80)",
      "n": 532,
      "error_rate": 0.4830827067669173,
      "mean_confidence": 0.7495424863924318
    },
    {
      "bin": "[0.80,0.90)",
      "n": 625,
      "error_rate": 0.424,
      "mean_confidence": 0.8481306053652865
    },
    {
      "bin": "[0.90,1.00)",
      "n": 836,
      "error_rate": 0.21770334928229665,
      "mean_confidence": 0.9585257210351185
    }
  ],
  "theta_mae_rad": 0.016068575903773308,
  "theta_mae_deg": 0.9206615090370178,
  "uphill_recall": 0.7784366576819407,
  "downhill_recall": 0.800333704115684,
  "slope_sign_acc": 0.9657815494114427,
  "theta_flat_mae_deg": 0.9817617535591125,
  "theta_flat_abs_p95_deg": 2.9362242221832275,
  "theta_flat_abs_max_deg": 7.652701377868652,
  "theta_flat_bias_deg": 0.4748925268650055,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4838207960128784,
  "theta_near_flat_abs_p95_deg": 3.940945625305176,
  "theta_near_flat_abs_max_deg": 7.652701377868652,
  "theta_near_flat_bias_deg": 0.9061967134475708,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.3302232027053833,
  "theta_flat_turn_abs_p95_deg": 4.351861000061035,
  "theta_flat_turn_abs_max_deg": 7.652701377868652,
  "theta_flat_turn_bias_deg": 0.7559999227523804,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9206615090370178,
  "theta_slope_control_abs_p95_deg": 8.886478424072266,
  "theta_slope_control_abs_max_deg": 12.146660804748535,
  "theta_slope_control_bias_deg": 0.2046366035938263,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.920661449432373,
  "theta_all_rmse_deg": 1.2830806970596313,
  "theta_all_p95_abs_err_deg": 2.6584885120391846,
  "theta_all_max_abs_err_deg": 8.152701377868652,
  "theta_all_bias_deg": 0.2046365886926651,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.9072626829147339,
  "theta_active_abs_ge_2_rmse_deg": 1.2350208759307861,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.6191093921661377,
  "theta_active_abs_ge_2_max_abs_err_deg": 8.089914321899414,
  "theta_active_abs_ge_2_bias_deg": 0.14537154138088226,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9216331839561462,
  "theta_abs_le_8_rmse_deg": 1.2851085662841797,
  "theta_abs_le_8_p95_abs_err_deg": 2.730815887451172,
  "theta_abs_le_8_max_abs_err_deg": 8.152701377868652,
  "theta_abs_le_8_bias_deg": 0.25025033950805664,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.920661449432373,
  "theta_abs_le_10_rmse_deg": 1.2830806970596313,
  "theta_abs_le_10_p95_abs_err_deg": 2.6584885120391846,
  "theta_abs_le_10_max_abs_err_deg": 8.152701377868652,
  "theta_abs_le_10_bias_deg": 0.2046365886926651,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.951952338218689,
  "theta_pos_8_10_rmse_deg": 1.1244577169418335,
  "theta_pos_8_10_p95_abs_err_deg": 2.0017824172973633,
  "theta_pos_8_10_max_abs_err_deg": 5.13089656829834,
  "theta_pos_8_10_bias_deg": -0.6246781349182129,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8805606961250305,
  "theta_neg_10_8_rmse_deg": 1.4108402729034424,
  "theta_neg_10_8_p95_abs_err_deg": 2.866194009780884,
  "theta_neg_10_8_max_abs_err_deg": 7.418032646179199,
  "theta_neg_10_8_bias_deg": 0.6601141691207886,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.8821802735328674,
  "theta_pos_6_8_rmse_deg": 1.109881043434143,
  "theta_pos_6_8_p95_abs_err_deg": 2.1527490615844727,
  "theta_pos_6_8_max_abs_err_deg": 3.9207510948181152,
  "theta_pos_6_8_bias_deg": -0.46738749742507935,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8311527371406555,
  "theta_neg_8_6_rmse_deg": 1.1756669282913208,
  "theta_neg_8_6_p95_abs_err_deg": 2.173978328704834,
  "theta_neg_8_6_max_abs_err_deg": 8.089914321899414,
  "theta_neg_8_6_bias_deg": 0.41156497597694397,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.9181149005889893,
  "theta_neg_4_2_rmse_deg": 1.2258708477020264,
  "theta_neg_4_2_p95_abs_err_deg": 2.3693602085113525,
  "theta_neg_4_2_max_abs_err_deg": 7.675380229949951,
  "theta_neg_4_2_bias_deg": 0.37238243222236633,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.46250811219215393,
  "theta_neg_2_0p5_rmse_deg": 0.7287002801895142,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.129244089126587,
  "theta_neg_2_0p5_max_abs_err_deg": 5.458404064178467,
  "theta_neg_2_0p5_bias_deg": 0.09031496942043304,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.8384695053100586,
  "theta_pos_0p5_2_rmse_deg": 1.0792484283447266,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.741075038909912,
  "theta_pos_0p5_2_max_abs_err_deg": 5.326474189758301,
  "theta_pos_0p5_2_bias_deg": 0.35792276263237,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2779965083073215,
  "loss_turn": 1.0702497583926127,
  "loss_theta": 0.0005017225824501894,
  "loss_main_bundle_base": 0.2779965083073215,
  "loss_turn_bundle_base": 0.21404995743250815,
  "loss_theta_bundle_base": 0.00034316919603969787,
  "loss_main_bundle": 0.2779965083073215,
  "loss_turn_bundle": 0.21404995743250815,
  "loss_theta_bundle": 0.00034316919603969787,
  "loss_theta_flat": 0.0003695905042077504,
  "loss_theta_near_flat": 0.0011681662969472686,
  "loss_theta_error_excess": 0.00017051445737705442,
  "loss_theta_flat_excess": 0.00016891447845060334,
  "loss_theta_near_flat_excess": 0.0008037898144924179,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00014345187592069354,
  "loss_theta_small_neg": 0.0004539421857530012,
  "loss_theta_small_neg_excess": 0.00012395918029597556,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.5209774640480784,
  "loss_false_turn_straight": 0.393602906584901,
  "loss_transition_focal_raw": 0.6958221140507916,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.4407826226966107,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
