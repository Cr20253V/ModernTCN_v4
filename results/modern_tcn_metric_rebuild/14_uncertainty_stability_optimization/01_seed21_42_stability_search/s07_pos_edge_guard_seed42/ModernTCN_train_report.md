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
  "lambda_theta": 0.58,
  "lambda_theta_flat": 0.12,
  "theta_flat_loss_mode": "near_zero",
  "theta_flat_zero_tol_deg": 0.3,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 0.08,
  "lambda_theta_flat_excess": 0.0,
  "lambda_theta_near_flat_excess": 0.0,
  "lambda_theta_true_zero_excess": 0.1,
  "lambda_theta_active_excess": 0.04,
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
  "theta_neg_weight": 1.15,
  "theta_pos_weight": 1.5,
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
  "select_theta_flat_peak_weight": 0.9,
  "select_theta_flat_peak_target_deg": 5.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 1.6,
  "select_theta_edge_p95_target_deg": 1.1,
  "select_theta_small_nonzero_p95_weight": 0.8,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.3,
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9584 |
| acc_turn | 0.4789 |
| acc_turn_pure | 0.4930 |
| acc_turn_transition | 0.4173 |
| main_confidence_mean | 0.9725 |
| main_low_conf_0p60_ratio | 0.0175 |
| main_low_conf_0p70_ratio | 0.0289 |
| turn_confidence_mean | 0.6685 |
| turn_low_conf_0p60_ratio | 0.4203 |
| turn_low_conf_0p70_ratio | 0.5974 |
| turn_right_recall | 0.5782 |
| turn_straight_recall | 0.4144 |
| turn_left_recall | 0.5310 |
| theta_mae_deg | 0.9524 |
| theta_abs_le_10_p95_abs_err_deg | 2.5681 |
| theta_neg_10_8_p95_abs_err_deg | 1.8307 |
| theta_pos_8_10_p95_abs_err_deg | 3.3334 |
| theta_abs_le_8_p95_abs_err_deg | 2.5377 |
| theta_neg_8_6_p95_abs_err_deg | 2.2995 |
| theta_pos_6_8_p95_abs_err_deg | 2.2765 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.7725 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.6950 |
| theta_flat_abs_p95_deg | 3.6431 |
| theta_flat_bias_deg | -0.8070 |
| theta_near_flat_abs_p95_deg | 3.2679 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -1.1291 |
| theta_flat_turn_abs_p95_deg | 2.9912 |
| flat_recall | 0.9497 |
| stall_recall | 0.6250 |
| slope_recall | 0.9724 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1146 |
| uphill_recall | 0.7460 |
| downhill_recall | 0.8008 |

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
    60,
    25
  ],
  [
    64,
    12,
    2674
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    462,
    171,
    166
  ],
  [
    595,
    801,
    537
  ],
  [
    218,
    190,
    462
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.268405 |
| test_loss_turn_bundle_base | 0.216626 |
| test_loss_theta_bundle_base | 0.000436 |
| test_loss_transition_focal_raw | 0.699632 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 2.766296 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 20
- train_seconds: 161.6

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 63 | 0.4127 | 0.5442 |
| [0.60,0.70) | 41 | 0.5122 | 0.6454 |
| [0.70,0.80) | 127 | 0.2126 | 0.7598 |
| [0.80,0.90) | 67 | 0.2687 | 0.8514 |
| [0.90,1.00) | 3304 | 0.0176 | 0.9954 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1514 | 0.6347 | 0.4967 |
| [0.60,0.70) | 638 | 0.5486 | 0.6474 |
| [0.70,0.80) | 482 | 0.5166 | 0.7506 |
| [0.80,0.90) | 433 | 0.4781 | 0.8432 |
| [0.90,1.00) | 535 | 0.2056 | 0.9642 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.4173
- theta_mae_deg <= 0.7000 未满足，实际 0.9524

## 验证集最佳点

```json
{
  "loss_total": 0.4450426782096997,
  "acc_main": 0.9410013531799729,
  "acc_turn": 0.5225981055480379,
  "acc_turn_pure": 0.5355621107833497,
  "acc_turn_transition": 0.4611801242236025,
  "false_turn_straight": 0.5940748440748441,
  "flat_recall": 0.9497716894977168,
  "stall_recall": 0.4523809523809524,
  "slope_recall": 0.9459279038718291,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.023809523809523808,
  "recall_main": [
    0.9497716894977168,
    0.4523809523809524,
    0.9459279038718291
  ],
  "turn_right_recall": 0.6421800947867299,
  "turn_straight_recall": 0.40592515592515593,
  "turn_left_recall": 0.6558791801510249,
  "recall_turn": [
    0.6421800947867299,
    0.40592515592515593,
    0.6558791801510249
  ],
  "cm_turn": [
    [
      542,
      172,
      130
    ],
    [
      587,
      781,
      556
    ],
    [
      167,
      152,
      608
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      624,
      0,
      33
    ],
    [
      1,
      19,
      22
    ],
    [
      153,
      9,
      2834
    ]
  ],
  "main_confidence_mean": 0.9599732384094094,
  "main_confidence_error_mean": 0.7383927712821168,
  "main_low_conf_0p60_ratio": 0.05196211096075778,
  "main_low_conf_0p70_ratio": 0.06062246278755074,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 192,
      "error_rate": 0.4583333333333333,
      "mean_confidence": 0.5139818606784476
    },
    {
      "bin": "[0.60,0.70)",
      "n": 32,
      "error_rate": 0.40625,
      "mean_confidence": 0.651140563354845
    },
    {
      "bin": "[0.70,0.80)",
      "n": 60,
      "error_rate": 0.36666666666666664,
      "mean_confidence": 0.7565135224941264
    },
    {
      "bin": "[0.80,0.90)",
      "n": 77,
      "error_rate": 0.19480519480519481,
      "mean_confidence": 0.8558240234370382
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3334,
      "error_rate": 0.02399520095980804,
      "mean_confidence": 0.9946883141844186
    }
  ],
  "turn_confidence_mean": 0.6858937718952169,
  "turn_confidence_error_mean": 0.6336810989089366,
  "turn_low_conf_0p60_ratio": 0.40108254397834914,
  "turn_low_conf_0p70_ratio": 0.5299052774018944,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 1482,
      "error_rate": 0.581646423751687,
      "mean_confidence": 0.4917120762560773
    },
    {
      "bin": "[0.60,0.70)",
      "n": 476,
      "error_rate": 0.5105042016806722,
      "mean_confidence": 0.6490743575862893
    },
    {
      "bin": "[0.70,0.80)",
      "n": 530,
      "error_rate": 0.5509433962264151,
      "mean_confidence": 0.7547505365597814
    },
    {
      "bin": "[0.80,0.90)",
      "n": 549,
      "error_rate": 0.47176684881602915,
      "mean_confidence": 0.845542889808268
    },
    {
      "bin": "[0.90,1.00)",
      "n": 658,
      "error_rate": 0.1641337386018237,
      "mean_confidence": 0.9612157523538347
    }
  ],
  "theta_mae_rad": 0.018590547144412994,
  "theta_mae_deg": 1.065159797668457,
  "uphill_recall": 0.7660377358490567,
  "downhill_recall": 0.8042269187986651,
  "slope_sign_acc": 0.9479879551053928,
  "theta_flat_mae_deg": 1.4249204397201538,
  "theta_flat_abs_p95_deg": 3.5585055351257324,
  "theta_flat_abs_max_deg": 5.376006603240967,
  "theta_flat_bias_deg": -0.09934639930725098,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.7513649463653564,
  "theta_near_flat_abs_p95_deg": 3.622227191925049,
  "theta_near_flat_abs_max_deg": 5.376006603240967,
  "theta_near_flat_bias_deg": 0.06497722864151001,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.6643095016479492,
  "theta_flat_turn_abs_p95_deg": 3.6043975353240967,
  "theta_flat_turn_abs_max_deg": 5.376006603240967,
  "theta_flat_turn_bias_deg": -0.41688650846481323,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 1.065159797668457,
  "theta_slope_control_abs_p95_deg": 9.254035949707031,
  "theta_slope_control_abs_max_deg": 11.824572563171387,
  "theta_slope_control_bias_deg": -0.20194195210933685,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 1.065159797668457,
  "theta_all_rmse_deg": 1.4318710565567017,
  "theta_all_p95_abs_err_deg": 2.828537940979004,
  "theta_all_max_abs_err_deg": 9.018074035644531,
  "theta_all_bias_deg": -0.20194195210933685,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.9862670302391052,
  "theta_active_abs_ge_2_rmse_deg": 1.3412113189697266,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.604607582092285,
  "theta_active_abs_ge_2_max_abs_err_deg": 9.018074035644531,
  "theta_active_abs_ge_2_bias_deg": -0.22444038093090057,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 1.0689254999160767,
  "theta_abs_le_8_rmse_deg": 1.4357861280441284,
  "theta_abs_le_8_p95_abs_err_deg": 2.8736424446105957,
  "theta_abs_le_8_max_abs_err_deg": 6.6937127113342285,
  "theta_abs_le_8_bias_deg": -0.19857913255691528,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 1.065159797668457,
  "theta_abs_le_10_rmse_deg": 1.4318710565567017,
  "theta_abs_le_10_p95_abs_err_deg": 2.828537940979004,
  "theta_abs_le_10_max_abs_err_deg": 9.018074035644531,
  "theta_abs_le_10_bias_deg": -0.20194195210933685,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 1.0093083381652832,
  "theta_pos_8_10_rmse_deg": 1.2277051210403442,
  "theta_pos_8_10_p95_abs_err_deg": 2.115720510482788,
  "theta_pos_8_10_max_abs_err_deg": 5.1947808265686035,
  "theta_pos_8_10_bias_deg": -0.7384296655654907,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 1.0899304151535034,
  "theta_neg_10_8_rmse_deg": 1.5833805799484253,
  "theta_neg_10_8_p95_abs_err_deg": 2.9586353302001953,
  "theta_neg_10_8_max_abs_err_deg": 9.018074035644531,
  "theta_neg_10_8_bias_deg": 0.3152041435241699,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 1.1273391246795654,
  "theta_pos_6_8_rmse_deg": 1.3575681447982788,
  "theta_pos_6_8_p95_abs_err_deg": 2.477416515350342,
  "theta_pos_6_8_max_abs_err_deg": 4.863433361053467,
  "theta_pos_6_8_bias_deg": -0.6666726469993591,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.9388219118118286,
  "theta_neg_8_6_rmse_deg": 1.2560056447982788,
  "theta_neg_8_6_p95_abs_err_deg": 2.3144822120666504,
  "theta_neg_8_6_max_abs_err_deg": 6.421632766723633,
  "theta_neg_8_6_bias_deg": -0.11941556632518768,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7697911262512207,
  "theta_neg_4_2_rmse_deg": 1.08903968334198,
  "theta_neg_4_2_p95_abs_err_deg": 2.4080638885498047,
  "theta_neg_4_2_max_abs_err_deg": 5.530961036682129,
  "theta_neg_4_2_bias_deg": 0.029504839330911636,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 1.361216425895691,
  "theta_neg_2_0p5_rmse_deg": 1.625319480895996,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.817603588104248,
  "theta_neg_2_0p5_max_abs_err_deg": 4.178695201873779,
  "theta_neg_2_0p5_bias_deg": -0.24840191006660461,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0174850225448608,
  "theta_pos_0p5_2_rmse_deg": 1.3942288160324097,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.5507962703704834,
  "theta_pos_0p5_2_max_abs_err_deg": 5.8496012687683105,
  "theta_pos_0p5_2_bias_deg": 0.022515326738357544,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.22604364397077342,
  "loss_turn": 1.092456158830284,
  "loss_theta": 0.0006208905476965867,
  "loss_main_bundle_base": 0.22604364397077342,
  "loss_turn_bundle_base": 0.21849123486323996,
  "loss_theta_bundle_base": 0.0005078012623864507,
  "loss_main_bundle": 0.22604364397077342,
  "loss_turn_bundle": 0.21849123486323996,
  "loss_theta_bundle": 0.0005078012623864507,
  "loss_theta_flat": 0.0010275544345073897,
  "loss_theta_near_flat": 0.001370999485087935,
  "loss_theta_error_excess": 0.00021348331453302605,
  "loss_theta_flat_excess": 0.0006377496329231972,
  "loss_theta_near_flat_excess": 0.0009150596506608819,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00018248920910519137,
  "loss_theta_small_neg": 0.00035154249965552246,
  "loss_theta_small_neg_excess": 9.133206347219554e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.48143101186971704,
  "loss_false_turn_straight": 0.376798339311099,
  "loss_transition_focal_raw": 0.6903177179406235,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.2579183366366506,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
