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
| acc_turn | 0.8725 |
| acc_turn_pure | 0.8949 |
| acc_turn_transition | 0.7383 |
| main_confidence_mean | 0.9944 |
| main_low_conf_0p60_ratio | 0.0032 |
| main_low_conf_0p70_ratio | 0.0064 |
| turn_confidence_mean | 0.9299 |
| turn_low_conf_0p60_ratio | 0.0447 |
| turn_low_conf_0p70_ratio | 0.0828 |
| turn_right_recall | 0.8401 |
| turn_straight_recall | 0.8734 |
| turn_left_recall | 0.9057 |
| theta_mae_deg | 0.3353 |
| theta_abs_le_10_p95_abs_err_deg | 0.9870 |
| theta_neg_10_8_p95_abs_err_deg | 0.8279 |
| theta_pos_8_10_p95_abs_err_deg | 1.1743 |
| theta_abs_le_8_p95_abs_err_deg | 0.9643 |
| theta_neg_8_6_p95_abs_err_deg | 1.0082 |
| theta_pos_6_8_p95_abs_err_deg | 0.9792 |
| theta_neg_2_0p5_p95_abs_err_deg | 0.6704 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4108 |
| theta_flat_abs_p95_deg | 2.2296 |
| theta_flat_bias_deg | 0.0877 |
| theta_near_flat_abs_p95_deg | 1.0815 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.1520 |
| theta_flat_turn_abs_p95_deg | 0.8254 |
| flat_recall | 0.9590 |
| stall_recall | 0.6752 |
| slope_recall | 0.9927 |
| uphill_recall | 0.8112 |
| downhill_recall | 0.7767 |

- best_epoch: 81
- train_seconds: 376.6

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 12 | 0.8333 | 0.5246 |
| [0.60,0.70) | 12 | 0.2500 | 0.6315 |
| [0.70,0.80) | 14 | 0.5000 | 0.7495 |
| [0.80,0.90) | 23 | 0.4348 | 0.8629 |
| [0.90,1.00) | 3672 | 0.0163 | 0.9989 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 167 | 0.5090 | 0.5300 |
| [0.60,0.70) | 142 | 0.4577 | 0.6525 |
| [0.70,0.80) | 189 | 0.3810 | 0.7521 |
| [0.80,0.90) | 300 | 0.2767 | 0.8590 |
| [0.90,1.00) | 2935 | 0.0583 | 0.9847 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.7383

## 验证集最佳点

