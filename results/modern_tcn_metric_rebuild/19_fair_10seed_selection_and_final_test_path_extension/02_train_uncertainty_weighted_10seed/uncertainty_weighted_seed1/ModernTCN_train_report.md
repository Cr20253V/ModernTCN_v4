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
| acc_main | 0.9653 |
| acc_turn | 0.5316 |
| acc_turn_pure | 0.5462 |
| acc_turn_transition | 0.4680 |
| main_confidence_mean | 0.9833 |
| main_low_conf_0p60_ratio | 0.0072 |
| main_low_conf_0p70_ratio | 0.0197 |
| turn_confidence_mean | 0.7414 |
| turn_low_conf_0p60_ratio | 0.2723 |
| turn_low_conf_0p70_ratio | 0.4217 |
| turn_right_recall | 0.6796 |
| turn_straight_recall | 0.4366 |
| turn_left_recall | 0.6069 |
| theta_mae_deg | 1.0169 |
| theta_abs_le_10_p95_abs_err_deg | 2.6660 |
| theta_neg_10_8_p95_abs_err_deg | 2.0702 |
| theta_pos_8_10_p95_abs_err_deg | 4.1802 |
| theta_abs_le_8_p95_abs_err_deg | 2.6438 |
| theta_neg_8_6_p95_abs_err_deg | 2.5094 |
| theta_pos_6_8_p95_abs_err_deg | 2.3181 |
| theta_neg_2_0p5_p95_abs_err_deg | 3.0922 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.7432 |
| theta_flat_abs_p95_deg | 3.7745 |
| theta_flat_bias_deg | -0.6221 |
| theta_near_flat_abs_p95_deg | 2.9834 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.4425 |
| theta_flat_turn_abs_p95_deg | 2.5904 |
| flat_recall | 0.9722 |
| stall_recall | 0.6562 |
| slope_recall | 0.9742 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7489 |
| downhill_recall | 0.7911 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    735,
    0,
    21
  ],
  [
    10,
    63,
    23
  ],
  [
    64,
    7,
    2679
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    543,
    116,
    140
  ],
  [
    545,
    844,
    544
  ],
  [
    208,
    134,
    528
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.287443 |
| test_loss_turn_bundle_base | 0.246835 |
| test_loss_theta_bundle_base | 0.000408 |
| test_loss_transition_focal_raw | 0.952270 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.194951 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 34
- train_seconds: 193.5

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 26 | 0.3846 | 0.5532 |
| [0.60,0.70) | 45 | 0.4889 | 0.6462 |
| [0.70,0.80) | 37 | 0.2703 | 0.7489 |
| [0.80,0.90) | 71 | 0.2535 | 0.8604 |
| [0.90,1.00) | 3423 | 0.0190 | 0.9961 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 981 | 0.5872 | 0.4969 |
| [0.60,0.70) | 538 | 0.5558 | 0.6478 |
| [0.70,0.80) | 504 | 0.5595 | 0.7494 |
| [0.80,0.90) | 583 | 0.4117 | 0.8511 |
| [0.90,1.00) | 996 | 0.2912 | 0.9643 |


## 验证集最佳点

```json
{
  "loss_total": 0.5359962753094581,
  "acc_main": 0.945872801082544,
  "acc_turn": 0.5751014884979703,
  "acc_turn_pure": 0.5834152736807604,
  "acc_turn_transition": 0.5357142857142857,
  "false_turn_straight": 0.5228690228690228,
  "flat_recall": 0.954337899543379,
  "stall_recall": 0.47619047619047616,
  "slope_recall": 0.9506008010680908,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.09523809523809523,
  "recall_main": [
    0.954337899543379,
    0.47619047619047616,
    0.9506008010680908
  ],
  "turn_right_recall": 0.6409952606635071,
  "turn_straight_recall": 0.47713097713097713,
  "turn_left_recall": 0.7184466019417476,
  "recall_turn": [
    0.6409952606635071,
    0.47713097713097713,
    0.7184466019417476
  ],
  "cm_turn": [
    [
      541,
      187,
      116
    ],
    [
      427,
      918,
      579
    ],
    [
      96,
      165,
      666
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
      4,
      20,
      18
    ],
    [
      144,
      4,
      2848
    ]
  ],
  "main_confidence_mean": 0.9761279174169583,
  "main_confidence_error_mean": 0.851821170488896,
  "main_low_conf_0p60_ratio": 0.006495263870094722,
  "main_low_conf_0p70_ratio": 0.011907983761840324,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 24,
      "error_rate": 0.25,
      "mean_confidence": 0.5492501955116421
    },
    {
      "bin": "[0.60,0.70)",
      "n": 20,
      "error_rate": 0.55,
      "mean_confidence": 0.6504464414801795
    },
    {
      "bin": "[0.70,0.80)",
      "n": 208,
      "error_rate": 0.42788461538461536,
      "mean_confidence": 0.77830505090759
    },
    {
      "bin": "[0.80,0.90)",
      "n": 77,
      "error_rate": 0.19480519480519481,
      "mean_confidence": 0.8511543325483628
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3366,
      "error_rate": 0.023469994058229353,
      "mean_confidence": 0.996189954586683
    }
  ],
  "turn_confidence_mean": 0.7579190880160659,
  "turn_confidence_error_mean": 0.6869228176282046,
  "turn_low_conf_0p60_ratio": 0.26008119079837616,
  "turn_low_conf_0p70_ratio": 0.3916102841677943,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 961,
      "error_rate": 0.6160249739854319,
      "mean_confidence": 0.48991692181645846
    },
    {
      "bin": "[0.60,0.70)",
      "n": 486,
      "error_rate": 0.5267489711934157,
      "mean_confidence": 0.6504234989155118
    },
    {
      "bin": "[0.70,0.80)",
      "n": 466,
      "error_rate": 0.43991416309012876,
      "mean_confidence": 0.7509402294130098
    },
    {
      "bin": "[0.80,0.90)",
      "n": 516,
      "error_rate": 0.42248062015503873,
      "mean_confidence": 0.8512403745266771
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1266,
      "error_rate": 0.23617693522906794,
      "mean_confidence": 0.9671539239483257
    }
  ],
  "theta_mae_rad": 0.020183343440294266,
  "theta_mae_deg": 1.156420350074768,
  "uphill_recall": 0.783288409703504,
  "downhill_recall": 0.7925472747497219,
  "slope_sign_acc": 0.9556528880372297,
  "theta_flat_mae_deg": 1.450577735900879,
  "theta_flat_abs_p95_deg": 3.604654312133789,
  "theta_flat_abs_max_deg": 10.471400260925293,
  "theta_flat_bias_deg": -0.13220825791358948,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.8141369819641113,
  "theta_near_flat_abs_p95_deg": 4.948474884033203,
  "theta_near_flat_abs_max_deg": 10.471400260925293,
  "theta_near_flat_bias_deg": 0.33174288272857666,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.80802583694458,
  "theta_flat_turn_abs_p95_deg": 5.973779678344727,
  "theta_flat_turn_abs_max_deg": 10.471400260925293,
  "theta_flat_turn_bias_deg": 0.1442759484052658,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 1.156420350074768,
  "theta_slope_control_abs_p95_deg": 9.886992454528809,
  "theta_slope_control_abs_max_deg": 12.833463668823242,
  "theta_slope_control_bias_deg": -0.421548455953598,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 1.1564202308654785,
  "theta_all_rmse_deg": 1.577310562133789,
  "theta_all_p95_abs_err_deg": 2.926445245742798,
  "theta_all_max_abs_err_deg": 10.971399307250977,
  "theta_all_bias_deg": -0.42154842615127563,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 1.0919139385223389,
  "theta_active_abs_ge_2_rmse_deg": 1.4780209064483643,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.7999494075775146,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.13219690322876,
  "theta_active_abs_ge_2_bias_deg": -0.48499855399131775,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 1.153598666191101,
  "theta_abs_le_8_rmse_deg": 1.6052707433700562,
  "theta_abs_le_8_p95_abs_err_deg": 2.95890212059021,
  "theta_abs_le_8_max_abs_err_deg": 10.971399307250977,
  "theta_abs_le_8_bias_deg": -0.34851717948913574,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 1.1564202308654785,
  "theta_abs_le_10_rmse_deg": 1.577310562133789,
  "theta_abs_le_10_p95_abs_err_deg": 2.926445245742798,
  "theta_abs_le_10_max_abs_err_deg": 10.971399307250977,
  "theta_abs_le_10_bias_deg": -0.42154842615127563,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 1.1009060144424438,
  "theta_pos_8_10_rmse_deg": 1.3749423027038574,
  "theta_pos_8_10_p95_abs_err_deg": 2.304974317550659,
  "theta_pos_8_10_max_abs_err_deg": 6.250238418579102,
  "theta_pos_8_10_bias_deg": -0.8171952366828918,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 1.2369071245193481,
  "theta_neg_10_8_rmse_deg": 1.5291845798492432,
  "theta_neg_10_8_p95_abs_err_deg": 3.1920478343963623,
  "theta_neg_10_8_max_abs_err_deg": 5.743319988250732,
  "theta_neg_10_8_bias_deg": -0.6405627131462097,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.8591670989990234,
  "theta_pos_6_8_rmse_deg": 1.0985993146896362,
  "theta_pos_6_8_p95_abs_err_deg": 2.362233877182007,
  "theta_pos_6_8_max_abs_err_deg": 4.098663330078125,
  "theta_pos_6_8_bias_deg": -0.23786771297454834,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.177004098892212,
  "theta_neg_8_6_rmse_deg": 1.5494823455810547,
  "theta_neg_8_6_p95_abs_err_deg": 2.8815758228302,
  "theta_neg_8_6_max_abs_err_deg": 6.414639472961426,
  "theta_neg_8_6_bias_deg": -0.7702455520629883,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 1.1263580322265625,
  "theta_neg_4_2_rmse_deg": 1.575143814086914,
  "theta_neg_4_2_p95_abs_err_deg": 3.2149295806884766,
  "theta_neg_4_2_max_abs_err_deg": 7.13219690322876,
  "theta_neg_4_2_bias_deg": -0.523622989654541,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 1.1646169424057007,
  "theta_neg_2_0p5_rmse_deg": 1.4152414798736572,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.5943076610565186,
  "theta_neg_2_0p5_max_abs_err_deg": 4.139870643615723,
  "theta_neg_2_0p5_bias_deg": -0.9096865057945251,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.23056161403656,
  "theta_pos_0p5_2_rmse_deg": 1.6187262535095215,
  "theta_pos_0p5_2_p95_abs_err_deg": 3.1595423221588135,
  "theta_pos_0p5_2_max_abs_err_deg": 6.119924545288086,
  "theta_pos_0p5_2_bias_deg": 0.11719032377004623,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3007360254718099,
  "loss_turn": 1.1736556073164262,
  "loss_theta": 0.0007579291510964077,
  "loss_main_bundle_base": 0.3007360254718099,
  "loss_turn_bundle_base": 0.2347311233837001,
  "loss_theta_bundle_base": 0.0005291300372715853,
  "loss_main_bundle": 0.3007360254718099,
  "loss_turn_bundle": 0.2347311233837001,
  "loss_theta_bundle": 0.0005291300372715853,
  "loss_theta_flat": 0.0006068844321254434,
  "loss_theta_near_flat": 0.0017432216271324554,
  "loss_theta_error_excess": 0.0003006826468295366,
  "loss_theta_flat_excess": 0.00031787364993966533,
  "loss_theta_near_flat_excess": 0.0012673346290783263,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00024408739041574854,
  "loss_theta_small_neg": 0.0007598673177477229,
  "loss_theta_small_neg_excess": 0.00031125039537720814,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4514789877789592,
  "loss_false_turn_straight": 0.35362395842601224,
  "loss_transition_focal_raw": 0.791182511246414,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.9711128840829075,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
