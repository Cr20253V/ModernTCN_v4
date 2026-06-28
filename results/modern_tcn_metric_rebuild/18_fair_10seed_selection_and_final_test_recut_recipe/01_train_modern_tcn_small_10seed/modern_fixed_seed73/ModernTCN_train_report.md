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
| acc_turn | 0.5805 |
| acc_turn_pure | 0.5875 |
| acc_turn_transition | 0.5499 |
| main_confidence_mean | 0.9904 |
| main_low_conf_0p60_ratio | 0.0047 |
| main_low_conf_0p70_ratio | 0.0128 |
| turn_confidence_mean | 0.8458 |
| turn_low_conf_0p60_ratio | 0.1371 |
| turn_low_conf_0p70_ratio | 0.2363 |
| turn_right_recall | 0.6195 |
| turn_straight_recall | 0.5644 |
| turn_left_recall | 0.5805 |
| theta_mae_deg | 0.5875 |
| theta_abs_le_10_p95_abs_err_deg | 1.6343 |
| theta_neg_10_8_p95_abs_err_deg | 1.5858 |
| theta_pos_8_10_p95_abs_err_deg | 3.1634 |
| theta_abs_le_8_p95_abs_err_deg | 1.5772 |
| theta_neg_8_6_p95_abs_err_deg | 1.5852 |
| theta_pos_6_8_p95_abs_err_deg | 1.1576 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.9726 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.6178 |
| theta_flat_abs_p95_deg | 2.9290 |
| theta_flat_bias_deg | -0.2440 |
| theta_near_flat_abs_p95_deg | 1.9419 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.0495 |
| theta_flat_turn_abs_p95_deg | 1.5304 |
| flat_recall | 0.9484 |
| stall_recall | 0.6250 |
| slope_recall | 0.9818 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1146 |
| uphill_recall | 0.7615 |
| downhill_recall | 0.8008 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    717,
    0,
    39
  ],
  [
    11,
    60,
    25
  ],
  [
    44,
    6,
    2700
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    495,
    162,
    142
  ],
  [
    378,
    1091,
    464
  ],
  [
    176,
    189,
    505
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.455570 |
| test_loss_turn_bundle_base | 0.382173 |
| test_loss_theta_bundle_base | 0.000154 |
| test_loss_transition_focal_raw | 1.604371 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 5.375789 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 82
- train_seconds: 373.7

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 17 | 0.5294 | 0.5516 |
| [0.60,0.70) | 29 | 0.1724 | 0.6676 |
| [0.70,0.80) | 23 | 0.5217 | 0.7402 |
| [0.80,0.90) | 35 | 0.1714 | 0.8565 |
| [0.90,1.00) | 3498 | 0.0266 | 0.9982 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 494 | 0.5607 | 0.5195 |
| [0.60,0.70) | 357 | 0.5574 | 0.6498 |
| [0.70,0.80) | 360 | 0.5028 | 0.7503 |
| [0.80,0.90) | 399 | 0.5013 | 0.8541 |
| [0.90,1.00) | 1992 | 0.3283 | 0.9775 |


## 验证集最佳点

```json
{
  "loss_total": 0.6231366138658279,
  "acc_main": 0.9453315290933694,
  "acc_turn": 0.6359945872801083,
  "acc_turn_pure": 0.647984267453294,
  "acc_turn_transition": 0.5791925465838509,
  "false_turn_straight": 0.42775467775467774,
  "flat_recall": 0.9467275494672754,
  "stall_recall": 0.30952380952380953,
  "slope_recall": 0.9539385847797063,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.023809523809523808,
  "recall_main": [
    0.9467275494672754,
    0.30952380952380953,
    0.9539385847797063
  ],
  "turn_right_recall": 0.6706161137440758,
  "turn_straight_recall": 0.5722453222453222,
  "turn_left_recall": 0.7367853290183387,
  "recall_turn": [
    0.6706161137440758,
    0.5722453222453222,
    0.7367853290183387
  ],
  "cm_turn": [
    [
      566,
      188,
      90
    ],
    [
      361,
      1101,
      462
    ],
    [
      78,
      166,
      683
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
      1,
      13,
      28
    ],
    [
      130,
      8,
      2858
    ]
  ],
  "main_confidence_mean": 0.9707768804132805,
  "main_confidence_error_mean": 0.7443207352704643,
  "main_low_conf_0p60_ratio": 0.047631935047361296,
  "main_low_conf_0p70_ratio": 0.052232746955345064,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 176,
      "error_rate": 0.4715909090909091,
      "mean_confidence": 0.5118365911029094
    },
    {
      "bin": "[0.60,0.70)",
      "n": 17,
      "error_rate": 0.5882352941176471,
      "mean_confidence": 0.6549457808505209
    },
    {
      "bin": "[0.70,0.80)",
      "n": 25,
      "error_rate": 0.6,
      "mean_confidence": 0.7577194605728391
    },
    {
      "bin": "[0.80,0.90)",
      "n": 30,
      "error_rate": 0.6,
      "mean_confidence": 0.8584332249695418
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3447,
      "error_rate": 0.022048157818392804,
      "mean_confidence": 0.9982904762271809
    }
  ],
  "turn_confidence_mean": 0.8597853510504113,
  "turn_confidence_error_mean": 0.7833498186733483,
  "turn_low_conf_0p60_ratio": 0.13234100135317997,
  "turn_low_conf_0p70_ratio": 0.20757780784844385,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 489,
      "error_rate": 0.6482617586912065,
      "mean_confidence": 0.5102902595696648
    },
    {
      "bin": "[0.60,0.70)",
      "n": 278,
      "error_rate": 0.5251798561151079,
      "mean_confidence": 0.6479791121726282
    },
    {
      "bin": "[0.70,0.80)",
      "n": 292,
      "error_rate": 0.5205479452054794,
      "mean_confidence": 0.748232694029205
    },
    {
      "bin": "[0.80,0.90)",
      "n": 451,
      "error_rate": 0.44124168514412415,
      "mean_confidence": 0.8554366292872293
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2185,
      "error_rate": 0.24302059496567505,
      "mean_confidence": 0.9807555494520114
    }
  ],
  "theta_mae_rad": 0.012763405218720436,
  "theta_mae_deg": 0.7312892079353333,
  "uphill_recall": 0.7789757412398922,
  "downhill_recall": 0.8053392658509455,
  "slope_sign_acc": 0.9756364631809472,
  "theta_flat_mae_deg": 1.0270323753356934,
  "theta_flat_abs_p95_deg": 3.8400073051452637,
  "theta_flat_abs_max_deg": 8.2593994140625,
  "theta_flat_bias_deg": 0.4137454330921173,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4343992471694946,
  "theta_near_flat_abs_p95_deg": 3.9797303676605225,
  "theta_near_flat_abs_max_deg": 8.2593994140625,
  "theta_near_flat_bias_deg": 0.9126912355422974,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.2295503616333008,
  "theta_flat_turn_abs_p95_deg": 4.108893871307373,
  "theta_flat_turn_abs_max_deg": 8.2593994140625,
  "theta_flat_turn_bias_deg": 0.5632764101028442,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7312892079353333,
  "theta_slope_control_abs_p95_deg": 9.326393127441406,
  "theta_slope_control_abs_max_deg": 12.139118194580078,
  "theta_slope_control_bias_deg": 0.05368444696068764,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7312892079353333,
  "theta_all_rmse_deg": 1.1489930152893066,
  "theta_all_p95_abs_err_deg": 2.4380884170532227,
  "theta_all_max_abs_err_deg": 8.759398460388184,
  "theta_all_bias_deg": 0.05368444696068764,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6664349436759949,
  "theta_active_abs_ge_2_rmse_deg": 1.010845422744751,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.9679830074310303,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.853987216949463,
  "theta_active_abs_ge_2_bias_deg": -0.025274178013205528,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.745374321937561,
  "theta_abs_le_8_rmse_deg": 1.164177656173706,
  "theta_abs_le_8_p95_abs_err_deg": 2.514958381652832,
  "theta_abs_le_8_max_abs_err_deg": 8.759398460388184,
  "theta_abs_le_8_bias_deg": 0.06806103140115738,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7312892079353333,
  "theta_abs_le_10_rmse_deg": 1.1489930152893066,
  "theta_abs_le_10_p95_abs_err_deg": 2.4380884170532227,
  "theta_abs_le_10_max_abs_err_deg": 8.759398460388184,
  "theta_abs_le_10_bias_deg": 0.05368444696068764,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7091513276100159,
  "theta_pos_8_10_rmse_deg": 1.0024415254592896,
  "theta_pos_8_10_p95_abs_err_deg": 1.6464462280273438,
  "theta_pos_8_10_max_abs_err_deg": 6.496790409088135,
  "theta_pos_8_10_bias_deg": -0.23458895087242126,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6339440941810608,
  "theta_neg_10_8_rmse_deg": 1.1584560871124268,
  "theta_neg_10_8_p95_abs_err_deg": 2.007051467895508,
  "theta_neg_10_8_max_abs_err_deg": 7.853987216949463,
  "theta_neg_10_8_bias_deg": 0.22459639608860016,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5686996579170227,
  "theta_pos_6_8_rmse_deg": 0.9513236284255981,
  "theta_pos_6_8_p95_abs_err_deg": 1.5040569305419922,
  "theta_pos_6_8_max_abs_err_deg": 5.639118194580078,
  "theta_pos_6_8_bias_deg": 0.022541871294379234,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7422245144844055,
  "theta_neg_8_6_rmse_deg": 1.0670750141143799,
  "theta_neg_8_6_p95_abs_err_deg": 1.9870694875717163,
  "theta_neg_8_6_max_abs_err_deg": 6.412652969360352,
  "theta_neg_8_6_bias_deg": -0.05908206105232239,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6995254755020142,
  "theta_neg_4_2_rmse_deg": 1.0290660858154297,
  "theta_neg_4_2_p95_abs_err_deg": 2.3249571323394775,
  "theta_neg_4_2_max_abs_err_deg": 5.579831600189209,
  "theta_neg_4_2_bias_deg": -0.20381319522857666,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5886680483818054,
  "theta_neg_2_0p5_rmse_deg": 0.7895694375038147,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.4028033018112183,
  "theta_neg_2_0p5_max_abs_err_deg": 3.702049732208252,
  "theta_neg_2_0p5_bias_deg": -0.2885279357433319,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.9898351430892944,
  "theta_pos_0p5_2_rmse_deg": 1.3510669469833374,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.3400068283081055,
  "theta_pos_0p5_2_max_abs_err_deg": 3.940103769302368,
  "theta_pos_0p5_2_bias_deg": 0.5365161299705505,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.31664247628155195,
  "loss_turn": 1.5311361060897455,
  "loss_theta": 0.00040210947045125065,
  "loss_main_bundle_base": 0.31664247628155195,
  "loss_turn_bundle_base": 0.3062272251136248,
  "loss_theta_bundle_base": 0.00026692319306934373,
  "loss_main_bundle": 0.31664247628155195,
  "loss_turn_bundle": 0.3062272251136248,
  "loss_theta_bundle": 0.00026692319306934373,
  "loss_theta_flat": 0.00022983089439033408,
  "loss_theta_near_flat": 0.001423415343979114,
  "loss_theta_error_excess": 0.00015708097877470506,
  "loss_theta_flat_excess": 0.00011262595919905734,
  "loss_theta_near_flat_excess": 0.0010511780315688754,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010329230293267343,
  "loss_theta_small_neg": 0.0003168130230791211,
  "loss_theta_small_neg_excess": 9.186422823000755e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.38817042818088815,
  "loss_false_turn_straight": 0.31926344629876185,
  "loss_transition_focal_raw": 1.4560865860991936,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 6.031518193349464,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