```json
{
  "loss_total": 0.2645873693291328,
  "acc_main": 0.9754507096279248,
  "acc_turn": 0.7825086306098964,
  "acc_turn_pure": 0.8184727937814358,
  "acc_turn_transition": 0.5952380952380952,
  "flat_recall": 0.9548133595284872,
  "stall_recall": 0.8936170212765957,
  "slope_recall": 0.9824475865431497,
  "recall_main": [
    0.9548133595284872,
    0.8936170212765957,
    0.9824475865431497
  ],
  "turn_right_recall": 0.717948717948718,
  "turn_straight_recall": 0.8021026592455164,
  "turn_left_recall": 0.7796934865900383,
  "recall_turn": [
    0.717948717948718,
    0.8021026592455164,
    0.7796934865900383
  ],
  "cm_turn": [
    [
      336,
      90,
      42
    ],
    [
      115,
      1297,
      205
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
      486,
      0,
      23
    ],
    [
      5,
      42,
      0
    ],
    [
      30,
      6,
      2015
    ]
  ],
  "main_confidence_mean": 0.9935123898903784,
  "main_confidence_error_mean": 0.8854200712365903,
  "main_low_conf_0p60_ratio": 0.0038358266206367474,
  "main_low_conf_0p70_ratio": 0.007671653241273495,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 10,
      "error_rate": 0.4,
      "mean_confidence": 0.5442857021139483
    },
    {
      "bin": "[0.60,0.70)",
      "n": 10,
      "error_rate": 0.5,
      "mean_confidence": 0.6520745729553596
    },
    {
      "bin": "[0.70,0.80)",
      "n": 13,
      "error_rate": 0.46153846153846156,
      "mean_confidence": 0.7484407224254839
    },
    {
      "bin": "[0.80,0.90)",
      "n": 18,
      "error_rate": 0.6111111111111112,
      "mean_confidence": 0.8559243251112014
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2556,
      "error_rate": 0.01486697965571205,
      "mean_confidence": 0.9988211386737054
    }
  ],
  "turn_confidence_mean": 0.9101969039465264,
  "turn_confidence_error_mean": 0.816095277315759,
  "turn_low_conf_0p60_ratio": 0.05485232067510549,
  "turn_low_conf_0p70_ratio": 0.10510164940544688,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 143,
      "error_rate": 0.5524475524475524,
      "mean_confidence": 0.5396794758331063
    },
    {
      "bin": "[0.60,0.70)",
      "n": 131,
      "error_rate": 0.5038167938931297,
      "mean_confidence": 0.6484180918342813
    },
    {
      "bin": "[0.70,0.80)",
      "n": 210,
      "error_rate": 0.44285714285714284,
      "mean_confidence": 0.7503651047909524
    },
    {
      "bin": "[0.80,0.90)",
      "n": 287,
      "error_rate": 0.34146341463414637,
      "mean_confidence": 0.8554152340630153
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1836,
      "error_rate": 0.12581699346405228,
      "mean_confidence": 0.9845781859106666
    }
  ],
  "theta_mae_rad": 0.00548357842490077,
  "theta_mae_deg": 0.31418588757514954,
  "uphill_recall": 0.7813455657492355,
  "downhill_recall": 0.8115015974440895,
  "slope_sign_acc": 0.981640625,
  "theta_flat_mae_deg": 0.30197975039482117,
  "theta_flat_abs_p95_deg": 1.8146790266036987,
  "theta_flat_abs_max_deg": 3.53287410736084,
  "theta_flat_bias_deg": 0.06038758158683777,
  "theta_flat_n": 509.0,
  "theta_near_flat_mae_deg": 0.37016600370407104,
  "theta_near_flat_abs_p95_deg": 1.6187011003494263,
  "theta_near_flat_abs_max_deg": 5.024937152862549,
  "theta_near_flat_bias_deg": 0.161727175116539,
  "theta_near_flat_n": 212.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.36342406272888184,
  "theta_flat_turn_abs_p95_deg": 1.457910180091858,
  "theta_flat_turn_abs_max_deg": 1.78815495967865,
  "theta_flat_turn_bias_deg": 0.1995709389448166,
  "theta_flat_turn_n": 94.0,
  "theta_slope_control_mae_deg": 0.31418588757514954,
  "theta_slope_control_abs_p95_deg": 9.306507110595703,
  "theta_slope_control_abs_max_deg": 10.032977104187012,
  "theta_slope_control_bias_deg": 0.018322482705116272,
  "theta_slope_control_n": 2560.0,
  "theta_all_mae_deg": 0.3141859173774719,
  "theta_all_rmse_deg": 0.4720006585121155,
  "theta_all_p95_abs_err_deg": 0.8034086227416992,
  "theta_all_max_abs_err_deg": 3.7567191123962402,
  "theta_all_bias_deg": 0.01832248643040657,
  "theta_all_n": 2560.0,
  "theta_active_abs_ge_2_mae_deg": 0.31721511483192444,
  "theta_active_abs_ge_2_rmse_deg": 0.46544647216796875,
  "theta_active_abs_ge_2_p95_abs_err_deg": 0.8066028356552124,
  "theta_active_abs_ge_2_max_abs_err_deg": 3.35833477973938,
  "theta_active_abs_ge_2_bias_deg": 0.007883122190833092,
  "theta_active_abs_ge_2_n": 2051.0,
  "theta_abs_le_8_mae_deg": 0.3015524446964264,
  "theta_abs_le_8_rmse_deg": 0.44939833879470825,
  "theta_abs_le_8_p95_abs_err_deg": 0.746525228023529,
  "theta_abs_le_8_max_abs_err_deg": 3.7567191123962402,
  "theta_abs_le_8_bias_deg": -0.02748243138194084,
  "theta_abs_le_8_n": 2031.0,
  "theta_abs_le_10_mae_deg": 0.3141859173774719,
  "theta_abs_le_10_rmse_deg": 0.4720006585121155,
  "theta_abs_le_10_p95_abs_err_deg": 0.8034086227416992,
  "theta_abs_le_10_max_abs_err_deg": 3.7567191123962402,
  "theta_abs_le_10_bias_deg": 0.01832248643040657,
  "theta_abs_le_10_n": 2560.0,
  "theta_pos_8_10_mae_deg": 0.2553237974643707,
  "theta_pos_8_10_rmse_deg": 0.43867045640945435,
  "theta_pos_8_10_p95_abs_err_deg": 0.9840602874755859,
  "theta_pos_8_10_max_abs_err_deg": 2.248305559158325,
  "theta_pos_8_10_bias_deg": -0.07890182733535767,
  "theta_pos_8_10_n": 251.0,
  "theta_neg_10_8_mae_deg": 0.4596279263496399,
  "theta_neg_10_8_rmse_deg": 0.6343005895614624,
  "theta_neg_10_8_p95_abs_err_deg": 1.3154855966567993,
  "theta_neg_10_8_max_abs_err_deg": 3.35833477973938,
  "theta_neg_10_8_bias_deg": 0.44074365496635437,
  "theta_neg_10_8_n": 278.0,
  "theta_pos_6_8_mae_deg": 0.3765736222267151,
  "theta_pos_6_8_rmse_deg": 0.46111705899238586,
  "theta_pos_6_8_p95_abs_err_deg": 0.8478718996047974,
  "theta_pos_6_8_max_abs_err_deg": 1.562595248222351,
  "theta_pos_6_8_bias_deg": -0.21271540224552155,
  "theta_pos_6_8_n": 241.0,
  "theta_neg_8_6_mae_deg": 0.31263551115989685,
  "theta_neg_8_6_rmse_deg": 0.5688657760620117,
  "theta_neg_8_6_p95_abs_err_deg": 0.9898325204849243,
  "theta_neg_8_6_max_abs_err_deg": 2.739124298095703,
  "theta_neg_8_6_bias_deg": 0.20982597768306732,
  "theta_neg_8_6_n": 251.0,
  "theta_neg_4_2_mae_deg": 0.2902955710887909,
  "theta_neg_4_2_rmse_deg": 0.37733468413352966,
  "theta_neg_4_2_p95_abs_err_deg": 0.7271885275840759,
  "theta_neg_4_2_max_abs_err_deg": 1.5402320623397827,
  "theta_neg_4_2_bias_deg": -0.16419903934001923,
  "theta_neg_4_2_n": 198.0,
  "theta_neg_2_0p5_mae_deg": 0.3907681405544281,
  "theta_neg_2_0p5_rmse_deg": 0.7094603180885315,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.2624589204788208,
  "theta_neg_2_0p5_max_abs_err_deg": 3.7567191123962402,
  "theta_neg_2_0p5_bias_deg": 0.16809554398059845,
  "theta_neg_2_0p5_n": 138.0,
  "theta_pos_0p5_2_mae_deg": 0.24921604990959167,
  "theta_pos_0p5_2_rmse_deg": 0.31613287329673767,
  "theta_pos_0p5_2_p95_abs_err_deg": 0.5442401766777039,
  "theta_pos_0p5_2_max_abs_err_deg": 1.760901689529419,
  "theta_pos_0p5_2_bias_deg": -0.03681114688515663,
  "theta_pos_0p5_2_n": 168.0
}
```
