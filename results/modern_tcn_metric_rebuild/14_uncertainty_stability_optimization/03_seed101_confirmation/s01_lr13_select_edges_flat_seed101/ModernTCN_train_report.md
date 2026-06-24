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
  "select_stall_weight": 0.2,
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
  "select_theta_flat_peak_weight": 1.0,
  "select_theta_flat_peak_target_deg": 5.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 1.2,
  "select_theta_edge_p95_target_deg": 1.15,
  "select_theta_small_nonzero_p95_weight": 0.8,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.3,
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9692 |
| acc_turn | 0.5911 |
| acc_turn_pure | 0.6066 |
| acc_turn_transition | 0.5231 |
| main_confidence_mean | 0.9907 |
| main_low_conf_0p60_ratio | 0.0053 |
| main_low_conf_0p70_ratio | 0.0122 |
| turn_confidence_mean | 0.8516 |
| turn_low_conf_0p60_ratio | 0.1274 |
| turn_low_conf_0p70_ratio | 0.2210 |
| turn_right_recall | 0.6358 |
| turn_straight_recall | 0.5758 |
| turn_left_recall | 0.5839 |
| theta_mae_deg | 0.6195 |
| theta_abs_le_10_p95_abs_err_deg | 1.5471 |
| theta_neg_10_8_p95_abs_err_deg | 1.1088 |
| theta_pos_8_10_p95_abs_err_deg | 2.1396 |
| theta_abs_le_8_p95_abs_err_deg | 1.5176 |
| theta_neg_8_6_p95_abs_err_deg | 1.3518 |
| theta_pos_6_8_p95_abs_err_deg | 1.5190 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.2283 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.6069 |
| theta_flat_abs_p95_deg | 2.5530 |
| theta_flat_bias_deg | 0.0129 |
| theta_near_flat_abs_p95_deg | 1.8290 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.0646 |
| theta_flat_turn_abs_p95_deg | 1.4414 |
| flat_recall | 0.9577 |
| stall_recall | 0.6875 |
| slope_recall | 0.9822 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7615 |
| downhill_recall | 0.7974 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    724,
    0,
    32
  ],
  [
    10,
    66,
    20
  ],
  [
    41,
    8,
    2701
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    508,
    180,
    111
  ],
  [
    387,
    1113,
    433
  ],
  [
    141,
    221,
    508
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.348363 |
| test_loss_turn_bundle_base | 0.378163 |
| test_loss_theta_bundle_base | 0.000138 |
| test_loss_transition_focal_raw | 1.847242 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.667402 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 85
- train_seconds: 392.4

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 19 | 0.2632 | 0.5633 |
| [0.60,0.70) | 25 | 0.3200 | 0.6482 |
| [0.70,0.80) | 25 | 0.3600 | 0.7393 |
| [0.80,0.90) | 31 | 0.2903 | 0.8540 |
| [0.90,1.00) | 3502 | 0.0228 | 0.9984 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 459 | 0.6078 | 0.5287 |
| [0.60,0.70) | 337 | 0.4985 | 0.6471 |
| [0.70,0.80) | 365 | 0.5205 | 0.7526 |
| [0.80,0.90) | 441 | 0.4739 | 0.8504 |
| [0.90,1.00) | 2000 | 0.3135 | 0.9786 |


## 验证集最佳点

```json
{
  "loss_total": 0.6539654704811447,
  "acc_main": 0.9491204330175913,
  "acc_turn": 0.6211096075778079,
  "acc_turn_pure": 0.6397902327105867,
  "acc_turn_transition": 0.532608695652174,
  "false_turn_straight": 0.43607068607068605,
  "flat_recall": 0.9710806697108066,
  "stall_recall": 0.5,
  "slope_recall": 0.9506008010680908,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9710806697108066,
    0.5,
    0.9506008010680908
  ],
  "turn_right_recall": 0.6445497630331753,
  "turn_straight_recall": 0.5639293139293139,
  "turn_left_recall": 0.7184466019417476,
  "recall_turn": [
    0.6445497630331753,
    0.5639293139293139,
    0.7184466019417476
  ],
  "cm_turn": [
    [
      544,
      186,
      114
    ],
    [
      356,
      1085,
      483
    ],
    [
      61,
      200,
      666
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      638,
      0,
      19
    ],
    [
      0,
      21,
      21
    ],
    [
      140,
      8,
      2848
    ]
  ],
  "main_confidence_mean": 0.9720401265585361,
  "main_confidence_error_mean": 0.7715441058322162,
  "main_low_conf_0p60_ratio": 0.04925575101488498,
  "main_low_conf_0p70_ratio": 0.05331529093369418,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 182,
      "error_rate": 0.45054945054945056,
      "mean_confidence": 0.5444438833071723
    },
    {
      "bin": "[0.60,0.70)",
      "n": 15,
      "error_rate": 0.26666666666666666,
      "mean_confidence": 0.6462876981436424
    },
    {
      "bin": "[0.70,0.80)",
      "n": 16,
      "error_rate": 0.5,
      "mean_confidence": 0.7330013882389456
    },
    {
      "bin": "[0.80,0.90)",
      "n": 40,
      "error_rate": 0.175,
      "mean_confidence": 0.854382122348922
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3442,
      "error_rate": 0.0252760023242301,
      "mean_confidence": 0.9985478960761043
    }
  ],
  "turn_confidence_mean": 0.8603255649628141,
  "turn_confidence_error_mean": 0.7777296637242336,
  "turn_low_conf_0p60_ratio": 0.12855209742895804,
  "turn_low_conf_0p70_ratio": 0.19945872801082545,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 475,
      "error_rate": 0.6968421052631579,
      "mean_confidence": 0.4882386851036296
    },
    {
      "bin": "[0.60,0.70)",
      "n": 262,
      "error_rate": 0.5801526717557252,
      "mean_confidence": 0.6488673479814666
    },
    {
      "bin": "[0.70,0.80)",
      "n": 304,
      "error_rate": 0.5460526315789473,
      "mean_confidence": 0.7540787583887001
    },
    {
      "bin": "[0.80,0.90)",
      "n": 438,
      "error_rate": 0.4657534246575342,
      "mean_confidence": 0.8546934593327412
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2216,
      "error_rate": 0.24684115523465705,
      "mean_confidence": 0.9807719603810126
    }
  ],
  "theta_mae_rad": 0.012860557064414024,
  "theta_mae_deg": 0.7368556261062622,
  "uphill_recall": 0.7741239892183288,
  "downhill_recall": 0.7958843159065628,
  "slope_sign_acc": 0.979742677251574,
  "theta_flat_mae_deg": 0.9631978273391724,
  "theta_flat_abs_p95_deg": 3.7871592044830322,
  "theta_flat_abs_max_deg": 6.858957290649414,
  "theta_flat_bias_deg": 0.47329846024513245,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.289833664894104,
  "theta_near_flat_abs_p95_deg": 3.787374258041382,
  "theta_near_flat_abs_max_deg": 6.858957290649414,
  "theta_near_flat_bias_deg": 0.8159315586090088,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.051842451095581,
  "theta_flat_turn_abs_p95_deg": 3.787158727645874,
  "theta_flat_turn_abs_max_deg": 6.858957290649414,
  "theta_flat_turn_bias_deg": 0.32759249210357666,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7368556261062622,
  "theta_slope_control_abs_p95_deg": 9.408297538757324,
  "theta_slope_control_abs_max_deg": 12.96403980255127,
  "theta_slope_control_bias_deg": -0.04039030149579048,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7368555665016174,
  "theta_all_rmse_deg": 1.0977636575698853,
  "theta_all_p95_abs_err_deg": 2.3138532638549805,
  "theta_all_max_abs_err_deg": 6.358956813812256,
  "theta_all_bias_deg": -0.04039030149579048,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6872203946113586,
  "theta_active_abs_ge_2_rmse_deg": 0.9973036646842957,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.9590946435928345,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.184974670410156,
  "theta_active_abs_ge_2_bias_deg": -0.15303833782672882,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7567195296287537,
  "theta_abs_le_8_rmse_deg": 1.130028247833252,
  "theta_abs_le_8_p95_abs_err_deg": 2.4746716022491455,
  "theta_abs_le_8_max_abs_err_deg": 6.358956813812256,
  "theta_abs_le_8_bias_deg": 0.024770639836788177,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7368555665016174,
  "theta_abs_le_10_rmse_deg": 1.0977636575698853,
  "theta_abs_le_10_p95_abs_err_deg": 2.3138532638549805,
  "theta_abs_le_10_max_abs_err_deg": 6.358956813812256,
  "theta_abs_le_10_bias_deg": -0.04039030149579048,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5905513763427734,
  "theta_pos_8_10_rmse_deg": 0.8321014642715454,
  "theta_pos_8_10_p95_abs_err_deg": 1.6791496276855469,
  "theta_pos_8_10_max_abs_err_deg": 4.557836532592773,
  "theta_pos_8_10_bias_deg": -0.32721835374832153,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7166457772254944,
  "theta_neg_10_8_rmse_deg": 1.0559114217758179,
  "theta_neg_10_8_p95_abs_err_deg": 1.977019190788269,
  "theta_neg_10_8_max_abs_err_deg": 5.582956790924072,
  "theta_neg_10_8_bias_deg": -0.3031279742717743,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6128424406051636,
  "theta_pos_6_8_rmse_deg": 0.82845538854599,
  "theta_pos_6_8_p95_abs_err_deg": 1.577720046043396,
  "theta_pos_6_8_max_abs_err_deg": 3.4976730346679688,
  "theta_pos_6_8_bias_deg": -0.18434232473373413,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7557191252708435,
  "theta_neg_8_6_rmse_deg": 1.0484521389007568,
  "theta_neg_8_6_p95_abs_err_deg": 2.151587963104248,
  "theta_neg_8_6_max_abs_err_deg": 5.334954738616943,
  "theta_neg_8_6_bias_deg": -0.30207061767578125,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6644347310066223,
  "theta_neg_4_2_rmse_deg": 0.9397028088569641,
  "theta_neg_4_2_p95_abs_err_deg": 1.9782016277313232,
  "theta_neg_4_2_max_abs_err_deg": 5.122971057891846,
  "theta_neg_4_2_bias_deg": -0.19007748365402222,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.4340626001358032,
  "theta_neg_2_0p5_rmse_deg": 0.6087090969085693,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.1965372562408447,
  "theta_neg_2_0p5_max_abs_err_deg": 3.5004520416259766,
  "theta_neg_2_0p5_bias_deg": -0.2055332213640213,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.125023365020752,
  "theta_pos_0p5_2_rmse_deg": 1.45500910282135,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.287158727645874,
  "theta_pos_0p5_2_max_abs_err_deg": 4.2466607093811035,
  "theta_pos_0p5_2_bias_deg": 0.8075540661811829,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3494866698375413,
  "loss_turn": 1.5212008194284607,
  "loss_theta": 0.00036706812134710756,
  "loss_main_bundle_base": 0.3494866698375413,
  "loss_turn_bundle_base": 0.3042401671893542,
  "loss_theta_bundle_base": 0.000238622332860417,
  "loss_main_bundle": 0.3494866698375413,
  "loss_turn_bundle": 0.3042401671893542,
  "loss_theta_bundle": 0.000238622332860417,
  "loss_theta_flat": 0.00018419239822784104,
  "loss_theta_near_flat": 0.001158135841034746,
  "loss_theta_error_excess": 0.00012011415428209152,
  "loss_theta_flat_excess": 0.0001004084511111438,
  "loss_theta_near_flat_excess": 0.0008113204574033477,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 8.626070192138221e-05,
  "loss_theta_small_neg": 0.00026322162295981525,
  "loss_theta_small_neg_excess": 6.508111213891563e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.40895058592536937,
  "loss_false_turn_straight": 0.3188137452641101,
  "loss_transition_focal_raw": 1.4238255566285976,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.5317426175699107,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
