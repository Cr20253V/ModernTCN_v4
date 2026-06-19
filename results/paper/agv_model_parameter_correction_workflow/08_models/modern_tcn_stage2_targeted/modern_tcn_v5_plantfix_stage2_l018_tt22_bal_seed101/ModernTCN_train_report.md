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
  "lambda_turn": 0.18,
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
    1.35,
    0.85,
    1.35
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 2.2,
  "select_turn_weight": 0.55,
  "select_turn_transition_weight": 1.25,
  "select_turn_transition_target": 0.82,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.88,
  "select_turn_lr_weight": 0.55,
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
| acc_main | 0.9656 |
| acc_turn | 0.5750 |
| acc_turn_pure | 0.5937 |
| acc_turn_transition | 0.4933 |
| main_confidence_mean | 0.9865 |
| main_low_conf_0p60_ratio | 0.0056 |
| main_low_conf_0p70_ratio | 0.0128 |
| turn_confidence_mean | 0.8105 |
| turn_low_conf_0p60_ratio | 0.1780 |
| turn_low_conf_0p70_ratio | 0.2979 |
| turn_right_recall | 0.5732 |
| turn_straight_recall | 0.5732 |
| turn_left_recall | 0.5805 |
| theta_mae_deg | 0.7082 |
| theta_abs_le_10_p95_abs_err_deg | 1.8880 |
| theta_neg_10_8_p95_abs_err_deg | 2.1006 |
| theta_pos_8_10_p95_abs_err_deg | 2.7594 |
| theta_abs_le_8_p95_abs_err_deg | 1.7496 |
| theta_neg_8_6_p95_abs_err_deg | 1.8018 |
| theta_pos_6_8_p95_abs_err_deg | 1.5823 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6966 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.7275 |
| theta_flat_abs_p95_deg | 2.7535 |
| theta_flat_bias_deg | 0.0942 |
| theta_near_flat_abs_p95_deg | 2.3649 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.0735 |
| theta_flat_turn_abs_p95_deg | 2.0904 |
| flat_recall | 0.9563 |
| stall_recall | 0.7188 |
| slope_recall | 0.9767 |
| uphill_recall | 0.7557 |
| downhill_recall | 0.7951 |

- best_epoch: 56
- train_seconds: 622.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 20 | 0.3500 | 0.5458 |
| [0.60,0.70) | 26 | 0.3846 | 0.6527 |
| [0.70,0.80) | 44 | 0.3409 | 0.7688 |
| [0.80,0.90) | 53 | 0.3019 | 0.8535 |
| [0.90,1.00) | 3459 | 0.0220 | 0.9964 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 641 | 0.6115 | 0.5189 |
| [0.60,0.70) | 432 | 0.5046 | 0.6499 |
| [0.70,0.80) | 415 | 0.5807 | 0.7532 |
| [0.80,0.90) | 503 | 0.4493 | 0.8531 |
| [0.90,1.00) | 1611 | 0.2818 | 0.9710 |


## 验证集最佳点

