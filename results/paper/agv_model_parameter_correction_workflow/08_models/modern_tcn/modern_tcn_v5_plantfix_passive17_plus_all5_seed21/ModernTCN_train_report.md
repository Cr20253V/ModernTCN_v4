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
| acc_main | 0.9725 |
| acc_turn | 0.5797 |
| acc_turn_pure | 0.6035 |
| acc_turn_transition | 0.4754 |
| main_confidence_mean | 0.9898 |
| main_low_conf_0p60_ratio | 0.0053 |
| main_low_conf_0p70_ratio | 0.0089 |
| turn_confidence_mean | 0.7759 |
| turn_low_conf_0p60_ratio | 0.2046 |
| turn_low_conf_0p70_ratio | 0.3615 |
| turn_right_recall | 0.5469 |
| turn_straight_recall | 0.6901 |
| turn_left_recall | 0.3644 |
| theta_mae_deg | 0.8188 |
| theta_abs_le_10_p95_abs_err_deg | 1.9814 |
| theta_neg_10_8_p95_abs_err_deg | 2.2440 |
| theta_pos_8_10_p95_abs_err_deg | 3.3465 |
| theta_abs_le_8_p95_abs_err_deg | 1.8818 |
| theta_neg_8_6_p95_abs_err_deg | 1.5294 |
| theta_pos_6_8_p95_abs_err_deg | 1.7766 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.4173 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.0057 |
| theta_flat_abs_p95_deg | 2.4166 |
| theta_flat_bias_deg | -0.4929 |
| theta_near_flat_abs_p95_deg | 1.6540 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.5785 |
| theta_flat_turn_abs_p95_deg | 1.5924 |
| flat_recall | 0.9577 |
| stall_recall | 0.6979 |
| slope_recall | 0.9862 |
| uphill_recall | 0.7683 |
| downhill_recall | 0.7968 |

- best_epoch: 56
- train_seconds: 744.6

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 19 | 0.4737 | 0.5469 |
| [0.60,0.70) | 13 | 0.3077 | 0.6496 |
| [0.70,0.80) | 34 | 0.0882 | 0.7643 |
| [0.80,0.90) | 36 | 0.2500 | 0.8589 |
| [0.90,1.00) | 3500 | 0.0211 | 0.9970 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 737 | 0.5699 | 0.5188 |
| [0.60,0.70) | 565 | 0.5115 | 0.6510 |
| [0.70,0.80) | 582 | 0.5550 | 0.7544 |
| [0.80,0.90) | 533 | 0.4034 | 0.8472 |
| [0.90,1.00) | 1185 | 0.2253 | 0.9740 |


## 验证集最佳点

