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
  "lambda_theta": 0.5,
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
| acc_main | 0.9645 |
| acc_turn | 0.5847 |
| acc_turn_pure | 0.6008 |
| acc_turn_transition | 0.5142 |
| main_confidence_mean | 0.9886 |
| main_low_conf_0p60_ratio | 0.0044 |
| main_low_conf_0p70_ratio | 0.0114 |
| turn_confidence_mean | 0.8300 |
| turn_low_conf_0p60_ratio | 0.1499 |
| turn_low_conf_0p70_ratio | 0.2554 |
| turn_right_recall | 0.6208 |
| turn_straight_recall | 0.5835 |
| turn_left_recall | 0.5540 |
| theta_mae_deg | 0.6291 |
| theta_abs_le_10_p95_abs_err_deg | 1.7202 |
| theta_neg_10_8_p95_abs_err_deg | 2.2020 |
| theta_pos_8_10_p95_abs_err_deg | 2.7541 |
| theta_abs_le_8_p95_abs_err_deg | 1.6169 |
| theta_neg_8_6_p95_abs_err_deg | 1.2995 |
| theta_pos_6_8_p95_abs_err_deg | 1.5090 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.4755 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5137 |
| theta_flat_abs_p95_deg | 2.5175 |
| theta_flat_bias_deg | -0.4782 |
| theta_near_flat_abs_p95_deg | 1.9802 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.6494 |
| theta_flat_turn_abs_p95_deg | 1.7578 |
| flat_recall | 0.9669 |
| stall_recall | 0.6562 |
| slope_recall | 0.9745 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7494 |
| downhill_recall | 0.7934 |

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
    63,
    24
  ],
  [
    61,
    9,
    2680
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    496,
    186,
    117
  ],
  [
    412,
    1128,
    393
  ],
  [
    172,
    216,
    482
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.344473 |
| test_loss_turn_bundle_base | 0.330163 |
| test_loss_theta_bundle_base | 0.000163 |
| test_loss_transition_focal_raw | 1.378739 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.990267 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 73
- train_seconds: 347.7

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 16 | 0.6875 | 0.5579 |
| [0.60,0.70) | 25 | 0.4800 | 0.6536 |
| [0.70,0.80) | 38 | 0.4474 | 0.7611 |
| [0.80,0.90) | 56 | 0.4821 | 0.8493 |
| [0.90,1.00) | 3467 | 0.0176 | 0.9977 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 540 | 0.5815 | 0.5293 |
| [0.60,0.70) | 380 | 0.5474 | 0.6530 |
| [0.70,0.80) | 398 | 0.5352 | 0.7526 |
| [0.80,0.90) | 540 | 0.4574 | 0.8527 |
| [0.90,1.00) | 1744 | 0.2947 | 0.9723 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.5142

## 验证集最佳点

```json
{
  "loss_total": 0.563678413589204,
  "acc_main": 0.9491204330175913,
  "acc_turn": 0.6476319350473613,
  "acc_turn_pure": 0.6627335299901671,
  "acc_turn_transition": 0.5760869565217391,
  "false_turn_straight": 0.3903326403326403,
  "flat_recall": 0.9573820395738204,
  "stall_recall": 0.47619047619047616,
  "slope_recall": 0.9539385847797063,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9573820395738204,
    0.47619047619047616,
    0.9539385847797063
  ],
  "turn_right_recall": 0.6800947867298578,
  "turn_straight_recall": 0.6096673596673596,
  "turn_left_recall": 0.6968716289104638,
  "recall_turn": [
    0.6800947867298578,
    0.6096673596673596,
    0.6968716289104638
  ],
  "cm_turn": [
    [
      574,
      229,
      41
    ],
    [
      386,
      1173,
      365
    ],
    [
      100,
      181,
      646
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
      20,
      22
    ],
    [
      131,
      7,
      2858
    ]
  ],
  "main_confidence_mean": 0.9677567990710487,
  "main_confidence_error_mean": 0.7534238821561093,
  "main_low_conf_0p60_ratio": 0.050608930987821384,
  "main_low_conf_0p70_ratio": 0.05737483085250338,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 187,
      "error_rate": 0.44919786096256686,
      "mean_confidence": 0.5202352197712067
    },
    {
      "bin": "[0.60,0.70)",
      "n": 25,
      "error_rate": 0.2,
      "mean_confidence": 0.646741469180549
    },
    {
      "bin": "[0.70,0.80)",
      "n": 22,
      "error_rate": 0.18181818181818182,
      "mean_confidence": 0.7554398415257834
    },
    {
      "bin": "[0.80,0.90)",
      "n": 52,
      "error_rate": 0.2692307692307692,
      "mean_confidence": 0.8514120615944611
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3409,
      "error_rate": 0.02376063361689645,
      "mean_confidence": 0.9978045602887404
    }
  ],
  "turn_confidence_mean": 0.8345630495655094,
  "turn_confidence_error_mean": 0.760996572727072,
  "turn_low_conf_0p60_ratio": 0.15859269282814614,
  "turn_low_conf_0p70_ratio": 0.25358592692828147,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 586,
      "error_rate": 0.6006825938566553,
      "mean_confidence": 0.5063614570593811
    },
    {
      "bin": "[0.60,0.70)",
      "n": 351,
      "error_rate": 0.47293447293447294,
      "mean_confidence": 0.6538972166574143
    },
    {
      "bin": "[0.70,0.80)",
      "n": 356,
      "error_rate": 0.4353932584269663,
      "mean_confidence": 0.749089487648614
    },
    {
      "bin": "[0.80,0.90)",
      "n": 430,
      "error_rate": 0.39767441860465114,
      "mean_confidence": 0.8514056002277001
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1972,
      "error_rate": 0.23225152129817445,
      "mean_confidence": 0.9760063212779865
    }
  ],
  "theta_mae_rad": 0.014420152641832829,
  "theta_mae_deg": 0.8262138366699219,
  "uphill_recall": 0.783288409703504,
  "downhill_recall": 0.7969966629588432,
  "slope_sign_acc": 0.9616753353408157,
  "theta_flat_mae_deg": 1.237909197807312,
  "theta_flat_abs_p95_deg": 4.507064342498779,
  "theta_flat_abs_max_deg": 7.6228928565979,
  "theta_flat_bias_deg": 0.3790377378463745,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.6489564180374146,
  "theta_near_flat_abs_p95_deg": 4.50712776184082,
  "theta_near_flat_abs_max_deg": 7.6228928565979,
  "theta_near_flat_bias_deg": 0.7326490879058838,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.194649338722229,
  "theta_flat_turn_abs_p95_deg": 4.507064342498779,
  "theta_flat_turn_abs_max_deg": 7.6228928565979,
  "theta_flat_turn_bias_deg": 0.357902854681015,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8262138366699219,
  "theta_slope_control_abs_p95_deg": 9.256318092346191,
  "theta_slope_control_abs_max_deg": 11.620041847229004,
  "theta_slope_control_bias_deg": 0.08106184005737305,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8262138366699219,
  "theta_all_rmse_deg": 1.2458640336990356,
  "theta_all_p95_abs_err_deg": 2.831678628921509,
  "theta_all_max_abs_err_deg": 8.122892379760742,
  "theta_all_bias_deg": 0.08106184005737305,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7359321713447571,
  "theta_active_abs_ge_2_rmse_deg": 1.0691765546798706,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.1406896114349365,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.268726825714111,
  "theta_active_abs_ge_2_bias_deg": 0.01571798324584961,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8614633679389954,
  "theta_abs_le_8_rmse_deg": 1.292937994003296,
  "theta_abs_le_8_p95_abs_err_deg": 3.0070645809173584,
  "theta_abs_le_8_max_abs_err_deg": 8.122892379760742,
  "theta_abs_le_8_bias_deg": 0.09502874314785004,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8262138366699219,
  "theta_abs_le_10_rmse_deg": 1.2458640336990356,
  "theta_abs_le_10_p95_abs_err_deg": 2.831678628921509,
  "theta_abs_le_10_max_abs_err_deg": 8.122892379760742,
  "theta_abs_le_10_bias_deg": 0.08106184005737305,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6055507659912109,
  "theta_pos_8_10_rmse_deg": 0.7961945533752441,
  "theta_pos_8_10_p95_abs_err_deg": 1.3909310102462769,
  "theta_pos_8_10_max_abs_err_deg": 4.617537498474121,
  "theta_pos_8_10_bias_deg": -0.25004228949546814,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7507151961326599,
  "theta_neg_10_8_rmse_deg": 1.2121272087097168,
  "theta_neg_10_8_p95_abs_err_deg": 1.8331981897354126,
  "theta_neg_10_8_max_abs_err_deg": 6.811762809753418,
  "theta_neg_10_8_bias_deg": 0.299031525850296,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6474816203117371,
  "theta_pos_6_8_rmse_deg": 0.8901211023330688,
  "theta_pos_6_8_p95_abs_err_deg": 1.6818773746490479,
  "theta_pos_6_8_max_abs_err_deg": 4.0119147300720215,
  "theta_pos_6_8_bias_deg": -0.19072310626506805,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.6603254079818726,
  "theta_neg_8_6_rmse_deg": 1.0196048021316528,
  "theta_neg_8_6_p95_abs_err_deg": 1.8933817148208618,
  "theta_neg_8_6_max_abs_err_deg": 6.194214344024658,
  "theta_neg_8_6_bias_deg": -0.06995758414268494,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7227379083633423,
  "theta_neg_4_2_rmse_deg": 1.0207089185714722,
  "theta_neg_4_2_p95_abs_err_deg": 2.2093513011932373,
  "theta_neg_4_2_max_abs_err_deg": 6.378983020782471,
  "theta_neg_4_2_bias_deg": -0.00808024127036333,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.8031630516052246,
  "theta_neg_2_0p5_rmse_deg": 1.052079439163208,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.9906845092773438,
  "theta_neg_2_0p5_max_abs_err_deg": 4.637040138244629,
  "theta_neg_2_0p5_bias_deg": -0.050700776278972626,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1778173446655273,
  "theta_pos_0p5_2_rmse_deg": 1.68305504322052,
  "theta_pos_0p5_2_p95_abs_err_deg": 3.0070645809173584,
  "theta_pos_0p5_2_max_abs_err_deg": 5.36268424987793,
  "theta_pos_0p5_2_bias_deg": 0.4903686046600342,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2854807756024543,
  "loss_turn": 1.389502790203275,
  "loss_theta": 0.00047261814329412755,
  "loss_main_bundle_base": 0.2854807756024543,
  "loss_turn_bundle_base": 0.2779005620532817,
  "loss_theta_bundle_base": 0.00029705934467062566,
  "loss_main_bundle": 0.2854807756024543,
  "loss_turn_bundle": 0.2779005620532817,
  "loss_theta_bundle": 0.00029705934467062566,
  "loss_theta_flat": 0.0003377111401255791,
  "loss_theta_near_flat": 0.0016563875061624933,
  "loss_theta_error_excess": 0.00018369778449233137,
  "loss_theta_flat_excess": 0.00018238787844046794,
  "loss_theta_near_flat_excess": 0.0012251837809818403,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00011040044556443072,
  "loss_theta_small_neg": 0.0003140074602710726,
  "loss_theta_small_neg_excess": 8.600782038375681e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3688582736035968,
  "loss_false_turn_straight": 0.28739893742923966,
  "loss_transition_focal_raw": 1.2711207005103322,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.4589430935741583,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
