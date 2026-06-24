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
  "lambda_theta_flat": 0.14,
  "theta_flat_loss_mode": "near_zero",
  "theta_flat_zero_tol_deg": 0.3,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 0.04,
  "lambda_theta_flat_excess": 0.06,
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
  "select_theta_flat_peak_weight": 1.2,
  "select_theta_flat_peak_target_deg": 5.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 1.0,
  "select_theta_edge_p95_target_deg": 1.2,
  "select_theta_small_nonzero_p95_weight": 0.8,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.3,
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9667 |
| acc_turn | 0.5702 |
| acc_turn_pure | 0.5793 |
| acc_turn_transition | 0.5306 |
| main_confidence_mean | 0.9878 |
| main_low_conf_0p60_ratio | 0.0064 |
| main_low_conf_0p70_ratio | 0.0139 |
| turn_confidence_mean | 0.7940 |
| turn_low_conf_0p60_ratio | 0.2077 |
| turn_low_conf_0p70_ratio | 0.3270 |
| turn_right_recall | 0.6433 |
| turn_straight_recall | 0.5556 |
| turn_left_recall | 0.5356 |
| theta_mae_deg | 0.5781 |
| theta_abs_le_10_p95_abs_err_deg | 1.5368 |
| theta_neg_10_8_p95_abs_err_deg | 1.4724 |
| theta_pos_8_10_p95_abs_err_deg | 2.5248 |
| theta_abs_le_8_p95_abs_err_deg | 1.4585 |
| theta_neg_8_6_p95_abs_err_deg | 1.4623 |
| theta_pos_6_8_p95_abs_err_deg | 1.4480 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.5447 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.3548 |
| theta_flat_abs_p95_deg | 2.5037 |
| theta_flat_bias_deg | 0.1419 |
| theta_near_flat_abs_p95_deg | 1.8335 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.3273 |
| theta_flat_turn_abs_p95_deg | 1.6452 |
| flat_recall | 0.9669 |
| stall_recall | 0.6667 |
| slope_recall | 0.9771 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7597 |
| downhill_recall | 0.7872 |

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
    55,
    8,
    2687
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    514,
    189,
    96
  ],
  [
    486,
    1074,
    373
  ],
  [
    183,
    221,
    466
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.318677 |
| test_loss_turn_bundle_base | 0.288312 |
| test_loss_theta_bundle_base | 0.000129 |
| test_loss_transition_focal_raw | 1.232951 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.630655 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 67
- train_seconds: 317.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 23 | 0.3913 | 0.5631 |
| [0.60,0.70) | 27 | 0.3333 | 0.6540 |
| [0.70,0.80) | 28 | 0.3929 | 0.7530 |
| [0.80,0.90) | 62 | 0.4839 | 0.8556 |
| [0.90,1.00) | 3462 | 0.0176 | 0.9975 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 748 | 0.6070 | 0.5195 |
| [0.60,0.70) | 430 | 0.5419 | 0.6511 |
| [0.70,0.80) | 478 | 0.4644 | 0.7520 |
| [0.80,0.90) | 490 | 0.5184 | 0.8510 |
| [0.90,1.00) | 1456 | 0.2644 | 0.9719 |


## 验证集最佳点

```json
{
  "loss_total": 0.5534307841357746,
  "acc_main": 0.9420838971583221,
  "acc_turn": 0.6330175913396482,
  "acc_turn_pure": 0.6450344149459194,
  "acc_turn_transition": 0.5760869565217391,
  "false_turn_straight": 0.4319126819126819,
  "flat_recall": 0.9421613394216134,
  "stall_recall": 0.35714285714285715,
  "slope_recall": 0.9502670226969292,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9421613394216134,
    0.35714285714285715,
    0.9502670226969292
  ],
  "turn_right_recall": 0.7085308056872038,
  "turn_straight_recall": 0.568087318087318,
  "turn_left_recall": 0.6990291262135923,
  "recall_turn": [
    0.7085308056872038,
    0.568087318087318,
    0.6990291262135923
  ],
  "cm_turn": [
    [
      598,
      198,
      48
    ],
    [
      449,
      1093,
      382
    ],
    [
      109,
      170,
      648
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      619,
      0,
      38
    ],
    [
      0,
      15,
      27
    ],
    [
      135,
      14,
      2847
    ]
  ],
  "main_confidence_mean": 0.9716937802041989,
  "main_confidence_error_mean": 0.7903897665792237,
  "main_low_conf_0p60_ratio": 0.010284167794316644,
  "main_low_conf_0p70_ratio": 0.06197564276048714,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 38,
      "error_rate": 0.5263157894736842,
      "mean_confidence": 0.5489827995344599
    },
    {
      "bin": "[0.60,0.70)",
      "n": 191,
      "error_rate": 0.4607329842931937,
      "mean_confidence": 0.654939794233408
    },
    {
      "bin": "[0.70,0.80)",
      "n": 32,
      "error_rate": 0.375,
      "mean_confidence": 0.7511878516850304
    },
    {
      "bin": "[0.80,0.90)",
      "n": 44,
      "error_rate": 0.20454545454545456,
      "mean_confidence": 0.8555494662867079
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3390,
      "error_rate": 0.025073746312684365,
      "mean_confidence": 0.9978676941012059
    }
  ],
  "turn_confidence_mean": 0.8009612169348802,
  "turn_confidence_error_mean": 0.7179461437327627,
  "turn_low_conf_0p60_ratio": 0.19512855209742896,
  "turn_low_conf_0p70_ratio": 0.30365358592692826,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 721,
      "error_rate": 0.5866851595006934,
      "mean_confidence": 0.490064108913427
    },
    {
      "bin": "[0.60,0.70)",
      "n": 401,
      "error_rate": 0.5286783042394015,
      "mean_confidence": 0.6510574231563833
    },
    {
      "bin": "[0.70,0.80)",
      "n": 466,
      "error_rate": 0.4313304721030043,
      "mean_confidence": 0.751079674251829
    },
    {
      "bin": "[0.80,0.90)",
      "n": 478,
      "error_rate": 0.3807531380753138,
      "mean_confidence": 0.8501744577897286
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1629,
      "error_rate": 0.20748925721301412,
      "mean_confidence": 0.9752946153083177
    }
  ],
  "theta_mae_rad": 0.012565969489514828,
  "theta_mae_deg": 0.7199769616127014,
  "uphill_recall": 0.7789757412398922,
  "downhill_recall": 0.8008898776418243,
  "slope_sign_acc": 0.9690665206679442,
  "theta_flat_mae_deg": 1.0693778991699219,
  "theta_flat_abs_p95_deg": 4.1747260093688965,
  "theta_flat_abs_max_deg": 7.740776062011719,
  "theta_flat_bias_deg": 0.8680863976478577,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5082660913467407,
  "theta_near_flat_abs_p95_deg": 4.174802303314209,
  "theta_near_flat_abs_max_deg": 7.740776062011719,
  "theta_near_flat_bias_deg": 1.378032922744751,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.287126064300537,
  "theta_flat_turn_abs_p95_deg": 4.180063724517822,
  "theta_flat_turn_abs_max_deg": 7.740776062011719,
  "theta_flat_turn_bias_deg": 1.1140990257263184,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7199769616127014,
  "theta_slope_control_abs_p95_deg": 9.199850082397461,
  "theta_slope_control_abs_max_deg": 11.431386947631836,
  "theta_slope_control_bias_deg": 0.18083789944648743,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.719977080821991,
  "theta_all_rmse_deg": 1.1458513736724854,
  "theta_all_p95_abs_err_deg": 2.5439038276672363,
  "theta_all_max_abs_err_deg": 8.240776062011719,
  "theta_all_bias_deg": 0.18083789944648743,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6433560848236084,
  "theta_active_abs_ge_2_rmse_deg": 0.9721036553382874,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.1063485145568848,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.6234259605407715,
  "theta_active_abs_ge_2_bias_deg": 0.030129527673125267,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7554259896278381,
  "theta_abs_le_8_rmse_deg": 1.1933071613311768,
  "theta_abs_le_8_p95_abs_err_deg": 2.6747257709503174,
  "theta_abs_le_8_max_abs_err_deg": 8.240776062011719,
  "theta_abs_le_8_bias_deg": 0.25576335191726685,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.719977080821991,
  "theta_abs_le_10_rmse_deg": 1.1458513736724854,
  "theta_abs_le_10_p95_abs_err_deg": 2.5439038276672363,
  "theta_abs_le_10_max_abs_err_deg": 8.240776062011719,
  "theta_abs_le_10_bias_deg": 0.18083789944648743,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6111018061637878,
  "theta_pos_8_10_rmse_deg": 0.8421839475631714,
  "theta_pos_8_10_p95_abs_err_deg": 1.747003436088562,
  "theta_pos_8_10_max_abs_err_deg": 4.667735576629639,
  "theta_pos_8_10_bias_deg": -0.3963296711444855,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.5290613770484924,
  "theta_neg_10_8_rmse_deg": 0.9911797642707825,
  "theta_neg_10_8_p95_abs_err_deg": 1.853438138961792,
  "theta_neg_10_8_max_abs_err_deg": 6.6234259605407715,
  "theta_neg_10_8_bias_deg": 0.130363330245018,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5546031594276428,
  "theta_pos_6_8_rmse_deg": 0.8243844509124756,
  "theta_pos_6_8_p95_abs_err_deg": 1.6393331289291382,
  "theta_pos_6_8_max_abs_err_deg": 3.647639274597168,
  "theta_pos_6_8_bias_deg": -0.2102537602186203,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.633185625076294,
  "theta_neg_8_6_rmse_deg": 0.9918505549430847,
  "theta_neg_8_6_p95_abs_err_deg": 2.0173683166503906,
  "theta_neg_8_6_max_abs_err_deg": 6.554426670074463,
  "theta_neg_8_6_bias_deg": -0.04233880341053009,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6138835549354553,
  "theta_neg_4_2_rmse_deg": 0.9070014953613281,
  "theta_neg_4_2_p95_abs_err_deg": 1.8845232725143433,
  "theta_neg_4_2_max_abs_err_deg": 5.554545879364014,
  "theta_neg_4_2_bias_deg": -0.09066300839185715,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.42684924602508545,
  "theta_neg_2_0p5_rmse_deg": 0.6830024123191833,
  "theta_neg_2_0p5_p95_abs_err_deg": 0.8882350921630859,
  "theta_neg_2_0p5_max_abs_err_deg": 5.018975734710693,
  "theta_neg_2_0p5_bias_deg": 0.1266331970691681,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1740193367004395,
  "theta_pos_0p5_2_rmse_deg": 1.5359959602355957,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.6747257709503174,
  "theta_pos_0p5_2_max_abs_err_deg": 4.007188320159912,
  "theta_pos_0p5_2_bias_deg": 0.957801103591919,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3327950365327208,
  "loss_turn": 1.101822607943105,
  "loss_theta": 0.00040004216258997586,
  "loss_main_bundle_base": 0.3327950365327208,
  "loss_turn_bundle_base": 0.22036452324045205,
  "loss_theta_bundle_base": 0.00027122594227419513,
  "loss_main_bundle": 0.3327950365327208,
  "loss_turn_bundle": 0.22036452324045205,
  "loss_theta_bundle": 0.00027122594227419513,
  "loss_theta_flat": 0.00020730704459021582,
  "loss_theta_near_flat": 0.0015104560312879283,
  "loss_theta_error_excess": 0.00015371560603657456,
  "loss_theta_flat_excess": 0.00012536470801955473,
  "loss_theta_near_flat_excess": 0.0011279496127526566,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 8.509260736905538e-05,
  "loss_theta_small_neg": 0.0002475173584360715,
  "loss_theta_small_neg_excess": 6.4681905122264e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3767830934753599,
  "loss_false_turn_straight": 0.3005767345912402,
  "loss_transition_focal_raw": 0.8173838150033448,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.117230846110797,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
