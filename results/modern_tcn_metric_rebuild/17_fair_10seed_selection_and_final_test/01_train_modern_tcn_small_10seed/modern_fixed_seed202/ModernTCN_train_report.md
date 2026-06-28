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
| acc_main | 0.9542 |
| acc_turn | 0.5905 |
| acc_turn_pure | 0.6073 |
| acc_turn_transition | 0.5171 |
| main_confidence_mean | 0.9859 |
| main_low_conf_0p60_ratio | 0.0125 |
| main_low_conf_0p70_ratio | 0.0178 |
| turn_confidence_mean | 0.7515 |
| turn_low_conf_0p60_ratio | 0.2618 |
| turn_low_conf_0p70_ratio | 0.4134 |
| turn_right_recall | 0.5419 |
| turn_straight_recall | 0.6570 |
| turn_left_recall | 0.4874 |
| theta_mae_deg | 0.6340 |
| theta_abs_le_10_p95_abs_err_deg | 1.7836 |
| theta_neg_10_8_p95_abs_err_deg | 2.4081 |
| theta_pos_8_10_p95_abs_err_deg | 2.6114 |
| theta_abs_le_8_p95_abs_err_deg | 1.6842 |
| theta_neg_8_6_p95_abs_err_deg | 1.8153 |
| theta_pos_6_8_p95_abs_err_deg | 1.4763 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.2351 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5628 |
| theta_flat_abs_p95_deg | 2.3470 |
| theta_flat_bias_deg | -0.1453 |
| theta_near_flat_abs_p95_deg | 1.9416 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1516 |
| theta_flat_turn_abs_p95_deg | 1.9613 |
| flat_recall | 0.9259 |
| stall_recall | 0.6354 |
| slope_recall | 0.9731 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7477 |
| downhill_recall | 0.8104 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    700,
    0,
    56
  ],
  [
    9,
    61,
    26
  ],
  [
    66,
    8,
    2676
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    433,
    264,
    102
  ],
  [
    374,
    1270,
    289
  ],
  [
    156,
    290,
    424
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.338437 |
| test_loss_turn_bundle_base | 0.092355 |
| test_loss_theta_bundle_base | 0.000179 |
| test_loss_transition_focal_raw | 0.965923 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 2.930496 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 51
- train_seconds: 837.4

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 45 | 0.6444 | 0.5403 |
| [0.60,0.70) | 19 | 0.4211 | 0.6441 |
| [0.70,0.80) | 22 | 0.4091 | 0.7492 |
| [0.80,0.90) | 56 | 0.2857 | 0.8527 |
| [0.90,1.00) | 3460 | 0.0298 | 0.9972 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 943 | 0.5620 | 0.5066 |
| [0.60,0.70) | 546 | 0.4835 | 0.6485 |
| [0.70,0.80) | 525 | 0.4057 | 0.7459 |
| [0.80,0.90) | 468 | 0.4231 | 0.8524 |
| [0.90,1.00) | 1120 | 0.2411 | 0.9684 |


## 验证集最佳点

```json
{
  "loss_total": 0.41779781239603786,
  "acc_main": 0.9404600811907984,
  "acc_turn": 0.5940460081190798,
  "acc_turn_pure": 0.6037364798426745,
  "acc_turn_transition": 0.5481366459627329,
  "false_turn_straight": 0.4376299376299376,
  "flat_recall": 0.9467275494672754,
  "stall_recall": 0.23809523809523808,
  "slope_recall": 0.9489319092122831,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.09523809523809523,
  "recall_main": [
    0.9467275494672754,
    0.23809523809523808,
    0.9489319092122831
  ],
  "turn_right_recall": 0.5770142180094787,
  "turn_straight_recall": 0.5623700623700624,
  "turn_left_recall": 0.6752966558791802,
  "recall_turn": [
    0.5770142180094787,
    0.5623700623700624,
    0.6752966558791802
  ],
  "cm_turn": [
    [
      487,
      234,
      123
    ],
    [
      334,
      1082,
      508
    ],
    [
      70,
      231,
      626
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      622,
      0,
      35
    ],
    [
      4,
      10,
      28
    ],
    [
      143,
      10,
      2843
    ]
  ],
  "main_confidence_mean": 0.9646363651832328,
  "main_confidence_error_mean": 0.7495157527939144,
  "main_low_conf_0p60_ratio": 0.053585926928281465,
  "main_low_conf_0p70_ratio": 0.060081190798376184,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 198,
      "error_rate": 0.4595959595959596,
      "mean_confidence": 0.5127345402298651
    },
    {
      "bin": "[0.60,0.70)",
      "n": 24,
      "error_rate": 0.4583333333333333,
      "mean_confidence": 0.6447032204931609
    },
    {
      "bin": "[0.70,0.80)",
      "n": 31,
      "error_rate": 0.3870967741935484,
      "mean_confidence": 0.751767738316185
    },
    {
      "bin": "[0.80,0.90)",
      "n": 59,
      "error_rate": 0.23728813559322035,
      "mean_confidence": 0.8519560893177479
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3383,
      "error_rate": 0.027194797516996747,
      "mean_confidence": 0.9972707194611727
    }
  ],
  "turn_confidence_mean": 0.7647090950197847,
  "turn_confidence_error_mean": 0.6851223596585052,
  "turn_low_conf_0p60_ratio": 0.2411366711772666,
  "turn_low_conf_0p70_ratio": 0.38105548037889037,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 891,
      "error_rate": 0.6184062850729517,
      "mean_confidence": 0.49816044500561824
    },
    {
      "bin": "[0.60,0.70)",
      "n": 517,
      "error_rate": 0.5531914893617021,
      "mean_confidence": 0.6472683660407091
    },
    {
      "bin": "[0.70,0.80)",
      "n": 497,
      "error_rate": 0.40643863179074446,
      "mean_confidence": 0.7502952694049528
    },
    {
      "bin": "[0.80,0.90)",
      "n": 526,
      "error_rate": 0.3403041825095057,
      "mean_confidence": 0.8517597880733623
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1264,
      "error_rate": 0.2231012658227848,
      "mean_confidence": 0.9700783282707292
    }
  ],
  "theta_mae_rad": 0.013383166864514351,
  "theta_mae_deg": 0.7667989134788513,
  "uphill_recall": 0.7719676549865229,
  "downhill_recall": 0.8042269187986651,
  "slope_sign_acc": 0.9633178209690665,
  "theta_flat_mae_deg": 1.0361343622207642,
  "theta_flat_abs_p95_deg": 3.314305543899536,
  "theta_flat_abs_max_deg": 8.458006858825684,
  "theta_flat_bias_deg": 0.46048006415367126,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.351873755455017,
  "theta_near_flat_abs_p95_deg": 3.694871425628662,
  "theta_near_flat_abs_max_deg": 8.458006858825684,
  "theta_near_flat_bias_deg": 0.7787824869155884,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.0763678550720215,
  "theta_flat_turn_abs_p95_deg": 3.314305543899536,
  "theta_flat_turn_abs_max_deg": 8.458006858825684,
  "theta_flat_turn_bias_deg": 0.5101283192634583,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7667989134788513,
  "theta_slope_control_abs_p95_deg": 9.233861923217773,
  "theta_slope_control_abs_max_deg": 12.398725509643555,
  "theta_slope_control_bias_deg": 0.1363184005022049,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7667989134788513,
  "theta_all_rmse_deg": 1.1623239517211914,
  "theta_all_p95_abs_err_deg": 2.7023799419403076,
  "theta_all_max_abs_err_deg": 8.958006858825684,
  "theta_all_bias_deg": 0.1363184005022049,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7077357172966003,
  "theta_active_abs_ge_2_rmse_deg": 1.0776342153549194,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.3405542373657227,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.721207618713379,
  "theta_active_abs_ge_2_bias_deg": 0.06523220986127853,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8018130660057068,
  "theta_abs_le_8_rmse_deg": 1.1992028951644897,
  "theta_abs_le_8_p95_abs_err_deg": 2.8142712116241455,
  "theta_abs_le_8_max_abs_err_deg": 8.958006858825684,
  "theta_abs_le_8_bias_deg": 0.18474262952804565,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7667989134788513,
  "theta_abs_le_10_rmse_deg": 1.1623239517211914,
  "theta_abs_le_10_p95_abs_err_deg": 2.7023799419403076,
  "theta_abs_le_10_max_abs_err_deg": 8.958006858825684,
  "theta_abs_le_10_bias_deg": 0.1363184005022049,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5737687945365906,
  "theta_pos_8_10_rmse_deg": 0.7391772866249084,
  "theta_pos_8_10_p95_abs_err_deg": 1.2255216836929321,
  "theta_pos_8_10_max_abs_err_deg": 4.693727493286133,
  "theta_pos_8_10_bias_deg": -0.307050883769989,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6651935577392578,
  "theta_neg_10_8_rmse_deg": 1.1951464414596558,
  "theta_neg_10_8_p95_abs_err_deg": 2.5790677070617676,
  "theta_neg_10_8_max_abs_err_deg": 7.5242204666137695,
  "theta_neg_10_8_bias_deg": 0.17525961995124817,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5810145139694214,
  "theta_pos_6_8_rmse_deg": 0.9034548997879028,
  "theta_pos_6_8_p95_abs_err_deg": 1.9971898794174194,
  "theta_pos_6_8_max_abs_err_deg": 3.6734676361083984,
  "theta_pos_6_8_bias_deg": -0.033818550407886505,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.740439772605896,
  "theta_neg_8_6_rmse_deg": 1.1400483846664429,
  "theta_neg_8_6_p95_abs_err_deg": 2.375253200531006,
  "theta_neg_8_6_max_abs_err_deg": 7.721207618713379,
  "theta_neg_8_6_bias_deg": -0.10954762995243073,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6032772660255432,
  "theta_neg_4_2_rmse_deg": 0.8680071234703064,
  "theta_neg_4_2_p95_abs_err_deg": 1.8179646730422974,
  "theta_neg_4_2_max_abs_err_deg": 4.689365863800049,
  "theta_neg_4_2_bias_deg": 0.16542062163352966,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.7701932191848755,
  "theta_neg_2_0p5_rmse_deg": 1.0551882982254028,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.1478776931762695,
  "theta_neg_2_0p5_max_abs_err_deg": 4.515873432159424,
  "theta_neg_2_0p5_bias_deg": 0.1463155299425125,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0607709884643555,
  "theta_pos_0p5_2_rmse_deg": 1.2923839092254639,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.0010063648223877,
  "theta_pos_0p5_2_max_abs_err_deg": 4.374587535858154,
  "theta_pos_0p5_2_bias_deg": 0.5765580534934998,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3270869025035543,
  "loss_turn": 1.130274108298254,
  "loss_theta": 0.0004115946667775492,
  "loss_main_bundle_base": 0.3270869025035543,
  "loss_turn_bundle_base": 0.09042192624531514,
  "loss_theta_bundle_base": 0.0002889773855994031,
  "loss_main_bundle": 0.3270869025035543,
  "loss_turn_bundle": 0.09042192624531514,
  "loss_theta_bundle": 0.0002889773855994031,
  "loss_theta_flat": 0.0003587138493502773,
  "loss_theta_near_flat": 0.0010266370124893114,
  "loss_theta_error_excess": 0.00014763264139422313,
  "loss_theta_flat_excess": 0.00018916586404527677,
  "loss_theta_near_flat_excess": 0.0006947639362359765,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00012173023176590908,
  "loss_theta_small_neg": 0.000225596809356457,
  "loss_theta_small_neg_excess": 5.1836928641920594e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.35742539894919595,
  "loss_false_turn_straight": 0.2804956409782776,
  "loss_transition_focal_raw": 0.8251915410019871,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 5.087433695502793,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
