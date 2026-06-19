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
  "lambda_turn": 0.16,
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
  "turn_transition_weight": 2.0,
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
| acc_main | 0.9703 |
| acc_turn | 0.5641 |
| acc_turn_pure | 0.5831 |
| acc_turn_transition | 0.4814 |
| main_confidence_mean | 0.9871 |
| main_low_conf_0p60_ratio | 0.0075 |
| main_low_conf_0p70_ratio | 0.0172 |
| turn_confidence_mean | 0.8162 |
| turn_low_conf_0p60_ratio | 0.1641 |
| turn_low_conf_0p70_ratio | 0.2660 |
| turn_right_recall | 0.6558 |
| turn_straight_recall | 0.5085 |
| turn_left_recall | 0.6034 |
| theta_mae_deg | 0.6861 |
| theta_abs_le_10_p95_abs_err_deg | 1.8277 |
| theta_neg_10_8_p95_abs_err_deg | 1.3821 |
| theta_pos_8_10_p95_abs_err_deg | 2.7611 |
| theta_abs_le_8_p95_abs_err_deg | 1.7491 |
| theta_neg_8_6_p95_abs_err_deg | 1.7015 |
| theta_pos_6_8_p95_abs_err_deg | 1.5804 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.4546 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4937 |
| theta_flat_abs_p95_deg | 2.5691 |
| theta_flat_bias_deg | 0.2038 |
| theta_near_flat_abs_p95_deg | 1.8420 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.2684 |
| theta_flat_turn_abs_p95_deg | 1.6709 |
| flat_recall | 0.9669 |
| stall_recall | 0.7188 |
| slope_recall | 0.9800 |
| uphill_recall | 0.7615 |
| downhill_recall | 0.7894 |

- best_epoch: 60
- train_seconds: 288.5

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 27 | 0.4815 | 0.5415 |
| [0.60,0.70) | 35 | 0.3714 | 0.6576 |
| [0.70,0.80) | 34 | 0.2059 | 0.7495 |
| [0.80,0.90) | 36 | 0.2500 | 0.8578 |
| [0.90,1.00) | 3470 | 0.0187 | 0.9976 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 591 | 0.5821 | 0.5227 |
| [0.60,0.70) | 367 | 0.6022 | 0.6501 |
| [0.70,0.80) | 491 | 0.5193 | 0.7494 |
| [0.80,0.90) | 551 | 0.4973 | 0.8514 |
| [0.90,1.00) | 1602 | 0.2971 | 0.9710 |


## 验证集最佳点