```json
{
  "loss_total": 0.5085147575209363,
  "acc_main": 0.9461434370771312,
  "acc_turn": 0.6246278755074425,
  "acc_turn_pure": 0.6384791871517536,
  "acc_turn_transition": 0.5590062111801242,
  "flat_recall": 0.954337899543379,
  "stall_recall": 0.38095238095238093,
  "slope_recall": 0.9522696929238985,
  "recall_main": [
    0.954337899543379,
    0.38095238095238093,
    0.9522696929238985
  ],
  "turn_right_recall": 0.6350710900473934,
  "turn_straight_recall": 0.5753638253638254,
  "turn_left_recall": 0.7173678532901834,
  "recall_turn": [
    0.6350710900473934,
    0.5753638253638254,
    0.7173678532901834
  ],
  "cm_turn": [
    [
      536,
      214,
      94
    ],
    [
      332,
      1107,
      485
    ],
    [
      78,
      184,
      665
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      627,
      0,
      30
    ],
    [
      0,
      16,
      26
    ],
    [
      132,
      11,
      2853
    ]
  ],
  "main_confidence_mean": 0.9651183770441912,
  "main_confidence_error_mean": 0.7431486039299392,
  "main_low_conf_0p60_ratio": 0.05250338294993234,
  "main_low_conf_0p70_ratio": 0.058186738836265225,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 194,
      "error_rate": 0.4690721649484536,
      "mean_confidence": 0.5236464354964702
    },
    {
      "bin": "[0.60,0.70)",
      "n": 21,
      "error_rate": 0.38095238095238093,
      "mean_confidence": 0.646411934547726
    },
    {
      "bin": "[0.70,0.80)",
      "n": 34,
      "error_rate": 0.23529411764705882,
      "mean_confidence": 0.7488982048877281
    },
    {
      "bin": "[0.80,0.90)",
      "n": 66,
      "error_rate": 0.16666666666666666,
      "mean_confidence": 0.8594065954521045
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3380,
      "error_rate": 0.02396449704142012,
      "mean_confidence": 0.9966766182841561
    }
  ],
  "turn_confidence_mean": 0.8257195885975546,
  "turn_confidence_error_mean": 0.7645827025265837,
  "turn_low_conf_0p60_ratio": 0.16941813261163735,
  "turn_low_conf_0p70_ratio": 0.2706359945872801,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 626,
      "error_rate": 0.5894568690095847,
      "mean_confidence": 0.5352197766576108
    },
    {
      "bin": "[0.60,0.70)",
      "n": 374,
      "error_rate": 0.4893048128342246,
      "mean_confidence": 0.651851325360179
    },
    {
      "bin": "[0.70,0.80)",
      "n": 415,
      "error_rate": 0.4457831325301205,
      "mean_confidence": 0.752120973351633
    },
    {
      "bin": "[0.80,0.90)",
      "n": 522,
      "error_rate": 0.42911877394636017,
      "mean_confidence": 0.8531969902561877
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1758,
      "error_rate": 0.24232081911262798,
      "mean_confidence": 0.9753668208992804
    }
  ],
  "theta_mae_rad": 0.015341331250965595,
  "theta_mae_deg": 0.8789935111999512,
  "uphill_recall": 0.7778975741239892,
  "downhill_recall": 0.8008898776418243,
  "slope_sign_acc": 0.960580344921982,
  "theta_flat_mae_deg": 1.2326511144638062,
  "theta_flat_abs_p95_deg": 3.747323751449585,
  "theta_flat_abs_max_deg": 9.10291862487793,
  "theta_flat_bias_deg": 0.42833346128463745,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.576403260231018,
  "theta_near_flat_abs_p95_deg": 3.8888416290283203,
  "theta_near_flat_abs_max_deg": 9.10291862487793,
  "theta_near_flat_bias_deg": 0.7057687640190125,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.2212101221084595,
  "theta_flat_turn_abs_p95_deg": 4.422366142272949,
  "theta_flat_turn_abs_max_deg": 9.10291862487793,
  "theta_flat_turn_bias_deg": -0.012079406529664993,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8789935111999512,
  "theta_slope_control_abs_p95_deg": 9.337520599365234,
  "theta_slope_control_abs_max_deg": 12.1348295211792,
  "theta_slope_control_bias_deg": 0.3355950713157654,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8789933919906616,
  "theta_all_rmse_deg": 1.2580294609069824,
  "theta_all_p95_abs_err_deg": 2.633680582046509,
  "theta_all_max_abs_err_deg": 8.60291862487793,
  "theta_all_bias_deg": 0.335595041513443,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.8014390468597412,
  "theta_active_abs_ge_2_rmse_deg": 1.1335272789001465,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.280933380126953,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.078789710998535,
  "theta_active_abs_ge_2_bias_deg": 0.3152582347393036,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9231064319610596,
  "theta_abs_le_8_rmse_deg": 1.2910724878311157,
  "theta_abs_le_8_p95_abs_err_deg": 2.709181308746338,
  "theta_abs_le_8_max_abs_err_deg": 8.60291862487793,
  "theta_abs_le_8_bias_deg": 0.35416659712791443,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8789933919906616,
  "theta_abs_le_10_rmse_deg": 1.2580294609069824,
  "theta_abs_le_10_p95_abs_err_deg": 2.633680582046509,
  "theta_abs_le_10_max_abs_err_deg": 8.60291862487793,
  "theta_abs_le_10_bias_deg": 0.335595041513443,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.546480119228363,
  "theta_pos_8_10_rmse_deg": 0.7474538087844849,
  "theta_pos_8_10_p95_abs_err_deg": 1.5016719102859497,
  "theta_pos_8_10_max_abs_err_deg": 3.2953884601593018,
  "theta_pos_8_10_bias_deg": 0.009301161393523216,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8418509364128113,
  "theta_neg_10_8_rmse_deg": 1.3811192512512207,
  "theta_neg_10_8_p95_abs_err_deg": 2.4018383026123047,
  "theta_neg_10_8_max_abs_err_deg": 7.078789710998535,
  "theta_neg_10_8_bias_deg": 0.5094852447509766,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6263734102249146,
  "theta_pos_6_8_rmse_deg": 0.8406282067298889,
  "theta_pos_6_8_p95_abs_err_deg": 1.6038810014724731,
  "theta_pos_6_8_max_abs_err_deg": 3.3954105377197266,
  "theta_pos_6_8_bias_deg": 0.2879922688007355,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.0594741106033325,
  "theta_neg_8_6_rmse_deg": 1.3872417211532593,
  "theta_neg_8_6_p95_abs_err_deg": 2.6352553367614746,
  "theta_neg_8_6_max_abs_err_deg": 6.59104585647583,
  "theta_neg_8_6_bias_deg": 0.7425448298454285,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8278687596321106,
  "theta_neg_4_2_rmse_deg": 1.069100260734558,
  "theta_neg_4_2_p95_abs_err_deg": 1.9224605560302734,
  "theta_neg_4_2_max_abs_err_deg": 5.1703338623046875,
  "theta_neg_4_2_bias_deg": 0.2594628930091858,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.9043530821800232,
  "theta_neg_2_0p5_rmse_deg": 1.177934169769287,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.191999673843384,
  "theta_neg_2_0p5_max_abs_err_deg": 4.440379619598389,
  "theta_neg_2_0p5_bias_deg": -0.06839063763618469,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1546554565429688,
  "theta_pos_0p5_2_rmse_deg": 1.4237060546875,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.2468421459198,
  "theta_pos_0p5_2_max_abs_err_deg": 4.100708484649658,
  "theta_pos_0p5_2_bias_deg": 0.730056881904602,
  "theta_pos_0p5_2_n": 163.0
}
```
