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
| acc_main | 0.9622 |
| acc_turn | 0.6033 |
| acc_turn_pure | 0.6220 |
| acc_turn_transition | 0.5216 |
| main_confidence_mean | 0.9874 |
| main_low_conf_0p60_ratio | 0.0072 |
| main_low_conf_0p70_ratio | 0.0147 |
| turn_confidence_mean | 0.8239 |
| turn_low_conf_0p60_ratio | 0.1574 |
| turn_low_conf_0p70_ratio | 0.2604 |
| turn_right_recall | 0.5945 |
| turn_straight_recall | 0.6389 |
| turn_left_recall | 0.5322 |
| theta_mae_deg | 0.5951 |
| theta_abs_le_10_p95_abs_err_deg | 1.6177 |
| theta_neg_10_8_p95_abs_err_deg | 1.6274 |
| theta_pos_8_10_p95_abs_err_deg | 2.9937 |
| theta_abs_le_8_p95_abs_err_deg | 1.4786 |
| theta_neg_8_6_p95_abs_err_deg | 1.4117 |
| theta_pos_6_8_p95_abs_err_deg | 1.2964 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6604 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.2290 |
| theta_flat_abs_p95_deg | 2.5589 |
| theta_flat_bias_deg | -0.2891 |
| theta_near_flat_abs_p95_deg | 1.6839 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.2053 |
| theta_flat_turn_abs_p95_deg | 1.4648 |
| flat_recall | 0.9656 |
| stall_recall | 0.6562 |
| slope_recall | 0.9720 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7460 |
| downhill_recall | 0.7934 |

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
    63,
    23
  ],
  [
    70,
    7,
    2673
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    475,
    218,
    106
  ],
  [
    364,
    1235,
    334
  ],
  [
    158,
    249,
    463
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.328878 |
| test_loss_turn_bundle_base | 0.119562 |
| test_loss_theta_bundle_base | 0.000150 |
| test_loss_transition_focal_raw | 1.343870 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.759555 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 96
- train_seconds: 1956.2

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 26 | 0.6154 | 0.5436 |
| [0.60,0.70) | 27 | 0.4815 | 0.6487 |
| [0.70,0.80) | 31 | 0.3226 | 0.7595 |
| [0.80,0.90) | 65 | 0.4769 | 0.8531 |
| [0.90,1.00) | 3453 | 0.0191 | 0.9980 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 567 | 0.5855 | 0.5089 |
| [0.60,0.70) | 371 | 0.5229 | 0.6507 |
| [0.70,0.80) | 418 | 0.5167 | 0.7502 |
| [0.80,0.90) | 541 | 0.3900 | 0.8553 |
| [0.90,1.00) | 1705 | 0.2792 | 0.9744 |


## 验证集最佳点

```json
{
  "loss_total": 0.44479764145830486,
  "acc_main": 0.9493910690121786,
  "acc_turn": 0.652232746955345,
  "acc_turn_pure": 0.6660111438872501,
  "acc_turn_transition": 0.5869565217391305,
  "false_turn_straight": 0.38461538461538464,
  "flat_recall": 0.969558599695586,
  "stall_recall": 0.42857142857142855,
  "slope_recall": 0.9522696929238985,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.07142857142857142,
  "recall_main": [
    0.969558599695586,
    0.42857142857142855,
    0.9522696929238985
  ],
  "turn_right_recall": 0.6386255924170616,
  "turn_straight_recall": 0.6153846153846154,
  "turn_left_recall": 0.7411003236245954,
  "recall_turn": [
    0.6386255924170616,
    0.6153846153846154,
    0.7411003236245954
  ],
  "cm_turn": [
    [
      539,
      206,
      99
    ],
    [
      282,
      1184,
      458
    ],
    [
      63,
      177,
      687
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      637,
      0,
      20
    ],
    [
      3,
      18,
      21
    ],
    [
      136,
      7,
      2853
    ]
  ],
  "main_confidence_mean": 0.9698054929446237,
  "main_confidence_error_mean": 0.7354203561774025,
  "main_low_conf_0p60_ratio": 0.04925575101488498,
  "main_low_conf_0p70_ratio": 0.05331529093369418,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 182,
      "error_rate": 0.4835164835164835,
      "mean_confidence": 0.5029180546157711
    },
    {
      "bin": "[0.60,0.70)",
      "n": 15,
      "error_rate": 0.6,
      "mean_confidence": 0.6507828011637289
    },
    {
      "bin": "[0.70,0.80)",
      "n": 17,
      "error_rate": 0.17647058823529413,
      "mean_confidence": 0.7608104390112475
    },
    {
      "bin": "[0.80,0.90)",
      "n": 36,
      "error_rate": 0.16666666666666666,
      "mean_confidence": 0.8501098392676298
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3445,
      "error_rate": 0.02351233671988389,
      "mean_confidence": 0.9981424489973969
    }
  ],
  "turn_confidence_mean": 0.8451320752452636,
  "turn_confidence_error_mean": 0.7634546453375037,
  "turn_low_conf_0p60_ratio": 0.1445196211096076,
  "turn_low_conf_0p70_ratio": 0.21975642760487143,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 534,
      "error_rate": 0.6123595505617978,
      "mean_confidence": 0.47533570469314146
    },
    {
      "bin": "[0.60,0.70)",
      "n": 278,
      "error_rate": 0.5035971223021583,
      "mean_confidence": 0.6505535739182943
    },
    {
      "bin": "[0.70,0.80)",
      "n": 330,
      "error_rate": 0.47575757575757577,
      "mean_confidence": 0.7518051107852098
    },
    {
      "bin": "[0.80,0.90)",
      "n": 467,
      "error_rate": 0.3618843683083512,
      "mean_confidence": 0.8527335760649081
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2086,
      "error_rate": 0.23585810162991372,
      "mean_confidence": 0.978790791751867
    }
  ],
  "theta_mae_rad": 0.012676232494413853,
  "theta_mae_deg": 0.7262945771217346,
  "uphill_recall": 0.7778975741239892,
  "downhill_recall": 0.7953281423804227,
  "slope_sign_acc": 0.9742677251574049,
  "theta_flat_mae_deg": 1.0320169925689697,
  "theta_flat_abs_p95_deg": 3.7599775791168213,
  "theta_flat_abs_max_deg": 8.394902229309082,
  "theta_flat_bias_deg": 0.3360600471496582,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4533910751342773,
  "theta_near_flat_abs_p95_deg": 4.0237812995910645,
  "theta_near_flat_abs_max_deg": 8.394902229309082,
  "theta_near_flat_bias_deg": 0.9167191386222839,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1899205446243286,
  "theta_flat_turn_abs_p95_deg": 5.89867639541626,
  "theta_flat_turn_abs_max_deg": 8.394902229309082,
  "theta_flat_turn_bias_deg": 0.5906738638877869,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7262945771217346,
  "theta_slope_control_abs_p95_deg": 9.284128189086914,
  "theta_slope_control_abs_max_deg": 11.956225395202637,
  "theta_slope_control_bias_deg": 0.10402372479438782,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7262946367263794,
  "theta_all_rmse_deg": 1.138290524482727,
  "theta_all_p95_abs_err_deg": 2.3004603385925293,
  "theta_all_max_abs_err_deg": 8.894902229309082,
  "theta_all_bias_deg": 0.10402371734380722,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6592519879341125,
  "theta_active_abs_ge_2_rmse_deg": 0.9753904342651367,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.8865019083023071,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.9976677894592285,
  "theta_active_abs_ge_2_bias_deg": 0.05313991382718086,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7442901134490967,
  "theta_abs_le_8_rmse_deg": 1.1553417444229126,
  "theta_abs_le_8_p95_abs_err_deg": 2.467780351638794,
  "theta_abs_le_8_max_abs_err_deg": 8.894902229309082,
  "theta_abs_le_8_bias_deg": 0.05532805249094963,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7262946367263794,
  "theta_abs_le_10_rmse_deg": 1.138290524482727,
  "theta_abs_le_10_p95_abs_err_deg": 2.3004603385925293,
  "theta_abs_le_10_max_abs_err_deg": 8.894902229309082,
  "theta_abs_le_10_bias_deg": 0.10402371734380722,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.44423404335975647,
  "theta_pos_8_10_rmse_deg": 0.762513279914856,
  "theta_pos_8_10_p95_abs_err_deg": 1.6881918907165527,
  "theta_pos_8_10_max_abs_err_deg": 5.296274185180664,
  "theta_pos_8_10_bias_deg": 0.008594454266130924,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8600894808769226,
  "theta_neg_10_8_rmse_deg": 1.2998114824295044,
  "theta_neg_10_8_p95_abs_err_deg": 2.300963878631592,
  "theta_neg_10_8_max_abs_err_deg": 6.9976677894592285,
  "theta_neg_10_8_bias_deg": 0.6155073046684265,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5792545676231384,
  "theta_pos_6_8_rmse_deg": 0.9149588942527771,
  "theta_pos_6_8_p95_abs_err_deg": 1.6344411373138428,
  "theta_pos_6_8_max_abs_err_deg": 4.846874237060547,
  "theta_pos_6_8_bias_deg": -0.08945810049772263,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.6789583563804626,
  "theta_neg_8_6_rmse_deg": 0.9669204354286194,
  "theta_neg_8_6_p95_abs_err_deg": 1.625593900680542,
  "theta_neg_8_6_max_abs_err_deg": 6.683741569519043,
  "theta_neg_8_6_bias_deg": 0.2701350748538971,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6299686431884766,
  "theta_neg_4_2_rmse_deg": 0.8523093461990356,
  "theta_neg_4_2_p95_abs_err_deg": 1.8836596012115479,
  "theta_neg_4_2_max_abs_err_deg": 4.949159145355225,
  "theta_neg_4_2_bias_deg": -0.11890744417905807,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5428531765937805,
  "theta_neg_2_0p5_rmse_deg": 0.7348359227180481,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.2147393226623535,
  "theta_neg_2_0p5_max_abs_err_deg": 4.796502590179443,
  "theta_neg_2_0p5_bias_deg": -0.3463287651538849,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0097761154174805,
  "theta_pos_0p5_2_rmse_deg": 1.3646587133407593,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.291586399078369,
  "theta_pos_0p5_2_max_abs_err_deg": 3.541579246520996,
  "theta_pos_0p5_2_bias_deg": 0.26635053753852844,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3255496609598116,
  "loss_turn": 1.487279916874288,
  "loss_theta": 0.00039452120525628853,
  "loss_main_bundle_base": 0.3255496609598116,
  "loss_turn_bundle_base": 0.11898238948257753,
  "loss_theta_bundle_base": 0.0002655885694847796,
  "loss_main_bundle": 0.3255496609598116,
  "loss_turn_bundle": 0.11898238948257753,
  "loss_theta_bundle": 0.0002655885694847796,
  "loss_theta_flat": 0.00027100406514659665,
  "loss_theta_near_flat": 0.0015294807217952182,
  "loss_theta_error_excess": 0.00015107307864916392,
  "loss_theta_flat_excess": 0.000141241544926856,
  "loss_theta_near_flat_excess": 0.0011411137831635542,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 8.527757890594314e-05,
  "loss_theta_small_neg": 0.00021641969168653235,
  "loss_theta_small_neg_excess": 3.860123346350005e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.35511461543940076,
  "loss_false_turn_straight": 0.27095041021765165,
  "loss_transition_focal_raw": 1.3524515224245146,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.940515727830921,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
