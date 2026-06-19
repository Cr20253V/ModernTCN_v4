# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
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
    1.5,
    0.75,
    1.5
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 3.0,
  "select_turn_weight": 0.6,
  "select_turn_transition_weight": 1.45,
  "select_turn_transition_target": 0.82,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.88,
  "select_turn_lr_weight": 0.8,
  "select_turn_lr_target": 0.88,
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
| acc_main | 0.9567 |
| acc_turn | 0.5883 |
| acc_turn_pure | 0.5988 |
| acc_turn_transition | 0.5425 |
| main_confidence_mean | 0.9875 |
| main_low_conf_0p60_ratio | 0.0050 |
| main_low_conf_0p70_ratio | 0.0147 |
| turn_confidence_mean | 0.8428 |
| turn_low_conf_0p60_ratio | 0.1308 |
| turn_low_conf_0p70_ratio | 0.2260 |
| turn_right_recall | 0.6008 |
| turn_straight_recall | 0.5996 |
| turn_left_recall | 0.5517 |
| theta_mae_deg | 0.6246 |
| theta_abs_le_10_p95_abs_err_deg | 1.6794 |
| theta_neg_10_8_p95_abs_err_deg | 1.5239 |
| theta_pos_8_10_p95_abs_err_deg | 2.4705 |
| theta_abs_le_8_p95_abs_err_deg | 1.6130 |
| theta_neg_8_6_p95_abs_err_deg | 1.5937 |
| theta_pos_6_8_p95_abs_err_deg | 1.6978 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.4426 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.6883 |
| theta_flat_abs_p95_deg | 2.6832 |
| theta_flat_bias_deg | 0.0252 |
| theta_near_flat_abs_p95_deg | 1.6664 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.0019 |
| theta_flat_turn_abs_p95_deg | 1.5775 |
| flat_recall | 0.9312 |
| stall_recall | 0.7083 |
| slope_recall | 0.9724 |
| uphill_recall | 0.7489 |
| downhill_recall | 0.8059 |

- best_epoch: 83
- train_seconds: 1067.8

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 18 | 0.4444 | 0.5336 |
| [0.60,0.70) | 35 | 0.7143 | 0.6478 |
| [0.70,0.80) | 34 | 0.6471 | 0.7553 |
| [0.80,0.90) | 54 | 0.3889 | 0.8616 |
| [0.90,1.00) | 3461 | 0.0231 | 0.9975 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 471 | 0.6178 | 0.5098 |
| [0.60,0.70) | 343 | 0.5627 | 0.6516 |
| [0.70,0.80) | 417 | 0.5348 | 0.7502 |
| [0.80,0.90) | 487 | 0.4394 | 0.8537 |
| [0.90,1.00) | 1884 | 0.2983 | 0.9785 |


## 验证集最佳点

