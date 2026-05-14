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
| acc_main | 0.9783 |
| acc_turn | 0.9006 |
| acc_turn_pure | 0.9190 |
| acc_turn_transition | 0.7907 |
| main_confidence_mean | 0.9949 |
| main_low_conf_0p60_ratio | 0.0024 |
| main_low_conf_0p70_ratio | 0.0064 |
| turn_confidence_mean | 0.9644 |
| turn_low_conf_0p60_ratio | 0.0188 |
| turn_low_conf_0p70_ratio | 0.0388 |
| turn_right_recall | 0.8782 |
| turn_straight_recall | 0.9086 |
| turn_left_recall | 0.9016 |
| theta_mae_deg | 0.2507 |
| theta_abs_le_10_p95_abs_err_deg | 0.7995 |
| theta_neg_10_8_p95_abs_err_deg | 0.8823 |
| theta_pos_8_10_p95_abs_err_deg | 0.7723 |
| theta_abs_le_8_p95_abs_err_deg | 0.7927 |
| theta_neg_8_6_p95_abs_err_deg | 0.6831 |
| theta_pos_6_8_p95_abs_err_deg | 0.3985 |
| theta_neg_2_0p5_p95_abs_err_deg | 0.4663 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.3600 |
| theta_flat_abs_p95_deg | 2.0980 |
| theta_flat_bias_deg | 0.1249 |
| theta_near_flat_abs_p95_deg | 0.9715 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.2345 |
| theta_flat_turn_abs_p95_deg | 0.6888 |
| flat_recall | 0.9590 |
| stall_recall | 0.7009 |
| slope_recall | 0.9948 |
| uphill_recall | 0.8112 |
| downhill_recall | 0.7799 |

- best_epoch: 160
- train_seconds: 575.8

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 9 | 0.5556 | 0.5422 |
| [0.60,0.70) | 15 | 0.2667 | 0.6536 |
| [0.70,0.80) | 19 | 0.3158 | 0.7670 |
| [0.80,0.90) | 14 | 0.4286 | 0.8618 |
| [0.90,1.00) | 3676 | 0.0163 | 0.9991 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 70 | 0.5143 | 0.5465 |
| [0.60,0.70) | 75 | 0.4400 | 0.6480 |
| [0.70,0.80) | 94 | 0.4043 | 0.7549 |
| [0.80,0.90) | 177 | 0.2373 | 0.8561 |
| [0.90,1.00) | 3317 | 0.0669 | 0.9920 |


## 验证集最佳点

