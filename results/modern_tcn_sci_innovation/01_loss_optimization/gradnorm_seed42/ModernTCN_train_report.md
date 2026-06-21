# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
- loss_mode: `gradnorm`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- vehicle: `diagonal_dual_steer_drive_agv`; active=`LF,RR`; passive=`RF,LR`
- feature_policy: `keep_current_algorithm_inputs_unchanged`
- label_time_policy: `current_window_end`, horizon_steps=0
- split: 使用 MAT 文件已有 run-level split，不重划分。
- scaler: 使用 MAT 文件已有归一化后 X，不重新拟合。
- confidence_policy: `derive_classification_confidence_from_softmax_and_export`
- input: `[batch, time=128, feature=22]`
- output: `logits_main`, `logits_turn`, `theta_hat`

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
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9642 |
| acc_turn | 0.5733 |
| acc_turn_pure | 0.5875 |
| acc_turn_transition | 0.5112 |
| main_confidence_mean | 0.9848 |
| main_low_conf_0p60_ratio | 0.0158 |
| main_low_conf_0p70_ratio | 0.0208 |
| turn_confidence_mean | 0.8019 |
| turn_low_conf_0p60_ratio | 0.1818 |
| turn_low_conf_0p70_ratio | 0.3140 |
| turn_right_recall | 0.5770 |
| turn_straight_recall | 0.5629 |
| turn_left_recall | 0.5931 |
| theta_mae_deg | 0.7454 |
| theta_abs_le_10_p95_abs_err_deg | 1.8680 |
| theta_neg_10_8_p95_abs_err_deg | 1.3489 |
| theta_pos_8_10_p95_abs_err_deg | 2.4733 |
| theta_abs_le_8_p95_abs_err_deg | 1.8317 |
| theta_neg_8_6_p95_abs_err_deg | 1.7751 |
| theta_pos_6_8_p95_abs_err_deg | 1.7383 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.8600 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.1268 |
| theta_flat_abs_p95_deg | 2.5179 |
| theta_flat_bias_deg | -0.3839 |
| theta_near_flat_abs_p95_deg | 1.9269 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.5658 |
| theta_flat_turn_abs_p95_deg | 2.0620 |
| flat_recall | 0.9511 |
| stall_recall | 0.6875 |
| slope_recall | 0.9775 |
| uphill_recall | 0.7569 |
| downhill_recall | 0.7968 |

- best_epoch: 52
- train_seconds: 493.8

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 57 | 0.6140 | 0.5500 |
| [0.60,0.70) | 18 | 0.3333 | 0.6598 |
| [0.70,0.80) | 28 | 0.3214 | 0.7486 |
| [0.80,0.90) | 45 | 0.2222 | 0.8504 |
| [0.90,1.00) | 3454 | 0.0200 | 0.9974 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 655 | 0.6427 | 0.5143 |
| [0.60,0.70) | 476 | 0.5651 | 0.6509 |
| [0.70,0.80) | 421 | 0.5154 | 0.7506 |
| [0.80,0.90) | 557 | 0.4291 | 0.8510 |
| [0.90,1.00) | 1493 | 0.2619 | 0.9725 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.5112
- theta_mae_deg <= 0.7000 未满足，实际 0.7454

## 验证集最佳点

