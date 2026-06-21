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
- alpha_final: `0.36432222`
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
  "alpha_init": 0.1,
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
| acc_main | 0.9659 |
| acc_turn | 0.5780 |
| acc_turn_pure | 0.5930 |
| acc_turn_transition | 0.5127 |
| main_confidence_mean | 0.9909 |
| main_low_conf_0p60_ratio | 0.0053 |
| main_low_conf_0p70_ratio | 0.0094 |
| turn_confidence_mean | 0.8315 |
| turn_low_conf_0p60_ratio | 0.1557 |
| turn_low_conf_0p70_ratio | 0.2626 |
| turn_right_recall | 0.6258 |
| turn_straight_recall | 0.5908 |
| turn_left_recall | 0.5057 |
| theta_mae_deg | 0.6350 |
| theta_abs_le_10_p95_abs_err_deg | 1.7739 |
| theta_neg_10_8_p95_abs_err_deg | 1.5549 |
| theta_pos_8_10_p95_abs_err_deg | 3.2538 |
| theta_abs_le_8_p95_abs_err_deg | 1.6107 |
| theta_neg_8_6_p95_abs_err_deg | 1.5607 |
| theta_pos_6_8_p95_abs_err_deg | 1.8785 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.7263 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4702 |
| theta_flat_abs_p95_deg | 2.5018 |
| theta_flat_bias_deg | -0.1232 |
| theta_near_flat_abs_p95_deg | 2.0286 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1917 |
| theta_flat_turn_abs_p95_deg | 2.1497 |
| flat_recall | 0.9696 |
| stall_recall | 0.6354 |
| slope_recall | 0.9764 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7626 |
| downhill_recall | 0.7821 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    733,
    0,
    23
  ],
  [
    9,
    61,
    26
  ],
  [
    64,
    1,
    2685
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    500,
    207,
    92
  ],
  [
    415,
    1142,
    376
  ],
  [
    156,
    274,
    440
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.417410 |
| test_loss_turn_bundle_base | 0.345872 |
| test_loss_theta_bundle_base | 0.000159 |
| test_loss_transition_focal_raw | 1.602418 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.844877 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |

- best_epoch: 76
- train_seconds: 443.1

## E3 Gate Statistics

| metric | value |
|---|---:|
| test_gate_all_finite | True |
| test_gate_single_collapse | False |
| test_gate_mean_entropy | 0.361416 |
| test_gate_interpretability_score | 2.000000 |
| test_gate_yaw_transition_minus_overall | -0.001730 |
| test_gate_drive_stall_minus_overall | 0.195646 |
| test_gate_velocity_slope_flat_abs_delta | 0.029104 |

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
  "mean_entropy": 0.3614164888858795,
  "overall": {
    "yaw_steering": {
      "n": 3602,
      "mean": 0.27561500668525696,
      "std": 0.36399245262145996
    },
    "drive_current_load": {
      "n": 3602,
      "mean": 0.5361374616622925,
      "std": 0.44243019819259644
    },
    "velocity_acceleration": {
      "n": 3602,
      "mean": 0.14088942110538483,
      "std": 0.27762120962142944
    },
    "wheel_imbalance": {
      "n": 3602,
      "mean": 0.047358062118291855,
      "std": 0.1116429939866066
    }
  },
  "by_main_true": {
    "flat": {
      "yaw_steering": {
        "n": 756,
        "mean": 0.2535697817802429,
        "std": 0.381242573261261
      },
      "drive_current_load": {
        "n": 756,
        "mean": 0.5534640550613403,
        "std": 0.460429847240448
      },
      "velocity_acceleration": {
        "n": 756,
        "mean": 0.1658453494310379,
        "std": 0.305573046207428
      },
      "wheel_imbalance": {
        "n": 756,
        "mean": 0.027120811864733696,
        "std": 0.055605411529541016
      }
    },
    "stall": {
      "yaw_steering": {
        "n": 96,
        "mean": 0.18345512449741364,
        "std": 0.32047078013420105
      },
      "drive_current_load": {
        "n": 96,
        "mean": 0.7317840456962585,
        "std": 0.39078661799430847
      },
      "velocity_acceleration": {
        "n": 96,
        "mean": 0.06319303810596466,
        "std": 0.13737176358699799
      },
      "wheel_imbalance": {
        "n": 96,
        "mean": 0.021567760035395622,
        "std": 0.045661237090826035
      }
    },
    "slope": {
      "yaw_steering": {
        "n": 2750,
        "mean": 0.2848926782608032,
        "std": 0.3598335385322571
      },
      "drive_current_load": {
        "n": 2750,
        "mean": 0.5245444178581238,
        "std": 0.43729379773139954
      },
      "velocity_acceleration": {
        "n": 2750,
        "mean": 0.13674111664295197,
        "std": 0.2724422514438629
      },
      "wheel_imbalance": {
        "n": 2750,
        "mean": 0.053821783512830734,
        "std": 0.12339124828577042
      }
    }
  },
  "turn_transition": {
    "yaw_steering": {
      "n": 671,
      "mean": 0.27388516068458557,
      "std": 0.3570229709148407
    },
    "drive_current_load": {
      "n": 671,
      "mean": 0.5371513366699219,
      "std": 0.44155076146125793
    },
    "velocity_acceleration": {
      "n": 671,
      "mean": 0.14763496816158295,
      "std": 0.2815417945384979
    },
    "wheel_imbalance": {
      "n": 671,
      "mean": 0.0413285568356514,
      "std": 0.09985937923192978
    }
  },
  "interpretability": {
    "yaw_transition_minus_overall": -0.0017297565937042236,
    "drive_stall_minus_overall": 0.1956462264060974,
    "velocity_slope_flat_abs_delta": 0.029104232788085938,
    "score_0_to_3": 2
  }
}
```

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 19 | 0.3684 | 0.5467 |
| [0.60,0.70) | 15 | 0.4000 | 0.6646 |
| [0.70,0.80) | 21 | 0.3810 | 0.7525 |
| [0.80,0.90) | 47 | 0.6170 | 0.8613 |
| [0.90,1.00) | 3500 | 0.0209 | 0.9979 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 561 | 0.5900 | 0.5263 |
| [0.60,0.70) | 385 | 0.5948 | 0.6520 |
| [0.70,0.80) | 393 | 0.5522 | 0.7506 |
| [0.80,0.90) | 459 | 0.4902 | 0.8489 |
| [0.90,1.00) | 1804 | 0.2871 | 0.9779 |


## 验证集最佳点

```json
{
  "loss_total": 0.7088225767964117,
  "acc_main": 0.937212449255751,
  "acc_turn": 0.6354533152909337,
  "acc_turn_pure": 0.644706653556211,
  "acc_turn_transition": 0.5916149068322981,
  "false_turn_straight": 0.39656964656964655,
  "flat_recall": 0.9345509893455098,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.945260347129506,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9345509893455098,
    0.40476190476190477,
    0.945260347129506
  ],
  "turn_right_recall": 0.6563981042654028,
  "turn_straight_recall": 0.6034303534303534,
  "turn_left_recall": 0.6828478964401294,
  "recall_turn": [
    0.6563981042654028,
    0.6034303534303534,
    0.6828478964401294
  ],
  "cm_turn": [
    [
      554,
      206,
      84
    ],
    [
      346,
      1161,
      417
    ],
    [
      78,
      216,
      633
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      614,
      0,
      43
    ],
    [
      0,
      17,
      25
    ],
    [
      151,
      13,
      2832
    ]
  ],
  "main_confidence_mean": 0.9681438204029782,
  "main_confidence_error_mean": 0.777484186801607,
  "main_low_conf_0p60_ratio": 0.05196211096075778,
  "main_low_conf_0p70_ratio": 0.05872801082543978,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 192,
      "error_rate": 0.4791666666666667,
      "mean_confidence": 0.5339533855601895
    },
    {
      "bin": "[0.60,0.70)",
      "n": 25,
      "error_rate": 0.4,
      "mean_confidence": 0.6523396196382261
    },
    {
      "bin": "[0.70,0.80)",
      "n": 28,
      "error_rate": 0.2857142857142857,
      "mean_confidence": 0.7480632528968989
    },
    {
      "bin": "[0.80,0.90)",
      "n": 34,
      "error_rate": 0.3235294117647059,
      "mean_confidence": 0.8528349652966696
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3416,
      "error_rate": 0.03249414519906323,
      "mean_confidence": 0.9978108067825799
    }
  ],
  "turn_confidence_mean": 0.8420989963108564,
  "turn_confidence_error_mean": 0.7585739605732724,
  "turn_low_conf_0p60_ratio": 0.14668470906630582,
  "turn_low_conf_0p70_ratio": 0.23734776725304466,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 542,
      "error_rate": 0.6309963099630996,
      "mean_confidence": 0.4908804949122577
    },
    {
      "bin": "[0.60,0.70)",
      "n": 335,
      "error_rate": 0.5313432835820896,
      "mean_confidence": 0.6499980694770247
    },
    {
      "bin": "[0.70,0.80)",
      "n": 345,
      "error_rate": 0.4608695652173913,
      "mean_confidence": 0.752618865725306
    },
    {
      "bin": "[0.80,0.90)",
      "n": 420,
      "error_rate": 0.48095238095238096,
      "mean_confidence": 0.8521582184263577
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2053,
      "error_rate": 0.22698490014612763,
      "mean_confidence": 0.9791472233010555
    }
  ],
  "theta_mae_rad": 0.014017870649695396,
  "theta_mae_deg": 0.8031647801399231,
  "uphill_recall": 0.7730458221024259,
  "downhill_recall": 0.8014460511679644,
  "slope_sign_acc": 0.9619490829455243,
  "theta_flat_mae_deg": 1.10806405544281,
  "theta_flat_abs_p95_deg": 3.84959077835083,
  "theta_flat_abs_max_deg": 7.070568561553955,
  "theta_flat_bias_deg": 0.5338963866233826,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.3532979488372803,
  "theta_near_flat_abs_p95_deg": 3.84959077835083,
  "theta_near_flat_abs_max_deg": 7.070568561553955,
  "theta_near_flat_bias_deg": 0.92545086145401,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.101812481880188,
  "theta_flat_turn_abs_p95_deg": 4.024986743927002,
  "theta_flat_turn_abs_max_deg": 7.070568561553955,
  "theta_flat_turn_bias_deg": 0.6479968428611755,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8031647801399231,
  "theta_slope_control_abs_p95_deg": 9.026501655578613,
  "theta_slope_control_abs_max_deg": 12.301810264587402,
  "theta_slope_control_bias_deg": -0.005437391344457865,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8031647205352783,
  "theta_all_rmse_deg": 1.2062174081802368,
  "theta_all_p95_abs_err_deg": 2.860593318939209,
  "theta_all_max_abs_err_deg": 7.570568561553955,
  "theta_all_bias_deg": -0.005437388550490141,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7363026738166809,
  "theta_active_abs_ge_2_rmse_deg": 1.0877872705459595,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.3286452293395996,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.768887996673584,
  "theta_active_abs_ge_2_bias_deg": -0.12370917201042175,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8371292948722839,
  "theta_abs_le_8_rmse_deg": 1.2460509538650513,
  "theta_abs_le_8_p95_abs_err_deg": 3.1049416065216064,
  "theta_abs_le_8_max_abs_err_deg": 7.570568561553955,
  "theta_abs_le_8_bias_deg": 0.00866757333278656,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8031647205352783,
  "theta_abs_le_10_rmse_deg": 1.2062174081802368,
  "theta_abs_le_10_p95_abs_err_deg": 2.860593318939209,
  "theta_abs_le_10_max_abs_err_deg": 7.570568561553955,
  "theta_abs_le_10_bias_deg": -0.005437388550490141,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6640625596046448,
  "theta_pos_8_10_rmse_deg": 0.8892355561256409,
  "theta_pos_8_10_p95_abs_err_deg": 1.5055879354476929,
  "theta_pos_8_10_max_abs_err_deg": 5.395749092102051,
  "theta_pos_8_10_bias_deg": -0.4044804871082306,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6556310057640076,
  "theta_neg_10_8_rmse_deg": 1.1399037837982178,
  "theta_neg_10_8_p95_abs_err_deg": 2.247756242752075,
  "theta_neg_10_8_max_abs_err_deg": 6.226466655731201,
  "theta_neg_10_8_bias_deg": 0.28047114610671997,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6624636650085449,
  "theta_pos_6_8_rmse_deg": 0.889802098274231,
  "theta_pos_6_8_p95_abs_err_deg": 1.657143473625183,
  "theta_pos_6_8_max_abs_err_deg": 3.6884539127349854,
  "theta_pos_6_8_bias_deg": -0.24201172590255737,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.6675379872322083,
  "theta_neg_8_6_rmse_deg": 1.0443049669265747,
  "theta_neg_8_6_p95_abs_err_deg": 2.129847288131714,
  "theta_neg_8_6_max_abs_err_deg": 6.768887996673584,
  "theta_neg_8_6_bias_deg": -0.023396680131554604,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7286562323570251,
  "theta_neg_4_2_rmse_deg": 1.0115878582000732,
  "theta_neg_4_2_p95_abs_err_deg": 2.1654183864593506,
  "theta_neg_4_2_max_abs_err_deg": 5.132593154907227,
  "theta_neg_4_2_bias_deg": -0.16635243594646454,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.7378197312355042,
  "theta_neg_2_0p5_rmse_deg": 0.9723572134971619,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.915517807006836,
  "theta_neg_2_0p5_max_abs_err_deg": 4.16485595703125,
  "theta_neg_2_0p5_bias_deg": 0.07932720333337784,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.2220348119735718,
  "theta_pos_0p5_2_rmse_deg": 1.5152137279510498,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.3586208820343018,
  "theta_pos_0p5_2_max_abs_err_deg": 4.226475715637207,
  "theta_pos_0p5_2_bias_deg": 0.49486008286476135,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.42074809605117097,
  "loss_turn": 1.438942557291023,
  "loss_theta": 0.00044331405238098436,
  "loss_main_bundle_base": 0.42074809605117097,
  "loss_turn_bundle_base": 0.2877885208118591,
  "loss_theta_bundle_base": 0.0002859586086886631,
  "loss_main_bundle": 0.42074809605117097,
  "loss_turn_bundle": 0.2877885208118591,
  "loss_theta_bundle": 0.0002859586086886631,
  "loss_theta_flat": 0.00018293181757157877,
  "loss_theta_near_flat": 0.001238612179185676,
  "loss_theta_error_excess": 0.00016404246810665518,
  "loss_theta_flat_excess": 0.0001078260915607775,
  "loss_theta_near_flat_excess": 0.000892300458788161,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00011981931631689631,
  "loss_theta_small_neg": 0.0003061122709320649,
  "loss_theta_small_neg_excess": 7.259882750446153e-05,
  "loss_turn_release": 0.3342371039929345,
  "loss_false_turn_straight": 0.28481278075900873,
  "loss_transition_focal_raw": 1.158893970868907,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 5.155731626055575,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0,
  "val_gate_all_finite": true,
  "val_gate_single_collapse": false,
  "val_gate_mean_entropy": 0.26271164417266846,
  "val_gate_interpretability_score": 3,
  "val_gate_yaw_transition_minus_overall": 0.044034138321876526,
  "val_gate_drive_stall_minus_overall": 0.038844406604766846,
  "val_gate_velocity_slope_flat_abs_delta": 0.05821290612220764,
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
    "mean_entropy": 0.26271164417266846,
    "overall": {
      "yaw_steering": {
        "n": 3695,
        "mean": 0.24672642350196838,
        "std": 0.37891829013824463
      },
      "drive_current_load": {
        "n": 3695,
        "mean": 0.5562043190002441,
        "std": 0.4561910331249237
      },
      "velocity_acceleration": {
        "n": 3695,
        "mean": 0.16123099625110626,
        "std": 0.313916951417923
      },
      "wheel_imbalance": {
        "n": 3695,
        "mean": 0.035838257521390915,
        "std": 0.1049877181649208
      }
    },
    "by_main_true": {
      "flat": {
        "yaw_steering": {
          "n": 657,
          "mean": 0.4239244759082794,
          "std": 0.46011340618133545
        },
        "drive_current_load": {
          "n": 657,
          "mean": 0.4454301595687866,
          "std": 0.47012633085250854
        },
        "velocity_acceleration": {
          "n": 657,
          "mean": 0.11418184638023376,
          "std": 0.2764618396759033
        },
        "wheel_imbalance": {
          "n": 657,
          "mean": 0.016463618725538254,
          "std": 0.03890693932771683
        }
      },
      "stall": {
        "yaw_steering": {
          "n": 42,
          "mean": 0.2693762481212616,
          "std": 0.3501254618167877
        },
        "drive_current_load": {
          "n": 42,
          "mean": 0.5950486063957214,
          "std": 0.45200014114379883
        },
        "velocity_acceleration": {
          "n": 42,
          "mean": 0.10086546838283539,
          "std": 0.1862386167049408
        },
        "wheel_imbalance": {
          "n": 42,
          "mean": 0.03470969945192337,
          "std": 0.041959311813116074
        }
      },
      "slope": {
        "yaw_steering": {
          "n": 2996,
          "mean": 0.20755071938037872,
          "std": 0.34714043140411377
        },
        "drive_current_load": {
          "n": 2996,
          "mean": 0.5799517631530762,
          "std": 0.44950738549232483
        },
        "velocity_acceleration": {
          "n": 2996,
          "mean": 0.1723947525024414,
          "std": 0.3219115734100342
        },
        "wheel_imbalance": {
          "n": 2996,
          "mean": 0.04010279104113579,
          "std": 0.11461640149354935
        }
      }
    },
    "turn_transition": {
      "yaw_steering": {
        "n": 644,
        "mean": 0.2907603681087494,
        "std": 0.3969418704509735
      },
      "drive_current_load": {
        "n": 644,
        "mean": 0.5423270463943481,
        "std": 0.4538191854953766
      },
      "velocity_acceleration": {
        "n": 644,
        "mean": 0.13371461629867554,
        "std": 0.2785663604736328
      },
      "wheel_imbalance": {
        "n": 644,
        "mean": 0.03319802135229111,
        "std": 0.1097777783870697
      }
    },
    "interpretability": {
      "yaw_transition_minus_overall": 0.044034138321876526,
      "drive_stall_minus_overall": 0.038844406604766846,
      "velocity_slope_flat_abs_delta": 0.05821290612220764,
      "score_0_to_3": 3
    }
  },
  "val_gate_yaw_steering_mean": 0.24672642350196838,
  "val_gate_yaw_steering_std": 0.37891829013824463,
  "val_gate_drive_current_load_mean": 0.5562043190002441,
  "val_gate_drive_current_load_std": 0.4561910331249237,
  "val_gate_velocity_acceleration_mean": 0.16123099625110626,
  "val_gate_velocity_acceleration_std": 0.313916951417923,
  "val_gate_wheel_imbalance_mean": 0.035838257521390915,
  "val_gate_wheel_imbalance_std": 0.1049877181649208
}
```