```json
{
  "loss_total": 0.32288132102086164,
  "acc_main": 0.9677790563866513,
  "acc_turn": 0.8243191407748369,
  "acc_turn_pure": 0.8500228623685414,
  "acc_turn_transition": 0.6904761904761905,
  "flat_recall": 0.9449901768172888,
  "stall_recall": 0.8936170212765957,
  "slope_recall": 0.9751340809361287,
  "recall_main": [
    0.9449901768172888,
    0.8936170212765957,
    0.9751340809361287
  ],
  "turn_right_recall": 0.7692307692307693,
  "turn_straight_recall": 0.8435374149659864,
  "turn_left_recall": 0.814176245210728,
  "recall_turn": [
    0.7692307692307693,
    0.8435374149659864,
    0.814176245210728
  ],
  "cm_turn": [
    [
      360,
      64,
      44
    ],
    [
      114,
      1364,
      139
    ],
    [
      23,
      74,
      425
    ]
  ],
  "n_turn_transition": 420,
  "n_turn_pure": 2187,
  "cm_main": [
    [
      481,
      1,
      27
    ],
    [
      5,
      42,
      0
    ],
    [
      48,
      3,
      2000
    ]
  ],
  "main_confidence_mean": 0.9931610478410092,
  "main_confidence_error_mean": 0.9189654453639223,
  "main_low_conf_0p60_ratio": 0.004602991944764097,
  "main_low_conf_0p70_ratio": 0.008438818565400843,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 12,
      "error_rate": 0.4166666666666667,
      "mean_confidence": 0.5447554112013805
    },
    {
      "bin": "[0.60,0.70)",
      "n": 10,
      "error_rate": 0.7,
      "mean_confidence": 0.6476989012962304
    },
    {
      "bin": "[0.70,0.80)",
      "n": 11,
      "error_rate": 0.2727272727272727,
      "mean_confidence": 0.7581267684432592
    },
    {
      "bin": "[0.80,0.90)",
      "n": 24,
      "error_rate": 0.25,
      "mean_confidence": 0.8555724426156691
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2550,
      "error_rate": 0.024705882352941175,
      "mean_confidence": 0.9989347704699922
    }
  ],
  "turn_confidence_mean": 0.9479443651553743,
  "turn_confidence_error_mean": 0.8802528045395291,
  "turn_low_conf_0p60_ratio": 0.03068661296509398,
  "turn_low_conf_0p70_ratio": 0.05945531261986958,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 80,
      "error_rate": 0.4875,
      "mean_confidence": 0.5410484576601119
    },
    {
      "bin": "[0.60,0.70)",
      "n": 75,
      "error_rate": 0.4533333333333333,
      "mean_confidence": 0.6486693135188668
    },
    {
      "bin": "[0.70,0.80)",
      "n": 104,
      "error_rate": 0.46153846153846156,
      "mean_confidence": 0.7546071775295418
    },
    {
      "bin": "[0.80,0.90)",
      "n": 174,
      "error_rate": 0.3103448275862069,
      "mean_confidence": 0.8560226787372354
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2174,
      "error_rate": 0.13017479300827967,
      "mean_confidence": 0.9898481105197724
    }
  ],
  "theta_mae_rad": 0.004095743410289288,
  "theta_mae_deg": 0.2346687912940979,
  "uphill_recall": 0.77217125382263,
  "downhill_recall": 0.8123003194888179,
  "slope_sign_acc": 0.98515625,
  "theta_flat_mae_deg": 0.26616162061691284,
  "theta_flat_abs_p95_deg": 1.9226521253585815,
  "theta_flat_abs_max_deg": 2.900019407272339,
  "theta_flat_bias_deg": 0.1663060337305069,
  "theta_flat_n": 509.0,
  "theta_near_flat_mae_deg": 0.38383176922798157,
  "theta_near_flat_abs_p95_deg": 1.4407703876495361,
  "theta_near_flat_abs_max_deg": 5.477874279022217,
  "theta_near_flat_bias_deg": 0.24465936422348022,
  "theta_near_flat_n": 212.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.27678611874580383,
  "theta_flat_turn_abs_p95_deg": 0.954170823097229,
  "theta_flat_turn_abs_max_deg": 1.4254937171936035,
  "theta_flat_turn_bias_deg": 0.27378156781196594,
  "theta_flat_turn_n": 94.0,
  "theta_slope_control_mae_deg": 0.2346687912940979,
  "theta_slope_control_abs_p95_deg": 9.285088539123535,
  "theta_slope_control_abs_max_deg": 10.031657218933105,
  "theta_slope_control_bias_deg": -0.0019405386410653591,
  "theta_slope_control_n": 2560.0,
  "theta_all_mae_deg": 0.2346688061952591,
  "theta_all_rmse_deg": 0.39093199372291565,
  "theta_all_p95_abs_err_deg": 0.6675336360931396,
  "theta_all_max_abs_err_deg": 3.8000195026397705,
  "theta_all_bias_deg": -0.0019405385246500373,
  "theta_all_n": 2560.0,
  "theta_active_abs_ge_2_mae_deg": 0.2268531769514084,
  "theta_active_abs_ge_2_rmse_deg": 0.3725736439228058,
  "theta_active_abs_ge_2_p95_abs_err_deg": 0.6682018637657166,
  "theta_active_abs_ge_2_max_abs_err_deg": 3.2063910961151123,
  "theta_active_abs_ge_2_bias_deg": -0.04369456693530083,
  "theta_active_abs_ge_2_n": 2051.0,
  "theta_abs_le_8_mae_deg": 0.22395160794258118,
  "theta_abs_le_8_rmse_deg": 0.3700976073741913,
  "theta_abs_le_8_p95_abs_err_deg": 0.6284807920455933,
  "theta_abs_le_8_max_abs_err_deg": 3.8000195026397705,
  "theta_abs_le_8_bias_deg": 0.014270065352320671,
  "theta_abs_le_8_n": 2031.0,
  "theta_abs_le_10_mae_deg": 0.2346688061952591,
  "theta_abs_le_10_rmse_deg": 0.39093199372291565,
  "theta_abs_le_10_p95_abs_err_deg": 0.6675336360931396,
  "theta_abs_le_10_max_abs_err_deg": 3.8000195026397705,
  "theta_abs_le_10_bias_deg": -0.0019405385246500373,
  "theta_abs_le_10_n": 2560.0,
  "theta_pos_8_10_mae_deg": 0.2886958718299866,
  "theta_pos_8_10_rmse_deg": 0.3981892168521881,
  "theta_pos_8_10_p95_abs_err_deg": 0.739868700504303,
  "theta_pos_8_10_max_abs_err_deg": 1.6239908933639526,
  "theta_pos_8_10_bias_deg": -0.24430342018604279,
  "theta_pos_8_10_n": 251.0,
  "theta_neg_10_8_mae_deg": 0.2641861140727997,
  "theta_neg_10_8_rmse_deg": 0.5133169293403625,
  "theta_neg_10_8_p95_abs_err_deg": 1.2637064456939697,
  "theta_neg_10_8_max_abs_err_deg": 3.2063910961151123,
  "theta_neg_10_8_bias_deg": 0.09845279157161713,
  "theta_neg_10_8_n": 278.0,
  "theta_pos_6_8_mae_deg": 0.258909672498703,
  "theta_pos_6_8_rmse_deg": 0.3333459794521332,
  "theta_pos_6_8_p95_abs_err_deg": 0.6674593091011047,
  "theta_pos_6_8_max_abs_err_deg": 1.0961053371429443,
  "theta_pos_6_8_bias_deg": -0.21607400476932526,
  "theta_pos_6_8_n": 241.0,
  "theta_neg_8_6_mae_deg": 0.19279856979846954,
  "theta_neg_8_6_rmse_deg": 0.41380777955055237,
  "theta_neg_8_6_p95_abs_err_deg": 0.9387240409851074,
  "theta_neg_8_6_max_abs_err_deg": 2.107431173324585,
  "theta_neg_8_6_bias_deg": 0.1057235449552536,
  "theta_neg_8_6_n": 251.0,
  "theta_neg_4_2_mae_deg": 0.17086733877658844,
  "theta_neg_4_2_rmse_deg": 0.23419177532196045,
  "theta_neg_4_2_p95_abs_err_deg": 0.48687851428985596,
  "theta_neg_4_2_max_abs_err_deg": 0.7922677397727966,
  "theta_neg_4_2_bias_deg": 0.027478886768221855,
  "theta_neg_4_2_n": 198.0,
  "theta_neg_2_0p5_mae_deg": 0.30912524461746216,
  "theta_neg_2_0p5_rmse_deg": 0.6934260725975037,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.0502840280532837,
  "theta_neg_2_0p5_max_abs_err_deg": 3.8000195026397705,
  "theta_neg_2_0p5_bias_deg": 0.19923123717308044,
  "theta_neg_2_0p5_n": 138.0,
  "theta_pos_0p5_2_mae_deg": 0.2217312604188919,
  "theta_pos_0p5_2_rmse_deg": 0.2758835554122925,
  "theta_pos_0p5_2_p95_abs_err_deg": 0.532995879650116,
  "theta_pos_0p5_2_max_abs_err_deg": 0.8693178296089172,
  "theta_pos_0p5_2_bias_deg": 0.18508504331111908,
  "theta_pos_0p5_2_n": 168.0
}
```
