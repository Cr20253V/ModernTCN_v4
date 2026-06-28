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
| acc_main | 0.9642 |
| acc_turn | 0.6002 |
| acc_turn_pure | 0.6189 |
| acc_turn_transition | 0.5186 |
| main_confidence_mean | 0.9884 |
| main_low_conf_0p60_ratio | 0.0050 |
| main_low_conf_0p70_ratio | 0.0136 |
| turn_confidence_mean | 0.8173 |
| turn_low_conf_0p60_ratio | 0.1816 |
| turn_low_conf_0p70_ratio | 0.2865 |
| turn_right_recall | 0.6108 |
| turn_straight_recall | 0.6203 |
| turn_left_recall | 0.5460 |
| theta_mae_deg | 0.7533 |
| theta_abs_le_10_p95_abs_err_deg | 1.9416 |
| theta_neg_10_8_p95_abs_err_deg | 1.8884 |
| theta_pos_8_10_p95_abs_err_deg | 2.7192 |
| theta_abs_le_8_p95_abs_err_deg | 1.8463 |
| theta_neg_8_6_p95_abs_err_deg | 1.9706 |
| theta_pos_6_8_p95_abs_err_deg | 2.1490 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.8507 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.6341 |
| theta_flat_abs_p95_deg | 2.6337 |
| theta_flat_bias_deg | 0.5999 |
| theta_near_flat_abs_p95_deg | 1.8992 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.6065 |
| theta_flat_turn_abs_p95_deg | 1.8146 |
| flat_recall | 0.9669 |
| stall_recall | 0.6979 |
| slope_recall | 0.9727 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7477 |
| downhill_recall | 0.7923 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    731,
    0,
    25
  ],
  [
    9,
    67,
    20
  ],
  [
    71,
    4,
    2675
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    488,
    199,
    112
  ],
  [
    372,
    1199,
    362
  ],
  [
    184,
    211,
    475
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.338821 |
| test_loss_turn_bundle_base | 0.289019 |
| test_loss_theta_bundle_base | 0.000193 |
| test_loss_transition_focal_raw | 1.451324 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.612181 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 1
- train_seconds: 4.1

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 18 | 0.5000 | 0.5488 |
| [0.60,0.70) | 31 | 0.7419 | 0.6503 |
| [0.70,0.80) | 33 | 0.5758 | 0.7422 |
| [0.80,0.90) | 39 | 0.3077 | 0.8506 |
| [0.90,1.00) | 3481 | 0.0190 | 0.9976 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 654 | 0.5734 | 0.5132 |
| [0.60,0.70) | 378 | 0.5370 | 0.6494 |
| [0.70,0.80) | 384 | 0.5052 | 0.7503 |
| [0.80,0.90) | 472 | 0.4047 | 0.8534 |
| [0.90,1.00) | 1714 | 0.2783 | 0.9754 |


## 验证集最佳点

```json
{
  "loss_total": 0.5635188322912533,
  "acc_main": 0.9491204330175913,
  "acc_turn": 0.6254397834912043,
  "acc_turn_pure": 0.6414290396591281,
  "acc_turn_transition": 0.5496894409937888,
  "false_turn_straight": 0.4017671517671518,
  "flat_recall": 0.9452054794520548,
  "stall_recall": 0.5238095238095238,
  "slope_recall": 0.9559412550066756,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9452054794520548,
    0.5238095238095238,
    0.9559412550066756
  ],
  "turn_right_recall": 0.6338862559241706,
  "turn_straight_recall": 0.5982328482328483,
  "turn_left_recall": 0.674217907227616,
  "recall_turn": [
    0.6338862559241706,
    0.5982328482328483,
    0.674217907227616
  ],
  "cm_turn": [
    [
      535,
      264,
      45
    ],
    [
      361,
      1151,
      412
    ],
    [
      80,
      222,
      625
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      621,
      0,
      36
    ],
    [
      0,
      22,
      20
    ],
    [
      128,
      4,
      2864
    ]
  ],
  "main_confidence_mean": 0.9713533688825575,
  "main_confidence_error_mean": 0.7686313739894628,
  "main_low_conf_0p60_ratio": 0.05006765899864682,
  "main_low_conf_0p70_ratio": 0.05899864682002706,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 185,
      "error_rate": 0.4756756756756757,
      "mean_confidence": 0.5851809773674205
    },
    {
      "bin": "[0.60,0.70)",
      "n": 33,
      "error_rate": 0.2727272727272727,
      "mean_confidence": 0.6542413129856876
    },
    {
      "bin": "[0.70,0.80)",
      "n": 17,
      "error_rate": 0.29411764705882354,
      "mean_confidence": 0.7465668327950015
    },
    {
      "bin": "[0.80,0.90)",
      "n": 36,
      "error_rate": 0.25,
      "mean_confidence": 0.8530351232467095
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3424,
      "error_rate": 0.022488317757009345,
      "mean_confidence": 0.9976347410295424
    }
  ],
  "turn_confidence_mean": 0.8307865391271518,
  "turn_confidence_error_mean": 0.7548014062466584,
  "turn_low_conf_0p60_ratio": 0.18024357239512856,
  "turn_low_conf_0p70_ratio": 0.26008119079837616,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 666,
      "error_rate": 0.6141141141141141,
      "mean_confidence": 0.49895585874899906
    },
    {
      "bin": "[0.60,0.70)",
      "n": 295,
      "error_rate": 0.4915254237288136,
      "mean_confidence": 0.6483990378498654
    },
    {
      "bin": "[0.70,0.80)",
      "n": 340,
      "error_rate": 0.5088235294117647,
      "mean_confidence": 0.7505684069669786
    },
    {
      "bin": "[0.80,0.90)",
      "n": 424,
      "error_rate": 0.4481132075471698,
      "mean_confidence": 0.8538589589301984
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1970,
      "error_rate": 0.23705583756345178,
      "mean_confidence": 0.9791596380848253
    }
  ],
  "theta_mae_rad": 0.015986261889338493,
  "theta_mae_deg": 0.915945291519165,
  "uphill_recall": 0.7816711590296496,
  "downhill_recall": 0.8064516129032258,
  "slope_sign_acc": 0.960032849712565,
  "theta_flat_mae_deg": 1.1483378410339355,
  "theta_flat_abs_p95_deg": 3.880016326904297,
  "theta_flat_abs_max_deg": 7.039588451385498,
  "theta_flat_bias_deg": 0.8951082825660706,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4521048069000244,
  "theta_near_flat_abs_p95_deg": 3.887570381164551,
  "theta_near_flat_abs_max_deg": 7.5313520431518555,
  "theta_near_flat_bias_deg": 1.1177126169204712,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1081701517105103,
  "theta_flat_turn_abs_p95_deg": 3.880016326904297,
  "theta_flat_turn_abs_max_deg": 7.039588451385498,
  "theta_flat_turn_bias_deg": 0.5215640068054199,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.915945291519165,
  "theta_slope_control_abs_p95_deg": 9.223627090454102,
  "theta_slope_control_abs_max_deg": 11.946807861328125,
  "theta_slope_control_bias_deg": 0.6319255232810974,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.9159451723098755,
  "theta_all_rmse_deg": 1.3467272520065308,
  "theta_all_p95_abs_err_deg": 2.8716254234313965,
  "theta_all_max_abs_err_deg": 7.643265724182129,
  "theta_all_bias_deg": 0.6319255232810974,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.8649832010269165,
  "theta_active_abs_ge_2_rmse_deg": 1.2796822786331177,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.7547214031219482,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.643265724182129,
  "theta_active_abs_ge_2_bias_deg": 0.5742115378379822,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9536542892456055,
  "theta_abs_le_8_rmse_deg": 1.3769440650939941,
  "theta_abs_le_8_p95_abs_err_deg": 3.02390193939209,
  "theta_abs_le_8_max_abs_err_deg": 7.461370944976807,
  "theta_abs_le_8_bias_deg": 0.6514403820037842,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.9159451723098755,
  "theta_abs_le_10_rmse_deg": 1.3467272520065308,
  "theta_abs_le_10_p95_abs_err_deg": 2.8716254234313965,
  "theta_abs_le_10_max_abs_err_deg": 7.643265724182129,
  "theta_abs_le_10_bias_deg": 0.6319255232810974,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.4979347586631775,
  "theta_pos_8_10_rmse_deg": 0.7446333765983582,
  "theta_pos_8_10_p95_abs_err_deg": 1.537435531616211,
  "theta_pos_8_10_max_abs_err_deg": 3.8056023120880127,
  "theta_pos_8_10_bias_deg": 0.17304162681102753,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 1.020275592803955,
  "theta_neg_10_8_rmse_deg": 1.547338604927063,
  "theta_neg_10_8_p95_abs_err_deg": 2.8120622634887695,
  "theta_neg_10_8_max_abs_err_deg": 7.643265724182129,
  "theta_neg_10_8_bias_deg": 0.9326702952384949,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6029452085494995,
  "theta_pos_6_8_rmse_deg": 0.8459352254867554,
  "theta_pos_6_8_p95_abs_err_deg": 1.8024910688400269,
  "theta_pos_6_8_max_abs_err_deg": 3.842007637023926,
  "theta_pos_6_8_bias_deg": 0.35122963786125183,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.9129509925842285,
  "theta_neg_8_6_rmse_deg": 1.288509488105774,
  "theta_neg_8_6_p95_abs_err_deg": 2.7336835861206055,
  "theta_neg_8_6_max_abs_err_deg": 7.27924108505249,
  "theta_neg_8_6_bias_deg": 0.6520463228225708,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.9006451368331909,
  "theta_neg_4_2_rmse_deg": 1.1405996084213257,
  "theta_neg_4_2_p95_abs_err_deg": 2.080517053604126,
  "theta_neg_4_2_max_abs_err_deg": 5.121999263763428,
  "theta_neg_4_2_bias_deg": 0.569785475730896,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5362266302108765,
  "theta_neg_2_0p5_rmse_deg": 0.8133723139762878,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.3529855012893677,
  "theta_neg_2_0p5_max_abs_err_deg": 5.538967132568359,
  "theta_neg_2_0p5_bias_deg": 0.2872403860092163,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.486207127571106,
  "theta_pos_0p5_2_rmse_deg": 1.7022712230682373,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.380016326904297,
  "theta_pos_0p5_2_max_abs_err_deg": 4.565609931945801,
  "theta_pos_0p5_2_bias_deg": 1.4076873064041138,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.291049872941674,
  "loss_turn": 1.3606702901675027,
  "loss_theta": 0.0005526017338410524,
  "loss_main_bundle_base": 0.291049872941674,
  "loss_turn_bundle_base": 0.2721340631680495,
  "loss_theta_bundle_base": 0.0003348933451154291,
  "loss_main_bundle": 0.291049872941674,
  "loss_turn_bundle": 0.2721340631680495,
  "loss_theta_bundle": 0.0003348933451154291,
  "loss_theta_flat": 0.00025801988173629174,
  "loss_theta_near_flat": 0.001249477237302946,
  "loss_theta_error_excess": 0.00021427228049808643,
  "loss_theta_flat_excess": 0.00013249129603336253,
  "loss_theta_near_flat_excess": 0.0008815680053626995,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00018859209861188587,
  "loss_theta_small_neg": 0.0003899929016883358,
  "loss_theta_small_neg_excess": 8.68279013238628e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.38106392572793973,
  "loss_false_turn_straight": 0.30265154305427094,
  "loss_transition_focal_raw": 1.189054612732708,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.7094426782273744,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0,
  "preserve_loss": 0.003153128083795309
}
```