```json
{
  "loss_total": 0.5771917510097179,
  "acc_main": 0.9380243572395128,
  "acc_turn": 0.6267929634641407,
  "acc_turn_pure": 0.637823664372337,
  "acc_turn_transition": 0.5745341614906833,
  "false_turn_straight": 0.43347193347193347,
  "flat_recall": 0.908675799086758,
  "stall_recall": 0.42857142857142855,
  "slope_recall": 0.9516021361815754,
  "recall_main": [
    0.908675799086758,
    0.42857142857142855,
    0.9516021361815754
  ],
  "turn_right_recall": 0.6469194312796208,
  "turn_straight_recall": 0.5665280665280665,
  "turn_left_recall": 0.7335490830636462,
  "recall_turn": [
    0.6469194312796208,
    0.5665280665280665,
    0.7335490830636462
  ],
  "cm_turn": [
    [
      546,
      201,
      97
    ],
    [
      359,
      1090,
      475
    ],
    [
      76,
      171,
      680
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      597,
      0,
      60
    ],
    [
      0,
      18,
      24
    ],
    [
      140,
      5,
      2851
    ]
  ],
  "main_confidence_mean": 0.9713205056169312,
  "main_confidence_error_mean": 0.7972379133337236,
  "main_low_conf_0p60_ratio": 0.005683355886332882,
  "main_low_conf_0p70_ratio": 0.0571041948579161,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 21,
      "error_rate": 0.6190476190476191,
      "mean_confidence": 0.532760933284706
    },
    {
      "bin": "[0.60,0.70)",
      "n": 190,
      "error_rate": 0.45263157894736844,
      "mean_confidence": 0.6185596885802421
    },
    {
      "bin": "[0.70,0.80)",
      "n": 28,
      "error_rate": 0.5,
      "mean_confidence": 0.7552432042703069
    },
    {
      "bin": "[0.80,0.90)",
      "n": 51,
      "error_rate": 0.23529411764705882,
      "mean_confidence": 0.852581950903332
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3405,
      "error_rate": 0.030543318649045522,
      "mean_confidence": 0.9972647455535087
    }
  ],
  "turn_confidence_mean": 0.8149959348235366,
  "turn_confidence_error_mean": 0.7369671060188544,
  "turn_low_conf_0p60_ratio": 0.17889039242219215,
  "turn_low_conf_0p70_ratio": 0.2814614343707713,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 661,
      "error_rate": 0.6036308623298033,
      "mean_confidence": 0.48692090900369894
    },
    {
      "bin": "[0.60,0.70)",
      "n": 379,
      "error_rate": 0.5435356200527705,
      "mean_confidence": 0.6541412997775192
    },
    {
      "bin": "[0.70,0.80)",
      "n": 361,
      "error_rate": 0.43213296398891965,
      "mean_confidence": 0.7493797148858666
    },
    {
      "bin": "[0.80,0.90)",
      "n": 539,
      "error_rate": 0.34879406307977734,
      "mean_confidence": 0.8533243325990103
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1755,
      "error_rate": 0.245014245014245,
      "mean_confidence": 0.9750243950775945
    }
  ],
  "theta_mae_rad": 0.01622987911105156,
  "theta_mae_deg": 0.929903507232666,
  "uphill_recall": 0.7789757412398922,
  "downhill_recall": 0.8153503893214683,
  "slope_sign_acc": 0.9674240350396934,
  "theta_flat_mae_deg": 1.1565958261489868,
  "theta_flat_abs_p95_deg": 3.2581191062927246,
  "theta_flat_abs_max_deg": 7.371956825256348,
  "theta_flat_bias_deg": 0.38974982500076294,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4052691459655762,
  "theta_near_flat_abs_p95_deg": 3.258164405822754,
  "theta_near_flat_abs_max_deg": 7.371956825256348,
  "theta_near_flat_bias_deg": 0.5815953612327576,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.3209770917892456,
  "theta_flat_turn_abs_p95_deg": 3.3381905555725098,
  "theta_flat_turn_abs_max_deg": 7.371956825256348,
  "theta_flat_turn_bias_deg": 0.32657092809677124,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.929903507232666,
  "theta_slope_control_abs_p95_deg": 9.148884773254395,
  "theta_slope_control_abs_max_deg": 11.906698226928711,
  "theta_slope_control_bias_deg": -0.12038948386907578,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.9299036264419556,
  "theta_all_rmse_deg": 1.284240484237671,
  "theta_all_p95_abs_err_deg": 2.6991324424743652,
  "theta_all_max_abs_err_deg": 7.8719563484191895,
  "theta_all_bias_deg": -0.12038948386907578,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.8801918029785156,
  "theta_active_abs_ge_2_rmse_deg": 1.2121179103851318,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.4144551753997803,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.189648628234863,
  "theta_active_abs_ge_2_bias_deg": -0.232259139418602,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9704427719116211,
  "theta_abs_le_8_rmse_deg": 1.322601318359375,
  "theta_abs_le_8_p95_abs_err_deg": 2.7580957412719727,
  "theta_abs_le_8_max_abs_err_deg": 7.8719563484191895,
  "theta_abs_le_8_bias_deg": -0.10658495128154755,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.9299036264419556,
  "theta_abs_le_10_rmse_deg": 1.284240484237671,
  "theta_abs_le_10_p95_abs_err_deg": 2.6991324424743652,
  "theta_abs_le_10_max_abs_err_deg": 7.8719563484191895,
  "theta_abs_le_10_bias_deg": -0.12038948386907578,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7673998475074768,
  "theta_pos_8_10_rmse_deg": 0.9398972988128662,
  "theta_pos_8_10_p95_abs_err_deg": 1.556909441947937,
  "theta_pos_8_10_max_abs_err_deg": 5.191487789154053,
  "theta_pos_8_10_bias_deg": -0.5916759371757507,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7502256035804749,
  "theta_neg_10_8_rmse_deg": 1.2559337615966797,
  "theta_neg_10_8_p95_abs_err_deg": 2.252748489379883,
  "theta_neg_10_8_max_abs_err_deg": 7.164162635803223,
  "theta_neg_10_8_bias_deg": 0.24156831204891205,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.876919686794281,
  "theta_pos_6_8_rmse_deg": 1.0943918228149414,
  "theta_pos_6_8_p95_abs_err_deg": 2.233175277709961,
  "theta_pos_6_8_max_abs_err_deg": 4.1486124992370605,
  "theta_pos_6_8_bias_deg": -0.5247857570648193,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8646990656852722,
  "theta_neg_8_6_rmse_deg": 1.2211576700210571,
  "theta_neg_8_6_p95_abs_err_deg": 2.3352744579315186,
  "theta_neg_8_6_max_abs_err_deg": 6.279568195343018,
  "theta_neg_8_6_bias_deg": -0.21536356210708618,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7640374898910522,
  "theta_neg_4_2_rmse_deg": 1.0728012323379517,
  "theta_neg_4_2_p95_abs_err_deg": 2.2850255966186523,
  "theta_neg_4_2_max_abs_err_deg": 5.756995677947998,
  "theta_neg_4_2_bias_deg": -0.1606939285993576,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.8008043169975281,
  "theta_neg_2_0p5_rmse_deg": 1.0815529823303223,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.249789237976074,
  "theta_neg_2_0p5_max_abs_err_deg": 4.002667427062988,
  "theta_neg_2_0p5_bias_deg": 0.1039586067199707,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.2184463739395142,
  "theta_pos_0p5_2_rmse_deg": 1.3884831666946411,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.0603365898132324,
  "theta_pos_0p5_2_max_abs_err_deg": 3.9254026412963867,
  "theta_pos_0p5_2_bias_deg": 0.542076051235199,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3239915802933689,
  "loss_turn": 1.2642882133530344,
  "loss_theta": 0.0005022792581182745,
  "loss_main_bundle": 0.3239915802933689,
  "loss_turn_bundle": 0.2528576461807478,
  "loss_theta_bundle": 0.00034252624645739725,
  "loss_theta_flat": 0.00036477427921763274,
  "loss_theta_near_flat": 0.0011978669574733759,
  "loss_theta_error_excess": 0.00016804014886549835,
  "loss_theta_flat_excess": 0.00014836391194547743,
  "loss_theta_near_flat_excess": 0.0008104501005403284,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00014097725927873222,
  "loss_theta_small_neg": 0.0003454486954628322,
  "loss_theta_small_neg_excess": 9.486147629302524e-05,
  "loss_turn_release": 0.39127579081364994,
  "loss_false_turn_straight": 0.30394571509025736
}
```
