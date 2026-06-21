# ModernTCN-small mode-conditioned theta experts 训练报告

## 固定约束

- model_family: `small_mode_theta`
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

## E4 Mode-Conditioned Theta Experts

- theta fusion: `sum(softmax(main_logits) * theta_experts)`.
- theta_gate_detach: `True`
- flat_theta_reg_lambda: `0.010000`
- theta_expert_hidden: `0`

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
  "theta_gate_detach": true,
  "flat_theta_reg_lambda": 0.01,
  "theta_expert_hidden": 0
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9697 |
| acc_turn | 0.5813 |
| acc_turn_pure | 0.6039 |
| acc_turn_transition | 0.4829 |
| main_confidence_mean | 0.9899 |
| main_low_conf_0p60_ratio | 0.0044 |
| main_low_conf_0p70_ratio | 0.0139 |
| turn_confidence_mean | 0.8330 |
| turn_low_conf_0p60_ratio | 0.1435 |
| turn_low_conf_0p70_ratio | 0.2490 |
| turn_right_recall | 0.6158 |
| turn_straight_recall | 0.5903 |
| turn_left_recall | 0.5299 |
| theta_mae_deg | 0.6164 |
| theta_abs_le_10_p95_abs_err_deg | 1.6970 |
| theta_neg_10_8_p95_abs_err_deg | 1.4071 |
| theta_pos_8_10_p95_abs_err_deg | 2.6513 |
| theta_abs_le_8_p95_abs_err_deg | 1.5796 |
| theta_neg_8_6_p95_abs_err_deg | 1.2559 |
| theta_pos_6_8_p95_abs_err_deg | 1.3689 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.1702 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.1317 |
| theta_flat_abs_p95_deg | 2.6349 |
| theta_flat_bias_deg | -0.4422 |
| theta_near_flat_abs_p95_deg | 1.8187 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.5390 |
| theta_flat_turn_abs_p95_deg | 1.4010 |
| flat_recall | 0.9669 |
| stall_recall | 0.6667 |
| slope_recall | 0.9811 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7626 |
| downhill_recall | 0.7906 |

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
    64,
    23
  ],
  [
    40,
    12,
    2698
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    492,
    199,
    108
  ],
  [
    421,
    1141,
    371
  ],
  [
    162,
    247,
    461
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.344708 |
| test_loss_turn_bundle_base | 0.341233 |
| test_loss_theta_bundle_base | 0.000299 |
| test_loss_transition_focal_raw | 1.538635 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.890990 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000578 |
| test_loss_flat_theta_expert_reg_weighted | 0.000006 |

- best_epoch: 72
- train_seconds: 334.7

## E3 Gate Statistics

| metric | value |
|---|---:|
| test_gate_all_finite | nan |
| test_gate_single_collapse | nan |
| test_gate_mean_entropy | nan |
| test_gate_interpretability_score | nan |
| test_gate_yaw_transition_minus_overall | nan |
| test_gate_drive_stall_minus_overall | nan |
| test_gate_velocity_slope_flat_abs_delta | nan |

```json
{}
```

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 16 | 0.3750 | 0.5523 |
| [0.60,0.70) | 34 | 0.3235 | 0.6524 |
| [0.70,0.80) | 16 | 0.5000 | 0.7411 |
| [0.80,0.90) | 42 | 0.3571 | 0.8554 |
| [0.90,1.00) | 3494 | 0.0197 | 0.9979 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 517 | 0.6112 | 0.5118 |
| [0.60,0.70) | 380 | 0.5026 | 0.6507 |
| [0.70,0.80) | 444 | 0.6059 | 0.7533 |
| [0.80,0.90) | 447 | 0.5280 | 0.8525 |
| [0.90,1.00) | 1814 | 0.2734 | 0.9775 |


## 验证集最佳点

```json
{
  "loss_total": 0.5870333083750269,
  "acc_main": 0.9380243572395128,
  "acc_turn": 0.6598105548037889,
  "acc_turn_pure": 0.6653556211078335,
  "acc_turn_transition": 0.6335403726708074,
  "false_turn_straight": 0.3783783783783784,
  "flat_recall": 0.9178082191780822,
  "stall_recall": 0.42857142857142855,
  "slope_recall": 0.9495994659546061,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.023809523809523808,
  "recall_main": [
    0.9178082191780822,
    0.42857142857142855,
    0.9495994659546061
  ],
  "turn_right_recall": 0.7274881516587678,
  "turn_straight_recall": 0.6216216216216216,
  "turn_left_recall": 0.6774541531823085,
  "recall_turn": [
    0.7274881516587678,
    0.6216216216216216,
    0.6774541531823085
  ],
  "cm_turn": [
    [
      614,
      194,
      36
    ],
    [
      397,
      1196,
      331
    ],
    [
      101,
      198,
      628
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      603,
      0,
      54
    ],
    [
      1,
      18,
      23
    ],
    [
      136,
      15,
      2845
    ]
  ],
  "main_confidence_mean": 0.9684278634815584,
  "main_confidence_error_mean": 0.7730197118583416,
  "main_low_conf_0p60_ratio": 0.052232746955345064,
  "main_low_conf_0p70_ratio": 0.06089309878213803,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 193,
      "error_rate": 0.47668393782383417,
      "mean_confidence": 0.554978971788846
    },
    {
      "bin": "[0.60,0.70)",
      "n": 32,
      "error_rate": 0.5,
      "mean_confidence": 0.6505627274935931
    },
    {
      "bin": "[0.70,0.80)",
      "n": 23,
      "error_rate": 0.4782608695652174,
      "mean_confidence": 0.7464788250911362
    },
    {
      "bin": "[0.80,0.90)",
      "n": 41,
      "error_rate": 0.21951219512195122,
      "mean_confidence": 0.8534386483606208
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3406,
      "error_rate": 0.029653552554315912,
      "mean_confidence": 0.9977251935318362
    }
  ],
  "turn_confidence_mean": 0.8452686937816849,
  "turn_confidence_error_mean": 0.7690833277255135,
  "turn_low_conf_0p60_ratio": 0.14587280108254397,
  "turn_low_conf_0p70_ratio": 0.23518267929634643,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 539,
      "error_rate": 0.6159554730983302,
      "mean_confidence": 0.5155236539137817
    },
    {
      "bin": "[0.60,0.70)",
      "n": 330,
      "error_rate": 0.41818181818181815,
      "mean_confidence": 0.6531307346241736
    },
    {
      "bin": "[0.70,0.80)",
      "n": 333,
      "error_rate": 0.45345345345345345,
      "mean_confidence": 0.7479289679547572
    },
    {
      "bin": "[0.80,0.90)",
      "n": 467,
      "error_rate": 0.4346895074946467,
      "mean_confidence": 0.8543211604476713
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2026,
      "error_rate": 0.21372161895360317,
      "mean_confidence": 0.9782029138103766
    }
  ],
  "theta_mae_rad": 0.01285671815276146,
  "theta_mae_deg": 0.7366356253623962,
  "uphill_recall": 0.7746630727762803,
  "downhill_recall": 0.8131256952169077,
  "slope_sign_acc": 0.9761839583903641,
  "theta_flat_mae_deg": 0.9633284211158752,
  "theta_flat_abs_p95_deg": 3.3680806159973145,
  "theta_flat_abs_max_deg": 7.682435989379883,
  "theta_flat_bias_deg": 0.287564754486084,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.435939908027649,
  "theta_near_flat_abs_p95_deg": 4.238800048828125,
  "theta_near_flat_abs_max_deg": 16.09433364868164,
  "theta_near_flat_bias_deg": 0.7891955971717834,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.0787192583084106,
  "theta_flat_turn_abs_p95_deg": 3.4823801517486572,
  "theta_flat_turn_abs_max_deg": 7.682435989379883,
  "theta_flat_turn_bias_deg": 0.480907142162323,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7366356253623962,
  "theta_slope_control_abs_p95_deg": 9.308029174804688,
  "theta_slope_control_abs_max_deg": 41.045928955078125,
  "theta_slope_control_bias_deg": 0.043631792068481445,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.736635684967041,
  "theta_all_rmse_deg": 1.361740231513977,
  "theta_all_p95_abs_err_deg": 2.730165481567383,
  "theta_all_max_abs_err_deg": 33.59085464477539,
  "theta_all_bias_deg": 0.043631795793771744,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6869236826896667,
  "theta_active_abs_ge_2_rmse_deg": 1.3380823135375977,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2623534202575684,
  "theta_active_abs_ge_2_max_abs_err_deg": 33.59085464477539,
  "theta_active_abs_ge_2_bias_deg": -0.009860854595899582,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7580306529998779,
  "theta_abs_le_8_rmse_deg": 1.4222606420516968,
  "theta_abs_le_8_p95_abs_err_deg": 2.868070363998413,
  "theta_abs_le_8_max_abs_err_deg": 33.59085464477539,
  "theta_abs_le_8_bias_deg": 0.029214369133114815,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.736635684967041,
  "theta_abs_le_10_rmse_deg": 1.361740231513977,
  "theta_abs_le_10_p95_abs_err_deg": 2.730165481567383,
  "theta_abs_le_10_max_abs_err_deg": 33.59085464477539,
  "theta_abs_le_10_bias_deg": 0.043631795793771744,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5879400372505188,
  "theta_pos_8_10_rmse_deg": 0.8978471755981445,
  "theta_pos_8_10_p95_abs_err_deg": 1.5697619915008545,
  "theta_pos_8_10_max_abs_err_deg": 5.516744136810303,
  "theta_pos_8_10_bias_deg": -0.10794763267040253,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7058290839195251,
  "theta_neg_10_8_rmse_deg": 1.2193496227264404,
  "theta_neg_10_8_p95_abs_err_deg": 2.162477731704712,
  "theta_neg_10_8_max_abs_err_deg": 7.256590843200684,
  "theta_neg_10_8_bias_deg": 0.3205257058143616,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6121047139167786,
  "theta_pos_6_8_rmse_deg": 0.8794654011726379,
  "theta_pos_6_8_p95_abs_err_deg": 1.8611944913864136,
  "theta_pos_6_8_max_abs_err_deg": 3.5235612392425537,
  "theta_pos_6_8_bias_deg": 0.0006001007277518511,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7444441318511963,
  "theta_neg_8_6_rmse_deg": 2.0101089477539062,
  "theta_neg_8_6_p95_abs_err_deg": 1.950211763381958,
  "theta_neg_8_6_max_abs_err_deg": 33.59085464477539,
  "theta_neg_8_6_bias_deg": -0.17609979212284088,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.5664535164833069,
  "theta_neg_4_2_rmse_deg": 0.8948482871055603,
  "theta_neg_4_2_p95_abs_err_deg": 1.876772165298462,
  "theta_neg_4_2_max_abs_err_deg": 5.9626898765563965,
  "theta_neg_4_2_bias_deg": -0.009426888078451157,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5234656929969788,
  "theta_neg_2_0p5_rmse_deg": 0.7893409729003906,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.125752568244934,
  "theta_neg_2_0p5_max_abs_err_deg": 6.247814178466797,
  "theta_neg_2_0p5_bias_deg": -0.00012083001638529822,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0233393907546997,
  "theta_pos_0p5_2_rmse_deg": 1.2525588274002075,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.9779471158981323,
  "theta_pos_0p5_2_max_abs_err_deg": 4.270838737487793,
  "theta_pos_0p5_2_bias_deg": 0.16897162795066833,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3267681370891318,
  "loss_turn": 1.2992680134082841,
  "loss_theta": 0.0005651431566898879,
  "loss_main_bundle_base": 0.3267681370891318,
  "loss_turn_bundle_base": 0.25985360852517037,
  "loss_theta_bundle_base": 0.00040305688411233054,
  "loss_main_bundle": 0.3267681370891318,
  "loss_turn_bundle": 0.25985360852517037,
  "loss_theta_bundle": 0.0004115648455199494,
  "loss_theta_flat": 0.0003823418586095228,
  "loss_theta_near_flat": 0.0011399781570709355,
  "loss_theta_error_excess": 0.00030831528067619055,
  "loss_theta_flat_excess": 0.00019399028454802637,
  "loss_theta_near_flat_excess": 0.0007926321818372953,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00030931356702556303,
  "loss_theta_small_neg": 0.00024111145175205787,
  "loss_theta_small_neg_excess": 7.128507443621795e-05,
  "loss_flat_theta_expert_reg": 0.0008507957783148338,
  "loss_flat_theta_expert_reg_weighted": 8.507957588725693e-06,
  "loss_turn_release": 0.33684002115052186,
  "loss_false_turn_straight": 0.28576068829780343,
  "loss_transition_focal_raw": 1.070367168589761,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.889963011973927,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
