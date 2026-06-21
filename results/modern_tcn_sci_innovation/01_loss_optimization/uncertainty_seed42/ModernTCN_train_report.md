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
| acc_main | 0.9672 |
| acc_turn | 0.5644 |
| acc_turn_pure | 0.5797 |
| acc_turn_transition | 0.4978 |
| main_confidence_mean | 0.9865 |
| main_low_conf_0p60_ratio | 0.0064 |
| main_low_conf_0p70_ratio | 0.0139 |
| turn_confidence_mean | 0.7842 |
| turn_low_conf_0p60_ratio | 0.2168 |
| turn_low_conf_0p70_ratio | 0.3465 |
| turn_right_recall | 0.6020 |
| turn_straight_recall | 0.5360 |
| turn_left_recall | 0.5931 |
| theta_mae_deg | 0.8750 |
| theta_abs_le_10_p95_abs_err_deg | 2.3904 |
| theta_neg_10_8_p95_abs_err_deg | 1.9406 |
| theta_pos_8_10_p95_abs_err_deg | 3.4214 |
| theta_abs_le_8_p95_abs_err_deg | 2.3257 |
| theta_neg_8_6_p95_abs_err_deg | 2.0793 |
| theta_pos_6_8_p95_abs_err_deg | 2.1997 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.5556 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.7306 |
| theta_flat_abs_p95_deg | 3.3471 |
| theta_flat_bias_deg | -0.2075 |
| theta_near_flat_abs_p95_deg | 2.1386 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1118 |
| theta_flat_turn_abs_p95_deg | 2.2106 |
| flat_recall | 0.9405 |
| stall_recall | 0.6979 |
| slope_recall | 0.9840 |
| uphill_recall | 0.7655 |
| downhill_recall | 0.8036 |

- best_epoch: 52
- train_seconds: 234.5

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 23 | 0.5217 | 0.5492 |
| [0.60,0.70) | 27 | 0.2222 | 0.6508 |
| [0.70,0.80) | 46 | 0.2391 | 0.7475 |
| [0.80,0.90) | 49 | 0.2857 | 0.8558 |
| [0.90,1.00) | 3457 | 0.0217 | 0.9971 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 781 | 0.6031 | 0.5111 |
| [0.60,0.70) | 467 | 0.5310 | 0.6473 |
| [0.70,0.80) | 429 | 0.4825 | 0.7501 |
| [0.80,0.90) | 559 | 0.4490 | 0.8510 |
| [0.90,1.00) | 1366 | 0.2870 | 0.9704 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.4978
- theta_mae_deg <= 0.7000 未满足，实际 0.8750

## 验证集最佳点

