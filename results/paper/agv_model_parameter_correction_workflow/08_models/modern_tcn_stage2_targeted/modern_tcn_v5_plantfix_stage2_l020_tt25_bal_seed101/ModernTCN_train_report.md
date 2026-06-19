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
| acc_main | 0.9670 |
| acc_turn | 0.5788 |
| acc_turn_pure | 0.5974 |
| acc_turn_transition | 0.4978 |
| main_confidence_mean | 0.9877 |
| main_low_conf_0p60_ratio | 0.0094 |
| main_low_conf_0p70_ratio | 0.0153 |
| turn_confidence_mean | 0.8373 |
| turn_low_conf_0p60_ratio | 0.1452 |
| turn_low_conf_0p70_ratio | 0.2401 |
| turn_right_recall | 0.6120 |
| turn_straight_recall | 0.5763 |
| turn_left_recall | 0.5540 |
| theta_mae_deg | 0.6794 |
| theta_abs_le_10_p95_abs_err_deg | 1.8275 |
| theta_neg_10_8_p95_abs_err_deg | 1.3394 |
| theta_pos_8_10_p95_abs_err_deg | 2.7551 |
| theta_abs_le_8_p95_abs_err_deg | 1.7706 |
| theta_neg_8_6_p95_abs_err_deg | 1.7457 |
| theta_pos_6_8_p95_abs_err_deg | 1.5541 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.5686 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5545 |
| theta_flat_abs_p95_deg | 2.5565 |
| theta_flat_bias_deg | -0.4761 |
| theta_near_flat_abs_p95_deg | 2.3973 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.5854 |
| theta_flat_turn_abs_p95_deg | 2.2504 |
| flat_recall | 0.9696 |
| stall_recall | 0.7188 |
| slope_recall | 0.9749 |
| uphill_recall | 0.7494 |
| downhill_recall | 0.7928 |

- best_epoch: 63
- train_seconds: 805.2

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 34 | 0.5588 | 0.5477 |
| [0.60,0.70) | 21 | 0.4762 | 0.6452 |
| [0.70,0.80) | 32 | 0.2500 | 0.7511 |
| [0.80,0.90) | 36 | 0.3056 | 0.8558 |
| [0.90,1.00) | 3479 | 0.0204 | 0.9976 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 523 | 0.6157 | 0.5127 |
| [0.60,0.70) | 342 | 0.6111 | 0.6497 |
| [0.70,0.80) | 355 | 0.5014 | 0.7537 |
| [0.80,0.90) | 523 | 0.4876 | 0.8545 |
| [0.90,1.00) | 1859 | 0.2975 | 0.9742 |


## 验证集最佳点

