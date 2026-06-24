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
  "lambda_theta": 0.58,
  "lambda_theta_flat": 0.12,
  "theta_flat_loss_mode": "near_zero",
  "theta_flat_zero_tol_deg": 0.3,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 0.08,
  "lambda_theta_flat_excess": 0.0,
  "lambda_theta_near_flat_excess": 0.0,
  "lambda_theta_true_zero_excess": 0.1,
  "lambda_theta_active_excess": 0.04,
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
  "theta_neg_weight": 1.15,
  "theta_pos_weight": 1.5,
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
  "select_theta_flat_peak_weight": 0.9,
  "select_theta_flat_peak_target_deg": 5.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 1.6,
  "select_theta_edge_p95_target_deg": 1.1,
  "select_theta_small_nonzero_p95_weight": 0.8,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.3,
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9722 |
| acc_turn | 0.5974 |
| acc_turn_pure | 0.6145 |
| acc_turn_transition | 0.5231 |
| main_confidence_mean | 0.9879 |
| main_low_conf_0p60_ratio | 0.0108 |
| main_low_conf_0p70_ratio | 0.0172 |
| turn_confidence_mean | 0.8414 |
| turn_low_conf_0p60_ratio | 0.1330 |
| turn_low_conf_0p70_ratio | 0.2268 |
| turn_right_recall | 0.6458 |
| turn_straight_recall | 0.6110 |
| turn_left_recall | 0.5230 |
| theta_mae_deg | 0.6923 |
| theta_abs_le_10_p95_abs_err_deg | 2.1435 |
| theta_neg_10_8_p95_abs_err_deg | 1.6570 |
| theta_pos_8_10_p95_abs_err_deg | 3.2501 |
| theta_abs_le_8_p95_abs_err_deg | 2.1369 |
| theta_neg_8_6_p95_abs_err_deg | 1.5471 |
| theta_pos_6_8_p95_abs_err_deg | 1.6629 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.2544 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4875 |
| theta_flat_abs_p95_deg | 2.9277 |
| theta_flat_bias_deg | 0.1494 |
| theta_near_flat_abs_p95_deg | 2.1559 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.2451 |
| theta_flat_turn_abs_p95_deg | 2.7442 |
| flat_recall | 0.9656 |
| stall_recall | 0.7083 |
| slope_recall | 0.9833 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7695 |
| downhill_recall | 0.7877 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    730,
    0,
    26
  ],
  [
    9,
    68,
    19
  ],
  [
    33,
    13,
    2704
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    516,
    192,
    91
  ],
  [
    432,
    1181,
    320
  ],
  [
    164,
    251,
    455
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.282143 |
| test_loss_turn_bundle_base | 0.342411 |
| test_loss_theta_bundle_base | 0.000208 |
| test_loss_transition_focal_raw | 1.518584 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.169333 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 74
- train_seconds: 354.5

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 39 | 0.6154 | 0.5436 |
| [0.60,0.70) | 23 | 0.2174 | 0.6483 |
| [0.70,0.80) | 21 | 0.2381 | 0.7455 |
| [0.80,0.90) | 31 | 0.1935 | 0.8562 |
| [0.90,1.00) | 3488 | 0.0172 | 0.9978 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 479 | 0.5344 | 0.5259 |
| [0.60,0.70) | 338 | 0.5089 | 0.6523 |
| [0.70,0.80) | 444 | 0.5270 | 0.7550 |
| [0.80,0.90) | 512 | 0.4941 | 0.8489 |
| [0.90,1.00) | 1829 | 0.2925 | 0.9778 |


## 验证集最佳点

```json
{
  "loss_total": 0.6023308057746319,
  "acc_main": 0.9488497970230041,
  "acc_turn": 0.6438430311231393,
  "acc_turn_pure": 0.6555227794165848,
  "acc_turn_transition": 0.5885093167701864,
  "false_turn_straight": 0.38513513513513514,
  "flat_recall": 0.9573820395738204,
  "stall_recall": 0.5476190476190477,
  "slope_recall": 0.9526034712950601,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9573820395738204,
    0.5476190476190477,
    0.9526034712950601
  ],
  "turn_right_recall": 0.6990521327014217,
  "turn_straight_recall": 0.6148648648648649,
  "turn_left_recall": 0.6537216828478964,
  "recall_turn": [
    0.6990521327014217,
    0.6148648648648649,
    0.6537216828478964
  ],
  "cm_turn": [
    [
      590,
      213,
      41
    ],
    [
      414,
      1183,
      327
    ],
    [
      97,
      224,
      606
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      629,
      0,
      28
    ],
    [
      0,
      23,
      19
    ],
    [
      129,
      13,
      2854
    ]
  ],
  "main_confidence_mean": 0.9733951733750438,
  "main_confidence_error_mean": 0.7871928190841235,
  "main_low_conf_0p60_ratio": 0.04709066305818674,
  "main_low_conf_0p70_ratio": 0.052232746955345064,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 174,
      "error_rate": 0.45977011494252873,
      "mean_confidence": 0.5871133084555683
    },
    {
      "bin": "[0.60,0.70)",
      "n": 19,
      "error_rate": 0.47368421052631576,
      "mean_confidence": 0.6399016025943334
    },
    {
      "bin": "[0.70,0.80)",
      "n": 24,
      "error_rate": 0.2916666666666667,
      "mean_confidence": 0.7426901963169446
    },
    {
      "bin": "[0.80,0.90)",
      "n": 43,
      "error_rate": 0.2558139534883721,
      "mean_confidence": 0.8519352281772138
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3435,
      "error_rate": 0.023871906841339156,
      "mean_confidence": 0.99793931294818
    }
  ],
  "turn_confidence_mean": 0.8529487885751565,
  "turn_confidence_error_mean": 0.7800076476686771,
  "turn_low_conf_0p60_ratio": 0.15209742895805142,
  "turn_low_conf_0p70_ratio": 0.23355886332882272,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 562,
      "error_rate": 0.604982206405694,
      "mean_confidence": 0.5374992295501316
    },
    {
      "bin": "[0.60,0.70)",
      "n": 301,
      "error_rate": 0.5249169435215947,
      "mean_confidence": 0.6493377418176696
    },
    {
      "bin": "[0.70,0.80)",
      "n": 306,
      "error_rate": 0.5032679738562091,
      "mean_confidence": 0.7500689452818821
    },
    {
      "bin": "[0.80,0.90)",
      "n": 402,
      "error_rate": 0.40049751243781095,
      "mean_confidence": 0.8546613670113631
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2124,
      "error_rate": 0.23681732580037665,
      "mean_confidence": 0.9797672220791369
    }
  ],
  "theta_mae_rad": 0.013793851248919964,
  "theta_mae_deg": 0.7903293967247009,
  "uphill_recall": 0.7795148247978436,
  "downhill_recall": 0.7986651835372637,
  "slope_sign_acc": 0.9679715302491103,
  "theta_flat_mae_deg": 1.1888498067855835,
  "theta_flat_abs_p95_deg": 3.89473032951355,
  "theta_flat_abs_max_deg": 6.379548072814941,
  "theta_flat_bias_deg": 0.7591441869735718,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.6261191368103027,
  "theta_near_flat_abs_p95_deg": 3.894749879837036,
  "theta_near_flat_abs_max_deg": 6.379548072814941,
  "theta_near_flat_bias_deg": 1.2471734285354614,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.4795095920562744,
  "theta_flat_turn_abs_p95_deg": 4.224514007568359,
  "theta_flat_turn_abs_max_deg": 6.379548072814941,
  "theta_flat_turn_bias_deg": 0.987076997756958,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7903293967247009,
  "theta_slope_control_abs_p95_deg": 9.282488822937012,
  "theta_slope_control_abs_max_deg": 11.585068702697754,
  "theta_slope_control_bias_deg": 0.27017343044281006,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7903294563293457,
  "theta_all_rmse_deg": 1.1996127367019653,
  "theta_all_p95_abs_err_deg": 2.6899068355560303,
  "theta_all_max_abs_err_deg": 7.140041828155518,
  "theta_all_bias_deg": 0.27017343044281006,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7029369473457336,
  "theta_active_abs_ge_2_rmse_deg": 1.0426267385482788,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2001194953918457,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.140041828155518,
  "theta_active_abs_ge_2_bias_deg": 0.16294583678245544,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8428494334220886,
  "theta_abs_le_8_rmse_deg": 1.2511951923370361,
  "theta_abs_le_8_p95_abs_err_deg": 2.8432328701019287,
  "theta_abs_le_8_max_abs_err_deg": 7.140041828155518,
  "theta_abs_le_8_bias_deg": 0.3437335193157196,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7903294563293457,
  "theta_abs_le_10_rmse_deg": 1.1996127367019653,
  "theta_abs_le_10_p95_abs_err_deg": 2.6899068355560303,
  "theta_abs_le_10_max_abs_err_deg": 7.140041828155518,
  "theta_abs_le_10_bias_deg": 0.27017343044281006,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.558875560760498,
  "theta_pos_8_10_rmse_deg": 0.7564457654953003,
  "theta_pos_8_10_p95_abs_err_deg": 1.4974594116210938,
  "theta_pos_8_10_max_abs_err_deg": 4.534456253051758,
  "theta_pos_8_10_bias_deg": -0.3008277714252472,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.5788357257843018,
  "theta_neg_10_8_rmse_deg": 1.1158345937728882,
  "theta_neg_10_8_p95_abs_err_deg": 1.7889811992645264,
  "theta_neg_10_8_max_abs_err_deg": 6.840304374694824,
  "theta_neg_10_8_bias_deg": 0.2250451296567917,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6496955752372742,
  "theta_pos_6_8_rmse_deg": 0.9085366725921631,
  "theta_pos_6_8_p95_abs_err_deg": 2.0095176696777344,
  "theta_pos_6_8_max_abs_err_deg": 3.678372621536255,
  "theta_pos_6_8_bias_deg": -0.23166462779045105,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.6909230947494507,
  "theta_neg_8_6_rmse_deg": 1.0791085958480835,
  "theta_neg_8_6_p95_abs_err_deg": 2.1209518909454346,
  "theta_neg_8_6_max_abs_err_deg": 7.140041828155518,
  "theta_neg_8_6_bias_deg": 0.046140726655721664,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7466839551925659,
  "theta_neg_4_2_rmse_deg": 0.9699881672859192,
  "theta_neg_4_2_p95_abs_err_deg": 1.90054452419281,
  "theta_neg_4_2_max_abs_err_deg": 4.717640399932861,
  "theta_neg_4_2_bias_deg": 0.3342626690864563,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5446388125419617,
  "theta_neg_2_0p5_rmse_deg": 0.7421994805335999,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.3962000608444214,
  "theta_neg_2_0p5_max_abs_err_deg": 3.9789321422576904,
  "theta_neg_2_0p5_bias_deg": -0.009548187255859375,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.3083152770996094,
  "theta_pos_0p5_2_rmse_deg": 1.6547372341156006,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.9388539791107178,
  "theta_pos_0p5_2_max_abs_err_deg": 4.075203895568848,
  "theta_pos_0p5_2_bias_deg": 0.9494136571884155,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3276183026569299,
  "loss_turn": 1.37208711855789,
  "loss_theta": 0.00043277838220126693,
  "loss_main_bundle_base": 0.3276183026569299,
  "loss_turn_bundle_base": 0.27441742616190157,
  "loss_theta_bundle_base": 0.0002950734400656074,
  "loss_main_bundle": 0.3276183026569299,
  "loss_turn_bundle": 0.27441742616190157,
  "loss_theta_bundle": 0.0002950734400656074,
  "loss_theta_flat": 0.0002301406350472341,
  "loss_theta_near_flat": 0.0015070286792726918,
  "loss_theta_error_excess": 0.00015599036988054297,
  "loss_theta_flat_excess": 0.00013912705650462881,
  "loss_theta_near_flat_excess": 0.001081720847007598,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 9.914697298741646e-05,
  "loss_theta_small_neg": 0.00028431759127201477,
  "loss_theta_small_neg_excess": 5.641135518503387e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3586419176184276,
  "loss_false_turn_straight": 0.2834555226104669,
  "loss_transition_focal_raw": 1.1708084232591003,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.7156600886682276,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
