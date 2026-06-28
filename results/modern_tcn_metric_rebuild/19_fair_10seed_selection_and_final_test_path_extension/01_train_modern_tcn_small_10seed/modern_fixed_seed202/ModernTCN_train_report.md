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
| acc_main | 0.9589 |
| acc_turn | 0.5944 |
| acc_turn_pure | 0.6114 |
| acc_turn_transition | 0.5201 |
| main_confidence_mean | 0.9855 |
| main_low_conf_0p60_ratio | 0.0111 |
| main_low_conf_0p70_ratio | 0.0189 |
| turn_confidence_mean | 0.8279 |
| turn_low_conf_0p60_ratio | 0.1571 |
| turn_low_conf_0p70_ratio | 0.2657 |
| turn_right_recall | 0.6158 |
| turn_straight_recall | 0.6048 |
| turn_left_recall | 0.5517 |
| theta_mae_deg | 0.7393 |
| theta_abs_le_10_p95_abs_err_deg | 2.1233 |
| theta_neg_10_8_p95_abs_err_deg | 1.5939 |
| theta_pos_8_10_p95_abs_err_deg | 3.0416 |
| theta_abs_le_8_p95_abs_err_deg | 2.0508 |
| theta_neg_8_6_p95_abs_err_deg | 2.2647 |
| theta_pos_6_8_p95_abs_err_deg | 1.6575 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6839 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.7332 |
| theta_flat_abs_p95_deg | 2.7554 |
| theta_flat_bias_deg | -0.3220 |
| theta_near_flat_abs_p95_deg | 2.1476 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.3363 |
| theta_flat_turn_abs_p95_deg | 1.7852 |
| flat_recall | 0.9471 |
| stall_recall | 0.6458 |
| slope_recall | 0.9731 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7511 |
| downhill_recall | 0.7980 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    716,
    0,
    40
  ],
  [
    9,
    62,
    25
  ],
  [
    63,
    11,
    2676
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    492,
    196,
    111
  ],
  [
    397,
    1169,
    367
  ],
  [
    161,
    229,
    480
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.298167 |
| test_loss_turn_bundle_base | 0.321067 |
| test_loss_theta_bundle_base | 0.000199 |
| test_loss_transition_focal_raw | 1.432072 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.082348 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 66
- train_seconds: 317.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 40 | 0.7000 | 0.5425 |
| [0.60,0.70) | 28 | 0.6429 | 0.6420 |
| [0.70,0.80) | 33 | 0.4242 | 0.7527 |
| [0.80,0.90) | 53 | 0.1698 | 0.8503 |
| [0.90,1.00) | 3448 | 0.0229 | 0.9977 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 566 | 0.6201 | 0.5313 |
| [0.60,0.70) | 391 | 0.5473 | 0.6524 |
| [0.70,0.80) | 418 | 0.5263 | 0.7521 |
| [0.80,0.90) | 511 | 0.4305 | 0.8516 |
| [0.90,1.00) | 1716 | 0.2657 | 0.9771 |


## 验证集最佳点

```json
{
  "loss_total": 0.6738359039626682,
  "acc_main": 0.9431664411366711,
  "acc_turn": 0.6538565629228688,
  "acc_turn_pure": 0.6656833824975418,
  "acc_turn_transition": 0.5978260869565217,
  "false_turn_straight": 0.3737006237006237,
  "flat_recall": 0.943683409436834,
  "stall_recall": 0.2619047619047619,
  "slope_recall": 0.9526034712950601,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.943683409436834,
    0.2619047619047619,
    0.9526034712950601
  ],
  "turn_right_recall": 0.6563981042654028,
  "turn_straight_recall": 0.6262993762993763,
  "turn_left_recall": 0.7087378640776699,
  "recall_turn": [
    0.6563981042654028,
    0.6262993762993763,
    0.7087378640776699
  ],
  "cm_turn": [
    [
      554,
      204,
      86
    ],
    [
      292,
      1205,
      427
    ],
    [
      59,
      211,
      657
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
      11,
      31
    ],
    [
      131,
      11,
      2854
    ]
  ],
  "main_confidence_mean": 0.9754591474904002,
  "main_confidence_error_mean": 0.8205638068165957,
  "main_low_conf_0p60_ratio": 0.004600811907983762,
  "main_low_conf_0p70_ratio": 0.0557510148849797,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 17,
      "error_rate": 0.4117647058823529,
      "mean_confidence": 0.5629483820318882
    },
    {
      "bin": "[0.60,0.70)",
      "n": 189,
      "error_rate": 0.4444444444444444,
      "mean_confidence": 0.6571325274856504
    },
    {
      "bin": "[0.70,0.80)",
      "n": 21,
      "error_rate": 0.6666666666666666,
      "mean_confidence": 0.7551710351978433
    },
    {
      "bin": "[0.80,0.90)",
      "n": 36,
      "error_rate": 0.19444444444444445,
      "mean_confidence": 0.84915772004643
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3432,
      "error_rate": 0.028554778554778556,
      "mean_confidence": 0.9977054516686691
    }
  ],
  "turn_confidence_mean": 0.8455172024473646,
  "turn_confidence_error_mean": 0.7663772379736129,
  "turn_low_conf_0p60_ratio": 0.13369418132611638,
  "turn_low_conf_0p70_ratio": 0.22489851150202977,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 494,
      "error_rate": 0.6700404858299596,
      "mean_confidence": 0.4873132992617921
    },
    {
      "bin": "[0.60,0.70)",
      "n": 337,
      "error_rate": 0.4391691394658754,
      "mean_confidence": 0.653471888716486
    },
    {
      "bin": "[0.70,0.80)",
      "n": 330,
      "error_rate": 0.40606060606060607,
      "mean_confidence": 0.7464986346942506
    },
    {
      "bin": "[0.80,0.90)",
      "n": 483,
      "error_rate": 0.37681159420289856,
      "mean_confidence": 0.8559781024668534
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2051,
      "error_rate": 0.23598244758654316,
      "mean_confidence": 0.9768168180251771
    }
  ],
  "theta_mae_rad": 0.015287118032574654,
  "theta_mae_deg": 0.8758872747421265,
  "uphill_recall": 0.7789757412398922,
  "downhill_recall": 0.8042269187986651,
  "slope_sign_acc": 0.9709827539009034,
  "theta_flat_mae_deg": 1.032952070236206,
  "theta_flat_abs_p95_deg": 4.0177741050720215,
  "theta_flat_abs_max_deg": 6.441836357116699,
  "theta_flat_bias_deg": 0.3070959448814392,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.3415061235427856,
  "theta_near_flat_abs_p95_deg": 4.019434452056885,
  "theta_near_flat_abs_max_deg": 5.9970502853393555,
  "theta_near_flat_bias_deg": 0.8058387041091919,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.9316899180412292,
  "theta_flat_turn_abs_p95_deg": 4.0177741050720215,
  "theta_flat_turn_abs_max_deg": 5.4739251136779785,
  "theta_flat_turn_bias_deg": 0.41371017694473267,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8758872747421265,
  "theta_slope_control_abs_p95_deg": 9.526667594909668,
  "theta_slope_control_abs_max_deg": 14.216804504394531,
  "theta_slope_control_bias_deg": -0.26313960552215576,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8758872747421265,
  "theta_all_rmse_deg": 1.2237346172332764,
  "theta_all_p95_abs_err_deg": 2.519397258758545,
  "theta_all_max_abs_err_deg": 7.000709056854248,
  "theta_all_bias_deg": -0.26313960552215576,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.8414441347122192,
  "theta_active_abs_ge_2_rmse_deg": 1.1436125040054321,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2900397777557373,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.000709056854248,
  "theta_active_abs_ge_2_bias_deg": -0.3881879448890686,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9013524651527405,
  "theta_abs_le_8_rmse_deg": 1.249108076095581,
  "theta_abs_le_8_p95_abs_err_deg": 2.6296520233154297,
  "theta_abs_le_8_max_abs_err_deg": 7.000709056854248,
  "theta_abs_le_8_bias_deg": -0.22105920314788818,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8758872747421265,
  "theta_abs_le_10_rmse_deg": 1.2237346172332764,
  "theta_abs_le_10_p95_abs_err_deg": 2.519397258758545,
  "theta_abs_le_10_max_abs_err_deg": 7.000709056854248,
  "theta_abs_le_10_bias_deg": -0.26313960552215576,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6757897138595581,
  "theta_pos_8_10_rmse_deg": 0.8393291234970093,
  "theta_pos_8_10_p95_abs_err_deg": 1.364052414894104,
  "theta_pos_8_10_max_abs_err_deg": 4.539759159088135,
  "theta_pos_8_10_bias_deg": -0.48183473944664,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8627328276634216,
  "theta_neg_10_8_rmse_deg": 1.3305366039276123,
  "theta_neg_10_8_p95_abs_err_deg": 2.427182912826538,
  "theta_neg_10_8_max_abs_err_deg": 6.759294033050537,
  "theta_neg_10_8_bias_deg": -0.3987710773944855,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.639186680316925,
  "theta_pos_6_8_rmse_deg": 0.8250972628593445,
  "theta_pos_6_8_p95_abs_err_deg": 1.4859075546264648,
  "theta_pos_6_8_max_abs_err_deg": 3.4097506999969482,
  "theta_pos_6_8_bias_deg": -0.30136731266975403,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.0112541913986206,
  "theta_neg_8_6_rmse_deg": 1.4027316570281982,
  "theta_neg_8_6_p95_abs_err_deg": 2.589306592941284,
  "theta_neg_8_6_max_abs_err_deg": 7.000709056854248,
  "theta_neg_8_6_bias_deg": -0.5358384847640991,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8984818458557129,
  "theta_neg_4_2_rmse_deg": 1.19016432762146,
  "theta_neg_4_2_p95_abs_err_deg": 2.3086767196655273,
  "theta_neg_4_2_max_abs_err_deg": 5.132411956787109,
  "theta_neg_4_2_bias_deg": -0.70173579454422,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5407429337501526,
  "theta_neg_2_0p5_rmse_deg": 0.757548451423645,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.2153383493423462,
  "theta_neg_2_0p5_max_abs_err_deg": 4.3146514892578125,
  "theta_neg_2_0p5_bias_deg": -0.1715487539768219,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.2927786111831665,
  "theta_pos_0p5_2_rmse_deg": 1.6309250593185425,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.55047869682312,
  "theta_pos_0p5_2_max_abs_err_deg": 4.669863700866699,
  "theta_pos_0p5_2_bias_deg": 0.22825407981872559,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.38548570766500595,
  "loss_turn": 1.4402055470966035,
  "loss_theta": 0.0004562627141967577,
  "loss_main_bundle_base": 0.38548570766500595,
  "loss_turn_bundle_base": 0.2880411131980455,
  "loss_theta_bundle_base": 0.00030908211369410217,
  "loss_main_bundle": 0.38548570766500595,
  "loss_turn_bundle": 0.2880411131980455,
  "loss_theta_bundle": 0.00030908211369410217,
  "loss_theta_flat": 0.000329721162682626,
  "loss_theta_near_flat": 0.001130173398977012,
  "loss_theta_error_excess": 0.00014683686738552749,
  "loss_theta_flat_excess": 0.00018025933590133805,
  "loss_theta_near_flat_excess": 0.0007892498802122722,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00011229235101954354,
  "loss_theta_small_neg": 0.0004268050520033078,
  "loss_theta_small_neg_excess": 0.00010929153652824537,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.36113045234157526,
  "loss_false_turn_straight": 0.2768346103344299,
  "loss_transition_focal_raw": 1.247756656338946,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 5.129561729586012,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