```json
{
  "loss_total": 0.5706024295744941,
  "acc_main": 0.9488497970230041,
  "acc_turn": 0.6313937753721245,
  "acc_turn_pure": 0.6473287446738775,
  "acc_turn_transition": 0.5559006211180124,
  "flat_recall": 0.9452054794520548,
  "stall_recall": 0.5952380952380952,
  "slope_recall": 0.9546061415220294,
  "recall_main": [
    0.9452054794520548,
    0.5952380952380952,
    0.9546061415220294
  ],
  "turn_right_recall": 0.7049763033175356,
  "turn_straight_recall": 0.5665280665280665,
  "turn_left_recall": 0.6990291262135923,
  "recall_turn": [
    0.7049763033175356,
    0.5665280665280665,
    0.6990291262135923
  ],
  "cm_turn": [
    [
      595,
      217,
      32
    ],
    [
      433,
      1090,
      401
    ],
    [
      108,
      171,
      648
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      621,
      0,
      36
    ],
    [
      0,
      25,
      17
    ],
    [
      130,
      6,
      2860
    ]
  ],
  "main_confidence_mean": 0.9674205828153506,
  "main_confidence_error_mean": 0.7352553166878298,
  "main_low_conf_0p60_ratio": 0.05277401894451962,
  "main_low_conf_0p70_ratio": 0.0571041948579161,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 195,
      "error_rate": 0.4717948717948718,
      "mean_confidence": 0.5281842108885593
    },
    {
      "bin": "[0.60,0.70)",
      "n": 16,
      "error_rate": 0.3125,
      "mean_confidence": 0.6535867175742942
    },
    {
      "bin": "[0.70,0.80)",
      "n": 30,
      "error_rate": 0.23333333333333334,
      "mean_confidence": 0.749372937043507
    },
    {
      "bin": "[0.80,0.90)",
      "n": 44,
      "error_rate": 0.25,
      "mean_confidence": 0.856102765757041
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3410,
      "error_rate": 0.021700879765395895,
      "mean_confidence": 0.9973654061858204
    }
  ],
  "turn_confidence_mean": 0.843676052868201,
  "turn_confidence_error_mean": 0.7765874535243075,
  "turn_low_conf_0p60_ratio": 0.14587280108254397,
  "turn_low_conf_0p70_ratio": 0.23328822733423546,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 539,
      "error_rate": 0.5936920222634509,
      "mean_confidence": 0.5040509602448768
    },
    {
      "bin": "[0.60,0.70)",
      "n": 323,
      "error_rate": 0.5232198142414861,
      "mean_confidence": 0.6515296350447167
    },
    {
      "bin": "[0.70,0.80)",
      "n": 337,
      "error_rate": 0.4421364985163205,
      "mean_confidence": 0.7517521228673936
    },
    {
      "bin": "[0.80,0.90)",
      "n": 482,
      "error_rate": 0.4460580912863071,
      "mean_confidence": 0.8515031834648947
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2014,
      "error_rate": 0.25273088381330683,
      "mean_confidence": 0.9788929870010823
    }
  ],
  "theta_mae_rad": 0.013736630789935589,
  "theta_mae_deg": 0.7870509028434753,
  "uphill_recall": 0.7795148247978436,
  "downhill_recall": 0.8064516129032258,
  "slope_sign_acc": 0.9783739392280317,
  "theta_flat_mae_deg": 1.1422817707061768,
  "theta_flat_abs_p95_deg": 3.3851137161254883,
  "theta_flat_abs_max_deg": 8.939093589782715,
  "theta_flat_bias_deg": -0.06637310981750488,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.440950632095337,
  "theta_near_flat_abs_p95_deg": 3.6001369953155518,
  "theta_near_flat_abs_max_deg": 8.939093589782715,
  "theta_near_flat_bias_deg": 0.21259362995624542,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.0836067199707031,
  "theta_flat_turn_abs_p95_deg": 3.999958038330078,
  "theta_flat_turn_abs_max_deg": 8.939093589782715,
  "theta_flat_turn_bias_deg": -0.4161737561225891,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7870509028434753,
  "theta_slope_control_abs_p95_deg": 9.469234466552734,
  "theta_slope_control_abs_max_deg": 12.99479866027832,
  "theta_slope_control_bias_deg": -0.05300269275903702,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7870509624481201,
  "theta_all_rmse_deg": 1.1655471324920654,
  "theta_all_p95_abs_err_deg": 2.596693515777588,
  "theta_all_max_abs_err_deg": 8.439093589782715,
  "theta_all_bias_deg": -0.05300268903374672,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7091515064239502,
  "theta_active_abs_ge_2_rmse_deg": 1.05241060256958,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2467947006225586,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.812583923339844,
  "theta_active_abs_ge_2_bias_deg": -0.05007065832614899,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8332028985023499,
  "theta_abs_le_8_rmse_deg": 1.2078698873519897,
  "theta_abs_le_8_p95_abs_err_deg": 2.735630750656128,
  "theta_abs_le_8_max_abs_err_deg": 8.439093589782715,
  "theta_abs_le_8_bias_deg": -0.0810881108045578,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7870509624481201,
  "theta_abs_le_10_rmse_deg": 1.1655471324920654,
  "theta_abs_le_10_p95_abs_err_deg": 2.596693515777588,
  "theta_abs_le_10_max_abs_err_deg": 8.439093589782715,
  "theta_abs_le_10_bias_deg": -0.05300268903374672,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.47745752334594727,
  "theta_pos_8_10_rmse_deg": 0.7024139761924744,
  "theta_pos_8_10_p95_abs_err_deg": 1.576554536819458,
  "theta_pos_8_10_max_abs_err_deg": 4.0589823722839355,
  "theta_pos_8_10_bias_deg": 0.035674817860126495,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7092410922050476,
  "theta_neg_10_8_rmse_deg": 1.1763237714767456,
  "theta_neg_10_8_p95_abs_err_deg": 2.2387073040008545,
  "theta_neg_10_8_max_abs_err_deg": 6.812583923339844,
  "theta_neg_10_8_bias_deg": 0.09579592943191528,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5457685589790344,
  "theta_pos_6_8_rmse_deg": 0.7860933542251587,
  "theta_pos_6_8_p95_abs_err_deg": 1.5395653247833252,
  "theta_pos_6_8_max_abs_err_deg": 3.827333927154541,
  "theta_pos_6_8_bias_deg": 0.07877080142498016,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8530511856079102,
  "theta_neg_8_6_rmse_deg": 1.1695231199264526,
  "theta_neg_8_6_p95_abs_err_deg": 1.9946731328964233,
  "theta_neg_8_6_max_abs_err_deg": 5.795051574707031,
  "theta_neg_8_6_bias_deg": -0.2330974042415619,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6645415425300598,
  "theta_neg_4_2_rmse_deg": 0.9344902634620667,
  "theta_neg_4_2_p95_abs_err_deg": 2.1207380294799805,
  "theta_neg_4_2_max_abs_err_deg": 3.6127617359161377,
  "theta_neg_4_2_bias_deg": -0.27624955773353577,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.8350244760513306,
  "theta_neg_2_0p5_rmse_deg": 1.1188451051712036,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.489424467086792,
  "theta_neg_2_0p5_max_abs_err_deg": 3.7408969402313232,
  "theta_neg_2_0p5_bias_deg": -0.7366548180580139,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1885055303573608,
  "theta_pos_0p5_2_rmse_deg": 1.4212909936904907,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.0091373920440674,
  "theta_pos_0p5_2_max_abs_err_deg": 3.450639486312866,
  "theta_pos_0p5_2_bias_deg": 0.5154407024383545,
  "theta_pos_0p5_2_n": 163.0
}
```
