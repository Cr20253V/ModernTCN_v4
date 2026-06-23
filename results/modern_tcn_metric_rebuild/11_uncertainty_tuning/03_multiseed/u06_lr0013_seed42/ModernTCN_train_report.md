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
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9578 |
| acc_turn | 0.6027 |
| acc_turn_pure | 0.6131 |
| acc_turn_transition | 0.5574 |
| main_confidence_mean | 0.9897 |
| main_low_conf_0p60_ratio | 0.0044 |
| main_low_conf_0p70_ratio | 0.0114 |
| turn_confidence_mean | 0.8415 |
| turn_low_conf_0p60_ratio | 0.1385 |
| turn_low_conf_0p70_ratio | 0.2421 |
| turn_right_recall | 0.6070 |
| turn_straight_recall | 0.6425 |
| turn_left_recall | 0.5103 |
| theta_mae_deg | 0.6141 |
| theta_abs_le_10_p95_abs_err_deg | 1.6320 |
| theta_neg_10_8_p95_abs_err_deg | 1.4968 |
| theta_pos_8_10_p95_abs_err_deg | 2.4889 |
| theta_abs_le_8_p95_abs_err_deg | 1.5800 |
| theta_neg_8_6_p95_abs_err_deg | 1.7883 |
| theta_pos_6_8_p95_abs_err_deg | 1.4530 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.3460 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4237 |
| theta_flat_abs_p95_deg | 2.6960 |
| theta_flat_bias_deg | 0.3113 |
| theta_near_flat_abs_p95_deg | 2.0396 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.3553 |
| theta_flat_turn_abs_p95_deg | 1.5280 |
| flat_recall | 0.9405 |
| stall_recall | 0.6250 |
| slope_recall | 0.9742 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7489 |
| downhill_recall | 0.8048 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    711,
    0,
    45
  ],
  [
    10,
    60,
    26
  ],
  [
    63,
    8,
    2679
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    485,
    208,
    106
  ],
  [
    359,
    1242,
    332
  ],
  [
    156,
    270,
    444
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.377942 |
| test_loss_turn_bundle_base | 0.347204 |
| test_loss_theta_bundle_base | 0.000144 |
| test_loss_transition_focal_raw | 1.557249 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.953763 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 81
- train_seconds: 375.2

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 16 | 0.5625 | 0.5490 |
| [0.60,0.70) | 25 | 0.4800 | 0.6518 |
| [0.70,0.80) | 26 | 0.6923 | 0.7403 |
| [0.80,0.90) | 46 | 0.5652 | 0.8386 |
| [0.90,1.00) | 3489 | 0.0249 | 0.9980 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 499 | 0.5571 | 0.5190 |
| [0.60,0.70) | 373 | 0.5362 | 0.6504 |
| [0.70,0.80) | 376 | 0.5372 | 0.7504 |
| [0.80,0.90) | 459 | 0.4619 | 0.8525 |
| [0.90,1.00) | 1895 | 0.2844 | 0.9795 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.5574

## 验证集最佳点

```json
{
  "loss_total": 0.591029730056071,
  "acc_main": 0.945872801082544,
  "acc_turn": 0.6433017591339648,
  "acc_turn_pure": 0.6496230744018354,
  "acc_turn_transition": 0.6133540372670807,
  "false_turn_straight": 0.3633056133056133,
  "flat_recall": 0.9665144596651446,
  "stall_recall": 0.35714285714285715,
  "slope_recall": 0.9495994659546061,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9665144596651446,
    0.35714285714285715,
    0.9495994659546061
  ],
  "turn_right_recall": 0.6469194312796208,
  "turn_straight_recall": 0.6366943866943867,
  "turn_left_recall": 0.6537216828478964,
  "recall_turn": [
    0.6469194312796208,
    0.6366943866943867,
    0.6537216828478964
  ],
  "cm_turn": [
    [
      546,
      219,
      79
    ],
    [
      322,
      1225,
      377
    ],
    [
      72,
      249,
      606
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      635,
      0,
      22
    ],
    [
      0,
      15,
      27
    ],
    [
      141,
      10,
      2845
    ]
  ],
  "main_confidence_mean": 0.97110474233579,
  "main_confidence_error_mean": 0.7718289919438546,
  "main_low_conf_0p60_ratio": 0.05115020297699594,
  "main_low_conf_0p70_ratio": 0.056562922868741546,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 189,
      "error_rate": 0.4656084656084656,
      "mean_confidence": 0.5540838318651474
    },
    {
      "bin": "[0.60,0.70)",
      "n": 20,
      "error_rate": 0.35,
      "mean_confidence": 0.6548994065287419
    },
    {
      "bin": "[0.70,0.80)",
      "n": 15,
      "error_rate": 0.4,
      "mean_confidence": 0.7588344821571973
    },
    {
      "bin": "[0.80,0.90)",
      "n": 38,
      "error_rate": 0.21052631578947367,
      "mean_confidence": 0.8609623215919623
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3433,
      "error_rate": 0.026507427905621904,
      "mean_confidence": 0.9980521716064095
    }
  ],
  "turn_confidence_mean": 0.8489655719626604,
  "turn_confidence_error_mean": 0.7655828186934982,
  "turn_low_conf_0p60_ratio": 0.14506089309878215,
  "turn_low_conf_0p70_ratio": 0.227063599458728,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 536,
      "error_rate": 0.628731343283582,
      "mean_confidence": 0.49777949141844613
    },
    {
      "bin": "[0.60,0.70)",
      "n": 303,
      "error_rate": 0.5214521452145214,
      "mean_confidence": 0.6496137167547071
    },
    {
      "bin": "[0.70,0.80)",
      "n": 340,
      "error_rate": 0.5029411764705882,
      "mean_confidence": 0.7517209315893509
    },
    {
      "bin": "[0.80,0.90)",
      "n": 402,
      "error_rate": 0.4079601990049751,
      "mean_confidence": 0.8548629725151039
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2114,
      "error_rate": 0.23084200567644275,
      "mean_confidence": 0.9810998075371883
    }
  ],
  "theta_mae_rad": 0.013396315276622772,
  "theta_mae_deg": 0.7675522565841675,
  "uphill_recall": 0.7730458221024259,
  "downhill_recall": 0.7969966629588432,
  "slope_sign_acc": 0.9718039967150287,
  "theta_flat_mae_deg": 1.1096588373184204,
  "theta_flat_abs_p95_deg": 4.1846842765808105,
  "theta_flat_abs_max_deg": 6.842155933380127,
  "theta_flat_bias_deg": 0.8833543062210083,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.485298991203308,
  "theta_near_flat_abs_p95_deg": 4.185190200805664,
  "theta_near_flat_abs_max_deg": 6.842155933380127,
  "theta_near_flat_bias_deg": 1.3388097286224365,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.072026252746582,
  "theta_flat_turn_abs_p95_deg": 4.1846842765808105,
  "theta_flat_turn_abs_max_deg": 6.842155933380127,
  "theta_flat_turn_bias_deg": 0.9288344979286194,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7675522565841675,
  "theta_slope_control_abs_p95_deg": 9.611809730529785,
  "theta_slope_control_abs_max_deg": 11.618972778320312,
  "theta_slope_control_bias_deg": 0.023185480386018753,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7675523161888123,
  "theta_all_rmse_deg": 1.192342758178711,
  "theta_all_p95_abs_err_deg": 2.6846842765808105,
  "theta_all_max_abs_err_deg": 7.342155933380127,
  "theta_all_bias_deg": 0.023185476660728455,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6925309300422668,
  "theta_active_abs_ge_2_rmse_deg": 1.041757345199585,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.9938268661499023,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.822197437286377,
  "theta_active_abs_ge_2_bias_deg": -0.16544300317764282,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7917475700378418,
  "theta_abs_le_8_rmse_deg": 1.2294690608978271,
  "theta_abs_le_8_p95_abs_err_deg": 2.6846842765808105,
  "theta_abs_le_8_max_abs_err_deg": 7.342155933380127,
  "theta_abs_le_8_bias_deg": 0.10199519246816635,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7675523161888123,
  "theta_abs_le_10_rmse_deg": 1.192342758178711,
  "theta_abs_le_10_p95_abs_err_deg": 2.6846842765808105,
  "theta_abs_le_10_max_abs_err_deg": 7.342155933380127,
  "theta_abs_le_10_bias_deg": 0.023185476660728455,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.525012195110321,
  "theta_pos_8_10_rmse_deg": 0.7552980780601501,
  "theta_pos_8_10_p95_abs_err_deg": 1.5425375699996948,
  "theta_pos_8_10_max_abs_err_deg": 4.681801795959473,
  "theta_pos_8_10_bias_deg": -0.2584642767906189,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8083823323249817,
  "theta_neg_10_8_rmse_deg": 1.233871579170227,
  "theta_neg_10_8_p95_abs_err_deg": 1.9527744054794312,
  "theta_neg_10_8_max_abs_err_deg": 6.822197437286377,
  "theta_neg_10_8_bias_deg": -0.36097219586372375,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5667986273765564,
  "theta_pos_6_8_rmse_deg": 0.8048161268234253,
  "theta_pos_6_8_p95_abs_err_deg": 1.6633596420288086,
  "theta_pos_6_8_max_abs_err_deg": 3.5472662448883057,
  "theta_pos_6_8_bias_deg": -0.11035295575857162,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8105185031890869,
  "theta_neg_8_6_rmse_deg": 1.1398857831954956,
  "theta_neg_8_6_p95_abs_err_deg": 2.0341508388519287,
  "theta_neg_8_6_max_abs_err_deg": 6.154580593109131,
  "theta_neg_8_6_bias_deg": -0.3329213261604309,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.721074104309082,
  "theta_neg_4_2_rmse_deg": 1.1009299755096436,
  "theta_neg_4_2_p95_abs_err_deg": 2.048342704772949,
  "theta_neg_4_2_max_abs_err_deg": 6.743669033050537,
  "theta_neg_4_2_bias_deg": -0.2734954357147217,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.4785846769809723,
  "theta_neg_2_0p5_rmse_deg": 0.7206910252571106,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.1383371353149414,
  "theta_neg_2_0p5_max_abs_err_deg": 4.690512657165527,
  "theta_neg_2_0p5_bias_deg": 0.11688822507858276,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.3759310245513916,
  "theta_pos_0p5_2_rmse_deg": 1.7265225648880005,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.6846842765808105,
  "theta_pos_0p5_2_max_abs_err_deg": 4.6799635887146,
  "theta_pos_0p5_2_bias_deg": 1.1601297855377197,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2853506553076278,
  "loss_turn": 1.5269748343505136,
  "loss_theta": 0.0004329511514708591,
  "loss_main_bundle_base": 0.2853506553076278,
  "loss_turn_bundle_base": 0.30539497203207466,
  "loss_theta_bundle_base": 0.0002841025940378868,
  "loss_main_bundle": 0.2853506553076278,
  "loss_turn_bundle": 0.30539497203207466,
  "loss_theta_bundle": 0.0002841025940378868,
  "loss_theta_flat": 0.00022517275774269521,
  "loss_theta_near_flat": 0.0014054711684723246,
  "loss_theta_error_excess": 0.00016583876689585337,
  "loss_theta_flat_excess": 0.00013268400363629587,
  "loss_theta_near_flat_excess": 0.0010350086171109435,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010666791664514279,
  "loss_theta_small_neg": 0.00036425783503069687,
  "loss_theta_small_neg_excess": 0.00012523893486514323,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.31323580100668624,
  "loss_false_turn_straight": 0.26373594121778127,
  "loss_transition_focal_raw": 1.310829484253033,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.327641287394604,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
