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
| acc_main | 0.9650 |
| acc_turn | 0.5911 |
| acc_turn_pure | 0.6124 |
| acc_turn_transition | 0.4978 |
| main_confidence_mean | 0.9891 |
| main_low_conf_0p60_ratio | 0.0094 |
| main_low_conf_0p70_ratio | 0.0147 |
| turn_confidence_mean | 0.8424 |
| turn_low_conf_0p60_ratio | 0.1391 |
| turn_low_conf_0p70_ratio | 0.2418 |
| turn_right_recall | 0.6070 |
| turn_straight_recall | 0.5810 |
| turn_left_recall | 0.5989 |
| theta_mae_deg | 0.6045 |
| theta_abs_le_10_p95_abs_err_deg | 1.6292 |
| theta_neg_10_8_p95_abs_err_deg | 2.6309 |
| theta_pos_8_10_p95_abs_err_deg | 2.8147 |
| theta_abs_le_8_p95_abs_err_deg | 1.5218 |
| theta_neg_8_6_p95_abs_err_deg | 1.2258 |
| theta_pos_6_8_p95_abs_err_deg | 1.3314 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.5215 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5854 |
| theta_flat_abs_p95_deg | 2.6354 |
| theta_flat_bias_deg | -0.3288 |
| theta_near_flat_abs_p95_deg | 2.0265 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.4573 |
| theta_flat_turn_abs_p95_deg | 1.9415 |
| flat_recall | 0.9497 |
| stall_recall | 0.6458 |
| slope_recall | 0.9804 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7603 |
| downhill_recall | 0.7991 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    718,
    0,
    38
  ],
  [
    9,
    62,
    25
  ],
  [
    44,
    10,
    2696
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    485,
    178,
    136
  ],
  [
    352,
    1123,
    458
  ],
  [
    165,
    184,
    521
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.353357 |
| test_loss_turn_bundle_base | 0.370754 |
| test_loss_theta_bundle_base | 0.000162 |
| test_loss_transition_focal_raw | 1.829659 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.688387 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 90
- train_seconds: 386.9

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 34 | 0.3824 | 0.5465 |
| [0.60,0.70) | 19 | 0.7368 | 0.6437 |
| [0.70,0.80) | 25 | 0.4400 | 0.7527 |
| [0.80,0.90) | 38 | 0.3684 | 0.8570 |
| [0.90,1.00) | 3486 | 0.0212 | 0.9984 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 501 | 0.6008 | 0.5187 |
| [0.60,0.70) | 370 | 0.5351 | 0.6497 |
| [0.70,0.80) | 368 | 0.4348 | 0.7517 |
| [0.80,0.90) | 454 | 0.5000 | 0.8528 |
| [0.90,1.00) | 1909 | 0.3075 | 0.9796 |


## 验证集最佳点

```json
{
  "loss_total": 0.689018303599506,
  "acc_main": 0.9418132611637348,
  "acc_turn": 0.6449255751014885,
  "acc_turn_pure": 0.655850540806293,
  "acc_turn_transition": 0.593167701863354,
  "false_turn_straight": 0.4074844074844075,
  "flat_recall": 0.9360730593607306,
  "stall_recall": 0.4523809523809524,
  "slope_recall": 0.9499332443257676,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.023809523809523808,
  "recall_main": [
    0.9360730593607306,
    0.4523809523809524,
    0.9499332443257676
  ],
  "turn_right_recall": 0.6386255924170616,
  "turn_straight_recall": 0.5925155925155925,
  "turn_left_recall": 0.7594390507011867,
  "recall_turn": [
    0.6386255924170616,
    0.5925155925155925,
    0.7594390507011867
  ],
  "cm_turn": [
    [
      539,
      213,
      92
    ],
    [
      313,
      1140,
      471
    ],
    [
      59,
      164,
      704
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      615,
      0,
      42
    ],
    [
      1,
      19,
      22
    ],
    [
      139,
      11,
      2846
    ]
  ],
  "main_confidence_mean": 0.9686353439268761,
  "main_confidence_error_mean": 0.7505728083759279,
  "main_low_conf_0p60_ratio": 0.0503382949932341,
  "main_low_conf_0p70_ratio": 0.056833558863328824,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 186,
      "error_rate": 0.478494623655914,
      "mean_confidence": 0.5105872707896232
    },
    {
      "bin": "[0.60,0.70)",
      "n": 24,
      "error_rate": 0.5,
      "mean_confidence": 0.6466904065431711
    },
    {
      "bin": "[0.70,0.80)",
      "n": 25,
      "error_rate": 0.52,
      "mean_confidence": 0.7521964669234751
    },
    {
      "bin": "[0.80,0.90)",
      "n": 33,
      "error_rate": 0.2727272727272727,
      "mean_confidence": 0.8452916109513366
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3427,
      "error_rate": 0.026845637583892617,
      "mean_confidence": 0.9985171458568487
    }
  ],
  "turn_confidence_mean": 0.8561910164195763,
  "turn_confidence_error_mean": 0.777860738471573,
  "turn_low_conf_0p60_ratio": 0.13748308525033828,
  "turn_low_conf_0p70_ratio": 0.21732070365358594,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 508,
      "error_rate": 0.65748031496063,
      "mean_confidence": 0.4994629412864324
    },
    {
      "bin": "[0.60,0.70)",
      "n": 295,
      "error_rate": 0.44745762711864406,
      "mean_confidence": 0.6515159176969688
    },
    {
      "bin": "[0.70,0.80)",
      "n": 299,
      "error_rate": 0.4983277591973244,
      "mean_confidence": 0.7499948246717765
    },
    {
      "bin": "[0.80,0.90)",
      "n": 407,
      "error_rate": 0.4250614250614251,
      "mean_confidence": 0.8537321477634394
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2186,
      "error_rate": 0.23970722781335774,
      "mean_confidence": 0.9816944186000182
    }
  ],
  "theta_mae_rad": 0.013932321220636368,
  "theta_mae_deg": 0.7982631325721741,
  "uphill_recall": 0.7773584905660378,
  "downhill_recall": 0.8042269187986651,
  "slope_sign_acc": 0.9679715302491103,
  "theta_flat_mae_deg": 1.1549001932144165,
  "theta_flat_abs_p95_deg": 4.094296455383301,
  "theta_flat_abs_max_deg": 5.392411231994629,
  "theta_flat_bias_deg": 0.307169646024704,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4490584135055542,
  "theta_near_flat_abs_p95_deg": 4.097597122192383,
  "theta_near_flat_abs_max_deg": 5.530945777893066,
  "theta_near_flat_bias_deg": 0.724495530128479,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.0485762357711792,
  "theta_flat_turn_abs_p95_deg": 4.094291687011719,
  "theta_flat_turn_abs_max_deg": 5.368081092834473,
  "theta_flat_turn_bias_deg": 0.31958574056625366,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7982631325721741,
  "theta_slope_control_abs_p95_deg": 9.400269508361816,
  "theta_slope_control_abs_max_deg": 13.006309509277344,
  "theta_slope_control_bias_deg": -0.1489982306957245,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7982631325721741,
  "theta_all_rmse_deg": 1.1603143215179443,
  "theta_all_p95_abs_err_deg": 2.594291925430298,
  "theta_all_max_abs_err_deg": 6.690182685852051,
  "theta_all_bias_deg": -0.1489982306957245,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.720055341720581,
  "theta_active_abs_ge_2_rmse_deg": 1.0172992944717407,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.8805304765701294,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.690182685852051,
  "theta_active_abs_ge_2_bias_deg": -0.24903236329555511,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8317668437957764,
  "theta_abs_le_8_rmse_deg": 1.1999984979629517,
  "theta_abs_le_8_p95_abs_err_deg": 2.594291925430298,
  "theta_abs_le_8_max_abs_err_deg": 6.690182685852051,
  "theta_abs_le_8_bias_deg": -0.1063125878572464,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7982631325721741,
  "theta_abs_le_10_rmse_deg": 1.1603143215179443,
  "theta_abs_le_10_p95_abs_err_deg": 2.594291925430298,
  "theta_abs_le_10_max_abs_err_deg": 6.690182685852051,
  "theta_abs_le_10_bias_deg": -0.1489982306957245,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6827356219291687,
  "theta_pos_8_10_rmse_deg": 0.8774592876434326,
  "theta_pos_8_10_p95_abs_err_deg": 1.4059092998504639,
  "theta_pos_8_10_max_abs_err_deg": 5.168830871582031,
  "theta_pos_8_10_bias_deg": -0.4407518804073334,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6306690573692322,
  "theta_neg_10_8_rmse_deg": 1.065632939338684,
  "theta_neg_10_8_p95_abs_err_deg": 1.808810830116272,
  "theta_neg_10_8_max_abs_err_deg": 6.216066360473633,
  "theta_neg_10_8_bias_deg": -0.21545836329460144,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6014726161956787,
  "theta_pos_6_8_rmse_deg": 0.8063166737556458,
  "theta_pos_6_8_p95_abs_err_deg": 1.4978241920471191,
  "theta_pos_6_8_max_abs_err_deg": 3.2148818969726562,
  "theta_pos_6_8_bias_deg": -0.3282766342163086,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8149492740631104,
  "theta_neg_8_6_rmse_deg": 1.1894859075546265,
  "theta_neg_8_6_p95_abs_err_deg": 2.2997372150421143,
  "theta_neg_8_6_max_abs_err_deg": 6.690182685852051,
  "theta_neg_8_6_bias_deg": -0.5061245560646057,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6830019354820251,
  "theta_neg_4_2_rmse_deg": 0.955022394657135,
  "theta_neg_4_2_p95_abs_err_deg": 1.8184572458267212,
  "theta_neg_4_2_max_abs_err_deg": 4.379635334014893,
  "theta_neg_4_2_bias_deg": -0.278507262468338,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6149400472640991,
  "theta_neg_2_0p5_rmse_deg": 0.8227637410163879,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.5711369514465332,
  "theta_neg_2_0p5_max_abs_err_deg": 3.614928960800171,
  "theta_neg_2_0p5_bias_deg": -0.4398239254951477,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.310228943824768,
  "theta_pos_0p5_2_rmse_deg": 1.6012704372406006,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.594291925430298,
  "theta_pos_0p5_2_max_abs_err_deg": 3.620438814163208,
  "theta_pos_0p5_2_bias_deg": 0.5132763385772705,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3664053082627437,
  "loss_turn": 1.6117041049371392,
  "loss_theta": 0.0004099433637364025,
  "loss_main_bundle_base": 0.3664053082627437,
  "loss_turn_bundle_base": 0.32234082653493457,
  "loss_theta_bundle_base": 0.0002721830850346732,
  "loss_main_bundle": 0.3664053082627437,
  "loss_turn_bundle": 0.32234082653493457,
  "loss_theta_bundle": 0.0002721830850346732,
  "loss_theta_flat": 0.00026067307331583225,
  "loss_theta_near_flat": 0.0013306878495480013,
  "loss_theta_error_excess": 0.0001368302154368614,
  "loss_theta_flat_excess": 0.00014295877563654972,
  "loss_theta_near_flat_excess": 0.0009458634303567657,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 8.591953136108145e-05,
  "loss_theta_small_neg": 0.0002775460808914084,
  "loss_theta_small_neg_excess": 6.720235883412664e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3649322371118285,
  "loss_false_turn_straight": 0.30343726976637264,
  "loss_transition_focal_raw": 1.4351710059162084,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.120144800952716,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
