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
| acc_main | 0.9788 |
| acc_turn | 0.8722 |
| acc_turn_pure | 0.8990 |
| acc_turn_transition | 0.7121 |
| main_confidence_mean | 0.9940 |
| main_low_conf_0p60_ratio | 0.0021 |
| main_low_conf_0p70_ratio | 0.0035 |
| turn_confidence_mean | 0.9202 |
| turn_low_conf_0p60_ratio | 0.0469 |
| turn_low_conf_0p70_ratio | 0.0954 |
| turn_right_recall | 0.8290 |
| turn_straight_recall | 0.8894 |
| turn_left_recall | 0.8689 |
| theta_mae_deg | 0.3428 |
| theta_abs_le_10_p95_abs_err_deg | 0.9799 |
| theta_neg_10_8_p95_abs_err_deg | 1.2814 |
| theta_pos_8_10_p95_abs_err_deg | 1.1387 |
| theta_abs_le_8_p95_abs_err_deg | 0.9456 |
| theta_neg_8_6_p95_abs_err_deg | 1.0433 |
| theta_pos_6_8_p95_abs_err_deg | 0.6205 |
| theta_neg_2_0p5_p95_abs_err_deg | 0.8190 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.6898 |
| theta_flat_abs_p95_deg | 2.2195 |
| theta_flat_bias_deg | 0.0037 |
| theta_near_flat_abs_p95_deg | 1.2243 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.1194 |
| theta_flat_turn_abs_p95_deg | 1.1047 |
| flat_recall | 0.9683 |
| stall_recall | 0.7009 |
| slope_recall | 0.9930 |
| uphill_recall | 0.8043 |
| downhill_recall | 0.7799 |

- best_epoch: 68
- train_seconds: 333.8

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 8 | 0.6250 | 0.5286 |
| [0.60,0.70) | 5 | 0.4000 | 0.6643 |
| [0.70,0.80) | 20 | 0.2000 | 0.7543 |
| [0.80,0.90) | 39 | 0.2051 | 0.8552 |
| [0.90,1.00) | 3661 | 0.0164 | 0.9982 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 175 | 0.5314 | 0.5410 |
| [0.60,0.70) | 181 | 0.3646 | 0.6496 |
| [0.70,0.80) | 207 | 0.2802 | 0.7530 |
| [0.80,0.90) | 369 | 0.1762 | 0.8553 |
| [0.90,1.00) | 2801 | 0.0696 | 0.9823 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.7121

## 验证集最佳点

