# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
- loss_mode: `uncertainty_weighting`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- vehicle: `diagonal_dual_steer_drive_agv`; active=`LF,RR`; passive=`RF,LR`
- feature_policy: `keep_current_algorithm_inputs_unchanged`
- label_time_policy: `current_window_end`, horizon_steps=0
- split: 使用 MAT 文件已有 run-level split，不重划分。
- scaler: 使用 MAT 文件已有归一化后 X，不重新拟合。
- confidence_policy: `derive_classification_confidence_from_softmax_and_export`
- input: `[batch, time=128, feature=22]`
- output: `logits_main`, `logits_turn`, `theta_hat`

## E2 hard-sample focal settings

- lambda_transition_focal: `0.0`
- lambda_stall_focal: `0.0`
- lambda_theta_smooth: `0.0`
- focal_gamma: `2.0`
- theta_smooth_mode: `off`
- theta_smooth_status: `disabled_contract_limited`

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
  "command_dropout_prob": 0.0,
  "command_dropout_start_index": -1,
  "command_dropout_feature_count": 0,
  "command_dropout_mode": "window_block",
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
  "lambda_theta_flat": 0.2,
  "theta_flat_loss_mode": "near_zero",
  "theta_flat_zero_tol_deg": 0.3,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 0.05,
  "lambda_theta_flat_excess": 0.1,
  "lambda_theta_near_flat_excess": 0.0,
  "lambda_theta_true_zero_excess": 0.1,
  "lambda_theta_active_excess": 0.1,
  "lambda_theta_small_neg": 0.0,
  "lambda_theta_small_neg_excess": 0.0,
  "lambda_turn_release": 0.0,
  "lambda_false_turn_straight": 0.0,
  "lambda_transition_focal": 0.0,
  "lambda_stall_focal": 0.0,
  "lambda_theta_smooth": 0.0,
  "focal_gamma": 2.0,
  "theta_smooth_mode": "off",
  "theta_excess_target_deg": 1.0,
  "theta_flat_excess_target_deg": 0.4,
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
  "select_stall_weight": 0.0,
  "select_stall_target": 0.7,
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
  "select_theta_flat_peak_weight": 1.8,
  "select_theta_flat_peak_target_deg": 4.8,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 0.7,
  "select_theta_edge_p95_target_deg": 1.25,
  "select_theta_small_nonzero_p95_weight": 0.8,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.3,
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9634 |
| acc_turn | 0.5508 |
| acc_turn_pure | 0.5585 |
| acc_turn_transition | 0.5171 |
| main_confidence_mean | 0.9837 |
| main_low_conf_0p60_ratio | 0.0075 |
| main_low_conf_0p70_ratio | 0.0150 |
| turn_confidence_mean | 0.7586 |
| turn_low_conf_0p60_ratio | 0.2340 |
| turn_low_conf_0p70_ratio | 0.3798 |
| turn_right_recall | 0.6596 |
| turn_straight_recall | 0.5215 |
| turn_left_recall | 0.5161 |
| theta_mae_deg | 0.7544 |
| theta_abs_le_10_p95_abs_err_deg | 2.2255 |
| theta_neg_10_8_p95_abs_err_deg | 2.4540 |
| theta_pos_8_10_p95_abs_err_deg | 2.9822 |
| theta_abs_le_8_p95_abs_err_deg | 2.0171 |
| theta_neg_8_6_p95_abs_err_deg | 2.0616 |
| theta_pos_6_8_p95_abs_err_deg | 1.4948 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.9296 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.6651 |
| theta_flat_abs_p95_deg | 3.2158 |
| theta_flat_bias_deg | -0.2130 |
| theta_near_flat_abs_p95_deg | 1.7573 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.0965 |
| theta_flat_turn_abs_p95_deg | 1.5634 |
| flat_recall | 0.9444 |
| stall_recall | 0.7083 |
| slope_recall | 0.9775 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7506 |
| downhill_recall | 0.8065 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    714,
    0,
    42
  ],
  [
    9,
    68,
    19
  ],
  [
    53,
    9,
    2688
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    527,
    182,
    90
  ],
  [
    502,
    1008,
    423
  ],
  [
    194,
    227,
    449
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.319989 |
| test_loss_turn_bundle_base | 0.243455 |
| test_loss_theta_bundle_base | 0.000241 |
| test_loss_transition_focal_raw | 0.910794 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.495320 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 35
- train_seconds: 211.3

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 27 | 0.4444 | 0.5470 |
| [0.60,0.70) | 27 | 0.2963 | 0.6476 |
| [0.70,0.80) | 57 | 0.5439 | 0.7528 |
| [0.80,0.90) | 78 | 0.2308 | 0.8552 |
| [0.90,1.00) | 3413 | 0.0185 | 0.9966 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 843 | 0.5694 | 0.5148 |
| [0.60,0.70) | 525 | 0.5371 | 0.6492 |
| [0.70,0.80) | 633 | 0.5893 | 0.7457 |
| [0.80,0.90) | 520 | 0.4712 | 0.8475 |
| [0.90,1.00) | 1081 | 0.2202 | 0.9666 |


## 验证集最佳点

```json
{
  "loss_total": 0.586723752305698,
  "acc_main": 0.9399188092016239,
  "acc_turn": 0.5959404600811908,
  "acc_turn_pure": 0.6027531956735497,
  "acc_turn_transition": 0.5636645962732919,
  "false_turn_straight": 0.46621621621621623,
  "flat_recall": 0.9604261796042618,
  "stall_recall": 0.2857142857142857,
  "slope_recall": 0.9445927903871829,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.023809523809523808,
  "recall_main": [
    0.9604261796042618,
    0.2857142857142857,
    0.9445927903871829
  ],
  "turn_right_recall": 0.6646919431279621,
  "turn_straight_recall": 0.5337837837837838,
  "turn_left_recall": 0.6623516720604099,
  "recall_turn": [
    0.6646919431279621,
    0.5337837837837838,
    0.6623516720604099
  ],
  "cm_turn": [
    [
      561,
      206,
      77
    ],
    [
      510,
      1027,
      387
    ],
    [
      125,
      188,
      614
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      631,
      0,
      26
    ],
    [
      1,
      12,
      29
    ],
    [
      152,
      14,
      2830
    ]
  ],
  "main_confidence_mean": 0.9652138341832718,
  "main_confidence_error_mean": 0.7571017645649823,
  "main_low_conf_0p60_ratio": 0.05277401894451962,
  "main_low_conf_0p70_ratio": 0.059810554803788905,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 195,
      "error_rate": 0.46153846153846156,
      "mean_confidence": 0.5279870327264067
    },
    {
      "bin": "[0.60,0.70)",
      "n": 26,
      "error_rate": 0.5384615384615384,
      "mean_confidence": 0.6600227133335809
    },
    {
      "bin": "[0.70,0.80)",
      "n": 34,
      "error_rate": 0.3235294117647059,
      "mean_confidence": 0.7515911326209902
    },
    {
      "bin": "[0.80,0.90)",
      "n": 50,
      "error_rate": 0.28,
      "mean_confidence": 0.8636554909076689
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3390,
      "error_rate": 0.02743362831858407,
      "mean_confidence": 0.9963451865263627
    }
  ],
  "turn_confidence_mean": 0.763067609509222,
  "turn_confidence_error_mean": 0.6955796073010942,
  "turn_low_conf_0p60_ratio": 0.2506089309878214,
  "turn_low_conf_0p70_ratio": 0.38673883626522326,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 926,
      "error_rate": 0.5788336933045356,
      "mean_confidence": 0.5023571628126682
    },
    {
      "bin": "[0.60,0.70)",
      "n": 503,
      "error_rate": 0.47912524850894633,
      "mean_confidence": 0.651338677828189
    },
    {
      "bin": "[0.70,0.80)",
      "n": 514,
      "error_rate": 0.4669260700389105,
      "mean_confidence": 0.7521229866982512
    },
    {
      "bin": "[0.80,0.90)",
      "n": 489,
      "error_rate": 0.41513292433537835,
      "mean_confidence": 0.8500042448934031
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1263,
      "error_rate": 0.2161520190023753,
      "mean_confidence": 0.9695054936727554
    }
  ],
  "theta_mae_rad": 0.01551487110555172,
  "theta_mae_deg": 0.8889365792274475,
  "uphill_recall": 0.7628032345013477,
  "downhill_recall": 0.8014460511679644,
  "slope_sign_acc": 0.9742677251574049,
  "theta_flat_mae_deg": 1.162889838218689,
  "theta_flat_abs_p95_deg": 4.012592315673828,
  "theta_flat_abs_max_deg": 6.370279788970947,
  "theta_flat_bias_deg": 0.3853927254676819,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4510254859924316,
  "theta_near_flat_abs_p95_deg": 3.877762794494629,
  "theta_near_flat_abs_max_deg": 7.493710041046143,
  "theta_near_flat_bias_deg": 1.008864402770996,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.122169017791748,
  "theta_flat_turn_abs_p95_deg": 3.8777236938476562,
  "theta_flat_turn_abs_max_deg": 6.370279788970947,
  "theta_flat_turn_bias_deg": 0.5255199670791626,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8889365792274475,
  "theta_slope_control_abs_p95_deg": 9.520950317382812,
  "theta_slope_control_abs_max_deg": 13.039002418518066,
  "theta_slope_control_bias_deg": 0.21180014312267303,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8889365792274475,
  "theta_all_rmse_deg": 1.2776038646697998,
  "theta_all_p95_abs_err_deg": 2.7322449684143066,
  "theta_all_max_abs_err_deg": 7.452818393707275,
  "theta_all_bias_deg": 0.21180012822151184,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.8288607597351074,
  "theta_active_abs_ge_2_rmse_deg": 1.163938045501709,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.4849750995635986,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.452818393707275,
  "theta_active_abs_ge_2_bias_deg": 0.17373259365558624,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.936784029006958,
  "theta_abs_le_8_rmse_deg": 1.3262525796890259,
  "theta_abs_le_8_p95_abs_err_deg": 2.901334524154663,
  "theta_abs_le_8_max_abs_err_deg": 7.452818393707275,
  "theta_abs_le_8_bias_deg": 0.2158232480287552,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8889365792274475,
  "theta_abs_le_10_rmse_deg": 1.2776038646697998,
  "theta_abs_le_10_p95_abs_err_deg": 2.7322449684143066,
  "theta_abs_le_10_max_abs_err_deg": 7.452818393707275,
  "theta_abs_le_10_bias_deg": 0.21180012822151184,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5473224520683289,
  "theta_pos_8_10_rmse_deg": 0.8397690653800964,
  "theta_pos_8_10_p95_abs_err_deg": 1.914886474609375,
  "theta_pos_8_10_max_abs_err_deg": 4.651478290557861,
  "theta_pos_8_10_bias_deg": -0.000705054379068315,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.829271674156189,
  "theta_neg_10_8_rmse_deg": 1.2236639261245728,
  "theta_neg_10_8_p95_abs_err_deg": 2.310882329940796,
  "theta_neg_10_8_max_abs_err_deg": 6.4699554443359375,
  "theta_neg_10_8_bias_deg": 0.39374279975891113,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6407144665718079,
  "theta_pos_6_8_rmse_deg": 0.890813946723938,
  "theta_pos_6_8_p95_abs_err_deg": 1.5038484334945679,
  "theta_pos_6_8_max_abs_err_deg": 4.135991096496582,
  "theta_pos_6_8_bias_deg": -0.0657029002904892,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.9992002844810486,
  "theta_neg_8_6_rmse_deg": 1.3804211616516113,
  "theta_neg_8_6_p95_abs_err_deg": 2.5279037952423096,
  "theta_neg_8_6_max_abs_err_deg": 6.253812789916992,
  "theta_neg_8_6_bias_deg": 0.1552973836660385,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8707723021507263,
  "theta_neg_4_2_rmse_deg": 1.1372934579849243,
  "theta_neg_4_2_p95_abs_err_deg": 2.3245184421539307,
  "theta_neg_4_2_max_abs_err_deg": 5.117969512939453,
  "theta_neg_4_2_bias_deg": -0.02964896708726883,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 1.0057957172393799,
  "theta_neg_2_0p5_rmse_deg": 1.4140480756759644,
  "theta_neg_2_0p5_p95_abs_err_deg": 3.1111011505126953,
  "theta_neg_2_0p5_max_abs_err_deg": 4.528111457824707,
  "theta_neg_2_0p5_bias_deg": -0.46280908584594727,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0713802576065063,
  "theta_pos_0p5_2_rmse_deg": 1.4469921588897705,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.409332513809204,
  "theta_pos_0p5_2_max_abs_err_deg": 4.370676517486572,
  "theta_pos_0p5_2_bias_deg": 0.4625285863876343,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3484203562926859,
  "loss_turn": 1.189660691343883,
  "loss_theta": 0.0004972883889575127,
  "loss_main_bundle_base": 0.3484203562926859,
  "loss_turn_bundle_base": 0.2379321411594809,
  "loss_theta_bundle_base": 0.0003712506798843958,
  "loss_main_bundle": 0.3484203562926859,
  "loss_turn_bundle": 0.2379321411594809,
  "loss_theta_bundle": 0.0003712506798843958,
  "loss_theta_flat": 0.0003015761568333263,
  "loss_theta_near_flat": 0.0012574246614170796,
  "loss_theta_error_excess": 0.00017487018174430072,
  "loss_theta_flat_excess": 0.0001606375752220117,
  "loss_theta_near_flat_excess": 0.0009477144740654234,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00012619560230769095,
  "loss_theta_small_neg": 0.00039168869304950874,
  "loss_theta_small_neg_excess": 8.995926547329242e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.40666217414387507,
  "loss_false_turn_straight": 0.317550798956209,
  "loss_transition_focal_raw": 0.8085747769785508,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.38255451538566,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