```json
{
  "loss_total": 0.6663108485154757,
  "acc_main": 0.9420838971583221,
  "acc_turn": 0.638700947225981,
  "acc_turn_pure": 0.6515896427400852,
  "acc_turn_transition": 0.577639751552795,
  "flat_recall": 0.928462709284627,
  "stall_recall": 0.5,
  "slope_recall": 0.9512683578104139,
  "recall_main": [
    0.928462709284627,
    0.5,
    0.9512683578104139
  ],
  "turn_right_recall": 0.6872037914691943,
  "turn_straight_recall": 0.5977130977130977,
  "turn_left_recall": 0.6796116504854369,
  "recall_turn": [
    0.6872037914691943,
    0.5977130977130977,
    0.6796116504854369
  ],
  "cm_turn": [
    [
      580,
      206,
      58
    ],
    [
      401,
      1150,
      373
    ],
    [
      112,
      185,
      630
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
      21,
      21
    ],
    [
      132,
      14,
      2850
    ]
  ],
  "main_confidence_mean": 0.967667059629937,
  "main_confidence_error_mean": 0.7689326074776381,
  "main_low_conf_0p60_ratio": 0.05142083897158322,
  "main_low_conf_0p70_ratio": 0.05791610284167794,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 190,
      "error_rate": 0.45263157894736844,
      "mean_confidence": 0.5186941591972121
    },
    {
      "bin": "[0.60,0.70)",
      "n": 24,
      "error_rate": 0.2916666666666667,
      "mean_confidence": 0.6635541717363668
    },
    {
      "bin": "[0.70,0.80)",
      "n": 27,
      "error_rate": 0.37037037037037035,
      "mean_confidence": 0.7483929685272166
    },
    {
      "bin": "[0.80,0.90)",
      "n": 43,
      "error_rate": 0.32558139534883723,
      "mean_confidence": 0.8598637545708246
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3411,
      "error_rate": 0.028437408384637937,
      "mean_confidence": 0.9979102443174124
    }
  ],
  "turn_confidence_mean": 0.8576964346623418,
  "turn_confidence_error_mean": 0.7857124274850892,
  "turn_low_conf_0p60_ratio": 0.13315290933694182,
  "turn_low_conf_0p70_ratio": 0.20568335588633288,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 492,
      "error_rate": 0.6260162601626016,
      "mean_confidence": 0.5076233245343406
    },
    {
      "bin": "[0.60,0.70)",
      "n": 268,
      "error_rate": 0.4925373134328358,
      "mean_confidence": 0.6527509384352461
    },
    {
      "bin": "[0.70,0.80)",
      "n": 338,
      "error_rate": 0.47928994082840237,
      "mean_confidence": 0.7478761123548576
    },
    {
      "bin": "[0.80,0.90)",
      "n": 417,
      "error_rate": 0.4460431654676259,
      "mean_confidence": 0.8503006254734733
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2180,
      "error_rate": 0.2509174311926605,
      "mean_confidence": 0.980340785370381
    }
  ],
  "theta_mae_rad": 0.013808946125209332,
  "theta_mae_deg": 0.7911942601203918,
  "uphill_recall": 0.7778975741239892,
  "downhill_recall": 0.8086763070077865,
  "slope_sign_acc": 0.9685190254585272,
  "theta_flat_mae_deg": 1.0737022161483765,
  "theta_flat_abs_p95_deg": 3.4566152095794678,
  "theta_flat_abs_max_deg": 6.594043731689453,
  "theta_flat_bias_deg": 0.588955819606781,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.3204864263534546,
  "theta_near_flat_abs_p95_deg": 3.4574708938598633,
  "theta_near_flat_abs_max_deg": 6.0876994132995605,
  "theta_near_flat_bias_deg": 0.8571364879608154,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.0415401458740234,
  "theta_flat_turn_abs_p95_deg": 3.4566152095794678,
  "theta_flat_turn_abs_max_deg": 4.998394966125488,
  "theta_flat_turn_bias_deg": 0.47931304574012756,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7911942601203918,
  "theta_slope_control_abs_p95_deg": 9.35023021697998,
  "theta_slope_control_abs_max_deg": 12.863958358764648,
  "theta_slope_control_bias_deg": 0.07872254401445389,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7911942601203918,
  "theta_all_rmse_deg": 1.161718726158142,
  "theta_all_p95_abs_err_deg": 2.4641501903533936,
  "theta_all_max_abs_err_deg": 7.0329976081848145,
  "theta_all_bias_deg": 0.07872253656387329,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7292425036430359,
  "theta_active_abs_ge_2_rmse_deg": 1.086620807647705,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.0962414741516113,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.0329976081848145,
  "theta_active_abs_ge_2_bias_deg": -0.03316773101687431,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8223274946212769,
  "theta_abs_le_8_rmse_deg": 1.1941258907318115,
  "theta_abs_le_8_p95_abs_err_deg": 2.6352851390838623,
  "theta_abs_le_8_max_abs_err_deg": 7.0329976081848145,
  "theta_abs_le_8_bias_deg": 0.11543656140565872,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7911942601203918,
  "theta_abs_le_10_rmse_deg": 1.161718726158142,
  "theta_abs_le_10_p95_abs_err_deg": 2.4641501903533936,
  "theta_abs_le_10_max_abs_err_deg": 7.0329976081848145,
  "theta_abs_le_10_bias_deg": 0.07872253656387329,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5448276996612549,
  "theta_pos_8_10_rmse_deg": 0.7334372997283936,
  "theta_pos_8_10_p95_abs_err_deg": 1.4293193817138672,
  "theta_pos_8_10_max_abs_err_deg": 3.6464192867279053,
  "theta_pos_8_10_bias_deg": -0.23557166755199432,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7768741846084595,
  "theta_neg_10_8_rmse_deg": 1.2351408004760742,
  "theta_neg_10_8_p95_abs_err_deg": 2.2138023376464844,
  "theta_neg_10_8_max_abs_err_deg": 6.671304225921631,
  "theta_neg_10_8_bias_deg": 0.08601175993680954,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.598999559879303,
  "theta_pos_6_8_rmse_deg": 0.7987620830535889,
  "theta_pos_6_8_p95_abs_err_deg": 1.626718521118164,
  "theta_pos_6_8_max_abs_err_deg": 3.3206822872161865,
  "theta_pos_6_8_bias_deg": 0.009439412504434586,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7765240669250488,
  "theta_neg_8_6_rmse_deg": 1.179206371307373,
  "theta_neg_8_6_p95_abs_err_deg": 2.541109800338745,
  "theta_neg_8_6_max_abs_err_deg": 6.269589424133301,
  "theta_neg_8_6_bias_deg": 0.03941793739795685,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7502206563949585,
  "theta_neg_4_2_rmse_deg": 1.0701885223388672,
  "theta_neg_4_2_p95_abs_err_deg": 2.0852725505828857,
  "theta_neg_4_2_max_abs_err_deg": 5.6456618309021,
  "theta_neg_4_2_bias_deg": -0.24334488809108734,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6975629329681396,
  "theta_neg_2_0p5_rmse_deg": 0.9559730291366577,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.757128357887268,
  "theta_neg_2_0p5_max_abs_err_deg": 4.826270580291748,
  "theta_neg_2_0p5_bias_deg": 0.014855864457786083,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.2400223016738892,
  "theta_pos_0p5_2_rmse_deg": 1.4645144939422607,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.9954283237457275,
  "theta_pos_0p5_2_max_abs_err_deg": 4.822071075439453,
  "theta_pos_0p5_2_bias_deg": 0.9708139896392822,
  "theta_pos_0p5_2_n": 163.0
}
```