```json
{
  "loss_total": 0.590334100297404,
  "acc_main": 0.9450608930987822,
  "acc_turn": 0.6029769959404601,
  "acc_turn_pure": 0.6201245493280891,
  "acc_turn_transition": 0.5217391304347826,
  "flat_recall": 0.9634703196347032,
  "stall_recall": 0.5238095238095238,
  "slope_recall": 0.9469292389853138,
  "recall_main": [
    0.9634703196347032,
    0.5238095238095238,
    0.9469292389853138
  ],
  "turn_right_recall": 0.659952606635071,
  "turn_straight_recall": 0.5166320166320166,
  "turn_left_recall": 0.7303128371089536,
  "recall_turn": [
    0.659952606635071,
    0.5166320166320166,
    0.7303128371089536
  ],
  "cm_turn": [
    [
      557,
      189,
      98
    ],
    [
      439,
      994,
      491
    ],
    [
      105,
      145,
      677
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      633,
      0,
      24
    ],
    [
      0,
      22,
      20
    ],
    [
      143,
      16,
      2837
    ]
  ],
  "main_confidence_mean": 0.9649131031039279,
  "main_confidence_error_mean": 0.7403285550214629,
  "main_low_conf_0p60_ratio": 0.05250338294993234,
  "main_low_conf_0p70_ratio": 0.059810554803788905,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 194,
      "error_rate": 0.4639175257731959,
      "mean_confidence": 0.49739788671091134
    },
    {
      "bin": "[0.60,0.70)",
      "n": 27,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.6457490162054831
    },
    {
      "bin": "[0.70,0.80)",
      "n": 25,
      "error_rate": 0.4,
      "mean_confidence": 0.7550124035672771
    },
    {
      "bin": "[0.80,0.90)",
      "n": 47,
      "error_rate": 0.1702127659574468,
      "mean_confidence": 0.8553208852599761
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3402,
      "error_rate": 0.025279247501469725,
      "mean_confidence": 0.9971628779580092
    }
  ],
  "turn_confidence_mean": 0.8304131793944165,
  "turn_confidence_error_mean": 0.7560703601652952,
  "turn_low_conf_0p60_ratio": 0.1645466847090663,
  "turn_low_conf_0p70_ratio": 0.24519621109607578,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 608,
      "error_rate": 0.6611842105263158,
      "mean_confidence": 0.4946854337660344
    },
    {
      "bin": "[0.60,0.70)",
      "n": 298,
      "error_rate": 0.5436241610738255,
      "mean_confidence": 0.6536418903470848
    },
    {
      "bin": "[0.70,0.80)",
      "n": 416,
      "error_rate": 0.4639423076923077,
      "mean_confidence": 0.7486631827879026
    },
    {
      "bin": "[0.80,0.90)",
      "n": 450,
      "error_rate": 0.4688888888888889,
      "mean_confidence": 0.8555501281138302
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1923,
      "error_rate": 0.2594903796151846,
      "mean_confidence": 0.9757572694322404
    }
  ],
  "theta_mae_rad": 0.014060629531741142,
  "theta_mae_deg": 0.805614709854126,
  "uphill_recall": 0.7714285714285715,
  "downhill_recall": 0.7953281423804227,
  "slope_sign_acc": 0.9698877634820695,
  "theta_flat_mae_deg": 1.0358912944793701,
  "theta_flat_abs_p95_deg": 3.294753313064575,
  "theta_flat_abs_max_deg": 8.508977890014648,
  "theta_flat_bias_deg": 0.6131241917610168,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.303661823272705,
  "theta_near_flat_abs_p95_deg": 3.5301005840301514,
  "theta_near_flat_abs_max_deg": 8.508977890014648,
  "theta_near_flat_bias_deg": 0.7611299157142639,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.0512539148330688,
  "theta_flat_turn_abs_p95_deg": 4.000064373016357,
  "theta_flat_turn_abs_max_deg": 8.508977890014648,
  "theta_flat_turn_bias_deg": 0.1018536388874054,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.805614709854126,
  "theta_slope_control_abs_p95_deg": 9.407488822937012,
  "theta_slope_control_abs_max_deg": 12.853983879089355,
  "theta_slope_control_bias_deg": 0.07744445651769638,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8056145906448364,
  "theta_all_rmse_deg": 1.1758440732955933,
  "theta_all_p95_abs_err_deg": 2.713125228881836,
  "theta_all_max_abs_err_deg": 8.008978843688965,
  "theta_all_bias_deg": 0.07744445651769638,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7551167011260986,
  "theta_active_abs_ge_2_rmse_deg": 1.0993865728378296,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2553746700286865,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.845739364624023,
  "theta_active_abs_ge_2_bias_deg": -0.04002602770924568,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8242383599281311,
  "theta_abs_le_8_rmse_deg": 1.2024898529052734,
  "theta_abs_le_8_p95_abs_err_deg": 2.7947194576263428,
  "theta_abs_le_8_max_abs_err_deg": 8.008978843688965,
  "theta_abs_le_8_bias_deg": 0.14052774012088776,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8056145906448364,
  "theta_abs_le_10_rmse_deg": 1.1758440732955933,
  "theta_abs_le_10_p95_abs_err_deg": 2.713125228881836,
  "theta_abs_le_10_max_abs_err_deg": 8.008978843688965,
  "theta_abs_le_10_bias_deg": 0.07744445651769638,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6332728862762451,
  "theta_pos_8_10_rmse_deg": 0.815750002861023,
  "theta_pos_8_10_p95_abs_err_deg": 1.4882467985153198,
  "theta_pos_8_10_max_abs_err_deg": 4.303191184997559,
  "theta_pos_8_10_bias_deg": -0.2862943410873413,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8224472999572754,
  "theta_neg_10_8_rmse_deg": 1.254138469696045,
  "theta_neg_10_8_p95_abs_err_deg": 2.4157731533050537,
  "theta_neg_10_8_max_abs_err_deg": 6.845739364624023,
  "theta_neg_10_8_bias_deg": -0.08937155455350876,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5860822200775146,
  "theta_pos_6_8_rmse_deg": 0.7992956042289734,
  "theta_pos_6_8_p95_abs_err_deg": 1.516777515411377,
  "theta_pos_6_8_max_abs_err_deg": 3.2905373573303223,
  "theta_pos_6_8_bias_deg": -0.09947653859853745,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8621832728385925,
  "theta_neg_8_6_rmse_deg": 1.2223032712936401,
  "theta_neg_8_6_p95_abs_err_deg": 2.3802950382232666,
  "theta_neg_8_6_max_abs_err_deg": 5.824952125549316,
  "theta_neg_8_6_bias_deg": -0.16177982091903687,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8224573731422424,
  "theta_neg_4_2_rmse_deg": 1.1104625463485718,
  "theta_neg_4_2_p95_abs_err_deg": 2.3644607067108154,
  "theta_neg_4_2_max_abs_err_deg": 4.686128616333008,
  "theta_neg_4_2_bias_deg": 0.2604222595691681,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.7132777571678162,
  "theta_neg_2_0p5_rmse_deg": 0.9185229539871216,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.8110778331756592,
  "theta_neg_2_0p5_max_abs_err_deg": 4.088472843170166,
  "theta_neg_2_0p5_bias_deg": 0.3032975196838379,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1369373798370361,
  "theta_pos_0p5_2_rmse_deg": 1.324016809463501,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.7947194576263428,
  "theta_pos_0p5_2_max_abs_err_deg": 4.032978534698486,
  "theta_pos_0p5_2_bias_deg": 0.9682638049125671,
  "theta_pos_0p5_2_n": 163.0
}
```
