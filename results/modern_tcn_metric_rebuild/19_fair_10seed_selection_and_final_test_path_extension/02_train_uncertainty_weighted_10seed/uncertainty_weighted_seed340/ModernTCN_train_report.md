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
| acc_main | 0.9625 |
| acc_turn | 0.5847 |
| acc_turn_pure | 0.6025 |
| acc_turn_transition | 0.5067 |
| main_confidence_mean | 0.9895 |
| main_low_conf_0p60_ratio | 0.0056 |
| main_low_conf_0p70_ratio | 0.0108 |
| turn_confidence_mean | 0.8353 |
| turn_low_conf_0p60_ratio | 0.1444 |
| turn_low_conf_0p70_ratio | 0.2449 |
| turn_right_recall | 0.5544 |
| turn_straight_recall | 0.5820 |
| turn_left_recall | 0.6184 |
| theta_mae_deg | 0.5484 |
| theta_abs_le_10_p95_abs_err_deg | 1.5391 |
| theta_neg_10_8_p95_abs_err_deg | 1.5435 |
| theta_pos_8_10_p95_abs_err_deg | 2.2324 |
| theta_abs_le_8_p95_abs_err_deg | 1.3854 |
| theta_neg_8_6_p95_abs_err_deg | 1.2819 |
| theta_pos_6_8_p95_abs_err_deg | 1.5583 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.3268 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.3906 |
| theta_flat_abs_p95_deg | 2.3242 |
| theta_flat_bias_deg | 0.0458 |
| theta_near_flat_abs_p95_deg | 1.8294 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.0526 |
| theta_flat_turn_abs_p95_deg | 1.1826 |
| flat_recall | 0.9683 |
| stall_recall | 0.6354 |
| slope_recall | 0.9724 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0625 |
| uphill_recall | 0.7483 |
| downhill_recall | 0.7906 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    732,
    0,
    24
  ],
  [
    6,
    61,
    29
  ],
  [
    68,
    8,
    2674
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    443,
    218,
    138
  ],
  [
    297,
    1125,
    511
  ],
  [
    154,
    178,
    538
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.353144 |
| test_loss_turn_bundle_base | 0.339742 |
| test_loss_theta_bundle_base | 0.000134 |
| test_loss_transition_focal_raw | 1.445194 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.055775 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 81
- train_seconds: 354.5

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 20 | 0.4000 | 0.5529 |
| [0.60,0.70) | 19 | 0.7368 | 0.6467 |
| [0.70,0.80) | 29 | 0.4828 | 0.7559 |
| [0.80,0.90) | 42 | 0.2857 | 0.8523 |
| [0.90,1.00) | 3492 | 0.0249 | 0.9974 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 520 | 0.5923 | 0.5053 |
| [0.60,0.70) | 362 | 0.5110 | 0.6488 |
| [0.70,0.80) | 365 | 0.4986 | 0.7533 |
| [0.80,0.90) | 490 | 0.4898 | 0.8514 |
| [0.90,1.00) | 1865 | 0.3115 | 0.9753 |


## 验证集最佳点

```json
{
  "loss_total": 0.6192917140959403,
  "acc_main": 0.9410013531799729,
  "acc_turn": 0.6476319350473613,
  "acc_turn_pure": 0.6545394952474598,
  "acc_turn_transition": 0.6149068322981367,
  "false_turn_straight": 0.38513513513513514,
  "flat_recall": 0.9269406392694064,
  "stall_recall": 0.30952380952380953,
  "slope_recall": 0.9529372496662216,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9269406392694064,
    0.30952380952380953,
    0.9529372496662216
  ],
  "turn_right_recall": 0.5936018957345972,
  "turn_straight_recall": 0.6148648648648649,
  "turn_left_recall": 0.7648327939590076,
  "recall_turn": [
    0.5936018957345972,
    0.6148648648648649,
    0.7648327939590076
  ],
  "cm_turn": [
    [
      501,
      236,
      107
    ],
    [
      238,
      1183,
      503
    ],
    [
      50,
      168,
      709
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      609,
      0,
      48
    ],
    [
      0,
      13,
      29
    ],
    [
      133,
      8,
      2855
    ]
  ],
  "main_confidence_mean": 0.970521552002509,
  "main_confidence_error_mean": 0.7860700634365975,
  "main_low_conf_0p60_ratio": 0.007307171853856563,
  "main_low_conf_0p70_ratio": 0.061705006765899864,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 27,
      "error_rate": 0.4444444444444444,
      "mean_confidence": 0.5402293920899038
    },
    {
      "bin": "[0.60,0.70)",
      "n": 201,
      "error_rate": 0.4577114427860697,
      "mean_confidence": 0.6195274213102211
    },
    {
      "bin": "[0.70,0.80)",
      "n": 32,
      "error_rate": 0.4375,
      "mean_confidence": 0.7480773144518865
    },
    {
      "bin": "[0.80,0.90)",
      "n": 41,
      "error_rate": 0.1951219512195122,
      "mean_confidence": 0.8504620196504956
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3394,
      "error_rate": 0.027106658809664112,
      "mean_confidence": 0.9982788781707006
    }
  ],
  "turn_confidence_mean": 0.8572663972510385,
  "turn_confidence_error_mean": 0.7781724670781172,
  "turn_low_conf_0p60_ratio": 0.13098782138024356,
  "turn_low_conf_0p70_ratio": 0.20541271989174562,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 484,
      "error_rate": 0.6570247933884298,
      "mean_confidence": 0.5008127849782215
    },
    {
      "bin": "[0.60,0.70)",
      "n": 275,
      "error_rate": 0.52,
      "mean_confidence": 0.6510814961262813
    },
    {
      "bin": "[0.70,0.80)",
      "n": 317,
      "error_rate": 0.5110410094637224,
      "mean_confidence": 0.7513281471535718
    },
    {
      "bin": "[0.80,0.90)",
      "n": 441,
      "error_rate": 0.3424036281179138,
      "mean_confidence": 0.8559851046652228
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2178,
      "error_rate": 0.24242424242424243,
      "mean_confidence": 0.9781901215212832
    }
  ],
  "theta_mae_rad": 0.01258289534598589,
  "theta_mae_deg": 0.720946729183197,
  "uphill_recall": 0.7789757412398922,
  "downhill_recall": 0.8109010011123471,
  "slope_sign_acc": 0.9723514919244457,
  "theta_flat_mae_deg": 0.9582533836364746,
  "theta_flat_abs_p95_deg": 4.276253700256348,
  "theta_flat_abs_max_deg": 6.619561672210693,
  "theta_flat_bias_deg": 0.614517867565155,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.2902839183807373,
  "theta_near_flat_abs_p95_deg": 4.276266574859619,
  "theta_near_flat_abs_max_deg": 6.228820323944092,
  "theta_near_flat_bias_deg": 0.9994639754295349,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.901430606842041,
  "theta_flat_turn_abs_p95_deg": 4.276253700256348,
  "theta_flat_turn_abs_max_deg": 4.276253700256348,
  "theta_flat_turn_bias_deg": 0.5884152054786682,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.720946729183197,
  "theta_slope_control_abs_p95_deg": 9.363240242004395,
  "theta_slope_control_abs_max_deg": 11.647165298461914,
  "theta_slope_control_bias_deg": 0.11894301325082779,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7209467887878418,
  "theta_all_rmse_deg": 1.132066249847412,
  "theta_all_p95_abs_err_deg": 2.7029731273651123,
  "theta_all_max_abs_err_deg": 7.607170581817627,
  "theta_all_bias_deg": 0.11894300580024719,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6689072251319885,
  "theta_active_abs_ge_2_rmse_deg": 1.00823974609375,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.102203369140625,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.607170581817627,
  "theta_active_abs_ge_2_bias_deg": 0.010267217643558979,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7302822470664978,
  "theta_abs_le_8_rmse_deg": 1.146060585975647,
  "theta_abs_le_8_p95_abs_err_deg": 2.7762537002563477,
  "theta_abs_le_8_max_abs_err_deg": 6.3956427574157715,
  "theta_abs_le_8_bias_deg": 0.17861168086528778,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7209467887878418,
  "theta_abs_le_10_rmse_deg": 1.132066249847412,
  "theta_abs_le_10_p95_abs_err_deg": 2.7029731273651123,
  "theta_abs_le_10_max_abs_err_deg": 7.607170581817627,
  "theta_abs_le_10_bias_deg": 0.11894300580024719,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5817626714706421,
  "theta_pos_8_10_rmse_deg": 0.8573828339576721,
  "theta_pos_8_10_p95_abs_err_deg": 1.5143753290176392,
  "theta_pos_8_10_max_abs_err_deg": 5.777827262878418,
  "theta_pos_8_10_bias_deg": -0.27244481444358826,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7830918431282043,
  "theta_neg_10_8_rmse_deg": 1.2514725923538208,
  "theta_neg_10_8_p95_abs_err_deg": 2.1188018321990967,
  "theta_neg_10_8_max_abs_err_deg": 7.607170581817627,
  "theta_neg_10_8_bias_deg": 0.009312829934060574,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5650644302368164,
  "theta_pos_6_8_rmse_deg": 0.8113821744918823,
  "theta_pos_6_8_p95_abs_err_deg": 1.4308652877807617,
  "theta_pos_6_8_max_abs_err_deg": 3.622131824493408,
  "theta_pos_6_8_bias_deg": -0.017896588891744614,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7053977847099304,
  "theta_neg_8_6_rmse_deg": 1.0219465494155884,
  "theta_neg_8_6_p95_abs_err_deg": 2.249135732650757,
  "theta_neg_8_6_max_abs_err_deg": 6.3956427574157715,
  "theta_neg_8_6_bias_deg": -0.12698332965373993,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.5642189383506775,
  "theta_neg_4_2_rmse_deg": 0.8458543419837952,
  "theta_neg_4_2_p95_abs_err_deg": 1.602547287940979,
  "theta_neg_4_2_max_abs_err_deg": 6.322701930999756,
  "theta_neg_4_2_bias_deg": -0.11652544140815735,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.589786171913147,
  "theta_neg_2_0p5_rmse_deg": 0.884231686592102,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.696595549583435,
  "theta_neg_2_0p5_max_abs_err_deg": 5.159515857696533,
  "theta_neg_2_0p5_bias_deg": 0.2512158155441284,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.9899659156799316,
  "theta_pos_0p5_2_rmse_deg": 1.5012186765670776,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.7762537002563477,
  "theta_pos_0p5_2_max_abs_err_deg": 4.847589015960693,
  "theta_pos_0p5_2_bias_deg": 0.5608795881271362,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3342224743514648,
  "loss_turn": 1.4240587560991795,
  "loss_theta": 0.00039040805432152793,
  "loss_main_bundle_base": 0.3342224743514648,
  "loss_turn_bundle_base": 0.2848117551155116,
  "loss_theta_bundle_base": 0.0002574893374280205,
  "loss_main_bundle": 0.3342224743514648,
  "loss_turn_bundle": 0.2848117551155116,
  "loss_theta_bundle": 0.0002574893374280205,
  "loss_theta_flat": 0.0002147567847118863,
  "loss_theta_near_flat": 0.0012004810572867767,
  "loss_theta_error_excess": 0.00014525450523016428,
  "loss_theta_flat_excess": 0.00013006296119233145,
  "loss_theta_near_flat_excess": 0.0008784009994534431,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 9.731362988187456e-05,
  "loss_theta_small_neg": 0.00021260147147115032,
  "loss_theta_small_neg_excess": 5.3363904806884375e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3623910665915364,
  "loss_false_turn_straight": 0.2922486622536779,
  "loss_transition_focal_raw": 1.2574518162116952,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.5085281781640525,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
