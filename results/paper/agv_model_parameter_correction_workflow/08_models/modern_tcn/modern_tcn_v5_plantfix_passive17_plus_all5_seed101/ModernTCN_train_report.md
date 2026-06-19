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
| acc_main | 0.9611 |
| acc_turn | 0.5747 |
| acc_turn_pure | 0.5991 |
| acc_turn_transition | 0.4680 |
| main_confidence_mean | 0.9895 |
| main_low_conf_0p60_ratio | 0.0042 |
| main_low_conf_0p70_ratio | 0.0133 |
| turn_confidence_mean | 0.7858 |
| turn_low_conf_0p60_ratio | 0.2041 |
| turn_low_conf_0p70_ratio | 0.3506 |
| turn_right_recall | 0.5532 |
| turn_straight_recall | 0.6068 |
| turn_left_recall | 0.5230 |
| theta_mae_deg | 0.6480 |
| theta_abs_le_10_p95_abs_err_deg | 1.6000 |
| theta_neg_10_8_p95_abs_err_deg | 1.3151 |
| theta_pos_8_10_p95_abs_err_deg | 2.5562 |
| theta_abs_le_8_p95_abs_err_deg | 1.5156 |
| theta_neg_8_6_p95_abs_err_deg | 1.2727 |
| theta_pos_6_8_p95_abs_err_deg | 1.7631 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.3414 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5146 |
| theta_flat_abs_p95_deg | 2.5134 |
| theta_flat_bias_deg | -0.1435 |
| theta_near_flat_abs_p95_deg | 2.0173 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.3951 |
| theta_flat_turn_abs_p95_deg | 2.0300 |
| flat_recall | 0.9272 |
| stall_recall | 0.6979 |
| slope_recall | 0.9796 |
| uphill_recall | 0.7569 |
| downhill_recall | 0.8110 |

- best_epoch: 74
- train_seconds: 973.5

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 15 | 0.6667 | 0.5590 |
| [0.60,0.70) | 33 | 0.2121 | 0.6511 |
| [0.70,0.80) | 28 | 0.3571 | 0.7539 |
| [0.80,0.90) | 33 | 0.3030 | 0.8544 |
| [0.90,1.00) | 3493 | 0.0295 | 0.9977 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 735 | 0.6286 | 0.5191 |
| [0.60,0.70) | 528 | 0.5833 | 0.6496 |
| [0.70,0.80) | 456 | 0.4649 | 0.7502 |
| [0.80,0.90) | 492 | 0.3923 | 0.8529 |
| [0.90,1.00) | 1391 | 0.2566 | 0.9664 |


## 验证集最佳点

