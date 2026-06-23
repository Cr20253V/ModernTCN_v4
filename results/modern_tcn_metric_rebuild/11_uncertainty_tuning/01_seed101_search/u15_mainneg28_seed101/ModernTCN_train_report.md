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
  "main_neg_slope_weight": 2.8,
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
| acc_main | 0.9634 |
| acc_turn | 0.5647 |
| acc_turn_pure | 0.5759 |
| acc_turn_transition | 0.5156 |
| main_confidence_mean | 0.9902 |
| main_low_conf_0p60_ratio | 0.0089 |
| main_low_conf_0p70_ratio | 0.0122 |
| turn_confidence_mean | 0.8435 |
| turn_low_conf_0p60_ratio | 0.1377 |
| turn_low_conf_0p70_ratio | 0.2390 |
| turn_right_recall | 0.6133 |
| turn_straight_recall | 0.5365 |
| turn_left_recall | 0.5828 |
| theta_mae_deg | 0.6169 |
| theta_abs_le_10_p95_abs_err_deg | 1.6739 |
| theta_neg_10_8_p95_abs_err_deg | 1.4075 |
| theta_pos_8_10_p95_abs_err_deg | 2.3425 |
| theta_abs_le_8_p95_abs_err_deg | 1.5316 |
| theta_neg_8_6_p95_abs_err_deg | 1.5741 |
| theta_pos_6_8_p95_abs_err_deg | 1.4862 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.3513 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5309 |
| theta_flat_abs_p95_deg | 2.4393 |
| theta_flat_bias_deg | -0.3192 |
| theta_near_flat_abs_p95_deg | 1.9591 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.3398 |
| theta_flat_turn_abs_p95_deg | 1.6017 |
| flat_recall | 0.9444 |
| stall_recall | 0.7083 |
| slope_recall | 0.9775 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7569 |
| downhill_recall | 0.8002 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    714,
    0,
    42
  ],
  [
    10,
    68,
    18
  ],
  [
    53,
    9,
    2688
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    490,
    179,
    130
  ],
  [
    404,
    1037,
    492
  ],
  [
    187,
    176,
    507
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.334661 |
| test_loss_turn_bundle_base | 0.368301 |
| test_loss_theta_bundle_base | 0.000155 |
| test_loss_transition_focal_raw | 1.701334 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.949735 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 83
- train_seconds: 378.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 32 | 0.6250 | 0.5294 |
| [0.60,0.70) | 12 | 0.3333 | 0.6602 |
| [0.70,0.80) | 22 | 0.5909 | 0.7518 |
| [0.80,0.90) | 27 | 0.3704 | 0.8596 |
| [0.90,1.00) | 3509 | 0.0242 | 0.9980 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 496 | 0.6250 | 0.5243 |
| [0.60,0.70) | 365 | 0.5726 | 0.6484 |
| [0.70,0.80) | 379 | 0.4934 | 0.7517 |
| [0.80,0.90) | 447 | 0.5324 | 0.8534 |
| [0.90,1.00) | 1915 | 0.3258 | 0.9791 |


## 验证集最佳点

```json
{
  "loss_total": 0.6628833313433501,
  "acc_main": 0.9445196211096076,
  "acc_turn": 0.6365358592692828,
  "acc_turn_pure": 0.6489675516224189,
  "acc_turn_transition": 0.577639751552795,
  "false_turn_straight": 0.4319126819126819,
  "flat_recall": 0.943683409436834,
  "stall_recall": 0.3333333333333333,
  "slope_recall": 0.9532710280373832,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.943683409436834,
    0.3333333333333333,
    0.9532710280373832
  ],
  "turn_right_recall": 0.6516587677725119,
  "turn_straight_recall": 0.568087318087318,
  "turn_left_recall": 0.7648327939590076,
  "recall_turn": [
    0.6516587677725119,
    0.568087318087318,
    0.7648327939590076
  ],
  "cm_turn": [
    [
      550,
      197,
      97
    ],
    [
      349,
      1093,
      482
    ],
    [
      74,
      144,
      709
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      620,
      0,
      37
    ],
    [
      0,
      14,
      28
    ],
    [
      129,
      11,
      2856
    ]
  ],
  "main_confidence_mean": 0.9673176975925556,
  "main_confidence_error_mean": 0.7484780776923885,
  "main_low_conf_0p60_ratio": 0.05277401894451962,
  "main_low_conf_0p70_ratio": 0.05899864682002706,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 195,
      "error_rate": 0.4512820512820513,
      "mean_confidence": 0.5091930149331337
    },
    {
      "bin": "[0.60,0.70)",
      "n": 23,
      "error_rate": 0.43478260869565216,
      "mean_confidence": 0.6438927723777337
    },
    {
      "bin": "[0.70,0.80)",
      "n": 28,
      "error_rate": 0.32142857142857145,
      "mean_confidence": 0.7550250975681001
    },
    {
      "bin": "[0.80,0.90)",
      "n": 32,
      "error_rate": 0.375,
      "mean_confidence": 0.8549842009250121
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3417,
      "error_rate": 0.025168276265730174,
      "mean_confidence": 0.9984303552140289
    }
  ],
  "turn_confidence_mean": 0.8600358847084494,
  "turn_confidence_error_mean": 0.7849706615135073,
  "turn_low_conf_0p60_ratio": 0.13234100135317997,
  "turn_low_conf_0p70_ratio": 0.20920162381596752,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 489,
      "error_rate": 0.6380368098159509,
      "mean_confidence": 0.4912423129430979
    },
    {
      "bin": "[0.60,0.70)",
      "n": 284,
      "error_rate": 0.5211267605633803,
      "mean_confidence": 0.6569887244778326
    },
    {
      "bin": "[0.70,0.80)",
      "n": 295,
      "error_rate": 0.48135593220338985,
      "mean_confidence": 0.7496284472954154
    },
    {
      "bin": "[0.80,0.90)",
      "n": 369,
      "error_rate": 0.43360433604336046,
      "mean_confidence": 0.8511906525748255
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2258,
      "error_rate": 0.25730735163861823,
      "mean_confidence": 0.9813111436955637
    }
  ],
  "theta_mae_rad": 0.012813149951398373,
  "theta_mae_deg": 0.7341393828392029,
  "uphill_recall": 0.7778975741239892,
  "downhill_recall": 0.8064516129032258,
  "slope_sign_acc": 0.9723514919244457,
  "theta_flat_mae_deg": 0.9851081967353821,
  "theta_flat_abs_p95_deg": 3.3890042304992676,
  "theta_flat_abs_max_deg": 9.117193222045898,
  "theta_flat_bias_deg": 0.06246352568268776,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.3750035762786865,
  "theta_near_flat_abs_p95_deg": 3.574633836746216,
  "theta_near_flat_abs_max_deg": 9.117193222045898,
  "theta_near_flat_bias_deg": 0.42773663997650146,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1037503480911255,
  "theta_flat_turn_abs_p95_deg": 3.573070764541626,
  "theta_flat_turn_abs_max_deg": 9.117193222045898,
  "theta_flat_turn_bias_deg": -0.16774143278598785,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7341393828392029,
  "theta_slope_control_abs_p95_deg": 9.085320472717285,
  "theta_slope_control_abs_max_deg": 11.670149803161621,
  "theta_slope_control_bias_deg": 0.12563470005989075,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7341394424438477,
  "theta_all_rmse_deg": 1.122655987739563,
  "theta_all_p95_abs_err_deg": 2.4601049423217773,
  "theta_all_max_abs_err_deg": 8.617193222045898,
  "theta_all_bias_deg": 0.12563470005989075,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6791038513183594,
  "theta_active_abs_ge_2_rmse_deg": 1.0309919118881226,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.1076583862304688,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.879879474639893,
  "theta_active_abs_ge_2_bias_deg": 0.13948765397071838,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7288815379142761,
  "theta_abs_le_8_rmse_deg": 1.130468726158142,
  "theta_abs_le_8_p95_abs_err_deg": 2.6920478343963623,
  "theta_abs_le_8_max_abs_err_deg": 8.617193222045898,
  "theta_abs_le_8_bias_deg": 0.11521995067596436,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7341394424438477,
  "theta_abs_le_10_rmse_deg": 1.122655987739563,
  "theta_abs_le_10_p95_abs_err_deg": 2.4601049423217773,
  "theta_abs_le_10_max_abs_err_deg": 8.617193222045898,
  "theta_abs_le_10_bias_deg": 0.12563470005989075,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6322481632232666,
  "theta_pos_8_10_rmse_deg": 0.8115810751914978,
  "theta_pos_8_10_p95_abs_err_deg": 1.5923582315444946,
  "theta_pos_8_10_max_abs_err_deg": 3.609490156173706,
  "theta_pos_8_10_bias_deg": -0.2935028374195099,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8825374841690063,
  "theta_neg_10_8_rmse_deg": 1.312497854232788,
  "theta_neg_10_8_p95_abs_err_deg": 2.3280937671661377,
  "theta_neg_10_8_max_abs_err_deg": 6.879879474639893,
  "theta_neg_10_8_bias_deg": 0.6406500339508057,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5370112061500549,
  "theta_pos_6_8_rmse_deg": 0.8231475353240967,
  "theta_pos_6_8_p95_abs_err_deg": 1.631612777709961,
  "theta_pos_6_8_max_abs_err_deg": 4.346139430999756,
  "theta_pos_6_8_bias_deg": -0.030340053141117096,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7026424407958984,
  "theta_neg_8_6_rmse_deg": 1.041553258895874,
  "theta_neg_8_6_p95_abs_err_deg": 1.9344788789749146,
  "theta_neg_8_6_max_abs_err_deg": 6.335249900817871,
  "theta_neg_8_6_bias_deg": 0.2671954929828644,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6892206072807312,
  "theta_neg_4_2_rmse_deg": 1.0127512216567993,
  "theta_neg_4_2_p95_abs_err_deg": 2.5362250804901123,
  "theta_neg_4_2_max_abs_err_deg": 5.1940741539001465,
  "theta_neg_4_2_bias_deg": 0.1454523205757141,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.7434770464897156,
  "theta_neg_2_0p5_rmse_deg": 0.9668388962745667,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.77656888961792,
  "theta_neg_2_0p5_max_abs_err_deg": 3.5679686069488525,
  "theta_neg_2_0p5_bias_deg": -0.5727559924125671,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.8013361692428589,
  "theta_pos_0p5_2_rmse_deg": 1.1324131488800049,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.8889727592468262,
  "theta_pos_0p5_2_max_abs_err_deg": 4.372335433959961,
  "theta_pos_0p5_2_bias_deg": 0.43728917837142944,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3589250726612721,
  "loss_turn": 1.5184508899229305,
  "loss_theta": 0.00038396398178005593,
  "loss_main_bundle_base": 0.3589250726612721,
  "loss_turn_bundle_base": 0.30369018211416365,
  "loss_theta_bundle_base": 0.0002680795770220418,
  "loss_main_bundle": 0.3589250726612721,
  "loss_turn_bundle": 0.30369018211416365,
  "loss_theta_bundle": 0.0002680795770220418,
  "loss_theta_flat": 0.00032927138829025337,
  "loss_theta_near_flat": 0.0011646602181175846,
  "loss_theta_error_excess": 0.00013596157437657965,
  "loss_theta_flat_excess": 0.00014669335105478703,
  "loss_theta_near_flat_excess": 0.0008271843634157647,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010588735361953414,
  "loss_theta_small_neg": 0.00031037648815405837,
  "loss_theta_small_neg_excess": 8.529042877087997e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3962186644783846,
  "loss_false_turn_straight": 0.3253494658634692,
  "loss_transition_focal_raw": 1.3541165332671592,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.937158660540239,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
