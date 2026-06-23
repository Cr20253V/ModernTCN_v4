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
  "lambda_theta": 0.5,
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
  "lambda_transition_focal": 0.0,
  "lambda_stall_focal": 0.0,
  "lambda_theta_smooth": 0.0,
  "focal_gamma": 2.0,
  "theta_smooth_mode": "off",
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
| acc_main | 0.9553 |
| acc_turn | 0.5203 |
| acc_turn_pure | 0.5288 |
| acc_turn_transition | 0.4829 |
| main_confidence_mean | 0.9797 |
| main_low_conf_0p60_ratio | 0.0117 |
| main_low_conf_0p70_ratio | 0.0208 |
| turn_confidence_mean | 0.6983 |
| turn_low_conf_0p60_ratio | 0.3684 |
| turn_low_conf_0p70_ratio | 0.5272 |
| turn_right_recall | 0.5957 |
| turn_straight_recall | 0.4899 |
| turn_left_recall | 0.5184 |
| theta_mae_deg | 0.8863 |
| theta_abs_le_10_p95_abs_err_deg | 2.3340 |
| theta_neg_10_8_p95_abs_err_deg | 3.5346 |
| theta_pos_8_10_p95_abs_err_deg | 2.7613 |
| theta_abs_le_8_p95_abs_err_deg | 2.2119 |
| theta_neg_8_6_p95_abs_err_deg | 2.2428 |
| theta_pos_6_8_p95_abs_err_deg | 1.9286 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.5804 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.0873 |
| theta_flat_abs_p95_deg | 2.6296 |
| theta_flat_bias_deg | -0.0547 |
| theta_near_flat_abs_p95_deg | 1.6321 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1444 |
| theta_flat_turn_abs_p95_deg | 1.7184 |
| flat_recall | 0.9484 |
| stall_recall | 0.6771 |
| slope_recall | 0.9669 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7368 |
| downhill_recall | 0.8019 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    717,
    0,
    39
  ],
  [
    10,
    65,
    21
  ],
  [
    67,
    24,
    2659
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    476,
    190,
    133
  ],
  [
    457,
    947,
    529
  ],
  [
    135,
    284,
    451
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.299807 |
| test_loss_turn_bundle_base | 0.226606 |
| test_loss_theta_bundle_base | 0.000255 |
| test_loss_transition_focal_raw | 0.882781 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.036887 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 28
- train_seconds: 195.8

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 42 | 0.3810 | 0.5491 |
| [0.60,0.70) | 33 | 0.4545 | 0.6569 |
| [0.70,0.80) | 61 | 0.3607 | 0.7570 |
| [0.80,0.90) | 91 | 0.4286 | 0.8593 |
| [0.90,1.00) | 3375 | 0.0204 | 0.9955 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1327 | 0.6300 | 0.5085 |
| [0.60,0.70) | 572 | 0.5157 | 0.6499 |
| [0.70,0.80) | 545 | 0.4606 | 0.7456 |
| [0.80,0.90) | 474 | 0.3945 | 0.8470 |
| [0.90,1.00) | 684 | 0.2325 | 0.9665 |


## 验证集最佳点

```json
{
  "loss_total": 0.521545546206473,
  "acc_main": 0.937212449255751,
  "acc_turn": 0.5534506089309879,
  "acc_turn_pure": 0.5663716814159292,
  "acc_turn_transition": 0.4922360248447205,
  "false_turn_straight": 0.5602910602910602,
  "flat_recall": 0.9269406392694064,
  "stall_recall": 0.5238095238095238,
  "slope_recall": 0.945260347129506,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9269406392694064,
    0.5238095238095238,
    0.945260347129506
  ],
  "turn_right_recall": 0.6824644549763034,
  "turn_straight_recall": 0.4397089397089397,
  "turn_left_recall": 0.6720604099244876,
  "recall_turn": [
    0.6824644549763034,
    0.4397089397089397,
    0.6720604099244876
  ],
  "cm_turn": [
    [
      576,
      164,
      104
    ],
    [
      577,
      846,
      501
    ],
    [
      137,
      167,
      623
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      609,
      0,
      48
    ],
    [
      0,
      22,
      20
    ],
    [
      140,
      24,
      2832
    ]
  ],
  "main_confidence_mean": 0.9717546753376327,
  "main_confidence_error_mean": 0.8270249681526501,
  "main_low_conf_0p60_ratio": 0.010013531799729363,
  "main_low_conf_0p70_ratio": 0.020838971583220567,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 37,
      "error_rate": 0.5405405405405406,
      "mean_confidence": 0.5480619559908789
    },
    {
      "bin": "[0.60,0.70)",
      "n": 40,
      "error_rate": 0.525,
      "mean_confidence": 0.6450627293092284
    },
    {
      "bin": "[0.70,0.80)",
      "n": 209,
      "error_rate": 0.4354066985645933,
      "mean_confidence": 0.7901309338350759
    },
    {
      "bin": "[0.80,0.90)",
      "n": 96,
      "error_rate": 0.22916666666666666,
      "mean_confidence": 0.8543144846554783
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3313,
      "error_rate": 0.023543616057953517,
      "mean_confidence": 0.9952916293782265
    }
  ],
  "turn_confidence_mean": 0.7201934562586595,
  "turn_confidence_error_mean": 0.6621414316745221,
  "turn_low_conf_0p60_ratio": 0.31610284167794317,
  "turn_low_conf_0p70_ratio": 0.4617050067658999,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 1168,
      "error_rate": 0.5933219178082192,
      "mean_confidence": 0.49979615536139604
    },
    {
      "bin": "[0.60,0.70)",
      "n": 538,
      "error_rate": 0.5074349442379182,
      "mean_confidence": 0.6504330895525696
    },
    {
      "bin": "[0.70,0.80)",
      "n": 611,
      "error_rate": 0.48936170212765956,
      "mean_confidence": 0.7515844818107836
    },
    {
      "bin": "[0.80,0.90)",
      "n": 531,
      "error_rate": 0.4048964218455744,
      "mean_confidence": 0.8545607416242761
    },
    {
      "bin": "[0.90,1.00)",
      "n": 847,
      "error_rate": 0.20070838252656434,
      "mean_confidence": 0.9615466789202767
    }
  ],
  "theta_mae_rad": 0.017289310693740845,
  "theta_mae_deg": 0.9906044602394104,
  "uphill_recall": 0.7638814016172507,
  "downhill_recall": 0.8136818687430478,
  "slope_sign_acc": 0.9698877634820695,
  "theta_flat_mae_deg": 1.0838193893432617,
  "theta_flat_abs_p95_deg": 3.5331878662109375,
  "theta_flat_abs_max_deg": 8.89081859588623,
  "theta_flat_bias_deg": 0.7015299797058105,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.597571611404419,
  "theta_near_flat_abs_p95_deg": 5.102733135223389,
  "theta_near_flat_abs_max_deg": 8.89081859588623,
  "theta_near_flat_bias_deg": 1.258575201034546,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.3677972555160522,
  "theta_flat_turn_abs_p95_deg": 5.065011024475098,
  "theta_flat_turn_abs_max_deg": 8.89081859588623,
  "theta_flat_turn_bias_deg": 0.9646271467208862,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9906044602394104,
  "theta_slope_control_abs_p95_deg": 9.036572456359863,
  "theta_slope_control_abs_max_deg": 11.766403198242188,
  "theta_slope_control_bias_deg": 0.32812345027923584,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.9906045198440552,
  "theta_all_rmse_deg": 1.344252109527588,
  "theta_all_p95_abs_err_deg": 2.669520378112793,
  "theta_all_max_abs_err_deg": 9.390817642211914,
  "theta_all_bias_deg": 0.32812342047691345,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.9701631665229797,
  "theta_active_abs_ge_2_rmse_deg": 1.2684365510940552,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.3591840267181396,
  "theta_active_abs_ge_2_max_abs_err_deg": 8.272912979125977,
  "theta_active_abs_ge_2_bias_deg": 0.24623823165893555,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9809526205062866,
  "theta_abs_le_8_rmse_deg": 1.339064359664917,
  "theta_abs_le_8_p95_abs_err_deg": 2.751824378967285,
  "theta_abs_le_8_max_abs_err_deg": 9.390817642211914,
  "theta_abs_le_8_bias_deg": 0.37413010001182556,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.9906045198440552,
  "theta_abs_le_10_rmse_deg": 1.344252109527588,
  "theta_abs_le_10_p95_abs_err_deg": 2.669520378112793,
  "theta_abs_le_10_max_abs_err_deg": 9.390817642211914,
  "theta_abs_le_10_bias_deg": 0.32812342047691345,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.9516615271568298,
  "theta_pos_8_10_rmse_deg": 1.1375950574874878,
  "theta_pos_8_10_p95_abs_err_deg": 1.8507351875305176,
  "theta_pos_8_10_max_abs_err_deg": 5.573338031768799,
  "theta_pos_8_10_bias_deg": -0.5657277703285217,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 1.112358808517456,
  "theta_neg_10_8_rmse_deg": 1.5643649101257324,
  "theta_neg_10_8_p95_abs_err_deg": 3.007802724838257,
  "theta_neg_10_8_max_abs_err_deg": 8.272912979125977,
  "theta_neg_10_8_bias_deg": 0.8459094762802124,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.7993089556694031,
  "theta_pos_6_8_rmse_deg": 0.9910302758216858,
  "theta_pos_6_8_p95_abs_err_deg": 1.9282307624816895,
  "theta_pos_6_8_max_abs_err_deg": 3.059582233428955,
  "theta_pos_6_8_bias_deg": -0.266988605260849,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.181415319442749,
  "theta_neg_8_6_rmse_deg": 1.4991142749786377,
  "theta_neg_8_6_p95_abs_err_deg": 2.8668556213378906,
  "theta_neg_8_6_max_abs_err_deg": 7.683069229125977,
  "theta_neg_8_6_bias_deg": 0.4054912328720093,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.9845269322395325,
  "theta_neg_4_2_rmse_deg": 1.2551381587982178,
  "theta_neg_4_2_p95_abs_err_deg": 2.3845207691192627,
  "theta_neg_4_2_max_abs_err_deg": 6.280999660491943,
  "theta_neg_4_2_bias_deg": 0.478725403547287,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5474464297294617,
  "theta_neg_2_0p5_rmse_deg": 0.7219418883323669,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.2279490232467651,
  "theta_neg_2_0p5_max_abs_err_deg": 3.868901014328003,
  "theta_neg_2_0p5_bias_deg": 0.21954433619976044,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.045065999031067,
  "theta_pos_0p5_2_rmse_deg": 1.3289304971694946,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.221865653991699,
  "theta_pos_0p5_2_max_abs_err_deg": 3.9198265075683594,
  "theta_pos_0p5_2_bias_deg": 0.5440704226493835,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3049717818287293,
  "loss_turn": 1.0811997333947312,
  "loss_theta": 0.0005506438217255009,
  "loss_main_bundle_base": 0.3049717818287293,
  "loss_turn_bundle_base": 0.21623995154491135,
  "loss_theta_bundle_base": 0.00033381114225816965,
  "loss_main_bundle": 0.3049717818287293,
  "loss_turn_bundle": 0.21623995154491135,
  "loss_theta_bundle": 0.00033381114225816965,
  "loss_theta_flat": 0.00029790655283327624,
  "loss_theta_near_flat": 0.0014082541867286593,
  "loss_theta_error_excess": 0.00018171127123130592,
  "loss_theta_flat_excess": 0.00013003983095317064,
  "loss_theta_near_flat_excess": 0.0010130117644199218,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00013654880506732892,
  "loss_theta_small_neg": 0.0004809384948888438,
  "loss_theta_small_neg_excess": 0.00011968670908884045,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4720101713811593,
  "loss_false_turn_straight": 0.36705154299897336,
  "loss_transition_focal_raw": 0.6958439942787078,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.180955114069787,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
