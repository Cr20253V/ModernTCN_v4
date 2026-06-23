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
  "lambda_turn": 0.24,
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
  "main_neg_slope_weight": 2.4,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 3.0,
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
| acc_main | 0.9561 |
| acc_turn | 0.5527 |
| acc_turn_pure | 0.5681 |
| acc_turn_transition | 0.4858 |
| main_confidence_mean | 0.9847 |
| main_low_conf_0p60_ratio | 0.0105 |
| main_low_conf_0p70_ratio | 0.0200 |
| turn_confidence_mean | 0.7993 |
| turn_low_conf_0p60_ratio | 0.1952 |
| turn_low_conf_0p70_ratio | 0.3093 |
| turn_right_recall | 0.5444 |
| turn_straight_recall | 0.5360 |
| turn_left_recall | 0.5977 |
| theta_mae_deg | 0.6692 |
| theta_abs_le_10_p95_abs_err_deg | 1.8164 |
| theta_neg_10_8_p95_abs_err_deg | 1.5392 |
| theta_pos_8_10_p95_abs_err_deg | 3.0237 |
| theta_abs_le_8_p95_abs_err_deg | 1.7536 |
| theta_neg_8_6_p95_abs_err_deg | 1.2541 |
| theta_pos_6_8_p95_abs_err_deg | 1.8740 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.5088 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.6392 |
| theta_flat_abs_p95_deg | 2.8814 |
| theta_flat_bias_deg | 0.1992 |
| theta_near_flat_abs_p95_deg | 2.2779 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.3565 |
| theta_flat_turn_abs_p95_deg | 2.1059 |
| flat_recall | 0.9458 |
| stall_recall | 0.6667 |
| slope_recall | 0.9691 |
| flat_as_stall_ratio | 0.0013 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7443 |
| downhill_recall | 0.7985 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    715,
    1,
    40
  ],
  [
    10,
    64,
    22
  ],
  [
    74,
    11,
    2665
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    435,
    207,
    157
  ],
  [
    369,
    1036,
    528
  ],
  [
    142,
    208,
    520
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.347087 |
| test_loss_turn_bundle_base | 0.379598 |
| test_loss_theta_bundle_base | 0.000184 |
| test_loss_transition_focal_raw | 1.325378 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.836130 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 53
- train_seconds: 281.3

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 38 | 0.8421 | 0.5396 |
| [0.60,0.70) | 34 | 0.5588 | 0.6519 |
| [0.70,0.80) | 32 | 0.1562 | 0.7673 |
| [0.80,0.90) | 55 | 0.2364 | 0.8516 |
| [0.90,1.00) | 3443 | 0.0258 | 0.9970 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 703 | 0.6117 | 0.5171 |
| [0.60,0.70) | 411 | 0.5304 | 0.6478 |
| [0.70,0.80) | 480 | 0.5542 | 0.7513 |
| [0.80,0.90) | 508 | 0.5020 | 0.8501 |
| [0.90,1.00) | 1500 | 0.2947 | 0.9713 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.4858

## 验证集最佳点

```json
{
  "loss_total": 0.5256201015596299,
  "acc_main": 0.9442489851150203,
  "acc_turn": 0.6354533152909337,
  "acc_turn_pure": 0.6473287446738775,
  "acc_turn_transition": 0.5791925465838509,
  "false_turn_straight": 0.42411642411642414,
  "flat_recall": 0.9680365296803652,
  "stall_recall": 0.5,
  "slope_recall": 0.945260347129506,
  "flat_as_stall_ratio": 0.0015220700152207,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9680365296803652,
    0.5,
    0.945260347129506
  ],
  "turn_right_recall": 0.6232227488151659,
  "turn_straight_recall": 0.5758835758835759,
  "turn_left_recall": 0.7702265372168284,
  "recall_turn": [
    0.6232227488151659,
    0.5758835758835759,
    0.7702265372168284
  ],
  "cm_turn": [
    [
      526,
      205,
      113
    ],
    [
      303,
      1108,
      513
    ],
    [
      52,
      161,
      714
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      636,
      1,
      20
    ],
    [
      0,
      21,
      21
    ],
    [
      149,
      15,
      2832
    ]
  ],
  "main_confidence_mean": 0.9706084609145775,
  "main_confidence_error_mean": 0.780029672088357,
  "main_low_conf_0p60_ratio": 0.0040595399188092015,
  "main_low_conf_0p70_ratio": 0.05466847090663058,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 15,
      "error_rate": 0.6,
      "mean_confidence": 0.5562391944229865
    },
    {
      "bin": "[0.60,0.70)",
      "n": 187,
      "error_rate": 0.46524064171123,
      "mean_confidence": 0.6114150135642464
    },
    {
      "bin": "[0.70,0.80)",
      "n": 42,
      "error_rate": 0.30952380952380953,
      "mean_confidence": 0.7469502623314932
    },
    {
      "bin": "[0.80,0.90)",
      "n": 65,
      "error_rate": 0.3230769230769231,
      "mean_confidence": 0.8547339092612589
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3386,
      "error_rate": 0.02244536326048435,
      "mean_confidence": 0.9972801100137627
    }
  ],
  "turn_confidence_mean": 0.8133092902582558,
  "turn_confidence_error_mean": 0.7415246704303137,
  "turn_low_conf_0p60_ratio": 0.18322056833558864,
  "turn_low_conf_0p70_ratio": 0.28416779431664413,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 677,
      "error_rate": 0.620384047267356,
      "mean_confidence": 0.5092408371532086
    },
    {
      "bin": "[0.60,0.70)",
      "n": 373,
      "error_rate": 0.40214477211796246,
      "mean_confidence": 0.6500421102917365
    },
    {
      "bin": "[0.70,0.80)",
      "n": 443,
      "error_rate": 0.4221218961625282,
      "mean_confidence": 0.7514034596944665
    },
    {
      "bin": "[0.80,0.90)",
      "n": 497,
      "error_rate": 0.358148893360161,
      "mean_confidence": 0.8515428176335832
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1705,
      "error_rate": 0.24164222873900293,
      "mean_confidence": 0.974702381586027
    }
  ],
  "theta_mae_rad": 0.014920998364686966,
  "theta_mae_deg": 0.8549101948738098,
  "uphill_recall": 0.768733153638814,
  "downhill_recall": 0.7931034482758621,
  "slope_sign_acc": 0.9586641116890228,
  "theta_flat_mae_deg": 1.2403684854507446,
  "theta_flat_abs_p95_deg": 3.4934678077697754,
  "theta_flat_abs_max_deg": 10.479735374450684,
  "theta_flat_bias_deg": 0.9827771782875061,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5692247152328491,
  "theta_near_flat_abs_p95_deg": 3.8701133728027344,
  "theta_near_flat_abs_max_deg": 10.479735374450684,
  "theta_near_flat_bias_deg": 1.3656017780303955,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.3795945644378662,
  "theta_flat_turn_abs_p95_deg": 3.49340558052063,
  "theta_flat_turn_abs_max_deg": 10.479735374450684,
  "theta_flat_turn_bias_deg": 1.1004118919372559,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8549101948738098,
  "theta_slope_control_abs_p95_deg": 9.388689041137695,
  "theta_slope_control_abs_max_deg": 11.658881187438965,
  "theta_slope_control_bias_deg": 0.1194092184305191,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8549102544784546,
  "theta_all_rmse_deg": 1.2996293306350708,
  "theta_all_p95_abs_err_deg": 2.6430587768554688,
  "theta_all_max_abs_err_deg": 10.979735374450684,
  "theta_all_bias_deg": 0.11940920352935791,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7703821659088135,
  "theta_active_abs_ge_2_rmse_deg": 1.1517360210418701,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.143160343170166,
  "theta_active_abs_ge_2_max_abs_err_deg": 8.415787696838379,
  "theta_active_abs_ge_2_bias_deg": -0.06992083042860031,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8709377646446228,
  "theta_abs_le_8_rmse_deg": 1.327709436416626,
  "theta_abs_le_8_p95_abs_err_deg": 2.75780987739563,
  "theta_abs_le_8_max_abs_err_deg": 10.979735374450684,
  "theta_abs_le_8_bias_deg": 0.21661004424095154,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8549102544784546,
  "theta_abs_le_10_rmse_deg": 1.2996293306350708,
  "theta_abs_le_10_p95_abs_err_deg": 2.6430587768554688,
  "theta_abs_le_10_max_abs_err_deg": 10.979735374450684,
  "theta_abs_le_10_bias_deg": 0.11940920352935791,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.8034957647323608,
  "theta_pos_8_10_rmse_deg": 0.9989590048789978,
  "theta_pos_8_10_p95_abs_err_deg": 1.6801241636276245,
  "theta_pos_8_10_max_abs_err_deg": 5.522556781768799,
  "theta_pos_8_10_bias_deg": -0.5362426042556763,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7708183526992798,
  "theta_neg_10_8_rmse_deg": 1.3282550573349,
  "theta_neg_10_8_p95_abs_err_deg": 2.156564712524414,
  "theta_neg_10_8_max_abs_err_deg": 8.415787696838379,
  "theta_neg_10_8_bias_deg": -0.040789734572172165,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.7019051313400269,
  "theta_pos_6_8_rmse_deg": 0.9097211360931396,
  "theta_pos_6_8_p95_abs_err_deg": 1.765244960784912,
  "theta_pos_6_8_max_abs_err_deg": 3.5681912899017334,
  "theta_pos_6_8_bias_deg": -0.34274041652679443,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7509876489639282,
  "theta_neg_8_6_rmse_deg": 1.147011399269104,
  "theta_neg_8_6_p95_abs_err_deg": 2.638803243637085,
  "theta_neg_8_6_max_abs_err_deg": 6.692823886871338,
  "theta_neg_8_6_bias_deg": -0.07137523591518402,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7553310990333557,
  "theta_neg_4_2_rmse_deg": 1.115731120109558,
  "theta_neg_4_2_p95_abs_err_deg": 2.322460174560547,
  "theta_neg_4_2_max_abs_err_deg": 7.0683135986328125,
  "theta_neg_4_2_bias_deg": 0.10971469432115555,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.8392965793609619,
  "theta_neg_2_0p5_rmse_deg": 1.1285204887390137,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.177408456802368,
  "theta_neg_2_0p5_max_abs_err_deg": 4.198581218719482,
  "theta_neg_2_0p5_bias_deg": 0.4838978052139282,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.3484057188034058,
  "theta_pos_0p5_2_rmse_deg": 1.579491376876831,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.320364475250244,
  "theta_pos_0p5_2_max_abs_err_deg": 4.628954887390137,
  "theta_pos_0p5_2_bias_deg": 1.1126431226730347,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.21363256975343003,
  "loss_turn": 1.2985502097538908,
  "loss_theta": 0.0005142310652528992,
  "loss_main_bundle_base": 0.21363256975343003,
  "loss_turn_bundle_base": 0.31165204251409384,
  "loss_theta_bundle_base": 0.0003354951712688499,
  "loss_main_bundle": 0.21363256975343003,
  "loss_turn_bundle": 0.31165204251409384,
  "loss_theta_bundle": 0.0003354951712688499,
  "loss_theta_flat": 0.00023046591675478627,
  "loss_theta_near_flat": 0.0015660232679694085,
  "loss_theta_error_excess": 0.00020861981935352993,
  "loss_theta_flat_excess": 0.00011441330699249629,
  "loss_theta_near_flat_excess": 0.0011785095624993675,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00014581178861300943,
  "loss_theta_small_neg": 0.0003719515126691287,
  "loss_theta_small_neg_excess": 0.00012260830291523723,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3767914296970961,
  "loss_false_turn_straight": 0.297561520886518,
  "loss_transition_focal_raw": 1.0426639987748112,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.717886099566283,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
