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
  "lambda_turn": 0.08,
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
    1.08,
    1.0,
    1.08
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 1.4,
  "select_turn_weight": 0.3,
  "select_turn_transition_weight": 1.2,
  "select_turn_transition_target": 0.82,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.88,
  "select_turn_lr_weight": 0.2,
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
| acc_main | 0.9686 |
| acc_turn | 0.6208 |
| acc_turn_pure | 0.6414 |
| acc_turn_transition | 0.5306 |
| main_confidence_mean | 0.9913 |
| main_low_conf_0p60_ratio | 0.0036 |
| main_low_conf_0p70_ratio | 0.0097 |
| turn_confidence_mean | 0.8546 |
| turn_low_conf_0p60_ratio | 0.1308 |
| turn_low_conf_0p70_ratio | 0.2213 |
| turn_right_recall | 0.5807 |
| turn_straight_recall | 0.6746 |
| turn_left_recall | 0.5379 |
| theta_mae_deg | 0.4045 |
| theta_abs_le_10_p95_abs_err_deg | 1.1018 |
| theta_neg_10_8_p95_abs_err_deg | 0.8719 |
| theta_pos_8_10_p95_abs_err_deg | 2.0482 |
| theta_abs_le_8_p95_abs_err_deg | 1.0245 |
| theta_neg_8_6_p95_abs_err_deg | 1.0319 |
| theta_pos_6_8_p95_abs_err_deg | 0.9482 |
| theta_neg_2_0p5_p95_abs_err_deg | 0.8246 |
| theta_pos_0p5_2_p95_abs_err_deg | 0.9244 |
| theta_flat_abs_p95_deg | 2.0527 |
| theta_flat_bias_deg | -0.1446 |
| theta_near_flat_abs_p95_deg | 1.6375 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1308 |
| theta_flat_turn_abs_p95_deg | 1.5700 |
| flat_recall | 0.9537 |
| stall_recall | 0.6979 |
| slope_recall | 0.9822 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1146 |
| uphill_recall | 0.7620 |
| downhill_recall | 0.7985 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    721,
    0,
    35
  ],
  [
    11,
    67,
    18
  ],
  [
    39,
    10,
    2701
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    464,
    216,
    119
  ],
  [
    304,
    1304,
    325
  ],
  [
    152,
    250,
    468
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.392169 |
| test_loss_turn_bundle_base | 0.146232 |
| test_loss_theta_bundle_base | 0.000083 |
| test_loss_transition_focal_raw | 1.795667 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.560932 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 149
- train_seconds: 1771.5

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 13 | 0.3077 | 0.5403 |
| [0.60,0.70) | 22 | 0.4091 | 0.6493 |
| [0.70,0.80) | 23 | 0.3478 | 0.7405 |
| [0.80,0.90) | 37 | 0.4595 | 0.8527 |
| [0.90,1.00) | 3507 | 0.0214 | 0.9983 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 471 | 0.5393 | 0.5198 |
| [0.60,0.70) | 326 | 0.5153 | 0.6543 |
| [0.70,0.80) | 323 | 0.5077 | 0.7528 |
| [0.80,0.90) | 433 | 0.4434 | 0.8518 |
| [0.90,1.00) | 2049 | 0.2870 | 0.9800 |


## 验证集最佳点

```json
{
  "loss_total": 0.5116105438407929,
  "acc_main": 0.9385656292286875,
  "acc_turn": 0.6630581867388363,
  "acc_turn_pure": 0.6709275647328745,
  "acc_turn_transition": 0.6257763975155279,
  "false_turn_straight": 0.33316008316008316,
  "flat_recall": 0.9162861491628614,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.9509345794392523,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9162861491628614,
    0.40476190476190477,
    0.9509345794392523
  ],
  "turn_right_recall": 0.6362559241706162,
  "turn_straight_recall": 0.6668399168399168,
  "turn_left_recall": 0.6796116504854369,
  "recall_turn": [
    0.6362559241706162,
    0.6668399168399168,
    0.6796116504854369
  ],
  "cm_turn": [
    [
      537,
      225,
      82
    ],
    [
      249,
      1283,
      392
    ],
    [
      72,
      225,
      630
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      602,
      0,
      55
    ],
    [
      0,
      17,
      25
    ],
    [
      135,
      12,
      2849
    ]
  ],
  "main_confidence_mean": 0.9689267433161634,
  "main_confidence_error_mean": 0.7552368240742866,
  "main_low_conf_0p60_ratio": 0.0516914749661705,
  "main_low_conf_0p70_ratio": 0.056562922868741546,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 191,
      "error_rate": 0.4869109947643979,
      "mean_confidence": 0.5300809362354595
    },
    {
      "bin": "[0.60,0.70)",
      "n": 18,
      "error_rate": 0.7222222222222222,
      "mean_confidence": 0.6497104773439563
    },
    {
      "bin": "[0.70,0.80)",
      "n": 25,
      "error_rate": 0.4,
      "mean_confidence": 0.7467296111588287
    },
    {
      "bin": "[0.80,0.90)",
      "n": 47,
      "error_rate": 0.5319148936170213,
      "mean_confidence": 0.861542298849238
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3414,
      "error_rate": 0.025190392501464556,
      "mean_confidence": 0.9982669422422891
    }
  ],
  "turn_confidence_mean": 0.8650290931841623,
  "turn_confidence_error_mean": 0.7799108761850411,
  "turn_low_conf_0p60_ratio": 0.1253044654939107,
  "turn_low_conf_0p70_ratio": 0.19052774018944518,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 463,
      "error_rate": 0.6436285097192225,
      "mean_confidence": 0.4659914795613617
    },
    {
      "bin": "[0.60,0.70)",
      "n": 241,
      "error_rate": 0.43568464730290457,
      "mean_confidence": 0.6499941430634625
    },
    {
      "bin": "[0.70,0.80)",
      "n": 287,
      "error_rate": 0.5121951219512195,
      "mean_confidence": 0.7495260664609935
    },
    {
      "bin": "[0.80,0.90)",
      "n": 390,
      "error_rate": 0.4025641025641026,
      "mean_confidence": 0.8513338562745635
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2314,
      "error_rate": 0.23249783923941228,
      "mean_confidence": 0.9839004627393646
    }
  ],
  "theta_mae_rad": 0.010425267741084099,
  "theta_mae_deg": 0.5973238348960876,
  "uphill_recall": 0.7778975741239892,
  "downhill_recall": 0.8125695216907676,
  "slope_sign_acc": 0.9802901724609909,
  "theta_flat_mae_deg": 0.9424095153808594,
  "theta_flat_abs_p95_deg": 4.688273906707764,
  "theta_flat_abs_max_deg": 6.0687079429626465,
  "theta_flat_bias_deg": 0.5030983090400696,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.2819112539291382,
  "theta_near_flat_abs_p95_deg": 4.688288688659668,
  "theta_near_flat_abs_max_deg": 6.059548854827881,
  "theta_near_flat_bias_deg": 0.8906651735305786,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.7446244955062866,
  "theta_flat_turn_abs_p95_deg": 4.688273906707764,
  "theta_flat_turn_abs_max_deg": 4.688273906707764,
  "theta_flat_turn_bias_deg": 0.4672960638999939,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.5973238348960876,
  "theta_slope_control_abs_p95_deg": 9.228129386901855,
  "theta_slope_control_abs_max_deg": 10.880899429321289,
  "theta_slope_control_bias_deg": 0.06560634076595306,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.5973238348960876,
  "theta_all_rmse_deg": 1.003378987312317,
  "theta_all_p95_abs_err_deg": 2.1882741451263428,
  "theta_all_max_abs_err_deg": 6.234856605529785,
  "theta_all_bias_deg": 0.06560634076595306,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.5216491222381592,
  "theta_active_abs_ge_2_rmse_deg": 0.8078911900520325,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.6140633821487427,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.234856605529785,
  "theta_active_abs_ge_2_bias_deg": -0.03033231757581234,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.6268269419670105,
  "theta_abs_le_8_rmse_deg": 1.0518755912780762,
  "theta_abs_le_8_p95_abs_err_deg": 2.47700572013855,
  "theta_abs_le_8_max_abs_err_deg": 6.234856605529785,
  "theta_abs_le_8_bias_deg": 0.09948980808258057,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.5973238348960876,
  "theta_abs_le_10_rmse_deg": 1.003378987312317,
  "theta_abs_le_10_p95_abs_err_deg": 2.1882741451263428,
  "theta_abs_le_10_max_abs_err_deg": 6.234856605529785,
  "theta_abs_le_10_bias_deg": 0.06560634076595306,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.4597426950931549,
  "theta_pos_8_10_rmse_deg": 0.6186143159866333,
  "theta_pos_8_10_p95_abs_err_deg": 1.226275086402893,
  "theta_pos_8_10_max_abs_err_deg": 3.8245205879211426,
  "theta_pos_8_10_bias_deg": -0.28695639967918396,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.4862096607685089,
  "theta_neg_10_8_rmse_deg": 0.8907414078712463,
  "theta_neg_10_8_p95_abs_err_deg": 1.4949564933776855,
  "theta_neg_10_8_max_abs_err_deg": 6.063300132751465,
  "theta_neg_10_8_bias_deg": 0.13591401278972626,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.4652598798274994,
  "theta_pos_6_8_rmse_deg": 0.7443788647651672,
  "theta_pos_6_8_p95_abs_err_deg": 1.4360198974609375,
  "theta_pos_6_8_max_abs_err_deg": 3.787858009338379,
  "theta_pos_6_8_bias_deg": -0.14995618164539337,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.4868544936180115,
  "theta_neg_8_6_rmse_deg": 0.7742936611175537,
  "theta_neg_8_6_p95_abs_err_deg": 1.23074471950531,
  "theta_neg_8_6_max_abs_err_deg": 6.234856605529785,
  "theta_neg_8_6_bias_deg": -0.06170976907014847,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.48637574911117554,
  "theta_neg_4_2_rmse_deg": 0.7308328151702881,
  "theta_neg_4_2_p95_abs_err_deg": 1.3747355937957764,
  "theta_neg_4_2_max_abs_err_deg": 6.01206636428833,
  "theta_neg_4_2_bias_deg": -0.09888803958892822,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.4253396987915039,
  "theta_neg_2_0p5_rmse_deg": 0.5817919373512268,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.090133547782898,
  "theta_neg_2_0p5_max_abs_err_deg": 3.281170606613159,
  "theta_neg_2_0p5_bias_deg": -0.09508341550827026,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0466324090957642,
  "theta_pos_0p5_2_rmse_deg": 1.65690279006958,
  "theta_pos_0p5_2_p95_abs_err_deg": 3.1882741451263428,
  "theta_pos_0p5_2_max_abs_err_deg": 4.296735763549805,
  "theta_pos_0p5_2_bias_deg": 0.6354818344116211,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3834522088906439,
  "loss_turn": 1.599368135629068,
  "loss_theta": 0.00030667512018028116,
  "loss_main_bundle_base": 0.3834522088906439,
  "loss_turn_bundle_base": 0.12794944700836652,
  "loss_theta_bundle_base": 0.0002088841233599089,
  "loss_main_bundle": 0.3834522088906439,
  "loss_turn_bundle": 0.12794944700836652,
  "loss_theta_bundle": 0.0002088841233599089,
  "loss_theta_flat": 0.00024084422729148702,
  "loss_theta_near_flat": 0.0013428064906611755,
  "loss_theta_error_excess": 0.00011793457709323094,
  "loss_theta_flat_excess": 0.0001558004352800499,
  "loss_theta_near_flat_excess": 0.0009962726794375443,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 5.414764859514495e-05,
  "loss_theta_small_neg": 0.00015838011504665738,
  "loss_theta_small_neg_excess": 3.447354071484047e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3133161433333473,
  "loss_false_turn_straight": 0.2454933587849866,
  "loss_transition_focal_raw": 1.4353731569321133,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.853938226455207,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