```json
{
  "loss_total": 0.4032710266452036,
  "acc_main": 0.9399188092016239,
  "acc_turn": 0.6381596752368065,
  "acc_turn_pure": 0.6561783021960013,
  "acc_turn_transition": 0.5527950310559007,
  "flat_recall": 0.9056316590563166,
  "stall_recall": 0.42857142857142855,
  "slope_recall": 0.9546061415220294,
  "recall_main": [
    0.9056316590563166,
    0.42857142857142855,
    0.9546061415220294
  ],
  "turn_right_recall": 0.659952606635071,
  "turn_straight_recall": 0.6787941787941788,
  "turn_left_recall": 0.5339805825242718,
  "recall_turn": [
    0.659952606635071,
    0.6787941787941788,
    0.5339805825242718
  ],
  "cm_turn": [
    [
      557,
      252,
      35
    ],
    [
      357,
      1306,
      261
    ],
    [
      99,
      333,
      495
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      595,
      0,
      62
    ],
    [
      0,
      18,
      24
    ],
    [
      128,
      8,
      2860
    ]
  ],
  "main_confidence_mean": 0.9641729238570749,
  "main_confidence_error_mean": 0.7358640235034093,
  "main_low_conf_0p60_ratio": 0.05277401894451962,
  "main_low_conf_0p70_ratio": 0.060081190798376184,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 195,
      "error_rate": 0.47692307692307695,
      "mean_confidence": 0.49678459246227463
    },
    {
      "bin": "[0.60,0.70)",
      "n": 27,
      "error_rate": 0.4074074074074074,
      "mean_confidence": 0.6478493792111507
    },
    {
      "bin": "[0.70,0.80)",
      "n": 33,
      "error_rate": 0.5454545454545454,
      "mean_confidence": 0.752856258128487
    },
    {
      "bin": "[0.80,0.90)",
      "n": 60,
      "error_rate": 0.2833333333333333,
      "mean_confidence": 0.8563894076725678
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3380,
      "error_rate": 0.024556213017751478,
      "mean_confidence": 0.9976409479007258
    }
  ],
  "turn_confidence_mean": 0.7785870410779379,
  "turn_confidence_error_mean": 0.7053958373354072,
  "turn_low_conf_0p60_ratio": 0.23518267929634643,
  "turn_low_conf_0p70_ratio": 0.36265223274695535,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 869,
      "error_rate": 0.5684695051783659,
      "mean_confidence": 0.5260181148412221
    },
    {
      "bin": "[0.60,0.70)",
      "n": 471,
      "error_rate": 0.445859872611465,
      "mean_confidence": 0.6505363825217433
    },
    {
      "bin": "[0.70,0.80)",
      "n": 493,
      "error_rate": 0.4198782961460446,
      "mean_confidence": 0.7514595170486782
    },
    {
      "bin": "[0.80,0.90)",
      "n": 561,
      "error_rate": 0.30303030303030304,
      "mean_confidence": 0.8519239545665449
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1301,
      "error_rate": 0.196771714066103,
      "mean_confidence": 0.9723042724069083
    }
  ],
  "theta_mae_rad": 0.01678873412311077,
  "theta_mae_deg": 0.9619235396385193,
  "uphill_recall": 0.7827493261455526,
  "downhill_recall": 0.8175750834260289,
  "slope_sign_acc": 0.9649603065973172,
  "theta_flat_mae_deg": 1.2020738124847412,
  "theta_flat_abs_p95_deg": 3.9952831268310547,
  "theta_flat_abs_max_deg": 6.7112812995910645,
  "theta_flat_bias_deg": 0.20333993434906006,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.6061981916427612,
  "theta_near_flat_abs_p95_deg": 3.9957072734832764,
  "theta_near_flat_abs_max_deg": 6.7112812995910645,
  "theta_near_flat_bias_deg": 0.7151650190353394,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.3463592529296875,
  "theta_flat_turn_abs_p95_deg": 3.9952831268310547,
  "theta_flat_turn_abs_max_deg": 6.7112812995910645,
  "theta_flat_turn_bias_deg": 0.3338911831378937,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9619235396385193,
  "theta_slope_control_abs_p95_deg": 8.643356323242188,
  "theta_slope_control_abs_max_deg": 11.322677612304688,
  "theta_slope_control_bias_deg": -0.1041925922036171,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.9619235396385193,
  "theta_all_rmse_deg": 1.3139636516571045,
  "theta_all_p95_abs_err_deg": 2.699528932571411,
  "theta_all_max_abs_err_deg": 8.383753776550293,
  "theta_all_bias_deg": -0.10419259965419769,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.9092604517936707,
  "theta_active_abs_ge_2_rmse_deg": 1.2101249694824219,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.4501686096191406,
  "theta_active_abs_ge_2_max_abs_err_deg": 8.383753776550293,
  "theta_active_abs_ge_2_bias_deg": -0.17163214087486267,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9729928970336914,
  "theta_abs_le_8_rmse_deg": 1.3403853178024292,
  "theta_abs_le_8_p95_abs_err_deg": 3.0209436416625977,
  "theta_abs_le_8_max_abs_err_deg": 8.383753776550293,
  "theta_abs_le_8_bias_deg": -0.09415663778781891,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.9619235396385193,
  "theta_abs_le_10_rmse_deg": 1.3139636516571045,
  "theta_abs_le_10_p95_abs_err_deg": 2.699528932571411,
  "theta_abs_le_10_max_abs_err_deg": 8.383753776550293,
  "theta_abs_le_10_bias_deg": -0.10419259965419769,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 1.0495587587356567,
  "theta_pos_8_10_rmse_deg": 1.1966370344161987,
  "theta_pos_8_10_p95_abs_err_deg": 2.016894817352295,
  "theta_pos_8_10_max_abs_err_deg": 5.09970235824585,
  "theta_pos_8_10_bias_deg": -0.9178518652915955,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7785724401473999,
  "theta_neg_10_8_rmse_deg": 1.1955422163009644,
  "theta_neg_10_8_p95_abs_err_deg": 1.8198825120925903,
  "theta_neg_10_8_max_abs_err_deg": 7.8586812019348145,
  "theta_neg_10_8_bias_deg": 0.6381288170814514,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 1.0208910703659058,
  "theta_pos_6_8_rmse_deg": 1.2283209562301636,
  "theta_pos_6_8_p95_abs_err_deg": 2.437110662460327,
  "theta_pos_6_8_max_abs_err_deg": 3.063568115234375,
  "theta_pos_6_8_bias_deg": -0.7860056161880493,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7190335392951965,
  "theta_neg_8_6_rmse_deg": 1.0508434772491455,
  "theta_neg_8_6_p95_abs_err_deg": 2.001660108566284,
  "theta_neg_8_6_max_abs_err_deg": 8.383753776550293,
  "theta_neg_8_6_bias_deg": 0.11357329785823822,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7409397959709167,
  "theta_neg_4_2_rmse_deg": 0.99310302734375,
  "theta_neg_4_2_p95_abs_err_deg": 1.8241509199142456,
  "theta_neg_4_2_max_abs_err_deg": 5.515902519226074,
  "theta_neg_4_2_bias_deg": -0.1781451404094696,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6223610639572144,
  "theta_neg_2_0p5_rmse_deg": 0.8000333905220032,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.2084192037582397,
  "theta_neg_2_0p5_max_abs_err_deg": 4.672632694244385,
  "theta_neg_2_0p5_bias_deg": -0.46161869168281555,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.2429301738739014,
  "theta_pos_0p5_2_rmse_deg": 1.539169430732727,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.4952831268310547,
  "theta_pos_0p5_2_max_abs_err_deg": 4.3307294845581055,
  "theta_pos_0p5_2_bias_deg": 0.20000909268856049,
  "theta_pos_0p5_2_n": 163.0
}
```