```json
{
  "loss_total": 0.5337182522626627,
  "acc_main": 0.9415426251691476,
  "acc_turn": 0.6016238159675237,
  "acc_turn_pure": 0.6201245493280891,
  "acc_turn_transition": 0.5139751552795031,
  "false_turn_straight": 0.48232848232848236,
  "flat_recall": 0.928462709284627,
  "stall_recall": 0.4523809523809524,
  "slope_recall": 0.9512683578104139,
  "recall_main": [
    0.928462709284627,
    0.4523809523809524,
    0.9512683578104139
  ],
  "turn_right_recall": 0.6457345971563981,
  "turn_straight_recall": 0.5176715176715176,
  "turn_left_recall": 0.7357065803667745,
  "recall_turn": [
    0.6457345971563981,
    0.5176715176715176,
    0.7357065803667745
  ],
  "cm_turn": [
    [
      545,
      185,
      114
    ],
    [
      409,
      996,
      519
    ],
    [
      82,
      163,
      682
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      610,
      0,
      47
    ],
    [
      0,
      19,
      23
    ],
    [
      137,
      9,
      2850
    ]
  ],
  "main_confidence_mean": 0.972126864662448,
  "main_confidence_error_mean": 0.8050586654587915,
  "main_low_conf_0p60_ratio": 0.007307171853856563,
  "main_low_conf_0p70_ratio": 0.05764546684709066,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 27,
      "error_rate": 0.37037037037037035,
      "mean_confidence": 0.5348403018932123
    },
    {
      "bin": "[0.60,0.70)",
      "n": 186,
      "error_rate": 0.46236559139784944,
      "mean_confidence": 0.6514009962289635
    },
    {
      "bin": "[0.70,0.80)",
      "n": 38,
      "error_rate": 0.42105263157894735,
      "mean_confidence": 0.7453369392108645
    },
    {
      "bin": "[0.80,0.90)",
      "n": 50,
      "error_rate": 0.3,
      "mean_confidence": 0.8596716854596644
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3394,
      "error_rate": 0.026222746022392458,
      "mean_confidence": 0.9973780505347807
    }
  ],
  "turn_confidence_mean": 0.8051250310754033,
  "turn_confidence_error_mean": 0.736479262907095,
  "turn_low_conf_0p60_ratio": 0.18944519621109607,
  "turn_low_conf_0p70_ratio": 0.30013531799729365,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 700,
      "error_rate": 0.61,
      "mean_confidence": 0.497091910323893
    },
    {
      "bin": "[0.60,0.70)",
      "n": 409,
      "error_rate": 0.5036674816625917,
      "mean_confidence": 0.6497794128675844
    },
    {
      "bin": "[0.70,0.80)",
      "n": 416,
      "error_rate": 0.47596153846153844,
      "mean_confidence": 0.7525807018001541
    },
    {
      "bin": "[0.80,0.90)",
      "n": 545,
      "error_rate": 0.44770642201834865,
      "mean_confidence": 0.8530505987290037
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1625,
      "error_rate": 0.2443076923076923,
      "mean_confidence": 0.9742933689094629
    }
  ],
  "theta_mae_rad": 0.016346348449587822,
  "theta_mae_deg": 0.9365767240524292,
  "uphill_recall": 0.7816711590296496,
  "downhill_recall": 0.8047830923248054,
  "slope_sign_acc": 0.9693402682726526,
  "theta_flat_mae_deg": 0.9770140051841736,
  "theta_flat_abs_p95_deg": 3.3367910385131836,
  "theta_flat_abs_max_deg": 7.01961088180542,
  "theta_flat_bias_deg": 0.4530036151409149,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.1937143802642822,
  "theta_near_flat_abs_p95_deg": 3.3367931842803955,
  "theta_near_flat_abs_max_deg": 7.01961088180542,
  "theta_near_flat_bias_deg": 0.8551796674728394,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.028824806213379,
  "theta_flat_turn_abs_p95_deg": 3.3367910385131836,
  "theta_flat_turn_abs_max_deg": 7.01961088180542,
  "theta_flat_turn_bias_deg": 0.6292563080787659,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9365767240524292,
  "theta_slope_control_abs_p95_deg": 9.016743659973145,
  "theta_slope_control_abs_max_deg": 12.498513221740723,
  "theta_slope_control_bias_deg": -0.23474988341331482,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.936576783657074,
  "theta_all_rmse_deg": 1.3018385171890259,
  "theta_all_p95_abs_err_deg": 2.6694562435150146,
  "theta_all_max_abs_err_deg": 7.51961088180542,
  "theta_all_bias_deg": -0.23474986851215363,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.9277092218399048,
  "theta_active_abs_ge_2_rmse_deg": 1.263069987297058,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.423931837081909,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.977638244628906,
  "theta_active_abs_ge_2_bias_deg": -0.3855690360069275,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9526041150093079,
  "theta_abs_le_8_rmse_deg": 1.3237391710281372,
  "theta_abs_le_8_p95_abs_err_deg": 2.7662837505340576,
  "theta_abs_le_8_max_abs_err_deg": 7.51961088180542,
  "theta_abs_le_8_bias_deg": -0.23622585833072662,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.936576783657074,
  "theta_abs_le_10_rmse_deg": 1.3018385171890259,
  "theta_abs_le_10_p95_abs_err_deg": 2.6694562435150146,
  "theta_abs_le_10_max_abs_err_deg": 7.51961088180542,
  "theta_abs_le_10_bias_deg": -0.23474986851215363,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.8845624923706055,
  "theta_pos_8_10_rmse_deg": 1.083021879196167,
  "theta_pos_8_10_p95_abs_err_deg": 1.9472248554229736,
  "theta_pos_8_10_max_abs_err_deg": 4.560789108276367,
  "theta_pos_8_10_bias_deg": -0.7407497763633728,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8530954122543335,
  "theta_neg_10_8_rmse_deg": 1.3176898956298828,
  "theta_neg_10_8_p95_abs_err_deg": 2.344910144805908,
  "theta_neg_10_8_max_abs_err_deg": 6.977638244628906,
  "theta_neg_10_8_bias_deg": 0.2925599217414856,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 1.0499944686889648,
  "theta_pos_6_8_rmse_deg": 1.26248037815094,
  "theta_pos_6_8_p95_abs_err_deg": 2.277265787124634,
  "theta_pos_6_8_max_abs_err_deg": 3.7447662353515625,
  "theta_pos_6_8_bias_deg": -0.8383254408836365,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8386064767837524,
  "theta_neg_8_6_rmse_deg": 1.189168095588684,
  "theta_neg_8_6_p95_abs_err_deg": 2.320167064666748,
  "theta_neg_8_6_max_abs_err_deg": 6.033095836639404,
  "theta_neg_8_6_bias_deg": -0.03302532061934471,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7894759178161621,
  "theta_neg_4_2_rmse_deg": 1.168089747428894,
  "theta_neg_4_2_p95_abs_err_deg": 2.187192916870117,
  "theta_neg_4_2_max_abs_err_deg": 6.279759407043457,
  "theta_neg_4_2_bias_deg": -0.4920472502708435,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5012443661689758,
  "theta_neg_2_0p5_rmse_deg": 0.7494584918022156,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.2815378904342651,
  "theta_neg_2_0p5_max_abs_err_deg": 4.589678764343262,
  "theta_neg_2_0p5_bias_deg": 0.04738751798868179,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.196681261062622,
  "theta_pos_0p5_2_rmse_deg": 1.4401931762695312,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.5667340755462646,
  "theta_pos_0p5_2_max_abs_err_deg": 4.20667839050293,
  "theta_pos_0p5_2_bias_deg": 0.264949232339859,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2804440800408065,
  "loss_turn": 1.2647273559208974,
  "loss_theta": 0.0005161441222377655,
  "loss_main_bundle": 0.2804440800408065,
  "loss_turn_bundle": 0.25294547563718683,
  "loss_theta_bundle": 0.00032869251028266617,
  "loss_theta_flat": 0.00017818960762728907,
  "loss_theta_near_flat": 0.0010387583696554353,
  "loss_theta_error_excess": 0.0001706171855966892,
  "loss_theta_flat_excess": 8.540339678792566e-05,
  "loss_theta_near_flat_excess": 0.0007164769648436925,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00014899621864686896,
  "loss_theta_small_neg": 0.0004104773021058629,
  "loss_theta_small_neg_excess": 0.00014325801881895993,
  "loss_turn_release": 0.43313770849101435,
  "loss_false_turn_straight": 0.3458787119436974
}
```
