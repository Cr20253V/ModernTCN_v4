# ModernTCN-small 第一阶段训练报告

## 固定约束

- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`
- vehicle: `diagonal_dual_steer_drive_agv`; active=`LF,RR`; passive=`RF,LR`
- feature_policy: `keep_current_algorithm_inputs_unchanged`
- label_time_policy: `current_window_end`, horizon_steps=0
- split: 使用 MAT 文件已有 run-level split，不重划分。
- scaler: 使用 MAT 文件已有归一化后 X，不重新拟合。
- confidence_policy: `derive_classification_confidence_from_softmax_and_export`
- input: `[batch, time=128, feature=19]`
- output: `logits_main`, `logits_turn`, `theta_hat`

## 配置

```json
{
  "input_dim": 19,
  "seq_len": 128,
  "channels": 64,
  "blocks": 5,
  "kernel_size": 31,
  "temporal_padding": "causal",
  "dropout": 0.15,
  "expansion": 2,
  "readout_input_stats": true,
  "turn_head_source": "full",
  "turn_feature_indices": [
    1,
    4,
    5,
    6,
    7,
    9,
    10,
    11,
    16
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
| acc_main | 0.9759 |
| acc_turn | 0.8845 |
| acc_turn_pure | 0.9074 |
| acc_turn_transition | 0.7477 |
| main_confidence_mean | 0.9922 |
| main_low_conf_0p60_ratio | 0.0054 |
| main_low_conf_0p70_ratio | 0.0099 |
| turn_confidence_mean | 0.9331 |
| turn_low_conf_0p60_ratio | 0.0445 |
| turn_low_conf_0p70_ratio | 0.0804 |
| turn_right_recall | 0.8635 |
| turn_straight_recall | 0.8908 |
| turn_left_recall | 0.8893 |
| theta_mae_deg | 0.3624 |
| theta_abs_le_10_p95_abs_err_deg | 1.0491 |
| theta_neg_10_8_p95_abs_err_deg | 1.0001 |
| theta_pos_8_10_p95_abs_err_deg | 2.2814 |
| theta_abs_le_8_p95_abs_err_deg | 0.9328 |
| theta_neg_8_6_p95_abs_err_deg | 0.9315 |
| theta_pos_6_8_p95_abs_err_deg | 0.8785 |
| theta_neg_2_0p5_p95_abs_err_deg | 0.8430 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5075 |
| theta_flat_abs_p95_deg | 2.2972 |
| theta_flat_bias_deg | 0.0045 |
| theta_near_flat_abs_p95_deg | 1.1099 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.2035 |
| theta_flat_turn_abs_p95_deg | 0.8883 |
| flat_recall | 0.9709 |
| stall_recall | 0.6838 |
| slope_recall | 0.9892 |
| uphill_recall | 0.8032 |
| downhill_recall | 0.7740 |

- best_epoch: 82
- train_seconds: 379.4

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 20 | 0.7000 | 0.5330 |
| [0.60,0.70) | 17 | 0.5882 | 0.6555 |
| [0.70,0.80) | 12 | 0.4167 | 0.7515 |
| [0.80,0.90) | 32 | 0.3125 | 0.8556 |
| [0.90,1.00) | 3652 | 0.0140 | 0.9983 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 166 | 0.4458 | 0.5426 |
| [0.60,0.70) | 134 | 0.4254 | 0.6534 |
| [0.70,0.80) | 189 | 0.3016 | 0.7536 |
| [0.80,0.90) | 284 | 0.2254 | 0.8585 |
| [0.90,1.00) | 2960 | 0.0605 | 0.9862 |


## 验证集最佳点

```json
{
  "loss_total": 0.28751576165152454,
  "acc_main": 0.9685462217107786,
  "acc_turn": 0.7871116225546605,
  "acc_turn_pure": 0.8116140832190215,
  "acc_turn_transition": 0.6595238095238095,
  "flat_recall": 0.9390962671905697,
  "stall_recall": 0.8723404255319149,
  "slope_recall": 0.9780594831789371,
  "recall_main": [
    0.9390962671905697,
    0.8723404255319149,
    0.9780594831789371
  ],
  "turn_right_recall": 0.7051282051282052,
  "turn_straight_recall": 0.8132343846629561,
  "turn_left_recall": 0.7796934865900383,
  "recall_turn": [
    0.7051282051282052,
    0.8132343846629561,
    0.7796934865900383
  ],
  "cm_turn": [
    [
      330,
      105,
      33
    ],
    [
      160,
      1315,
      142
    ],
    [
      19,
      96,
      407
    ]
  ],
  "n_turn_transition": 420,
  "n_turn_pure": 2187,
  "cm_main": [
    [
      478,
      0,
      31
    ],
    [
      6,
      41,
      0
    ],
    [
      37,
      8,
      2006
    ]
  ],
  "main_confidence_mean": 0.9911339074964096,
  "main_confidence_error_mean": 0.873634795939353,
  "main_low_conf_0p60_ratio": 0.004602991944764097,
  "main_low_conf_0p70_ratio": 0.011507479861910242,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 12,
      "error_rate": 0.5833333333333334,
      "mean_confidence": 0.5391415749605936
    },
    {
      "bin": "[0.60,0.70)",
      "n": 18,
      "error_rate": 0.4444444444444444,
      "mean_confidence": 0.6581175039724233
    },
    {
      "bin": "[0.70,0.80)",
      "n": 14,
      "error_rate": 0.5714285714285714,
      "mean_confidence": 0.7439200887799915
    },
    {
      "bin": "[0.80,0.90)",
      "n": 21,
      "error_rate": 0.42857142857142855,
      "mean_confidence": 0.856347062736778
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2542,
      "error_rate": 0.01966955153422502,
      "mean_confidence": 0.9981007526796685
    }
  ],
  "turn_confidence_mean": 0.9138851809032068,
  "turn_confidence_error_mean": 0.8041563850769713,
  "turn_low_conf_0p60_ratio": 0.06098964326812428,
  "turn_low_conf_0p70_ratio": 0.11814345991561181,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 159,
      "error_rate": 0.6729559748427673,
      "mean_confidence": 0.5424884757532413
    },
    {
      "bin": "[0.60,0.70)",
      "n": 149,
      "error_rate": 0.48322147651006714,
      "mean_confidence": 0.6492568280721142
    },
    {
      "bin": "[0.70,0.80)",
      "n": 161,
      "error_rate": 0.42857142857142855,
      "mean_confidence": 0.7506183846899946
    },
    {
      "bin": "[0.80,0.90)",
      "n": 215,
      "error_rate": 0.3395348837209302,
      "mean_confidence": 0.8564864635219277
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1923,
      "error_rate": 0.12168486739469579,
      "mean_confidence": 0.9851843900129205
    }
  ],
  "theta_mae_rad": 0.005639627575874329,
  "theta_mae_deg": 0.3231268525123596,
  "uphill_recall": 0.7805810397553516,
  "downhill_recall": 0.8115015974440895,
  "slope_sign_acc": 0.977734375,
  "theta_flat_mae_deg": 0.30715224146842957,
  "theta_flat_abs_p95_deg": 1.9941304922103882,
  "theta_flat_abs_max_deg": 2.373168468475342,
  "theta_flat_bias_deg": -0.012729405425488949,
  "theta_flat_n": 509.0,
  "theta_near_flat_mae_deg": 0.4410984516143799,
  "theta_near_flat_abs_p95_deg": 1.532742977142334,
  "theta_near_flat_abs_max_deg": 4.905267715454102,
  "theta_near_flat_bias_deg": 0.08793773502111435,
  "theta_near_flat_n": 212.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.26309219002723694,
  "theta_flat_turn_abs_p95_deg": 1.0886380672454834,
  "theta_flat_turn_abs_max_deg": 1.9731196165084839,
  "theta_flat_turn_bias_deg": -0.009256131015717983,
  "theta_flat_turn_n": 94.0,
  "theta_slope_control_mae_deg": 0.3231268525123596,
  "theta_slope_control_abs_p95_deg": 9.318086624145508,
  "theta_slope_control_abs_max_deg": 10.71541690826416,
  "theta_slope_control_bias_deg": -0.14471690356731415,
  "theta_slope_control_n": 2560.0,
  "theta_all_mae_deg": 0.3231268525123596,
  "theta_all_rmse_deg": 0.4614635705947876,
  "theta_all_p95_abs_err_deg": 0.8325545787811279,
  "theta_all_max_abs_err_deg": 2.9181652069091797,
  "theta_all_bias_deg": -0.14471688866615295,
  "theta_all_n": 2560.0,
  "theta_active_abs_ge_2_mae_deg": 0.327091246843338,
  "theta_active_abs_ge_2_rmse_deg": 0.460894912481308,
  "theta_active_abs_ge_2_p95_abs_err_deg": 0.8307257890701294,
  "theta_active_abs_ge_2_max_abs_err_deg": 2.5411972999572754,
  "theta_active_abs_ge_2_bias_deg": -0.17747245728969574,
  "theta_active_abs_ge_2_n": 2051.0,
  "theta_abs_le_8_mae_deg": 0.3095463812351227,
  "theta_abs_le_8_rmse_deg": 0.4390093982219696,
  "theta_abs_le_8_p95_abs_err_deg": 0.781577467918396,
  "theta_abs_le_8_max_abs_err_deg": 2.9181652069091797,
  "theta_abs_le_8_bias_deg": -0.11739425361156464,
  "theta_abs_le_8_n": 2031.0,
  "theta_abs_le_10_mae_deg": 0.3231268525123596,
  "theta_abs_le_10_rmse_deg": 0.4614635705947876,
  "theta_abs_le_10_p95_abs_err_deg": 0.8325545787811279,
  "theta_abs_le_10_max_abs_err_deg": 2.9181652069091797,
  "theta_abs_le_10_bias_deg": -0.14471688866615295,
  "theta_abs_le_10_n": 2560.0,
  "theta_pos_8_10_mae_deg": 0.3857411742210388,
  "theta_pos_8_10_rmse_deg": 0.5812473297119141,
  "theta_pos_8_10_p95_abs_err_deg": 1.3128585815429688,
  "theta_pos_8_10_max_abs_err_deg": 2.5411972999572754,
  "theta_pos_8_10_bias_deg": -0.3671458065509796,
  "theta_pos_8_10_n": 251.0,
  "theta_neg_10_8_mae_deg": 0.36580920219421387,
  "theta_neg_10_8_rmse_deg": 0.4978926479816437,
  "theta_neg_10_8_p95_abs_err_deg": 0.9880511164665222,
  "theta_neg_10_8_max_abs_err_deg": 2.520285129547119,
  "theta_neg_10_8_bias_deg": -0.14350338280200958,
  "theta_neg_10_8_n": 278.0,
  "theta_pos_6_8_mae_deg": 0.34706050157546997,
  "theta_pos_6_8_rmse_deg": 0.45368117094039917,
  "theta_pos_6_8_p95_abs_err_deg": 0.8335199356079102,
  "theta_pos_6_8_max_abs_err_deg": 1.7171918153762817,
  "theta_pos_6_8_bias_deg": -0.28412574529647827,
  "theta_pos_6_8_n": 241.0,
  "theta_neg_8_6_mae_deg": 0.26079031825065613,
  "theta_neg_8_6_rmse_deg": 0.46731603145599365,
  "theta_neg_8_6_p95_abs_err_deg": 0.8979487419128418,
  "theta_neg_8_6_max_abs_err_deg": 2.265080213546753,
  "theta_neg_8_6_bias_deg": 0.0026329942047595978,
  "theta_neg_8_6_n": 251.0,
  "theta_neg_4_2_mae_deg": 0.31961992383003235,
  "theta_neg_4_2_rmse_deg": 0.3703446388244629,
  "theta_neg_4_2_p95_abs_err_deg": 0.6175187826156616,
  "theta_neg_4_2_max_abs_err_deg": 0.924148678779602,
  "theta_neg_4_2_bias_deg": -0.18261036276817322,
  "theta_neg_4_2_n": 198.0,
  "theta_neg_2_0p5_mae_deg": 0.41369712352752686,
  "theta_neg_2_0p5_rmse_deg": 0.6595531702041626,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.2528156042099,
  "theta_neg_2_0p5_max_abs_err_deg": 2.9181652069091797,
  "theta_neg_2_0p5_bias_deg": -0.024330778047442436,
  "theta_neg_2_0p5_n": 138.0,
  "theta_pos_0p5_2_mae_deg": 0.2188328355550766,
  "theta_pos_0p5_2_rmse_deg": 0.2723565995693207,
  "theta_pos_0p5_2_p95_abs_err_deg": 0.5175847411155701,
  "theta_pos_0p5_2_max_abs_err_deg": 0.823261022567749,
  "theta_pos_0p5_2_bias_deg": 0.05513142794370651,
  "theta_pos_0p5_2_n": 168.0
}
```