```json
{
  "loss_total": 0.24954726615021133,
  "acc_main": 0.9677790563866513,
  "acc_turn": 0.797084771768316,
  "acc_turn_pure": 0.8317329675354367,
  "acc_turn_transition": 0.6166666666666667,
  "flat_recall": 0.9508840864440079,
  "stall_recall": 0.8936170212765957,
  "slope_recall": 0.9736713798147245,
  "recall_main": [
    0.9508840864440079,
    0.8936170212765957,
    0.9736713798147245
  ],
  "turn_right_recall": 0.75,
  "turn_straight_recall": 0.8280766852195424,
  "turn_left_recall": 0.7432950191570882,
  "recall_turn": [
    0.75,
    0.8280766852195424,
    0.7432950191570882
  ],
  "cm_turn": [
    [
      351,
      95,
      22
    ],
    [
      132,
      1339,
      146
    ],
    [
      17,
      117,
      388
    ]
  ],
  "n_turn_transition": 420,
  "n_turn_pure": 2187,
  "cm_main": [
    [
      484,
      0,
      25
    ],
    [
      5,
      42,
      0
    ],
    [
      46,
      8,
      1997
    ]
  ],
  "main_confidence_mean": 0.9906062780575922,
  "main_confidence_error_mean": 0.8630851725979175,
  "main_low_conf_0p60_ratio": 0.005753739930955121,
  "main_low_conf_0p70_ratio": 0.010356731875719217,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 15,
      "error_rate": 0.8666666666666667,
      "mean_confidence": 0.5542546704691358
    },
    {
      "bin": "[0.60,0.70)",
      "n": 12,
      "error_rate": 0.5,
      "mean_confidence": 0.647065805772057
    },
    {
      "bin": "[0.70,0.80)",
      "n": 17,
      "error_rate": 0.35294117647058826,
      "mean_confidence": 0.7556469489885904
    },
    {
      "bin": "[0.80,0.90)",
      "n": 31,
      "error_rate": 0.25806451612903225,
      "mean_confidence": 0.8420792821900183
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2532,
      "error_rate": 0.02014218009478673,
      "mean_confidence": 0.9982154428472134
    }
  ],
  "turn_confidence_mean": 0.9032157786343795,
  "turn_confidence_error_mean": 0.8118083033451412,
  "turn_low_conf_0p60_ratio": 0.06904487917146145,
  "turn_low_conf_0p70_ratio": 0.12811660912926737,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 180,
      "error_rate": 0.5166666666666667,
      "mean_confidence": 0.5362703432351361
    },
    {
      "bin": "[0.60,0.70)",
      "n": 154,
      "error_rate": 0.43506493506493504,
      "mean_confidence": 0.6460351316556693
    },
    {
      "bin": "[0.70,0.80)",
      "n": 170,
      "error_rate": 0.34705882352941175,
      "mean_confidence": 0.7530298231342011
    },
    {
      "bin": "[0.80,0.90)",
      "n": 291,
      "error_rate": 0.27835051546391754,
      "mean_confidence": 0.8559520116222553
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1812,
      "error_rate": 0.12637969094922738,
      "mean_confidence": 0.9832054953243042
    }
  ],
  "theta_mae_rad": 0.0060023358091712,
  "theta_mae_deg": 0.34390848875045776,
  "uphill_recall": 0.7729357798165137,
  "downhill_recall": 0.8075079872204473,
  "slope_sign_acc": 0.982421875,
  "theta_flat_mae_deg": 0.33968016505241394,
  "theta_flat_abs_p95_deg": 1.8889790773391724,
  "theta_flat_abs_max_deg": 2.781822443008423,
  "theta_flat_bias_deg": -0.0252897497266531,
  "theta_flat_n": 509.0,
  "theta_near_flat_mae_deg": 0.41151365637779236,
  "theta_near_flat_abs_p95_deg": 1.6339207887649536,
  "theta_near_flat_abs_max_deg": 5.531010150909424,
  "theta_near_flat_bias_deg": 0.18389490246772766,
  "theta_near_flat_n": 212.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.32753056287765503,
  "theta_flat_turn_abs_p95_deg": 1.121042013168335,
  "theta_flat_turn_abs_max_deg": 2.0087239742279053,
  "theta_flat_turn_bias_deg": 0.2510872781276703,
  "theta_flat_turn_n": 94.0,
  "theta_slope_control_mae_deg": 0.34390848875045776,
  "theta_slope_control_abs_p95_deg": 9.385300636291504,
  "theta_slope_control_abs_max_deg": 10.825706481933594,
  "theta_slope_control_bias_deg": -0.14112038910388947,
  "theta_slope_control_n": 2560.0,
  "theta_all_mae_deg": 0.34390848875045776,
  "theta_all_rmse_deg": 0.5007795691490173,
  "theta_all_p95_abs_err_deg": 0.9563126564025879,
  "theta_all_max_abs_err_deg": 3.6818222999572754,
  "theta_all_bias_deg": -0.14112038910388947,
  "theta_all_n": 2560.0,
  "theta_active_abs_ge_2_mae_deg": 0.3449578285217285,
  "theta_active_abs_ge_2_rmse_deg": 0.49524858593940735,
  "theta_active_abs_ge_2_p95_abs_err_deg": 0.9923155307769775,
  "theta_active_abs_ge_2_max_abs_err_deg": 3.4602112770080566,
  "theta_active_abs_ge_2_bias_deg": -0.16986624896526337,
  "theta_active_abs_ge_2_n": 2051.0,
  "theta_abs_le_8_mae_deg": 0.34328585863113403,
  "theta_abs_le_8_rmse_deg": 0.49243995547294617,
  "theta_abs_le_8_p95_abs_err_deg": 0.9497776627540588,
  "theta_abs_le_8_max_abs_err_deg": 3.6818222999572754,
  "theta_abs_le_8_bias_deg": -0.12224490940570831,
  "theta_abs_le_8_n": 2031.0,
  "theta_abs_le_10_mae_deg": 0.34390848875045776,
  "theta_abs_le_10_rmse_deg": 0.5007795691490173,
  "theta_abs_le_10_p95_abs_err_deg": 0.9563126564025879,
  "theta_abs_le_10_max_abs_err_deg": 3.6818222999572754,
  "theta_abs_le_10_bias_deg": -0.14112038910388947,
  "theta_abs_le_10_n": 2560.0,
  "theta_pos_8_10_mae_deg": 0.3796064257621765,
  "theta_pos_8_10_rmse_deg": 0.5471282601356506,
  "theta_pos_8_10_p95_abs_err_deg": 0.8948879241943359,
  "theta_pos_8_10_max_abs_err_deg": 2.1112966537475586,
  "theta_pos_8_10_bias_deg": -0.31978967785835266,
  "theta_pos_8_10_n": 251.0,
  "theta_neg_10_8_mae_deg": 0.3162263333797455,
  "theta_neg_10_8_rmse_deg": 0.5171478390693665,
  "theta_neg_10_8_p95_abs_err_deg": 1.01839017868042,
  "theta_neg_10_8_max_abs_err_deg": 3.009058952331543,
  "theta_neg_10_8_bias_deg": -0.11770349740982056,
  "theta_neg_10_8_n": 278.0,
  "theta_pos_6_8_mae_deg": 0.4912993311882019,
  "theta_pos_6_8_rmse_deg": 0.6592191457748413,
  "theta_pos_6_8_p95_abs_err_deg": 1.288263201713562,
  "theta_pos_6_8_max_abs_err_deg": 2.618666172027588,
  "theta_pos_6_8_bias_deg": -0.4547215700149536,
  "theta_pos_6_8_n": 241.0,
  "theta_neg_8_6_mae_deg": 0.2774369716644287,
  "theta_neg_8_6_rmse_deg": 0.4474465250968933,
  "theta_neg_8_6_p95_abs_err_deg": 0.7255009412765503,
  "theta_neg_8_6_max_abs_err_deg": 2.062023639678955,
  "theta_neg_8_6_bias_deg": 0.09422130137681961,
  "theta_neg_8_6_n": 251.0,
  "theta_neg_4_2_mae_deg": 0.30859753489494324,
  "theta_neg_4_2_rmse_deg": 0.37153470516204834,
  "theta_neg_4_2_p95_abs_err_deg": 0.6510926485061646,
  "theta_neg_4_2_max_abs_err_deg": 1.043554425239563,
  "theta_neg_4_2_bias_deg": -0.045336637645959854,
  "theta_neg_4_2_n": 198.0,
  "theta_neg_2_0p5_mae_deg": 0.40369072556495667,
  "theta_neg_2_0p5_rmse_deg": 0.7017276883125305,
  "theta_neg_2_0p5_p95_abs_err_deg": 0.9797415137290955,
  "theta_neg_2_0p5_max_abs_err_deg": 3.6818222999572754,
  "theta_neg_2_0p5_bias_deg": 0.0903892070055008,
  "theta_neg_2_0p5_n": 138.0,
  "theta_pos_0p5_2_mae_deg": 0.32668808102607727,
  "theta_pos_0p5_2_rmse_deg": 0.4065806269645691,
  "theta_pos_0p5_2_p95_abs_err_deg": 0.6791327595710754,
  "theta_pos_0p5_2_max_abs_err_deg": 1.3326010704040527,
  "theta_pos_0p5_2_bias_deg": -0.23449593782424927,
  "theta_pos_0p5_2_n": 168.0
}
```
