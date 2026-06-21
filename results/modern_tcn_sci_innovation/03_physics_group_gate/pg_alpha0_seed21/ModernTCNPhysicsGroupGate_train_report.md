# PG-ModernTCN-small physics-group residual gate 训练报告

## 固定约束

- model_family: `small_physics_group_gate`
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

## E3 Physics-Group Residual Gate

- residual insertion: trunk-level `[B, channels, T]`, before original small readout and heads.
- gate statistics policy: true main labels and dataset `turn_transition` mask.
- alpha0 note: alpha_init=0.0 can warm up slowly because the branch is initially gated by alpha.
- alpha_final: `0.20843320`
- physics_group_names: `['yaw_steering', 'drive_current_load', 'velocity_acceleration', 'wheel_imbalance']`

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
  "branch_channels": 16,
  "branch_kernel": 31,
  "alpha_init": 0.0,
  "gate_hidden": 32,
  "physics_group_spec": "default_22d_agv",
  "physics_group_names": [
    "yaw_steering",
    "drive_current_load",
    "velocity_acceleration",
    "wheel_imbalance"
  ],
  "physics_group_indices": [
    [
      0,
      5,
      6,
      13,
      21
    ],
    [
      1,
      2,
      10,
      11,
      12,
      17,
      19,
      18,
      14
    ],
    [
      7,
      8,
      15,
      16,
      20
    ],
    [
      3,
      4,
      9
    ]
  ]
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9572 |
| acc_turn | 0.5777 |
| acc_turn_pure | 0.5937 |
| acc_turn_transition | 0.5082 |
| main_confidence_mean | 0.9861 |
| main_low_conf_0p60_ratio | 0.0053 |
| main_low_conf_0p70_ratio | 0.0128 |
| turn_confidence_mean | 0.7769 |
| turn_low_conf_0p60_ratio | 0.2326 |
| turn_low_conf_0p70_ratio | 0.3690 |
| turn_right_recall | 0.5494 |
| turn_straight_recall | 0.6337 |
| turn_left_recall | 0.4793 |
| theta_mae_deg | 0.6577 |
| theta_abs_le_10_p95_abs_err_deg | 1.8964 |
| theta_neg_10_8_p95_abs_err_deg | 2.2878 |
| theta_pos_8_10_p95_abs_err_deg | 3.4222 |
| theta_abs_le_8_p95_abs_err_deg | 1.6701 |
| theta_neg_8_6_p95_abs_err_deg | 1.7825 |
| theta_pos_6_8_p95_abs_err_deg | 1.6597 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6557 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.3317 |
| theta_flat_abs_p95_deg | 2.6235 |
| theta_flat_bias_deg | -0.0888 |
| theta_near_flat_abs_p95_deg | 1.3989 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.0628 |
| theta_flat_turn_abs_p95_deg | 1.4965 |
| flat_recall | 0.9206 |
| stall_recall | 0.6354 |
| slope_recall | 0.9785 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7529 |
| downhill_recall | 0.8161 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    696,
    0,
    60
  ],
  [
    10,
    61,
    25
  ],
  [
    51,
    8,
    2691
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    439,
    265,
    95
  ],
  [
    390,
    1225,
    318
  ],
  [
    180,
    273,
    417
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.413328 |
| test_loss_turn_bundle_base | 0.277830 |
| test_loss_theta_bundle_base | 0.000171 |
| test_loss_transition_focal_raw | 1.156440 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.233355 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |

- best_epoch: 46
- train_seconds: 294.4

## E3 Gate Statistics

| metric | value |
|---|---:|
| test_gate_all_finite | True |
| test_gate_single_collapse | False |
| test_gate_mean_entropy | 0.111430 |
| test_gate_interpretability_score | 1.000000 |
| test_gate_yaw_transition_minus_overall | -0.021927 |
| test_gate_drive_stall_minus_overall | 0.129110 |
| test_gate_velocity_slope_flat_abs_delta | 0.000068 |

```json
{
  "prefix": "test",
  "stat_label_policy": "true label for main class; dataset turn_transition mask for transition",
  "group_names": [
    "yaw_steering",
    "drive_current_load",
    "velocity_acceleration",
    "wheel_imbalance"
  ],
  "all_finite": true,
  "single_collapse": false,
  "mean_entropy": 0.11142974346876144,
  "overall": {
    "yaw_steering": {
      "n": 3602,
      "mean": 0.23363876342773438,
      "std": 0.4037184715270996
    },
    "drive_current_load": {
      "n": 3602,
      "mean": 0.479098379611969,
      "std": 0.4679017961025238
    },
    "velocity_acceleration": {
      "n": 3602,
      "mean": 4.1353589040227234e-05,
      "std": 0.0001599408860784024
    },
    "wheel_imbalance": {
      "n": 3602,
      "mean": 0.2872215211391449,
      "std": 0.43360865116119385
    }
  },
  "by_main_true": {
    "flat": {
      "yaw_steering": {
        "n": 756,
        "mean": 0.023930992931127548,
        "std": 0.0945868119597435
      },
      "drive_current_load": {
        "n": 756,
        "mean": 0.6583878397941589,
        "std": 0.4382423162460327
      },
      "velocity_acceleration": {
        "n": 756,
        "mean": 9.386199235450476e-05,
        "std": 0.0002763155789580196
      },
      "wheel_imbalance": {
        "n": 756,
        "mean": 0.31758731603622437,
        "std": 0.4438282251358032
      }
    },
    "stall": {
      "yaw_steering": {
        "n": 96,
        "mean": 0.3799106180667877,
        "std": 0.4556116759777069
      },
      "drive_current_load": {
        "n": 96,
        "mean": 0.6082081198692322,
        "std": 0.4633888900279999
      },
      "velocity_acceleration": {
        "n": 96,
        "mean": 7.727761840214953e-05,
        "std": 0.0002345420653000474
      },
      "wheel_imbalance": {
        "n": 96,
        "mean": 0.011803987435996532,
        "std": 0.05336308851838112
      }
    },
    "slope": {
      "yaw_steering": {
        "n": 2750,
        "mean": 0.28618311882019043,
        "std": 0.4337993264198303
      },
      "drive_current_load": {
        "n": 2750,
        "mean": 0.4253029525279999,
        "std": 0.4627682566642761
      },
      "velocity_acceleration": {
        "n": 2750,
        "mean": 2.566447619756218e-05,
        "std": 9.771223267307505e-05
      },
      "wheel_imbalance": {
        "n": 2750,
        "mean": 0.2884882688522339,
        "std": 0.43487051129341125
      }
    }
  },
  "turn_transition": {
    "yaw_steering": {
      "n": 671,
      "mean": 0.21171197295188904,
      "std": 0.3944787383079529
    },
    "drive_current_load": {
      "n": 671,
      "mean": 0.5040322542190552,
      "std": 0.4703752398490906
    },
    "velocity_acceleration": {
      "n": 671,
      "mean": 4.1897717892425135e-05,
      "std": 0.0001721607695799321
    },
    "wheel_imbalance": {
      "n": 671,
      "mean": 0.2842139005661011,
      "std": 0.430133193731308
    }
  },
  "interpretability": {
    "yaw_transition_minus_overall": -0.021926507353782654,
    "drive_stall_minus_overall": 0.12911024689674377,
    "velocity_slope_flat_abs_delta": 6.819751615694258e-05,
    "score_0_to_3": 1
  }
}
```

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 19 | 0.3684 | 0.5300 |
| [0.60,0.70) | 27 | 0.3333 | 0.6518 |
| [0.70,0.80) | 44 | 0.4091 | 0.7584 |
| [0.80,0.90) | 62 | 0.1774 | 0.8554 |
| [0.90,1.00) | 3450 | 0.0316 | 0.9965 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 838 | 0.6002 | 0.5146 |
| [0.60,0.70) | 491 | 0.5031 | 0.6502 |
| [0.70,0.80) | 456 | 0.4956 | 0.7501 |
| [0.80,0.90) | 484 | 0.4132 | 0.8525 |
| [0.90,1.00) | 1333 | 0.2588 | 0.9701 |


## 验证集最佳点

```json
{
  "loss_total": 0.5528095955777717,
  "acc_main": 0.9385656292286875,
  "acc_turn": 0.631935047361299,
  "acc_turn_pure": 0.6374959029826286,
  "acc_turn_transition": 0.6055900621118012,
  "false_turn_straight": 0.3981288981288981,
  "flat_recall": 0.9254185692541856,
  "stall_recall": 0.5238095238095238,
  "slope_recall": 0.9472630173564753,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9254185692541856,
    0.5238095238095238,
    0.9472630173564753
  ],
  "turn_right_recall": 0.6729857819905213,
  "turn_straight_recall": 0.6018711018711018,
  "turn_left_recall": 0.656957928802589,
  "recall_turn": [
    0.6729857819905213,
    0.6018711018711018,
    0.656957928802589
  ],
  "cm_turn": [
    [
      568,
      233,
      43
    ],
    [
      405,
      1158,
      361
    ],
    [
      88,
      230,
      609
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      608,
      0,
      49
    ],
    [
      0,
      22,
      20
    ],
    [
      151,
      7,
      2838
    ]
  ],
  "main_confidence_mean": 0.9666739639184183,
  "main_confidence_error_mean": 0.7752057913511671,
  "main_low_conf_0p60_ratio": 0.05277401894451962,
  "main_low_conf_0p70_ratio": 0.06197564276048714,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 195,
      "error_rate": 0.4717948717948718,
      "mean_confidence": 0.5744349390332355
    },
    {
      "bin": "[0.60,0.70)",
      "n": 34,
      "error_rate": 0.4117647058823529,
      "mean_confidence": 0.6430955194356465
    },
    {
      "bin": "[0.70,0.80)",
      "n": 38,
      "error_rate": 0.2631578947368421,
      "mean_confidence": 0.7490049880208517
    },
    {
      "bin": "[0.80,0.90)",
      "n": 55,
      "error_rate": 0.36363636363636365,
      "mean_confidence": 0.8527179270302304
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3373,
      "error_rate": 0.026978950489178772,
      "mean_confidence": 0.9969221940037972
    }
  ],
  "turn_confidence_mean": 0.7943007266828184,
  "turn_confidence_error_mean": 0.7209975088786172,
  "turn_low_conf_0p60_ratio": 0.21028416779431663,
  "turn_low_conf_0p70_ratio": 0.3307171853856563,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 777,
      "error_rate": 0.5701415701415702,
      "mean_confidence": 0.5077034616670482
    },
    {
      "bin": "[0.60,0.70)",
      "n": 445,
      "error_rate": 0.451685393258427,
      "mean_confidence": 0.6500649915067223
    },
    {
      "bin": "[0.70,0.80)",
      "n": 422,
      "error_rate": 0.45260663507109006,
      "mean_confidence": 0.7509432015683356
    },
    {
      "bin": "[0.80,0.90)",
      "n": 520,
      "error_rate": 0.36923076923076925,
      "mean_confidence": 0.8551450877602522
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1531,
      "error_rate": 0.21750489875898105,
      "mean_confidence": 0.9729609389027152
    }
  ],
  "theta_mae_rad": 0.014690454117953777,
  "theta_mae_deg": 0.8417009711265564,
  "uphill_recall": 0.7681940700808625,
  "downhill_recall": 0.8131256952169077,
  "slope_sign_acc": 0.970161511086778,
  "theta_flat_mae_deg": 1.0769013166427612,
  "theta_flat_abs_p95_deg": 3.645526170730591,
  "theta_flat_abs_max_deg": 11.130268096923828,
  "theta_flat_bias_deg": 0.6151418089866638,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5032708644866943,
  "theta_near_flat_abs_p95_deg": 4.514283657073975,
  "theta_near_flat_abs_max_deg": 11.130268096923828,
  "theta_near_flat_bias_deg": 1.1056585311889648,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.2975406646728516,
  "theta_flat_turn_abs_p95_deg": 5.729579925537109,
  "theta_flat_turn_abs_max_deg": 11.130268096923828,
  "theta_flat_turn_bias_deg": 0.8931333422660828,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8417009711265564,
  "theta_slope_control_abs_p95_deg": 9.422222137451172,
  "theta_slope_control_abs_max_deg": 13.351130485534668,
  "theta_slope_control_bias_deg": -0.06876135617494583,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8417010307312012,
  "theta_all_rmse_deg": 1.2751150131225586,
  "theta_all_p95_abs_err_deg": 2.584193706512451,
  "theta_all_max_abs_err_deg": 11.630268096923828,
  "theta_all_bias_deg": -0.06876135617494583,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7901233434677124,
  "theta_active_abs_ge_2_rmse_deg": 1.1279600858688354,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2413337230682373,
  "theta_active_abs_ge_2_max_abs_err_deg": 8.17467212677002,
  "theta_active_abs_ge_2_bias_deg": -0.21873611211776733,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8595548272132874,
  "theta_abs_le_8_rmse_deg": 1.304930567741394,
  "theta_abs_le_8_p95_abs_err_deg": 2.74188232421875,
  "theta_abs_le_8_max_abs_err_deg": 11.630268096923828,
  "theta_abs_le_8_bias_deg": -0.00459316885098815,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8417010307312012,
  "theta_abs_le_10_rmse_deg": 1.2751150131225586,
  "theta_abs_le_10_p95_abs_err_deg": 2.584193706512451,
  "theta_abs_le_10_max_abs_err_deg": 11.630268096923828,
  "theta_abs_le_10_bias_deg": -0.06876135617494583,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7966400384902954,
  "theta_pos_8_10_rmse_deg": 1.010202169418335,
  "theta_pos_8_10_p95_abs_err_deg": 1.7901005744934082,
  "theta_pos_8_10_max_abs_err_deg": 5.778113842010498,
  "theta_pos_8_10_bias_deg": -0.5659058690071106,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7356036901473999,
  "theta_neg_10_8_rmse_deg": 1.2598224878311157,
  "theta_neg_10_8_p95_abs_err_deg": 2.508699417114258,
  "theta_neg_10_8_max_abs_err_deg": 6.7308878898620605,
  "theta_neg_10_8_bias_deg": -0.10909752547740936,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.8854943513870239,
  "theta_pos_6_8_rmse_deg": 1.12444007396698,
  "theta_pos_6_8_p95_abs_err_deg": 2.2396442890167236,
  "theta_pos_6_8_max_abs_err_deg": 3.4589860439300537,
  "theta_pos_6_8_bias_deg": -0.6147797107696533,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.9878886342048645,
  "theta_neg_8_6_rmse_deg": 1.380184292793274,
  "theta_neg_8_6_p95_abs_err_deg": 2.7423272132873535,
  "theta_neg_8_6_max_abs_err_deg": 8.17467212677002,
  "theta_neg_8_6_bias_deg": -0.3650107979774475,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6984615921974182,
  "theta_neg_4_2_rmse_deg": 0.9678852558135986,
  "theta_neg_4_2_p95_abs_err_deg": 2.154946804046631,
  "theta_neg_4_2_max_abs_err_deg": 4.59815788269043,
  "theta_neg_4_2_bias_deg": -0.16889524459838867,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5484471321105957,
  "theta_neg_2_0p5_rmse_deg": 0.7423997521400452,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.2252280712127686,
  "theta_neg_2_0p5_max_abs_err_deg": 4.079066753387451,
  "theta_neg_2_0p5_bias_deg": -0.1335807591676712,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0601913928985596,
  "theta_pos_0p5_2_rmse_deg": 1.3483469486236572,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.1771106719970703,
  "theta_pos_0p5_2_max_abs_err_deg": 4.3179731369018555,
  "theta_pos_0p5_2_bias_deg": 0.752608060836792,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.30771413270449605,
  "loss_turn": 1.2238886768666268,
  "loss_theta": 0.0004952677574256972,
  "loss_main_bundle_base": 0.30771413270449605,
  "loss_turn_bundle_base": 0.24477774039092343,
  "loss_theta_bundle_base": 0.00031772130382428743,
  "loss_main_bundle": 0.30771413270449605,
  "loss_turn_bundle": 0.24477774039092343,
  "loss_theta_bundle": 0.00031772130382428743,
  "loss_theta_flat": 0.00019600430917163683,
  "loss_theta_near_flat": 0.0016867719288204616,
  "loss_theta_error_excess": 0.00019613635476665376,
  "loss_theta_flat_excess": 0.00011127700967968426,
  "loss_theta_near_flat_excess": 0.0013003168589182208,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00011996694622153016,
  "loss_theta_small_neg": 0.00028053148180505965,
  "loss_theta_small_neg_excess": 6.43395931571889e-05,
  "loss_turn_release": 0.3303659838494493,
  "loss_false_turn_straight": 0.27105200327781603,
  "loss_transition_focal_raw": 0.8456984044573143,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.1812857420907443,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0,
  "val_gate_all_finite": true,
  "val_gate_single_collapse": false,
  "val_gate_mean_entropy": 0.10036618262529373,
  "val_gate_interpretability_score": 1,
  "val_gate_yaw_transition_minus_overall": 0.031406283378601074,
  "val_gate_drive_stall_minus_overall": -0.2719188928604126,
  "val_gate_velocity_slope_flat_abs_delta": 4.474526576814242e-06,
  "val_gate_detail": {
    "prefix": "val",
    "stat_label_policy": "true label for main class; dataset turn_transition mask for transition",
    "group_names": [
      "yaw_steering",
      "drive_current_load",
      "velocity_acceleration",
      "wheel_imbalance"
    ],
    "all_finite": true,
    "single_collapse": false,
    "mean_entropy": 0.10036618262529373,
    "overall": {
      "yaw_steering": {
        "n": 3695,
        "mean": 0.17148682475090027,
        "std": 0.3596714735031128
      },
      "drive_current_load": {
        "n": 3695,
        "mean": 0.5809192657470703,
        "std": 0.46339842677116394
      },
      "velocity_acceleration": {
        "n": 3695,
        "mean": 2.424312879156787e-05,
        "std": 0.00012922563473694026
      },
      "wheel_imbalance": {
        "n": 3695,
        "mean": 0.24756965041160583,
        "std": 0.41137734055519104
      }
    },
    "by_main_true": {
      "flat": {
        "yaw_steering": {
          "n": 657,
          "mean": 0.003499237122014165,
          "std": 0.015053274109959602
        },
        "drive_current_load": {
          "n": 657,
          "mean": 0.5211140513420105,
          "std": 0.47766977548599243
        },
        "velocity_acceleration": {
          "n": 657,
          "mean": 2.8126347388024442e-05,
          "std": 8.539304690202698e-05
        },
        "wheel_imbalance": {
          "n": 657,
          "mean": 0.47535860538482666,
          "std": 0.4805890619754791
        }
      },
      "stall": {
        "yaw_steering": {
          "n": 42,
          "mean": 0.0003818461555056274,
          "std": 0.0009024788741953671
        },
        "drive_current_load": {
          "n": 42,
          "mean": 0.3090008497238159,
          "std": 0.43921878933906555
        },
        "velocity_acceleration": {
          "n": 42,
          "mean": 5.67870847589802e-06,
          "std": 9.174732440442313e-06
        },
        "wheel_imbalance": {
          "n": 42,
          "mean": 0.6906115412712097,
          "std": 0.4397733509540558
        }
      },
      "slope": {
        "yaw_steering": {
          "n": 2996,
          "mean": 0.210723876953125,
          "std": 0.389046847820282
        },
        "drive_current_load": {
          "n": 2996,
          "mean": 0.5978460907936096,
          "std": 0.4582482874393463
        },
        "velocity_acceleration": {
          "n": 2996,
          "mean": 2.36518208112102e-05,
          "std": 0.00013779205619357526
        },
        "wheel_imbalance": {
          "n": 2996,
          "mean": 0.19140641391277313,
          "std": 0.3715777099132538
        }
      }
    },
    "turn_transition": {
      "yaw_steering": {
        "n": 644,
        "mean": 0.20289279520511627,
        "std": 0.3794190287590027
      },
      "drive_current_load": {
        "n": 644,
        "mean": 0.5604791045188904,
        "std": 0.4620269536972046
      },
      "velocity_acceleration": {
        "n": 644,
        "mean": 2.7971853342023678e-05,
        "std": 9.115764987654984e-05
      },
      "wheel_imbalance": {
        "n": 644,
        "mean": 0.2366001009941101,
        "std": 0.4061795771121979
      }
    },
    "interpretability": {
      "yaw_transition_minus_overall": 0.031406283378601074,
      "drive_stall_minus_overall": -0.2719188928604126,
      "velocity_slope_flat_abs_delta": 4.474526576814242e-06,
      "score_0_to_3": 1
    }
  },
  "val_gate_yaw_steering_mean": 0.17148682475090027,
  "val_gate_yaw_steering_std": 0.3596714735031128,
  "val_gate_drive_current_load_mean": 0.5809192657470703,
  "val_gate_drive_current_load_std": 0.46339842677116394,
  "val_gate_velocity_acceleration_mean": 2.424312879156787e-05,
  "val_gate_velocity_acceleration_std": 0.00012922563473694026,
  "val_gate_wheel_imbalance_mean": 0.24756965041160583,
  "val_gate_wheel_imbalance_std": 0.41137734055519104
}
```
