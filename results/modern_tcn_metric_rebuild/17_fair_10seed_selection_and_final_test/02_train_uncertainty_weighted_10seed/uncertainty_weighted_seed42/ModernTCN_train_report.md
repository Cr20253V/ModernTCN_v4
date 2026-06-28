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
| acc_main | 0.9578 |
| acc_turn | 0.5652 |
| acc_turn_pure | 0.5834 |
| acc_turn_transition | 0.4858 |
| main_confidence_mean | 0.9881 |
| main_low_conf_0p60_ratio | 0.0061 |
| main_low_conf_0p70_ratio | 0.0122 |
| turn_confidence_mean | 0.8074 |
| turn_low_conf_0p60_ratio | 0.1602 |
| turn_low_conf_0p70_ratio | 0.3043 |
| turn_right_recall | 0.6070 |
| turn_straight_recall | 0.5566 |
| turn_left_recall | 0.5460 |
| theta_mae_deg | 0.6511 |
| theta_abs_le_10_p95_abs_err_deg | 1.7302 |
| theta_neg_10_8_p95_abs_err_deg | 1.4925 |
| theta_pos_8_10_p95_abs_err_deg | 2.7268 |
| theta_abs_le_8_p95_abs_err_deg | 1.6728 |
| theta_neg_8_6_p95_abs_err_deg | 1.3720 |
| theta_pos_6_8_p95_abs_err_deg | 1.5569 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.2991 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.7315 |
| theta_flat_abs_p95_deg | 2.4714 |
| theta_flat_bias_deg | -0.0657 |
| theta_near_flat_abs_p95_deg | 1.6013 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.2232 |
| theta_flat_turn_abs_p95_deg | 1.4268 |
| flat_recall | 0.9220 |
| stall_recall | 0.6875 |
| slope_recall | 0.9771 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7563 |
| downhill_recall | 0.8099 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    697,
    0,
    59
  ],
  [
    10,
    66,
    20
  ],
  [
    50,
    13,
    2687
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    485,
    199,
    115
  ],
  [
    397,
    1076,
    460
  ],
  [
    179,
    216,
    475
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.332251 |
| test_loss_turn_bundle_base | 0.110189 |
| test_loss_theta_bundle_base | 0.000164 |
| test_loss_transition_focal_raw | 1.259239 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.344612 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 75
- train_seconds: 1623.4

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 22 | 0.6364 | 0.5511 |
| [0.60,0.70) | 22 | 0.5455 | 0.6498 |
| [0.70,0.80) | 32 | 0.3750 | 0.7559 |
| [0.80,0.90) | 63 | 0.5556 | 0.8554 |
| [0.90,1.00) | 3463 | 0.0228 | 0.9976 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 577 | 0.5945 | 0.5255 |
| [0.60,0.70) | 519 | 0.5568 | 0.6506 |
| [0.70,0.80) | 455 | 0.5429 | 0.7497 |
| [0.80,0.90) | 553 | 0.4702 | 0.8549 |
| [0.90,1.00) | 1498 | 0.2850 | 0.9702 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.4858

## 验证集最佳点

```json
{
  "loss_total": 0.376906172291997,
  "acc_main": 0.9483085250338295,
  "acc_turn": 0.6281461434370771,
  "acc_turn_pure": 0.6460176991150443,
  "acc_turn_transition": 0.5434782608695652,
  "false_turn_straight": 0.4402286902286902,
  "flat_recall": 0.954337899543379,
  "stall_recall": 0.5238095238095238,
  "slope_recall": 0.9529372496662216,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.954337899543379,
    0.5238095238095238,
    0.9529372496662216
  ],
  "turn_right_recall": 0.6966824644549763,
  "turn_straight_recall": 0.5597713097713097,
  "turn_left_recall": 0.7076591154261057,
  "recall_turn": [
    0.6966824644549763,
    0.5597713097713097,
    0.7076591154261057
  ],
  "cm_turn": [
    [
      588,
      212,
      44
    ],
    [
      479,
      1077,
      368
    ],
    [
      126,
      145,
      656
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
      22,
      20
    ],
    [
      133,
      8,
      2855
    ]
  ],
  "main_confidence_mean": 0.9733158194754511,
  "main_confidence_error_mean": 0.787142850660603,
  "main_low_conf_0p60_ratio": 0.0037889039242219214,
  "main_low_conf_0p70_ratio": 0.0557510148849797,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 14,
      "error_rate": 0.35714285714285715,
      "mean_confidence": 0.5600468777239626
    },
    {
      "bin": "[0.60,0.70)",
      "n": 192,
      "error_rate": 0.46875,
      "mean_confidence": 0.6168563233559153
    },
    {
      "bin": "[0.70,0.80)",
      "n": 23,
      "error_rate": 0.21739130434782608,
      "mean_confidence": 0.7629648476558605
    },
    {
      "bin": "[0.80,0.90)",
      "n": 42,
      "error_rate": 0.2619047619047619,
      "mean_confidence": 0.8512846797944398
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3424,
      "error_rate": 0.02336448598130841,
      "mean_confidence": 0.9979038360227421
    }
  ],
  "turn_confidence_mean": 0.8100130542740351,
  "turn_confidence_error_mean": 0.734060465261005,
  "turn_low_conf_0p60_ratio": 0.1983761840324763,
  "turn_low_conf_0p70_ratio": 0.30121786197564276,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 733,
      "error_rate": 0.6125511596180082,
      "mean_confidence": 0.5072961902978967
    },
    {
      "bin": "[0.60,0.70)",
      "n": 380,
      "error_rate": 0.4605263157894737,
      "mean_confidence": 0.6503016910468147
    },
    {
      "bin": "[0.70,0.80)",
      "n": 361,
      "error_rate": 0.4265927977839335,
      "mean_confidence": 0.7482180256981877
    },
    {
      "bin": "[0.80,0.90)",
      "n": 506,
      "error_rate": 0.39920948616600793,
      "mean_confidence": 0.8564804281082778
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1715,
      "error_rate": 0.22973760932944606,
      "mean_confidence": 0.9740814469717656
    }
  ],
  "theta_mae_rad": 0.013067231513559818,
  "theta_mae_deg": 0.7486971616744995,
  "uphill_recall": 0.7784366576819407,
  "downhill_recall": 0.8014460511679644,
  "slope_sign_acc": 0.9723514919244457,
  "theta_flat_mae_deg": 1.065439224243164,
  "theta_flat_abs_p95_deg": 3.6469902992248535,
  "theta_flat_abs_max_deg": 7.134735584259033,
  "theta_flat_bias_deg": 0.659509003162384,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4301804304122925,
  "theta_near_flat_abs_p95_deg": 3.647017478942871,
  "theta_near_flat_abs_max_deg": 7.134735584259033,
  "theta_near_flat_bias_deg": 0.9356152415275574,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1560516357421875,
  "theta_flat_turn_abs_p95_deg": 4.361601829528809,
  "theta_flat_turn_abs_max_deg": 7.134735584259033,
  "theta_flat_turn_bias_deg": 0.49025458097457886,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7486971616744995,
  "theta_slope_control_abs_p95_deg": 9.705117225646973,
  "theta_slope_control_abs_max_deg": 11.977774620056152,
  "theta_slope_control_bias_deg": 0.10972250252962112,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7486971616744995,
  "theta_all_rmse_deg": 1.1803494691848755,
  "theta_all_p95_abs_err_deg": 2.5917837619781494,
  "theta_all_max_abs_err_deg": 7.301496505737305,
  "theta_all_bias_deg": 0.10972249507904053,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6792380213737488,
  "theta_active_abs_ge_2_rmse_deg": 1.0720605850219727,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.219353199005127,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.275216579437256,
  "theta_active_abs_ge_2_bias_deg": -0.010841485112905502,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7849294543266296,
  "theta_abs_le_8_rmse_deg": 1.2159864902496338,
  "theta_abs_le_8_p95_abs_err_deg": 2.7655017375946045,
  "theta_abs_le_8_max_abs_err_deg": 7.301496505737305,
  "theta_abs_le_8_bias_deg": 0.1084517240524292,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7486971616744995,
  "theta_abs_le_10_rmse_deg": 1.1803494691848755,
  "theta_abs_le_10_p95_abs_err_deg": 2.5917837619781494,
  "theta_abs_le_10_max_abs_err_deg": 7.301496505737305,
  "theta_abs_le_10_bias_deg": 0.10972249507904053,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5697528719902039,
  "theta_pos_8_10_rmse_deg": 0.7976647019386292,
  "theta_pos_8_10_p95_abs_err_deg": 2.0209803581237793,
  "theta_pos_8_10_max_abs_err_deg": 3.9347188472747803,
  "theta_pos_8_10_bias_deg": 0.20504161715507507,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6223952174186707,
  "theta_neg_10_8_rmse_deg": 1.198549747467041,
  "theta_neg_10_8_p95_abs_err_deg": 1.795484185218811,
  "theta_neg_10_8_max_abs_err_deg": 7.133045673370361,
  "theta_neg_10_8_bias_deg": 0.023569565266370773,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.49249497056007385,
  "theta_pos_6_8_rmse_deg": 0.7899524569511414,
  "theta_pos_6_8_p95_abs_err_deg": 1.5237574577331543,
  "theta_pos_6_8_max_abs_err_deg": 3.834242582321167,
  "theta_pos_6_8_bias_deg": 0.1577635109424591,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7339943051338196,
  "theta_neg_8_6_rmse_deg": 1.0870672464370728,
  "theta_neg_8_6_p95_abs_err_deg": 2.1179192066192627,
  "theta_neg_8_6_max_abs_err_deg": 6.883356094360352,
  "theta_neg_8_6_bias_deg": -0.07663144171237946,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8170112371444702,
  "theta_neg_4_2_rmse_deg": 1.1821202039718628,
  "theta_neg_4_2_p95_abs_err_deg": 2.238743782043457,
  "theta_neg_4_2_max_abs_err_deg": 7.275216579437256,
  "theta_neg_4_2_bias_deg": -0.2707512378692627,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.43937933444976807,
  "theta_neg_2_0p5_rmse_deg": 0.686324954032898,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.116936445236206,
  "theta_neg_2_0p5_max_abs_err_deg": 5.227802276611328,
  "theta_neg_2_0p5_bias_deg": 0.13611413538455963,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.268325924873352,
  "theta_pos_0p5_2_rmse_deg": 1.5002617835998535,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.1469905376434326,
  "theta_pos_0p5_2_max_abs_err_deg": 4.754593849182129,
  "theta_pos_0p5_2_bias_deg": 0.9526569247245789,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2772089731225464,
  "loss_turn": 1.242619369478445,
  "loss_theta": 0.00042439687739382215,
  "loss_main_bundle_base": 0.2772089731225464,
  "loss_turn_bundle_base": 0.09940954768407652,
  "loss_theta_bundle_base": 0.00028764401766987006,
  "loss_main_bundle": 0.2772089731225464,
  "loss_turn_bundle": 0.09940954768407652,
  "loss_theta_bundle": 0.00028764401766987006,
  "loss_theta_flat": 0.00027645050415257876,
  "loss_theta_near_flat": 0.001281851806699302,
  "loss_theta_error_excess": 0.00016512049981002244,
  "loss_theta_flat_excess": 0.00012645386095029264,
  "loss_theta_near_flat_excess": 0.0009133845910490446,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00012795651076028832,
  "loss_theta_small_neg": 0.00042149174108745905,
  "loss_theta_small_neg_excess": 0.00014940707055701848,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4119255625104711,
  "loss_false_turn_straight": 0.3134288739932245,
  "loss_transition_focal_raw": 1.0117081308558442,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.1439830238022273,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