```json
{
  "loss_total": 0.3740808241825465,
  "acc_main": 0.9483085250338295,
  "acc_turn": 0.6167794316644114,
  "acc_turn_pure": 0.6293018682399213,
  "acc_turn_transition": 0.5574534161490683,
  "flat_recall": 0.9467275494672754,
  "stall_recall": 0.5476190476190477,
  "slope_recall": 0.9542723631508678,
  "recall_main": [
    0.9467275494672754,
    0.5476190476190477,
    0.9542723631508678
  ],
  "turn_right_recall": 0.5971563981042654,
  "turn_straight_recall": 0.5873180873180873,
  "turn_left_recall": 0.6957928802588996,
  "recall_turn": [
    0.5971563981042654,
    0.5873180873180873,
    0.6957928802588996
  ],
  "cm_turn": [
    [
      504,
      229,
      111
    ],
    [
      308,
      1130,
      486
    ],
    [
      67,
      215,
      645
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      622,
      0,
      35
    ],
    [
      0,
      23,
      19
    ],
    [
      126,
      11,
      2859
    ]
  ],
  "main_confidence_mean": 0.9705070624728298,
  "main_confidence_error_mean": 0.7387994193947469,
  "main_low_conf_0p60_ratio": 0.050608930987821384,
  "main_low_conf_0p70_ratio": 0.056562922868741546,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 187,
      "error_rate": 0.47058823529411764,
      "mean_confidence": 0.5567664130346393
    },
    {
      "bin": "[0.60,0.70)",
      "n": 22,
      "error_rate": 0.5909090909090909,
      "mean_confidence": 0.6448207872796177
    },
    {
      "bin": "[0.70,0.80)",
      "n": 29,
      "error_rate": 0.4482758620689655,
      "mean_confidence": 0.7504560604642659
    },
    {
      "bin": "[0.80,0.90)",
      "n": 38,
      "error_rate": 0.3684210526315789,
      "mean_confidence": 0.8483341070077629
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3419,
      "error_rate": 0.01842644047967242,
      "mean_confidence": 0.9984563607662236
    }
  ],
  "turn_confidence_mean": 0.820115612806938,
  "turn_confidence_error_mean": 0.7524689989199628,
  "turn_low_conf_0p60_ratio": 0.1699594046008119,
  "turn_low_conf_0p70_ratio": 0.2752368064952639,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 628,
      "error_rate": 0.6146496815286624,
      "mean_confidence": 0.5367342021249593
    },
    {
      "bin": "[0.60,0.70)",
      "n": 389,
      "error_rate": 0.4961439588688946,
      "mean_confidence": 0.6499698835773192
    },
    {
      "bin": "[0.70,0.80)",
      "n": 451,
      "error_rate": 0.5277161862527716,
      "mean_confidence": 0.7542924759301944
    },
    {
      "bin": "[0.80,0.90)",
      "n": 531,
      "error_rate": 0.4331450094161959,
      "mean_confidence": 0.8530119202645499
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1696,
      "error_rate": 0.21757075471698112,
      "mean_confidence": 0.9712762909024713
    }
  ],
  "theta_mae_rad": 0.015061193145811558,
  "theta_mae_deg": 0.8629427552223206,
  "uphill_recall": 0.7773584905660378,
  "downhill_recall": 0.8075639599555061,
  "slope_sign_acc": 0.976731453599781,
  "theta_flat_mae_deg": 1.232059121131897,
  "theta_flat_abs_p95_deg": 4.20255184173584,
  "theta_flat_abs_max_deg": 9.401199340820312,
  "theta_flat_bias_deg": 0.42794349789619446,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5562294721603394,
  "theta_near_flat_abs_p95_deg": 4.255307674407959,
  "theta_near_flat_abs_max_deg": 9.401199340820312,
  "theta_near_flat_bias_deg": 0.8005932569503784,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.2242069244384766,
  "theta_flat_turn_abs_p95_deg": 4.20255184173584,
  "theta_flat_turn_abs_max_deg": 9.401199340820312,
  "theta_flat_turn_bias_deg": 0.22659364342689514,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8629427552223206,
  "theta_slope_control_abs_p95_deg": 9.16348934173584,
  "theta_slope_control_abs_max_deg": 13.3445463180542,
  "theta_slope_control_bias_deg": -0.11720453202724457,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8629426956176758,
  "theta_all_rmse_deg": 1.2437256574630737,
  "theta_all_p95_abs_err_deg": 2.702552080154419,
  "theta_all_max_abs_err_deg": 8.901199340820312,
  "theta_all_bias_deg": -0.11720453202724457,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.781998336315155,
  "theta_active_abs_ge_2_rmse_deg": 1.0748465061187744,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.0938830375671387,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.561563968658447,
  "theta_active_abs_ge_2_bias_deg": -0.23675137758255005,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.871748685836792,
  "theta_abs_le_8_rmse_deg": 1.2626765966415405,
  "theta_abs_le_8_p95_abs_err_deg": 2.702552080154419,
  "theta_abs_le_8_max_abs_err_deg": 8.901199340820312,
  "theta_abs_le_8_bias_deg": -0.05391141399741173,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8629426956176758,
  "theta_abs_le_10_rmse_deg": 1.2437256574630737,
  "theta_abs_le_10_p95_abs_err_deg": 2.702552080154419,
  "theta_abs_le_10_max_abs_err_deg": 8.901199340820312,
  "theta_abs_le_10_bias_deg": -0.11720453202724457,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.9218613505363464,
  "theta_pos_8_10_rmse_deg": 1.0743539333343506,
  "theta_pos_8_10_p95_abs_err_deg": 1.8039445877075195,
  "theta_pos_8_10_max_abs_err_deg": 5.447071552276611,
  "theta_pos_8_10_bias_deg": -0.7696199417114258,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7280654311180115,
  "theta_neg_10_8_rmse_deg": 1.2417892217636108,
  "theta_neg_10_8_p95_abs_err_deg": 2.428642511367798,
  "theta_neg_10_8_max_abs_err_deg": 6.561563968658447,
  "theta_neg_10_8_bias_deg": 0.007861822843551636,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.7560844421386719,
  "theta_pos_6_8_rmse_deg": 0.9144136309623718,
  "theta_pos_6_8_p95_abs_err_deg": 1.7930041551589966,
  "theta_pos_6_8_max_abs_err_deg": 2.8861398696899414,
  "theta_pos_6_8_bias_deg": -0.5131832957267761,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.747940719127655,
  "theta_neg_8_6_rmse_deg": 1.0976479053497314,
  "theta_neg_8_6_p95_abs_err_deg": 2.2635302543640137,
  "theta_neg_8_6_max_abs_err_deg": 5.902707576751709,
  "theta_neg_8_6_bias_deg": -0.1789785921573639,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6835651397705078,
  "theta_neg_4_2_rmse_deg": 0.9354538917541504,
  "theta_neg_4_2_p95_abs_err_deg": 2.0261142253875732,
  "theta_neg_4_2_max_abs_err_deg": 4.674816608428955,
  "theta_neg_4_2_bias_deg": -0.20475052297115326,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.7029708027839661,
  "theta_neg_2_0p5_rmse_deg": 0.9965332746505737,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.139563798904419,
  "theta_neg_2_0p5_max_abs_err_deg": 4.418600559234619,
  "theta_neg_2_0p5_bias_deg": -0.26091307401657104,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.4317768812179565,
  "theta_pos_0p5_2_rmse_deg": 1.7384488582611084,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.702552080154419,
  "theta_pos_0p5_2_max_abs_err_deg": 3.9859414100646973,
  "theta_pos_0p5_2_bias_deg": 0.770165205001831,
  "theta_pos_0p5_2_n": 163.0
}
```
